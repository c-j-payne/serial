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

    booltemp: bool = False
    BAUD_RATE: int = 9600
    SERIAL_PORT: str = '/dev/ttyACM0'

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
        LOGGER.info('Define port and Baud Rate')
        # Initialize serial communication
        self.ser = serial.Serial(self.SERIAL_PORT, self.BAUD_RATE, timeout=1)
        LOGGER.info(type(self.ser))
        # Wait for serial port to be ready
        time.sleep(2)

    async def close(self):
        LOGGER.info("%s is closed.", self.name)

    async def send_message(self, message: str):
        # Check if serial object exists
        if self.ser is not None:
            # Encode the message as bytes and send it
            self.ser.write(message.encode())
            LOGGER.info("Serial sent:")
            LOGGER.info(message)
            # Wait for a short time before sending the next message
            time.sleep(1)
        else:
            LOGGER.error("Serial port is not initialized.")

    async def do_command(self, command: Mapping[str, ValueTypes], *, timeout: Optional[float] = None, **kwargs) -> Mapping[str, ValueTypes]:
        LOGGER.info(f'command: {command}')
        if "IS_TRUE?" in command:
            self.booltemp = True
            LOGGER.info("ON")
            message1 = "hello"
            await self.send_message(message1)
        else:
            LOGGER.info("OFF")
            self.booltemp = False
        return {"executed": True}

    async def get_readings(self, extra: Optional[Dict[str, Any]] = None, **kwargs) -> Mapping[str, Any]:
        LOGGER.info('reading data')
        return {'reading': self.booltemp}
