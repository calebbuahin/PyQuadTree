__author__ = 'calebbuahin'

import random
import numpy as np
import matplotlib.pyplot as plt
import time
from QuadTree import  Triangle , QuadTree , GObject

np.random.seed(0)


triangles = np.ones((150*3,2))

for i in range(0, len(triangles), 3):
    triangles[i:i+3,0] *= random.uniform(0, 100)
    triangles[i:i+3,1] *= random.uniform(0, 100)
    triangles[i,0] -= 2
    triangles[i+1,0] += 2
    triangles[i+2,1] += 2

my_points =[np.array([random.uniform(0,100), random.uniform(0,100)]) for i in range(0,1000)]

triobjects =[]

for i in range(0, len(triangles),3):
    triobjects.append(Triangle(triangles[i,:], triangles[i+1,:], triangles[i+2,:] ))

mins = triangles.min(axis=0) - 0.0001
maxs = triangles.max(axis=0) + 0.0001


fig1 = plt.figure(figsize=(20, 10))
ax = plt.subplot(1,2,1)
ax2 = plt.subplot(1,2,2)
plt.ion()
plt.show()


from matplotlib import cm

MAX_OBJECTS = 5

for d in range(2,10):

    ax = plt.subplot(1,2,1)
    ax2 = plt.subplot(1,2,2)

    print 'Depth = %d' % d

    st = time.time()
    # build quadtree
    print 'Building QuadTree...',

    quadtree = QuadTree(d,[ mins[0], maxs[0], mins[1], maxs[1]], MAX_OBJECTS)

    quadtree.clear_gobjects();

    colors = []
    for i in range(d):
        colors.append(cm.Blues(1.*i/d) )

    level = quadtree.get_minlevel()
    plt.title('Level '+str(level))
    plotted_bounds = []

    for t in triobjects:
        quadtree.insert_gobject(t)
        bounds = []
        quadtree.getBounds(bounds)
        ax.plot([t.P1[0], t.P2[0], t.P3[0], t.P1[0]],
                [t.P1[1], t.P2[1], t.P3[1], t.P1[1]])
        # plt.draw()

        level = quadtree.get_minlevel()
        plt.title('Level '+str(level))

        for b in bounds:
            ax.plot(b[0], b[1] , color = "r")

    plt.draw()



    print '%3.5f sec' % (time.time() - st)

    st = time.time()
    print 'Searching QuadTree...',
    found = 0
    for p in my_points:
        res = quadtree.find_gobject_that_contains(p)
        if res is not None:
            bounds = []
            res[0].getBounds(bounds)
            for b in bounds:
                ax2.plot(b[0], b[1], 'k-')

            t = res[1]
            ax2.plot([t.P1[0], t.P2[0], t.P3[0], t.P1[0]],
                [t.P1[1], t.P2[1], t.P3[1], t.P1[1]])

            ax2.plot(p[0], p[1], 'g+')

            plt.draw()
            found += 1
    print '%3.5f sec' % (time.time() - st)
    print 'Found %d triangles\n\n'%found