from src.data.loader import load_leads
from src.scoring.engine import score_leads


def test_score_engine_adds_required_columns():
    df = score_leads(load_leads())
    expected = {
        "lead_score",
        "lead_label",
        "urgency_level",
        "score_explanation",
        "strongest_positive_signals",
        "biggest_risks",
    }
    assert expected.issubset(df.columns)


def test_score_ranges_and_labels_are_valid():
    df = score_leads(load_leads())
    assert df["lead_score"].between(0, 100).all()
    assert set(df["lead_label"].unique()).issubset({"Hot Lead", "Warm Lead", "Cold Lead"})


def test_explanation_fields_are_non_empty():
    df = score_leads(load_leads())
    assert (df["score_explanation"].str.len() > 0).all()
    assert (df["strongest_positive_signals"].str.contains(r"\+", regex=True)).all()
    assert (df["biggest_risks"].str.len() > 0).all()
