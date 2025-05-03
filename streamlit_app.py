import streamlit as st
import pandas as pd
import os
import zipfile

st.set_page_config(layout="wide")

st.title("Water Quality Prediction Results")
st.markdown("## Table of Contents")
st.markdown("""
1. [Model Performance Metrics](#model-performance-metrics)  
2. [Compare Models](#compare-models)  
3. [Data Summaries](#data-summaries)  
4. [Model Performance Visualizations](#model-performance-visualizations)  
5. [Site Specific Summary](#site-specific-summary)  
6. [Raw Data Exploration](#raw-data-exploration)  
7. [Download All Graphs](#download-all-graphs)  
8. [Group 1 Members](#group-1-members)  
9. [Contact / More Info](#contact--more-info)
""", unsafe_allow_html=True)

# -------------------------------
# 1. Model Performance Metrics
# -------------------------------
st.markdown("### Model Performance Metrics")

if os.path.exists("combined_results.parquet"):
    df = pd.read_parquet("combined_results.parquet")
    
    forecast_options = {
        "Next Week": ["Final MAE - Next Week", "Final MSE - Next Week", "Final RMSE - Next Week", "R2 Score - Next Week"],
        "Next Month": ["Final MAE - Next Month", "Final MSE - Next Month", "Final RMSE - Next Month", "R2 Score - Next Month"],
        "Next Year": ["Final MAE - Next Year", "Final MSE - Next Year", "Final RMSE - Next Year", "R2 Score - Next Year"]
    }
    
    selected_forecast = st.selectbox("Select Forecast Range", list(forecast_options.keys()))
    
    selected_columns = [col for col in ["Model"] + forecast_options[selected_forecast] if col in df.columns]
    if len(selected_columns) < 2:
        st.error("Not enough valid columns found. Please check the column names in combined_results.parquet.")
    else:
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
    selected_models = st.multiselect("Select Models to Compare", models, default=[models[0], models[1]] if len(models) > 1 else [])
    
    metrics_map = {
        "Next Week": ["Final MAE - Next Week", "Final MSE - Next Week", "Final RMSE - Next Week", "R2 Score - Next Week"],
        "Next Month": ["Final MAE - Next Month", "Final MSE - Next Month", "Final RMSE - Next Month", "R2 Score - Next Month"],
        "Next Year": ["Final MAE - Next Year", "Final MSE - Next Year", "Final RMSE - Next Year", "R2 Score - Next Year"]
    }
    
    selected_forecast = st.selectbox("Select Forecast Range for Comparison", ["Next Week", "Next Month", "Next Year"])
    
    selected_columns = [col for col in ["Model"] + metrics_map[selected_forecast] if col in df.columns]
    if len(selected_columns) < 2:
        st.error("Not enough valid columns found. Please check the column names in combined_results.parquet.")
    else:
        comparison_df = df[df["Model"].isin(selected_models)][selected_columns]
        st.dataframe(comparison_df)
else:
    st.error("combined_results.parquet not found.")

# -------------------------------
# 3. Data Summaries
# -------------------------------
st.markdown("### Data Summaries")

col1, col2, col3 = st.columns(3)

with col1:
    if os.path.exists("weather_conditions.parquet"):
        weather_df = pd.read_parquet("weather_conditions.parquet")
        unique_weather = weather_df['weather_condition'].unique()
        st.write("**Unique Weather Conditions:**")
        weather_df_display = pd.DataFrame(unique_weather, columns=["Weather Condition"])
        st.dataframe(weather_df_display, use_container_width=True)

with col2:
    if os.path.exists("wind_directions.parquet"):
        wind_df = pd.read_parquet("wind_directions.parquet")
        unique_winds = wind_df['wind_direction'].unique()
        st.write("**Unique Wind Directions:**")
        wind_df_display = pd.DataFrame(unique_winds, columns=["Wind Direction"])
        st.dataframe(wind_df_display, use_container_width=True)

with col3:
    if os.path.exists("sites.parquet"):
        site_df = pd.read_parquet("sites.parquet")
        unique_sites = site_df['site'].unique()
        st.write("**Unique Sites:**")
        site_df_display = pd.DataFrame(unique_sites, columns=["Site"])
        st.dataframe(site_df_display, use_container_width=True)

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

    # Define columns for horizontal belt
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write(f"**Summary for {selected_site}:**")
        if 'site' in filtered.columns:
            st.write("**Site:**")
            st.write(filtered['site'].iloc[0])
        if 'avg_surface_temperature' in filtered.columns:
            st.write("**Avg Surface Temp (°C):**")
            st.write(filtered['avg_surface_temperature'].iloc[0])
        if 'avg_middle_temperature' in filtered.columns:
            st.write("**Avg Middle Temp (°C):**")
            st.write(filtered['avg_middle_temperature'].iloc[0])
        if 'avg_bottom_temperature' in filtered.columns:
            st.write("**Avg Bottom Temp (°C):**")
            st.write(filtered['avg_bottom_temperature'].iloc[0])

    with col2:
        if 'avg_ph' in filtered.columns:
            st.write("**Avg pH:**")
            st.write(filtered['avg_ph'].iloc[0])
        if 'avg_ammonia' in filtered.columns:
            st.write("**Avg Ammonia (mg/L):**")
            st.write(filtered['avg_ammonia'].iloc[0])
        if 'avg_nitrate' in filtered.columns:
            st.write("**Avg Nitrate (mg/L):**")
            st.write(filtered['avg_nitrate'].iloc[0])
        if 'avg_phosphate' in filtered.columns:
            st.write("**Avg Phosphate (mg/L):**")
            st.write(filtered['avg_phosphate'].iloc[0])

    with col3:
        if 'avg_dissolved_oxygen' in filtered.columns:
            st.write("**Avg Dissolved Oxygen (mg/L):**")
            st.write(filtered['avg_dissolved_oxygen'].iloc[0])
        if 'avg_sulfide' in filtered.columns:
            st.write("**Avg Sulfide (mg/L):**")
            st.write(filtered['avg_sulfide'].iloc[0])
        if 'avg_carbon_dioxide' in filtered.columns:
            st.write("**Avg Carbon Dioxide (mg/L):**")
            st.write(filtered['avg_carbon_dioxide'].iloc[0])
        if 'avg_air_temperature' in filtered.columns:
            st.write("**Avg Air Temp (°C):**")
            st.write(filtered['avg_air_temperature'].iloc[0])

else:
    st.error("site_summary.parquet not found.")
# -------------------------------
# 6. Raw Data Exploration
# -------------------------------
st.markdown("### Raw Data Exploration")
st.markdown("Explore the raw data files generated from the pipeline.")

# Combined Results
with st.expander("Combined Results"):
    if os.path.exists("combined_results.parquet"):
        df = pd.read_parquet("combined_results.parquet")
        st.write("**Combined Model Metrics (All Forecast Ranges)**")
        st.dataframe(df)
    else:
        st.error("combined_results.parquet not found.")

# Site Summary
with st.expander("Site Summary"):
    if os.path.exists("site_summary.parquet"):
        site_summary = pd.read_parquet("site_summary.parquet")
        st.write("**Site Summary Data**")
        st.dataframe(site_summary)
    else:
        st.error("site_summary.parquet not found.")

# Weather Conditions
with st.expander("Weather Conditions"):
    if os.path.exists("weather_conditions.parquet"):
        weather_df = pd.read_parquet("weather_conditions.parquet")
        st.write("**Weather Conditions Data**")
        st.dataframe(weather_df)
    else:
        st.error("weather_conditions.parquet not found.")

# Wind Directions
with st.expander("Wind Directions"):
    if os.path.exists("wind_directions.parquet"):
        wind_df = pd.read_parquet("wind_directions.parquet")
        st.write("**Wind Directions Data**")
        st.dataframe(wind_df)
    else:
        st.error("wind_directions.parquet not found.")

# Sites
with st.expander("Sites"):
    if os.path.exists("sites.parquet"):
        site_df = pd.read_parquet("sites.parquet")
        st.write("**Sites Data**")
        st.dataframe(site_df)
    else:
        st.error("sites.parquet not found.")

# -------------------------------
# 7. Download All Graphs
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
# 8. Group 1 Members
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
# 9. Contact Section
# -------------------------------
st.markdown("### Contact / More Info")
st.markdown("""
For more information, visit the [https://github.com/ReyesChianrossC](https://github.com/ReyesChianrossC)
""")

# -------------------------------
# 10. Back to Top Anchor
# -------------------------------
st.markdown("---")
st.markdown("<a href='#water-quality-prediction-results'>⬆Back to Top</a>", unsafe_allow_html=True)
