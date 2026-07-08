from src.copilot.analysis import generate_sales_copilot_analysis
from src.data.loader import load_leads
from src.scoring.engine import score_leads
from src.scoring.metrics import apply_pipeline_probability
from src.workspace.lead_workspace import (
    derive_contact_name,
    enrich_workspace_leads,
    get_workspace_lead,
    recommend_workspace_actions,
    search_workspace_leads,
)


def _workspace_df():
    return enrich_workspace_leads(apply_pipeline_probability(score_leads(load_leads())))


def test_enrich_workspace_leads_adds_stable_contact_name():
    df = _workspace_df()

    assert "contact_name" in df.columns
    assert derive_contact_name("L-1001") == derive_contact_name("L-1001")
    assert df.loc[df["lead_id"] == "L-1001", "contact_name"].iloc[0] == derive_contact_name("L-1001")


def test_search_workspace_leads_matches_company_contact_industry_and_owner():
    df = _workspace_df()
    contact = df.loc[df["company"] == "ArcNova Pharma", "contact_name"].iloc[0]

    assert "ArcNova Pharma" in set(search_workspace_leads(df, "arcnova")["company"])
    assert "ArcNova Pharma" in set(search_workspace_leads(df, contact.split()[0])["company"])
    assert not search_workspace_leads(df, "healthcare").empty
    assert not search_workspace_leads(df, "Jordan Kim").empty


def test_search_workspace_leads_empty_query_returns_all_sorted_leads():
    df = _workspace_df()
    results = search_workspace_leads(df, "")

    assert len(results) == len(df)
    assert results.iloc[0]["lead_score"] >= results.iloc[-1]["lead_score"]


def test_get_workspace_lead_returns_selected_row():
    df = _workspace_df()
    selected = get_workspace_lead(df, "L-1019")

    assert selected["company"] == "ArcNova Pharma"
    assert selected["lead_id"] == "L-1019"


def test_get_workspace_lead_raises_for_unknown_id():
    df = _workspace_df()

    try:
        get_workspace_lead(df, "missing")
    except ValueError as exc:
        assert "Lead id not found" in str(exc)
    else:
        raise AssertionError("Expected ValueError for unknown lead id")


def test_recommend_workspace_actions_returns_three_to_five_actions():
    lead = get_workspace_lead(_workspace_df(), "L-1019")
    analysis = generate_sales_copilot_analysis(lead)
    actions = recommend_workspace_actions(lead, analysis)

    assert 3 <= len(actions) <= 5
    assert any("executive" in action.lower() or "prioritize" in action.lower() for action in actions)
    assert any("proposal" in action.lower() for action in actions)


def test_recommend_workspace_actions_for_new_low_engagement_lead_rebuilds_engagement():
    lead = get_workspace_lead(_workspace_df(), "L-1023")
    analysis = generate_sales_copilot_analysis(lead)
    actions = recommend_workspace_actions(lead, analysis)

    assert any("discovery" in action.lower() for action in actions)
    assert any("rebuild engagement" in action.lower() for action in actions)
