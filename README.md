# Busy Buffet: Data Analytics Dashboard

**Live App:** [View the Dashboard on Streamlit](https://singhanart-chaichimplee-atmind-intern-test-buffet-data-analysis.streamlit.app/)  
**Direct Link:** `https://singhanart-chaichimplee-atmind-intern-test-buffet-data-analysis.streamlit.app/`

This repository contains a Python and Streamlit dashboard created for the Hotel Amber 85 "Busy Buffet" data analysis assignment. The project analyzes restaurant traffic data to identify operational bottlenecks and evaluate proposed management solutions.

## Project Overview

The dashboard processes raw traffic data to analyze wait times, table turnover, and customer behavior. It is structured into an overview and three main tasks:

* **Overview:** KPI summary and traffic heatmaps to identify peak hours.
* **Task 1:** Analysis of staff feedback regarding queue times, weekday vs. weekend traffic, and table capacity constraints.
* **Task 2:** Evaluation of proposed management actions (e.g., price increases, reducing seating limits, queue skipping).
* **Task 3:** Recommendation for a Weekend Timeslot Booking system to manage the physical table bottleneck.

## Tech Stack

* Python 3
* Streamlit (Frontend/UI)
* Pandas (Data cleaning and feature engineering)
* Plotly (Data visualization)

## Repository Structure

* `app.py`: Main entry point and Overview page.
* `pages/`: Contains individual pages (`1_Task_1.py`, `2_Task_2.py`, `3_Task_3.py`).
* `data_pipeline.py`: Data cleaning script that handles table string parsing (e.g., `1A-1B`), date extraction, and time duration calculations.
* `utils.py`: Shared UI components and dataset loaders.
* `requirements.txt`: Project dependencies.
* `*.csv`: Raw data files.

**Live App:**
[View the Dashboard on Streamlit](https://singhanart-chaichimplee-atmind-intern-test-buffet-data-analysis.streamlit.app/)
## How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone git@github.com:ewakelian/Atmind_DataAnalysis_Intern_Test.git
   cd Atmind_DataAnalysis_Intern_Test
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```
