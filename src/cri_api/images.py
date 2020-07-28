from __future__ import annotations

from typing import List, Optional

from grpc import RpcError, StatusCode

from .channel import Channel
from .pkg.apis.runtime.v1alpha2.api_pb2 import (AuthConfig, Image, ImageSpec, ImageStatusRequest,
                                                ListImagesRequest, PullImageRequest, RemoveImageRequest)
from .pkg.apis.runtime.v1alpha2.api_pb2_grpc import ImageServiceStub


class ImageServiceException(Exception):
    def __init__(self, status_code: StatusCode, details: str):
        super().__init__(details)
        self.status_code = status_code


class Images:
    def __init__(self, channel: Channel) -> None:
        self.channel = channel
        self.stub = ImageServiceStub(channel.channel)

    # TODO filter?
    def list_images(self) -> List[Image]:
        try:
            response = self.stub.ListImages(ListImagesRequest())
            return response.images
        except RpcError as e:
            raise ImageServiceException(e.code(), e.details()) from e

    def get_image(self, image_ref: str) -> Image:
        image_spec = ImageSpec(image=image_ref)
        try:
            response = self.stub.ImageStatus(ImageStatusRequest(image=image_spec))
            return response.image
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