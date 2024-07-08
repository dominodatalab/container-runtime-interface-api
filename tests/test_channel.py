from os import environ
from unittest import TestCase
from unittest.mock import patch

import grpc._channel

from cri_api.channel import Channel
from cri_api.exceptions import ServiceException


class TestChannel(TestCase):
    @patch.dict(environ, {}, clear=True)
    def test_from_env_empty(self):
        with self.assertRaisesRegex(ServiceException, "Could not find address"):
            Channel.from_env()

    @patch.dict(environ, {"RUNTIME_SOCK": "unix://my-socket.sock"}, clear=True)
    def test_from_env(self):
        channel = Channel.from_env()
        self.assertIsInstance(channel.channel, grpc._channel.Channel)

    def test_init(self):
        channel = Channel("unix://my-socket.sock")
        self.assertIsInstance(channel.channel, grpc._channel.Channel)
