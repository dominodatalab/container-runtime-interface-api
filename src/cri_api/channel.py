from __future__ import annotations

from os import getenv

from grpc import insecure_channel


class Channel:
    @classmethod
    def from_env(cls) -> Channel:
        return Channel(getenv("RUNTIME_SOCK"))

    def __init__(self, address: str) -> None:
        self.channel = insecure_channel(address)
