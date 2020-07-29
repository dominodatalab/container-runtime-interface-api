## container-runtime-interface-api

Python library for communication with the Kubernetes [Container Runtime Interface API](https://github.com/kubernetes/cri-api).

### Usage

Install `container-runtime-interface-api` with `pipenv` or `pip`:

```shell
$ pipenv install container-runtime-interface-api
Adding container-runtime-interface-api to Pipfile's [packages]…
✔ Installation Succeeded
...
```

This project currently supports Python 3.8+.

#### Connection

Connection to the CRI API is generally done through a UNIX socket, but any gRPC address supported by [insecure_channel](https://grpc.github.io/grpc/python/grpc.html#grpc.insecure_channel) will work.

```python
from cri_api.channel import Channel
channel = Channel.from_env() # Loads from RUNTIME_SOCK
channel = Channel("unix:///var/run/dockershim.sock") # Explicit argument
```

#### Images

The `Images` class is a thin wrapper around the existing ImageService API:

```python
from cri_api.images import Images

channel = Channel.from_env()
images = Images(channel)

images.list_images()
images.pull_image("busybox")

busybox_images = [i["id"] for i in images.list_images() if any("busybox" in r for r in i["repoTags"])]
[images.remove_image(i) for i in busybox_images]
```

#### Containers

The `Containers` class is a thin wrapper around the existing RuntimeService API:

```python
from cri_api.images import Images
from cri_api import ContainerFilter, ContainerState, ContainerStateValue

channel = Channel.from_env()
images = Containers(channel)

containers.list_containers()
containers.list_containers(ContainerFilter(state=ContainerStateValue(state=ContainerState.CONTAINER_EXITED)))

containers.get_container("9d81052cc027a1fb2ec61b898ea0fd6fc88216ce730ad75f4c52b29849cb440f")
```

#### Raw

Raw access to the underlying CRI API objects can be done by importing from `cri_api`:

```python
from os import getenv
from grpc import insecure_channel
from cri_api import RuntimeServiceStub, ListContainersRequest

stub = RuntimeServiceStub(insecure_channel(getenv("RUNTIME_SOCK")))
response = stub.ListContainers(ListContainersRequest())
containers = response.containers
```

### Updating Protobuf Python Generated Code

```shell
$ bin/update-protos.sh
```

Commit & create a new pull request!

### Development

Interactive development on MacOS can be done by leveraging [minikube](https://kubernetes.io/docs/tasks/tools/install-minikube/):

```shell
$ minikube start --container-runtime=cri-o
$ minikube ssh
$ socat -d -d TCP4-LISTEN:15432,fork UNIX-CONNECT:/var/run/crio/crio.sock

# In another window, you can now connect on $(minikube ip):15432
$ export RUNTIME_SOCK=$(minikube ip):15432
...
```
