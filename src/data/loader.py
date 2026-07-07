from pathlib import Path
from typing import Union

import pandas as pd


DEFAULT_DATA_PATH = Path("data/leads.csv")


def load_leads(path: Union[str, Path] = DEFAULT_DATA_PATH) -> pd.DataFrame:
    """Load fictional B2B lead data for dashboard analytics."""
    csv_path = Path(path)
    df = pd.read_csv(csv_path, parse_dates=["last_contact_date"])
    df["lead_score"] = (0.6 * df["fit_score"] + 0.4 * df["engagement_score"]).round(1)
    return df
