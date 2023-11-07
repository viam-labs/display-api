"""
This file outlines the general structure for the API around a custom, modularized component.

It defines the abstract class definition that all concrete implementations must follow,
the gRPC service that will handle calls to the service,
and the gRPC client that will be able to make calls to this service.

In this example, the ``Display`` abstract class defines what functionality is required for all Display components.
It extends ``ComponentBase``, as all component types must.
It also defines its specific ``SUBTYPE``, which is used internally to keep track of supported types.

The ``DisplayRPCService`` implements the gRPC service for the Display component. This will allow other robots and clients to make
requests of the Display component. It extends both from ``DisplayServiceBase`` and ``RPCServiceBase``.
The former is the gRPC service as defined by the proto, and the latter is the class that all gRPC services must inherit from.

Finally, the ``DisplayClient`` is the gRPC client for a Display component. It inherits from DisplayService since it implements
 all the same functions. The implementations are simply gRPC calls to some remote Display component.

To see how this custom modular component is registered, see the __init__.py file.
To see the custom implementation of this component, see the luma-oled.py file.
"""

import abc
from typing import Final, Sequence

from grpclib.client import Channel
from grpclib.server import Stream

from viam.resource.rpc_service_base import ResourceRPCServiceBase
from viam.resource.types import RESOURCE_TYPE_COMPONENT, Subtype
from viam.components.component_base import ComponentBase

from ..proto.display_grpc import DisplayServiceBase, DisplayServiceStub

# update the below with actual methods for your API!
from ..proto.display_pb2 import EchoRequest, EchoResponse


class Display(ComponentBase):

    SUBTYPE: Final = Subtype("viam-labs", RESOURCE_TYPE_COMPONENT, "display")

    # update with actual API methods
    @abc.abstractmethod
    async def echo(self, text: str) -> str:
        ...

class DisplayRPCService(DisplayServiceBase, ResourceRPCServiceBase):

    RESOURCE_TYPE = Display

    # update with actual API methods
    async def Echo(self, stream: Stream[EchoRequest, EchoResponse]) -> None:
        request = await stream.recv_message()
        assert request is not None
        name = request.name
        service = self.get_resource(name)
        resp = await service.say(request.text)
        await stream.send_message(EchoResponse(text=resp))

class DisplayClient(Display):

    def __init__(self, name: str, channel: Channel) -> None:
        self.channel = channel
        self.client = DisplayServiceStub(channel)
        super().__init__(name)

    # update with actual API methods
    async def echo(self, text: str) -> str:
        request = EchoRequest(name=self.name, text=text)
        response: EchoResponse = await self.client.Echo(request)
        return response.text