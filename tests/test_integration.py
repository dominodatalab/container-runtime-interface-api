from os import getenv
from unittest import TestCase, skipUnless

from cri_api.channel import Channel
from cri_api.containers import Containers
from cri_api.images import Images


@skipUnless(
    getenv("RUNTIME_SOCK"), "RUNTIME_SOCK is not configured for integration testing"
)
class TestCRI(TestCase):
    def test_list_images(self):
        channel = Channel.from_env()
        images = Images(channel)

        images.pull_image("busybox")

        self.assertNotEqual([], images.list_images())

    def test_list_containers(self):
        channel = Channel.from_env()
        containers = Containers(channel)

        self.assertNotEqual([], containers.list_containers())
