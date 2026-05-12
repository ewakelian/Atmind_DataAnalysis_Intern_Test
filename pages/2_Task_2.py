import streamlit as st
import plotly.express as px
from utils import get_data, render_filters, render_footer_navigation

st.set_page_config(page_title="Task 2: Evaluating Actions", layout="wide")

st.title("Task 2: Disproving Management's Actions")

raw_df = get_data()
if raw_df.empty:
    st.error("No data available. Please check the CSV files.")
    st.stop()

df = render_filters(raw_df)
if df.empty:
    st.warning("No data matches the selected filters.")
    st.stop()

tab_m1, tab_m2, tab_m3 = st.tabs([
    "Action 1: Reduce Seating Time", 
    "Action 2: Raise Price to 259", 
    "Action 3: In-House Queue Skipping"
])

with tab_m1:
    st.subheader("Action 1: Reducing the 5-hour limit")
    
    valid_meals_df = df[df['meal_duration_mins'] > 0]
    total_meals = len(valid_meals_df)
    over_2_hours = len(valid_meals_df[valid_meals_df['meal_duration_mins'] > 120])
    pct_over_2_hours = (over_2_hours / total_meals) * 100 if total_meals > 0 else 0
    
    colA, colB = st.columns([2, 1])
    with colA:
        fig_m1 = px.histogram(valid_meals_df, x="meal_duration_mins",
                              title="Distribution of Meal Durations",
                              labels={'meal_duration_mins': 'Minutes Spent Eating'},
                              nbins=30,
                              color_discrete_sequence=['#636EFA'])
        
        fig_m1.add_vline(x=120, line_dash="dash", line_color="orange", annotation_text="2 Hour")
        fig_m1.add_vline(x=300, line_dash="dash", line_color="red", annotation_text="Current 5 Hour Limit")
        
        st.plotly_chart(fig_m1, width="stretch")
    
    with colB:
        st.markdown(f"**Data Point: Only {pct_over_2_hours:.1f}% of groups stay longer than 2 hours.**")
        st.markdown("""
        **Evaluation:** The "5-Hour Buffet" promotion is a primary driver of the recent traffic increase. 
        
        The data demonstrates that the vast majority of customers naturally finish their meals within 2 hours. 
        
        Reducing the limit of 5 hours would negatively impact the marketing message while providing minimal operational benefit, as tables are already turning over within that timeframe.
        """)

with tab_m2:
    st.subheader("Action 2: Implementing a flat price increase to 259")
        
    hourly_traffic = df.groupby('arrival_hour')['pax'].sum().reset_index()
    
    colC, colD = st.columns([2, 1])
    with colC:
        fig_m2 = px.bar(hourly_traffic, x="arrival_hour", y="pax",
                        title="Total Guests Arriving by Hour (The Bottleneck)",
                        labels={'arrival_hour': 'Hour of Morning', 'pax': 'Total People Arriving'})
        fig_m2.update_xaxes(tickmode='linear', tick0=6, dtick=1)
        st.plotly_chart(fig_m2, width="stretch")
        
    with colD:
        st.markdown("**Observation: Traffic distribution is uneven.**")
        st.markdown("""
        **Evaluation:** The high volume is concentrated during specific morning hours (7 AM - 9 AM) rather than consistently throughout the day. 
        A flat price increase could broadly reduce overall demand rather than addressing the specific peak-hour bottleneck.
        """)

with tab_m3:
    st.subheader("Action 3: Allowing In-House Guests to skip the queue")
    
    guest_mix = df.groupby('Guest_type')['pax'].sum().reset_index()
    
    colE, colF = st.columns([2, 1])
    with colE:
        if not guest_mix.empty:
            fig_m3 = px.pie(guest_mix, values='pax', names='Guest_type', 
                            title="Guest Volume Breakdown", hole=0.4,
                            color='Guest_type', color_discrete_map={'Walk in':'#FFA15A', 'In house':'#636EFA'})
            st.plotly_chart(fig_m3, width="stretch")
        else:
            st.write("No guest mix data available for the current filter.")
        
    with colF:
        st.markdown("**Observation: Walk-in volume dominates.**")
        st.markdown("""
        **Evaluation:** Walk-in customers constitute the majority of the total volume. Allowing in-house guests to bypass the queue would significantly increase wait times for walk-ins during peak hours, potentially leading to higher walk-away rates and negative customer feedback.
        """)

render_footer_navigation()
