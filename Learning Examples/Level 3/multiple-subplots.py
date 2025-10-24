import matplotlib.pyplot as plt
import numpy as np

# Subplots allow multiple charts in one figure
# plt.subplots(rows, cols) creates a grid of charts

# Create 2x2 grid of subplots
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Flatten axes for easier indexing (converts 2D array to 1D)
axes = axes.flatten()

# Subplot 1: Bar chart
categories = ['A', 'B', 'C', 'D']
values = [23, 45, 56, 78]
axes[0].bar(categories, values, color='#FF6B6B')
axes[0].set_title('Bar Chart', fontweight='bold')
axes[0].set_ylabel('Values')

# Subplot 2: Line plot
x = np.linspace(0, 10, 100)
y = np.sin(x)
axes[1].plot(x, y, linewidth=2, color='#4D96FF')
axes[1].set_title('Line Plot (Sin Wave)', fontweight='bold')
axes[1].grid(True, alpha=0.3)

# Subplot 3: Scatter plot
x_scatter = np.random.rand(50) * 10
y_scatter = np.random.rand(50) * 10
axes[2].scatter(x_scatter, y_scatter, color='#6BCB77', s=100, alpha=0.6)
axes[2].set_title('Scatter Plot', fontweight='bold')
axes[2].set_xlabel('X')
axes[2].set_ylabel('Y')

# Subplot 4: Histogram
data = np.random.normal(0, 1, 1000)
axes[3].hist(data, bins=30, color='#FFD93D', edgecolor='black')
axes[3].set_title('Histogram (Normal Distribution)', fontweight='bold')
axes[3].set_xlabel('Value')
axes[3].set_ylabel('Frequency')

# Add overall title
fig.suptitle('Multiple Subplots Example', fontsize=16, fontweight='bold', y=0.995)

# Adjust spacing between subplots
plt.tight_layout()
plt.show()