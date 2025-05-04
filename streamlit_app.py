import streamlit as st
import pandas as pd
import base64
import os
import uuid
import zipfile

# Set page config as the first Streamlit command
st.set_page_config(layout="wide")

# Custom CSS for the banner and content
st.markdown("""
    <style>
    .banner-container {
        width: 100%;
        height: 50%;  /* Reduced height to make the banner smaller */
    }
    .banner-image {
        width: 100%;
        height: 150px;
        object-fit: cover;  /* Ensure image covers the area */
        object-position: center;  /* Crop top and bottom, focus on the center */
        opacity: 0.7;  /* Slightly more visible */
    }
    .content {
        padding-top: 20px;  /* Small padding to separate content from banner */
    }
    #title-section {
        margin: 0;
        padding: 20px;
        background: transparent;  /* Remove the white background */
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Load and display the banner image
banner_image_path = "banner.jpg"
st.markdown('<div class="banner-container">', unsafe_allow_html=True)
if os.path.exists(banner_image_path):
    try:
        with open(banner_image_path, "rb") as image_file:
            encoded_banner = base64.b64encode(image_file.read()).decode()
        st.markdown(
            f'<img class="banner-image" src="data:image/jpeg;base64,{encoded_banner}" alt="Banner">',
            unsafe_allow_html=True
        )
    except Exception as e:
        st.error(f"Failed to load banner image: {e}")
else:
    st.warning("Banner image 'banner.jpg' not found.")
st.markdown('</div>', unsafe_allow_html=True)

# Wrap content in a div
st.markdown('<div class="content">', unsafe_allow_html=True)

# Wrap the title section in a div with an ID for JavaScript targeting
st.markdown('<div id="title-section">', unsafe_allow_html=True)

st.title("Taal Water Quality Prediction Dashboard")
st.markdown("## Table of Contents")
st.markdown("""
1. [Unique Data Summaries](#unique-data-summaries)  
2. [Exploratory Data Analysis](#exploratory-data-analysis)  
3. [Model Performance Metrics](#model-performance-metrics)  
4. [Compare Models](#compare-models)  
5. [Model Performance Visualizations](#model-performance-visualizations)  
6. [Site Specific Summary](#site-specific-summary)  
7. [Raw Data Exploration](#raw-data-exploration)  
8. [Download All Graphs](#download-all-graphs)  
9. [Group 1 Members](#group-1-members)  
""", unsafe_allow_html=True)

# -------------------------------
# 1. Unique Data Summaries
# -------------------------------
st.markdown('<div id="unique-data-summaries">', unsafe_allow_html=True)
st.markdown("### Unique Data Summaries")

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
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# 2. Exploratory Data Analysis
# -------------------------------
st.markdown('<div id="exploratory-data-analysis">', unsafe_allow_html=True)
st.markdown("### Exploratory Data Analysis")

# Custom CSS for horizontal image belt
st.markdown("""
    <style>
    .image-belt {
        display: flex;
        justify-content: space-between;
        gap: 20px;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .image-belt img {
        width: 33%;
        height: auto;
        object-fit: cover;
        border-radius: 10px;
        border: 2px solid #ddd;
    }
    </style>
""", unsafe_allow_html=True)

# List of EDA images
eda_images = ["EDA1.png", "EDA2.png", "EDA3.png"]
cols = st.columns(3)

for idx, image_file in enumerate(eda_images):
    with cols[idx]:
        if os.path.exists(image_file):
            st.image(image_file, caption=image_file.replace(".png", ""), use_column_width=True)
        else:
            st.error(f"{image_file} not found.")
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# 3. Model Performance Metrics
# -------------------------------
st.markdown('<div id="model-performance-metrics">', unsafe_allow_html=True)
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
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# 4. Compare Models
# -------------------------------
st.markdown('<div id="compare-models">', unsafe_allow_html=True)
st.markdown("### Compare Models")

if os.path.exists("combined_results.parquet"):
    df = pd.read_parquet("combined_results.parquet")

    models = df["Model"].unique()
    selected_models = st.multiselect(
        "Select Models to Compare",
        models,
        default=[models[0], models[1]] if len(models) > 1 else []
    )

    metrics_map = {
        "Next Week": ["Final MAE - Next Week", "Final MSE - Next Week", "Final RMSE - Next Week", "R2 Score - Next Week"],
        "Next Month": ["Final MAE - Next Month", "Final MSE - Next Month", "Final RMSE - Next Month", "R2 Score - Next Month"],
        "Next Year": ["Final MAE - Next Year", "Final MSE - Next Year", "Final RMSE - Next Year", "R2 Score - Next Year"]
    }

    selected_forecast = st.selectbox("Select Forecast Range for Comparison", list(metrics_map.keys()))
    metric_columns = metrics_map[selected_forecast]
    valid_columns = ["Model"] + [col for col in metric_columns if col in df.columns]

    if len(valid_columns) < 2:
        missing_cols = [col for col in metric_columns if col not in df.columns]
        st.error(f"Not enough valid columns found. Missing columns: {', '.join(missing_cols)}")
    else:
        comparison_df = df[df["Model"].isin(selected_models)][valid_columns].reset_index(drop=True)

        # Clean column names for display
        clean_names = {
            metric_columns[0]: "Final MAE",
            metric_columns[1]: "Final MSE",
            metric_columns[2]: "Final RMSE",
            metric_columns[3]: "R2 Score"
        }
        comparison_df = comparison_df.rename(columns=clean_names)

        # Fixed gradient styling function for the entire dataframe
        def style_dataframe(df):
            gradient_map = {
                "Final MAE": (210, 80, 50, True),
                "Final MSE": (210, 80, 50, True),
                "Final RMSE": (210, 80, 50, True),
                "R2 Score": (210, 80, 50, False)
            }

            styles = pd.DataFrame("", index=df.index, columns=df.columns)

            for col in df.columns:
                if col == "Model":
                    styles[col] = "color: white"
                elif col in gradient_map:
                    hue, light_start, light_end, reverse = gradient_map[col]
                    valid_vals = df[col].dropna()
                    if len(valid_vals) < 2:
                        continue
                    # Rank values appropriately
                    ranks = valid_vals.rank(method='min', ascending=reverse)
                    norm_ranks = (ranks - 1) / (len(valid_vals) - 1)
                    lightness_vals = light_start - norm_ranks * (light_start - light_end)

                    for i in valid_vals.index:
                        lightness = lightness_vals[i]
                        styles.at[i, col] = f"background-color: hsl({hue}, 50%, {lightness:.1f}%); color: black"

            return styles

        # Display the combined table with styling
        styled_df = comparison_df.style.apply(style_dataframe, axis=None)
        st.dataframe(styled_df)

else:
    st.error("combined_results.parquet not found.")
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# 5. Model Performance Visualizations
# -------------------------------
st.markdown('<div id="model-performance-visualizations">', unsafe_allow_html=True)
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
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# 6. Site Specific Summary# -------------------------------
st.markdown('<div id="site-specific-summary">', unsafe_allow_html=True)
st.markdown("### Site Specific Summary (Aggregated Raw Data)")
if os.path.exists("site_summary.parquet"):
    site_summary = pd.read_parquet("site_summary.parquet")
    site_list = site_summary['site'].unique()
    # Remove 'None' from site_list if it exists
    site_list = [site for site in site_list if site is not None]
    selected_site = st.selectbox("Select a site:", site_list)
    filtered = site_summary[site_summary['site'] == selected_site]

    # Add custom CSS for text alignment and to hide indexes
    st.markdown(
        """
        <style>
        table {
            text-align: left !important;
        }
        th:nth-child(1), td:nth-child(1) {
            display: none !important;  /* Hide the index column */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Define columns for horizontal belt
    col1, col2 = st.columns(2)
    
    with col1:
        # Group by °C
        data1 = {
            "Metric": ["Avg Surface Temp (°C)", "Avg Middle Temp (°C)", "Avg Bottom Temp (°C)", "Avg Air Temp (°C)"],
            "Value": [
                filtered['avg_surface_temperature'].iloc[0] if 'avg_surface_temperature' in filtered.columns else "-",
                filtered['avg_middle_temperature'].iloc[0] if 'avg_middle_temperature' in filtered.columns else "-",
                filtered['avg_bottom_temperature'].iloc[0] if 'avg_bottom_temperature' in filtered.columns else "-",
                filtered['avg_air_temperature'].iloc[0] if 'avg_air_temperature' in filtered.columns else "-"
            ]
        }
        df1 = pd.DataFrame(data1)
        st.table(df1)

        # Group by pH (placed below the °C table)
        data3 = {
            "Metric": ["Avg pH"],
            "Value": [
                filtered['avg_ph'].iloc[0] if 'avg_ph' in filtered.columns else "-"
            ]
        }
        df3 = pd.DataFrame(data3)
        st.table(df3)

    with col2:
        # Group by mg/L (merged into one table)
        data2 = {
            "Metric": ["Avg Ammonia (mg/L)", "Avg Nitrate (mg/L)", "Avg Phosphate (mg/L)", 
                       "Avg Dissolved Oxygen (mg/L)", "Avg Sulfide (mg/L)", "Avg Carbon Dioxide (mg/L)"],
            "Value": [
                filtered['avg_ammonia'].iloc[0] if 'avg_ammonia' in filtered.columns else "-",
                filtered['avg_nitrate'].iloc[0] if 'avg_nitrate' in filtered.columns else "-",
                filtered['avg_phosphate'].iloc[0] if 'avg_phosphate' in filtered.columns else "-",
                filtered['avg_dissolved_oxygen'].iloc[0] if 'avg_dissolved_oxygen' in filtered.columns else "-",
                filtered['avg_sulfide'].iloc[0] if 'avg_sulfide' in filtered.columns else "-",
                filtered['avg_carbon_dioxide'].iloc[0] if 'avg_carbon_dioxide' in filtered.columns else "-"
            ]
        }
        df2 = pd.DataFrame(data2)
        st.table(df2)

else:
    st.error("site_summary.parquet not found.")
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# 7. Raw Data Exploration
# -------------------------------
st.markdown('<div id="raw-data-exploration">', unsafe_allow_html=True)
st.markdown("### Raw Data Exploration")
st.markdown("Explore the raw data files generated from the machine learning pipelines.")

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
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# 8. Downloads
# -------------------------------
st.markdown('<div id="download-all-graphs">', unsafe_allow_html=True)
st.markdown("### Downloads")

# ZIP for all graphs, including EDA images
zip_filename = "all_graphs.zip"
all_plot_files = [
    "mae_comparison.png",
    "mse_comparison.png",
    "rmse_comparison.png",
    "r2_comparison.png",
    "EDA1.png",
    "EDA2.png",
    "EDA3.png"
]
if not os.path.exists(zip_filename):
    if st.button("Create ZIP of All Graphs"):
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for plot_file in all_plot_files:
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
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# 9. Group 1 Members
# -------------------------------
st.markdown('<div id="group-1-members">', unsafe_allow_html=True)
st.markdown("### Group 1 Members")

# Custom CSS to center the images in a horizontal belt with rounded edges and black border
st.markdown("""
    <style>
    .center-images {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .center-images img {
        width: 100px;
        height: 100px;
        object-fit: cover;
        border-radius: 10px;  /* Softens the edges */
        border: 4px solid black;  /* Adds a slight black border */
    }
    </style>
""", unsafe_allow_html=True)

# List of group members' image paths (adjust paths as needed)
group_members = [
    {"name": "Reyes", "image": "1.png"},
    {"name": "Gregorio", "image": "2.png"},
    {"name": "Agana", "image": "3.png"},
    {"name": "Casa", "image": "4.jpg"},
    {"name": "Jeremillos", "image": "5.jpg"},
]

# Create a div to hold the images and center them
image_html = '<div class="center-images">'
for member in group_members:
    if os.path.exists(member["image"]):
        with open(member["image"], "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
        # Determine MIME type based on file extension
        mime_type = "image/png" if member["image"].lower().endswith(".png") else "image/jpeg"
        image_html += f'<div style="text-align: center;"><img src="data:{mime_type};base64,{encoded}" alt="{member["name"]}"><p>{member["name"]}</p></div>'
    else:
        st.warning(f"Image for {member['name']} not found: {member['image']}")
image_html += '</div>'

# Render the centered images with names
st.markdown(image_html, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# 10. Contact Section
# -------------------------------
st.markdown("### Contact / More Info")
st.markdown("""
For more information, visit the host @ [https://github.com/ReyesChianrossC](https://github.com/ReyesChianrossC)
""")

# -------------------------------
# 11. Back to Top Anchor
# -------------------------------
st.markdown("---")
st.markdown("<a href='#title-section'>⬆Back to Top</a>", unsafe_allow_html=True)
