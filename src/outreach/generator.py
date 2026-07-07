from typing import Dict

import pandas as pd


TONE_GUIDE = {
    "Professional": {
        "salutation": "Hello",
        "opener": "I am reaching out because",
        "close": "Would you be open to a 20-minute discussion next week?",
        "linkedin_close": "Open to connecting for a quick exchange?",
        "followup_prefix": "Following up on my previous note",
    },
    "Friendly": {
        "salutation": "Hi",
        "opener": "I wanted to reach out since",
        "close": "If helpful, happy to share ideas in a quick chat.",
        "linkedin_close": "Happy to connect and compare notes.",
        "followup_prefix": "Quick follow-up in case this got buried",
    },
    "Executive": {
        "salutation": "Good day",
        "opener": "I am writing with a focused recommendation because",
        "close": "If this is a priority, we can align on outcomes in a short executive briefing.",
        "linkedin_close": "Open to a concise executive-level conversation?",
        "followup_prefix": "Revisiting this with urgency",
    },
}


def _value_statement(deal_value: float, lead_score: int, lead_label: str) -> str:
    return (
        f"this ${deal_value:,.0f} opportunity is currently rated {lead_score}/100 "
        f"({lead_label}) and has clear revenue impact potential."
    )


def generate_outreach_for_lead(lead: pd.Series, tone: str = "Professional") -> Dict[str, str]:
    """Generate deterministic outreach messages using lead profile data and scoring signals."""
    tone_pack = TONE_GUIDE.get(tone, TONE_GUIDE["Professional"])

    company = str(lead["company"])
    industry = str(lead["industry"])
    stage = str(lead["stage"])
    deal_value = float(lead["deal_value"])
    lead_score = int(lead["lead_score"])
    lead_label = str(lead["lead_label"])
    risks = str(lead["biggest_risks"])

    subject = f"{company}: {stage} priorities for a ${deal_value:,.0f} pipeline opportunity"

    email = (
        f"{tone_pack['salutation']} {company} team,\n\n"
        f"{tone_pack['opener']} {company} is scaling in {industry}, and "
        f"{_value_statement(deal_value, lead_score, lead_label)}\n"
        f"Based on our review, the biggest execution risks are: {risks}. "
        f"We can help reduce those risks while keeping momentum in the {stage} stage.\n\n"
        f"{tone_pack['close']}\n\n"
        "Best regards,\n"
        "Sales Lead Intelligence Team"
    )

    linkedin = (
        f"{tone_pack['salutation']} - noticed {company}'s growth in {industry}. "
        f"Your current opportunity is scored {lead_score}/100 ({lead_label}) at ${deal_value:,.0f}. "
        f"Main risks we identified: {risks}. {tone_pack['linkedin_close']}"
    )

    follow_up = (
        f"{tone_pack['followup_prefix']} for {company}. "
        f"Given the {stage} stage and ${deal_value:,.0f} potential, "
        f"addressing {risks} could improve conversion confidence. "
        "Would a short review this week be useful?"
    )

    return {
        "subject_line": subject,
        "short_email": email,
        "linkedin_message": linkedin,
        "follow_up_message": follow_up,
    }
