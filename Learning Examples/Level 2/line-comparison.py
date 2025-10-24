import matplotlib.pyplot as plt

# Plotting multiple lines allows comparison of trends
# Define data: quarters and sales for two companies
quarters = ['Q1', 'Q2', 'Q3', 'Q4']
company_a = [100, 120, 145, 160]
company_b = [95, 110, 125, 155]

# Create figure and axis
fig, ax = plt.subplots()

# Plot both lines with different colors and styles
ax.plot(quarters, company_a, marker='s', linewidth=2.5, 
        markersize=8, color='#FF6B6B', label='Company A')

ax.plot(quarters, company_b, marker='o', linewidth=2.5, 
        markersize=8, color='#4D96FF', label='Company B')

# Customize appearance
ax.set_xlabel('Quarter', fontsize=12, fontweight='bold')
ax.set_ylabel('Sales (in thousands)', fontsize=12, fontweight='bold')
ax.set_title('Sales Comparison: Company A vs B', fontsize=14, fontweight='bold')

# Add grid for easier comparison
ax.grid(True, alpha=0.3, linestyle='--')

# Add legend to distinguish lines
ax.legend(fontsize=11, loc='upper left')

plt.tight_layout()
plt.show()