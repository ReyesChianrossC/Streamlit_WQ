import streamlit as st
import pandas as pd
from PIL import Image
import os
import numpy as np

# Page setup
st.set_page_config(page_title="Water Quality Analysis Dashboard", layout="wide")

# File paths
output_dir = "."
parquet_files = {
    'Combined Results': 'combined_results.parquet',
    'Weather Conditions': 'weather_conditions.parquet',
    'Wind Directions': 'wind_directions.parquet',
    'Sites': 'sites.parquet',
    'Site Predictions': 'site_predictions.parquet'
}
plot_files = {
    'MAE': 'mae_comparison.png',
    'MSE': 'mse_comparison.png',
    'RMSE': 'rmse_comparison.png',
    'R2 Score': 'r2_comparison.png'
}

# Title
st.title("Water Quality Analysis Dashboard")

# Introduction
st.markdown("""
This dashboard displays the results of a water quality analysis, including model performance metrics, site-specific predictions, and model comparisons.
""")

# Load combined results
st.header("Model Performance Metrics")
try:
    combined_results = pd.read_parquet(os.path.join(output_dir, parquet_files['Combined Results']))
    st.dataframe(combined_results, use_container_width=True)
except Exception as e:
    st.error(f"Error loading combined results: {e}")

# Data summaries
st.header("Data Summaries")
cols = st.columns(3)
summary_titles = ["Weather Conditions", "Wind Directions", "Sites"]
summary_files = ['Weather Conditions', 'Wind Directions', 'Sites']

for col, title, file_key in zip(cols, summary_titles, summary_files):
    with col:
        st.subheader(f"Unique {title}")
        try:
            df = pd.read_parquet(os.path.join(output_dir, parquet_files[file_key]))
            st.table(df)
        except Exception as e:
            st.error(f"Error loading {title.lower()}: {e}")

# Model performance plots
st.header("Model Performance Visualizations")
for metric, plot_file in plot_files.items():
    st.subheader(f"{metric} Comparison")
    try:
        image = Image.open(os.path.join(output_dir, plot_file))
        st.image(image, caption=f"{metric} Comparison Across Models", use_column_width=True)
    except Exception as e:
        st.error(f"Error loading {plot_file}: {e}")

# Site-specific predictions
st.header("Site-Specific Predictions")
try:
    site_predictions = pd.read_parquet(os.path.join(output_dir, parquet_files['Site Predictions']))
    sites = pd.read_parquet(os.path.join(output_dir, parquet_files['Sites']))
    
    site_list = sites['site'].dropna().unique().tolist()
    selected_site = st.selectbox("Select a Site", options=site_list)
    
    model_list = site_predictions['model'].dropna().unique().tolist()
    selected_model = st.selectbox("Select a Model", options=model_list)
    
    horizon_list = ["Next Week", "Next Month", "Next Year"]
    selected_horizon = st.selectbox("Select Prediction Horizon", options=horizon_list)
    
    filtered = site_predictions[
        (site_predictions['site'] == selected_site) &
        (site_predictions['model'] == selected_model) &
        (site_predictions['horizon'] == selected_horizon)
    ]

    metric_cols = [
        "pred_surface_temperature",
        "pred_middle_temperature",
        "pred_bottom_temperature",
        "pred_ph",
        "pred_ammonia",
        "pred_nitrate",
        "pred_phosphate",
        "pred_dissolved_oxygen",
        "pred_sulfide",
        "pred_carbon_dioxide"
    ]

    if not filtered.empty:
        st.subheader(f"Predicted Water Quality for {selected_site} ({selected_model}, {selected_horizon})")
        limited = filtered.head(10)
        summary = limited[metric_cols].agg(['mean', 'min', 'max', 'std']).T.reset_index()
        summary.columns = ['Metric', 'Mean', 'Min', 'Max', 'Std']
        summary['Metric'] = summary['Metric'].str.replace('pred_', '')
        for col in ['Mean', 'Min', 'Max', 'Std']:
            summary[col] = pd.to_numeric(summary[col], errors='coerce').round(3).astype(str)
        st.dataframe(summary, use_container_width=True, height=600)
        if len(filtered) == 1:
            st.warning("Only one prediction available. Standard deviation is undefined.")
    else:
        st.warning("No data available for the selected site, model, and horizon.")
except Exception as e:
    st.error(f"Error processing site-specific predictions: {e}")

# Model comparison
st.header("Model Performance Comparison")
try:
    selected_horizon = st.selectbox("Select Time Horizon for Comparison", options=horizon_list, key="horizon_compare")
    metrics = ['Final MAE', 'Final MSE', 'Final RMSE', 'R2 Score']
    horizon_cols = [f"{m} - {selected_horizon}" for m in metrics]

    comparison_df = combined_results[['Model'] + horizon_cols].copy()
    for col in horizon_cols:
        comparison_df[col] = pd.to_numeric(comparison_df[col], errors='coerce').round(3).astype(str)

    def highlight_selected(row):
        return ['background-color: #d3d3d3' if row['Model'] == selected_model else '' for _ in row]

    st.subheader(f"Comparison for {selected_horizon}")
    st.dataframe(comparison_df.style.apply(highlight_selected, axis=1), use_container_width=True)

    selected_metrics = comparison_df[comparison_df['Model'] == selected_model]
    if not selected_metrics.empty:
        st.markdown(f"**Selected Model ({selected_model}) Metrics for {selected_horizon}:**")
        for m, v in selected_metrics[horizon_cols].iloc[0].items():
            st.markdown(f"- {m}: {v}")
except Exception as e:
    st.error(f"Error displaying model comparison: {e}")
