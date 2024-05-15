import serial
import time
import threading
import asyncio
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
    MODEL: ClassVar[Model] = Model(ModelFamily("chris", "serial-port"), "ascii")
    serial_baud_rate: int
    serial_path: str 
    serial_timeout: int
    serial_lock: threading.Lock()
    ser: Optional[serial.Serial] = None
    

    @classmethod
    def validate_config(cls, config: ComponentConfig) -> Sequence[str]:
        serial_path = config.attributes.fields.get("serial_path", {}).string_value
        if serial_path == '':
            raise Exception('serial path is required')
        return []

    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> "SerialSensor":
        sensor = cls(config.name)
        sensor.reconfigure(config, dependencies)
        return sensor

    def __init__(self, name: str):
        super().__init__(name)
        self.serial_lock = threading.Lock() 

    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        try:
            if self.ser is not None:
                self.ser.close()

            self.serial_baud_rate = int(config.attributes.fields.get("serial_baud_rate", {}).number_value or 115200)
            self.serial_path = config.attributes.fields.get("serial_path", {}).string_value
            self.serial_timeout = int(config.attributes.fields.get("serial_timeout", {}).number_value or .1)

            if not self.serial_path:
                LOGGER.error("Serial port configuration error: Missing 'serial_path' field")
                return

            standard_baud_rates = [300, 1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200]
            if self.serial_baud_rate not in standard_baud_rates:
                LOGGER.error("Serial port configuration error: Invalid baud rate")
                return

            # Try alternative paths first
            alternative_paths = [f"/dev/ttyACM{i}" for i in range(3)]  # Try /dev/ttyACM0, /dev/ttyACM1, /dev/ttyACM2
            for path in alternative_paths:
                try:
                    self.ser = serial.Serial(path, self.serial_baud_rate, timeout=self.serial_timeout)
                    LOGGER.info(f"Serial port configured with alternative path: {path}")
                    self.serial_path = path  # Update the serial path to the successfully opened one
                    return  # Exit the function if successful
                except serial.SerialException as e:
                    LOGGER.error(f"Failed to open serial port at {path}: {e}")

            # If alternative paths fail, try the provided path
            try:
                self.ser = serial.Serial(self.serial_path, self.serial_baud_rate, timeout=self.serial_timeout)
                LOGGER.info("Serial port configured")
            except serial.SerialException as e:
                LOGGER.error(f"Failed to open serial port at {self.serial_path}: {e}")            
        except KeyError:
            LOGGER.error("Serial port configuration error: missing required fields")

    async def close(self):

        # When closing the module, close the serial port
        if self.ser is not None:
            self.ser.close()
        LOGGER.info("%s is closed.", self.name)
        

    async def send_message(self, message: str):        
        # Lock the serial port and write the message
        with self.serial_lock:
            self.ser.write(message.encode())
            LOGGER.info(f"Sent:{message}")


    async def receive_message(self) -> str:
        # Lock the serial port 
        with self.serial_lock:
            # Create empty array for the response
            response_lines = []
            # Loop through each line received by the serial port
            while True:
                # Read a line of the serial port
                line = self.ser.readline().decode().strip()
                if line:  # Check if the line is not empty and append
                    response_lines.append(line)
                else:
                    break  # Exit the loop if an empty line is received                    
        return response_lines
        

    async def do_command(self, command: Mapping[str, ValueTypes], *, timeout: Optional[float] = None, **kwargs) -> Mapping[str, ValueTypes]:
        
        # Check if a serial port exists
        if self.ser is not None:
            # Check do_command is receiving a dictionary and error if not
            if not isinstance(command, dict):
                LOGGER.error("Invalid command. Expected a dictionary.")
                return {"executed": False}
            # Send the Value to the send_message function and log the message sent
            for value in command.values():
                await self.send_message(str(value))
                #LOGGER.info(f"Sending message: {value}")
            return {"executed": True}
        else:
            LOGGER.error("Serial port is not initialized.")
            return ""

    async def get_readings(self, extra: Optional[Dict[str, Any]] = None, **kwargs) -> Mapping[str, Any]:

        # Check if a serial port exists
        if self.ser is not None:
            # Execute the receive_message function
            reading = await self.receive_message()            
            LOGGER.info(f"Message received: {reading}")
            return {'reading': reading}
        else:
            LOGGER.error("Serial port is not initialized.")
            return {'reading': "Serial port is not initialized."}


