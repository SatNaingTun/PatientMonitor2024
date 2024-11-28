# view.py
from django.shortcuts import get_object_or_404, render, redirect
import pandas
import plotly.express as px
from .controllers import InfluxDb




def chart(request):
    pass

def index(request):
    client=InfluxDb.connectConnection()

    # data= ECG_Sensor.readData()
    # if data is not None:
    #     InfluxDb.create_measurement(database_name='health',measurement_name='ECG',field_name='value',field_value=data)
    
    dataList=InfluxDb.execute(query='select value,time from ECG where time > now() -60s order by time asc limit 100',database='health',measurementName='ECG')
    ambientTemperature=InfluxDb.execute(query='select value,time from AmbientTemperature where time > now() - 60s  order by time desc limit 1',database='health',measurementName='AmbientTemperature')
    objTemperature=InfluxDb.execute(query='select value,time from ObjectTemperature where time > now() - 60s  order by time desc limit 1',database='health',measurementName='ObjectTemperature')
    spo2=InfluxDb.execute(query='select value, time from Spo2 where time > now() - 60s order by time desc limit 1;',database='health',measurementName='Spo2')
    pulse=InfluxDb.execute(query='select value, time from Pulse where time > now() - 60s order by time desc limit 1;',database='health',measurementName='Pulse')
    # print(ambientTemperature[0])
    print(spo2)

    if len(dataList)>0:
        yData=[r['value'] for r in dataList]
        xData=[r['time'] for r in dataList]
    else:
        yData=[0,0,0]
        xData=[1,2,3]
    fig=px.line(
        x=xData,
        y=yData,
        title="ECG",
        labels={'x':'time','y':'ECG Value'}
    )
    chart=fig.to_html()

    if spo2 is None:
        spo2=[{'value':0,'time':''}]
    if pulse is None:
        pulse=[{'value':0,'time':''}]
    context={'chart':chart,'ambientTemperature':ambientTemperature[0] if ambientTemperature else None,'objTemperature':objTemperature[0] if ambientTemperature else None,'spo2': spo2[0] if spo2 else None, 'pulse': pulse[0] if pulse else None}
    return render(request,'health/chart.html',context)