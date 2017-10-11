from pyinfra.api import deploy

from .configure import configure_kubeconfig, configure_kubernetes_component
from .install import install_kubernetes


@deploy('Deploy Kubernetes master')
def deploy_kubernetes_master(
    state, host,
    etcd_nodes,
    kube_apiserver_kwargs=None,
    kube_scheduler_kwargs=None,
    kube_controller_manager_kwargs=None,
):
    # Install server components
    install_kubernetes(
        state, host,
        components=(
            'kube-apiserver', 'kube-scheduler', 'kube-controller-manager',
        ),
    )

    # Configure the API server, passing in our etcd nodes
    configure_kubernetes_component(
        state, host,
        'kube-apiserver',
        etcd_nodes=etcd_nodes,
        service_kwargs=kube_apiserver_kwargs,
    )

    # Setup the kube-scheduler service/config
    configure_kubernetes_component(
        state, host,
        'kube-scheduler',
        service_kwargs=kube_scheduler_kwargs,
    )

    # Setup the kube-controller-manager service/config
    configure_kubernetes_component(
        state, host,
        'kube-controller-manager',
        service_kwargs=kube_controller_manager_kwargs,
    )


@deploy('Deploy Kubernetes node')
def deploy_kubernetes_node(
    state, host,
    master_address,
    kubelet_kwargs=None,
    kube_proxy_kwargs=None,
):
    # Install node components
    install_kubernetes(
        state, host,
        components=(
            'kubelet', 'kube-proxy',
        ),
    )

    # Setup the kubeconfig for kubelet & kube-proxy to use
    configure_kubeconfig(
        state, host,
        master_address,
    )

    # Setup the kubelet service/config
    configure_kubernetes_component(
        state, host,
        'kubelet',
        service_kwargs=kubelet_kwargs,
    )

    # Setup the kube-proxy service/config
    configure_kubernetes_component(
        state, host,
        'kube-proxy',
        service_kwargs=kube_proxy_kwargs,
    )
