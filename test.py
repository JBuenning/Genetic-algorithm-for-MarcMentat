import matplotlib.pyplot as plt

a = [(0,0),(1,1),(2,2)]

plt.scatter(*zip(*a))
plt.show()