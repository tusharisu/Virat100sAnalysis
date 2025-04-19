import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Virat Kohli 100s Analyzer", layout="wide")
st.title("🏏 Virat Kohli 100s — Offline Analyzer")
st.caption("Auto-loaded data from backend (no file upload needed!)")

# 🗂 Load the CSV from backend
DATA_FILE = "Virat_Kohli_100s.csv"

if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)

    # Clean and prepare
    if "Year" not in df.columns and "Date" in df.columns:
        df["Year"] = pd.to_datetime(df["Date"], errors='coerce').dt.year

    df["Score"] = df["Score"].astype(str).str.replace("*", "", regex=False).astype(int)

    st.subheader("📋 Raw Data Preview")
    st.dataframe(df)

    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    formats = st.sidebar.multiselect("Format", df["Format"].unique(), default=df["Format"].unique())
    years = st.sidebar.multiselect("Year", sorted(df["Year"].dropna().unique()), default=sorted(df["Year"].dropna().unique()))
    opponents = st.sidebar.multiselect("Against", df["Against"].unique(), default=df["Against"].unique())

    filtered_df = df[
        df["Format"].isin(formats) &
        df["Year"].isin(years) &
        df["Against"].isin(opponents)
    ]

    st.subheader(f"📊 Filtered Data — {len(filtered_df)} Centuries")
    st.dataframe(filtered_df)

    # Summary metrics
    st.markdown("### 📈 Summary Stats")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Centuries", len(filtered_df))
    col2.metric("Total Score", filtered_df["Score"].sum())
    col3.metric("Average Score", round(filtered_df["Score"].mean(), 2))

    # Charts
    st.markdown("### 📅 Centuries by Year")
    year_chart = filtered_df.groupby("Year").size().reset_index(name="Centuries")
    fig1 = px.bar(year_chart, x="Year", y="Centuries", text="Centuries")
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("### 🏟️ Centuries by Opponent")
    opp_chart = filtered_df.groupby("Against").size().reset_index(name="Centuries")
    fig2 = px.bar(opp_chart, x="Against", y="Centuries", text="Centuries")
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### 🏏 Score by Format")
    format_chart = filtered_df.groupby("Format")["Score"].sum().reset_index()
    fig3 = px.pie(format_chart, names="Format", values="Score", title="Total Score by Format")
    st.plotly_chart(fig3, use_container_width=True)

else:
    st.error(f"CSV file not found at `{DATA_FILE}`. Please add it to your repo.")
