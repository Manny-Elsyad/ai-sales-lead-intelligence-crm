from typing import Dict, List, Tuple

import pandas as pd


COMPANY_SIZE_SCORE = {
    "SMB": 8,
    "Mid-Market": 14,
    "Enterprise": 20,
}

SOURCE_SCORE = {
    "Outbound": 8,
    "Inbound": 10,
    "Event": 12,
    "Partner": 13,
    "Referral": 15,
}

STAGE_SCORE = {
    "New": 6,
    "Qualified": 12,
    "Proposal": 16,
    "Negotiation": 20,
}

INDUSTRY_FIT_SCORE = {
    "FinTech": 17,
    "Healthcare": 16,
    "Cybersecurity": 16,
    "Biotech": 15,
    "Insurance": 15,
    "Manufacturing": 14,
    "Telecom": 14,
    "Energy": 14,
    "Pharmaceuticals": 14,
    "Logistics": 13,
    "Transportation": 13,
    "Aerospace": 13,
    "Retail": 12,
    "HR Tech": 12,
    "Construction": 11,
    "Legal Tech": 11,
    "AgriTech": 11,
    "EdTech": 10,
    "Real Estate": 9,
    "Media": 8,
}


def _deal_value_score(deal_value: float) -> int:
    if deal_value >= 250000:
        return 15
    if deal_value >= 175000:
        return 12
    if deal_value >= 100000:
        return 9
    if deal_value >= 60000:
        return 6
    return 3


def _engagement_score_points(engagement: float) -> int:
    if engagement >= 85:
        return 15
    if engagement >= 75:
        return 12
    if engagement >= 65:
        return 9
    if engagement >= 55:
        return 6
    return 3


def _urgency_score(days_in_pipeline: int, stage: str) -> Tuple[int, str]:
    # Longer cycle in late stages indicates urgency to close while stale early-stage leads are risky.
    if stage in {"Proposal", "Negotiation"}:
        if days_in_pipeline >= 45:
            return 10, "High"
        if days_in_pipeline >= 25:
            return 8, "Medium"
        return 6, "Low"

    if days_in_pipeline <= 14:
        return 8, "High"
    if days_in_pipeline <= 30:
        return 6, "Medium"
    return 3, "Low"


def _score_label(score: int) -> str:
    if score >= 75:
        return "Hot Lead"
    if score >= 50:
        return "Warm Lead"
    return "Cold Lead"


def _build_explanations(contributions: Dict[str, int]) -> Tuple[str, str, str]:
    positives = sorted(contributions.items(), key=lambda item: item[1], reverse=True)[:3]
    risks = sorted(contributions.items(), key=lambda item: item[1])[:2]

    positive_text = ", ".join([f"{name} (+{value})" for name, value in positives])
    risk_text = ", ".join([f"{name} ({value})" for name, value in risks])

    total = sum(contributions.values())
    if total >= 75:
        headline = "High-priority opportunity with strong buying signals and close potential."
    elif total >= 50:
        headline = "Promising lead with upside, but still needs qualification momentum."
    else:
        headline = "Lower-priority lead with weak conversion indicators right now."

    return headline, positive_text, risk_text


def score_leads(df: pd.DataFrame) -> pd.DataFrame:
    """Score leads from 0-100 using weighted business factors and add explanations."""
    data = df.copy()

    total_scores: List[int] = []
    labels: List[str] = []
    urgency_levels: List[str] = []
    score_explanations: List[str] = []
    strongest_signals: List[str] = []
    biggest_risks: List[str] = []

    for _, row in data.iterrows():
        urgency_points, urgency_level = _urgency_score(int(row["days_in_pipeline"]), str(row["stage"]))

        contributions = {
            "Company size": COMPANY_SIZE_SCORE.get(str(row["company_size"]), 8),
            "Estimated deal value": _deal_value_score(float(row["deal_value"])),
            "Industry fit": INDUSTRY_FIT_SCORE.get(str(row["industry"]), 10),
            "Engagement level": _engagement_score_points(float(row["engagement_score"])),
            "Urgency": urgency_points,
            "Lead source": SOURCE_SCORE.get(str(row["source"]), 8),
            "Pipeline stage": STAGE_SCORE.get(str(row["stage"]), 6),
        }

        total_score = max(0, min(100, int(round(sum(contributions.values())))))
        label = _score_label(total_score)
        explanation, positive_text, risk_text = _build_explanations(contributions)

        total_scores.append(total_score)
        labels.append(label)
        urgency_levels.append(urgency_level)
        score_explanations.append(explanation)
        strongest_signals.append(positive_text)
        biggest_risks.append(risk_text)

    data["lead_score"] = total_scores
    data["lead_label"] = labels
    data["urgency_level"] = urgency_levels
    data["score_explanation"] = score_explanations
    data["strongest_positive_signals"] = strongest_signals
    data["biggest_risks"] = biggest_risks
    return data
