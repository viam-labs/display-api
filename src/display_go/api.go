// Package display implements the viam-labs.components.display API
package display

import (
	"context"

	"github.com/edaniels/golog"
	"go.viam.com/utils/rpc"

	pb "github.com/viam-labs/display-api/src/display_go/grpc"
	"go.viam.com/rdk/resource"
	"go.viam.com/rdk/robot"
)

// API is the full API definition.
var API = resource.APINamespace("viam-labs").WithServiceType("display")

// Named is a helper for getting the named Display's typed resource name.
func Named(name string) resource.Name {
	return resource.NewName(API, name)
}

// FromRobot is a helper for getting the named Display from the given Robot.
func FromRobot(r robot.Robot, name string) (Display, error) {
	return robot.ResourceFromRobot[Display](r, Named(name))
}

func init() {
	resource.RegisterAPI(API, resource.APIRegistration[Display]{
		// Reconfigurable, and contents of reconfwrapper.go are only needed for standalone (non-module) uses.
		RPCServiceServerConstructor: NewRPCServiceServer,
		RPCServiceHandler:           pb.RegisterDisplayServiceHandlerFromEndpoint,
		RPCServiceDesc:              &pb.DisplayService_ServiceDesc,
		RPCClient: func(
			ctx context.Context,
			conn rpc.ClientConn,
			remoteName string,
			name resource.Name,
			logger golog.Logger,
		) (Display, error) {
			return NewClientFromConn(conn, remoteName, name, logger), nil
		},
	})
}

// Display defines the Go interface for the component (should match the protobuf methods.)
type Display interface {
	resource.Resource
	// replace with actual methods!
	Echo(ctx context.Context, text string) error
}

// serviceServer implements the Display RPC service from display.proto.
type serviceServer struct {
	pb.UnimplementedDisplayServiceServer
	coll resource.APIResourceCollection[Display]
}

// NewRPCServiceServer returns a new RPC server for the Display API.
func NewRPCServiceServer(coll resource.APIResourceCollection[Display]) interface{} {
	return &serviceServer{coll: coll}
}

// replace with methods that match your proto!
func (s *serviceServer) Echo(ctx context.Context, req *pb.EchoRequest) (*pb.EchoResponse, error) {
	g, err := s.coll.Resource(req.Name)
	if err != nil {
		return nil, err
	}
	err = g.Echo(ctx, req.Text)
	if err != nil {
		return nil, err
	}
	return &pb.EchoResponse{}, nil
}

// NewClientFromConn creates a new Display RPC client from an existing connection.
func NewClientFromConn(conn rpc.ClientConn, remoteName string, name resource.Name, logger golog.Logger) Display {
	sc := newSvcClientFromConn(conn, remoteName, name, logger)
	return clientFromSvcClient(sc, name.ShortName())
}

func newSvcClientFromConn(conn rpc.ClientConn, remoteName string, name resource.Name, logger golog.Logger) *serviceClient {
	client := pb.NewDisplayServiceClient(conn)
	sc := &serviceClient{
		Named:  name.PrependRemote(remoteName).AsNamed(),
		client: client,
		logger: logger,
	}
	return sc
}

type serviceClient struct {
	resource.Named
	resource.AlwaysRebuild
	resource.TriviallyCloseable
	client pb.DisplayServiceClient
	logger golog.Logger
}

// client is an Display client.
type client struct {
	*serviceClient
	name string
}

func clientFromSvcClient(sc *serviceClient, name string) Display {
	return &client{sc, name}
}

// replace with actual methods that match your proto!
func (c *client) Echo(ctx context.Context, text string) error {
	_, err := c.client.Echo(ctx, &pb.EchoRequest{
		Name:      c.name,
		Text:  text
	})
	if err != nil {
		return err
	}
	return nil
}
