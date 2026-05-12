import pandas as pd
import glob
def load_and_clean_data():
    all_files = glob.glob("*.csv")
    df_list = []
    
    for filename in all_files:
        df = pd.read_csv(filename)
        
        # --- Extract Date from Filename ---
        sheet_code = filename.replace('buffet_data_', '').replace('.csv', '')
        try:
            day = int(sheet_code[:-1])
            month = int(sheet_code[-1])
            date_str = f"2026-{month:02d}-{day:02d}"
            real_date = pd.to_datetime(date_str).date()
            
            df['Date'] = real_date
            df['Day_of_Week'] = pd.to_datetime(date_str).day_name()
            df['Is_Weekend'] = df['Day_of_Week'].isin(['Saturday', 'Sunday'])
        except Exception as e:
            pass # Skips extraction if the file name format is slightly off
            
        df_list.append(df)

    # Combine all files into one DataFrame
    df = pd.concat(df_list, ignore_index=True)
    df.columns = df.columns.str.strip()

    # ==========================================
    # STEP 1: TIME PARSING
    # ==========================================
    time_cols = ['queue_start', 'queue_end', 'meal_start', 'meal_end']
    for col in time_cols:
        df[col] = pd.to_datetime(df[col], format='%H:%M:%S', errors='coerce')

    # ==========================================
    # STEP 2: DATA CLEANING (Removing Anomalies)
    # ==========================================
    # 1. Remove Early Birds: The restaurant opens at 6:30 AM, 
    # so any meal starting before 6:00 AM is a manual data entry typo.
    df = df[(df['meal_start'].isna()) | (df['meal_start'].dt.hour >= 6)]
    
    # 2. Remove Ghost Guests: Tables recorded with 0 people.
    df = df[df['pax'] > 0]

    # ==========================================
    # STEP 3: FEATURE ENGINEERING (Math)
    # ==========================================
    # --- Table Parsing ---
    def parse_table_count(t):
        if pd.isna(t) or t == '':
            return 0
        t_str = str(t).strip()
        if t_str == '99' or t_str == '99.0':  # 99 is the queueing area
            return 0
            
        # Replace commas with hyphens in case they used commas instead, and split
        t_str = t_str.replace(',', '-').replace(' ', '')
        tables_used = [x for x in t_str.split('-') if x]
        return len(tables_used)

    if 'table_no.' in df.columns:
        df['table_count'] = df['table_no.'].apply(parse_table_count)
    elif 'table_no' in df.columns:
        df['table_count'] = df['table_no'].apply(parse_table_count)
    else:
        df['table_count'] = 1 # Fallback if missing

    df['wait_time_mins'] = (df['queue_end'] - df['queue_start']).dt.total_seconds() / 60
    df['meal_duration_mins'] = (df['meal_end'] - df['meal_start']).dt.total_seconds() / 60

    # 3. Remove Time-Travelers: End time was typed in earlier than start time (negative duration)
    df = df[(df['meal_duration_mins'] > 0) | (df['meal_duration_mins'].isna())]

    # ==========================================
    # STEP 4: FLAGS AND EDGE CASES
    # ==========================================
    df['is_walkaway'] = df['queue_start'].notna() & df['meal_start'].isna()
    df['waited'] = df['queue_start'].notna()
    df['direct_seating'] = df['meal_start'].notna() & df['queue_start'].isna()

    # Calculate arrival hour for all visuals
    df['arrival_hour'] = df['queue_start'].dt.hour.fillna(df['meal_start'].dt.hour)

    # Fill NaN wait times with 0 for easier math later
    df['wait_time_mins'] = df['wait_time_mins'].fillna(0)
    
    return df

if __name__ == "__main__":
    clean_df = load_and_clean_data()
    print("Data processed successfully. Total clean records:", len(clean_df))