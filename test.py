import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(111)

theta = np.linspace(-np.pi, np.pi, 100)
ax.plot(theta, np.sin(theta), label='sin') 
ax.plot(theta, np.tan(theta), label='tan') 
ax.set_xlabel('x')
ax.set_ylabel('y')
plt.show()
