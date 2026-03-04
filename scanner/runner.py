
import requests
import pandas as pd
from bs4 import BeautifulSoup
from models.indicator_registry import INDICATORS

def run_scan(urls, selected, progress):

    feature_rows = []
    evidence_rows = []

    total = len(urls)

    for i, url in enumerate(urls):

        try:
            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.text, "lxml")
        except:
            soup = None

        row = {"municipality": url}

        for code in selected:

            module = INDICATORS[code]["module"]
            func = module.run

            result, evidence = func(soup, url)

            row[code] = result

            if evidence:
                evidence_rows.append({
                    "municipality": url,
                    "indicator": code,
                    "evidence": evidence
                })

        feature_rows.append(row)

        progress.progress((i+1)/total)

    feature_df = pd.DataFrame(feature_rows)
    evidence_df = pd.DataFrame(evidence_rows)

    return feature_df, evidence_df
