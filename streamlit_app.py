import streamlit as st
import pandas as pd
import os
from PIL import Image
import google.colab.files as files

# Cache data loading for performance
@st.cache_data
def load_parquet(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found")
    return pd.read_parquet(file_path)

# Initialize Streamlit page
st.set_page_config(page_title="Water Quality Analysis Dashboard", layout="wide")
st.title("Water Quality Analysis Dashboard")
st.markdown("""
This dashboard displays the results of a water quality analysis, including model performance metrics, data summaries, site-specific predictions, and model comparisons.
The metrics compare different models for predicting water quality parameters over various time horizons (Next Week, Next Month, Next Year).
""")

# Define local output directory and water columns
local_output_dir = '/content'
water_cols = [
    'surface_temperature', 'middle_temperature', 'bottom_temperature',
    'ph', 'ammonia', 'nitrate', 'phosphate',
    'dissolved_oxygen', 'sulfide', 'carbon_dioxide'
]

# Model Performance Metrics
st.header("Model Performance Metrics")
try:
    with st.spinner("Loading model performance metrics..."):
        combined_results = load_parquet(os.path.join(local_output_dir, 'combined_results.parquet'))
    if combined_results.empty:
        st.warning("No model performance metrics available.")
    else:
        # Format numerical columns
        formatted_results = combined_results.round(3).astype(str)
        formatted_results['Model'] = combined_results['Model']  # Preserve Model column as string
        st.dataframe(formatted_results, use_container_width=True)
except Exception as e:
    st.error(f"Failed to load model performance metrics: {str(e)}")

# Data Summaries
st.header("Data Summaries")
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Unique Weather Conditions")
    try:
        with st.spinner("Loading weather conditions..."):
            weather_conditions = load_parquet(os.path.join(local_output_dir, 'weather_conditions.parquet'))
        if weather_conditions.empty:
            st.warning("No weather conditions data available.")
        else:
            st.table(weather_conditions)
    except Exception as e:
        st.error(f"Failed to load weather conditions: {str(e)}")

with col2:
    st.subheader("Unique Wind Directions")
    try:
        with st.spinner("Loading wind directions..."):
            wind_directions = load_parquet(os.path.join(local_output_dir, 'wind_directions.parquet'))
        if wind_directions.empty:
            st.warning("No wind directions data available.")
        else:
            st.table(wind_directions)
    except Exception as e:
        st.error(f"Failed to load wind directions: {str(e)}")

with col3:
    st.subheader("Unique Sites")
    try:
        with st.spinner("Loading sites..."):
            sites = load_parquet(os.path.join(local_output_dir, 'sites.parquet'))
        if sites.empty:
            st.warning("No sites data available.")
        else:
            st.table(sites)
    except Exception as e:
        st.error(f"Failed to load sites: {str(e)}")

# Model Performance Visualizations
st.header("Model Performance Visualizations")
for metric, caption in [
    ('mae_comparison.png', 'MAE Comparison'),
    ('mse_comparison.png', 'MSE Comparison'),
    ('rmse_comparison.png', 'RMSE Comparison'),
    ('r2_comparison.png', 'R2 Score Comparison')
]:
    st.subheader(caption)
    try:
        file_path = os.path.join(local_output_dir, metric)
        if not os.path.exists(file_path):
            st.warning(f"Visualization {metric} not found.")
        else:
            with st.spinner(f"Loading {caption}..."):
                image = Image.open(file_path)
            st.image(image, caption=caption, use_column_width=True)
    except Exception as e:
        st.error(f"Failed to load {metric}: {str(e)}")

# Site-Specific Predictions
st.header("Site-Specific Predictions")
st.markdown("""
This section displays raw, model-specific predictions for each site, replacing previous model aggregated results. 
Select a site, prediction horizon, and model to view unaggregated predictions or compare predictions across all models.
""")
try:
    with st.spinner("Loading site predictions and sites data..."):
        site_predictions = load_parquet(os.path.join(local_output_dir, 'site_predictions.parquet'))
        sites = load_parquet(os.path.join(local_output_dir, 'sites.parquet'))

    if site_predictions.empty or sites.empty:
        st.warning("No site predictions or sites data available.")
    else:
        # Debug prediction diversity
        model_groups = site_predictions.groupby('model')
        for model_name, group in model_groups:
            pred_cols = [col for col in group.columns if col.startswith('pred_')]
            pred_std = group[pred_cols].std().mean()
            st.write(f"Prediction std for {model_name}: {pred_std:.6f}")
            if pred_std < 1e-5:
                st.warning(f"Low prediction variance for {model_name}. Model may not be learning distinct patterns.")

        # Cache site list
        @st.cache_data
        def get_site_list():
            return sorted(sites['site'].dropna().unique().tolist())

        # Dropdowns
        site_list = get_site_list()
        selected_site = st.selectbox("Select a Site", options=site_list, key="site_select")
        horizon_list = ["Next Week", "Next Month", "Next Year"]
        selected_horizon = st.selectbox("Select Prediction Horizon", options=horizon_list, key="horizon_select_predictions")

        # Model selection for detailed view
        model_list = [
            'CNN - Water Only', 'LSTM - Water Only', 'CNN-LSTM - Water Only',
            'CNN - Water + External', 'LSTM - Water + External', 'CNN-LSTM - Water + External'
        ]
        selected_model = st.selectbox("Select a Model for Detailed View", options=model_list, key="model_select")

        st.markdown(f"**Detailed View: {selected_site} - {selected_model} - {selected_horizon}**")

        # Filter predictions for selected site and horizon
        site_horizon_data = site_predictions[
            (site_predictions['site'] == selected_site) &
            (site_predictions['horizon'] == selected_horizon)
        ]

        if site_horizon_data.empty:
            st.warning(f"No predictions available for {selected_site}, {selected_horizon}.")
        else:
            # Detailed view for selected model (unaggregated predictions)
            site_data = site_horizon_data[site_horizon_data['model'] == selected_model]
            if not site_data.empty:
                st.subheader(f"Raw Predictions for {selected_site} ({selected_model}, {selected_horizon})")
                pred_cols = [col for col in site_data.columns if col.startswith('pred_')]
                display_cols = ['index', 'site', 'model', 'horizon'] + pred_cols
                display_data = site_data[display_cols].reset_index(drop=True).round(3).astype(str)
                st.dataframe(display_data, use_container_width=True, height=600)
                st.write(f"Number of predictions: {len(site_data)}")
            else:
                st.warning(f"No predictions for {selected_model} at {selected_site}, {selected_horizon}.")

            # Model comparison table (unaggregated, limited rows)
            st.subheader(f"Model Comparison for {selected_site} ({selected_horizon})")
            comparison_data = []
            for model in model_list:
                model_data = site_horizon_data[site_horizon_data['model'] == model]
                if not model_data.empty:
                    # Limit to first 5 predictions per model to avoid overwhelming display
                    model_data = model_data.head(5)
                    model_data = model_data[display_cols].reset_index(drop=True)
                    model_data['Row'] = model_data.index  # Add row identifier
                    model_data = model_data[['Row', 'index', 'model'] + pred_cols]
                    comparison_data.append(model_data)
            if comparison_data:
                comparison_df = pd.concat(comparison_data, ignore_index=True).round(3).astype(str)
                def highlight_selected_model(row):
                    return ['background-color: #d3d3d3' if row['model'] == selected_model else '' for _ in row]
                st.dataframe(comparison_df.style.apply(highlight_selected_model, axis=1), use_container_width=True)
                st.markdown("**Note**: Showing up to 5 predictions per model for brevity.")
            else:
                st.warning("No predictions available for any model.")
except Exception as e:
    st.error(f"Failed to load site-specific predictions: {str(e)}")

# Model Performance Comparison
st.header("Model Performance Comparison")
try:
    if combined_results.empty:
        st.warning("No model performance data available for comparison.")
    else:
        time_horizons = ["Next Week", "Next Month", "Next Year"]
        selected_horizon = st.selectbox("Select Time Horizon for Comparison", options=time_horizons, key="horizon_select_comparison")
        metrics = ['Final MAE', 'Final MSE', 'Final RMSE', 'R2 Score']
        horizon_columns = [f"{metric} - {selected_horizon}" for metric in metrics]
        comparison_df = combined_results[['Model'] + horizon_columns].round(3).astype(str)
        def highlight_selected_model(row):
            return ['background-color: #d3d3d3' if row['Model'] == selected_model else '' for _ in row]
        st.subheader(f"Model Comparison for {selected_horizon} Prediction")
        st.dataframe(comparison_df.style.apply(highlight_selected_model, axis=1), use_container_width=True)
        selected_model_metrics = comparison_df[comparison_df['Model'] == selected_model]
        st.markdown(f"**Selected Model ({selected_model}) Metrics for {selected_horizon}:**")
        for metric, value in selected_model_metrics[horizon_columns].iloc[0].items():
            st.markdown(f"- {metric}: {value}")
except Exception as e:
    st.error(f"Failed to display model comparison: {str(e)}")

# Dynamic File Download
st.header("Download Results")
try:
    available_files = [f for f in os.listdir(local_output_dir) if f.endswith(('.parquet', '.png'))]
    if not available_files:
        st.warning("No files available for download.")
    else:
        for file_name in available_files:
            file_path = os.path.join(local_output_dir, file_name)
            with open(file_path, 'rb') as f:
                st.download_button(
                    label=f"Download {file_name}",
                    data=f,
                    file_name=file_name,
                    mime='application/octet-stream' if file_name.endswith('.parquet') else 'image/png'
                )
except Exception as e:
    st.error(f"Failed to list downloadable files: {str(e)}")

# Footer
st.markdown("""
---
**Note**: To run this app, ensure all required files are present and execute `streamlit run water_quality_dashboard.py`.
""")
