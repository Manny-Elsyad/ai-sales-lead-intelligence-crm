import pandas as pd
import streamlit as st

from src.data.loader import load_leads
from src.scoring.metrics import apply_pipeline_probability, summarize_kpis
from src.ui.theme import DARK_THEME_CSS
from src.visualizations.charts import pipeline_by_stage_chart


st.set_page_config(
    page_title="AI Sales Lead Intelligence CRM",
    page_icon="📈",
    layout="wide",
)


def _apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("Filters")

    industries = st.sidebar.multiselect(
        "Industry",
        options=sorted(df["industry"].unique()),
        default=sorted(df["industry"].unique()),
    )
    stages = st.sidebar.multiselect(
        "Stage",
        options=["New", "Qualified", "Proposal", "Negotiation"],
        default=["New", "Qualified", "Proposal", "Negotiation"],
    )
    owners = st.sidebar.multiselect(
        "Lead Owner",
        options=sorted(df["lead_owner"].unique()),
        default=sorted(df["lead_owner"].unique()),
    )
    min_score = st.sidebar.slider("Minimum Lead Score", min_value=0, max_value=100, value=60)

    filtered = df[
        (df["industry"].isin(industries))
        & (df["stage"].isin(stages))
        & (df["lead_owner"].isin(owners))
        & (df["lead_score"] >= min_score)
    ]
    return filtered


def _render_kpis(kpis: dict[str, float]) -> None:
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown("<div class='kpi-card'>", unsafe_allow_html=True)
        st.metric("Total Leads", f"{kpis['total_leads']:,}")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='kpi-card'>", unsafe_allow_html=True)
        st.metric("Pipeline", f"${kpis['total_pipeline']:,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='kpi-card'>", unsafe_allow_html=True)
        st.metric("Weighted Pipeline", f"${kpis['weighted_pipeline']:,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with c4:
        st.markdown("<div class='kpi-card'>", unsafe_allow_html=True)
        st.metric("Avg Lead Score", f"{kpis['avg_lead_score']:.1f}")
        st.markdown("</div>", unsafe_allow_html=True)


def render_dashboard() -> None:
    st.markdown(DARK_THEME_CSS, unsafe_allow_html=True)
    st.markdown(
        """
        <div class='hero'>
            <h2 style='margin-bottom:0.3rem;'>Executive Lead Intelligence Dashboard</h2>
            <p style='margin-bottom:0;'>Track qualified pipeline, monitor sales momentum, and prioritize high-fit B2B opportunities.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    leads = load_leads()
    leads = apply_pipeline_probability(leads)
    filtered_leads = _apply_filters(leads)
    kpis = summarize_kpis(filtered_leads)

    _render_kpis(kpis)

    st.subheader("Pipeline Analytics")
    stage_fig = pipeline_by_stage_chart(filtered_leads)
    st.plotly_chart(stage_fig, use_container_width=True)

    st.subheader("Lead Portfolio")
    table_columns = [
        "lead_id",
        "company",
        "industry",
        "region",
        "lead_owner",
        "stage",
        "deal_value",
        "lead_score",
        "weighted_value",
        "last_contact_date",
        "next_step",
    ]

    display_df = filtered_leads[table_columns].sort_values(
        by=["lead_score", "deal_value"], ascending=[False, False]
    )

    st.data_editor(
        display_df,
        use_container_width=True,
        hide_index=True,
        disabled=True,
        column_config={
            "deal_value": st.column_config.NumberColumn("Deal Value", format="$%d"),
            "weighted_value": st.column_config.NumberColumn("Weighted Value", format="$%d"),
            "lead_score": st.column_config.NumberColumn("Lead Score", format="%.1f"),
            "last_contact_date": st.column_config.DateColumn("Last Contact"),
        },
    )

    st.caption(f"Showing {len(display_df)} leads after filters.")
