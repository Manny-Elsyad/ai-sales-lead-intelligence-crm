from src.analytics.executive import (
    executive_insights,
    executive_kpis,
    executive_summary,
    industry_momentum,
    lead_source_value,
    top_opportunities,
)
from src.data.loader import load_leads
from src.scoring.engine import score_leads
from src.scoring.metrics import apply_pipeline_probability


def _executive_df():
    return apply_pipeline_probability(score_leads(load_leads()))


def test_executive_kpis_include_required_management_metrics():
    df = _executive_df()
    kpis = executive_kpis(df)

    assert set(kpis.keys()) == {
        "total_pipeline_value",
        "expected_revenue",
        "average_deal_size",
        "win_rate",
        "qualified_leads",
        "average_lead_score",
        "hot_leads",
        "pipeline_velocity",
    }
    assert kpis["total_pipeline_value"] == df["deal_value"].sum()
    assert kpis["expected_revenue"] == df["weighted_value"].sum()
    assert 0 <= kpis["win_rate"] <= 1
    assert kpis["pipeline_velocity"] > 0


def test_executive_insights_cover_required_business_topics():
    insights = executive_insights(_executive_df())
    titles = {insight.title for insight in insights}

    assert titles == {
        "Largest opportunity",
        "Fastest-growing industry",
        "Highest-value lead source",
        "Best-performing pipeline stage",
        "Biggest pipeline risk",
        "Industries needing attention",
        "Highest priority follow-ups",
    }
    assert all(insight.value for insight in insights)
    assert all(insight.detail for insight in insights)


def test_executive_summary_returns_management_bullets():
    summary = executive_summary(_executive_df())

    assert 5 <= len(summary) <= 10
    assert any("pipeline" in point.lower() for point in summary)
    assert any("risk" in point.lower() for point in summary)
    assert any("Recommended action" in point for point in summary)


def test_top_opportunities_are_ranked_by_deal_value():
    opportunities = top_opportunities(_executive_df(), limit=5)

    assert len(opportunities) == 5
    assert opportunities["deal_value"].is_monotonic_decreasing
    assert opportunities.iloc[0]["company"] == "ArcNova Pharma"


def test_ranked_groups_are_sorted_by_executive_value():
    df = _executive_df()
    momentum = industry_momentum(df)
    sources = lead_source_value(df)

    assert momentum.iloc[0]["momentum"] >= momentum.iloc[-1]["momentum"]
    assert sources.iloc[0]["weighted_value"] >= sources.iloc[-1]["weighted_value"]


def test_empty_filters_return_zero_kpis_and_guidance():
    empty = _executive_df().iloc[0:0]
    kpis = executive_kpis(empty)
    insights = executive_insights(empty)
    summary = executive_summary(empty)

    assert all(value == 0 for value in kpis.values())
    assert insights[0].title == "No matching pipeline"
    assert 5 <= len(summary) <= 10
