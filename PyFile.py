import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Virat Kohli 100s Analyzer", layout="wide")
st.title("🏏 Virat Kohli 100s — Data Visualizer")
st.caption("No file upload needed — data loads from backend!")

# 🗂 Load CSV
DATA_FILE = "Virat_Kohli_100s.csv"

if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)

    # Extract year if not already present
    if "Year" not in df.columns and "Date" in df.columns:
        df["Year"] = pd.to_datetime(df["Date"], errors='coerce').dt.year

    # Clean Score column
    df["Score"] = df["Score"].astype(str).str.replace("*", "", regex=False).astype(int)

    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    formats = st.sidebar.multiselect("Format", df["Format"].unique(), default=df["Format"].unique())
    years = st.sidebar.multiselect("Year", sorted(df["Year"].dropna().unique()), default=sorted(df["Year"].dropna().unique()))
    opponents = st.sidebar.multiselect("Against", df["Against"].unique(), default=df["Against"].unique())

    # Apply filters
    filtered_df = df[
        df["Format"].isin(formats) &
        df["Year"].isin(years) &
        df["Against"].isin(opponents)
    ]

    # 📈 Summary metrics
    st.markdown("### 📊 Summary Stats")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Centuries", len(filtered_df))
    col2.metric("Total Score", filtered_df["Score"].sum())
    col3.metric("Average Score", round(filtered_df["Score"].mean(), 2))

    # 🗓️ Centuries by Year
    st.markdown("### 📅 Centuries by Year")
    year_chart = filtered_df.groupby("Year").size().reset_index(name="Centuries")
    fig1 = px.bar(year_chart, x="Year", y="Centuries", text="Centuries")
    st.plotly_chart(fig1, use_container_width=True)

    # 🏟️ Centuries by Opponent
    st.markdown("### 🏟️ Centuries by Opponent")
    opp_chart = filtered_df.groupby("Against").size().reset_index(name="Centuries")
    fig2 = px.bar(opp_chart, x="Against", y="Centuries", text="Centuries")
    st.plotly_chart(fig2, use_container_width=True)

    # 🏏 Total Score by Format (Pie)
    st.markdown("### 🏏 Score by Format")
    format_chart = filtered_df.groupby("Format")["Score"].sum().reset_index()
    fig3 = px.pie(format_chart, names="Format", values="Score", title="Total Score by Format")
    st.plotly_chart(fig3, use_container_width=True)

    # 🥇 Top 10 Highest Scores
    st.markdown("### 🥇 Top 10 Highest Scores")
    top_scores = filtered_df.sort_values(by="Score", ascending=False).head(10)
    fig4 = px.bar(top_scores, x="Score", y="Against", color="Format", orientation="h", text="Score")
    fig4.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig4, use_container_width=True)

    # 📊 Average Score by Format
    st.markdown("### 📈 Average Score by Format")
    avg_score_format = filtered_df.groupby("Format")["Score"].mean().reset_index()
    fig5 = px.bar(avg_score_format, x="Format", y="Score", text=avg_score_format["Score"].round(2))
    st.plotly_chart(fig5, use_container_width=True)

    # 🧠 Pie: Century Count by Opponent
    st.markdown("### 🍕 Centuries by Opponent (Pie)")
    opp_pie = filtered_df.groupby("Against").size().reset_index(name="Centuries")
    fig6 = px.pie(opp_pie, names="Against", values="Centuries")
    st.plotly_chart(fig6, use_container_width=True)

else:
    st.error(f"CSV file not found at `{DATA_FILE}`. Please add it to your repo.")
