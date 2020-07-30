from cri_api import ContainerFilter, ContainerState, ContainerStateValue
from cri_api.channel import Channel
from cri_api.containers import Containers

channel = Channel.from_env()
containers = Containers(channel)

print(containers.list_containers())
print(containers.list_containers(ContainerFilter(label_selector={"io.kubernetes.container.name": "etcd"})))
print(containers.list_containers(ContainerFilter(state=ContainerStateValue(state=ContainerState.CONTAINER_EXITED))))
print(containers.get_container("9d81052cc027a1fb2ec61b898ea0fd6fc88216ce730ad75f4c52b29849cb440f"))
print(containers.get_container("718fe644d9b2b9fdb3d55f44c994b20099c2d2e8dace0ab8a78c4dd9c3ca5c50"))
