DEFAULTS = {
    # Install
    'kubernetes_version': None,  # must be provided
    'kubernetes_download_base_url': 'https://dl.k8s.io',
    'kubernetes_install_dir': '/usr/local/kubernetes',
    'kubernetes_bin_dir': '/usr/local/bin',
    'kubernetes_conf_dir': '/etc/kubernetes',

    # Config
    'kubernetes_service_cidr': None,  # must be provided
    'kubernetes_master_url': 'http://127.0.0.1',
}
