for col in horizon_columns:
comparison_df[col] = comparison_df[col].apply(lambda x: f"{x:.3f}" if isinstance(x, (int, float)) else x)

    # Highlight the selected model's row
    # Highlight the selected model's row with a more visible color
def highlight_selected_model(row):
        return ['background-color: #d3d3d3' if row['Model'] == selected_model else '' for _ in row]
        return ['background-color: #a9a9a9' if row['Model'] == selected_model else '' for _ in row]

st.subheader(f"Model Comparison for {selected_horizon} Prediction")
st.dataframe(comparison_df.style.apply(highlight_selected_model, axis=1), use_container_width=True)
