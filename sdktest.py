import asyncio
import time

from viam.robot.client import RobotClient
from viam.components.sensor import Sensor


async def connect():
    # Connect to the robot
    opts = RobotClient.Options.with_api_key(
        api_key='14mia6u7kvoei46w3dbz65i3ne2w6ysr',
        api_key_id='2c49424e-54cc-4d20-8e4a-768f22c947b5'
    )
    return await RobotClient.at_address('serial-main.k6chw1atuv.viam.cloud', opts)


async def main():
    # Connect to the robot
    robot = await connect()

    print("connected to robot")
    # Get the serial sensor
    serial = Sensor.from_robot(robot, "serial")

    print("create serial port")

    try:
        # Set the maximum number of iterations for the loop
        max_iterations = 100
        print("trying serial")
        for _ in range(max_iterations):
            # Query help
            set_velocity_command = {"message": "h"}
            print("sending help message ", set_velocity_command)
            await serial.do_command(set_velocity_command)
            print("sending h")

            # Check controller
            reading = await serial.get_readings()
            print(reading)
            time.sleep(0.2)

    finally:
        print("close")

        # Close the robot connection
        await robot.close()

if __name__ == '__main__':
    asyncio.run(main())
