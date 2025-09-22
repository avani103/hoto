import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- Custom CSS for top-right corner text ---
st.markdown(
    """
    <style>
    .top-right {
        position: absolute;
        top: 10px;
        right: 20px;
        font-size: 14px;
        font-weight: bold;
        color: #4CAF50;
    }
    </style>
    <div class="top-right">Developed by Triava</div>
    """,
    unsafe_allow_html=True
)

FILE_PATH = "pyth.xlsx"

# Load Excel template
if os.path.exists(FILE_PATH):
    df = pd.read_excel(FILE_PATH)
else:
    st.error("Template file 'pyth.xlsx' not found!")
    st.stop()

# First column is fixed parameters
parameters = df.iloc[:, 0]

# Sidebar: Choose shift
shift = st.sidebar.selectbox("Select Shift", ["DS", "NS"])

# Create new column name
today = datetime.now().strftime("%Y-%m-%d")
new_col_name = f"{shift}_{today}"

# If column doesn’t exist, add it
if new_col_name not in df.columns:
    df[new_col_name] = ""

# Editable DataFrame (only parameters + today’s column)
edit_df = pd.DataFrame({
    "Parameters": parameters,
    new_col_name: df[new_col_name]
})

st.write("### Enter Data for Today")
edited = st.data_editor(edit_df, use_container_width=True)

# Save changes
if st.button("Save Data"):
    # Update only today’s column in original df
    df[new_col_name] = edited[new_col_name].values
    df.to_excel(FILE_PATH, index=False)
    st.success(f"✅ Data saved successfully for {new_col_name}!")

# Show the full dataset
st.write("### Full Data (All Days)")
st.dataframe(df, use_container_width=True)
