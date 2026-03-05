import streamlit as st
import pandas as pd
import json
import datetime
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

select_all = st.toggle("Select / Deselect all indicators", value=True)

selected = []
keyword_inputs = {}

for code, meta in INDICATORS.items():

    if st.checkbox(
    f"{code} – {meta['name']}",
    value=select_all,
    help=meta.get("description")
    ):

        selected.append(code)

        if "config" in meta and meta["config"]["type"] == "keyword":

            defaults = meta["config"]["keywords_default"]

            txt = st.text_area(
                f"Keywords for indicator {code}",
                value="\n".join(defaults),
                height=120
            )

            keyword_inputs[code] = [
                k.strip() for k in txt.split("\n") if k.strip()
            ]

if st.button("Run analysis"):
    urls = [u.strip() for u in urls_text.split("\n") if u.strip()]
    progress = st.progress(0)

    config = {
    "timestamp": datetime.datetime.utcnow().isoformat(),
    "urls": urls,
    "indicators": selected,
    "keywords": keyword_inputs
    }

    feature_df, evidence_df = run_scan(
    urls,
    selected,
    progress,
    keyword_inputs
    )

    st.subheader("Feature Matrix")
    display_df = feature_df.replace({1: "✓", 0: "✗"})
    
    st.dataframe(display_df)

    redirects = feature_df[feature_df["redirected"] == True]

    for _, r in redirects.iterrows():
        st.warning(
            f"⚠ Redirect detected: {r['municipality']} → {r['final_url']}"
        )

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

    config_json = json.dumps(config, indent=2, ensure_ascii=False)
    st.download_button(
    "Download configuration (JSON)",
    config_json,
    "losi_configuration.json",
    "application/json"
    )
    
st.markdown(
    """
    ---
    <small>
    This application is a work in progress developed within the Postgraduate Programme <b>"e-Government"</b> of the University of the Aegean. It aims to audit municipal websites using the Local Online Service Index (LOSI) indicators.<br><br>
    The analysis is fully rule-based and methodologically transparent. The source code is openly available at <a href="https://github.com/rinenweb/LOSI-scanner">GitHub</a>.
    </small>
    """,
    unsafe_allow_html=True
    )
