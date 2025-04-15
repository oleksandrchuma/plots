import matplotlib.pyplot as plt
import numpy as np

# For 3D plotting in older Matplotlib versions, you may need:
# from mpl_toolkits.mplot3d import Axes3D

# 1. Create the 3D figure and axis
fig = plt.figure()
ax = fig.add_subplot(projection='3d')

# 2. Turn off the axis lines and grid
ax.set_axis_off()

# 3. Define the vectors you want to draw
b1 = np.array([1, 0, 0])
b2 = np.array([0, 1, 0])
b3 = np.array([0, 0, 1])

# 4. Plot each vector starting at (0,0,0)
# The arrow_length_ratio adjusts the size of the arrowhead
qb1 = ax.quiver(0, 0, 0, b1[0], b1[1], b1[2],  color='black', arrow_length_ratio=0.1)
qb2 = ax.quiver(0, 0, 0, b2[0], b2[1], b2[2],  color='black', arrow_length_ratio=0.1)
qb3 = ax.quiver(0, 0, 0, b3[0], b3[1], b3[2],  color='black', arrow_length_ratio=0.1)
qb1.set_linewidth(0.5)
qb2.set_linewidth(0.5)
qb3.set_linewidth(0.5)
# 5. Optionally, label the tips of the vectors
ax.text(*b1, "b1", color='black')
ax.text(*b2, "b2", color='black')
ax.text(*b3, "b3", color='black')

ax.set_xlim([0, 2])
ax.set_ylim([2, 0])
ax.set_zlim([0, 2])

points = {
    "Γ": [0.0,  0.0,  0.0 ],
    "H": [0.5, -0.5,  0.5 ],
    "N": [0.0,  0.0,  0.5 ],
    "P": [0.25, 0.25, 0.25]
}
path_labels = ["Γ", "H", "N", "Γ", "P", "H"]
coords = np.array([points[label] for label in path_labels])
x = coords[:, 0]
y = coords[:, 1]
z = coords[:, 2]
ox, oy, oz = 0,0,0

ax.plot([0.5,0.5], [-0.5,-0.5], [0.5,0], color='blue', linewidth=0.5)
ax.plot([0.25,0.25], [0.25,0.25], [0.25,0], color='blue', linewidth=0.5)
ax.plot([0.0,0.25], [0.0,0.25], [0.0,0], color='blue', linewidth=0.5)
ax.plot([0.,0.5], [0.0,-0.5], [0,0], color='blue', linewidth=0.5)
for label in path_labels:  # skip the repeated last
    px, py, pz = points[label]
    xs = [ox, px]
    ys = [oy, py]
    zs = [oz, pz]

    ax.plot(xs, ys, zs, color='red', linewidth=3)
    #ax.text(px, py, pz, f"{label}", color='black')
    ox, oy, oz = px, py, pz
plt.show()