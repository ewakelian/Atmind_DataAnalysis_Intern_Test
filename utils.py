import streamlit as st
from data_pipeline import load_and_clean_data

MAX_TABLE_CAPACITY = 30

@st.cache_data
def get_data():
    return load_and_clean_data()

def render_filters(df):
    filter_val = st.radio("**Filter Guest Type:**", options=["All Guests", "In-House Only", "Walk-In Only"], horizontal=True)
    
    if filter_val == "In-House Only":
        return df[df['Guest_type'] == 'In house']
    elif filter_val == "Walk-In Only":
        return df[df['Guest_type'] == 'Walk in']
    
    return df

def render_footer_navigation():
    st.divider()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Overview", use_container_width=True):
            st.switch_page("app.py")
    with col2:
        if st.button("Task 1", use_container_width=True):
            st.switch_page("pages/1_Task_1.py")
    with col3:
        if st.button("Task 2", use_container_width=True):
            st.switch_page("pages/2_Task_2.py")
    with col4:
        if st.button("Task 3", use_container_width=True):
            st.switch_page("pages/3_Task_3.py")
