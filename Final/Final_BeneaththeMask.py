from matplotlib import pyplot as plt
from Pandemic import Pandemic_NoAnime as Panome
import time as time

people1,infections1, deaths1,ticktock1,reapers_list1 = Panome.ThePlague(500,masked=0,grid_spacing = 0.2/3)
people2,infections2,deaths2,ticktock2,reapers_list2 = Panome.ThePlague(500,masked=196,grid_spacing = 0.2/3)

plt.xlabel("Time")
plt.ylabel("Number of Sick")
plt.title("Number of Sick versus Time")
plt.plot(ticktock1,reapers_list1, c = "m", label = "NO MASK")
plt.plot(ticktock2,reapers_list2, c= "y", label = "MASKED")
plt.legend()
plt.savefig("FlatteningCurve.jpg")
plt.show()
