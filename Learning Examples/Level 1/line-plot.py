import matplotlib.pyplot as plt

# Line plots show trends over continuous data (like time)
# Define data: months and temperature readings
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
temperature = [5, 7, 12, 18, 22, 25]

# Create figure and axis
fig, ax = plt.subplots()

# Plot line chart
# marker='o' adds dots at each point, linewidth controls thickness
ax.plot(months, temperature, marker='o', linewidth=2.5, 
        markersize=8, color='#FF6B6B', label='Temperature')

# Customize the appearance
ax.set_xlabel('Month', fontsize=12, fontweight='bold')
ax.set_ylabel('Temperature (°C)', fontsize=12, fontweight='bold')
ax.set_title('Monthly Temperature Trend', fontsize=14, fontweight='bold')

# Add grid for reference
ax.grid(True, alpha=0.3, linestyle='--')

# Add legend (useful when multiple lines exist)
ax.legend(fontsize=10)

plt.tight_layout()
plt.show()