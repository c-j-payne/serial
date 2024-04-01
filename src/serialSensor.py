import serial
import time
from typing import Any, ClassVar, Dict, Mapping, Optional, Sequence, List, cast
from viam.components.sensor import Sensor
from viam.logging import getLogger
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
from viam.resource.registry import Registry, ResourceCreatorRegistration
from viam.resource.types import Model, ModelFamily
from viam.utils import ValueTypes, struct_to_dict

LOGGER = getLogger(__name__)


class SerialSensor(Sensor):
    MODEL: ClassVar[Model] = Model(ModelFamily("c-j-payne", "serial-sensor"), "serial")
    serial_baud_rate: int
    serial_path: str 
    serial_timeout: int

    # Keep a reference to the serial object at class level
    ser: Optional[serial.Serial] = None

    @classmethod
    def validate_config(cls, config: ComponentConfig) -> Sequence[str]:
        return []

    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> "SerialSensor":
        sensor = cls(config.name)
        sensor.reconfigure(config, dependencies)
        return sensor

    def __init__(self, name: str):
        super().__init__(name)

    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        try:
            # Extract baud rate, serial path, and timeout from the configuration
            self.serial_baud_rate = int(config.attributes.fields.get("serial_baud_rate", {}).number_value or 9600)
            self.serial_path = config.attributes.fields.get("serial_path", {}).string_value
            self.serial_timeout = int(config.attributes.fields.get("serial_timeout", {}).number_value or 1)
            
            # Check if all required fields are present
            if not self.serial_path:
                LOGGER.error("Serial port configuration error: Missing 'serial_path' field")
                return
            
            # Check if the specified baud rate is standard
            standard_baud_rates = [300, 1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200]
            if self.serial_baud_rate not in standard_baud_rates:
                LOGGER.error("Serial port configuration error: Invalid baud rate")
                return
            
            # Print if timeout and baud rate are set to default values
            if self.serial_baud_rate == 9600:
                LOGGER.info("Baud rate set to default value (9600)")
            if self.serial_timeout == 1:
                LOGGER.info("Timeout set to default value (1)")
            
            # Initialize the serial port with the provided parameters
            self.ser = serial.Serial(self.serial_path, self.serial_baud_rate, timeout=self.serial_timeout)
            LOGGER.info("Serial port configured")
        except KeyError:
            LOGGER.error("Serial port configuration error: Missing required fields")

    async def close(self):
        self.ser.close()
        LOGGER.info("%s is closed.", self.name)

    async def send_message(self, message: str):
        if self.ser is not None:
            # Encode the message as bytes and send it
            self.ser.write(message.encode())
            LOGGER.info(f"Sent:{message}")
        else:
            LOGGER.error("Serial port is not initialized.")

    async def receive_message(self) -> str:
        if self.ser is not None:
            # Read any incoming message 
            response = self.ser.readline().decode().strip()
            LOGGER.info(f"Received: {response}")
            return response
        else:
            LOGGER.error("Serial port is not initialized.")
            return ""

    async def do_command(self, command: Mapping[str, ValueTypes], *, timeout: Optional[float] = None, **kwargs) -> Mapping[str, ValueTypes]:
        if not isinstance(command, dict):
            LOGGER.error("Invalid command. Expected a dictionary.")
            return {"executed": False}
        for value in command.values():
            await self.send_message(str(value))
        return {"executed": True}

    async def get_readings(self, extra: Optional[Dict[str, Any]] = None, **kwargs) -> Mapping[str, Any]:
        # Execute receive_message function
        reading = await self.receive_message()
        # Output
        return {'reading': reading}


