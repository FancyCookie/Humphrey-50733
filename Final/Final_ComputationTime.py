from matplotlib import pyplot as plt
from Pandemic import Pandemic_NoAnime as Panome
import time as time


time_list = []
people_list = []
for i in range(1,6):
    start = time.time()
    people,infections,deaths,ticktock,reapers_list = Panome.ThePlague(500,grid_spacing = 0.2/i)
    end = time.time()
    duration = end - start
    time_list.append(duration)
    people_list.append(people)
    print(duration,people)


plt.xlabel("Number of People")
plt.ylabel("Time to Run Model")
plt.title("Time to Run Model versus Number of People")
plt.plot(people_list,time_list)
plt.savefig("ComputationTime.jpg")
plt.show()