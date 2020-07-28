from __future__ import annotations

from typing import List, Optional

from google.protobuf.json_format import MessageToDict
from grpc import RpcError, StatusCode

from .channel import Channel
from .pkg.apis.runtime.v1alpha2.api_pb2 import (Container, ContainerFilter, ContainerStatus, ContainerStatusRequest,
                                                ListContainersRequest, RemoveContainerRequest)
from .pkg.apis.runtime.v1alpha2.api_pb2_grpc import RuntimeServiceStub


class ContainerServiceException(Exception):
    def __init__(self, status_code: StatusCode, details: str):
        super().__init__(details)
        self.status_code = status_code


class Containers:
    def __init__(self, channel: Channel) -> None:
        self.channel = channel
        self.stub = RuntimeServiceStub(channel.channel)

    def list_containers(self, filter: Optional[ContainerFilter] = None) -> List[Container]:
        try:
            response = self.stub.ListContainers(ListContainersRequest(filter=filter))
            return MessageToDict(response).get("containers", [])
        except RpcError as e:
            raise ContainerServiceException(e.code(), e.details()) from e

    def get_container(self, container_id: str) -> Optional[ContainerStatus]:
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
