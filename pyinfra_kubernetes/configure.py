from pyinfra.api import deploy
from pyinfra.modules import files, init

from .defaults import DEFAULTS
from .util import get_template_path


def make_service_kwargs(service_kwargs):
    return '\n'.join(
        '    --{0}={1} \\'.format(key, value)
        for key, value in service_kwargs.items()
    )


@deploy('Configure kubeconfig', data_defaults=DEFAULTS)
def configure_kubeconfig(state, host, master_address, filename='kubeconfig.yml'):
    files.template(
        state, host,
        {'Upload kubeconfig'},
        get_template_path('kubeconfig.yml.j2'),
        '{{ host.data.kubernetes_conf_dir }}/%s' % filename,
        master_address=master_address,
    )


@deploy('Configure Kubernetes', data_defaults=DEFAULTS)
def configure_kubernetes_component(
    state, host, component,
    enable_service=True,
    **template_data
):
    generate_service = files.template(
        state, host,
        {'Upload the {0} systemd unit file'.format(component)},
        get_template_path('{0}.service.j2'.format(component)),
        '/etc/systemd/system/{0}.service'.format(component),
    )

    generate_config = files.template(
        state, host,
        {'Upload the {0} env file'.format(component)},
        get_template_path('{0}.conf.j2'.format(component)),
        '{{ host.data.kubernetes_conf_dir }}/%s' % component,
        make_service_kwargs=make_service_kwargs,
        **template_data
    )

    # Start (/enable) the service
    op_name = 'Ensure {0} service is running'.format(component)
    if enable_service:
        op_name = '{0} and enabled'.format(op_name)

    init.systemd(
        state, host,
        {op_name},
        component,
        enabled=enable_service,
        restarted=generate_config.changed,
        daemon_reload=generate_service.changed,
    )
