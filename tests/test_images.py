from unittest import TestCase
from unittest.mock import MagicMock, Mock

from grpc import RpcError, StatusCode

from cri_api.channel import V1, Channel
from cri_api.images import Images, ImageServiceException
from cri_api.v1.api_pb2 import Image, ListImagesRequest, ListImagesResponse


class TestImages(TestCase):
    def setUp(self):
        self.channel = Mock(Channel)
        self.channel.version = V1
        self.channel.channel = MagicMock()

        self.images = Images(self.channel)
        self.images.stub = MagicMock()

    def test_list_images_empty(self):
        self.images.stub.ListImages.return_value = ListImagesResponse()
        self.assertEqual([], self.images.list_images())
        self.images.stub.ListImages.assert_called_with(ListImagesRequest())

    def test_list_images(self):
        self.images.stub.ListImages.return_value = ListImagesResponse(
            images=[Image(id="testing")]
        )
        self.assertEqual([{"id": "testing"}], self.images.list_images())
        self.images.stub.ListImages.assert_called_with(ListImagesRequest())

    def test_list_images_exc(self):
        self.images.stub.ListImages.side_effect = err = RpcError()
        err.code = MagicMock(return_value=StatusCode.UNKNOWN)
        err.details = MagicMock(return_value="these are error details")

        with self.assertRaisesRegex(ImageServiceException, "these are error details"):
            self.images.list_images()

        self.images.stub.ListImages.assert_called_with(ListImagesRequest())
