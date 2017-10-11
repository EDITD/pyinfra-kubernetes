from pyinfra.api import deploy

from .configure import configure_kubeconfig, configure_kubernetes_component
from .install import install_kubernetes


@deploy('Deploy Kubernetes master')
def deploy_kubernetes_master(
    state, host,
    etcd_nodes,
):
    # Install server components
    install_kubernetes(components=(
        'kube-apiserver', 'kube-scheduler', 'kube-controller-manager',
    ))

    # Configure the API server, passing in our etcd nodes
    configure_kubernetes_component('kube-apiserver', etcd_nodes=etcd_nodes)

    configure_kubernetes_component('kube-scheduler')
    configure_kubernetes_component('kube-controller-manager')


@deploy('Deploy Kubernetes node')
def deploy_kubernetes_node(
    state, host,
    master_address,
):
    # Install node components
    install_kubernetes(components=(
        'kubelet', 'kube-proxy',
    ))

    # Setup the kubeconfig for kubelet & kube-proxy to use
    configure_kubeconfig(master_address)

    configure_kubernetes_component('kubelet')
    configure_kubernetes_component('kube-proxy')
