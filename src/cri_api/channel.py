from __future__ import annotations

from functools import cached_property
from os import getenv

from grpc import RpcError, StatusCode, insecure_channel

from .exceptions import ServiceException

V1 = "v1"
V1Alpha2 = "v1alpha2"


class Channel:
    @classmethod
    def from_env(cls) -> Channel:
        sock = getenv("RUNTIME_SOCK")
        if not sock:
            raise ServiceException("Could not find address in RUNTIME_SOCK")

        return Channel(sock)

    def __init__(self, address: str) -> None:
        self.channel = insecure_channel(address)

    @cached_property
    def version(self) -> str:
        if (api_version := getenv("CRI_API_VERSION")) in [V1, V1Alpha2]:
            return api_version

        from .v1.api_pb2 import VersionRequest as VersionRequestV1
        from .v1.api_pb2_grpc import RuntimeServiceStub as RuntimeServiceStubV1
        from .v1alpha2.api_pb2 import VersionRequest as VersionRequestV1Alpha2
        from .v1alpha2.api_pb2_grpc import (
            RuntimeServiceStub as RuntimeServiceStubV1Alpha2,
        )

        try:
            RuntimeServiceStubV1(self.channel).Version(VersionRequestV1())
            return V1
        except RpcError as e:
            if e.code() != StatusCode.UNIMPLEMENTED:
                raise e

        try:
            RuntimeServiceStubV1Alpha2(self.channel).Version(VersionRequestV1Alpha2())
            return V1Alpha2
        except RpcError as e:
            if e.code() != StatusCode.UNIMPLEMENTED:
                raise e

        return V1Alpha2
