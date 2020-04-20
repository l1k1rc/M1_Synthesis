import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


def f(x, y):
    return 0.7*x+0.3*y+1


x = np.linspace(0, 7, 20)
y = np.linspace(0, 7, 20)

x, y = np.meshgrid(x, y)
ax.plot_wireframe(x, y, f(x, y), rstride=2, cstride=2)
ax.plot_wireframe(3, 2, f(x, y), rstride=2, cstride=2, color="red")
ax.plot_wireframe(27, 5, f(x, y), rstride=2, cstride=2, color="green")
ax.plot_wireframe(38, 27, f(x, y), rstride=2, cstride=2, color="blue")
ax.plot_wireframe(21, 45, f(x, y), rstride=2, cstride=2, color="red")
ax.plot_wireframe(32, 15, f(x, y), rstride=2, cstride=2, color="green")
ax.plot_wireframe(5, 2, f(x, y), rstride=2, cstride=2, color="blue")
ax.plot_wireframe(8, 5, f(x, y), rstride=2, cstride=2, color="green")
ax.plot_wireframe(16, 5, f(x, y), rstride=2, cstride=2, color="green")
ax.plot_wireframe(11, 19, f(x, y), rstride=2, cstride=2, color="green")
ax.plot_wireframe(45, 80, f(x, y), rstride=2, cstride=2, color="green")


plt.show()