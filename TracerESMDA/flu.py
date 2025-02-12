import numpy as np
import matplotlib.pyplot as plt
from skimage.draw import ellipse
from skimage.draw import bezier_curve



def create_fluvial_channels(grid_size=(100, 100), n_channels=3, channel_width=5, sinuosity=0.3):
    """
    Generates a 2D fluvial facies model with sinuous channels.
    """
    facies = np.zeros(grid_size, dtype=int)
    ny, nx = grid_size

    for _ in range(n_channels):
        # Random starting position
        x_start = np.random.randint(0, nx)
        y_start = np.random.randint(0, ny)

        # Generate a sinusoidal centerline
        x = np.linspace(x_start, nx - 1, 100)
        y = y_start + sinuosity * ny * np.sin(2 * np.pi * (x - x_start) / nx)

        # Draw channel along the centerline
        for xi, yi in zip(x, y):
            rr, cc = ellipse(int(yi), int(xi), channel_width, channel_width, shape=(ny, nx))
            facies[rr, cc] = 1  # Channel facies = 1



    return facies

# Generate and plot
facies = create_fluvial_channels(grid_size=(200, 200), n_channels=5, sinuosity=0.2)
plt.imshow(facies, cmap="viridis")
plt.title("Object-Based Fluvial Channels")
plt.show()