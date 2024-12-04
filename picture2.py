import numpy as np
import matplotlib.pyplot as plt

# Step 1: Create an 8x8 grid of white squares (all set to 1)
grid = np.ones((8, 8))

# C
grid[2, 2:5] = 0
grid[3, 2] = 0
grid[4, 2:5] = 0

# U
grid[5:8, 5] = 0
grid[7, 6] = 0
grid[5:8, 7] = 0

plt.imshow(grid, cmap='gray', interpolation='nearest')
plt.axis('off')  # Hide the axis
plt.show()
