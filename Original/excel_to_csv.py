import pandas as pd

def convert_excel_to_csv(excel_file_path):
    print(f"Loading {excel_file_path}...")
    
    # Using sheet_name=None reads ALL sheets into a dictionary
    # Format: {'Sheet1_Name': DataFrame1, 'Sheet2_Name': DataFrame2}
    all_sheets = pd.read_excel(excel_file_path, sheet_name=None)
    
    # Loop through each sheet and save it as a separate CSV
    for sheet_name, df in all_sheets.items():
        # Create a clean filename using the sheet's name
        csv_filename = f"buffet_data_{sheet_name}.csv"
        
        # Save to CSV without the index column
        df.to_csv(csv_filename, index=False)
        print(f"Successfully saved: {csv_filename} ({len(df)} rows)")

if __name__ == "__main__":
    # Ensure this matches the exact name of your downloaded Excel file
    excel_file = "2026 Data Test1 Final - Busy Buffet Dataset.xlsx" 
    
    convert_excel_to_csv(excel_file)
    print("All sheets have been converted to csv")