from model_code import model_run
import numpy as np
import time
import matplotlib.pyplot as plt


def rmse(predictions, targets):
    #return np.sqrt(((predictions - targets) ** 2).mean())
    return (np.abs((predictions - targets))).mean()

def calibration(t_15min, rainfall_15min, Q_actual, params, mutate, start, end, freq):
    
    runoff, loss, Q_predicted, Q_surface, Q_base = model_run(t_15min, rainfall_15min,  params)
    
    rms = rmse(Q_predicted[start:end], Q_actual[start:end] )
    
    plt.plot(t_15min[start:end], Q_actual[start:end])
    plt.show()
    
    MAX = rms
    
    clock_start = time.clock()
    clock = 0

    while clock < freq:

        x = params[0] + (np.random.uniform(-1,1)*(params[0]*mutate))
        
        loss_factor = params[1] + (np.random.uniform(-1,1)*(params[1]*mutate))
        
        d_max = params[2] + (np.random.uniform(-1,1)*(params[2]*mutate))
        
        multiplier = params[3] + (np.random.uniform(-1,1)*(params[3]*mutate))
        
        multiplier_b = params[4] + (np.random.uniform(-1,1)*(params[4]*mutate))
        
        Tp = params[5] + (np.random.randint(-1,2))
        
        Tm = params[6] + (np.random.randint(-1,2))
        
        Te = params[7] + (np.random.randint(-1,2))
        
        Vm = params[8] + (np.random.uniform(-1,1)*(params[8]*mutate))
        
        min_flow = params[9] + (np.random.uniform(-1,1)*(params[9]*mutate))
        
        if Tp <= Tm and Tm <= Te and Vm <= 1:
            
            
            params_t = [x, loss_factor, d_max, multiplier, multiplier_b, Tp, Tm, Te, Vm, min_flow]
            
            runoff, loss, Q_predicted, Q_surface, Q_base = model_run(t_15min, rainfall_15min,  params_t)
        
            rms = rmse(Q_predicted[start:end], Q_actual[start:end])
            
            if rms < MAX:
                params = [x, loss_factor, d_max, multiplier, multiplier_b, Tp, Tm, Te, Vm, min_flow]
                MAX = rms
                print(rms)
        
        clock = time.clock() - clock_start
               
    return params

