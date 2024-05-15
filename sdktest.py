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


async def motor_command(serial,message,delay_response,delay_issue):
    await serial.do_command(message)
    time.sleep(delay_response)
    reading = await serial.get_readings()
    time.sleep(delay_issue)

    return reading



async def main():
    # Connect to the robot
    robot = await connect()

    print("connected to robot")
    # Get the components
    serial = Sensor.from_robot(robot, "serial")
    clearcore = Motor.from_robot(robot, "clearcore")

    #reading = await serial.get_readings()
    
    #while reading != None:
    ##    reading = await serial.get_readings()
    #    print(reading)


        

    try:
        timestamp = time.time()
        n = 10

        await motor_command(serial,{"message": "c0"},0.2,0.2)
        await motor_command(serial,{"message": "e0"},0.2,0.1)
        #command = {"message": "c0"}        
        #await serial.do_command(command)
        #reading = await serial.get_readings()
        #print(reading)
        #time.sleep(0.1)
        #await clearcore.reset_zero_position(0)
        time.sleep(0.1)


        for _ in range(n):
            '''await motor_command(serial,{"message": "v0 20000"},0.1,0)
            print(_)
            time.sleep(0.5)
            await motor_command(serial,{"message": "v0 0"},0.1,0)
            time.sleep(0.5)
            await motor_command(serial,{"message": "v0 5000"},0,0)
            await motor_command(serial,{"message": "v0 0"},0,0)'''
            
            await serial.do_command({"message": "c0"})
            time.sleep(0.1)
            reading = await serial.get_readings()
            time.sleep(0.1)

            '''if reading["reading"][1] != 'Motor 0 is in position (steps) 0':
                while True:
                    await serial.do_command({"message": "q0p"})
                    time.sleep(0.1)
                    reading = await serial.get_readings()
                    time.sleep(0.1)
                    print(reading)
                    print(reading["reading"][1])
                    if reading["reading"][1] == 'Motor 0 is in position (steps) 20000':
                        print("got here")
                        break'''


            """while True:
                reading = await serial.get_readings()
                time.sleep(0.1)
                if reading["reading"][1] == 'Motor 0 is in position (steps) 20000':
                    break"""

            
    


            #await serial.do_command({"message": "m0 20000"})
            #time.sleep(0.5)

            await serial.do_command({"message": "q0p"})
            time.sleep(0.1)
            reading = await serial.get_readings()
            print(reading)
            time.sleep(0.1)
            







    finally:
        timestamp = time.time() - timestamp
        print(timestamp)

        await motor_command(serial,{"message": "d0"},0.1,0.1)
        
        await robot.close()

if __name__ == '__main__':
    asyncio.run(main())
