# -*- coding: utf-8 -*-
import smbus
import time

# Create an SMBus instance
bus = smbus.SMBus(1)

# I2C address of the MLX90614
address = 0x5A

# Registers for temperature readings
AMBIENT_TEMP_REGISTER = 0x06
OBJECT_TEMP_REGISTER = 0x07

# Conversion factors
TEMP_SCALE_FACTOR = 0.02  # Each LSB equals 0.02�C
TEMP_OFFSET = 273.15      # Kelvin to Celsius conversion

# Function to read temperature from a specific register
def read_temperature(register):
    try:
        # Read two bytes of data from the given register
        data = bus.read_i2c_block_data(address, register, 2)
        raw_temp = (data[1] << 8) | data[0]  # Convert to 16-bit value (little-endian)
        temp_celsius = (raw_temp * TEMP_SCALE_FACTOR) - TEMP_OFFSET
        return temp_celsius
    except Exception as e:
        print(f"Error reading temperature: {e}")
        return None

def read_AmbientTemperature():
    return read_temperature(AMBIENT_TEMP_REGISTER)


def read_ObjectTemperature():
    return read_temperature(OBJECT_TEMP_REGISTER)



# while True:
#     # Read and print ambient and object temperatures
#     ambient_temp = read_temperature(AMBIENT_TEMP_REGISTER)
#     object_temp = read_temperature(OBJECT_TEMP_REGISTER)

#     if ambient_temp is not None and object_temp is not None:
#         print(f"Ambient Temperature: {ambient_temp:.2f} �C")
#         print(f"Object Temperature: {object_temp:.2f} �C")
#     else:
#         print("Failed to read temperature.")

#     time.sleep(1)
