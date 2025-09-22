import streamlit as st
import pandas as pd
from datetime import datetime

# Upload Excel template
uploaded_file = st.file_uploader("Upload template Excel file", type=["xlsx"])
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
else:
    st.warning("⚠️ Please upload an Excel file to continue.")
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
    # Save updated Excel back to user
    df.to_excel("updated_file.xlsx", index=False)
    st.success(f" Data saved successfully for {new_col_name}! (download updated_file.xlsx)")

# Show the full dataset
st.write("### Full Data (All Days)")
st.dataframe(df, use_container_width=True)
