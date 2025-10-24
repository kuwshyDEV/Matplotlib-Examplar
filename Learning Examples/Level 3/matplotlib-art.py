import matplotlib.pyplot as plt
import numpy as np

# Matplotlib is creative! We can draw artistic patterns using plotting functions

fig, ax = plt.subplots(figsize=(8, 8))

# Create concentric circles (art pattern)
for i in range(1, 11):
    # Draw circles with increasing radius
    circle = plt.Circle((0.5, 0.5), i/20, fill=False, 
                       color='#FF6B6B', linewidth=2, alpha=0.7)
    ax.add_patch(circle)

# Add scatter points in a spiral pattern (artistic effect)
theta = np.linspace(0, 4 * np.pi, 100)  # Angle from 0 to 4π
r = theta / (4 * np.pi)  # Radius increases with angle
x = 0.5 + r * np.cos(theta)
y = 0.5 + r * np.sin(theta)

ax.scatter(x, y, s=50, c=theta, cmap='viridis', alpha=0.8, edgecolors='black')

# Set equal aspect ratio so circles appear circular
ax.set_aspect('equal')
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')  # Hide axes for cleaner art

ax.set_title('Matplotlib Artistic Pattern', fontsize=14, fontweight='bold', pad=20)

plt.tight_layout()
plt.show()