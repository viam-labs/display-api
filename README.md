# display-api

Proto API and grpc bindings for display

*display-api* provides Proto API and grpc bindings for display capabilities

## API

The display resource implements the following API:

### echo(text=*string*)

The *echo()* command takes:

* string: The string to echo back

## Using display-api with the Python SDK

Because this module uses a custom protobuf-based API, you must include this project in your client code.  One way to do this is to include it in your requirements.txt as follows:

```
display_api @ git+https://github.com/viam-labs/display-api.git@main
```

You can now import and use it in your code as follows:

```
from display_python import Display
api = Display.from_robot(robot, name="display")
api.echo(...)
```

See client.py for an example.

## Using display with the Golang SDK

Because this module uses a custom protobuf-based API, you must import and use in your client code as follows:

``` go
import audioout "github.com/viam-labs/display-api/src/display_go"

api, err := display.FromRobot(robot, "display")
fmt.Println("err", err)
api.Echo(context.Background(), "hi")
```

See client.go for an example.

## Building

To rebuild the GRPC bindings, run:

``` bash
make generate
```

Then, in `src/display_python/grpc/display_grpc.py change:

``` python
import display_pb2
```

to:

``` python
from . import display_pb2
```

Then, update the version in pyproject.toml
