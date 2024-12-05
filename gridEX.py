import numpy as np
import matplotlib.pyplot as plt

# Assuming `test` contains the binary string (must be a multiple of 8 for an 8x8 grid)
test = "1111111100000000111111110000000011111111000000001111111100000000"  # Example binary data

# Define the grid size
grid_size = 8

# Validate test length
if len(test) % grid_size != 0:
    print("Error: Binary string length must be a multiple of", grid_size)
else:
    # Convert binary string into a 2D numpy array
    grid = np.array(list(test), dtype=int).reshape(grid_size, grid_size)

    # Plot the grid
    plt.imshow(grid, cmap='gray', interpolation='nearest')
    plt.axis('off')  # Hide the axis
    plt.title("Binary Grid Visualization")
    plt.show()