import numpy as np

def ThePlague(length, masked = 0, grid_spacing = 0.1, sick_days = 10, speed_factor = 800):
    
    class Person(object):

    # First, create a person with some position, r, and some velocity, v. These should be 2 dim arrays. Assume everyone is healthy and non-immune.
        def __init__(self,r,v):
            self.r = r
            self.v = v
            self.alive = True
            self.healthy = True
            self.immune = False
            self.counter = 0
            self.grave = 999
            self.future = np.random.randint(0,2) # if 0, person is destined to die
            self.masked = False

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

    # Dying means going off camera
        def dying(self):
            self.alive = False
            self.immune = True
            self.r = np.array((-10,-10))
            self.v = np.array((0,0))

        def recovery(self):
            self.healthy = True
            self.immune = True
            

    grid_size = 1
    deltat = 1
    timestep = 0
    scl_dist = 0.05
    minspeed = 5
    maxspeed = 10

    daylength = 12
    sick_time = daylength * sick_days
    sick_mid = sick_time / 2
    
    people = 0 
    deaths = 0
    register = list()
    swarm = int(grid_size / grid_spacing)
    ticktock = []
    reapers_list = []

    for i in range(swarm - 1):
        for j in range(swarm -1):
            x = (i+1)*grid_spacing
            y = (j+1)*grid_spacing
            r = np.array((x,y),float)

            # Minimum speed helps destick people in collisions; weird way to let velocities be negative
            speed1 = np.random.randint(-maxspeed,maxspeed+1)
            while np.abs(speed1) < minspeed:
                speed1 = np.random.randint(-maxspeed,maxspeed+1)
            speed2 = np.random.randint(-maxspeed,maxspeed+1)
            while np.abs(speed2) < minspeed:
                speed2 = np.random.randint(-maxspeed,maxspeed+1)
            speed = (speed1/speed_factor,speed2/speed_factor)

            v = np.array(speed,float)
            register.append(Person(r,v))
            people = people + 1
    if masked != 0:
        for i in range(masked):
            register[i].masked = True

    # Infect Patient Zero
    sickness_ammo = np.random.randint(0,people)
    register[sickness_ammo].sickness()
    infections = 1
    
    
    
    ##### The Main Pandemic Loop #####
    
    
    for frame in range(length):
        timestep += deltat
        ticktock.append(timestep)
        totalinfected = infections - deaths
        reapers_list.append(totalinfected)
        for i in range(len(register)):
            p1 = register[i]
            p1.move(deltat) 
        
            if not p1.alive:
                continue


            for j in range(i+1,len(register)):
                p2 = register[j]
                distance = (p1.r - p2.r)**2
                condition = np.sqrt(distance[0] + distance[1])
            # This is handling infections
                if condition < scl_dist:
                    if (not p1.healthy or not p2.healthy):
                        gambling = np.random.randint(1,11)
                        if (p1.masked and not p2.healthy) or (p2.masked and not p1.healthy):
                            illchance = 4
                        else:
                            illchance = 5
                        if gambling <= illchance:
                            if (p1.healthy and not p1.immune):
                                p1.sickness()
                                infections += 1
                            elif (p2.healthy and not p2.immune):
                                p2.sickness()
                                infections += 1
            #This is supposed to handle collisions; check if a component of their velocities is close to zero if they are close to one another. 
                if condition < 0.02:
                    addv = np.sqrt((p1.v + p2.v)**2)
                    if (addv[0] < 0.03):
                        p1.v[0] *= -1
                        p2.v[0] *= -1
                    if (addv[1] < 0.03):
                        p1.v[1] *= -1
                        p2.v[1] *= -1
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
                    infections -=1

    return people, infections, deaths, ticktock, reapers_list