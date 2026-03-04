
import streamlit as st
import pandas as pd
from scanner.runner import run_scan
from models.indicator_registry import INDICATORS

st.title("LOSI Municipal Portal Scanner")

with open("config/default_urls.txt") as f:
    default_urls = f.read()

urls_text = st.text_area(
    "Municipal portal URLs (one per line)",
    value=default_urls,
    height=200
)

st.subheader("Select LOSI Indicators")

selected = []
for code, meta in INDICATORS.items():
    if st.checkbox(f"{code} – {meta['name']}", value=meta.get("default", True)):
        selected.append(code)

if st.button("Run analysis"):
    urls = [u.strip() for u in urls_text.split("\n") if u.strip()]
    progress = st.progress(0)

    feature_df, evidence_df = run_scan(urls, selected, progress)

    st.subheader("Feature Matrix")
    display_df = feature_df.replace({1: "✓", 0: "✗"})
    st.dataframe(display_df)

    csv = feature_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download feature matrix CSV",
        csv,
        "losi_feature_matrix.csv",
        "text/csv"
    )

    st.subheader("Evidence Dataset")
    st.dataframe(evidence_df)

    csv2 = evidence_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download evidence CSV",
        csv2,
        "losi_evidence.csv",
        "text/csv"
    )
