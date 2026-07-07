from src.data.loader import load_leads
from src.pipeline.service import (
    CRM_STAGE_ORDER,
    add_crm_stage,
    average_lead_score_by_stage,
    group_leads_by_crm_stage,
    pipeline_summary_metrics,
)
from src.scoring.engine import score_leads


def _crm_df():
    return add_crm_stage(score_leads(load_leads()))


def test_group_leads_by_crm_stage_returns_all_stages():
    df = _crm_df()
    grouped = group_leads_by_crm_stage(df)

    assert list(grouped.keys()) == CRM_STAGE_ORDER
    assert sum(len(stage_df) for stage_df in grouped.values()) == len(df)


def test_pipeline_summary_metrics_are_consistent():
    df = _crm_df()
    metrics = pipeline_summary_metrics(df)

    assert set(metrics.keys()) == {
        "total_pipeline_value",
        "qualified_pipeline_value",
        "won_value",
    }
    assert metrics["total_pipeline_value"] >= metrics["qualified_pipeline_value"]
    assert metrics["qualified_pipeline_value"] >= metrics["won_value"]
    assert metrics["won_value"] >= 0


def test_average_lead_score_by_stage_has_all_rows():
    df = _crm_df()
    stage_scores = average_lead_score_by_stage(df)

    assert list(stage_scores["crm_stage"]) == CRM_STAGE_ORDER
    assert stage_scores["avg_lead_score"].between(0, 100).all()
