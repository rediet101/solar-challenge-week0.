import os
import pandas as pd
from typing import Dict, List

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
FILES: Dict[str, str] = {
    "Benin": "benin_clean.csv",
    "Sierra Leone": "sierra_leone_clean.csv",
    "Togo": "togo_clean.csv",
}
METRICS: List[str] = ["GHI", "DNI", "DHI"]


def load_country_frames(selected: List[str]) -> pd.DataFrame:
    frames = []
    for country in selected:
        fname = FILES.get(country)
        if not fname:
            continue
        fpath = os.path.join(DATA_DIR, fname)
        if not os.path.exists(fpath):
            continue
        df = pd.read_csv(fpath)
        df["Country"] = country
        frames.append(df)
    if not frames:
        return pd.DataFrame()
    df_all = pd.concat(frames, ignore_index=True)
    # keep common useful columns if present
    keep_cols = [c for c in df_all.columns if c in METRICS + ["Country", "region", "Region", "admin_name", "site", "location"]]
    return df_all[keep_cols]


def guess_region_column(df: pd.DataFrame) -> str:
    for c in ["region", "Region", "admin_name", "site", "location"]:
        if c in df.columns:
            return c
    return ""
