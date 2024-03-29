import asyncio

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.board import Board
from viam.components.sensor import Sensor


async def connect():
    opts = RobotClient.Options.with_api_key(
      api_key='14mia6u7kvoei46w3dbz65i3ne2w6ysr',
      api_key_id='2c49424e-54cc-4d20-8e4a-768f22c947b5'
    )
    return await RobotClient.at_address('serial-main.k6chw1atuv.viam.cloud', opts)

async def main():
    robot = await connect()

    print('Resources:')
    print(robot.resource_names)
    
    # Note that the pin supplied is a placeholder. Please change this to a valid pin you are using.
    # local
    local = Board.from_robot(robot, "local")
    local_return_value = await local.gpio_pin_by_name("16")
    print(f"local gpio_pin_by_name return value: {local_return_value}")
  
    # serial
    serial = Sensor.from_robot(robot, "serial")
    serial_return_value = await serial.get_readings()
    print(f"serial get_readings return value: {serial_return_value}")

    # Don't forget to close the machine when you're done!
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())
