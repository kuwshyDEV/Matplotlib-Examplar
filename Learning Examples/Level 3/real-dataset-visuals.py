import matplotlib.pyplot as plt
import pandas as pd

# This script reads data from 'sales_data.xlsx' and creates visualizations
# Make sure the Excel file is in the same directory as this script

try:
    # Read the Excel file
    df = pd.read_excel('Learning Examples\Level 3\data\sales_data.xlsx')
    
    # Display first few rows to understand data
    print("Data Preview:")
    print(df.head())
    print("\nData Info:")
    print(df.info())
    
except FileNotFoundError:
    print("Error: 'sales_data.xlsx' not found! Please ensure the file is in the same directory.")
    exit()

# Create 1x2 subplot layout for two different visualizations
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Chart 1: Total Sales by Product (Bar chart)
product_sales = df.groupby('Product')['Sales'].sum().sort_values(ascending=False)
axes[0].bar(product_sales.index, product_sales.values, color='#FF6B6B', edgecolor='black')
axes[0].set_title('Total Sales by Product', fontsize=12, fontweight='bold')
axes[0].set_xlabel('Product', fontweight='bold')
axes[0].set_ylabel('Sales ($)', fontweight='bold')
axes[0].tick_params(axis='x', rotation=45)
axes[0].grid(axis='y', alpha=0.3)

# Chart 2: Sales Trend Over Time (Line plot)
# Assumes data has 'Date' and 'Sales' columns
daily_sales = df.groupby('Date')['Sales'].sum()
axes[1].plot(daily_sales.index, daily_sales.values, marker='o', 
             linewidth=2, color='#4D96FF', markersize=5)
axes[1].set_title('Sales Trend Over Time', fontsize=12, fontweight='bold')
axes[1].set_xlabel('Date', fontweight='bold')
axes[1].set_ylabel('Sales ($)', fontweight='bold')
axes[1].tick_params(axis='x', rotation=45)
axes[1].grid(True, alpha=0.3)

# Adjust layout to prevent label cutoff
plt.tight_layout()
plt.show()

# Display basic statistics
print("\n--- Sales Statistics ---")
print(f"Total Sales: ${df['Sales'].sum():,.2f}")
print(f"Average Sale: ${df['Sales'].mean():,.2f}")
print(f"Highest Sale: ${df['Sales'].max():,.2f}")