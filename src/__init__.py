from viam.components.sensor import Sensor
from viam.resource.registry import Registry, ResourceCreatorRegistration
from .serialSensor import serialSensor

#from previous module: 
Registry.register_resource_creator(Sensor.SUBTYPE, serialSensor.MODEL, ResourceCreatorRegistration(serialSensor.new, serialSensor.validate_config))