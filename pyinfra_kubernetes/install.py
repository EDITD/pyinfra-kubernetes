from pyinfra.api import deploy, DeployError
from pyinfra.modules import files, server

from .defaults import DEFAULTS

SERVER_BINARIES = [
    'kube-apiserver',
    'kube-scheduler',
    'kube-controller-manager',
]


@deploy('Install Kubernetes', data_defaults=DEFAULTS)
def install_kubernetes(state, host, components=None):
    if not isinstance(components, (list, tuple)):
        raise TypeError('Invalid components of Kubernetes specified to download.')

    if not host.data.kubernetes_version:
        raise DeployError(
            'No kubernetes_version set for this host, refusing to install Kubernetes!',
        )

    files.directory(
        state, host,
        {'Ensure the Kubernetes install directory exists'},
        '{{ host.data.kubernetes_install_dir }}//{{ host.data.kubernetes_version }}',
    )

    files.directory(
        state, host,
        {'Ensure the Kubernetes environment directory exists'},
        host.data.kubernetes_conf_dir,
    )

    kube_type = (
        'server' if any(
            b in components for b in SERVER_BINARIES
        ) else 'node'
    )

    host.data.kubernetes_version_name = (
        'kubernetes-{0}-linux-'
        'amd64' if host.fact.arch == 'x86_64' else host.fact.arch
    ).format(kube_type)

    host.data.kubernetes_temp_filename = state.get_temp_filename(
        'kubernetes-{0}'.format(host.data.kubernetes_version),
    )

    download_kubernetes = files.download(
        state, host,
        {'Download Kubernetes'},
        (
            '{{ host.data.kubernetes_download_base_url }}/'
            '{{ host.data.kubernetes_version }}/'
            '{{ host.data.kubernetes_version_name }}.tar.gz'
        ),
        '{{ host.data.kubernetes_temp_filename }}',
    )

    server.shell(
        state, host,
        {'Extract Kubernetes'},
        '''
        tar -xzf {{ host.data.kubernetes_temp_filename }} \
        -C {{ host.data.kubernetes_install_dir }}/{{ host.data.kubernetes_version }} \
        --strip-components 1
        ''',
        when=download_kubernetes.changed,
    )

    for binary in components:
        files.link(
            state, host,
            {'Symlink {0} to {1}'.format(binary, host.data.kubernetes_bin_dir)},
            '{{ host.data.kubernetes_bin_dir }}/%s' % binary,  # link
            '{{ host.data.kubernetes_install_dir }}/{{ host.data.kubernetes_version }}/%s/bin/%s' % (kube_type, binary),
        )
