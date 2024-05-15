import serial
import time
# Open serial connection to Arduino
arduino = serial.Serial('/dev/ttyACM1', 112500)  # Adjust the port ('COM3') as needed
commands = ['o1 1', 'o1 0']  # Add your commands here
try:
    while True:
        # Loop through commands and send them to Arduino
        for command in commands:
            arduino.write(command.encode())
            print("Sent command:", command)

            response = arduino.readline().decode().strip()
            print(response)

            '''# Read response from Arduino and concatenate lines into one message
            response_message = ""
            while True:
                
                response = arduino.readline().decode().strip()
                print(response)
                if response:
                    response_message += response + "\n"  # Append response to message
                else:
                    break  # Break out of the loop if there is no more response
            #Print the concatenated response message
            print("Response from Arduino:", response_message)'''
            time.sleep(0.05)  # Adjust delay between commands as needed
except KeyboardInterrupt:
    # Close serial connection on Ctrl+C
    arduino.close()














