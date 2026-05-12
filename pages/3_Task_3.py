import streamlit as st
import pandas as pd
import plotly.express as px
from utils import get_data, render_filters, render_footer_navigation, MAX_TABLE_CAPACITY

st.set_page_config(page_title="Task 3: The Solution", layout="wide")

st.title("Task 3: The Solution - Weekend Timeslots Reserving")

raw_df = get_data()
if raw_df.empty:
    st.error("No data available. Check the CSV files.")
    st.stop()

df = render_filters(raw_df)
if df.empty:
    st.warning("No data matches the selected filters.")
    st.stop()

st.markdown("""
### Proposed Adjustment to Action 1
**Recommendation: Implement a Weekend-Only Timeslot Booking System for Walk-ins.**
* **Current Bottleneck:** The restaurant's capacity is technically ~30 tables. However, operational data shows the system breaks and queues form the moment we hit **24 concurrent tables**. On weekends, walk-in arrivals are heavily concentrated between 7:00 AM and 9:00 AM, rapidly occupying these 24 tables and completely stalling the queue.
* **Proposed Solution:** Maintain the 5-hour seating promotion, but require walk-in guests to reserve specific time-slots (e.g., 6:30 AM, 8:00 AM, 9:30 AM) on Saturdays and Sundays. By capping walk-in bookings at approximately 40 arrivals per hour, we ensure enough tables remain open for in-house guests, balancing the load.
""")

tab_weekend, tab_weekday = st.tabs(["Weekend Bottleneck", "Weekday Baseline"])

operating_hours = [6, 7, 8, 9, 10, 11]

with tab_weekend:
    weekend_df = df[df['Is_Weekend'] == True].copy()
    if not weekend_df.empty:
        num_weekend_days = weekend_df['Date'].nunique()
        current_we_traffic = weekend_df.groupby('arrival_hour')['pax'].sum().reset_index()
        current_we_traffic['pax'] = current_we_traffic['pax'] / num_weekend_days
        current_we_traffic.rename(columns={'pax': 'Current Arrivals (Chaos)'}, inplace=True)

        daily_we_pax = current_we_traffic['Current Arrivals (Chaos)'].sum()
        pax_per_hour_we = daily_we_pax / len(operating_hours)

        sim_we_data = pd.DataFrame({'arrival_hour': operating_hours, 'Time-Slot System (Controlled)': [pax_per_hour_we] * len(operating_hours)})
        plot_data_we = pd.merge(current_we_traffic, sim_we_data, on='arrival_hour', how='outer').fillna(0)
        
        plot_data_we_melted = pd.melt(plot_data_we, id_vars=['arrival_hour'], 
                                   value_vars=['Current Arrivals (Chaos)', 'Time-Slot System (Controlled)'],
                                   var_name='Scenario', value_name='Average Daily Arrivals')

        col_we1, col_we2 = st.columns([2, 1])
        with col_we1:
            fig_we = px.bar(plot_data_we_melted, x='arrival_hour', y='Average Daily Arrivals', color='Scenario', barmode='group',
                              title="Simulated Daily Impact of a Time-Slot System (Weekends)",
                              labels={'arrival_hour': 'Hour of Morning', 'Average Daily Arrivals': 'Average People Arriving'},
                              color_discrete_map={'Current Arrivals (Chaos)': '#EF553B', 'Time-Slot System (Controlled)': '#00CC96'})
            fig_we.add_hline(y=MAX_TABLE_CAPACITY, line_dash="dash", line_color="red", annotation_text="Physical Capacity (30 Tables)")
            
            fig_we.update_xaxes(
                tickvals=[6, 7, 8, 9, 10, 11],
                ticktext=['6:30 AM', '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM']
            )
            st.plotly_chart(fig_we, width="stretch")

        with col_we2:
            st.success("**Why this works for Weekends:**")
            st.markdown(f"""
            By distributing the weekend demand across the operating hours (6:30 AM - 12:00 PM), the arrival rate normalizes to approximately **{pax_per_hour_we:.0f} guests per hour**.
            
            * **Optimized Table Turnover:** The median meal duration is roughly 1 hour. By pacing arrivals to ~41 people per hour, we mathematically guarantee that concurrent occupancy hovers around 20 tables. This keeps us safely below the **24-table breaking point**.
            * **Queue Reduction:** Smoothing out the arrival curve mitigates long queues and ensures table availability for in-house guests.
            """)
    else:
        st.warning("No weekend data available in the current dataset or filter.")

with tab_weekday:
    weekday_df = df[df['Is_Weekend'] == False].copy()
    
    num_weekday_days = weekday_df['Date'].nunique()
    if num_weekday_days > 0 and not weekday_df.empty:
        current_wd_traffic = weekday_df.groupby('arrival_hour')['pax'].sum().reset_index()
        current_wd_traffic['pax'] = current_wd_traffic['pax'] / num_weekday_days
        current_wd_traffic.rename(columns={'pax': 'Current Arrivals (Natural Flow)'}, inplace=True)

        col_wd1, col_wd2 = st.columns([2, 1])
        with col_wd1:
            fig_wd = px.bar(current_wd_traffic, x='arrival_hour', y='Current Arrivals (Natural Flow)', 
                              title="Current Daily Traffic (Weekdays)",
                              labels={'arrival_hour': 'Hour of Morning', 'Current Arrivals (Natural Flow)': 'Average People Arriving'},
                              color_discrete_sequence=['#636EFA'])
            fig_wd.add_hline(y=MAX_TABLE_CAPACITY, line_dash="dash", line_color="red", annotation_text="Physical Capacity (30 Tables)")
            
            fig_wd.update_xaxes(
                tickvals=[6, 7, 8, 9, 10, 11],
                ticktext=['6:30 AM', '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM']
            )
            st.plotly_chart(fig_wd, width="stretch")

        with col_wd2:
            st.markdown("**For Weekday:**")
            st.markdown("""
            **Evaluation:** Weekday arrivals peak at approximately 27 guests per hour. Concurrent table tracking shows that maximum weekday occupancy reaches 37 seated guests, leaving sufficient buffer capacity.
            
            **Conclusion:** The natural flow of weekday traffic is manageable under the current system. Implementing the booking system should be restricted to weekends to avoid unnecessary operational friction.
            """)
    else:
        st.warning("No weekday data available in the current dataset or filter.")

render_footer_navigation()
