def exp_smooth(data, weight=0.97): 
    last = data[0]  # First value in the plot (first timestep)
    smoothed = list()
    for point in data:
        smoothed_val = last * weight + (1 - weight) * point  # 计算平滑值
        smoothed.append(smoothed_val)                    
        last = smoothed_val                                
    return smoothed

def converageup(data, weight=0.2):
    '''
    weight越高越向smoothed_data靠拢
    '''
    smoothed_data = exp_smooth(data, weight)
    cov = []
    for i in range(len(data)):
        cov.append((1-weight)*data[i] + weight*smoothed_data[i])
    return cov
    
    