import pandas as pd
import streamlit as st

from src.data.loader import load_leads
from src.outreach.generator import generate_outreach_for_lead
from src.pipeline.service import (
    CRM_STAGE_ORDER,
    add_crm_stage,
    average_lead_score_by_stage,
    group_leads_by_crm_stage,
    pipeline_summary_metrics,
)
from src.scoring.engine import score_leads
from src.scoring.metrics import apply_pipeline_probability, summarize_kpis
from src.ui.theme import DARK_THEME_CSS
from src.visualizations.charts import (
    lead_score_distribution_chart,
    pipeline_by_stage_chart,
    pipeline_funnel_chart,
)


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
        options=sorted(df["stage"].unique()),
        default=sorted(df["stage"].unique()),
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
    c1, c2, c3, c4, c5 = st.columns(5)

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
    with c5:
        st.markdown("<div class='kpi-card'>", unsafe_allow_html=True)
        st.metric("Hot Leads", f"{kpis['hot_leads']:,}")
        st.markdown("</div>", unsafe_allow_html=True)


def _render_outreach_generator(df: pd.DataFrame) -> None:
    st.subheader("Outreach Generator")

    if df.empty:
        st.info("No leads available with current filters. Adjust filters to generate outreach copy.")
        return

    selector_df = df.sort_values(by=["lead_score", "deal_value"], ascending=[False, False])
    lead_options = [
        f"{row.lead_id} | {row.company} | {row.lead_label} ({int(row.lead_score)})"
        for row in selector_df.itertuples(index=False)
    ]

    c1, c2 = st.columns([2, 1])
    with c1:
        selected_label = st.selectbox("Select Lead", options=lead_options, index=0)
    with c2:
        tone = st.selectbox("Tone", options=["Professional", "Friendly", "Executive"], index=0)

    selected_lead_id = selected_label.split(" | ")[0]
    selected_lead = selector_df.loc[selector_df["lead_id"] == selected_lead_id].iloc[0]

    generated = generate_outreach_for_lead(selected_lead, tone=tone)

    st.markdown("**Subject Line**")
    st.code(generated["subject_line"], language="text")

    st.markdown("**Short Email**")
    st.text_area("Generated Email", value=generated["short_email"], height=180)

    lc1, lc2 = st.columns(2)
    with lc1:
        st.markdown("**LinkedIn Message**")
        st.text_area("Generated LinkedIn", value=generated["linkedin_message"], height=140)
    with lc2:
        st.markdown("**Follow-up Message**")
        st.text_area("Generated Follow-up", value=generated["follow_up_message"], height=140)


def _render_lead_card(row: pd.Series) -> None:
    st.markdown(
        f"""
        <div class='lead-card'>
            <div><strong>{row['company']}</strong></div>
            <div style='font-size:0.85rem; opacity:0.9;'>{row['industry']}</div>
            <div style='font-size:0.85rem;'>Score: {int(row['lead_score'])} ({row['lead_label']})</div>
            <div style='font-size:0.85rem;'>Deal: ${row['deal_value']:,.0f}</div>
            <div style='font-size:0.85rem;'>Urgency: {row['urgency_level']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_crm_pipeline(df: pd.DataFrame) -> None:
    st.subheader("CRM Pipeline")

    crm_df = add_crm_stage(df)
    summary = pipeline_summary_metrics(crm_df)
    stage_scores = average_lead_score_by_stage(crm_df)

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Pipeline Value", f"${summary['total_pipeline_value']:,.0f}")
    c2.metric("Qualified Pipeline Value", f"${summary['qualified_pipeline_value']:,.0f}")
    c3.metric("Won Value", f"${summary['won_value']:,.0f}")

    st.plotly_chart(pipeline_funnel_chart(crm_df), use_container_width=True)

    st.markdown("**Average Lead Score by Stage**")
    st.dataframe(
        stage_scores,
        hide_index=True,
        use_container_width=True,
        column_config={
            "crm_stage": st.column_config.TextColumn("CRM Stage"),
            "avg_lead_score": st.column_config.NumberColumn("Avg Lead Score", format="%.1f"),
        },
    )

    grouped = group_leads_by_crm_stage(crm_df)
    stage_columns = st.columns(len(CRM_STAGE_ORDER))

    for index, stage in enumerate(CRM_STAGE_ORDER):
        stage_df = grouped[stage]
        with stage_columns[index]:
            st.markdown(
                f"""
                <div class='pipeline-stage'>
                    <strong>{stage}</strong><br/>
                    <span style='opacity:0.8'>{len(stage_df)} leads</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if stage_df.empty:
                st.caption("No leads")
            else:
                for _, row in stage_df.iterrows():
                    _render_lead_card(row)


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
    leads = score_leads(leads)
    leads = apply_pipeline_probability(leads)
    filtered_leads = _apply_filters(leads)
    kpis = summarize_kpis(filtered_leads)

    _render_kpis(kpis)

    st.subheader("Pipeline Analytics")
    chart_col_1, chart_col_2 = st.columns(2)
    with chart_col_1:
        stage_fig = pipeline_by_stage_chart(filtered_leads)
        st.plotly_chart(stage_fig, use_container_width=True)
    with chart_col_2:
        score_fig = lead_score_distribution_chart(filtered_leads)
        st.plotly_chart(score_fig, use_container_width=True)

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
        "lead_label",
        "weighted_value",
        "last_contact_date",
        "next_step",
        "score_explanation",
        "strongest_positive_signals",
        "biggest_risks",
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
            "lead_score": st.column_config.NumberColumn("Lead Score", format="%d"),
            "last_contact_date": st.column_config.DateColumn("Last Contact"),
            "lead_label": st.column_config.TextColumn("Score Label"),
            "score_explanation": st.column_config.TextColumn("Score Summary"),
            "strongest_positive_signals": st.column_config.TextColumn("Positive Signals"),
            "biggest_risks": st.column_config.TextColumn("Risks"),
        },
    )

    st.caption(f"Showing {len(display_df)} leads after filters.")
    _render_outreach_generator(filtered_leads)
    _render_crm_pipeline(filtered_leads)
