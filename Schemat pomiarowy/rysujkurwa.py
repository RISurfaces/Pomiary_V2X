import matplotlib.pyplot as plt
import numpy as np

# Parameters
angle_start = -43.2
angle_end = 43.2
angle_step = 4.8
radius = 2
# Generate angles and coordinates
angles = np.arange(
    np.radians(angle_start), np.radians(angle_end), np.radians(angle_step)
)  # Adjust to exclude the extra angle
x = np.sin(angles) * radius  # Swap x and y calculation to rotate 180 degrees
y = -np.cos(angles) * radius

# Create figure and axis
fig, ax = plt.subplots()
ax.set_aspect("equal", adjustable="datalim")

# Draw the semicircle
circle = plt.Circle((0, 0), radius, color="lightgray", fill=False)
ax.add_artist(circle)

# Plot the angles
for angle, x_coord, y_coord in zip(angles, x, y):
    ax.plot([0, x_coord], [0, y_coord], "k-", lw=1)
    ax.text(
        x_coord * 1.1,
        y_coord * 1.1,
        f"{np.degrees(angle):.1f}°",
        ha="center",
        va="center",
        fontsize=8,
    )

# Highlight the central angle
center_x = np.sin(0) * radius  # Adjust for rotation
center_y = -np.cos(0) * radius
ax.plot([0, center_x], [0, center_y], "r-", lw=2, label="0°")

# Styling
ax.axhline(0, color="black", linewidth=0.5, linestyle="--")
ax.axvline(0, color="black", linewidth=0.5, linestyle="--")
ax.set_xlim(-4, 4)
ax.set_ylim(-4, 4)
ax.axis("off")

# Show the plot
plt.legend()
plt.show()
fig.savefig("myimage.svg", format="svg", dpi=1200)
