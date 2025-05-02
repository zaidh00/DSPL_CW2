
import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('cleaned_environment_lka.csv')
    return df

df = load_data()

# App title
st.title("🌍 Environmental Indicators Dashboard - Sri Lanka")

# Sidebar Filters
st.sidebar.header("🔍 Filter Data")
years = sorted(df['year'].unique(), reverse=True)
indicators = df['indicator_name'].unique()

selected_year = st.sidebar.selectbox("Select Year", years)
selected_indicators = st.sidebar.multiselect(
    "Select Indicators",
    options=indicators,
    default=indicators[:5]  # default: first few
)

# Filtered data
filtered_df = df[(df['year'] == selected_year) & (df['indicator_name'].isin(selected_indicators))]

# Main Metrics
st.subheader(f"📅 Year: {selected_year}")
st.write(f"Showing {len(filtered_df)} records for selected indicators.")

# Indicator Breakdown
st.subheader("📈 Indicator Values")
fig = px.bar(
    filtered_df,
    x="indicator_name",
    y="value",
    text="value",
    labels={'value': 'Indicator Value'},
    title="Indicator Values in Selected Year",
)
fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.update_layout(xaxis_tickangle=-45, height=600)
st.plotly_chart(fig, use_container_width=True)

# Trends Over Time
st.subheader("📊 Trends Over Time")

trend_ind = st.selectbox("Select an Indicator to View Trend", indicators)

trend_df = df[df['indicator_name'] == trend_ind].sort_values("year")

fig_line = px.line(
    trend_df,
    x="year",
    y="value",
    title=f"Trend of '{trend_ind}' Over Time",
    markers=True
)
st.plotly_chart(fig_line, use_container_width=True)

# Data Table
st.subheader("🧾 Raw Data")
st.dataframe(filtered_df)

# Footer
st.markdown("---")
st.markdown("📘 Source: Cleaned Environmental Data for Sri Lanka")



