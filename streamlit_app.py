import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import os

# Set page configuration
st.set_page_config(page_title="Water Quality Analysis Dashboard", layout="wide")

# Define file paths (relative to the script in the GitHub repository)
output_dir = "."  # Files are in the same directory as the script
# Define file paths (relative to the script)
output_dir = "/content"  # Adjust as needed for your environment
parquet_files = {
'Combined Results': 'combined_results.parquet',
'Weather Conditions': 'weather_conditions.parquet',
@@ -37,7 +38,7 @@
combined_results = pd.read_parquet(os.path.join(output_dir, parquet_files['Combined Results']))
st.dataframe(combined_results, use_container_width=True)
except FileNotFoundError:
    st.error(f"Error: '{parquet_files['Combined Results']}' not found in {output_dir}. Ensure the file is included in the GitHub repository.")
    st.error(f"Error: '{parquet_files['Combined Results']}' not found in {output_dir}.")
except Exception as e:
st.error(f"Error loading combined results: {str(e)}")

@@ -83,7 +84,7 @@
image = Image.open(os.path.join(output_dir, plot_file))
st.image(image, caption=f"{metric} Comparison Across Models", use_column_width=True)
except FileNotFoundError:
        st.error(f"Error: '{plot_file}' not found in {output_dir}. Ensure the plot is included in the GitHub repository.")
        st.error(f"Error: '{plot_file}' not found in {output_dir}.")
except Exception as e:
st.error(f"Error loading {metric} plot: {str(e)}")

@@ -120,7 +121,7 @@
except Exception as e:
st.error(f"Error displaying site summary: {str(e)}")

# Model performance comparison section
# Model performance comparison section with bar chart
st.header("Model Performance Comparison")
try:
# Dropdown for time horizon selection
@@ -133,29 +134,40 @@

# Prepare comparison DataFrame
comparison_df = combined_results[['Model'] + horizon_columns].copy()
    # Format numerical values to 3 decimal places
    # Convert to numeric for plotting
for col in horizon_columns:
        comparison_df[col] = comparison_df[col].apply(lambda x: f"{x:.3f}" if isinstance(x, (int, float)) else x)
        comparison_df[col] = pd.to_numeric(comparison_df[col], errors='coerce')

    # Highlight the selected model's row with a more visible color
    # Highlight the selected model's row in the table
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
        st.markdown(f"- {metric}: {value}")
        st.markdown(f"- {metric}: {value:.3f}")
except Exception as e:
st.error(f"Error displaying model comparison: {str(e)}")

# Footer
st.markdown("""
---
**Note**: Ensure all required files (Parquet and PNGs) are included in the GitHub repository in the same directory as this script.
To deploy this app on Streamlit Cloud, link your GitHub repository and specify this script as the entry point.
To run locally, install dependencies (`pip install streamlit pandas pillow pyarrow`) and execute `streamlit run streamlit_app.py`.
**Note**: Ensure all required files (Parquet and PNGs) are included in the `/content` directory.
To run locally, install dependencies (`pip install streamlit pandas pillow pyarrow plotly`) and execute `streamlit run water_quality_analysis.py`.
""")
