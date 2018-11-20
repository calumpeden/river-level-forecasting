from run_data import rainfall_data, level_data
from model_code import model_run
from runtime_calibration import calibration, rmse
import numpy as np
import scipy.interpolate as spi
import matplotlib.pyplot as plt


#params = [2.2031504243159503, 0.0013483711573131635, 0.01653791866556452, 216.17835597687602, 11560.52979324557, 2, 4, 12, 0.0052615066888029634, 3.8904080286129337]
params = [1, 0.01, 0.5, 3000, 3000, 3,4,13,0.1,2]
#params = [1.5507260583290008, 0.005827541384114973, 0.14526216988100246, 1335.7688373126512, 434.7484190446534, 5, 5, 12, 0.190485424281642, 0.8461274964745216]
#[0.9891826115651172, 0.007876986241530269, 1.0173677992590793, 2839.4504719308907, 736.604557312018, 1, 1, 5, 0.06340428396062366, 0.5735051301251568]
mutate = 0.2
start = 0
end = 96*9
lon=-5.105218
lat=56.819817

while True:
    
    timestamps, x_array, rainfall = rainfall_data(14926, 'yr', lat, lon, start=-10, end=0)
    plt.plot(x_array, rainfall)
    
    level = level_data(371579, timestamps)
    plt.plot(x_array, level)
    plt.show()
    
    runoff, loss, level_predicted, level_surface, level_base = model_run(x_array, rainfall/1000, params)

    plt.plot(x_array, level_predicted)
    plt.plot(x_array, level)
    plt.show()
    
    params = calibration(x_array, rainfall/1000, level, params, mutate, start, end, 60)
    
    print(params)