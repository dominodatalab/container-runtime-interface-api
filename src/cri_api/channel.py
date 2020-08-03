from __future__ import annotations

from os import getenv

from grpc import insecure_channel

from .exceptions import ServiceException


class Channel:
    @classmethod
    def from_env(cls) -> Channel:
        sock = getenv("RUNTIME_SOCK")
        if not sock:
            raise ServiceException("Could not find address in RUNTIME_SOCK")

        return Channel(sock)

    def __init__(self, address: str) -> None:
        self.channel = insecure_channel(address)
