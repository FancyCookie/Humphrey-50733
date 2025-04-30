import matplotlib.animation as animation
import numpy as np
import time
from matplotlib import pyplot as plt

# Parameters for the model. Assumption that (0,0) is in the bottom left corner.

grid_size = 100
grid_spacing = 10
deltat = 1
scl_dist = 6

daylength = 12
sick_time = daylength * 10
sick_mid = sick_time / 2

class Person(object): # TO DO: Finish death table and then make a counter to count how long an individual has been sick to cross reference with their chance to die.

    # First, create a person with some position, r, and some velocity, v. These should be 2 dim arrays. Assume everyone is healthy and non-immune.
    def __init__(self,r,v):
        self.r = r
        self.v = v
        self.alive = True
        self.healthy = True
        self.immune = False
        self.counter = 0
        self.grave = 999
        self.future = np.random.randint(0,2)

    # How do these people move? A simple s*t = d for their default; later comes if they're too close to people.
    def move(self,deltat):
        if self.alive:
            self.r = self.r + self.v*deltat
        
            # The following keeps the people in their boxy prison and then gets them to "bounce" of the edges of it.
            if self.r[0] < 0:
                self.r[0] = np.abs(self.r[0])
                self.v[0] = -1*self.v[0] 

            if self.r[1] <0:
                self.r[1] = np.abs(self.r[1])
                self.v[1] = -1*self.v[1] 


            if self.r[0] > grid_size:
                self.r[0] = grid_size - (self.r[0] - grid_size)
                self.v[0] = -1*self.v[0] 

            if self.r[1] > grid_size:
                self.r[1] = grid_size - (self.r[1] - grid_size)
                self.v[1] = -1*self.v[1] 

    # Code for adjusting people if they meet each other. Right now, reflections. Commented code was failed attempt at some variance of it.       
    def adjust(self):
        self.v *= -1
    
    def sickness(self):
        if not self.immune:
            self.healthy = False
            if self.future == 0:
                self.grave = sick_mid + np.random.randint(-daylength,daylength+1)


    def dying(self):
        self.alive = False
        # self.healthy = True
        self.immune = True
        self.r = np.array((-10,-10))
        self.v = np.array((0,0))

    def recovery(self):
        self.healthy = True
        self.immune = True


# Birthing People to infect them later. Avoiding putting them on the borders. Using variable people to count the number of infection machines made.
people = 0
infections = 0
deaths = 0
register = list()
swarm = int(grid_size / grid_spacing)
for i in range(swarm - 1):
    for j in range(swarm -1):
        x = (i+1)*grid_spacing
        y = (j+1)*grid_spacing
        r = np.array((x,y),float)
        v = np.array(np.random.randn(2) ,float)
        register.append(Person(r,v))
        people = people + 1

sickness_ammo = np.random.randint(0,people)
sickness_gun = register[sickness_ammo].sickness()

# Bluntly, copying and pasting code from animate.py.
handles = list()
fig, ax = plt.subplots()

for i in range(people):
    handle = ax.scatter(register[i].r[0], register[i].r[1])
    handles.append(handle)


ax.set(xlim=[0, grid_size+1], ylim=[0,grid_size+1], xlabel='x', ylabel='y')
ax.legend()

start = time.time()
#def update(frame):
for frame in range(500):
    #global deaths, infections

    ax.set_title(f"{frame * deltat}")
    for i,handle in zip(range(len(register)),handles):
        p1 = register[i]
        p1.move(deltat)
        handle.set_offsets([p1.r[0],p1.r[1]])
        if p1.healthy:
            handle.set_facecolor("g")
        else:
            handle.set_facecolor("r")
        if not p1.alive:
            continue
        # A look ahead I guess 
        for j in range(i+1,len(register)):
            p2 = register[j]
            distance = (p1.r - p2.r)**2
            condition = np.sqrt(distance[0] + distance[1])
            if condition < scl_dist:
                #This will be where the pandemic can spread
                if (not p1.healthy or not p2.healthy):
                    gambling = np.random.randint(1,3)
                    if gambling % 2 == 0:
                        if (p1.healthy and not p1.immune):
                            p1.sickness()
                            infections += 1
                        elif (p2.healthy and not p2.immune):
                            p2.sickness()
                            infections += 1
            if condition < 3:
                p1.adjust()
                p2.adjust()

                adjustment = np.random.randint(1,4)
                adjustment *= 10
                adjustment = np.deg2rad(adjustment)
                v1 = np.array((1,1),float)
                v2 = np.array((1,1),float)
                v1[0] = p1.v[0]*np.cos(adjustment) + p1.v[1] * np.sin(adjustment)
                v1[1] = -p1.v[0]*np.sin(adjustment) + p1.v[1]* np.cos(adjustment)
                
                v2[0] = p2.v[0]*np.cos(adjustment) - p2.v[1] * np.sin(adjustment)
                v2[1] =  p2.v[0]*np.sin(adjustment) + p2.v[1]* np.cos(adjustment)
                p1.v = v1
                p2.v = v2
            elif condition < 1:
                p1.adjust()
                p2.adjust()





        # Killing people
        if (not p1.healthy and not p1.immune  and p1.alive):
            # print(p1.counter, death_chance[p1.counter])
            if (p1.counter == p1.grave):
                p1.dying()
                deaths += 1
            else:
                p1.counter += 1
        # Make people immune if they didn't die.
            if (p1.counter >= sick_time):
                p1.recovery()
                # print(frame, "No")

# set color is to get the color
    
# ani = animation.FuncAnimation(fig=fig, func=update, frames=500, interval=100)

# writer = animation.PillowWriter(fps=15,
#                                  metadata=dict(artist='Me'),
#                                  bitrate=1800)
# #ani.save('scatter.gif', writer=writer)
# plt.show()

print(people,infections, deaths)
print(time.time() - start)