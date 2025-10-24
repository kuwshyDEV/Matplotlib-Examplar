import matplotlib.pyplot as plt

# Bar charts are great for comparing discrete categories
# Define data: categories and their corresponding values
fruits = ['Apple', 'Banana', 'Orange', 'Mango']
sales = [45, 38, 52, 41]

# Create a figure and axis object
fig, ax = plt.subplots()

# Create the bar chart
# 'fruits' is x-axis, 'sales' is height of bars, 'color' customizes appearance
ax.bar(fruits, sales, color='skyblue', edgecolor='navy', linewidth=1.5)

# Add labels and title for clarity
ax.set_xlabel('Fruit Type', fontsize=12, fontweight='bold')
ax.set_ylabel('Sales (units)', fontsize=12, fontweight='bold')
ax.set_title('Fruit Sales Comparison', fontsize=14, fontweight='bold')

# Add a grid for easier reading
ax.grid(axis='y', alpha=0.3, linestyle='--')

# Display the chart
plt.tight_layout()
plt.show()