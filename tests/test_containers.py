from unittest import TestCase
from unittest.mock import MagicMock, Mock

from grpc import RpcError, StatusCode

from cri_api.channel import V1, Channel
from cri_api.containers import Containers, ContainerServiceException
from cri_api.v1.api_pb2 import (
    Container,
    ContainerFilter,
    ContainerState,
    ContainerStateValue,
    ListContainersRequest,
    ListContainersResponse,
)


class TestContainers(TestCase):
    def setUp(self):
        self.channel = Mock(Channel)
        self.channel.version = V1
        self.channel.channel = MagicMock()

        self.containers = Containers(self.channel)
        self.containers.stub = MagicMock()

    def test_list_containers_empty(self):
        self.containers.stub.ListContainers.return_value = ListContainersResponse()
        self.assertEqual([], self.containers.list_containers())
        self.containers.stub.ListContainers.assert_called_with(ListContainersRequest())

    def test_list_containers_filter(self):
        self.containers.stub.ListContainers.return_value = ListContainersResponse()
        self.assertEqual(
            [],
            self.containers.list_containers(
                filter={"state": {"state": "CONTAINER_EXITED"}}
            ),
        )
        self.containers.stub.ListContainers.assert_called_with(
            ListContainersRequest(
                filter=ContainerFilter(
                    state=ContainerStateValue(state=ContainerState.CONTAINER_EXITED)
                )
            )
        )

    def test_list_containers(self):
        self.containers.stub.ListContainers.return_value = ListContainersResponse(
            containers=[Container(id="testing")]
        )
        self.assertEqual([{"id": "testing"}], self.containers.list_containers())
        self.containers.stub.ListContainers.assert_called_with(ListContainersRequest())

    def test_list_containers_exc(self):
        self.containers.stub.ListContainers.side_effect = err = RpcError()
        err.code = MagicMock(return_value=StatusCode.UNKNOWN)
        err.details = MagicMock(return_value="these are error details")

        with self.assertRaisesRegex(
            ContainerServiceException, "these are error details"
        ):
            self.containers.list_containers()

        self.containers.stub.ListContainers.assert_called_with(ListContainersRequest())
