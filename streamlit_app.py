import streamlit as st
import pandas as pd
from PIL import Image
import os
import numpy as np

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

st.title("Water Quality Analysis Dashboard")

st.markdown("""
This dashboard displays model performance metrics, data summaries, site-specific statistics, and model comparisons across different time horizons.
""")

# Combined Results
st.header("Model Performance Metrics")
try:
    combined_results = pd.read_parquet(os.path.join(output_dir, parquet_files['Combined Results']))
    st.dataframe(combined_results, use_container_width=True)
except Exception as e:
    st.error(f"Failed to load Combined Results: {e}")

# Data Summaries
st.header("Data Summaries")
col1, col2, col3 = st.columns(3)

def load_table(parquet_key, label):
    try:
        df = pd.read_parquet(os.path.join(output_dir, parquet_files[parquet_key]))
        st.subheader(label)
        st.table(df)
    except Exception as e:
        st.error(f"Failed to load {label}: {e}")

with col1:
    load_table('Weather Conditions', "Weather Conditions")
with col2:
    load_table('Wind Directions', "Wind Directions")
with col3:
    load_table('Sites', "Sites")

# Model Performance Visualizations
st.header("Model Performance Visualizations")
for metric, plot_file in plot_files.items():
    try:
        image = Image.open(os.path.join(output_dir, plot_file))
        st.subheader(f"{metric} Comparison")
        st.image(image, caption=f"{metric} Across Models", use_column_width=True)
    except Exception as e:
        st.error(f"Failed to load {metric} plot: {e}")

# Site-Specific Predictions
st.header("Site-Specific Predictions")
try:
    site_predictions = pd.read_parquet(os.path.join(output_dir, parquet_files['Site Predictions']))
    sites = pd.read_parquet(os.path.join(output_dir, parquet_files['Sites']))
    site_list = sorted(sites['site'].dropna().unique())
    selected_site = st.selectbox("Select Site", site_list)

    model_list = combined_results['Model'].unique()
    selected_model = st.selectbox("Select Model", model_list)

    horizons = ["Next Week", "Next Month", "Next Year"]
    selected_horizon = st.selectbox("Select Prediction Horizon", horizons)

    # Filter
    filtered = site_predictions[
        (site_predictions['site'] == selected_site) &
        (site_predictions['model'] == selected_model) &
        (site_predictions['horizon'] == selected_horizon)
    ]

    if filtered.empty:
        st.warning(f"No predictions found for {selected_site}, {selected_model}, {selected_horizon}.")
    else:
        st.subheader(f"{selected_site} - {selected_model} - {selected_horizon}")
        metric_cols = [
            'pred_surface_temperature', 'pred_middle_temperature', 'pred_bottom_temperature',
            'pred_pH', 'pred_ammonia', 'pred_nitrate', 'pred_phosphate', 'pred_dissolved_oxygen',
            'pred_sulfide', 'pred_carbon_dioxide', 'pred_weather_condition',
            'pred_wind_direction', 'pred_air_temperature'
        ]
        summary = filtered[metric_cols].agg(['mean', 'min', 'max', 'std']).T.reset_index()
        summary['Metric'] = summary['index'].str.replace('pred_', '').str.replace('_', ' ').str.title()
        summary = summary[['Metric', 'mean', 'min', 'max', 'std']]

        for col in ['mean', 'min', 'max', 'std']:
            summary[col] = pd.to_numeric(summary[col], errors='coerce').round(3)

        st.dataframe(summary, use_container_width=True)
except Exception as e:
    st.error(f"Error processing site-specific predictions: {e}")

# Model Performance Comparison
st.header("Model Performance Comparison")
try:
    selected_horizon = st.selectbox("Select Time Horizon", horizons, key="horizon_compare")
    columns = [f"{m} - {selected_horizon}" for m in ['Final MAE', 'Final MSE', 'Final RMSE', 'R2 Score']]
    comparison_df = combined_results[['Model'] + columns].copy()

    for col in columns:
        comparison_df[col] = pd.to_numeric(comparison_df[col], errors='coerce').round(3)

    def highlight_model(row):
        return ['background-color: #cce5ff' if row['Model'] == selected_model else '' for _ in row]

    st.subheader(f"{selected_horizon} Comparison")
    st.dataframe(comparison_df.style.apply(highlight_model, axis=1), use_container_width=True)

    selected_row = comparison_df[comparison_df['Model'] == selected_model]
    if not selected_row.empty:
        st.markdown(f"**Metrics for {selected_model}**")
        for col in columns:
            st.markdown(f"- {col}: {selected_row.iloc[0][col]}")
except Exception as e:
    st.error(f"Error displaying model comparison: {e}")

# Footer
st.markdown("""
---
**Note**: Make sure all required `.parquet` and `.png` files exist in the working directory.
To run: `pip install streamlit pandas pillow pyarrow numpy` and then `streamlit run streamlit_app.py`.
""")
st.write("Columns in site_predictions:", site_predictions.columns.tolist())
