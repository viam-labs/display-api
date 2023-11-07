# Generated by the Protocol Buffers compiler. DO NOT EDIT!
# source: display.proto
# plugin: grpclib.plugin.main
import abc
import typing

import grpclib.const
import grpclib.client
if typing.TYPE_CHECKING:
    import grpclib.server

import google.api.annotations_pb2
import display_pb2


class DisplayServiceBase(abc.ABC):

    @abc.abstractmethod
    async def DisplayBytes(self, stream: 'grpclib.server.Stream[display_pb2.DisplayBytesRequest, display_pb2.DisplayBytesResponse]') -> None:
        pass

    @abc.abstractmethod
    async def WriteString(self, stream: 'grpclib.server.Stream[display_pb2.WriteStringRequest, display_pb2.WriteStringResponse]') -> None:
        pass

    @abc.abstractmethod
    async def DrawLine(self, stream: 'grpclib.server.Stream[display_pb2.DrawLineRequest, display_pb2.DrawLineResponse]') -> None:
        pass

    @abc.abstractmethod
    async def Reset(self, stream: 'grpclib.server.Stream[display_pb2.ResetRequest, display_pb2.ResetResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {
            '/viamlabs.component.display.v1.DisplayService/DisplayBytes': grpclib.const.Handler(
                self.DisplayBytes,
                grpclib.const.Cardinality.UNARY_UNARY,
                display_pb2.DisplayBytesRequest,
                display_pb2.DisplayBytesResponse,
            ),
            '/viamlabs.component.display.v1.DisplayService/WriteString': grpclib.const.Handler(
                self.WriteString,
                grpclib.const.Cardinality.UNARY_UNARY,
                display_pb2.WriteStringRequest,
                display_pb2.WriteStringResponse,
            ),
            '/viamlabs.component.display.v1.DisplayService/DrawLine': grpclib.const.Handler(
                self.DrawLine,
                grpclib.const.Cardinality.UNARY_UNARY,
                display_pb2.DrawLineRequest,
                display_pb2.DrawLineResponse,
            ),
            '/viamlabs.component.display.v1.DisplayService/Reset': grpclib.const.Handler(
                self.Reset,
                grpclib.const.Cardinality.UNARY_UNARY,
                display_pb2.ResetRequest,
                display_pb2.ResetResponse,
            ),
        }


class DisplayServiceStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.DisplayBytes = grpclib.client.UnaryUnaryMethod(
            channel,
            '/viamlabs.component.display.v1.DisplayService/DisplayBytes',
            display_pb2.DisplayBytesRequest,
            display_pb2.DisplayBytesResponse,
        )
        self.WriteString = grpclib.client.UnaryUnaryMethod(
            channel,
            '/viamlabs.component.display.v1.DisplayService/WriteString',
            display_pb2.WriteStringRequest,
            display_pb2.WriteStringResponse,
        )
        self.DrawLine = grpclib.client.UnaryUnaryMethod(
            channel,
            '/viamlabs.component.display.v1.DisplayService/DrawLine',
            display_pb2.DrawLineRequest,
            display_pb2.DrawLineResponse,
        )
        self.Reset = grpclib.client.UnaryUnaryMethod(
            channel,
            '/viamlabs.component.display.v1.DisplayService/Reset',
            display_pb2.ResetRequest,
            display_pb2.ResetResponse,
        )
