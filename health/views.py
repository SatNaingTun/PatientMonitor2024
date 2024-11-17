# view.py
from django.shortcuts import get_object_or_404, render, redirect
import pandas
import plotly.express as px
from .controllers import InfluxDb



def chart(request):
    pass

def index(request):
    client=InfluxDb.connectConnection()
    dataList=InfluxDb.execute(query='select value,time from ECG where time > now() -30s order by time asc limit 100',database='health',measurementName='ECG')
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
    context={'chart':chart}
    return render(request,'health/chart.html',context)