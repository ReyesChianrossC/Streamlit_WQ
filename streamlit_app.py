# Streamlit Dashboard
st.set_page_config(page_title="Water Quality Analysis Dashboard", layout="wide")
st.title("Water Quality Analysis Dashboard")
st.markdown("""
This dashboard displays the results of a water quality analysis, including model performance metrics, data summaries, site-specific statistics, and model comparisons.
The metrics compare different models for predicting water quality parameters over various time horizons (Next Week, Next Month, Next Year).
""")

# Model Performance Metrics
st.header("Model Performance Metrics")
try:
    # Format numerical columns to 3 decimal places
    formatted_results = combined_results.copy()
    for col in combined_results.columns:
        if col != 'Model':
            formatted_results[col] = formatted_results[col].apply(lambda x: f"{x:.3f}" if isinstance(x, (int, float)) else x)
    st.dataframe(formatted_results, use_container_width=True)
except Exception as e:
    st.error(f"Error loading model performance metrics: {str(e)}")

# Data Summaries
st.header("Data Summaries")
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Unique Weather Conditions")
    try:
        st.table(weather_conditions)
    except:
        st.error("Error loading weather conditions.")

with col2:
    st.subheader("Unique Wind Directions")
    try:
        st.table(wind_directions)
    except:
        st.error("Error loading wind directions.")

with col3:
    st.subheader("Unique Sites")
    try:
        st.table(sites)
    except:
        st.error("Error loading sites.")

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
        image = Image.open(os.path.join(local_output_dir, metric))
        st.image(image, caption=caption, use_column_width=True)
    except:
        st.error(f"Error loading {metric}.")

# Site-Specific Predictions
st.header("Site-Specific Predictions")
try:
    # Load site predictions and sites data
    site_predictions = pd.read_parquet(os.path.join(local_output_dir, 'site_predictions.parquet'))
    sites = pd.read_parquet(os.path.join(local_output_dir, 'sites.parquet'))

    # Dropdown for site selection
    site_list = sorted(sites['site'].dropna().unique().tolist())
    selected_site = st.selectbox("Select a Site", options=site_list, key="site_select")

    # Dropdown for model selection (including all specified models)
    model_list = [
        'CNN - Water Only', 'LSTM - Water Only', 'CNN-LSTM - Water Only',
        'CNN - Water + External', 'LSTM - Water + External', 'CNN-LSTM - Water + External'
    ]
    selected_model = st.selectbox("Select a Model", options=model_list, key="model_select")

    # Dropdown for horizon selection
    horizon_list = ["Next Week", "Next Month", "Next Year"]
    selected_horizon = st.selectbox("Select Prediction Horizon", options=horizon_list, key="horizon_select_predictions")

    st.markdown(f"**Selected: {selected_site} - {selected_model} - {selected_horizon}**")

    # Filter predictions for selected site, model, and horizon
    site_data = site_predictions[
        (site_predictions['site'] == selected_site) &
        (site_predictions['model'] == selected_model) &
        (site_predictions['horizon'] == selected_horizon)
    ]

    if not site_data.empty:
        st.subheader(f"Predicted Water Quality for {selected_site} ({selected_model}, {selected_horizon})")
        pred_cols = [col for col in site_data.columns if col.startswith('pred_')]

        # Compute summary statistics
        summary_data = site_data[pred_cols].agg(['mean', 'min', 'max', 'std']).transpose().reset_index()
        summary_data['Metric'] = summary_data['index'].str.replace('pred_', '')
        summary_data = summary_data[['Metric', 'mean', 'min', 'max', 'std']]

        # Format numerical values to 3 decimal places
        for col in ['mean', 'min', 'max', 'std']:
            summary_data[col] = summary_data[col].apply(lambda x: f"{x:.3f}" if pd.notnull(x) else "N/A")

        # Display the summary table
        st.dataframe(summary_data, use_container_width=True, height=600)

        # Display number of predictions
        st.write(f"Number of predictions: {len(site_data)}")

        # Warning for single prediction
        if len(site_data) == 1:
            st.warning("Only one prediction available. Standard deviation is undefined for a single data point.")
    else:
        st.warning(f"No prediction data available for {selected_site}, {selected_model}, {selected_horizon}.")
except Exception as e:
    st.error(f"Error processing site-specific predictions: {str(e)}")

# Footer
st.markdown("""
---
**Note**: To run this app, ensure all required files are present and execute `streamlit run water_quality_analysis.py`.
""")

# Download Files
files_to_download = [
    'combined_results.parquet', 'weather_conditions.parquet', 'wind_directions.parquet',
    'sites.parquet', 'site_summary.parquet', 'site_predictions.parquet',
    'mae_comparison.png', 'mse_comparison.png', 'rmse_comparison.png', 'r2_comparison.png'
]
for file_name in files_to_download:
    file_path = os.path.join(local_output_dir, file_name)
    if os.path.exists(file_path):
        files.download(file_path)
    else:
        print(f"Warning: {file_name} not found.")

# Clean up Spark session
spark.stop()
