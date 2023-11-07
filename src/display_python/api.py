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
from ..proto.display_pb2 import DisplayBytesRequest, DisplayBytesResponse, WriteStringRequest, WriteStringResponse, DrawLineRequest, DrawLineResponse, ResetRequest, ResetResponse


class Display(ComponentBase):

    SUBTYPE: Final = Subtype("viam-labs", RESOURCE_TYPE_COMPONENT, "display")

    # update with actual API methods
    @abc.abstractmethod
    async def display_bytes(self, data: bytes) -> str:
        ...
    async def write_string(self, x: int, y: int, text: str) -> str:
        ...
    async def draw_line(self, x_1: int, y_1: int, x_2: int, y_2: int) -> str:
        ...
    async def reset(self):
        ...

class DisplayRPCService(DisplayServiceBase, ResourceRPCServiceBase):

    RESOURCE_TYPE = Display

    async def DisplayBytes(self, stream: Stream[DisplayBytesRequest, DisplayBytesResponse]) -> None:
        request = await stream.recv_message()
        assert request is not None
        name = request.name
        service = self.get_resource(name)
        resp = await service.display_bytes(request.data)
        await stream.send_message(DisplayBytesResponse(text=resp))
     
    async def WriteString(self, stream: Stream[WriteStringRequest, WriteStringResponse]) -> None:
        request = await stream.recv_message()
        assert request is not None
        name = request.name
        service = self.get_resource(name)
        resp = await service.write_string(request.x, request.y, request.text)
        await stream.send_message(WriteStringResponse(text=resp))

    async def DrawLine(self, stream: Stream[DrawLineRequest, DrawLineResponse]) -> None:
        request = await stream.recv_message()
        assert request is not None
        name = request.name
        service = self.get_resource(name)
        resp = await service.draw_line(request.x_1, request.y_1, request.x_2, request.y_2)
        await stream.send_message(DrawLineResponse(text=resp))

    async def Reset(self, stream: Stream[ResetRequest, ResetResponse]) -> None:
        request = await stream.recv_message()
        assert request is not None
        name = request.name
        service = self.get_resource(name)
        resp = await service.reset()
        await stream.send_message(ResetResponse(text=resp))

class DisplayClient(Display):

    def __init__(self, name: str, channel: Channel) -> None:
        self.channel = channel
        self.client = DisplayServiceStub(channel)
        super().__init__(name)

    async def display_bytes(self, data: bytes) -> str:
        request = DisplayBytesRequest(name=self.name, data=data)
        response: DisplayBytesResponse = await self.client.DisplayBytes(request)
        return response.text
    
    async def write_string(self, x: int, y: int, text: str) -> str:
        request = WriteStringRequest(name=self.name, x=x, y=y, text=text)
        response: WriteStringResponse = await self.client.WriteString(request)
        return response.text
    
    async def draw_line(self, x_1: int, y_1: int, x_2: int, y_2: int) -> str:
        request = DrawLineRequest(name=self.name, x_1=x_1, y_1=y_1, x_2=x_2, y_2=y_2)
        response: DrawLineResponse = await self.client.DrawLine(request)
        return response.text
    
    async def reset(self) -> str:
        request = ResetRequest(name=self.name)
        response: ResetResponse = await self.client.Reset(request)
        return response.text