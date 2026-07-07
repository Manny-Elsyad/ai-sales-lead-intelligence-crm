from src.data.loader import load_leads


def test_load_leads_has_expected_columns():
    df = load_leads()
    expected_columns = {
        "lead_id",
        "company",
        "industry",
        "region",
        "company_size",
        "annual_revenue_m",
        "lead_owner",
        "stage",
        "deal_value",
        "engagement_score",
        "fit_score",
        "last_contact_date",
        "next_step",
        "source",
        "days_in_pipeline",
        "lead_score",
    }
    assert expected_columns.issubset(set(df.columns))
    assert len(df) >= 20
