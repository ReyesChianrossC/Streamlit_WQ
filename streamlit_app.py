import streamlit as st
import pandas as pd
import os

st.title("Water Quality Prediction Results")

# Load Parquet file from root directory
parquet_path = "combined_results.parquet"
if os.path.exists(parquet_path):
    df = pd.read_parquet(parquet_path)
    st.subheader("Combined Metrics Table")
    st.dataframe(df)
else:
    st.error("Parquet file not found. Please run the pipeline first.")

# Display plots from root directory
plot_files = [
    "mae_comparison.png",
    "mse_comparison.png",
    "rmse_comparison.png",
    "r2_comparison.png"  # This is the actual filename in your repo
]
st.subheader("Metric Plots")
for plot_file in plot_files:
    if os.path.exists(plot_file):
        st.image(plot_file, caption=plot_file.replace(".png", "").replace("_", " ").title())
    else:
        st.error(f"Plot file {plot_file} not found. Please run the pipeline first.")
