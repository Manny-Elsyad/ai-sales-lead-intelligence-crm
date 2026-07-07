from typing import Dict

import pandas as pd


CRM_STAGE_ORDER = ["New", "Contacted", "Qualified", "Proposal", "Won", "Lost"]


def _map_to_crm_stage(row: pd.Series) -> str:
    stage = str(row["stage"])
    score = int(row.get("lead_score", 0))
    engagement = int(row.get("engagement_score", 0))
    urgency = str(row.get("urgency_level", "Low"))

    if stage == "New":
        return "Contacted" if engagement >= 62 else "New"
    if stage == "Qualified":
        return "Qualified"
    if stage == "Proposal":
        if score >= 82 and urgency == "High":
            return "Won"
        if score <= 64:
            return "Lost"
        return "Proposal"
    if stage == "Negotiation":
        if score >= 84:
            return "Won"
        if score <= 70:
            return "Lost"
        return "Proposal"
    return "Contacted"


def add_crm_stage(df: pd.DataFrame) -> pd.DataFrame:
    """Add a CRM-focused stage column based on current pipeline signals."""
    data = df.copy()
    data["crm_stage"] = data.apply(_map_to_crm_stage, axis=1)
    return data


def group_leads_by_crm_stage(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """Return stage-ordered lead groups for CRM pipeline rendering."""
    grouped: Dict[str, pd.DataFrame] = {}
    for stage in CRM_STAGE_ORDER:
        stage_df = df[df["crm_stage"] == stage].copy()
        grouped[stage] = stage_df.sort_values(
            by=["lead_score", "deal_value"], ascending=[False, False]
        )
    return grouped


def pipeline_summary_metrics(df: pd.DataFrame) -> Dict[str, float]:
    """Compute pipeline summary metrics for CRM stage view."""
    total_pipeline_value = float(df["deal_value"].sum())
    qualified_pipeline_value = float(
        df[df["crm_stage"].isin(["Qualified", "Proposal", "Won"])]["deal_value"].sum()
    )
    won_value = float(df[df["crm_stage"] == "Won"]["deal_value"].sum())

    return {
        "total_pipeline_value": total_pipeline_value,
        "qualified_pipeline_value": qualified_pipeline_value,
        "won_value": won_value,
    }


def average_lead_score_by_stage(df: pd.DataFrame) -> pd.DataFrame:
    """Return average lead score by CRM stage in display order."""
    grouped = (
        df.groupby("crm_stage", as_index=False)["lead_score"]
        .mean()
        .rename(columns={"lead_score": "avg_lead_score"})
    )

    scaffold = pd.DataFrame({"crm_stage": CRM_STAGE_ORDER})
    merged = scaffold.merge(grouped, on="crm_stage", how="left")
    merged["avg_lead_score"] = merged["avg_lead_score"].fillna(0).round(1)
    return merged
