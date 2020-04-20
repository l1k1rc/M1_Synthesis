import numpy as np
import matplotlib.pyplot as plt


def f(x, y):
    return 0.7*x+0.3*y

x = np.linspace(-6, 6, 30)
y = np.linspace(-6, 6, 30)

X, Y = np.meshgrid(x, y)
Z = f(X, Y)

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.contour3D(X, Y, Z, 50, cmap='binary')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

# Data for three-dimensional scattered points
zdata = 15 * np.random.random(20)
xdata = 5
ydata = 6
ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='Greens');


plt.show()