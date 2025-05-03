st.markdown("## 📋 Table of Contents")
st.markdown("""
1. [Model Performance Metrics](#model-performance-metrics)  
2. [Data Summaries](#data-summaries)  
3. [Model Performance Visualizations](#model-performance-visualizations)  
4. [Site Specific Summary](#site-specific-summary)  
5. [Download All Graphs](#download-all-graphs)  
6. [Group 1 Members](#group-1-members)  
7. [Contact / More Info](#contact--more-info)
2. [Compare Models](#compare-models)  
3. [Data Summaries](#data-summaries)  
4. [Model Performance Visualizations](#model-performance-visualizations)  
5. [Site Specific Summary](#site-specific-summary)  
6. [Download All Graphs](#download-all-graphs)  
7. [Group 1 Members](#group-1-members)  
8. [Contact / More Info](#contact--more-info)
""", unsafe_allow_html=True)

# -------------------------------
@@ -26,9 +27,9 @@
df = pd.read_parquet("combined_results.parquet")

forecast_options = {
        "Next Week": ["Final MAE - Next Week", "Final MSE - Next Week"],
        "Next Month": ["Final MAE - Next Month", "Final MSE - Next Month"],
        "Next Year": ["Final MAE - Next Year", "Final MSE - Next Year"]
        "Next Week": ["Final MAE - Next Week", "Final MSE - Next Week", "Final RMSE - Next Week", "Final R² - Next Week"],
        "Next Month": ["Final MAE - Next Month", "Final MSE - Next Month", "Final RMSE - Next Month", "Final R² - Next Month"],
        "Next Year": ["Final MAE - Next Year", "Final MSE - Next Year", "Final RMSE - Next Year", "Final R² - Next Year"]
}

selected_forecast = st.selectbox("Select Forecast Range", list(forecast_options.keys()))
@@ -42,7 +43,28 @@
st.error("combined_results.parquet not found.")

# -------------------------------
# 2. Data Summaries
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

@@ -65,7 +87,7 @@
st.error("sites.parquet not found.")

# -------------------------------
# 3. Model Performance Visualizations
# 4. Model Performance Visualizations
# -------------------------------
st.markdown("### Model Performance Visualizations")
plot_files = [
@@ -81,7 +103,7 @@
st.error(f"{plot_file} not found.")

# -------------------------------
# 4. Site Specific Summary
# 5. Site Specific Summary
# -------------------------------
st.markdown("### Site Specific Summary")
if os.path.exists("site_summary.parquet"):
@@ -95,7 +117,7 @@
st.error("site_summary.parquet not found.")

# -------------------------------
# 5. Download All Graphs
# 6. Download All Graphs
# -------------------------------
st.markdown("### Download All Graphs")

@@ -117,7 +139,7 @@
)

# -------------------------------
# 6. Group 1 Members
# 7. Group 1 Members
# -------------------------------
st.markdown("### Group 1 Members")
st.markdown("""
@@ -129,15 +151,15 @@
""")

# -------------------------------
# 7. Contact Section
# 8. Contact Section
# -------------------------------
st.markdown("### Contact / More Info")
st.markdown("""
For more information, visit the [https://github.com/ReyesChianrossC](https://github.com/ReyesChianrossC)
""")

# -------------------------------
# 8. Back to Top Anchor
# 9. Back to Top Anchor
# -------------------------------
st.markdown("---")
st.markdown("<a href='#water-quality-prediction-results'>⬆Back to Top</a>", unsafe_allow_html=True)
