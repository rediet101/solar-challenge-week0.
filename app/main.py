import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from utils import load_country_frames, METRICS, guess_region_column

st.set_page_config(page_title="Solar Cross-Country Comparison", layout="wide")

st.title("Solar Cross-Country Comparison Dashboard")
st.caption("Compare GHI, DNI, and DHI across Benin, Sierra Leone, and Togo")

COUNTRIES = ["Benin", "Sierra Leone", "Togo"]

with st.sidebar:
    st.header("Controls")
    selected_countries = st.multiselect(
        "Select countries",
        options=COUNTRIES,
        default=COUNTRIES,
    )
    metric = st.selectbox("Metric", options=METRICS, index=0)
    top_n = st.slider("Top regions by average GHI", min_value=3, max_value=20, value=10)

if not selected_countries:
    st.info("Please select at least one country.")
    st.stop()

# Load data
df = load_country_frames(selected_countries)

if df.empty:
    st.warning("No local CSVs found in the data/ folder for the selected countries.")
    st.stop()

# Columns
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"{metric} distribution by Country")
    if metric in df.columns:
        fig, ax = plt.subplots(figsize=(7, 4))
        sns.boxplot(data=df, x="Country", y=metric, palette="Set2", ax=ax)
        ax.set_xlabel("Country")
        ax.set_ylabel(metric)
        st.pyplot(fig)
    else:
        st.info(f"Metric '{metric}' not found in data.")

with col2:
    if "GHI" in df.columns:
        avg_ghi = df.groupby("Country")["GHI"].mean().sort_values(ascending=False)
        st.subheader("Average GHI by Country")
        st.bar_chart(avg_ghi)

st.divider()

# Top regions table
region_col = guess_region_column(df)
if region_col and "GHI" in df.columns:
    st.subheader(f"Top {top_n} {region_col} by average GHI")
    top_regions = (
        df.groupby(["Country", region_col])["GHI"].mean().reset_index()
        .rename(columns={"GHI": "avg_GHI"})
        .sort_values(["avg_GHI"], ascending=False)
        .head(top_n)
    )
    st.dataframe(top_regions, use_container_width=True)
else:
    st.subheader("Country-level averages (no region column found)")
    if "GHI" in df.columns:
        country_avg = df.groupby("Country")["GHI"].mean().reset_index().rename(columns={"GHI": "avg_GHI"})
        st.dataframe(country_avg.sort_values("avg_GHI", ascending=False), use_container_width=True)
    else:
        st.info("GHI not found in data.")

st.caption("Data loaded from local CSVs in the data/ folder. Ensure data/ is present locally; it is gitignored.")
