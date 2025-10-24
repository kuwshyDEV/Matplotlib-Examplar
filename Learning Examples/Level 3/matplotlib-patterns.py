import matplotlib.pyplot as plt
import numpy as np

# Create visual patterns using mathematical functions

fig, ax = plt.subplots(figsize=(9, 9))

# Generate a grid of points
x = np.linspace(-3, 3, 500)
y = np.linspace(-3, 3, 500)
X, Y = np.meshgrid(x, y)

# Create pattern using mathematical formula (creates ripple effect)
Z = np.sin(np.sqrt(X**2 + Y**2)) * np.cos(X) * np.sin(Y)

# Display pattern using contourf (filled contour plot)
contour = ax.contourf(X, Y, Z, levels=20, cmap='twilight')

# Add colorbar to show value scale
cbar = plt.colorbar(contour, ax=ax)
cbar.set_label('Intensity', fontsize=10)

# Add contour lines for more detail
ax.contour(X, Y, Z, levels=10, colors='black', linewidths=0.5, alpha=0.3)

ax.set_xlabel('X', fontsize=11, fontweight='bold')
ax.set_ylabel('Y', fontsize=11, fontweight='bold')
ax.set_title('Mathematical Pattern: Ripple & Wave Effect', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.show()