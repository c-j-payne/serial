"""
A sensor component to send and receive serial messages
"""

from typing import Any, ClassVar, Dict, Mapping, Optional, Sequence, List, cast
from typing_extensions import Self
from viam.components.sensor import Sensor
from viam.logging import getLogger
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
from viam.resource.registry import Registry, ResourceCreatorRegistration
from viam.resource.types import Model, ModelFamily
from viam.utils import ValueTypes, struct_to_dict

import asyncio
import serial
import time

# Activate the logger to send log entries to app.viam.com, visible under the logs tab
LOGGER = getLogger(__name__)


class SerialSensor(Sensor):
    """
    Class representing the sensor to be implemented/wrapped.
    Subclass the Viam Sensor component and implement the required functions
    """

    MODEL: ClassVar[Model] = Model(ModelFamily("c-j-payne", "serial-sensor"), "serial")

    booltemp: bool = False
    command: str = "aaa"

    @classmethod
    def validate_config(cls, config: ComponentConfig) -> Sequence[str]:
        return []

    @classmethod
    def new(
        cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ) -> Self:
        """
        This constructor instantiates a new "serialsensor" component based upon the 
        configuration added to the RDK.
        """
        sensor = cls(config.name)
        sensor.reconfigure(config, dependencies)
        return sensor

    def __init__(self, name: str):
        """
        Actual component instance constructor
        """
        super().__init__(name)

    def reconfigure(
        self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ):
        LOGGER.info('Define port and Baud Rate')
        # Define the serial port and baud rate
        SERIAL_PORT = '/dev/ttyACM0'  # Change this to match your Arduino's serial port
        BAUD_RATE = 9600

        # Initialize serial communication
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

        # Wait for serial port to be ready
        time.sleep(2)


    async def close(self):
        """
        Optional function to include. This will be called when the resource
        is removed from the config or the module is shutting down.
        """
        LOGGER.info("%s is closed.", self.name)

    async def do_command(
        self, 
        command: Mapping[str, ValueTypes],
        *,
        timeout: Optional[float] = None,
        **kwargs
        ) -> Mapping[str, ValueTypes]:
        LOGGER.info(f'command: {command}')
        if "IS_TRUE?" in command:
            self.booltemp=True
            LOGGER.info("ON")

        else:
            LOGGER.info("OFF")
            self.booltemp=False 
        return {"executed": True}

    async def get_readings(
        self, extra: Optional[Dict[str, Any]] = None, **kwargs
    ) -> Mapping[str, Any]:
        """
        Required method to be implemented for a sensor component.
        This method now runs a database query and returns the results.
        """
        # Ensure that all necessary credentials are available
        LOGGER.info('reading data')
        #command="sss"
        #await send_message(command + '\n')
        return {'reading': self.booltemp}


    # Function to send a message to the Arduino
    #async def send_message(message):
        # Encode the message as bytes and send it
    #    ser.write(message.encode())
    #    print("Sent:", message)