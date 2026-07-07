from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd


HIGH_VALUE_DEAL = 175000
STALE_DAYS = 45


@dataclass(frozen=True)
class CopilotCard:
    title: str
    answer: str
    confidence: int
    rationale: str


@dataclass(frozen=True)
class ObjectionResponse:
    objection: str
    response: str
    confidence: int


@dataclass(frozen=True)
class SalesCopilotAnalysis:
    lead_id: str
    company: str
    buying_intent: str
    deal_probability: int
    estimated_time_to_close: str
    recommended_channel: str
    follow_up_timing: str
    executive_recommendation: str
    confidence: int
    cards: list[CopilotCard]
    meeting_agenda: list[str]
    objections: list[ObjectionResponse]

    def as_dict(self) -> dict[str, Any]:
        return {
            "lead_id": self.lead_id,
            "company": self.company,
            "buying_intent": self.buying_intent,
            "deal_probability": self.deal_probability,
            "estimated_time_to_close": self.estimated_time_to_close,
            "recommended_channel": self.recommended_channel,
            "follow_up_timing": self.follow_up_timing,
            "executive_recommendation": self.executive_recommendation,
            "confidence": self.confidence,
            "cards": [card.__dict__ for card in self.cards],
            "meeting_agenda": self.meeting_agenda,
            "objections": [objection.__dict__ for objection in self.objections],
        }


def _clamp(value: int, low: int = 0, high: int = 100) -> int:
    return max(low, min(high, int(value)))


def _money(value: float) -> str:
    return f"${value:,.0f}"


def _lead_value(row: pd.Series) -> str:
    reasons = [
        f"{row['company']} represents a {_money(float(row['deal_value']))} opportunity",
        f"with a {int(row['lead_score'])} lead score",
        f"and {int(row['engagement_score'])} engagement score",
    ]
    if float(row["deal_value"]) >= HIGH_VALUE_DEAL:
        reasons.append("making it material to the current forecast")
    if str(row["company_size"]) == "Enterprise":
        reasons.append("with enterprise expansion potential")
    return ", ".join(reasons) + "."


def _risk_factors(row: pd.Series) -> list[str]:
    risks: list[str] = []
    if int(row["days_in_pipeline"]) >= STALE_DAYS:
        risks.append(f"Pipeline age is elevated at {int(row['days_in_pipeline'])} days.")
    if int(row["engagement_score"]) < 70:
        risks.append("Engagement is below the preferred threshold for confident progression.")
    if int(row["lead_score"]) < 65:
        risks.append("Lead score suggests qualification gaps remain.")
    if str(row["stage"]) in {"Proposal", "Negotiation"} and str(row["urgency_level"]) != "High":
        risks.append("Late-stage urgency is not strong enough for a clean close path.")
    if str(row["source"]) == "Outbound":
        risks.append("Outbound-sourced interest may require stronger business-case validation.")
    if not risks:
        risks.append("No major red flags, but confirm decision process and buying timeline.")
    return risks


def _next_action(row: pd.Series) -> str:
    stage = str(row["stage"])
    if stage == "New":
        return "Run discovery, confirm the business pain, and qualify decision authority."
    if stage == "Qualified":
        return "Schedule a tailored demo tied to the documented use case and success criteria."
    if stage == "Proposal":
        return "Review the proposal with the buying committee and secure mutual close milestones."
    if stage == "Negotiation":
        return "Align commercial terms, confirm legal blockers, and ask for a signature date."
    return "Confirm the current stage and refresh the next best action."


def _follow_up_timing(row: pd.Series) -> str:
    score = int(row["lead_score"])
    days = int(row["days_in_pipeline"])
    if score >= 82 or str(row["stage"]) == "Negotiation":
        return "Within 24 hours"
    if score >= 72 or days >= STALE_DAYS:
        return "Within 2 business days"
    if score >= 60:
        return "This week"
    return "Within 10 business days"


def _channel(row: pd.Series) -> str:
    stage = str(row["stage"])
    if stage == "Qualified":
        return "Demo"
    if stage == "Negotiation" or int(row["days_in_pipeline"]) >= STALE_DAYS:
        return "Phone"
    if str(row["source"]) in {"Referral", "Partner", "Event"} and int(row["engagement_score"]) >= 75:
        return "LinkedIn"
    return "Email"


def _buying_intent(row: pd.Series) -> str:
    score = int(row["lead_score"])
    engagement = int(row["engagement_score"])
    stage = str(row["stage"])
    if score >= 80 and engagement >= 78 and stage in {"Proposal", "Negotiation"}:
        return "High"
    if score >= 65 and engagement >= 65 and stage in {"Qualified", "Proposal", "Negotiation"}:
        return "Medium"
    return "Low"


def _deal_probability(row: pd.Series) -> int:
    probability = int(round(float(row["win_probability"]) * 100))
    probability += max(-8, min(10, int(row["lead_score"]) - 72))
    if int(row["engagement_score"]) >= 85:
        probability += 5
    if str(row["urgency_level"]) == "High":
        probability += 4
    if int(row["days_in_pipeline"]) >= 65:
        probability -= 6
    elif int(row["days_in_pipeline"]) >= STALE_DAYS:
        probability -= 3
    return _clamp(probability, 5, 95)


def _time_to_close(row: pd.Series) -> str:
    stage = str(row["stage"])
    days = int(row["days_in_pipeline"])
    if stage == "Negotiation":
        return "1-3 weeks" if days < 65 else "2-4 weeks"
    if stage == "Proposal":
        return "3-6 weeks"
    if stage == "Qualified":
        return "6-10 weeks"
    return "10-14 weeks"


def _recommendation(row: pd.Series, probability: int) -> str:
    score = int(row["lead_score"])
    deal_value = float(row["deal_value"])
    if score >= 82 and probability >= 65:
        return "Pursue Immediately"
    if score >= 72 or (deal_value >= HIGH_VALUE_DEAL and probability >= 45):
        return "High Priority"
    if score >= 55:
        return "Monitor"
    return "Low Priority"


def _confidence(row: pd.Series, probability: int) -> int:
    confidence = 62
    if int(row["lead_score"]) >= 75:
        confidence += 10
    if int(row["engagement_score"]) >= 75:
        confidence += 8
    if str(row["stage"]) in {"Proposal", "Negotiation"}:
        confidence += 8
    if int(row["days_in_pipeline"]) >= STALE_DAYS:
        confidence -= 5
    if probability >= 70 or probability <= 25:
        confidence += 4
    return _clamp(confidence, 45, 94)


def _agenda(row: pd.Series) -> list[str]:
    stage = str(row["stage"])
    agenda = [
        "Confirm current business priority and success metric.",
        f"Review how the solution supports {row['industry']} operating goals.",
        "Validate stakeholders, decision process, and approval path.",
    ]
    if stage in {"Proposal", "Negotiation"}:
        agenda.append("Walk through proposal terms, risks, and mutual close plan.")
    else:
        agenda.append("Agree on next technical or executive validation step.")
    agenda.append(f"Lock the next step: {row['next_step']}.")
    return agenda


def _objections(row: pd.Series) -> list[ObjectionResponse]:
    stage = str(row["stage"])
    industry = str(row["industry"])
    return [
        ObjectionResponse(
            "Budget",
            f"Anchor on the cost of delaying the {industry} initiative and map pricing to the highest-value use case first.",
            82,
        ),
        ObjectionResponse(
            "Timing",
            f"Propose a phased rollout and connect the timeline to {row['next_step']} so momentum stays concrete.",
            78 if int(row["days_in_pipeline"]) < STALE_DAYS else 72,
        ),
        ObjectionResponse(
            "Competition",
            "Differentiate on business outcome, implementation support, and the signals that made this account high-fit.",
            76,
        ),
        ObjectionResponse(
            "Integration",
            "Offer a technical validation session with their operations owner and document integration requirements early.",
            80 if stage in {"Qualified", "Proposal"} else 74,
        ),
        ObjectionResponse(
            "Decision maker",
            "Ask who signs, who blocks, and who owns the success metric; request a joint meeting with those stakeholders.",
            84,
        ),
    ]


def generate_sales_copilot_analysis(row: pd.Series) -> SalesCopilotAnalysis:
    """Generate deterministic AI-style sales guidance for one scored lead."""
    probability = _deal_probability(row)
    recommendation = _recommendation(row, probability)
    confidence = _confidence(row, probability)
    risks = _risk_factors(row)

    cards = [
        CopilotCard(
            "Why this lead is valuable",
            _lead_value(row),
            _clamp(confidence + 2),
            "Value is based on deal size, fit score, engagement, stage, source, and company size.",
        ),
        CopilotCard(
            "Biggest risks",
            " ".join(risks),
            _clamp(confidence - 4),
            "Risk is driven by pipeline age, engagement, lead score, urgency, source, and late-stage readiness.",
        ),
        CopilotCard(
            "Next best action",
            _next_action(row),
            _clamp(confidence + 1),
            f"Current CRM next step is: {row['next_step']}.",
        ),
        CopilotCard(
            "Executive recommendation",
            recommendation,
            confidence,
            "Recommendation combines lead score, probability, opportunity value, and stage maturity.",
        ),
    ]

    return SalesCopilotAnalysis(
        lead_id=str(row["lead_id"]),
        company=str(row["company"]),
        buying_intent=_buying_intent(row),
        deal_probability=probability,
        estimated_time_to_close=_time_to_close(row),
        recommended_channel=_channel(row),
        follow_up_timing=_follow_up_timing(row),
        executive_recommendation=recommendation,
        confidence=confidence,
        cards=cards,
        meeting_agenda=_agenda(row),
        objections=_objections(row),
    )
