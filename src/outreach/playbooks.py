PLAYBOOK_BY_STAGE = {
    "New": "Run first-touch sequence with one value email and one LinkedIn touch.",
    "Qualified": "Personalize discovery agenda and validate buying committee roles.",
    "Proposal": "Share ROI summary and secure timeline for procurement handoff.",
    "Negotiation": "Align legal, pricing, and executive sponsors around close plan.",
}


def get_playbook(stage: str) -> str:
    """Return a non-AI outreach recommendation based on lead stage."""
    return PLAYBOOK_BY_STAGE.get(stage, "Review account context and define next action.")
