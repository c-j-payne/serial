import asyncio
import time

from viam.robot.client import RobotClient
from viam.components.sensor import Sensor
from viam.components.motor import Motor

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
    serial = Sensor.from_robot(robot, "serial")
    clearcore = Motor.from_robot(robot, "clearcore")
    print("hi")

    #await serial.do_command({"message":"c0"})
    #await serial.get_readings()
    #time.sleep(0.1)
    #await serial.do_command({"message":"e0"})
    #await serial.get_readings()
    time.sleep(0.1)
    print("hi")

    try:
        max_iterations = 3        
        for _ in range(max_iterations):
            
            await clearcore.set_power(.5)
            print("hello")
            time.sleep(.5)
            await clearcore.set_power(0)
            time.sleep(.5)

    finally:

        await clearcore.stop()

        #await serial.do_command({"message":"c0"})

        # clearcore
        #clearcore_return_value = await clearcore.is_moving()
        #print(f"clearcore is_moving return value: {clearcore_return_value}")

        #clearcore_return_value = await clearcore.get_properties()
        #print(f"clearcore is_moving return value: {clearcore_return_value}")

        #await clearcore.set_power(0)


        # Close the robot connection
        await robot.close()

if __name__ == '__main__':
    asyncio.run(main())
