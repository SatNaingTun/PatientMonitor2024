import time
from gpiozero import DigitalInputDevice, OutputDevice

# GPIO Pins for SPI Communication
SPI_MOSI = OutputDevice(17)  # GPIO 17 for MOSI
SPI_MISO = DigitalInputDevice(27)  # GPIO 27 for MISO
SPI_CLK = OutputDevice(22)  # GPIO 22 for Clock
SPI_CS = OutputDevice(18)  # GPIO 18 for Chip Select (CS)

# GPIO for Leads-Off Detection
lo_plus = DigitalInputDevice(5)  # GPIO pin for LO+
lo_minus = DigitalInputDevice(6)  # GPIO pin for LO-

def spi_transfer(data_out):
    """
    Transfers a single byte over SPI and reads the response.
    :param data_out: Byte to send.
    :return: Byte received.
    """
    data_in = 0
    for i in range(8):  # Send and receive 8 bits
        # Set MOSI based on the most significant bit
        SPI_MOSI.value = (data_out & 0x80) != 0
        data_out <<= 1  # Shift data_out left
        
        # Pulse the clock
        SPI_CLK.on()
        time.sleep(0.00001)  # Small delay
        data_in <<= 1  # Shift data_in left
        if SPI_MISO.value:  # Read MISO
            data_in |= 0x01
        SPI_CLK.off()
        time.sleep(0.00001)  # Small delay
    return data_in

def read_mcp3202(channel):
    """
    Reads data from the specified channel of the MCP3202 ADC.
    :param channel: Channel to read (0 or 1).
    :return: Raw ADC value (0-4095).
    """
    if channel not in [0, 1]:
        raise ValueError("Invalid channel. Choose 0 or 1.")

    # MCP3202 Start Bit, Single-Ended, and Channel Selection
    start_bit = 1
    single_ended = 1
    command = (start_bit << 2) | (single_ended << 1) | channel

    # Begin SPI transaction
    SPI_CS.off()  # Set CS low to start communication
    spi_transfer(command << 4)  # Send command (upper 4 bits)
    msb = spi_transfer(0)  # Read MSB of the result
    lsb = spi_transfer(0)  # Read LSB of the result
    SPI_CS.on()  # Set CS high to end communication

    # Combine MSB and LSB into a 12-bit value
    result = ((msb & 0x0F) << 8) | lsb
    return result


def startConnection():
    SPI_MOSI.off()  # Set MOSI to low
    SPI_CLK.off()  # Set CLK to low
    SPI_CS.on()  # Set CS to high


def readData():
    # try:
        # while True:
            # Check leads-off detection
            if lo_plus.value == 1 or lo_minus.value == 1:
                print('!')  # Leads-off detected
                return None
            else:
                # Read analog value from ADC (assumes channel 0 is connected to AD8232)
                ecg_value = read_mcp3202(channel=0)
                print(ecg_value)  # Send analog ECG value
                return ecg_value
                
            # time.sleep(0.001)  # Small delay to prevent serial saturation
    # except KeyboardInterrupt:
    #     print("\n Error in reading data.")
    # # finally:
    #     # Cleanup
    #     SPI_CS.on()  # Ensure CS is high
    #     SPI_CLK.off()  # Ensure CLK is low

def endConnection():
    # Cleanup
    SPI_CS.on()  # Ensure CS is high
    SPI_CLK.off()  # Ensure CLK is low

    

def main():
    """
    Main loop to monitor the leads-off status and read ADC values.
    """
    try:
        while True:
            # Check leads-off detection
            if lo_plus.value == 1 or lo_minus.value == 1:
                print('!')  # Leads-off detected
            else:
                # Read analog value from ADC (assumes channel 0 is connected to AD8232)
                ecg_value = read_mcp3202(channel=0)
                print(ecg_value)  # Send analog ECG value
                
            time.sleep(0.001)  # Small delay to prevent serial saturation
    except KeyboardInterrupt:
        print("\nExiting program.")
    finally:
        # Cleanup
        SPI_CS.on()  # Ensure CS is high
        SPI_CLK.off()  # Ensure CLK is low

if __name__ == "__main__":
    # Initialize SPI Pins
    SPI_MOSI.off()  # Set MOSI to low
    SPI_CLK.off()  # Set CLK to low
    SPI_CS.on()  # Set CS to high
    main()
