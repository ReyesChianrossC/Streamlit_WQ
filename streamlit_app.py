import streamlit as st
import pandas as pd
import os

st.title("Water Quality Prediction Results")

# Load Parquet file
parquet_path = "output/combined_results.parquet"
if os.path.exists(parquet_path):
    df = pd.read_parquet(parquet_path)
    st.subheader("Combined Metrics Table")
    st.dataframe(df)
else:
    st.error("Parquet file not found. Please run the pipeline first.")

# Display plots
plot_files = [
    "mae_comparison.png",
    "mse_comparison.png",
    "rmse_comparison.png",
    "r2_score_comparison.png"
]
st.subheader("Metric Plots")
for plot_file in plot_files:
    plot_path = os.path.join("output", plot_file)
    if os.path.exists(plot_path):
        st.image(plot_path, caption=plot_file.replace(".png", "").replace("_", " ").title())
    else:
        st.error(f"Plot file {plot_file} not found. Please run the pipeline first.")
