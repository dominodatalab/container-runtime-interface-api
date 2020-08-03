from unittest import TestCase
from unittest.mock import MagicMock, Mock

from cri_api import (
    Container,
    ContainerFilter,
    ContainerState,
    ContainerStateValue,
    ListContainersRequest,
    ListContainersResponse,
)
from cri_api.channel import Channel
from cri_api.containers import Containers, ContainerServiceException
from grpc import RpcError, StatusCode


class TestContainers(TestCase):
    def setUp(self):
        self.channel = Mock(Channel)
        self.channel.channel = MagicMock()

        self.containers = Containers(self.channel)
        self.containers.stub = MagicMock()

    def test_list_containers_empty(self):
        self.containers.stub.ListContainers.return_value = ListContainersResponse()
        self.assertEqual([], self.containers.list_containers())
        self.containers.stub.ListContainers.assert_called_with(ListContainersRequest())

    def test_list_containers_filter(self):
        self.containers.stub.ListContainers.return_value = ListContainersResponse()
        filt = ContainerFilter(state=ContainerStateValue(state=ContainerState.CONTAINER_EXITED))
        self.assertEqual([], self.containers.list_containers(filter=filt))
        self.containers.stub.ListContainers.assert_called_with(ListContainersRequest(filter=filt))

    def test_list_containers(self):
        self.containers.stub.ListContainers.return_value = ListContainersResponse(containers=[Container(id="testing")])
        self.assertEqual([{"id": "testing"}], self.containers.list_containers())
        self.containers.stub.ListContainers.assert_called_with(ListContainersRequest())

    def test_list_containers_exc(self):
        self.containers.stub.ListContainers.side_effect = err = RpcError()
        err.code = MagicMock(return_value=StatusCode.UNKNOWN)
        err.details = MagicMock(return_value="these are error details")

        with self.assertRaisesRegex(ContainerServiceException, "these are error details"):
            self.containers.list_containers()

        self.containers.stub.ListContainers.assert_called_with(ListContainersRequest())
