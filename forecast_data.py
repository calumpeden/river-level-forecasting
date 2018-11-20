import urllib
import datetime as dt
import numpy as np
import json
#import matplotlib.pyplot as plt

def metcheck_forecast(lat, lon):
    """
    Reads the forecast from metcheck for a given lat lon point and retuns a 
    dictionary with timestamps as keys and the rainfall and freezing level
    between the timestamp and the previous timestamp.
    """    
    
    MetCheck_URL = "http://ws1.metcheck.com/ENGINE/v9_0/json.asp?lat={0:0.1f}&lon={1:0.1f}&Fc=No"
    url = MetCheck_URL.format(lat,lon)
    
    response = urllib.request.urlopen(url).read().decode()
    
    text = response.split("\n")
    
    metcheck_dict = {}
    
    for i in range(len(text)):
        if '"rain":' in text[i]:
            rain = np.abs(float(text[i].split(': "')[1][:-3]))
            t = dt.datetime.strptime(text[i+22].split(': "')[1][:-5], "%Y-%m-%dT%H:%M:%S")
            metcheck_dict.update({t:rain})
    
    return metcheck_dict
 
def YR_forecast(lat, lon):    
    """
    Reads the forecast from YR (norway nat weather service) for a given lat lon
    point and retuns a dictionary with timestamps as keys and the rainfall 
    between the timestamp and the previous timestamp. 
    """
    
    YR_URL = "https://api.met.no/weatherapi/locationforecast/1.9/?lat={0:0.6f}&lon={1:0.6f}&msl=0"
        
    xml_list = urllib.request.urlopen(YR_URL.format(lat,lon)).read().decode().split('\n')
    
    YR_dict = {}
    
    for i in range(len(xml_list)):
        
        if '      <time datatype="forecast" from="' in xml_list[i]:
            line = xml_list[i].split('"')
            start = dt.datetime.strptime(line[3],"%Y-%m-%dT%H:%M:%SZ")
            end = dt.datetime.strptime(line[5],"%Y-%m-%dT%H:%M:%SZ")
            
            if str(end-start) == '1:00:00':
                rainfall = float(xml_list[i+2].split('"')[3])
                
                YR_dict.update({end:rainfall})
    
    return YR_dict

def weatherbit_forecast(lat, lon):
    """
    Reads the forecast from weatherbit for a given lat lon point and retuns a 
    dictionary with timestamps as keys and the rainfall between the timestamp 
    and the previous timestamp.
    """
    
    WeathBit_URL = "https://api.weatherbit.io/v2.0/forecast/hourly?lat={0:0.6f}&lon={1:0.6f}&key=b9949e5248be4958bd833b5e579efbac"
    
    WB = json.loads(urllib.request.urlopen(WeathBit_URL.format(lat,lon)).read().decode())
    
    weatherbit_dict = {}
    
    for forecast in WB['data']:
        t = (dt.datetime.strptime(forecast['datetime'], '%Y-%m-%d:%H'))
        r = float(forecast['precip'])
        weatherbit_dict.update({t:r})
        
    return weatherbit_dict

#lon=-5.105218
#lat=56.819817
#
#mc = metcheck_forecast(lat, lon)
#yr = YR_forecast(lat, lon)
#wb = weatherbit_forecast(lat, lon)
#
#t_current = dt.datetime.utcnow().replace(microsecond=0,second=0,minute=0)
#
#m = []
#y = []
#w = []
#t_ = []
#
#for i in range(100):
#    t = t_current + dt.timedelta(hours=i)
#        
#    if t in mc.keys() and t in yr.keys() and t in wb.keys():
#        m.append(mc[t][0])
#        y.append(yr[t])
#        w.append(wb[t])
#        t_.append(t)
#       
#    
#plt.plot(t_, m)
#plt.plot(t_, y)
#plt.plot(t_, w)
#plt.show()