from forecast_data import *
import pickle
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt

def rainfall_data(gauge_id, fcast, lat, lon, start=-3, end=2):
    """
    Combines the rainfall record with the forecast such that up to the point 
    where the record data ends the 15 minute output rainfall is based on the
    record and after that point it is based on the forecast. Each output 
    timestep is 15mins so the hourly rainfall is divided by 4 and is given 
    at the 4 15min timestamps preceding the timestamp of record or forecast.
    Takes:
    A rainfall gauge id that is in the records folder
    A forecast type (wb = weatherbit, yr = YR, mc = metcheck)
    The Latitude for the forecast
    The Longditude for the forecast
    A start time in days prior to the current time (negative number)
    An end time in days after the current time (positive number)
    """
    
    record_file = "sepa_rain_gauge/" + str(gauge_id) + ".pkl"
    historic = pickle.load(open(record_file, "rb"))
    
    if fcast == 'wb':
        forecast = weatherbit_forecast(lat, lon)
        
    if fcast == 'yr':
        forecast = YR_forecast(lat, lon)
    
    if fcast == 'mc':
        forecast = metcheck_forecast(lat, lon)
        
    if fcast == 'none':
        forecast = {}
    
    t_current = dt.datetime.utcnow().replace(microsecond=0,second=0,minute=0)
    t_start = t_current + dt.timedelta(hours=start*24)
    
    timestamps = []
    x_list = []
    rainfall = []
    
    for i in range((end-start)*24):
        
        t1 = t_start + dt.timedelta(hours=i+1)
        t2 = t_start + dt.timedelta(hours=i)
        
        for j in range(4):
            timestamp = t2 + dt.timedelta(minutes=15*j)
            x = start + (i*4 + j)/96
            rain = 0
            
            if t1 in forecast.keys():
                rain = forecast[t1]/4
                               
            if t1 in historic.keys():
                rain = historic[t1]/4
            
            timestamps.append(timestamp)
            x_list.append(x)
            rainfall.append(rain)
    
    x_array = np.array(x_list)
    rainfall = np.array(rainfall)
               
    return timestamps, x_array, rainfall

def level_data(gauge_id, timestamps):
    """
    For a given gauge id and timestamps list (from the rainfall_data function)
    the record is read from the record file and returned as a array of level
    data.
    """
    
    record_file = "sepa_level_gauge/" + str(gauge_id) + ".pkl"
    historic = pickle.load(open(record_file, "rb"))
    
    level = []
    
    for stamp in timestamps:
        
        l = 0
        
        if stamp in historic.keys():
            l = historic[stamp]
        
        level.append(l)
    
    level = np.array(level)
    
    return level