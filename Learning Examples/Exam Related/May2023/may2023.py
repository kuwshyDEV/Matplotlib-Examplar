import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# ============================================================================
# GURREB'S BBQ - SALES DATA SERVICE SOLUTION
# Task 4a: Developing a solution for menu item sales trend analysis
# ============================================================================

# Load the CSV data - contains menu item sales for lunch and dinner services
try:
    df = pd.read_csv('Learning Examples\Exam Related\May2023\Task4a_data.csv')
    print("✓ Data loaded successfully\n")
except FileNotFoundError:
    print("Error: Task4a_data.csv not found!")
    exit()

# ============================================================================
# FUNCTION 1: Get available menu items
# ============================================================================
def get_available_menu_items():
    """
    Extract unique menu items from the dataset.
    Provides users with valid options for selection (security & usability).
    """
    menu_items = df['Menu Item'].unique()
    return menu_items

# ============================================================================
# FUNCTION 2: Get available services (Lunch/Dinner)
# ============================================================================
def get_available_services():
    """
    Extract unique services (Lunch, Dinner) from the dataset.
    Allows filtering by meal service type.
    """
    services = df['Service'].unique()
    return services

# ============================================================================
# FUNCTION 3: Filter data by menu item and service
# ============================================================================
def get_menu_item_data(menu_item, service=None):
    """
    Filters dataset for a specific menu item and optionally by service type.
    Secure approach: validates inputs before filtering to prevent errors.
    """
    # Validate menu item exists (security: prevent invalid input)
    if menu_item not in df['Menu Item'].values:
        return None
    
    filtered_data = df[df['Menu Item'] == menu_item]
    
    # If service specified, filter further
    if service is not None:
        if service not in df['Service'].values:
            return None
        filtered_data = filtered_data[filtered_data['Service'] == service]
    
    return filtered_data

# ============================================================================
# FUNCTION 4: Extract sales data (time series)
# ============================================================================
def get_sales_time_series(menu_item, service=None):
    """
    Extracts daily sales data for a menu item.
    Sales data starts from column index 2 onwards (after Menu Item and Service).
    Returns date labels and sales values.
    """
    data = get_menu_item_data(menu_item, service)
    
    if data is None or data.empty:
        return None, None
    
    # Extract date columns (all columns from index 2 onwards)
    date_labels = df.columns[2:].tolist()
    
    # Get sales values and convert to numeric (security: ensure valid data)
    sales_values = data.iloc[0, 2:].values.astype(float)
    
    return date_labels, sales_values

# ============================================================================
# FUNCTION 5: Calculate sales statistics for a menu item
# ============================================================================
def calculate_menu_stats(menu_item, service=None):
    """
    Calculates key statistics: total sales, average, max, min, std deviation.
    Provides meaningful numerical output for decision-making.
    """
    dates, sales = get_sales_time_series(menu_item, service)
    
    if sales is None:
        return None
    
    stats = {
        'total': np.sum(sales),
        'average': np.mean(sales),
        'max': np.max(sales),
        'min': np.min(sales),
        'std_dev': np.std(sales),
        'count': len(sales)
    }
    
    return stats

# ============================================================================
# FUNCTION 6: Find highest performing menu item
# ============================================================================
def find_highest_performing_item(service=None, metric='total'):
    """
    Identifies the menu item with highest sales (by total or average).
    Metric can be 'total' or 'average'.
    Helps identify best-selling menu items.
    """
    menu_items = get_available_menu_items()
    best_item = None
    best_value = -1
    
    # Compare all menu items
    for item in menu_items:
        stats = calculate_menu_stats(item, service)
        if stats is None:
            continue
        
        value = stats[metric]
        if value > best_value:
            best_value = value
            best_item = item
    
    return best_item, best_value

# ============================================================================
# FUNCTION 7: Compare lunch vs dinner for a menu item
# ============================================================================
def compare_lunch_dinner(menu_item):
    """
    Compares sales performance between lunch and dinner services.
    Returns statistics for both services to identify peak service times.
    """
    lunch_stats = calculate_menu_stats(menu_item, 'Lunch')
    dinner_stats = calculate_menu_stats(menu_item, 'Dinner')
    
    return lunch_stats, dinner_stats

# ============================================================================
# FUNCTION 8: Display textual output (meaningful information)
# ============================================================================
def display_menu_item_summary(menu_item):
    """
    Provides comprehensive textual summary for a menu item.
    Displays statistics for both lunch and dinner services.
    """
    print("\n" + "="*75)
    print(f"MENU ITEM ANALYSIS: {menu_item.upper()}")
    print("="*75)
    
    lunch_stats, dinner_stats = compare_lunch_dinner(menu_item)
    
    # Overall statistics (both services combined)
    overall_stats = calculate_menu_stats(menu_item)
    
    if overall_stats is None:
        print(f"No data found for {menu_item}")
        return
    
    print(f"\nOVERALL STATISTICS (All Services):")
    print("-" * 75)
    print(f"  Total Sales: {overall_stats['total']:.0f} units")
    print(f"  Average Daily Sales: {overall_stats['average']:.2f} units")
    print(f"  Highest Daily Sales: {overall_stats['max']:.0f} units")
    print(f"  Lowest Daily Sales: {overall_stats['min']:.0f} units")
    print(f"  Standard Deviation: {overall_stats['std_dev']:.2f}")
    print(f"  Total Days Tracked: {overall_stats['count']}")
    
    # Lunch service statistics
    if lunch_stats:
        print(f"\nLUNCH SERVICE:")
        print("-" * 75)
        print(f"  Total Sales: {lunch_stats['total']:.0f} units")
        print(f"  Average Daily Sales: {lunch_stats['average']:.2f} units")
        print(f"  Highest Daily Sales: {lunch_stats['max']:.0f} units")
    
    # Dinner service statistics
    if dinner_stats:
        print(f"\nDINNER SERVICE:")
        print("-" * 75)
        print(f"  Total Sales: {dinner_stats['total']:.0f} units")
        print(f"  Average Daily Sales: {dinner_stats['average']:.2f} units")
        print(f"  Highest Daily Sales: {dinner_stats['max']:.0f} units")
    
    # Comparison
    if lunch_stats and dinner_stats:
        lunch_total = lunch_stats['total']
        dinner_total = dinner_stats['total']
        
        print(f"\nSERVICE COMPARISON:")
        print("-" * 75)
        
        if lunch_total > dinner_total:
            diff = lunch_total - dinner_total
            percentage = (diff / dinner_total) * 100
            print(f"  Lunch outsells Dinner by {diff:.0f} units ({percentage:.1f}%)")
        else:
            diff = dinner_total - lunch_total
            percentage = (diff / lunch_total) * 100
            print(f"  Dinner outsells Lunch by {diff:.0f} units ({percentage:.1f}%)")

# ============================================================================
# FUNCTION 9: Plot single menu item trend (graphical output)
# ============================================================================
def plot_menu_item_trend(menu_item, service=None):
    """
    Creates line chart showing sales trend over time.
    Graphical output makes patterns easily identifiable for end users.
    """
    dates, sales = get_sales_time_series(menu_item, service)
    
    if sales is None:
        print(f"No data found for {menu_item} ({service})")
        return
    
    # Create figure with professional styling
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # Plot line with markers
    service_label = service if service else "All Services"
    ax.plot(dates, sales, marker='o', linewidth=2.5, markersize=5, 
            color='#FF6B4A', label=f'{menu_item} - {service_label}')
    
    # Add trend line (polynomial fit) to show overall pattern
    x_numeric = np.arange(len(dates))
    z = np.polyfit(x_numeric, sales, 2)  # Quadratic trend
    p = np.poly1d(z)
    ax.plot(dates, p(x_numeric), '--', color='#2E86AB', 
            linewidth=2.5, label='Trend', alpha=0.8)
    
    # Customize appearance
    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('Sales (Units Sold)', fontsize=12, fontweight='bold')
    ax.set_title(f'Sales Trend: {menu_item} - {service_label}', 
                 fontsize=13, fontweight='bold', pad=15)
    
    # Rotate x-axis labels for readability
    ax.tick_params(axis='x', rotation=45)
    
    # Add grid for easier reading
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Add legend
    ax.legend(fontsize=11, loc='best')
    
    plt.tight_layout()
    plt.show()

# ============================================================================
# FUNCTION 10: Compare lunch vs dinner for a menu item (graphical)
# ============================================================================
def plot_lunch_dinner_comparison(menu_item):
    """
    Creates side-by-side comparison of lunch and dinner sales.
    Allows visual identification of peak service times.
    """
    lunch_dates, lunch_sales = get_sales_time_series(menu_item, 'Lunch')
    dinner_dates, dinner_sales = get_sales_time_series(menu_item, 'Dinner')
    
    if lunch_sales is None or dinner_sales is None:
        print(f"Data not available for {menu_item}")
        return
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # Plot both services
    x_numeric = np.arange(len(lunch_dates))
    ax.plot(x_numeric, lunch_sales, marker='s', linewidth=2.5, markersize=5,
            color='#FFD93D', label='Lunch', alpha=0.8)
    ax.plot(x_numeric, dinner_sales, marker='o', linewidth=2.5, markersize=5,
            color='#6BCB77', label='Dinner', alpha=0.8)
    
    # Customize appearance
    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('Sales (Units Sold)', fontsize=12, fontweight='bold')
    ax.set_title(f'Lunch vs Dinner Sales: {menu_item}', 
                 fontsize=13, fontweight='bold', pad=15)
    
    # Set x-axis labels (show every 5th date for clarity)
    ax.set_xticks(x_numeric[::5])
    ax.set_xticklabels(lunch_dates[::5], rotation=45)
    
    # Add grid
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Add legend
    ax.legend(fontsize=11, loc='best')
    
    plt.tight_layout()
    plt.show()

# ============================================================================
# FUNCTION 11: Compare multiple menu items (graphical)
# ============================================================================
def plot_menu_items_comparison(service=None):
    """
    Creates chart comparing all menu items sales performance.
    Enables comparative analysis across menu.
    """
    menu_items = get_available_menu_items()
    service_label = service if service else "All Services"
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # Extract dates from first item
    _, sales = get_sales_time_series(menu_items[0], service)
    dates = df.columns[2:].tolist()
    x_numeric = np.arange(len(dates))
    
    # Define colors for each menu item
    colors = ['#FF6B4A', '#4D96FF', '#6BCB77', '#FFD93D', '#FF85A2',
              '#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#6A994E']
    
    # Plot each menu item
    for idx, item in enumerate(menu_items):
        _, sales = get_sales_time_series(item, service)
        if sales is not None:
            ax.plot(x_numeric, sales, marker='o', linewidth=2, markersize=4,
                   label=item, color=colors[idx % len(colors)], alpha=0.8)
    
    # Customize appearance
    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('Sales (Units Sold)', fontsize=12, fontweight='bold')
    ax.set_title(f'All Menu Items Comparison - {service_label}', 
                 fontsize=13, fontweight='bold', pad=15)
    
    # Set x-axis labels (show every 7th date)
    ax.set_xticks(x_numeric[::7])
    ax.set_xticklabels(dates[::7], rotation=45)
    
    # Add grid
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Add legend (place outside if many items)
    ax.legend(fontsize=9, loc='upper left', bbox_to_anchor=(1.02, 1))
    
    plt.tight_layout()
    plt.show()

# ============================================================================
# FUNCTION 12: Calculate best performer in time period
# ============================================================================
def find_best_performer_in_period(start_idx, end_idx, service=None, metric='total'):
    """
    Finds best-selling menu item within a specified date range.
    Allows period-specific analysis (e.g., weekends vs weekdays).
    """
    menu_items = get_available_menu_items()
    best_item = None
    best_value = -1
    
    for item in menu_items:
        dates, sales = get_sales_time_series(item, service)
        
        if sales is None:
            continue
        
        # Extract period data
        period_sales = sales[start_idx:end_idx+1]
        
        if metric == 'total':
            value = np.sum(period_sales)
        elif metric == 'average':
            value = np.mean(period_sales)
        else:
            value = np.max(period_sales)
        
        if value > best_value:
            best_value = value
            best_item = item
    
    return best_item, best_value

# ============================================================================
# MAIN INTERACTIVE MENU
# ============================================================================
def main_menu():
    """
    Interactive menu providing easy-to-use interface for end users.
    Allows navigation through analysis options with clear prompts.
    """
    while True:
        print("\n" + "="*75)
        print("GURREB'S BBQ - SALES DATA SERVICE")
        print("="*75)
        print("\nSelect an option:")
        print("  1. View menu item summary (textual output)")
        print("  2. View menu item trend over time (graphical)")
        print("  3. Compare lunch vs dinner for menu item (graphical)")
        print("  4. Compare all menu items (graphical)")
        print("  5. Find best-selling menu item (overall)")
        print("  6. Find best-selling menu item (specific service)")
        print("  7. Exit")
        print("-"*75)
        
        choice = input("Enter your choice (1-7): ").strip()
        
        # Option 1: Menu item summary
        if choice == '1':
            menu_items = get_available_menu_items()
            print(f"\nAvailable menu items: {', '.join(menu_items)}")
            item = input("Enter menu item name: ").strip()
            display_menu_item_summary(item)
        
        # Option 2: Menu item trend
        elif choice == '2':
            menu_items = get_available_menu_items()
            print(f"\nAvailable menu items: {', '.join(menu_items)}")
            item = input("Enter menu item name: ").strip()
            
            services = get_available_services()
            print(f"Available services: {', '.join(services)} (or press Enter for all)")
            service = input("Enter service (optional): ").strip()
            service = service if service else None
            
            plot_menu_item_trend(item, service)
        
        # Option 3: Lunch vs dinner comparison
        elif choice == '3':
            menu_items = get_available_menu_items()
            print(f"\nAvailable menu items: {', '.join(menu_items)}")
            item = input("Enter menu item name: ").strip()
            plot_lunch_dinner_comparison(item)
        
        # Option 4: Compare all menu items
        elif choice == '4':
            services = get_available_services()
            print(f"Available services: {', '.join(services)} (or press Enter for all)")
            service = input("Enter service (optional): ").strip()
            service = service if service else None
            
            plot_menu_items_comparison(service)
        
        # Option 5: Best-selling item (overall)
        elif choice == '5':
            metric = input("Search by 'total' or 'average' sales? (default: total): ").strip()
            metric = metric if metric in ['total', 'average'] else 'total'
            
            item, value = find_highest_performing_item(metric=metric)
            print(f"\nBest-selling menu item: {item}")
            print(f"{metric.capitalize()} sales: {value:.0f}")
        
        # Option 6: Best-selling item (by service)
        elif choice == '6':
            services = get_available_services()
            print(f"Available services: {', '.join(services)}")
            service = input("Enter service: ").strip()
            
            metric = input("Search by 'total' or 'average' sales? (default: total): ").strip()
            metric = metric if metric in ['total', 'average'] else 'total'
            
            item, value = find_highest_performing_item(service, metric)
            print(f"\nBest-selling item ({service}): {item}")
            print(f"{metric.capitalize()} sales: {value:.0f}")
        
        # Option 7: Exit
        elif choice == '7':
            print("\nThank you for using Gurreb's BBQ Sales Data Service.")
            break
        
        else:
            print("Invalid choice. Please select 1-7.")

# ============================================================================
# EXECUTION
# ============================================================================
if __name__ == "__main__":
    main_menu()