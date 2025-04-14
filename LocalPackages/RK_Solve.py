


def fourth_rk(start,end,steps):
    x2 = np.zeros(steps)
    t2 = np.linspace(start,end,steps)
    h = (end-start)/steps

    for i in range(1,steps):
        k1 = h*f(x2[i-1],t2[i-1])
        k2 = h*f(x2[i-1]+k1/2, t2[i-1] + h/2)
        k3 = h*f(x2[i-1]+k2/2, t2[i-1] + h/2)
        k4 = h*f(x2[i-1]+k3, t2[i-1] + h)
        x2[i] = x2[i-1] + (k1+2*k2+2*k3+k4)/6
    
    return t2,x2