import streamlit as st
import pandas as pd
import base64
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
    if os.path.exists("sites.parquet"):
        site_df = pd.read_parquet("sites.parquet")
        unique_sites = site_df['site'].unique()
        # Remove None values
        unique_sites = [x for x in unique_sites if x is not None]
        st.write("**Unique Sites:**")
        site_df_display = pd.DataFrame(unique_sites, columns=["Site"])
        st.dataframe(site_df_display, use_container_width=True)

with col2:
    if os.path.exists("weather_conditions.parquet"):
        weather_df = pd.read_parquet("weather_conditions.parquet")
        unique_weather = weather_df['weather_condition'].unique()
        # Remove None values
        unique_weather = [x for x in unique_weather if x is not None]
        st.write("**Unique Weather Conditions:**")
        weather_df_display = pd.DataFrame(unique_weather, columns=["Weather Condition"])
        st.dataframe(weather_df_display, use_container_width=True)

with col3:
    if os.path.exists("wind_directions.parquet"):
        wind_df = pd.read_parquet("wind_directions.parquet")
        unique_winds = wind_df['wind_direction'].unique()
        # Remove None values
        unique_winds = [x for x in unique_winds if x is not None]
        st.write("**Unique Wind Directions:**")
        wind_df_display = pd.DataFrame(unique_winds, columns=["Wind Direction"])
        st.dataframe(wind_df_display, use_container_width=True)



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
    # Remove 'None' from site_list if it exists
    site_list = [site for site in site_list if site is not None]
    selected_site = st.selectbox("Select a site:", site_list)
    filtered = site_summary[site_summary['site'] == selected_site]

    # Define columns for horizontal belt
    col1, col2, col3 = st.columns(3)
    
    with col1:
        data = {
            "Metric": ["Site", "Avg Surface Temp (°C)", "Avg Middle Temp (°C)", "Avg Bottom Temp (°C)"],
            "Value": [
                filtered['site'].iloc[0] if 'site' in filtered.columns else "-",
                filtered['avg_surface_temperature'].iloc[0] if 'avg_surface_temperature' in filtered.columns else "-",
                filtered['avg_middle_temperature'].iloc[0] if 'avg_middle_temperature' in filtered.columns else "-",
                filtered['avg_bottom_temperature'].iloc[0] if 'avg_bottom_temperature' in filtered.columns else "-"
            ]
        }
        df = pd.DataFrame(data)
        st.table(df.style.set_properties(**{'text-align': 'left'}))

    with col2:
        data = {
            "Metric": ["Avg pH", "Avg Ammonia (mg/L)", "Avg Nitrate (mg/L)", "Avg Phosphate (mg/L)"],
            "Value": [
                filtered['avg_ph'].iloc[0] if 'avg_ph' in filtered.columns else "-",
                filtered['avg_ammonia'].iloc[0] if 'avg_ammonia' in filtered.columns else "-",
                filtered['avg_nitrate'].iloc[0] if 'avg_nitrate' in filtered.columns else "-",
                filtered['avg_phosphate'].iloc[0] if 'avg_phosphate' in filtered.columns else "-"
            ]
        }
        df = pd.DataFrame(data)
        st.table(df.style.set_properties(**{'text-align': 'left'}))

    with col3:
        data = {
            "Metric": ["Avg Dissolved Oxygen (mg/L)", "Avg Sulfide (mg/L)", "Avg Carbon Dioxide (mg/L)", "Avg Air Temp (°C)"],
            "Value": [
                filtered['avg_dissolved_oxygen'].iloc[0] if 'avg_dissolved_oxygen' in filtered.columns else "-",
                filtered['avg_sulfide'].iloc[0] if 'avg_sulfide' in filtered.columns else "-",
                filtered['avg_carbon_dioxide'].iloc[0] if 'avg_carbon_dioxide' in filtered.columns else "-",
                filtered['avg_air_temperature'].iloc[0] if 'avg_air_temperature' in filtered.columns else "-"
            ]
        }
        df = pd.DataFrame(data)
        st.table(df.style.set_properties(**{'text-align': 'left'}))

else:
    st.error("site_summary.parquet not found.")# -------------------------------
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
        # Remove rows where 'site' is None
        site_summary = site_summary[site_summary['site'].notna()]
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
        # Remove rows where 'site' is None
        site_df = site_df[site_df['site'].notna()]
        st.write("**Sites Data**")
        st.dataframe(site_df)
    else:
        st.error("sites.parquet not found.")

# -------------------------------
# 7. Downloads
# -------------------------------
st.markdown("### Downloads")

# ZIP for all graphs
zip_filename = "all_graphs.zip"
if not os.path.exists(zip_filename):
    if st.button("Create ZIP of All Graphs"):
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for plot_file in plot_files:
                if os.path.exists(plot_file):
                    zipf.write(plot_file)
        st.success("ZIP file created!")
else:
    with open(zip_filename, "rb") as f:
        st.download_button(
            label="Download ZIP of All Graphs",
            data=f,
            file_name=zip_filename,
            mime="application/zip"
        )

# ZIP for GitHub repo resources (excluding Streamlit file)
github_zip_filename = "github_resources.zip"
if not os.path.exists(github_zip_filename):
    if st.button("Create ZIP of GitHub Repo Resources"):
        with zipfile.ZipFile(github_zip_filename, 'w') as zipf:
            github_files = [
                "weather_conditions.parquet",
                "wind_directions.parquet",
                "sites.parquet",
                "site_summary.parquet",
                "combined_results.parquet"
            ]
            for repo_file in github_files:
                if os.path.exists(repo_file):
                    zipf.write(repo_file)
        st.success("GitHub resources ZIP file created!")
else:
    with open(github_zip_filename, "rb") as f:
        st.download_button(
            label="Download ZIP of GitHub Repo Resources",
            data=f,
            file_name=github_zip_filename,
            mime="application/zip"
        )

# -------------------------------
# 8. Group 1 Members
# -------------------------------
# Create a div to hold the images and center them
image_html = '<div class="center-images">'

# Define links for each member
member_links = {
    "Reyes": "https://www.facebook.com/chian.yooki",
    "Gregorio": "https://www.facebook.com/GregorioAce",
    "Agana": "https://www.facebook.com/jlen.hernan",
    "Casa": "https://www.facebook.com/kaneuzaki",
    "Jeremillos": "https://www.facebook.com/danlynniee"
}

for member in group_members:
    if os.path.exists(member["image"]):
        with open(member["image"], "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
        # Determine MIME type based on file extension
        mime_type = "image/png" if member["image"].lower().endswith(".png") else "image/jpeg"
        # Wrap the image in a hyperlink tag
        link = member_links.get(member["name"], "#")  # Fallback to "#" if no link found
        image_html += f'''
        <div style="text-align: center;">
            <a href="{link}" target="_blank">
                <img src="data:{mime_type};base64,{encoded}" alt="{member["name"]}">
            </a>
            <p>{member["name"]}</p>
        </div>
        '''
    else:
        st.warning(f"Image for {member['name']} not found: {member['image']}")
image_html += '</div>'

# Finally, render the HTML in Streamlit
st.markdown(image_html, unsafe_allow_html=True)
# 9. Contact Section
# -------------------------------
st.markdown("### Contact / More Info")
st.markdown("""
For more information, visit the host @ [https://github.com/ReyesChianrossC](https://github.com/ReyesChianrossC)
""")

# -------------------------------
# 10. Back to Top Anchor
# -------------------------------
st.markdown("---")
st.markdown("<a href='#water-quality-prediction-results'>⬆Back to Top</a>", unsafe_allow_html=True)

