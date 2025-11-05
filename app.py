import streamlit as st
import pandas as pd
from datetime import datetime
TEMPLATE_PATH = "pyth.xlsx"
@st.cache_data
def load_template():
    return pd.read_excel(TEMPLATE_PATH)
df = load_template()
parameters = df.iloc[:, 0]
shift = st.sidebar.selectbox("Select Shift", ["DS", "NS"])
today = datetime.now().strftime("%Y-%m-%d")
new_col_name = f"{shift}_{today}"
if new_col_name not in df.columns:
    df[new_col_name] = ""
edit_df = pd.DataFrame({
    "Parameters": parameters,
    new_col_name: df[new_col_name]
})

st.write("###  Enter Data for Today")
edited = st.data_editor(edit_df, use_container_width=True)
if st.button("Save Data"):
    df[new_col_name] = edited[new_col_name].values
    save_path = "updated_file.xlsx"
    df.to_excel(save_path, index=False)

    st.success(f" Data saved for {new_col_name}")
    with open(save_path, "rb") as f:
        st.download_button(
            label=" Download Updated Excel File",
            data=f,
            file_name="updated_file.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
st.write("###  Full Data (All Days)")
st.dataframe(df, use_container_width=True)
