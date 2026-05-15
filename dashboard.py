import streamlit as st
import pandas as pd
from PIL import Image
import os

st.set_page_config(page_title="Cell Count Dashboard", layout="wide")
st.title("Cell Count Analysis Dashboard")

# ── Part 2: Summary Table ────────────────────────────────────────────
st.header("Part 2: Cell Count Summary")
if os.path.exists("cell_count_summary.csv"):
    sumdf = pd.read_csv("cell_count_summary.csv")
    st.dataframe(sumdf, use_container_width=True)
else:
    st.warning("cell_count_summary.csv not found. Run `make pipeline` first.")

# ── Part 3: Statistical Results ──────────────────────────────────────
st.header("Part 3: Statistical Analysis")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Mann-Whitney U Test Results")
    if os.path.exists("mann_whit_results.csv"):
        st.dataframe(pd.read_csv("mann_whit_results.csv"), use_container_width=True)
    else:
        st.warning("mann_whit_results.csv not found.")

with col2:
    st.subheader("T-Test Results")
    if os.path.exists("t_test_results.csv"):
        st.dataframe(pd.read_csv("t_test_results.csv"), use_container_width=True)
    else:
        st.warning("t_test_results.csv not found.")

st.subheader("Cell Type Percentages by Response")
if os.path.exists("Cell_Type_by_Response.png"):
    st.image("Cell_Type_by_Response.png", use_container_width=True)
else:
    st.warning("Cell_Type_by_Response.png not found.")

# ── Part 4: Subset Analysis ──────────────────────────────────────────
st.header("Part 4: Data Subset Analysis")

col3, col4, col5 = st.columns(3)

with col3:
    st.subheader("Samples by Project")
    if os.path.exists("Project_counts.csv"):
        st.dataframe(pd.read_csv("Project_counts.csv"), use_container_width=True)
    else:
        st.warning("Project_counts.csv not found.")

with col4:
    st.subheader("Responders vs Non-Responders")
    if os.path.exists("Response_counts.csv"):
        st.dataframe(pd.read_csv("Response_counts.csv"), use_container_width=True)
    else:
        st.warning("Response_counts.csv not found.")

with col5:
    st.subheader("Sex Distribution")
    if os.path.exists("Sex_counts.csv"):
        st.dataframe(pd.read_csv("Sex_counts.csv"), use_container_width=True)
    else:
        st.warning("Sex_counts.csv not found.")
