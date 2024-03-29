import serial
import time

# Define the serial port and baud rate
SERIAL_PORT = '/dev/ttyACM0'  # Change this to match your Arduino's serial port
BAUD_RATE = 9600

# Initialize serial communication
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

# Wait for serial port to be ready
time.sleep(2)

# Function to send a message to the Arduino
def send_message(message):
    # Encode the message as bytes and send it
    ser.write(message.encode())
    print("Sent:", message)

try:
    while True:
        # Prompt the user to enter a command
        command = input("Enter command (LEDON / LEDOFF): ")

        # Send the command to the Arduino
        send_message(command + '\n')

        # Read any incoming message from the Arduino
        response = ser.readline().decode().strip()
        print("Received:", response)

        # Wait for a short time before sending the next message
        time.sleep(1)

except KeyboardInterrupt:
    # Handle Ctrl+C gracefully
    print("\nExiting program.")

finally:
    # Close the serial port
    ser.close()
