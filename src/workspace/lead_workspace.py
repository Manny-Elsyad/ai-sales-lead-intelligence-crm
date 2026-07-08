from __future__ import annotations

import pandas as pd

from src.copilot.analysis import SalesCopilotAnalysis


CONTACT_FIRST_NAMES = [
    "Avery",
    "Riley",
    "Morgan",
    "Casey",
    "Jordan",
    "Taylor",
    "Parker",
    "Quinn",
]
CONTACT_LAST_NAMES = [
    "Chen",
    "Patel",
    "Rivera",
    "Morgan",
    "Lee",
    "Reed",
    "Nguyen",
    "Carter",
]


def derive_contact_name(lead_id: str) -> str:
    """Create a stable fictional contact name from a lead id."""
    digits = "".join(character for character in str(lead_id) if character.isdigit())
    seed = int(digits or 0)
    first = CONTACT_FIRST_NAMES[seed % len(CONTACT_FIRST_NAMES)]
    last = CONTACT_LAST_NAMES[(seed // len(CONTACT_FIRST_NAMES)) % len(CONTACT_LAST_NAMES)]
    return f"{first} {last}"


def enrich_workspace_leads(df: pd.DataFrame) -> pd.DataFrame:
    """Attach fields needed by the lead workspace without mutating source data."""
    data = df.copy()
    if "contact_name" not in data.columns:
        data["contact_name"] = data["lead_id"].apply(derive_contact_name)
    return data.sort_values(["lead_score", "deal_value"], ascending=[False, False]).reset_index(drop=True)


def search_workspace_leads(df: pd.DataFrame, query: str) -> pd.DataFrame:
    """Search by company, contact, industry, or owner."""
    data = enrich_workspace_leads(df)
    normalized = query.strip().lower()
    if not normalized:
        return data

    searchable = (
        data["company"].astype(str)
        + " "
        + data["contact_name"].astype(str)
        + " "
        + data["industry"].astype(str)
        + " "
        + data["lead_owner"].astype(str)
    ).str.lower()
    return data.loc[searchable.str.contains(normalized, regex=False)].reset_index(drop=True)


def get_workspace_lead(df: pd.DataFrame, lead_id: str) -> pd.Series:
    data = enrich_workspace_leads(df)
    matches = data.loc[data["lead_id"] == lead_id]
    if matches.empty:
        raise ValueError(f"Lead id not found: {lead_id}")
    return matches.iloc[0]


def recommend_workspace_actions(row: pd.Series, analysis: SalesCopilotAnalysis) -> list[str]:
    """Return deterministic next actions from score, urgency, stage, and risk signals."""
    actions: list[str] = []
    stage = str(row["stage"])
    score = int(row["lead_score"])
    urgency = str(row["urgency_level"])
    days = int(row["days_in_pipeline"])

    if score >= 82:
        actions.append("Book an executive alignment touch within 24 hours.")
    elif score >= 72:
        actions.append("Prioritize this lead in the current selling block.")
    else:
        actions.append("Refresh qualification notes before increasing sales effort.")

    if stage == "New":
        actions.append("Run discovery to validate pain, timeline, authority, and budget.")
    elif stage == "Qualified":
        actions.append("Schedule a tailored demo around the highest-impact use case.")
    elif stage == "Proposal":
        actions.append("Review proposal terms with stakeholders and confirm close criteria.")
    elif stage == "Negotiation":
        actions.append("Confirm legal, procurement, and signature path with the buyer.")

    if urgency == "High" or days >= 45:
        actions.append("Escalate stale or urgent blockers into a mutual action plan.")

    if analysis.recommended_channel == "Demo":
        actions.append("Send a demo agenda and ask the buyer to add technical stakeholders.")
    else:
        actions.append(f"Use {analysis.recommended_channel} for the next follow-up.")

    if "Engagement is below" in analysis.cards[1].answer or score < 65:
        actions.append("Rebuild engagement with a concise business-case proof point.")
    else:
        actions.append(f"Advance the CRM next step: {row['next_step']}.")

    return actions[:5]
