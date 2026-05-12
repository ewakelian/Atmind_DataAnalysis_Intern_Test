import streamlit as st
import pandas as pd
import plotly.express as px
from utils import get_data, render_filters, render_footer_navigation

# --- Page Config & Constants ---
st.set_page_config(page_title="Hotel Amber 85 - Buffet Analytics", layout="wide", page_icon="🍳")

def render_kpi_row(df):
    st.markdown("### Hotel Buffet Operational Metrics")
    col1, col2, col3, col4 = st.columns(4)

    total_guests = df['pax'].sum()
    
    walk_aways_df = df[df['is_walkaway']]
    walk_aways = walk_aways_df['pax'].sum()
    
    # Prices: 159 weekday, 199 weekend
    weekday_missed = walk_aways_df[~walk_aways_df['Is_Weekend']]['pax'].sum() if not walk_aways_df.empty else 0
    weekend_missed = walk_aways_df[walk_aways_df['Is_Weekend']]['pax'].sum() if not walk_aways_df.empty else 0
    lost_revenue = (weekday_missed * 159) + (weekend_missed * 199)
    
    avg_wait = df[df['waited']]['wait_time_mins'].mean()
    avg_meal = df['meal_duration_mins'].mean()

    col1.metric("Total Customers Served", f"{total_guests:,.0f} Pax")
    col2.metric("Lost Revenue (Walk-aways)", f"฿{lost_revenue:,.0f}", f"{walk_aways:,.0f} Pax missed", delta_color="inverse")
    col3.metric("Average Wait Time (If Queued)", f"{avg_wait:.1f} mins")
    col4.metric("Average Meal Duration", f"{avg_meal:.1f} mins")
    st.divider()

def render_overview(df):
    st.markdown("## General Overview: Peak Traffic Analysis")
    st.markdown("Understanding *when* our guests arrive is the first step to solving the capacity issues.")
        
    heatmap_data = df.groupby(['Day_of_Week', 'arrival_hour'])['pax'].sum().reset_index()
    
    # Ensure Days of Week are sorted logically, but only include days that exist in the data
    all_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    present_days = df['Day_of_Week'].unique()
    days_order = [day for day in all_days if day in present_days]
    
    heatmap_data['Day_of_Week'] = pd.Categorical(heatmap_data['Day_of_Week'], categories=days_order, ordered=True)
    heatmap_data = heatmap_data.sort_values(['Day_of_Week', 'arrival_hour'])

    # Format the hour nicely so Plotly doesn't group them into weird bins like 6-7
    heatmap_data['arrival_time'] = heatmap_data['arrival_hour'].apply(lambda x: f"{int(x)}:00")
    
    fig_heat = px.density_heatmap(
        heatmap_data, 
        x="arrival_time", 
        y="Day_of_Week", 
        z="pax",
        title="Traffic Heatmap: Weekly Arrival Bottlenecks",
        labels={'arrival_time': 'Time of Day', 'Day_of_Week': 'Day of Week', 'pax': 'Total Arrivals'},
        color_continuous_scale="Viridis",
        text_auto=True
    )
    # Force the x-axis to be categorical so no hours are skipped
    fig_heat.update_xaxes(type='category', categoryorder='array', categoryarray=[f"{i}:00" for i in range(6, 12)])
    
    st.plotly_chart(fig_heat, width="stretch")
    st.markdown("**Insight:** The heatmap clearly visualizes the massive congestion happening exclusively on weekend mornings (Saturday & Sunday, 7 AM - 9 AM).")
    st.divider()

def main():
    st.title("Hotel Amber 85: Busy Buffet Dashboard")    
    # 1. Load data
    raw_df = get_data()
    
    if raw_df.empty:
        st.error("No data available. Please check the CSV files.")
        return

    # 2. Render In-Page Filters
    df = render_filters(raw_df)
    
    if df.empty:
        st.warning("No data matches the selected filters.")
        return

    # 3. Render Dashboard Components
    render_kpi_row(df)
    render_overview(df)

    render_footer_navigation()

if __name__ == "__main__":
    main()