import streamlit as st
import pandas as pd
from PIL import Image
import os
import numpy as np

# Page configuration
st.set_page_config(page_title="Water Quality Analysis Dashboard", layout="wide")

# File paths
output_dir = "."
parquet_files = {
    'Combined Results': 'combined_results.parquet',
    'Weather Conditions': 'weather_conditions.parquet',
    'Wind Directions': 'wind_directions.parquet',
    'Sites': 'sites.parquet',
    'Site Summary': 'site_summary.parquet',
    'Site Predictions': 'site_predictions.parquet'
}
plot_files = {
    'MAE': 'mae_comparison.png',
    'MSE': 'mse_comparison.png',
    'RMSE': 'rmse_comparison.png',
    'R2 Score': 'r2_comparison.png'
}

# Title & Introduction
st.title("Water Quality Analysis Dashboard")
st.markdown("""
This dashboard displays water quality analysis results, including model performance metrics, site-specific forecasts, and comparisons over time horizons (Next Week, Month, Year).
""")

# Load core data
try:
    combined_results = pd.read_parquet(os.path.join(output_dir, parquet_files['Combined Results']))
except Exception as e:
    st.error(f"Failed to load combined results: {e}")
    st.stop()

# Model Metrics Table
st.header("Model Performance Metrics")
st.dataframe(combined_results, use_container_width=True)

# Data Summaries
st.header("Data Summaries")
col1, col2, col3 = st.columns(3)

for col, key, label in zip([col1, col2, col3], 
                           ['Weather Conditions', 'Wind Directions', 'Sites'], 
                           ['Unique Weather Conditions', 'Unique Wind Directions', 'Unique Sites']):
    with col:
        st.subheader(label)
        try:
            df = pd.read_parquet(os.path.join(output_dir, parquet_files[key]))
            st.table(df)
        except Exception as e:
            st.error(f"Failed to load {key}: {e}")

# Model Performance Visuals
st.header("Model Performance Visualizations")
for metric, plot_file in plot_files.items():
    try:
        image = Image.open(os.path.join(output_dir, plot_file))
        st.image(image, caption=f"{metric} Comparison", use_column_width=True)
    except Exception as e:
        st.error(f"Failed to load {metric} plot: {e}")

# Site-Specific Predictions
st.header("Site-Specific Predictions")
try:
    site_predictions = pd.read_parquet(os.path.join(output_dir, parquet_files['Site Predictions']))
    sites = pd.read_parquet(os.path.join(output_dir, parquet_files['Sites']))
    
    site_list = sorted(sites['site'].dropna().unique())
    selected_site = st.selectbox("Select Site", site_list)

    model_list = sorted(combined_results['Model'].dropna().unique())
    selected_model = st.selectbox("Select Model", model_list)

    horizons = ["Next Week", "Next Month", "Next Year"]
    selected_horizon = st.selectbox("Select Prediction Horizon", horizons, key="horizon_pred")

    # Filter data
    site_data = site_predictions[
        (site_predictions['site'] == selected_site) &
        (site_predictions['model'] == selected_model) &
        (site_predictions['horizon'] == selected_horizon)
    ]

    if not site_data.empty:
        st.subheader(f"{selected_site} - {selected_model} ({selected_horizon})")

        pred_cols = [col for col in site_data.columns if col.startswith('pred_')]
        site_data_limited = site_data.head(10)

        # Summary stats
        summary = site_data_limited[pred_cols].agg(['mean', 'min', 'max', 'std']).transpose()
        summary.reset_index(inplace=True)
        summary['Metric'] = summary['index'].str.replace('pred_', '')
        summary = summary[['Metric', 'mean', 'min', 'max', 'std']]
        summary = summary.round(3).fillna("nan")

        st.dataframe(summary, use_container_width=True, height=400)

        if len(site_data) == 1:
            st.warning("Only one prediction found; standard deviation is undefined.")
    else:
        st.warning("No data available for selected site/model/horizon.")
except Exception as e:
    st.error(f"Site-specific predictions failed: {e}")

# Model Comparison by Time Horizon
st.header("Model Performance Comparison")
try:
    selected_horizon = st.selectbox("Select Time Horizon", horizons, key="horizon_compare")
    metrics = ['Final MAE', 'Final MSE', 'Final RMSE', 'R2 Score']
    horizon_cols = [f"{m} - {selected_horizon}" for m in metrics]

    comparison_df = combined_results[['Model'] + horizon_cols].copy()
    comparison_df[horizon_cols] = comparison_df[horizon_cols].applymap(lambda x: f"{x:.3f}" if isinstance(x, (int, float)) else x)

    def highlight_model(row):
        return ['background-color: #d3d3d3' if row['Model'] == selected_model else '' for _ in row]

    st.subheader(f"{selected_horizon} Comparison")
    st.dataframe(comparison_df.style.apply(highlight_model, axis=1), use_container_width=True)

    selected_metrics = comparison_df[comparison_df['Model'] == selected_model]
    st.markdown(f"**Metrics for {selected_model} ({selected_horizon}):**")
    for metric, val in selected_metrics[horizon_cols].iloc[0].items():
        st.markdown(f"- {metric}: {val}")
except Exception as e:
    st.error(f"Comparison failed: {e}")

# Footer
st.markdown("""
---
**Note**: Ensure all required files (Parquet and PNGs) are available in the working directory.  
Run with: `streamlit run streamlit_app.py`  
Dependencies: `pip install streamlit pandas pillow pyarrow numpy`
""")
