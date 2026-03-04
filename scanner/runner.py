import pandas as pd
from bs4 import BeautifulSoup
from models.indicator_registry import INDICATORS
from scanner.html_utils import fetch_url
from concurrent.futures import ThreadPoolExecutor

def run_scan(urls, selected, progress):

    feature_rows = []
    evidence_rows = []

    total = len(urls)

    with ThreadPoolExecutor(max_workers=8) as executor:

        futures = [executor.submit(scan_single, url, selected) for url in urls]

        for i, f in enumerate(futures):

            row, ev = f.result()

            feature_rows.append(row)

            evidence_rows.extend(ev)

            progress.progress((i + 1) / total)

    feature_df = pd.DataFrame(feature_rows)

    evidence_df = pd.DataFrame(evidence_rows)

    return feature_df, evidence_df
    
def scan_single(url, selected):

    result = fetch_url(url)

    row = {
        "municipality": url,
        "status": result["status"],
        "redirected": result["redirected"],
        "final_url": result["final_url"]
    }

    evidence_rows = []

    if result["status"] != 200 or result["response"] is None:
        return row, evidence_rows

    soup = BeautifulSoup(result["response"].text, "lxml")

    for code in selected:

        module = INDICATORS[code]["module"]

        res, evidence = module.run(soup, url)

        row[code] = res

        if evidence:
            evidence_rows.append({
                "municipality": url,
                "indicator": code,
                "evidence": evidence
            })

    return row, evidence_rows
