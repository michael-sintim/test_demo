import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_dataset(file_path):
    """
    Perform comprehensive data analysis on a given CSV file.
    
    Parameters:
    -----------
    file_path : str
        Path to the CSV file to be analyzed
    
    Returns:
    --------
    None (prints analysis results and generates visualizations)
    """
    # Read the CSV file
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return
    except pd.errors.EmptyDataError:
        print(f"Error: File {file_path} is empty.")
        return
    
    # 1. Basic Information about the Dataset
    print("1. DATASET OVERVIEW")
    print("-" * 50)
    print(f"Total number of rows: {len(df)}")
    print(f"Total number of columns: {len(df.columns)}")
    print("\nColumns in the dataset:")
    print(df.columns.tolist())
    
    # 2. Data Types and Missing Values
    print("\n2. DATA TYPES AND MISSING VALUES")
    print("-" * 50)
    print(df.info())
    
    # 3. Statistical Summary
    print("\n3. STATISTICAL SUMMARY")
    print("-" * 50)
    # Select only numeric columns for summary statistics
    numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
    if len(numeric_columns) > 0:
        print(df[numeric_columns].describe())
    else:
        print("No numeric columns found for statistical summary.")
    
    # 4. Visualization
    print("\n4. VISUALIZATIONS")
    print("-" * 50)
    
    # Ensure output directory exists
    import os
    os.makedirs('output', exist_ok=True)
    
    # Correlation Heatmap (for numeric columns)
    if len(numeric_columns) > 1:
        plt.figure(figsize=(10, 8))
        sns.heatmap(df[numeric_columns].corr(), annot=True, cmap='coolwarm', center=0)
        plt.title('Correlation Heatmap')
        plt.tight_layout()
        plt.savefig('output/correlation_heatmap.png')
        plt.close()
        print("Correlation heatmap saved to output/correlation_heatmap.png")
    
    # Box Plot for Numeric Columns
    if len(numeric_columns) > 0:
        plt.figure(figsize=(10, 6))
        df[numeric_columns].boxplot()
        plt.title('Box Plot of Numeric Columns')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('output/boxplot.png')
        plt.close()
        print("Box plot saved to output/boxplot.png")
    
    # 5. Additional Data Insights
    print("\n5. ADDITIONAL INSIGHTS")
    print("-" * 50)
    
    # Check for categorical columns
    categorical_columns = df.select_dtypes(include=['object']).columns
    if len(categorical_columns) > 0:
        print("\nCategory Value Counts:")
        for col in categorical_columns:
            print(f"\n{col} value counts:")
            print(df[col].value_counts())
    
    # Optional: Simple data cleaning suggestions
    print("\n6. DATA CLEANING SUGGESTIONS")
    print("-" * 50)
    
    # Check for duplicate rows
    duplicates = df.duplicated().sum()
    print(f"Number of duplicate rows: {duplicates}")
    
    # Check for missing values
    missing_values = df.isnull().sum()
    print("\nMissing Values:")
    print(missing_values[missing_values > 0])

# Example usage
if __name__ == "__main__":
    # Replace 'your_dataset.csv' with the path to your actual CSV file
    analyze_dataset('dataset.csv')

# Usage instructions
# print("\n--- USAGE INSTRUCTIONS ---")
# print("1. Save this script in a Python file (e.g., data_analysis.py)")
# print("2. Ensure you have pandas, matplotlib, and seaborn installed:")
# print("   pip install pandas matplotlib seaborn")
# print("3. Replace 'your_dataset.csv' with the path to your CSV file")
# print("4. Run the script: python data_analysis.py")