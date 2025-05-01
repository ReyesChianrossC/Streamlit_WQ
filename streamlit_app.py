import streamlit as st
import pandas as pd
from PIL import Image
import os
import numpy as np

# Set page configuration
st.set_page_config(page_title="Water Quality Analysis Dashboard", layout="wide")

# Define file paths
output_dir = "."  # Update to your directory if running locally
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

# Title
st.title("Water Quality Analysis Dashboard")

# Introduction
st.markdown("""
This dashboard displays the results of a water quality analysis, including model performance metrics, data summaries, site-specific statistics, and model comparisons.
The metrics compare different models for predicting water quality parameters over various time horizons (Next Week, Next Month, Next Year).
""")

# Load and display combined results
st.header("Model Performance Metrics")
try:
    combined_results = pd.read_parquet(os.path.join(output_dir, parquet_files['Combined Results']))
    st.dataframe(combined_results, use_container_width=True)
except FileNotFoundError:
    st.error(f"Error: '{parquet_files['Combined Results']}' not found snarled {output_dir}.")
except Exception as e:
    st.error(f"Error loading combined results: {str(e)}")

# Load and display unique weather conditions, wind directions, and sites
st.header("Data Summaries")
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Unique Weather Conditions")
    try:
        weather_conditions = pd.read_parquet(os.path.join(output_dir, parquet_files['Weather Conditions']))
        st.table(weather_conditions)
    except FileNotFoundError:
        st.error(f"Error: '{parquet_files['Weather Conditions']}' not found in {output_dir}.")
    except Exception as e:
        st.error(f"Error loading weather conditions: {str(e)}")

with col2:
    st.subheader("Unique Wind Directions")
    try:
        wind_directions = pd.read_parquet(os.path.join(output_dir, parquet_files['Wind Directions']))
        st.table(wind_directions)
    except FileNotFoundError:
        st.error(f"Error: '{parquet_files['Wind Directions']}' not found in {output_dir}.")
    except Exception as e:
        st.error(f"Error loading wind directions: {str(e)}")

with col3:
    st.subheader("Unique Sites")
    try:
        sites = pd.read_parquet(os.path.join(output_dir, parquet_files['Sites']))
        st.table(sites)
    except FileNotFoundError:
        st.error(f"Error: '{parquet_files['Sites']}' not found in {output_dir}.")
    except Exception as e:
        st.error(f"Error loading sites: {str(e)}")

# Display comparison plots
st.header("Model Performance Visualizations")
for metric, plot_file in plot_files.items():
    st.subheader(f"{metric} Comparison")
    try:
        image = Image.open(os.path.join(output_dir, plot_file))
        st.image(image, caption=f"{metric} Comparison Across Models", use_column_width=True)
    except FileNotFoundError:
        st.error(f"Error: '{plot_file}' not found in {output_dir}.")
    except Exception as e:
        st.error(f"Error loading {metric} plot: {str(e)}")

# Site-specific summary with dual-criteria dropdown
st.header("Site-Specific Predictions")
try:
    # Load site predictions and sites data
    site_predictions = pd.read_parquet(os.path.join(output_dir, parquet_files['Site Predictions']))
    sites = pd.read_parquet(os.path.join(output_dir, parquet_files['Sites']))
    
    # Create dropdown for site selection
    site_list = sites['site'].dropna().unique().tolist()
    selected_site = st.selectbox("Select a Site", options=site_list, key="site_select")
    
    # Create dropdown for model selection
    model_list = combined_results['Model'].unique().tolist()
    selected_model = st.selectbox("Select a Model", options=model_list, key="model_select")
    
    # Create dropdown for horizon selection
    horizon_list = ["Next Week", "Next Month", "Next Year"]
    selected_horizon = st.selectbox("Select Prediction Horizon", options=horizon_list, key="horizon_select_predictions")
    
    # Filter predictions for selected site, model, and horizon
    site_data = site_predictions[
        (site_predictions['site'] == selected_site) &
        (site_predictions['model'] == selected_model) &
        (site_predictions['horizon'] == selected_horizon)
    ]
    
    # Debug number of rows
    st.write(f"Number of predictions for {selected_site}, {selected_model}, {selected_horizon}: {len(site_data)}")
    
    if not site_data.empty:
        st.subheader(f"Predicted Water Quality for {selected_site} ({selected_model}, {selected_horizon})")
        # Compute summary statistics on predictions
        pred_cols = [col for col in site_data.columns if col.startswith('pred_')]
        
        # Limit to the first 5 metrics (to ensure only 5 rows)
        pred_cols_limited = pred_cols[:5]  # Select only the first 5 metrics
        
        # Limit to 10 rows for summary statistics if more than 10 predictions
        if len(site_data) > 10:
            st.write("More than 10 predictions available. Displaying summary statistics based on the first 10 predictions.")
            site_data_limited = site_data.head(10)
        else:
            site_data_limited = site_data
        
        # Compute summary statistics (mean, min, max, std) for the limited metrics
        summary_data = site_data_limited[pred_cols_limited].agg(['mean', 'min', 'max', 'std']).transpose().reset_index()
        summary_data['Metric'] = summary_data['index'].str.replace('pred_', '')
        summary_data = summary_data[['Metric', 'mean', 'min', 'max', 'std']]
        
        # Format numerical values to 3 decimal places
        for col in ['mean', 'min', 'max', 'std']:
            summary_data[col] = summary_data[col].apply(lambda x: f"{x:.3f}" if isinstance(x, (int, float)) and not np.isnan(x) else "nan")
        
        # Display the summary table
        st.dataframe(summary_data, use_container_width=True, height=300)  # Adjusted height for 5 rows
        
        # Add a note if there’s only one prediction
        if len(site_data) == 1:
            st.warning("Only one prediction available. Standard deviation is undefined for a single data point.")
    else:
        st.warning(f"No prediction data available for {selected_site}, {selected_model}, {selected_horizon}.")
except FileNotFoundError as e:
    st.error(f"Error: Unable to load site predictions or sites file. Ensure '{parquet_files['Site Predictions']}' and '{parquet_files['Sites']}' are in {output_dir}.")
except Exception as e:
    st.error(f"Error displaying site predictions: {str(e)}")

# Model performance comparison section
st.header("Model Performance Comparison")
try:
    # Dropdown for time horizon selection
    time_horizons = ["Next Week", "Next Month", "Next Year"]
    selected_horizon = st.selectbox("Select Time Horizon for Comparison", options=time_horizons, key="horizon_select")
    
    # Extract metrics for the selected time horizon
    metrics = ['Final MAE', "Final MSE", 'Final RMSE', 'R2 Score']
    horizon_columns = [f"{metric} - {selected_horizon}" for metric in metrics]
    
    # Prepare comparison DataFrame
    comparison_df = combined_results[['Model'] + horizon_columns].copy()
    # Format numerical values to 3 decimal places
    for col in horizon_columns:
        comparison_df[col] = comparison_df[col].apply(lambda x: f"{x:.3f}" if isinstance(x, (int, float)) else x)
    
    # Highlight the selected model's row with a more visible color
    def highlight_selected_model(row):
        return ['background-color: #a9a9a9' if row['Model'] == selected_model else '' for _ in row]
    
    st.subheader(f"Model Comparison for {selected_horizon} Prediction")
    st.dataframe(comparison_df.style.apply(highlight_selected_model, axis=1), use_container_width=True)
    
    # Display the selected model's metrics explicitly
    selected_model_metrics = comparison_df[comparison_df['Model'] == selected_model]
    st.markdown(f"**Selected Model ({selected_model}) Metrics for {selected_horizon}:**")
    for metric, value in selected_model_metrics[horizon_columns].iloc[0].items():
        st.markdown(f"- {metric}: {value}")
except Exception as e:
    st.error(f"Error displaying model comparison: {str(e)}")

# Footer
st.markdown("""
---
**Note**: Ensure all required files (Parquet and PNGs) are included in the directory.
To run locally, install dependencies (`pip install streamlit pandas pillow pyarrow numpy`) and execute `streamlit run streamlit_app.py`.
""")
