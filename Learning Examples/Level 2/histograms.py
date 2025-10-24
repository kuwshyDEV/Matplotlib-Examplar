import matplotlib.pyplot as plt
import numpy as np

# Histograms show distribution of continuous data
# They group data into "bins" (ranges) and show frequency

# Generate random test scores (simulating student performance)
np.random.seed(42)  # For reproducibility
test_scores = np.random.normal(loc=75, scale=12, size=100)  # Mean=75, StdDev=12

# Create figure and axis
fig, ax = plt.subplots()

# Create histogram
# bins=15 divides data into 15 ranges, edgecolor adds borders to bars
ax.hist(test_scores, bins=15, color='#7C3AED', 
        edgecolor='black', alpha=0.7)

# Customize labels
ax.set_xlabel('Test Score', fontsize=12, fontweight='bold')
ax.set_ylabel('Number of Students', fontsize=12, fontweight='bold')
ax.set_title('Distribution of Test Scores', fontsize=14, fontweight='bold')

# Add grid for reference
ax.grid(axis='y', alpha=0.3, linestyle='--')

# Add a vertical line showing the mean
mean_score = np.mean(test_scores)
ax.axvline(mean_score, color='red', linestyle='--', 
           linewidth=2, label=f'Mean: {mean_score:.1f}')

ax.legend(fontsize=10)

plt.tight_layout()
plt.show()