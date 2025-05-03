import streamlit as st
import pandas as pd
import os
import zipfile

st.set_page_config(layout="wide")

print(df.columns.tolist())

st.title("Water Quality Prediction Results")
st.markdown("## 📋 Table of Contents")
st.markdown("""
1. [Model Performance Metrics](#model-performance-metrics)  
2. [Compare Models](#compare-models)  
3. [Data Summaries](#data-summaries)  
4. [Model Performance Visualizations](#model-performance-visualizations)  
5. [Site Specific Summary](#site-specific-summary)  
6. [Download All Graphs](#download-all-graphs)  
7. [Group 1 Members](#group-1-members)  
8. [Contact / More Info](#contact--more-info)
""", unsafe_allow_html=True)

# -------------------------------
# 1. Model Performance Metrics
# -------------------------------
st.markdown("### Model Performance Metrics")

if os.path.exists("combined_results.parquet"):
    df = pd.read_parquet("combined_results.parquet")
    
    forecast_options = {
        "Next Week": ["Final MAE - Next Week", "Final MSE - Next Week", "Final RMSE - Next Week", "Final R² - Next Week"],
        "Next Month": ["Final MAE - Next Month", "Final MSE - Next Month", "Final RMSE - Next Month", "Final R² - Next Month"],
        "Next Year": ["Final MAE - Next Year", "Final MSE - Next Year", "Final RMSE - Next Year", "Final R² - Next Year"]
    }
    
    selected_forecast = st.selectbox("Select Forecast Range", list(forecast_options.keys()))
    
    selected_columns = ["Model"] + forecast_options[selected_forecast]
    filtered_df = df[selected_columns]
    
    st.dataframe(filtered_df)

else:
    st.error("combined_results.parquet not found.")

# -------------------------------
# 2. Compare Models
# -------------------------------
st.markdown("### Compare Models")
if os.path.exists("combined_results.parquet"):
    df = pd.read_parquet("combined_results.parquet")
    models = df["Model"].unique()
    selected_models = st.multiselect("Select Models to Compare", models, default=[models[0], models[1]])
    selected_forecast = st.selectbox("Select Forecast Range for Comparison", ["Next Week", "Next Month", "Next Year"])
    
    metrics_map = {
        "Next Week": ["Final MAE - Next Week", "Final MSE - Next Week", "Final RMSE - Next Week", "Final R² - Next Week"],
        "Next Month": ["Final MAE - Next Month", "Final MSE - Next Month", "Final RMSE - Next Month", "Final R² - Next Month"],
        "Next Year": ["Final MAE - Next Year", "Final MSE - Next Year", "Final RMSE - Next Year", "Final R² - Next Year"]
    }
    
    comparison_df = df[df["Model"].isin(selected_models)][["Model"] + metrics_map[selected_forecast]]
    st.dataframe(comparison_df)
else:
    st.error("combined_results.parquet not found.")

# -------------------------------
# 3. Data Summaries
# -------------------------------
st.markdown("### Data Summaries")

# Unique weather conditions
if os.path.exists("weather_conditions.parquet"):
    weather_df = pd.read_parquet("weather_conditions.parquet")
    unique_weather = weather_df['weather_condition'].unique()
    st.write("**Unique Weather Conditions:**")
    st.write(unique_weather)
else:
    st.error("weather_conditions.parquet not found.")

# Unique sites
if os.path.exists("sites.parquet"):
    site_df = pd.read_parquet("sites.parquet")
    unique_sites = site_df['site'].unique()
    st.write("**Unique Sites:**")
    st.write(unique_sites)
else:
    st.error("sites.parquet not found.")

# -------------------------------
# 4. Model Performance Visualizations
# -------------------------------
st.markdown("### Model Performance Visualizations")
plot_files = [
    "mae_comparison.png",
    "mse_comparison.png",
    "rmse_comparison.png",
    "r2_comparison.png"
]
for plot_file in plot_files:
    if os.path.exists(plot_file):
        st.image(plot_file, caption=plot_file.replace(".png", "").replace("_", " ").title())
    else:
        st.error(f"{plot_file} not found.")

# -------------------------------
# 5. Site Specific Summary
# -------------------------------
st.markdown("### Site Specific Summary")
if os.path.exists("site_summary.parquet"):
    site_summary = pd.read_parquet("site_summary.parquet")
    site_list = site_summary['site'].unique()
    selected_site = st.selectbox("Select a site:", site_list)
    filtered = site_summary[site_summary['site'] == selected_site]
    st.write(f"Summary for **{selected_site}**:")
    st.dataframe(filtered)
else:
    st.error("site_summary.parquet not found.")

# -------------------------------
# 6. Download All Graphs
# -------------------------------
st.markdown("### Download All Graphs")

zip_filename = "all_graphs.zip"
if st.button("Create ZIP of All Graphs"):
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for plot_file in plot_files:
            if os.path.exists(plot_file):
                zipf.write(plot_file)
    st.success("ZIP file created!")

if os.path.exists(zip_filename):
    with open(zip_filename, "rb") as f:
        st.download_button(
            label="Download All Graphs",
            data=f,
            file_name=zip_filename,
            mime="application/zip"
        )

# -------------------------------
# 7. Group 1 Members
# -------------------------------
st.markdown("### Group 1 Members")
st.markdown("""
- Agana  
- Casa  
- Gregorio  
- Jeremillos  
- Reyes
""")

# -------------------------------
# 8. Contact Section
# -------------------------------
st.markdown("### Contact / More Info")
st.markdown("""
For more information, visit the [https://github.com/ReyesChianrossC](https://github.com/ReyesChianrossC)
""")

# -------------------------------
# 9. Back to Top Anchor
# -------------------------------
st.markdown("---")
st.markdown("<a href='#water-quality-prediction-results'>⬆Back to Top</a>", unsafe_allow_html=True)
