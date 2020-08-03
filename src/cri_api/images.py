from __future__ import annotations

from typing import List, Optional

from google.protobuf.json_format import MessageToDict
from grpc import RpcError

from .channel import Channel
from .exceptions import ImageServiceException
from .v1alpha2.api_pb2 import (
    AuthConfig,
    ImageSpec,
    ImageStatusRequest,
    ListImagesRequest,
    PullImageRequest,
    RemoveImageRequest,
)
from .v1alpha2.api_pb2_grpc import ImageServiceStub


class Images:
    def __init__(self, channel: Channel) -> None:
        self.channel = channel
        self.stub = ImageServiceStub(channel.channel)

    # TODO filter?
    def list_images(self) -> List[dict]:
        try:
            response = self.stub.ListImages(ListImagesRequest())
            return MessageToDict(response).get("images", [])
        except RpcError as e:
            raise ImageServiceException(e.code(), e.details()) from e

    def get_image(self, image_ref: str) -> Optional[dict]:
        image_spec = ImageSpec(image=image_ref)
        try:
            response = self.stub.ImageStatus(ImageStatusRequest(image=image_spec))
            return MessageToDict(response).get("image")
        except RpcError as e:
            raise ImageServiceException(e.code(), e.details()) from e

    def pull_image(self, image_ref: str, auth_config: Optional[AuthConfig] = None) -> None:
        image_spec = ImageSpec(image=image_ref)

        try:
            self.stub.PullImage(PullImageRequest(image=image_spec, auth=auth_config))
        except RpcError as e:
            raise ImageServiceException(e.code(), e.details()) from e

    def remove_image(self, image_ref: str) -> None:
        image_spec = ImageSpec(image=image_ref)

        try:
            self.stub.RemoveImage(RemoveImageRequest(image=image_spec))
        except RpcError as e:
            raise ImageServiceException(e.code(), e.details()) from e
