import numpy as np
import scipy.interpolate as spi


def run_off(length, x, loss_factor, d_max, multiplier, multiplier_b, rainfall):
    """
    Takes the rainfall and the relevent runoff parameters and uses them to
    generate the surface runoff and the baseflow runoff as numpy arrays
    based on a loss model. The multipliers give more flexibility to the
    scaling of the hydrographs than using a fixed catchment size.
    """
    
    # defines the groundwater depth and the surface runoff arrays and initial conditions
    depth = np.zeros(length)
    flow = np.zeros(length)
    loss = np.zeros(length)
    depth[0] = 0
    
        
    for i in range(1,length):
        
        loss[i] = loss_factor*(depth[i-1]/d_max)**x

        flow[i] = (rainfall[i]*(depth[i-1]/d_max)**x)
        
        depth[i] = depth[i-1] + rainfall[i] - (rainfall[i]*(depth[i-1]/d_max)**x) 
        
        if depth[i] > d_max:
            depth[i] = d_max
        
        if depth[i] > loss[i-1]:
            depth[i] = depth[i] - loss[i-1]
        
        if depth[i] < loss[i-1]:
            depth[i] = 0
   
    flow = flow * multiplier
    loss = loss * multiplier_b
   
    return flow, loss


def unit_hydrograph(flow, loss, x_array, Tp, Tm, Te, Vm, min_flow):
    """
    A unit hydrograph routing module that routes the surface runoff and 
    baseflow runoff. The unit hydrograph is very flexible with a variable 
    time to peak, time to mid falling limb, magnitude of mid falling limb 
    and the time to end. Returns the routed surface and base flow and the 
    combined flow prediction as numpy arrays.
    """
    
    x = (0, Tp, Tm, Te)
    y = (0, 1, Vm, 0)
    
    f = spi.interp1d(x,y)
    
    x1 = np.arange(0, Te, 0.25, dtype=float)
    
    y1 = f(x1)
    
    Q_predicted = np.zeros(len(x_array))
    Q_surface = np.zeros(len(x_array))
    Q_base = np.zeros(len(x_array))
    
    for i in range(len(x_array)-len(y1)):
        
        temp1 = flow[i]*y1
        temp2 = loss[i]*y1
        temp1 = np.pad(temp1, (i, len(x_array)-i-len(y1)), 'constant', constant_values=(0, 0))
        temp2 = np.pad(temp2, (i, len(x_array)-i-len(y1)), 'constant', constant_values=(0, 0))
               
        Q_surface += temp1
        Q_base += temp2
        
    Q_predicted = Q_surface + Q_base + min_flow
    
    return Q_predicted, Q_surface, Q_base


def model_run(time, rainfall, params):    
    """
    Used to run the runoff and unit hydrograph models.
    """
    length = len(time)
    
    runoff, loss = run_off(length, params[0], params[1], params[2], params[3], params[4], rainfall)

    Q_predicted, Q_surface, Q_base  = unit_hydrograph(runoff, loss, time, params[5], params[6], params[7], params[8], params[9])
    
    return  runoff, loss, Q_predicted, Q_surface, Q_base