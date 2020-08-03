from __future__ import annotations

from typing import List, Optional

from google.protobuf.json_format import MessageToDict
from grpc import RpcError

from .channel import Channel
from .exceptions import ContainerServiceException
from .v1alpha2.api_pb2 import ContainerFilter, ContainerStatusRequest, ListContainersRequest, RemoveContainerRequest
from .v1alpha2.api_pb2_grpc import RuntimeServiceStub


class Containers:
    def __init__(self, channel: Channel) -> None:
        self.channel = channel
        self.stub = RuntimeServiceStub(channel.channel)

    def list_containers(self, filter: Optional[ContainerFilter] = None) -> List[dict]:
        try:
            response = self.stub.ListContainers(ListContainersRequest(filter=filter))
            return MessageToDict(response).get("containers", [])
        except RpcError as e:
            raise ContainerServiceException(e.code(), e.details()) from e

    def get_container(self, container_id: str) -> Optional[dict]:
        try:
            response = self.stub.ContainerStatus(ContainerStatusRequest(container_id=container_id))
            return MessageToDict(response).get("status")
        except RpcError as e:
            raise ContainerServiceException(e.code(), e.details()) from e

    def remove_container(self, container_id: str) -> None:
        try:
            self.stub.RemoveContainer(RemoveContainerRequest(container_id=container_id))
        except RpcError as e:
            raise ContainerServiceException(e.code(), e.details()) from e
