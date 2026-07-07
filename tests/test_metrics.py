from src.data.loader import load_leads
from src.scoring.metrics import apply_pipeline_probability, summarize_kpis


def test_apply_pipeline_probability_adds_columns():
    df = load_leads()
    scored = apply_pipeline_probability(df)
    assert "win_probability" in scored.columns
    assert "weighted_value" in scored.columns
    assert scored["win_probability"].between(0, 1).all()


def test_summarize_kpis_returns_expected_keys():
    df = apply_pipeline_probability(load_leads())
    kpis = summarize_kpis(df)
    assert set(kpis.keys()) == {
        "total_leads",
        "total_pipeline",
        "weighted_pipeline",
        "avg_lead_score",
    }
    assert kpis["total_leads"] > 0
    assert kpis["total_pipeline"] > 0
