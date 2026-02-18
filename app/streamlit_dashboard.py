import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pandas as pd
import streamlit as st

from experiments.ab_test_engine import analyze_ab

st.set_page_config(page_title="Buyer Retention Lab", layout="wide")

st.title("🛍️ Buyer Retention & Experimentation Analytics Lab")

st.sidebar.header("Upload experiment data")
file = st.sidebar.file_uploader("CSV with columns: variant, metric(s)", type=["csv"])

if file is None:
    st.info("Upload a CSV to begin. Example columns: variant, order_value, retained_d30")
    st.stop()

df = pd.read_csv(file)
st.subheader("Preview")
st.dataframe(df.head(20), use_container_width=True)

st.sidebar.header("A/B settings")
group_col = st.sidebar.selectbox("Group column", options=df.columns, index=list(df.columns).index("variant") if "variant" in df.columns else 0)
control = st.sidebar.text_input("Control value", value="control")
treatment = st.sidebar.text_input("Treatment value", value="treatment")

metric_col = st.sidebar.selectbox("Metric", options=[c for c in df.columns if c != group_col])
metric_type = st.sidebar.selectbox("Metric type", options=["continuous", "binary"])

if st.sidebar.button("Run analysis"):
    res = analyze_ab(
        df=df,
        metric_col=metric_col,
        group_col=group_col,
        control_value=control,
        treatment_value=treatment,
        metric_type=metric_type,
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Control mean", f"{res.control_mean:.4f}")
    c2.metric("Treatment mean", f"{res.treatment_mean:.4f}")
    c3.metric("Abs lift", f"{res.abs_lift:.4f}")

    st.write("### Stats")
    st.write(
        {
            "p_value": res.p_value,
            "ci_95": res.ci_95,
            "rel_lift": res.rel_lift,
            "decision": res.decision,
            "n_control": res.n_control,
            "n_treatment": res.n_treatment,
            "notes": res.notes,
        }
    )
