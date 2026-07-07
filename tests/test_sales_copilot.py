from src.copilot.analysis import generate_sales_copilot_analysis
from src.data.loader import load_leads
from src.scoring.engine import score_leads
from src.scoring.metrics import apply_pipeline_probability


def _scored_leads():
    return apply_pipeline_probability(score_leads(load_leads()))


def _lead(company: str):
    df = _scored_leads()
    return df.loc[df["company"] == company].iloc[0]


def test_sales_copilot_returns_required_outputs():
    analysis = generate_sales_copilot_analysis(_lead("ArcNova Pharma"))

    assert analysis.buying_intent in {"Low", "Medium", "High"}
    assert analysis.recommended_channel in {"Email", "LinkedIn", "Phone", "Demo"}
    assert analysis.executive_recommendation in {
        "Pursue Immediately",
        "High Priority",
        "Monitor",
        "Low Priority",
    }
    assert 0 <= analysis.deal_probability <= 100
    assert analysis.estimated_time_to_close
    assert analysis.follow_up_timing
    assert 45 <= analysis.confidence <= 94


def test_sales_copilot_cards_answer_core_questions():
    analysis = generate_sales_copilot_analysis(_lead("ArcNova Pharma"))
    card_titles = {card.title for card in analysis.cards}

    assert "Why this lead is valuable" in card_titles
    assert "Biggest risks" in card_titles
    assert "Next best action" in card_titles
    assert "Executive recommendation" in card_titles
    assert all(card.answer for card in analysis.cards)
    assert all(0 <= card.confidence <= 100 for card in analysis.cards)


def test_sales_copilot_objection_handling_covers_expected_topics():
    analysis = generate_sales_copilot_analysis(_lead("ArcNova Pharma"))
    objections = {objection.objection for objection in analysis.objections}

    assert objections == {
        "Budget",
        "Timing",
        "Competition",
        "Integration",
        "Decision maker",
    }
    assert all(objection.response for objection in analysis.objections)
    assert all(0 <= objection.confidence <= 100 for objection in analysis.objections)


def test_sales_copilot_recommends_immediate_action_for_strong_late_stage_lead():
    analysis = generate_sales_copilot_analysis(_lead("ArcNova Pharma"))

    assert analysis.buying_intent == "High"
    assert analysis.executive_recommendation == "Pursue Immediately"
    assert analysis.deal_probability >= 60


def test_sales_copilot_uses_demo_for_qualified_leads():
    analysis = generate_sales_copilot_analysis(_lead("OrbitIQ Aerospace"))

    assert analysis.recommended_channel == "Demo"
    assert "demo" in analysis.cards[2].answer.lower()


def test_sales_copilot_as_dict_is_streamlit_friendly():
    analysis = generate_sales_copilot_analysis(_lead("ArcNova Pharma")).as_dict()

    assert analysis["company"] == "ArcNova Pharma"
    assert isinstance(analysis["cards"], list)
    assert isinstance(analysis["objections"], list)
