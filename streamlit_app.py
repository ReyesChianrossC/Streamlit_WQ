import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import os
import numpy as np

# Page setup
# Set page configuration
st.set_page_config(page_title="Water Quality Analysis Dashboard", layout="wide")

# File paths
output_dir = "."
# Define file paths (relative to the script)
output_dir = "/content"  # Adjust as needed for your environment
# Define file paths (relative to the script in the GitHub repository)
output_dir = "."  # Files are in the same directory as the script
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
'Combined Results': 'combined_results.parquet',
'Weather Conditions': 'weather_conditions.parquet',
@@ -38,7 +37,7 @@
combined_results = pd.read_parquet(os.path.join(output_dir, parquet_files['Combined Results']))
st.dataframe(combined_results, use_container_width=True)
except FileNotFoundError:
    st.error(f"Error: '{parquet_files['Combined Results']}' not found in {output_dir}.")
    st.error(f"Error: '{parquet_files['Combined Results']}' not found in {output_dir}. Ensure the file is included in the GitHub repository.")
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

        # Convert columns to numeric and round to 3 decimals
        for col in ['Mean', 'Min', 'Max', 'Std']:
            summary[col] = pd.to_numeric(summary[col], errors='coerce').round(3).astype(str)
        
        # Display the summary dataframe
        st.dataframe(summary, use_container_width=True, height=600)
        
        # Display a warning if only one prediction is available
        if len(filtered) == 1:
            st.warning("Only one prediction available. Standard deviation is undefined.")
    else:
        st.warning("No data available for the selected site, model, and horizon.")

    # Additional numeric metrics summary
    st.subheader("Numeric Metrics Summary")
    try:
        # Define the 10 numeric metrics to include
        numeric_metrics_list = [
            'surface_temperature', 'middle_temperature', 'bottom_temperature',
            'ph', 'ammonia', 'nitrate', 'phosphate',
            'dissolved_oxygen', 'sulfide', 'carbon_dioxide'
        ]

        # Filter only the required columns from the DataFrame
        numeric_df = filtered[numeric_metrics_list]

        # Create summary statistics table
        summary_df = numeric_df.describe().transpose().reset_index()
        summary_df.rename(columns={'index': 'Metric', 'mean': 'Mean', 'min': 'Min', 'max': 'Max', 'std': 'Std'}, inplace=True)

        # Display only the first 10 rows (optional safeguard)
        summary_df = summary_df.head(10)

        # Display in Streamlit
        st.dataframe(summary_df, use_container_width=True)

    except Exception as e:
        st.error(f"Error displaying numeric metrics summary: {e}")
st.error(f"Error loading combined results: {str(e)}")

@@ -84,7 +83,7 @@
image = Image.open(os.path.join(output_dir, plot_file))
st.image(image, caption=f"{metric} Comparison Across Models", use_column_width=True)
except FileNotFoundError:
        st.error(f"Error: '{plot_file}' not found in {output_dir}.")
        st.error(f"Error: '{plot_file}' not found in {output_dir}. Ensure the plot is included in the GitHub repository.")
except Exception as e:
st.error(f"Error loading {metric} plot: {str(e)}")

@@ -121,7 +120,7 @@
except Exception as e:
    st.error(f"Error processing site-specific predictions: {e}")
st.error(f"Error displaying site summary: {str(e)}")

# Model comparison
# Model performance comparison section with bar chart
# Model performance comparison section
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
# Dropdown for time horizon selection
@@ -134,40 +133,29 @@

# Prepare comparison DataFrame
comparison_df = combined_results[['Model'] + horizon_columns].copy()
    # Convert to numeric for plotting
    # Format numerical values to 3 decimal places
for col in horizon_columns:
        comparison_df[col] = pd.to_numeric(comparison_df[col], errors='coerce')
        comparison_df[col] = comparison_df[col].apply(lambda x: f"{x:.3f}" if isinstance(x, (int, float)) else x)

    # Highlight the selected model's row in the table
    # Highlight the selected model's row with a more visible color
def highlight_selected_model(row):
return ['background-color: #a9a9a9' if row['Model'] == selected_model else '' for _ in row]

st.subheader(f"Model Comparison for {selected_horizon} Prediction")
st.dataframe(comparison_df.style.apply(highlight_selected_model, axis=1), use_container_width=True)

    # Create grouped bar chart
    plot_df = comparison_df.melt(id_vars='Model', var_name='Metric', value_name='Value')
    fig = px.bar(plot_df,
                 x='Model',
                 y='Value',
                 color='Metric',
                 barmode='group',
                 title=f"Model Comparison for {selected_horizon} Prediction",
                 labels={'Value': 'Metric Value', 'Model': 'Model'},
                 height=500)
    st.plotly_chart(fig, use_container_width=True)
    
# Display the selected model's metrics explicitly
selected_model_metrics = comparison_df[comparison_df['Model'] == selected_model]
st.markdown(f"**Selected Model ({selected_model}) Metrics for {selected_horizon}:**")
for metric, value in selected_model_metrics[horizon_columns].iloc[0].items():
        st.markdown(f"- {metric}: {value:.3f}")
        st.markdown(f"- {metric}: {value}")
except Exception as e:
    st.error(f"Error displaying model comparison: {e}")
st.error(f"Error displaying model comparison: {str(e)}")

# Footer
st.markdown("""
---
**Note**: Ensure all required files (Parquet and PNGs) are included in the `/content` directory.
To run locally, install dependencies (`pip install streamlit pandas pillow pyarrow plotly`) and execute `streamlit run water_quality_analysis.py`.
**Note**: Ensure all required files (Parquet and PNGs) are included in the GitHub repository in the same directory as this script.
To deploy this app on Streamlit Cloud, link your GitHub repository and specify this script as the entry point.
To run locally, install dependencies (`pip install streamlit pandas pillow pyarrow`) and execute `streamlit run streamlit_app.py`.
""")
