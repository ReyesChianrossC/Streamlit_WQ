import streamlit as st
import pandas as pd
from PIL import Image
import os

# Set page configuration
st.set_page_config(page_title="Water Quality Analysis Dashboard", layout="wide")

# Define file paths
output_dir = '/content'  # Adjust for local or other environments as needed
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
This dashboard displays the results of a water quality analysis, including model performance mot performance metrics, data summaries, and site-specific statistics.
The metrics compare different models for predicting water quality parameters over various time horizons (Next Week, Next Month, Next Year).
""")

# Load and display combined results
st.header("Model Performance Metrics")
try:
    combined_results = pd.read_parquet(os.path.join(output_dir, parquet_files['Combined Results']))
    st.dataframe(combined_results, use_container_width=True)
except FileNotFoundError:
    st.error(f"Error: '{parquet_files['Combined Results']}' not found in {output_dir}. Please ensure the file is generated and saved correctly.")
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
        st.image(image, caption=f"{metric} Comparison Across Models", use_container_width=True)
    except FileNotFoundError:
        st.error(f"Error: '{plot_file}' not found in {output_dir}. Please ensure the plot is generated and saved correctly.")
    except Exception as e:
        st.error(f"Error loading {metric} plot: {str(e)}")

# Site-specific summary with dropdown
st.header("Site-Specific Summary")
try:
    # Load site summary and sites data
    site_summary = pd.read_parquet(os.path.join(output_dir, parquet_files['Site Summary']))
    sites = pd.read_parquet(os.path.join(output_dir, parquet_files['Sites']))
    
    # Create dropdown with unique, non-null sites
    site_list = sites['site'].dropna().unique().tolist()
    selected_site = st.selectbox("Select a Site", options=site_list, key="site_select")
    
    # Filter and display summary for selected site
    site_data = site_summary[site_summary['site'] == selected_site]
    if not site_data.empty:
        st.subheader(f"Summary Statistics for {selected_site}")
        st.dataframe(site_data, use_container_width=True)
    else:
        st.warning(f"No summary data available for {selected_site}.")
except FileNotFoundError as e:
    st.error(f"Error: Unable to load site summary or sites file. Ensure '{parquet_files['Site Summary']}' and '{parquet_files['Sites']}' are in {output_dir}.")
except Exception as e:
    st.error(f"Error displaying site summary: {str(e)}")

# Footer
st.markdown("""
---
**Note**: Ensure all required files (Parquet and PNGs) are in the specified directory (`{}`).
To run this app in Google Colab, install Streamlit (`pip install streamlit pyngrok pyarrow`), set up ngrok, and execute `streamlit run streamlit_app.py`.
To run locally or on Streamlit Cloud, place all files in the same directory as this script and run `streamlit run streamlit_app.py`.
""".format(output_dir))