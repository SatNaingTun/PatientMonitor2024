from . import RepeatedTimer,ECG_Sensor,InfluxDb,MLX90614,Spo2Controller

client=InfluxDb.connectConnection()
def getECGCollect():
    dataECG= ECG_Sensor.readData()
    if dataECG is not None:
        InfluxDb.create_measurement(database_name='health',measurement_name='ECG',field_name='value',field_value=dataECG)
    
def getTemperatureCollect():
    ambientTemp=MLX90614.read_AmbientTemperature()
    if ambientTemp is not None:
        InfluxDb.create_measurement(database_name='health',measurement_name='AmbientTemperature',field_name='value',field_value=ambientTemp)
    objTemp=MLX90614.read_ObjectTemperature()
    if objTemp is not None:
        InfluxDb.create_measurement(database_name='health',measurement_name='ObjectTemperature',field_name='value',field_value=objTemp)

   
def getSpo2SensorCollect():
    spo2=Spo2Controller.getSpo2()
    if spo2 is not None:
        InfluxDb.create_measurement(database_name='health',measurement_name='Spo2',field_name='value',field_value=spo2)
    pulse=Spo2Controller.getPulse()
    if pulse is not None:
        InfluxDb.create_measurement(database_name='health',measurement_name='Pulse',field_name='value',field_value=pulse)
 
def getCollectBySchedule(interval):
    rt = RepeatedTimer.RepeatedTimer(interval=interval, function=getECGCollect)
    RepeatedTimer.RepeatedTimer(interval=interval, function=getTemperatureCollect)
    RepeatedTimer.RepeatedTimer(interval=interval, function=getSpo2SensorCollect)




    