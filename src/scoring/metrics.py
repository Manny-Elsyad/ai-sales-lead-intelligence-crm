import pandas as pd


PROBABILITY_BY_STAGE = {
    "New": 0.12,
    "Qualified": 0.35,
    "Proposal": 0.58,
    "Negotiation": 0.8,
}


def apply_pipeline_probability(df: pd.DataFrame) -> pd.DataFrame:
    """Attach win probability and weighted pipeline values per lead."""
    data = df.copy()
    data["win_probability"] = data["stage"].map(PROBABILITY_BY_STAGE).fillna(0.1)
    data["weighted_value"] = (data["deal_value"] * data["win_probability"]).round(0)
    return data


def summarize_kpis(df: pd.DataFrame) -> dict[str, float]:
    """Compute headline KPIs for the executive dashboard."""
    total_leads = int(df["lead_id"].nunique())
    total_pipeline = float(df["deal_value"].sum())
    weighted_pipeline = float(df["weighted_value"].sum())
    avg_lead_score = float(df["lead_score"].mean())
    return {
        "total_leads": total_leads,
        "total_pipeline": total_pipeline,
        "weighted_pipeline": weighted_pipeline,
        "avg_lead_score": avg_lead_score,
    }
