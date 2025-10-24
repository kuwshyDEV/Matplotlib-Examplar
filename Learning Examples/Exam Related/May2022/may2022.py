import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ============================================================================
# NEWHAVEN PROPERTY INVESTMENTS - DATA SERVICE SOLUTION
# Task 4a: Developing a solution for property value trend analysis
# ============================================================================

# Load the CSV data - contains property value percentage increases by region
try:
    df = pd.read_csv('Learning Examples\Exam Related\May2022\Task_4a.csv')
    print("✓ Data loaded successfully\n")
except FileNotFoundError:
    print("Error: Task4a_data.csv not found!")
    exit()

# ============================================================================
# FUNCTION 1: Display available regions for user selection
# ============================================================================
def get_available_regions():
    """
    Extract unique regions from the dataset for user selection.
    This promotes usability by showing valid options.
    """
    regions = df['Region'].unique()
    return regions

# ============================================================================
# FUNCTION 2: Filter data for selected region
# ============================================================================
def get_region_data(region_name):
    """
    Filters the dataset for a specific region.
    Secure approach: validates region exists before filtering to prevent errors.
    """
    # Validate that the region exists (security: prevent invalid input)
    if region_name not in df['Region'].values:
        return None
    
    region_data = df[df['Region'] == region_name]
    return region_data

# ============================================================================
# FUNCTION 3: Calculate overall region increase (highest performer)
# ============================================================================
def find_highest_performing_region():
    """
    Identifies the region with the highest overall increase in property value.
    Calculates the mean of all values for each region to determine overall trend.
    """
    # Group by region and calculate mean percentage increase across all properties
    region_means = df.groupby('Region').iloc[:, 4:].mean(axis=1).groupby(df['Region']).mean()
    
    # Find region with highest average increase
    highest_region = region_means.idxmax()
    highest_value = region_means.max()
    
    return highest_region, highest_value

# ============================================================================
# FUNCTION 4: Extract property types for selected region
# ============================================================================
def get_property_types_in_region(region_name):
    """
    Returns all property types available in the selected region.
    Allows users to view trends for specific property types.
    """
    region_data = get_region_data(region_name)
    if region_data is None:
        return []
    
    property_types = region_data['Property Type'].unique()
    return property_types

# ============================================================================
# FUNCTION 5: Extract room numbers for property type
# ============================================================================
def get_room_sizes_for_property(region_name, property_type):
    """
    Returns available room sizes for a specific property type in a region.
    Enables granular filtering for detailed analysis.
    """
    region_data = get_region_data(region_name)
    if region_data is None:
        return []
    
    # Filter for specific property type and get unique room counts
    property_data = region_data[region_data['Property Type'] == property_type]
    rooms = property_data['Rooms'].unique()
    return sorted(rooms)

# ============================================================================
# FUNCTION 6: Get time series data for visualization
# ============================================================================
def get_time_series_data(region_name, property_type, rooms):
    """
    Extracts time series data (monthly values) for a specific property.
    Month columns start from index 4 (after Region Code, Region, Property Type, Rooms).
    """
    region_data = get_region_data(region_name)
    if region_data is None:
        return None, None
    
    # Filter for specific property criteria
    filtered = region_data[
        (region_data['Property Type'] == property_type) & 
        (region_data['Rooms'] == rooms)
    ]
    
    if filtered.empty:
        return None, None
    
    # Extract time series values (all columns from index 4 onwards are months)
    # Convert to float to ensure numeric values for plotting and calculations
    time_series = filtered.iloc[0, 4:].values.astype(float)
    
    # Create month labels (Jan-19 to May-22)
    month_labels = df.columns[4:].tolist()
    
    return month_labels, time_series

# ============================================================================
# FUNCTION 7: Display textual output (meaningful information)
# ============================================================================
def display_region_summary(region_name):
    """
    Provides textual output summarizing key statistics for the region.
    Makes information meaningful for end users through clear formatting.
    """
    region_data = get_region_data(region_name)
    if region_data is None:
        print(f"Region '{region_name}' not found.")
        return
    
    print("\n" + "="*70)
    print(f"REGION ANALYSIS: {region_name.upper()}")
    print("="*70)
    
    # Calculate overall statistics for the region
    month_data = region_data.iloc[:, 4:].values
    
    print(f"\nTotal Property Records: {len(region_data)}")
    print(f"Average Value Increase (Overall): {np.mean(month_data):.3f}")
    print(f"Maximum Value Increase: {np.max(month_data):.3f}")
    print(f"Minimum Value Increase: {np.min(month_data):.3f}")
    print(f"Standard Deviation: {np.std(month_data):.3f}")
    
    # Display breakdown by property type
    print(f"\nProperty Types in {region_name}:")
    print("-" * 70)
    
    for prop_type in region_data['Property Type'].unique():
        prop_data = region_data[region_data['Property Type'] == prop_type]
        avg_increase = np.mean(prop_data.iloc[:, 4:].values)
        count = len(prop_data)
        print(f"  • {prop_type}: {count} records | Avg increase: {avg_increase:.3f}")

# ============================================================================
# FUNCTION 8: Visualize trends over time
# ============================================================================
def plot_property_trend(region_name, property_type, rooms):
    """
    Creates a line chart showing property value trends over time.
    Graphical output makes trends easily identifiable for end users.
    """
    month_labels, time_series = get_time_series_data(region_name, property_type, rooms)
    
    if time_series is None:
        print(f"No data found for {property_type} with {rooms} rooms in {region_name}.")
        return
    
    # Create figure with professional styling
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot line with markers for clear data point visibility
    ax.plot(month_labels, time_series, marker='o', linewidth=2.5, 
            markersize=6, color='#2E86AB', label=f'{property_type} ({rooms} rooms)')
    
    # Add trend line (polynomial fit) to show overall pattern
    x_numeric = np.arange(len(month_labels))
    z = np.polyfit(x_numeric, time_series, 2)  # Quadratic trend line
    p = np.poly1d(z)
    ax.plot(month_labels, p(x_numeric), '--', color='#A23B72', 
            linewidth=2, label='Trend', alpha=0.7)
    
    # Customize appearance for clarity
    ax.set_xlabel('Month', fontsize=12, fontweight='bold')
    ax.set_ylabel('Property Value Increase (%)', fontsize=12, fontweight='bold')
    ax.set_title(f'Property Value Trend: {region_name} - {property_type} ({rooms} rooms)', 
                 fontsize=13, fontweight='bold', pad=15)
    
    # Rotate x-axis labels for readability
    ax.tick_params(axis='x', rotation=45)
    
    # Add grid for easier reading
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Add legend
    ax.legend(fontsize=10, loc='best')
    
    plt.tight_layout()
    plt.show()

# ============================================================================
# FUNCTION 9: Compare multiple properties in region
# ============================================================================
def plot_region_comparison(region_name):
    """
    Creates a comprehensive chart comparing all property types in a region.
    Enables meaningful comparison of trends across property types.
    """
    region_data = get_region_data(region_name)
    if region_data is None:
        print(f"Region '{region_name}' not found.")
        return
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    # Extract month labels
    month_labels = df.columns[4:].tolist()
    
    # Plot each property type with different color
    colors = ['#FF6B6B', '#4D96FF', '#6BCB77', '#FFD93D', '#FF85A2']
    
    for idx, (prop_type, group) in enumerate(region_data.groupby('Property Type')):
        # Calculate mean values across all room sizes for this property type
        avg_values = group.iloc[:, 4:].mean()
        ax.plot(month_labels, avg_values, marker='o', linewidth=2.5, 
                markersize=5, label=prop_type, color=colors[idx % len(colors)])
    
    # Customize appearance
    ax.set_xlabel('Month', fontsize=12, fontweight='bold')
    ax.set_ylabel('Average Property Value Increase (%)', fontsize=12, fontweight='bold')
    ax.set_title(f'Property Type Comparison: {region_name}', 
                 fontsize=13, fontweight='bold', pad=15)
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(fontsize=10, loc='best')
    
    plt.tight_layout()
    plt.show()

# ============================================================================
# MAIN INTERACTIVE MENU
# ============================================================================
def main_menu():
    """
    Interactive menu providing easy-to-use interface for end users.
    Allows navigation through analysis options with clear prompts.
    """
    while True:
        print("\n" + "="*70)
        print("NEWHAVEN PROPERTY INVESTMENTS - DATA SERVICE")
        print("="*70)
        print("\nSelect an option:")
        print("  1. View region summary and statistics")
        print("  2. View property type trend (graphical)")
        print("  3. Compare all property types in a region")
        print("  4. Find highest performing region")
        print("  5. Exit")
        print("-"*70)
        
        choice = input("Enter your choice (1-5): ").strip()
        
        # Option 1: Region summary
        if choice == '1':
            available_regions = get_available_regions()
            print(f"\nAvailable regions: {', '.join(available_regions)}")
            region = input("Enter region name: ").strip()
            display_region_summary(region)
        
        # Option 2: Property trend visualization
        elif choice == '2':
            available_regions = get_available_regions()
            print(f"\nAvailable regions: {', '.join(available_regions)}")
            region = input("Enter region name: ").strip()
            
            property_types = get_property_types_in_region(region)
            if len(property_types) > 0:
                print(f"Property types: {', '.join(property_types)}")
                prop_type = input("Enter property type: ").strip()
                
                rooms = get_room_sizes_for_property(region, prop_type)
                if len(rooms) > 0:
                    print(f"Available room sizes: {rooms}")
                    room_input = int(input("Enter number of rooms: "))
                    plot_property_trend(region, prop_type, room_input)
        
        # Option 3: Region comparison
        elif choice == '3':
            available_regions = get_available_regions()
            print(f"\nAvailable regions: {', '.join(available_regions)}")
            region = input("Enter region name: ").strip()
            plot_region_comparison(region)
        
        # Option 4: Highest performing region
        elif choice == '4':
            highest_region, highest_value = find_highest_performing_region()
            print(f"\nHighest Performing Region: {highest_region}")
            print(f"Average Increase: {highest_value:.3f}")
        
        # Option 5: Exit
        elif choice == '5':
            print("\nThank you for using Newhaven Property Investments Data Service.")
            break
        
        else:
            print("Invalid choice. Please select 1-5.")

# ============================================================================
# EXECUTION
# ============================================================================
if __name__ == "__main__":
    main_menu()