from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


QUALIFIED_STAGES = {"Qualified", "Proposal", "Negotiation"}
RISK_STALE_DAYS = 45


@dataclass(frozen=True)
class ExecutiveInsight:
    title: str
    value: str
    detail: str
    priority: str


def _money(value: float) -> str:
    return f"${value:,.0f}"


def _percent(value: float) -> str:
    return f"{value:.1%}"


def _empty_kpis() -> dict[str, float]:
    return {
        "total_pipeline_value": 0.0,
        "expected_revenue": 0.0,
        "average_deal_size": 0.0,
        "win_rate": 0.0,
        "qualified_leads": 0,
        "average_lead_score": 0.0,
        "hot_leads": 0,
        "pipeline_velocity": 0.0,
    }


def executive_kpis(df: pd.DataFrame) -> dict[str, float]:
    """Return executive KPI values for the currently filtered pipeline."""
    if df.empty:
        return _empty_kpis()

    total_pipeline = float(df["deal_value"].sum())
    expected_revenue = float(df["weighted_value"].sum())
    deal_count = int(df["lead_id"].nunique())
    avg_cycle_days = float(df["days_in_pipeline"].mean()) if deal_count else 0.0

    return {
        "total_pipeline_value": total_pipeline,
        "expected_revenue": expected_revenue,
        "average_deal_size": total_pipeline / deal_count if deal_count else 0.0,
        "win_rate": expected_revenue / total_pipeline if total_pipeline else 0.0,
        "qualified_leads": int(df[df["stage"].isin(QUALIFIED_STAGES)]["lead_id"].nunique()),
        "average_lead_score": float(df["lead_score"].mean()) if deal_count else 0.0,
        "hot_leads": int((df["lead_label"] == "Hot Lead").sum()),
        "pipeline_velocity": expected_revenue / avg_cycle_days if avg_cycle_days else 0.0,
    }


def industry_momentum(df: pd.DataFrame) -> pd.DataFrame:
    """Rank industries by weighted pipeline created per day in pipeline."""
    if df.empty:
        return pd.DataFrame(
            columns=["industry", "deal_value", "weighted_value", "lead_id", "avg_days", "momentum"]
        )

    grouped = (
        df.groupby("industry", as_index=False)
        .agg(
            deal_value=("deal_value", "sum"),
            weighted_value=("weighted_value", "sum"),
            lead_id=("lead_id", "count"),
            avg_days=("days_in_pipeline", "mean"),
        )
        .sort_values(["weighted_value", "deal_value"], ascending=False)
    )
    grouped["momentum"] = grouped["weighted_value"] / grouped["avg_days"].clip(lower=1)
    return grouped.sort_values(["momentum", "weighted_value"], ascending=False).reset_index(drop=True)


def lead_source_value(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["source", "deal_value", "weighted_value", "lead_id"])

    return (
        df.groupby("source", as_index=False)
        .agg(deal_value=("deal_value", "sum"), weighted_value=("weighted_value", "sum"), lead_id=("lead_id", "count"))
        .sort_values(["weighted_value", "deal_value"], ascending=False)
        .reset_index(drop=True)
    )


def stage_performance(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["stage", "deal_value", "weighted_value", "lead_id", "avg_score"])

    return (
        df.groupby("stage", as_index=False)
        .agg(
            deal_value=("deal_value", "sum"),
            weighted_value=("weighted_value", "sum"),
            lead_id=("lead_id", "count"),
            avg_score=("lead_score", "mean"),
        )
        .sort_values(["weighted_value", "avg_score"], ascending=False)
        .reset_index(drop=True)
    )


def top_opportunities(df: pd.DataFrame, limit: int = 10) -> pd.DataFrame:
    columns = [
        "lead_id",
        "company",
        "industry",
        "source",
        "stage",
        "lead_owner",
        "deal_value",
        "weighted_value",
        "lead_score",
        "days_in_pipeline",
        "last_contact_date",
        "next_step",
    ]
    if df.empty:
        return pd.DataFrame(columns=columns)

    return (
        df[columns]
        .sort_values(["deal_value", "lead_score", "weighted_value"], ascending=False)
        .head(limit)
        .reset_index(drop=True)
    )


def executive_insights(df: pd.DataFrame) -> list[ExecutiveInsight]:
    """Build deterministic management insights from the filtered data."""
    if df.empty:
        return [
            ExecutiveInsight(
                "No matching pipeline",
                "Adjust filters",
                "There are no opportunities in the current executive view.",
                "Medium",
            )
        ]

    largest = df.sort_values(["deal_value", "lead_score"], ascending=False).iloc[0]
    momentum = industry_momentum(df)
    source_values = lead_source_value(df)
    stages = stage_performance(df)
    stale = df[df["days_in_pipeline"] >= RISK_STALE_DAYS].copy()
    attention = (
        df.groupby("industry", as_index=False)
        .agg(avg_score=("lead_score", "mean"), stale_count=("days_in_pipeline", lambda s: int((s >= RISK_STALE_DAYS).sum())))
        .sort_values(["avg_score", "stale_count"], ascending=[True, False])
    )
    followups = df.sort_values(
        ["lead_score", "deal_value", "days_in_pipeline"], ascending=[False, False, False]
    ).head(3)

    risk_row = (
        stale.sort_values(["deal_value", "days_in_pipeline"], ascending=False).iloc[0]
        if not stale.empty
        else df.sort_values(["days_in_pipeline", "deal_value"], ascending=False).iloc[0]
    )

    followup_text = ", ".join(
        f"{row.company} ({row.next_step})" for row in followups.itertuples(index=False)
    )

    return [
        ExecutiveInsight(
            "Largest opportunity",
            str(largest["company"]),
            f"{_money(float(largest['deal_value']))} in {largest['industry']} at {int(largest['lead_score'])} lead score.",
            "High",
        ),
        ExecutiveInsight(
            "Fastest-growing industry",
            str(momentum.iloc[0]["industry"]),
            f"{_money(float(momentum.iloc[0]['weighted_value']))} expected revenue with strongest current pipeline momentum.",
            "High",
        ),
        ExecutiveInsight(
            "Highest-value lead source",
            str(source_values.iloc[0]["source"]),
            f"{_money(float(source_values.iloc[0]['weighted_value']))} expected revenue across {int(source_values.iloc[0]['lead_id'])} leads.",
            "High",
        ),
        ExecutiveInsight(
            "Best-performing pipeline stage",
            str(stages.iloc[0]["stage"]),
            f"{_money(float(stages.iloc[0]['weighted_value']))} expected revenue with {stages.iloc[0]['avg_score']:.1f} average lead score.",
            "Medium",
        ),
        ExecutiveInsight(
            "Biggest pipeline risk",
            str(risk_row["company"]),
            f"{int(risk_row['days_in_pipeline'])} days in pipeline on a {_money(float(risk_row['deal_value']))} opportunity.",
            "High",
        ),
        ExecutiveInsight(
            "Industries needing attention",
            ", ".join(attention.head(3)["industry"].astype(str)),
            "Lowest average score or elevated stale-opportunity concentration in the current view.",
            "Medium",
        ),
        ExecutiveInsight(
            "Highest priority follow-ups",
            f"{len(followups)} accounts",
            followup_text,
            "High",
        ),
    ]


def executive_summary(df: pd.DataFrame) -> list[str]:
    """Generate a deterministic executive summary for morning review."""
    kpis = executive_kpis(df)
    insights = {insight.title: insight for insight in executive_insights(df)}

    if df.empty:
        return [
            "No opportunities match the current filters, so pipeline coverage cannot be assessed.",
            "Broaden filters before making executive decisions from this view.",
            "Recommended action: restore at least one industry, stage, owner, or lead score segment.",
            "Revenue outlook is unavailable until matching pipeline is visible.",
            "Sales risk is concentrated in filter coverage rather than opportunity quality.",
        ]

    stale_count = int((df["days_in_pipeline"] >= RISK_STALE_DAYS).sum())
    qualified_share = kpis["qualified_leads"] / max(int(df["lead_id"].nunique()), 1)
    hot_share = kpis["hot_leads"] / max(int(df["lead_id"].nunique()), 1)

    return [
        f"Current filtered pipeline totals {_money(kpis['total_pipeline_value'])}, with {_money(kpis['expected_revenue'])} in probability-weighted expected revenue.",
        f"Forecast win rate is {_percent(kpis['win_rate'])}, supported by {kpis['qualified_leads']} qualified-stage leads and {kpis['hot_leads']} hot leads.",
        f"Average deal size is {_money(kpis['average_deal_size'])}; pipeline velocity is {_money(kpis['pipeline_velocity'])} of expected revenue per pipeline day.",
        f"Largest upside is {insights['Largest opportunity'].value}: {insights['Largest opportunity'].detail}",
        f"Top acquisition channel is {insights['Highest-value lead source'].value}, while {insights['Fastest-growing industry'].value} shows the strongest current momentum.",
        f"Pipeline health is {'strong' if qualified_share >= 0.55 else 'developing'} with {qualified_share:.0%} of leads in qualified or later stages.",
        f"Primary sales risk: {stale_count} opportunities have been in pipeline for at least {RISK_STALE_DAYS} days.",
        f"Recommended action: focus executive follow-up on {insights['Highest priority follow-ups'].detail}.",
        f"Management attention should go to {insights['Industries needing attention'].value} to improve conversion quality.",
        f"Hot lead concentration is {hot_share:.0%}; keep next steps current for late-stage, high-value opportunities.",
    ]
