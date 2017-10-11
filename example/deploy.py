from pyinfra import inventory, state

from pyinfra_docker import deploy_docker
from pyinfra_etcd import deploy_etcd
from pyinfra_kubernetes import deploy_kubernetes_master, deploy_kubernetes_node

SUDO = True
FAIL_PERCENT = 0


def get_etcd_nodes():
    return [
        'http://{0}:2379'.format(
            etcd_node.fact.network_devices[etcd_node.data.etcd_interface]
            ['ipv4']['address'],
        )
        for etcd_node in inventory.get_group('etcd_nodes')
    ]


# Install/configure etcd cluster
with state.limit('etcd_nodes'):
    deploy_etcd()


# Install/configure the masters (apiserver, controller, scheduler)
with state.limit('kubernetes_masters'):
    deploy_kubernetes_master(etcd_nodes=get_etcd_nodes())


# Install/configure the nodes
with state.limit('kubernetes_nodes'):
    # Install Docker
    deploy_docker(config={
        # Make Docker use the Vagrant provided interface which has it's own /24
        'bip': '{{ host.fact.network_devices[host.data.network_interface].ipv4.address }}/24',
    })

    # Install Kubernetes node components (kubelet, kube-proxy)
    first_master = inventory.get_group('kubernetes_masters')[0]

    deploy_kubernetes_node(
        master_address='http://{0}'.format((
            first_master
            .fact.network_devices[first_master.data.network_interface]
            ['ipv4']['address']
        )),
    )
