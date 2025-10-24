import matplotlib.pyplot as plt
import numpy as np

# Scatter plots show relationship between two variables
# Each point represents an individual data item

# Generate study hours and test scores (simulating correlation)
np.random.seed(42)
study_hours = np.random.uniform(0, 10, 50)  # Random hours between 0-10
test_scores = 40 + 8 * study_hours + np.random.normal(0, 5, 50)  # Scores improve with hours

# Create figure and axis
fig, ax = plt.subplots()

# Create scatter plot
# s controls point size, alpha controls transparency
ax.scatter(study_hours, test_scores, s=100, color='#6BCB77', 
           alpha=0.6, edgecolors='darkgreen', linewidth=1)

# Customize labels
ax.set_xlabel('Study Hours', fontsize=12, fontweight='bold')
ax.set_ylabel('Test Score', fontsize=12, fontweight='bold')
ax.set_title('Relationship: Study Hours vs Test Score', fontsize=14, fontweight='bold')

# Add grid for reference
ax.grid(True, alpha=0.3, linestyle='--')

# Optional: Add a trend line to show the relationship
z = np.polyfit(study_hours, test_scores, 1)  # Linear fit
p = np.poly1d(z)
ax.plot(study_hours, p(study_hours), 'r--', linewidth=2, label='Trend')

ax.legend(fontsize=10)

plt.tight_layout()
plt.show()