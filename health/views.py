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
    
    dataList=InfluxDb.execute(query='select value,time from ECG where time > now() -30s order by time asc limit 100',database='health',measurementName='ECG')
    ambientTemperature=InfluxDb.execute(query='select value,time from AmbientTemperature order by time desc limit 1',database='health',measurementName='AmbientTemperature')
    objTemperature=InfluxDb.execute(query='select value,time from ObjectTemperature order by time desc limit 1',database='health',measurementName='ObjectTemperature')
    spo2=InfluxDb.execute(query='select value,time from Spo2 order by time desc limit 1',database='health',measurementName='Spo2')
    pulse=InfluxDb.execute(query='select value,time from Pulse order by time desc limit 1',database='health',measurementName='Pulse')
    # print(ambientTemperature[0])
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
    context={'chart':chart,'ambientTemperature':ambientTemperature[0],'objTemperature':objTemperature[0],'spo2':spo2[0],'pulse':pulse[0]}
    return render(request,'health/chart.html',context)