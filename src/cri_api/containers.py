from __future__ import annotations

from typing import List, Optional, Union

from google.protobuf.json_format import MessageToDict, ParseDict
from grpc import RpcError

from .channel import V1, Channel
from .exceptions import ContainerServiceException
from .v1.api_pb2 import (
    ContainerFilter,
    ContainerStatusRequest,
    ListContainersRequest,
    RemoveContainerRequest,
)
from .v1.api_pb2_grpc import RuntimeServiceStub
from .v1alpha2.api_pb2 import ContainerFilter as V1Alpha2ContainerFilter
from .v1alpha2.api_pb2 import ContainerStatusRequest as V1Alpha2ContainerStatusRequest
from .v1alpha2.api_pb2 import ListContainersRequest as V1Alpha2ListContainersRequest
from .v1alpha2.api_pb2 import RemoveContainerRequest as V1Alpha2RemoveContainerRequest
from .v1alpha2.api_pb2_grpc import RuntimeServiceStub as V1Alpha2RuntimeServiceStub


class Containers:
    def __init__(self, channel: Channel) -> None:
        self.channel = channel
        self.stub: Union[RuntimeServiceStub, V1Alpha2RuntimeServiceStub] = (
            RuntimeServiceStub(channel.channel)
            if channel.version == V1
            else V1Alpha2RuntimeServiceStub(channel.channel)
        )

    def list_containers(self, filter: Optional[dict] = None) -> List[dict]:
        if self.channel.version == V1:
            request: Union[ListContainersRequest, V1Alpha2ListContainersRequest] = ListContainersRequest(
                filter=ParseDict(filter, ContainerFilter()) if filter else None
            )
        else:
            request = V1Alpha2ListContainersRequest(
                filter=ParseDict(filter, V1Alpha2ContainerFilter()) if filter else None
            )

        try:
            response = self.stub.ListContainers(request)
            return MessageToDict(response).get("containers", [])
        except RpcError as e:
            raise ContainerServiceException(e.code(), e.details()) from e

    def get_container(self, container_id: str) -> Optional[dict]:
        try:
            response = self.stub.ContainerStatus(
                ContainerStatusRequest(container_id=container_id)
                if self.channel.version == V1
                else V1Alpha2ContainerStatusRequest(container_id=container_id)
            )
            return MessageToDict(response).get("status")
        except RpcError as e:
            raise ContainerServiceException(e.code(), e.details()) from e

    def remove_container(self, container_id: str) -> None:
        try:
            self.stub.RemoveContainer(
                RemoveContainerRequest(container_id=container_id)
                if self.channel.version == V1
                else V1Alpha2RemoveContainerRequest(container_id=container_id)
            )
        except RpcError as e:
            raise ContainerServiceException(e.code(), e.details()) from e
