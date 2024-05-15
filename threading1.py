import asyncio
import time
import re
import threading
from viam.robot.client import RobotClient
from viam.components.sensor import Sensor
from viam.components.motor import Motor

steps = 0

# Create a threading lock
lock = asyncio.Lock()

async def connect():
    # Connect to the robot
    opts = RobotClient.Options.with_api_key(
        api_key='14mia6u7kvoei46w3dbz65i3ne2w6ysr',
        api_key_id='2c49424e-54cc-4d20-8e4a-768f22c947b5'
    )
    return await RobotClient.at_address('serial-main.k6chw1atuv.viam.cloud', opts)

async def loop1(lock,serial):
    global steps

    timeinitial = time.time()
    

    while True:
        async with lock:
            reading = await serial.get_readings()
            messages = reading["reading"]
            
            #is there anything in the serial buffer?
            if len(messages) > 0:
                #loop through messages to extract data
                for message in messages:

                    #is it position feedback?
                    if 'is in position' in message:
                        position = reading["reading"][1]
                        pattern = r"\(steps\) (\d+)"
                        match = re.search(pattern, position)
                        steps = int(match.group(1))
                        print(steps)

                    #is it motor enabled?
                    if 'Motor enabled' in message:
                        print("motor enabled")
        
        await asyncio.sleep(0.01)
       

async def loop2(lock,serial):
    await serial.do_command({"message":"e0"})
    while True:
        async with lock:
            await serial.do_command({"message":"e0"})
        await asyncio.sleep(1)
        async with lock:
            await serial.do_command({"message":"v0 3000"})
        await asyncio.sleep(1)
        async with lock:
            await serial.do_command({"message":"v0 0"})
        await asyncio.sleep(1)
        async with lock:
            await serial.do_command({"message":"d0"})
        await asyncio.sleep(1)


async def main():
    robot = await connect()
    serial = Sensor.from_robot(robot, "serial")

    lock = asyncio.Lock()
    await asyncio.gather(
        loop1(lock,serial),
        loop2(lock,serial)
    )

if __name__ == "__main__":
    asyncio.run(main())
