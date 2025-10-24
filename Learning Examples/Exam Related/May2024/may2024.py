import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ============================================================================
# RECOATS ADVENTURE PARK - INCOME DATA SERVICE SOLUTION
# Task 4a: Developing a solution for income trend analysis
# ============================================================================

# Load the CSV data - contains daily income from different sources
try:
    df = pd.read_csv('Learning Examples\Exam Related\May2024\Task4a_data.csv')
    print("✓ Data loaded successfully\n")
except FileNotFoundError:
    print("Error: Task4a_data.csv not found!")
    exit()

# ============================================================================
# FUNCTION 1: Get available income sources
# ============================================================================
def get_available_sources():
    """
    Extract unique income sources (Tickets, Gift Shop, Snack Stand, Pictures).
    Provides users with valid options for selection (security & usability).
    """
    sources = df.columns[2:].tolist()
    return sources

# ============================================================================
# FUNCTION 2: Get available payment types
# ============================================================================
def get_available_payment_types():
    """
    Extract unique payment types (Cash, Card) from the dataset.
    Allows filtering by payment method for trend analysis.
    """
    pay_types = df['Pay Type'].unique()
    return pay_types

# ============================================================================
# FUNCTION 3: Get available days of week
# ============================================================================
def get_available_days():
    """
    Extract unique days of week from the dataset.
    Allows analysis by day-of-week patterns.
    """
    days = df['Day'].unique()
    # Maintain consistent week order
    week_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    days_ordered = [d for d in week_order if d in days]
    return days_ordered

# ============================================================================
# FUNCTION 4: Filter data by payment type
# ============================================================================
def get_payment_type_data(pay_type):
    """
    Filters dataset for a specific payment type.
    Secure approach: validates payment type exists before filtering.
    """
    # Validate payment type exists (security: prevent invalid input)
    if pay_type not in get_available_payment_types():
        return None
    
    filtered_data = df[df['Pay Type'] == pay_type]
    return filtered_data

# ============================================================================
# FUNCTION 5: Filter data by day of week
# ============================================================================
def get_day_data(day):
    """
    Filters dataset for a specific day of the week.
    Secure approach: validates day exists before filtering.
    """
    # Validate day exists (security: prevent invalid input)
    if day not in get_available_days():
        return None
    
    filtered_data = df[df['Day'] == day]
    return filtered_data

# ============================================================================
# FUNCTION 6: Get income data for specific source
# ============================================================================
def get_source_income_data(source):
    """
    Extracts time series income data for a specific income source.
    Source can be: Tickets, Gift Shop, Snack Stand, or Pictures.
    """
    # Validate source exists (security)
    if source not in get_available_sources():
        return None
    
    income_data = df[source].values.astype(float)
    return income_data

# ============================================================================
# FUNCTION 7: Calculate income statistics
# ============================================================================
def calculate_income_stats(data):
    """
    Calculates key statistics: total, average, max, min, std deviation.
    Provides meaningful numerical output for decision-making.
    """
    if data is None or len(data) == 0:
        return None
    
    stats = {
        'total': np.sum(data),
        'average': np.mean(data),
        'max': np.max(data),
        'min': np.min(data),
        'std_dev': np.std(data),
        'count': len(data)
    }
    
    return stats

# ============================================================================
# FUNCTION 8: Calculate total income by payment type
# ============================================================================
def calculate_by_payment_type(source=None):
    """
    Calculates income statistics for each payment type.
    Shows how different payment methods perform.
    """
    payment_types = get_available_payment_types()
    results = {}
    
    for pay_type in payment_types:
        data = get_payment_type_data(pay_type)
        
        if source is not None:
            if source not in get_available_sources():
                continue
            income = data[source].values.astype(float)
        else:
            # Sum all sources
            income = data[get_available_sources()].sum(axis=1).values.astype(float)
        
        stats = calculate_income_stats(income)
        results[pay_type] = stats
    
    return results

# ============================================================================
# FUNCTION 9: Calculate income by day of week
# ============================================================================
def calculate_by_day_of_week(source=None, pay_type=None):
    """
    Calculates income statistics for each day of the week.
    Identifies busy days and revenue patterns.
    """
    days = get_available_days()
    results = {}
    
    for day in days:
        data = get_day_data(day)
        
        # Filter by payment type if specified
        if pay_type is not None:
            data = data[data['Pay Type'] == pay_type]
        
        if source is not None:
            if source not in get_available_sources():
                continue
            income = data[source].values.astype(float)
        else:
            # Sum all sources
            income = data[get_available_sources()].sum(axis=1).values.astype(float)
        
        stats = calculate_income_stats(income)
        results[day] = stats
    
    return results

# ============================================================================
# FUNCTION 10: Display textual output - payment type analysis
# ============================================================================
def display_payment_type_analysis(source=None):
    """
    Provides comprehensive textual summary of payment type performance.
    Compares Cash vs Card payment methods across selected income source(s).
    """
    if source is None:
        source_label = "All Income Sources"
    else:
        source_label = source
    
    print("\n" + "="*80)
    print(f"PAYMENT TYPE ANALYSIS: {source_label.upper()}")
    print("="*80)
    
    results = calculate_by_payment_type(source)
    
    payment_types = get_available_payment_types()
    
    for pay_type in payment_types:
        if pay_type not in results or results[pay_type] is None:
            continue
        
        stats = results[pay_type]
        print(f"\n{pay_type.upper()} PAYMENT:")
        print("-" * 80)
        print(f"  Total Income: £{stats['total']:.2f}")
        print(f"  Average Daily Income: £{stats['average']:.2f}")
        print(f"  Highest Daily Income: £{stats['max']:.2f}")
        print(f"  Lowest Daily Income: £{stats['min']:.2f}")
        print(f"  Standard Deviation: £{stats['std_dev']:.2f}")
        print(f"  Number of Days: {stats['count']}")
    
    # Comparison
    if len(results) == 2:
        stats_list = list(results.values())
        pay_types_list = list(results.keys())
        
        total_cash = results[pay_types_list[0]]['total']
        total_card = results[pay_types_list[1]]['total']
        
        print(f"\nCOMPARISON:")
        print("-" * 80)
        
        if total_cash > total_card:
            diff = total_cash - total_card
            percentage = (diff / total_card) * 100
            print(f"  Cash generates £{diff:.2f} ({percentage:.1f}%) more than Card")
        else:
            diff = total_card - total_cash
            percentage = (diff / total_cash) * 100
            print(f"  Card generates £{diff:.2f} ({percentage:.1f}%) more than Cash")

# ============================================================================
# FUNCTION 11: Display textual output - day of week analysis
# ============================================================================
def display_day_of_week_analysis(source=None, pay_type=None):
    """
    Provides comprehensive textual summary of income by day of week.
    Identifies peak and low-performing days.
    """
    if source is None:
        source_label = "All Income Sources"
    else:
        source_label = source
    
    if pay_type is None:
        pay_label = "All Payment Types"
    else:
        pay_label = pay_type
    
    print("\n" + "="*80)
    print(f"DAILY ANALYSIS: {source_label.upper()} - {pay_label.upper()}")
    print("="*80)
    
    results = calculate_by_day_of_week(source, pay_type)
    days = get_available_days()
    
    for day in days:
        if day not in results or results[day] is None:
            continue
        
        stats = results[day]
        print(f"\n{day.upper()}:")
        print("-" * 80)
        print(f"  Total Income: £{stats['total']:.2f}")
        print(f"  Average Daily Income: £{stats['average']:.2f}")
        print(f"  Highest Single Day: £{stats['max']:.2f}")
        print(f"  Lowest Single Day: £{stats['min']:.2f}")
        print(f"  Days Recorded: {stats['count']}")
    
    # Identify best and worst days
    best_day = max(results.items(), key=lambda x: x[1]['total'] if x[1] else 0)
    worst_day = min(results.items(), key=lambda x: x[1]['total'] if x[1] else 0)
    
    print(f"\nSUMMARY:")
    print("-" * 80)
    print(f"  Best Day (Total Income): {best_day[0]} - £{best_day[1]['total']:.2f}")
    print(f"  Worst Day (Total Income): {worst_day[0]} - £{worst_day[1]['total']:.2f}")

# ============================================================================
# FUNCTION 12: Plot income trend over time
# ============================================================================
def plot_income_trend(source, pay_type=None):
    """
    Creates line chart showing income trend over time.
    Graphical output makes patterns easily identifiable for end users.
    """
    # Filter data
    if pay_type is not None:
        data = get_payment_type_data(pay_type)
    else:
        data = df.copy()
    
    # Validate source
    if source not in get_available_sources():
        print(f"Income source '{source}' not found.")
        return
    
    # Extract income data
    income = data[source].values.astype(float)
    x_values = np.arange(len(income))
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # Plot line with markers
    pay_label = pay_type if pay_type else "All Payment Types"
    ax.plot(x_values, income, marker='o', linewidth=2.5, markersize=5,
            color='#FF6B4A', label=f'{source} - {pay_label}', alpha=0.8)
    
    # Add trend line (polynomial fit)
    z = np.polyfit(x_values, income, 2)
    p = np.poly1d(z)
    ax.plot(x_values, p(x_values), '--', color='#2E86AB',
            linewidth=2.5, label='Trend', alpha=0.8)
    
    # Add average line
    avg_income = np.mean(income)
    ax.axhline(y=avg_income, color='#6BCB77', linestyle=':', 
               linewidth=2, label=f'Average: £{avg_income:.2f}', alpha=0.7)
    
    # Customize appearance
    ax.set_xlabel('Days', fontsize=12, fontweight='bold')
    ax.set_ylabel('Income (£)', fontsize=12, fontweight='bold')
    ax.set_title(f'Income Trend: {source} ({pay_label})',
                 fontsize=13, fontweight='bold', pad=15)
    
    # Add grid
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Add legend
    ax.legend(fontsize=11, loc='best')
    
    plt.tight_layout()
    plt.show()

# ============================================================================
# FUNCTION 13: Plot comparison of all income sources
# ============================================================================
def plot_income_sources_comparison(pay_type=None):
    """
    Creates chart comparing all income sources over time.
    Enables visual comparison of revenue streams.
    """
    # Filter data by payment type if specified
    if pay_type is not None:
        data = get_payment_type_data(pay_type)
    else:
        data = df.copy()
    
    sources = get_available_sources()
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    x_values = np.arange(len(data))
    
    # Define colors for each source
    colors = ['#FF6B4A', '#4D96FF', '#6BCB77', '#FFD93D']
    
    # Plot each income source
    for idx, source in enumerate(sources):
        income = data[source].values.astype(float)
        ax.plot(x_values, income, marker='o', linewidth=2.5, markersize=4,
                label=source, color=colors[idx % len(colors)], alpha=0.8)
    
    # Customize appearance
    pay_label = pay_type if pay_type else "All Payment Types"
    ax.set_xlabel('Days', fontsize=12, fontweight='bold')
    ax.set_ylabel('Income (£)', fontsize=12, fontweight='bold')
    ax.set_title(f'All Income Sources Comparison ({pay_label})',
                 fontsize=13, fontweight='bold', pad=15)
    
    # Add grid
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Add legend
    ax.legend(fontsize=11, loc='best')
    
    plt.tight_layout()
    plt.show()

# ============================================================================
# FUNCTION 14: Plot day-of-week comparison
# ============================================================================
def plot_day_of_week_comparison(source, pay_type=None):
    """
    Creates bar chart showing income by day of week.
    Identifies busiest and quietest days visually.
    """
    # Calculate income by day
    results = calculate_by_day_of_week(source, pay_type)
    days = get_available_days()
    
    # Extract totals for each day
    day_totals = [results[day]['total'] for day in days if day in results]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Create bar chart
    bars = ax.bar(days, day_totals, color='#FF6B4A', edgecolor='black', linewidth=1.5, alpha=0.8)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'£{height:.0f}',
                ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # Customize appearance
    pay_label = pay_type if pay_type else "All Payment Types"
    ax.set_xlabel('Day of Week', fontsize=12, fontweight='bold')
    ax.set_ylabel('Total Income (£)', fontsize=12, fontweight='bold')
    ax.set_title(f'Income by Day of Week: {source} ({pay_label})',
                 fontsize=13, fontweight='bold', pad=15)
    
    # Add grid for y-axis
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.show()

# ============================================================================
# FUNCTION 15: Plot payment type comparison
# ============================================================================
def plot_payment_type_comparison(source=None):
    """
    Creates bar chart comparing Cash vs Card income.
    Visualizes payment method preferences.
    """
    results = calculate_by_payment_type(source)
    pay_types = list(results.keys())
    totals = [results[pt]['total'] for pt in pay_types]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create bar chart
    colors = ['#4D96FF', '#6BCB77']
    bars = ax.bar(pay_types, totals, color=colors, edgecolor='black', linewidth=1.5, alpha=0.8)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'£{height:.0f}',
                ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    # Customize appearance
    source_label = source if source else "All Income Sources"
    ax.set_xlabel('Payment Type', fontsize=12, fontweight='bold')
    ax.set_ylabel('Total Income (£)', fontsize=12, fontweight='bold')
    ax.set_title(f'Income by Payment Type: {source_label}',
                 fontsize=13, fontweight='bold', pad=15)
    
    # Add grid for y-axis
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
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
        print("\n" + "="*80)
        print("RECOATS ADVENTURE PARK - INCOME DATA SERVICE")
        print("="*80)
        print("\nSelect an option:")
        print("  1. View payment type analysis (textual - all sources)")
        print("  2. View payment type analysis (textual - specific source)")
        print("  3. View day-of-week analysis (textual - all sources)")
        print("  4. View day-of-week analysis (textual - specific source)")
        print("  5. View income trend over time (graphical)")
        print("  6. Compare all income sources (graphical)")
        print("  7. Compare by day of week (graphical - bar chart)")
        print("  8. Compare payment types (graphical - bar chart)")
        print("  9. Exit")
        print("-"*80)
        
        choice = input("Enter your choice (1-9): ").strip()
        
        # Option 1: Payment type analysis (all sources)
        if choice == '1':
            display_payment_type_analysis()
        
        # Option 2: Payment type analysis (specific source)
        elif choice == '2':
            sources = get_available_sources()
            print(f"\nAvailable income sources: {', '.join(sources)}")
            source = input("Enter income source name: ").strip()
            display_payment_type_analysis(source)
        
        # Option 3: Day-of-week analysis (all sources)
        elif choice == '3':
            display_day_of_week_analysis()
        
        # Option 4: Day-of-week analysis (specific source)
        elif choice == '4':
            sources = get_available_sources()
            print(f"\nAvailable income sources: {', '.join(sources)}")
            source = input("Enter income source name: ").strip()
            
            pay_types = get_available_payment_types()
            print(f"Payment types: {', '.join(pay_types)} (or press Enter for all)")
            pay_type = input("Enter payment type (optional): ").strip()
            pay_type = pay_type if pay_type else None
            
            display_day_of_week_analysis(source, pay_type)
        
        # Option 5: Income trend over time
        elif choice == '5':
            sources = get_available_sources()
            print(f"\nAvailable income sources: {', '.join(sources)}")
            source = input("Enter income source name: ").strip()
            
            pay_types = get_available_payment_types()
            print(f"Payment types: {', '.join(pay_types)} (or press Enter for all)")
            pay_type = input("Enter payment type (optional): ").strip()
            pay_type = pay_type if pay_type else None
            
            plot_income_trend(source, pay_type)
        
        # Option 6: Compare all income sources
        elif choice == '6':
            pay_types = get_available_payment_types()
            print(f"Payment types: {', '.join(pay_types)} (or press Enter for all)")
            pay_type = input("Enter payment type (optional): ").strip()
            pay_type = pay_type if pay_type else None
            
            plot_income_sources_comparison(pay_type)
        
        # Option 7: Day-of-week comparison
        elif choice == '7':
            sources = get_available_sources()
            print(f"\nAvailable income sources: {', '.join(sources)}")
            source = input("Enter income source name: ").strip()
            
            pay_types = get_available_payment_types()
            print(f"Payment types: {', '.join(pay_types)} (or press Enter for all)")
            pay_type = input("Enter payment type (optional): ").strip()
            pay_type = pay_type if pay_type else None
            
            plot_day_of_week_comparison(source, pay_type)
        
        # Option 8: Payment type comparison
        elif choice == '8':
            sources = get_available_sources()
            print(f"Available income sources: {', '.join(sources)} (or press Enter for all)")
            source = input("Enter income source (optional): ").strip()
            source = source if source else None
            
            plot_payment_type_comparison(source)
        
        # Option 9: Exit
        elif choice == '9':
            print("\nThank you for using Recoats Adventure Park Income Data Service.")
            break
        
        else:
            print("Invalid choice. Please select 1-9.")

# ============================================================================
# EXECUTION
# ============================================================================
if __name__ == "__main__":
    main_menu()