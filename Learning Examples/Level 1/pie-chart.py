import matplotlib.pyplot as plt

# Pie charts show parts of a whole (percentages)
# Define data: categories and sizes
programming_languages = ['Python', 'JavaScript', 'Java', 'C++']
usage_percentage = [35, 28, 20, 17]

# Colors for each slice (optional but makes it prettier)
colors = ['#FFD93D', '#6BCB77', '#4D96FF', '#FF6B9D']

# Create figure and axis
fig, ax = plt.subplots()

# Create pie chart
# autopct='%1.1f%%' displays percentage on each slice
wedges, texts, autotexts = ax.pie(usage_percentage, 
                                    labels=programming_languages,
                                    autopct='%1.1f%%',
                                    colors=colors,
                                    startangle=90,
                                    textprops={'fontsize': 10})

# Make percentage text bold for better visibility
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')

# Add title
ax.set_title('Programming Language Usage', fontsize=14, fontweight='bold', pad=20)

plt.tight_layout()
plt.show()