import ECG_Sensor
import InfluxDb


if __name__ == "__main__":
    # Initialize SPI Pins
    ECG_Sensor.startConnection()
    InfluxDb.connectConnection()

    try:
        while True:
            data= ECG_Sensor.readData()
            if data is not None:
                InfluxDb.create_measurement(database_name='health',measurement_name='ECG',field_name='value',field_value=data)
    
    except KeyboardInterrupt:
            print("\n Exiting program.")
    finally:
        ECG_Sensor.endConnection()