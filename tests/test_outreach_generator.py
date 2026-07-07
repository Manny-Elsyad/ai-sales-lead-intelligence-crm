from src.data.loader import load_leads
from src.outreach.generator import generate_outreach_for_lead
from src.scoring.engine import score_leads


def _sample_lead():
    df = score_leads(load_leads())
    return df.iloc[0]


def test_generate_outreach_contains_required_fields():
    lead = _sample_lead()
    generated = generate_outreach_for_lead(lead, tone="Professional")

    assert set(generated.keys()) == {
        "subject_line",
        "short_email",
        "linkedin_message",
        "follow_up_message",
    }


def test_generate_outreach_personalizes_with_lead_data():
    lead = _sample_lead()
    generated = generate_outreach_for_lead(lead, tone="Executive")

    assert lead["company"] in generated["subject_line"]
    assert lead["industry"] in generated["short_email"]
    assert str(int(lead["lead_score"])) in generated["linkedin_message"]
    assert lead["lead_label"] in generated["linkedin_message"]
    assert lead["stage"] in generated["short_email"]
    assert lead["biggest_risks"] in generated["follow_up_message"]


def test_generate_outreach_tone_changes_copy_deterministically():
    lead = _sample_lead()
    professional = generate_outreach_for_lead(lead, tone="Professional")
    friendly = generate_outreach_for_lead(lead, tone="Friendly")

    assert professional["short_email"] != friendly["short_email"]
    assert "Hello" in professional["short_email"]
    assert "Hi" in friendly["short_email"]
