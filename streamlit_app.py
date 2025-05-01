import streamlit as st
import pandas as pd
from PIL import Image
import os

# Set page configuration
st.set_page_config(page_title="Water Quality Analysis Dashboard", layout="wide")

# Define file paths (relative to the script in the GitHub repository)
output_dir = "."  # Files are in the same directory as the script
parquet_files = {
    'Combined Results': 'combined_results.parquet',
    'Weather Conditions': 'weather_conditions.parquet',
    'Wind Directions': 'wind_directions.parquet',
    'Sites': 'sites.parquet',
    'Site Summary': 'site_summary.parquet'
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
    st.error(f"Error: '{parquet_files['Combined Results']}' not found in {output_dir}. Ensure the file is included in the GitHub repository.")
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
        st.error(f"Error: '{plot_file}' not found in {output_dir}. Ensure the plot is included in the GitHub repository.")
    except Exception as e:
        st.error(f"Error loading {metric} plot: {str(e)}")

# Site-specific summary with dual-criteria dropdown
st.header("Site-Specific Summary")
try:
    # Load site summary and sites data
    site_summary = pd.read_parquet(os.path.join(output_dir, parquet_files['Site Summary']))
    sites = pd.read_parquet(os.path.join(output_dir, parquet_files['Sites']))
    
    # Create dropdown for site selection
    site_list = sites['site'].dropna().unique().tolist()
    selected_site = st.selectbox("Select a Site", options=site_list, key="site_select")
    
    # Create dropdown for model selection
    model_list = combined_results['Model'].unique().tolist()
    selected_model = st.selectbox("Select a Model", options=model_list, key="model_select")
    
    # Filter summary for selected site
    site_data = site_summary[site_summary['site'] == selected_site]
    
    if not site_data.empty:
        st.subheader(f"Summary Statistics for {selected_site}")
        # Transpose the data to make columns into rows
        site_data_transposed = site_data.drop(columns=['site']).melt(var_name='Metric', value_name='Value')
        # Format numerical values to 3 decimal places
        site_data_transposed['Value'] = site_data_transposed['Value'].apply(lambda x: f"{x:.3f}" if isinstance(x, (int, float)) else x)
        # Display the transposed table
        st.dataframe(site_data_transposed, use_container_width=True, height=600)
    else:
        st.warning(f"No summary data available for {selected_site}.")
except FileNotFoundError as e:
    st.error(f"Error: Unable to load site summary or sites file. Ensure '{parquet_files['Site Summary']}' and '{parquet_files['Sites']}' are in {output_dir}.")
except Exception as e:
    st.error(f"Error displaying site summary: {str(e)}")

# Model performance comparison section
st.header("Model Performance Comparison")
try:
    # Dropdown for time horizon selection
    time_horizons = ["Next Week", "Next Month", "Next Year"]
    selected_horizon = st.selectbox("Select Time Horizon for Comparison", options=time_horizons, key="horizon_select")
    
    # Extract metrics for the selected time horizon
    metrics = ['Final MAE', 'Final MSE', 'Final RMSE', 'R2 Score']
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
**Note**: Ensure all required files (Parquet and PNGs) are included in the GitHub repository in the same directory as this script.
To deploy this app on Streamlit Cloud, link your GitHub repository and specify this script as the entry point.
To run locally, install dependencies (`pip install streamlit pandas pillow pyarrow`) and execute `streamlit run streamlit_app.py`.
""")
