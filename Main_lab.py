################ import ################

import numpy as np
import heapq
import math
import matplotlib.pyplot as plt
import numpy.random

plt.style.use("ggplot")

np.random.seed(0)

################ initialization ################

# setup
curr_time = 0
P = []
T = 600
Tp = 0
A = 0
E = 0
L = 0
Lq = []
H = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Q = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

################ assisting functions ################

# number of people in group generator
def quantify():
    perc_gen = np.random.uniform(0, 1)
    if perc_gen <= 0.3:
        return 3
    elif perc_gen >= 0.65:
        return 2
    else:
        return 1

################ classes ################

# create class for events
class Event():
    def __init__(self, time, eventType, group = None):
        self.time = time
        self.eventType = eventType
        self.group = group
        heapq.heappush(P, self)

    def __lt__(self, event2):
        return self.time < event2.time

# create class for single visitor
class Visitor():
    def __init__(self):
        self.height = np.random.normal(160,10)

# create class for groups
class Group():
    def __init__(self):
        self.rounds = 0
        self.quantity = quantify()
        self.visitors = []
        # create appropriate amount of visitors
        for i in range(self.quantity):
            self.visitors.append(Visitor())

################ first event ################

x = numpy.random.exponential(1.5)
first_group = Group()
Event(x, "arriving", first_group)

event = heapq.heappop(P)
curr_time = event.time

################ process ################

while curr_time < T:

    # event of arriving
    if event.eventType == "arriving":
        # document group in water park
        L += len(event.group.visitors)
        # tests
        print("group arrived at", curr_time, ", L is ", L, "Lq is ", Lq)
        print("the group has", len(event.group.visitors), "visitors")
        for i in range(len(event.group.visitors)):
            print(event.group.visitors[i].height)

        # line is longer than 5 visitors
        if len(Lq) > 5:
            event.group.rounds += 1
            Event(curr_time + 5, "walk around", event.group)
            print("line is too long, going for a spin")

        # line isn't over 5 visitors, group can enter slide or line
        # workers are busy, all visitors will enter line
        elif A == 2:
            for visitor in event.group.visitors:
                Lq.append(visitor)

        # worker is free, takes care of one of the visitors and the rest enter the line
        elif A == 1:
            A = 2
            # worker is free, but time of end of slide depends on group members
            # first visitor in group starts sliding event
            first_visitor = event.group.visitors[0]
            if first_visitor.height < 140:
                Event(curr_time + 1, "sliding")
                print("visitor is under 140, sliding event created")
            else:
                x = np.random.uniform(1.5, 2)
                if first_visitor.height <= 150:
                    z = np.random.uniform(0, 1)
                    if z <= 0.4:  # visitor is allowed
                        Event(curr_time + z, "sliding")
                        print("visitor is under 150 but got on, sliding event created")
                    else:
                        curr_time += 1
                        print("visitor is under 150 and kicked out, sliding event created")
                else:
                    Event(curr_time + x, "sliding")
                    print("visitor is over 150, sliding event created")

            # rest of the group enters line
            for visitor in event.group.visitors[1:]:
                heapq.heappush(Lq, (curr_time, visitor))

        # A == 0, both workers are free
        else:
            # group has one visitor
            if len(event.group.visitors) == 1:
                A = 1
                only_visitor = event.group.visitors[0]
                if only_visitor.height < 140:
                    Event(curr_time + 1, "sliding")
                    print("visitor is under 140, sliding event created")
                else:
                    x = np.random.uniform(1.5, 2)
                    if only_visitor.height <= 150:
                        z = np.random.uniform(0, 1)
                        if z <= 0.4:  # visitor is allowed
                            Event(curr_time + z, "sliding")
                            print("visitor is under 150 but got on, sliding event created")
                        else:
                            curr_time += 1
                            print("visitor is under 150 and kicked out, sliding event created")
                    else:
                        Event(curr_time + x, "sliding")
                        print("visitor is over 150, sliding event created")

            # group has two or three visitors
            if len(event.group.visitors) > 1:
                A = 2
                # enter two first visitors into line
                for i in range(2):
                    if event.group.visitors[i].height < 140:
                        Event(curr_time + 1, "sliding")
                        print("visitor is under 140, sliding event created")
                    else:
                        x = np.random.uniform(1.5, 2)
                        # visitor is between 140 and 150
                        if event.group.visitors[i].height <= 150:
                            z = np.random.uniform(0, 1)
                            if z <= 0.4:  # visitor is allowed
                                Event(curr_time + z, "sliding")
                                print("visitor is under 150 but got on, sliding event created")
                            else:
                                curr_time += 1
                                print("visitor is under 150 and kicked out, sliding event created")
                        # visitor is taller than 150
                        else:
                            Event(curr_time + x, "sliding")
                            print("visitor is over 150, sliding event created")
                # if group has a third member, he will enter line
                if len(event.group.visitors) > 2:
                    heapq.heappush(Lq, (event.group.visitors[2]))

        # regardless of sliding event, we must create the next arriving event
        if curr_time < 240:
            x = np.random.exponential(1.5)
            Event(curr_time + x, "arriving", Group())
        elif curr_time < 360:
            x = np.random.exponential(4)
            Event(curr_time + x, "arriving", Group())
        else:
            x = np.random.exponential(2)
            Event(curr_time + x, "arriving", Group())

    # event of walking around
    elif event.eventType == "walk_around":
        print("group is walking around")

    # event of sliding
    elif event.eventType == "sliding":
        print("group is sliding")

    # event of end of break for one of the workers
    elif event.eventType == "end_break":
        print("break is ending")

    # update variables for calculating final output
    H[math.floor(curr_time/60)] += ((len(Lq) * (T - Tp)) / 60)

    #setting up next event
    event = heapq.heappop(P)
    Tp = curr_time
    curr_time = event.time

