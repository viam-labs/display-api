"""
This file registers the model with the Python SDK.
"""

from viam.resource.registry import Registry, ResourceRegistration

from .api import DisplayClient, DisplayRPCService, Display

Registry.register_subtype(ResourceRegistration(Display, DisplayRPCService, lambda name, channel: DisplayClient(name, channel)))
