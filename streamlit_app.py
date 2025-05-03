import os
import pandas as pd
import streamlit as st
from PIL import Image
import zipfile
import io
from uuid import uuid4

# Set page configuration
st.set_page_config(page_title="Water Quality Analysis Dashboard", layout="wide")

# Define local output directory
local_output_dir = '/content'

# Title
st.title("Water Quality Analysis Dashboard")
st.markdown("""
This dashboard displays the results of a water quality analysis, including model performance metrics, 
data summaries, site-specific statistics, and model comparisons across different time horizons 
(Next Week, Next Month, Next Year).
""")

# Table of Contents
st.header("Table of Contents")
st.markdown("""
- [Model Performance Metrics](#model-performance-metrics)
- [Data Summaries](#data-summaries)
- [Model Performance Visualizations](#model-performance-visualizations)
- [Site-Specific Predictions](#site-specific-predictions)
- [Model Performance Comparison](#model-performance-comparison)
- [Download All Results](#download-all-results)
""")

# Model Performance Metrics
st.header("Model Performance Metrics", anchor="model-performance-metrics")
try:
    combined_results = pd.read_parquet(os.path.join(local_output_dir, 'combined_results.parquet'))
    st.dataframe(combined_results.style.format({col: "{:.3f}" for col in combined_results.columns if col != 'Model'}),
                 use_container_width=True)
except Exception as e:
    st.error(f"Error loading model performance metrics: {str(e)}")

# Data Summaries
st.header("Data Summaries", anchor="data-summaries")
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Unique Weather Conditions")
    try:
        weather_conditions = pd.read_parquet(os.path.join(local_output_dir, 'weather_conditions.parquet'))
        st.table(weather_conditions)
    except Exception as e:
        st.error(f"Error loading weather conditions: {str(e)}")

with col2:
    st.subheader("Unique Wind Directions")
    try:
        wind_directions = pd.read_parquet(os.path.join(local_output_dir, 'wind_directions.parquet'))
        st.table(wind_directions)
    except Exception as e:
        st.error(f"Error loading wind directions: {str(e)}")

with col3:
    st.subheader("Unique Sites")
    try:
        sites = pd.read_parquet(os.path.join(local_output_dir, 'sites.parquet'))
        st.table(sites)
    except Exception as e:
        st.error(f"Error loading sites: {str(e)}")

# Model Performance Visualizations
st.header("Model Performance Visualizations", anchor="model-performance-visualizations")
for metric, caption in [
    ('mae_comparison.png', 'MAE Comparison'),
    ('mse_comparison.png', 'MSE Comparison'),
    ('rmse_comparison.png', 'RMSE Comparison'),
    ('r2_comparison.png', 'R2 Score Comparison')
]:
    st.subheader(caption)
    try:
        image = Image.open(os.path.join(local_output_dir, metric))
        st.image(image, caption=caption, use_column_width=True)
    except Exception as e:
        st.error(f"Error loading {metric}: {str(e)}")

# Site-Specific Predictions
st.header("Site-Specific Predictions", anchor="site-specific-predictions")
try:
    site_predictions = pd.read_parquet(os.path.join(local_output_dir, 'site_predictions.parquet'))
    sites = pd.read_parquet(os.path.join(local_output_dir, 'sites.parquet'))
    combined_results = pd.read_parquet(os.path.join(local_output_dir, 'combined_results.parquet'))

    site_list = sites['site'].dropna().unique().tolist()
    selected_site = st.selectbox("Select a Site", options=site_list, key="site_select")

    model_list = combined_results['Model'].unique().tolist()
    selected_model = st.selectbox("Select a Model", options=model_list, key="model_select")

    horizon_list = ["Next Week", "Next Month", "Next Year"]
    selected_horizon = st.selectbox("Select Prediction Horizon", options=horizon_list, key="horizon_select_predictions")

    st.markdown(f"**{selected_site} - {selected_model} - {selected_horizon}**")

    site_data = site_predictions[
        (site_predictions['site'] == selected_site) &
        (site_predictions['model'] == selected_model) &
        (site_predictions['horizon'] == selected_horizon)
    ]

    st.write(f"Number of predictions: {len(site_data)}")

    if not site_data.empty:
        st.subheader(f"Predicted Water Quality for {selected_site} ({selected_model}, {selected_horizon})")
        pred_cols = [col for col in site_data.columns if col.startswith('pred_')]

        if len(site_data) > 10:
            st.write("More than 10 predictions available. Displaying summary statistics based on the first 10 predictions.")
            site_data_limited = site_data.head(10)
        else:
            site_data_limited = site_data

        summary_data = site_data_limited[pred_cols].agg(['mean', 'min', 'max', 'std']).transpose().reset_index()
        summary_data['Metric'] = summary_data['index'].str.replace('pred_', '')
        summary_data = summary_data[['Metric', 'mean', 'min', 'max', 'std']]

        summary_data = summary_data.round(3)
        st.dataframe(summary_data, use_container_width=True, height=600)

        if len(site_data) == 1:
            st.warning("Only one prediction available. Standard deviation is undefined for a single data point.")
    else:
        st.warning(f"No prediction data available for {selected_site}, {selected_model}, {selected_horizon}.")

    # Site Summary Table
    st.subheader("Site Summary Statistics")
    try:
        site_summary = pd.read_parquet(os.path.join(local_output_dir, 'site_summary.parquet'))
        site_summary_filtered = site_summary[site_summary['site'] == selected_site]
        if not site_summary_filtered.empty:
            st.dataframe(site_summary_filtered.style.format({col: "{:.3f}" for col in site_summary_filtered.columns if col != 'site'}),
                         use_container_width=True)
        else:
            st.warning(f"No summary data available for {selected_site}.")
    except Exception as e:
        st.error(f"Error loading site summary: {str(e)}")
except Exception as e:
    st.error(f"Error processing site-specific predictions: {str(e)}")

# Model Performance Comparison
st.header("Model Performance Comparison", anchor="model-performance-comparison")
try:
    combined_results = pd.read_parquet(os.path.join(local_output_dir, 'combined_results.parquet'))
    time_horizons = ["Next Week", "Next Month", "Next Year"]
    selected_horizon = st.selectbox("Select Time Horizon for Comparison", options=time_horizons, key="horizon_select")

    metrics = ['Final MAE', 'Final MSE', 'Final RMSE', 'R2 Score']
    horizon_columns = [f"{metric} - {selected_horizon}" for metric in metrics]

    comparison_df = combined_results[['Model'] + horizon_columns].copy()
    comparison_df = comparison_df.round(3)

    def highlight_selected_model(row):
        return ['background-color: #a9a9a9' if row['Model'] == selected_model else '' for _ in row]

    st.subheader(f"Model Comparison for {selected_horizon} Prediction")
    st.dataframe(comparison_df.style.apply(highlight_selected_model, axis=1), use_container_width=True)

    selected_model_metrics = comparison_df[comparison_df['Model'] == selected_model]
    st.markdown(f"**Selected Model ({selected_model}) Metrics for {selected_horizon}:**")
    for metric, value in selected_model_metrics[horizon_columns].iloc[0].items():
        st.markdown(f"- {metric}: {value:.3f}")
except Exception as e:
    st.error(f"Error displaying model comparison: {str(e)}")

# Download All Results
st.header("Download All Results", anchor="download-all-results")
files_to_download = [
    'combined_results.parquet', 'weather_conditions.parquet', 'wind_directions.parquet',
    'sites.parquet', 'site_summary.parquet', 'site_predictions.parquet',
    'mae_comparison.png', 'mse_comparison.png', 'rmse_comparison.png', 'r2_comparison.png'
]

def create_zip():
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file_name in files_to_download:
            file_path = os.path.join(local_output_dir, file_name)
            if os.path.exists(file_path):
                zip_file.write(file_path, file_name)
            else:
                st.warning(f"{file_name} not found and will be skipped.")
    buffer.seek(0)
    return buffer

try:
    st.download_button(
        label="Download All Results",
        data=create_zip(),
        file_name="water_quality_analysis_results.zip",
        mime="application/zip"
    )
except Exception as e:
    st.error(f"Error creating download zip: {str(e)}")

# Scroll to Top Anchor
st.markdown("""
---
[Back to Top](#table-of-contents)
""")

# Footer
st.markdown("""
---
**Note**: To run this app, ensure all required files are present in `/content` and execute `streamlit run water_quality_analysis.py`.
""")
