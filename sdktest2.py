import asyncio
import time
import re
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

    print("connected to robot")
    # Get the components
    serial = Sensor.from_robot(robot, "serial")

    await serial.do_command({"message":"c0"})
    time.sleep(0.4)

    await serial.do_command({"message":"e0"})
    time.sleep(0.4)
       

    try:
        while True:

            await serial.do_command({"message":"v0 6000"})
            time.sleep(0.4)
            #reading = await serial.get_readings()
            time.sleep(0.4)
            #print(reading)

            await serial.do_command({"message":"v0 6000"})
            time.sleep(0.4)
            #reading = await serial.get_readings()
            time.sleep(0.4)
            #print(reading)

            await serial.do_command({"message":"v0 0"})
            time.sleep(0.4)


            
    finally:
        timestamp = time.time() - timestamp
        print(timestamp)

        await serial.do_command({"message":"d0"})
        time.sleep(0.4)
        reading = await serial.get_readings()
        time.sleep(0.4)
        print(reading)

        
        await robot.close()

if __name__ == '__main__':
    asyncio.run(main())
