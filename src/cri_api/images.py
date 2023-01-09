from __future__ import annotations

from typing import List, Optional, Union

from google.protobuf.json_format import MessageToDict, ParseDict
from grpc import RpcError

from .channel import V1, Channel
from .exceptions import ImageServiceException
from .v1.api_pb2 import (
    AuthConfig,
    ImageSpec,
    ImageStatusRequest,
    ListImagesRequest,
    PullImageRequest,
    RemoveImageRequest,
)
from .v1.api_pb2_grpc import ImageServiceStub
from .v1alpha2.api_pb2 import AuthConfig as V1Alpha2AuthConfig
from .v1alpha2.api_pb2 import ImageSpec as V1Alpha2ImageSpec
from .v1alpha2.api_pb2 import ImageStatusRequest as V1Alpha2ImageStatusRequest
from .v1alpha2.api_pb2 import ListImagesRequest as V1Alpha2ListImagesRequest
from .v1alpha2.api_pb2 import PullImageRequest as V1Alpha2PullImageRequest
from .v1alpha2.api_pb2 import RemoveImageRequest as V1Alpha2RemoveImageRequest
from .v1alpha2.api_pb2_grpc import ImageServiceStub as V1Alpha2ImageServiceStub


class Images:
    def __init__(self, channel: Channel) -> None:
        self.channel = channel
        self.stub: Union[ImageServiceStub, V1Alpha2ImageServiceStub] = (
            ImageServiceStub(channel.channel) if channel.version == V1 else V1Alpha2ImageServiceStub(channel.channel)
        )

    # TODO filter?
    def list_images(self) -> List[dict]:
        try:
            response = self.stub.ListImages(
                ListImagesRequest() if self.channel.version == V1 else V1Alpha2ListImagesRequest()
            )
            return MessageToDict(response).get("images", [])
        except RpcError as e:
            raise ImageServiceException(e.code(), e.details()) from e

    def get_image(self, image_ref: str) -> Optional[dict]:
        if self.channel.version == V1:
            request: Union[ImageStatusRequest, V1Alpha2ImageStatusRequest] = ImageStatusRequest(
                image=ImageSpec(image=image_ref)
            )
        else:
            request = V1Alpha2ImageStatusRequest(image=V1Alpha2ImageSpec(image=image_ref))

        try:
            response = self.stub.ImageStatus(request)
            return MessageToDict(response).get("image")
        except RpcError as e:
            raise ImageServiceException(e.code(), e.details()) from e

    def pull_image(self, image_ref: str, auth_config: Optional[dict] = None) -> None:
        if self.channel.version == V1:
            request: Union[PullImageRequest, V1Alpha2PullImageRequest] = PullImageRequest(
                image=ImageSpec(image=image_ref), auth=ParseDict(auth_config, AuthConfig()) if auth_config else None
            )
        else:
            request = V1Alpha2PullImageRequest(
                image=V1Alpha2ImageSpec(image=image_ref),
                auth=ParseDict(auth_config, V1Alpha2AuthConfig()) if auth_config else None,
            )

        try:
            self.stub.PullImage(request)
        except RpcError as e:
            raise ImageServiceException(e.code(), e.details()) from e

    def remove_image(self, image_ref: str) -> None:
        if self.channel.version == V1:
            request: Union[RemoveImageRequest, V1Alpha2RemoveImageRequest] = RemoveImageRequest(
                image=ImageSpec(image=image_ref)
            )
        else:
            request = V1Alpha2RemoveImageRequest(image=V1Alpha2ImageSpec(image=image_ref))

        try:
            self.stub.RemoveImage(request)
        except RpcError as e:
            raise ImageServiceException(e.code(), e.details()) from e
