import numpy as np
from matplotlib import pyplot as plt
from LocalPackage import RK_Solve as rk

def function1(x,t):
    return t

def function2(x,t):
    return 2*t

def function3(x,t):
    result = 3*t
    return result


start = 0
end = 10
steps = 100

tpoints = np.linspace(0,10,100)
x1points = np.linspace(0,10,100)
x2points = np.linspace(0,10,100)
x3points = np.linspace(0,10,100)

for i in range(len(tpoints)):
    dummyx1 = rk.fourth_rk(function1,start,end,steps)
    dummyx2 = rk.fourth_rk(function2,start,end,steps)
    dummyx3 = rk.fourth_rk(function3,start,end,steps)


fig1 = plt.figure(figsize = (10,7))
graph = fig1.add_subplot(111)
plt.xlabel("t")
plt.title("Random Differential Equations")
plt.ylabel("f(t,x)")
graph.plot(tpoints,dummyx1)
graph.plot(tpoints,dummyx2)
graph.plot(tpoints,dummyx3)
plt.show()