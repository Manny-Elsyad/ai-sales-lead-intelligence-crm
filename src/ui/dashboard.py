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
from src.ui.components import badge, kpi_card, money, page_header, section_heading, sidebar_filter_header
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


def _render_plotly_chart(fig) -> None:
    if fig is not None:
        st.plotly_chart(fig, use_container_width=True)


def _apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    industry_options = sorted(df["industry"].unique())
    stage_options = sorted(df["stage"].unique())
    owner_options = sorted(df["lead_owner"].unique())

    reset = st.sidebar.button("Reset Filters", use_container_width=True, key="dashboard_reset")
    if reset:
        st.session_state["dashboard_industries"] = industry_options
        st.session_state["dashboard_stages"] = stage_options
        st.session_state["dashboard_owners"] = owner_options
        st.session_state["dashboard_min_score"] = 60

    active_count = 0
    active_count += int(st.session_state.get("dashboard_industries", industry_options) != industry_options)
    active_count += int(st.session_state.get("dashboard_stages", stage_options) != stage_options)
    active_count += int(st.session_state.get("dashboard_owners", owner_options) != owner_options)
    active_count += int(st.session_state.get("dashboard_min_score", 60) != 60)
    sidebar_filter_header(active_count)

    with st.sidebar.expander("🏢 Market", expanded=True):
        industries = st.multiselect(
            "Industry",
            options=industry_options,
            default=industry_options,
            key="dashboard_industries",
        )
    with st.sidebar.expander("🧭 Pipeline", expanded=True):
        stages = st.multiselect(
            "Stage",
            options=stage_options,
            default=stage_options,
            key="dashboard_stages",
        )
        min_score = st.slider(
            "Minimum Lead Score",
            min_value=0,
            max_value=100,
            value=60,
            key="dashboard_min_score",
        )
    with st.sidebar.expander("👤 Ownership", expanded=False):
        owners = st.multiselect(
            "Lead Owner",
            options=owner_options,
            default=owner_options,
            key="dashboard_owners",
        )

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
        kpi_card("◎", f"{kpis['total_leads']:,}", "Total Leads", "Filtered active records", "● Live", "neutral")
    with c2:
        kpi_card("◈", money(kpis["total_pipeline"]), "Pipeline", "Total opportunity value", "▲ Forecast", "positive")
    with c3:
        kpi_card("◆", money(kpis["weighted_pipeline"]), "Weighted Pipeline", "Probability-adjusted value", "▲ Expected", "positive")
    with c4:
        kpi_card("◉", f"{kpis['avg_lead_score']:.1f}", "Avg Lead Score", "Fit and engagement quality", "● Quality", "warning", kpis["avg_lead_score"])
    with c5:
        kpi_card("▲", f"{kpis['hot_leads']:,}", "Hot Leads", "Priority accounts", "▲ Priority", "positive")


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
            <div style='display:flex; justify-content:space-between; gap:0.5rem; align-items:flex-start;'>
                <strong>{row['company']}</strong>
                {badge(row['lead_label'])}
            </div>
            <div style='font-size:0.82rem; opacity:0.82; margin-top:0.25rem;'>{row['industry']} · {badge(row['stage'])}</div>
            <div style='font-size:0.85rem; margin-top:0.45rem;'>Score <strong>{int(row['lead_score'])}</strong> · Deal <strong>${row['deal_value']:,.0f}</strong></div>
            <div style='font-size:0.82rem; margin-top:0.25rem;'>Urgency {badge(row['urgency_level'])}</div>
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

    _render_plotly_chart(pipeline_funnel_chart(crm_df))

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

    leads = load_leads()
    leads = score_leads(leads)
    leads = apply_pipeline_probability(leads)
    filtered_leads = _apply_filters(leads)
    kpis = summarize_kpis(filtered_leads)

    page_header(
        "Executive Lead Intelligence Dashboard",
        "Track qualified pipeline, revenue momentum, and high-fit B2B opportunities.",
        len(filtered_leads),
        "📈",
    )

    _render_kpis(kpis)

    section_heading("Pipeline Analytics", "Stage value and score quality across the filtered pipeline.")
    chart_col_1, chart_col_2 = st.columns(2)
    with chart_col_1:
        stage_fig = pipeline_by_stage_chart(filtered_leads)
        _render_plotly_chart(stage_fig)
    with chart_col_2:
        score_fig = lead_score_distribution_chart(filtered_leads)
        _render_plotly_chart(score_fig)

    section_heading("Lead Portfolio", "Highest-signal leads are shown as cards with the full editable view preserved below.")
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
        "urgency_level",
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

    card_cols = st.columns(4)
    for index, (_, row) in enumerate(display_df.head(8).iterrows()):
        with card_cols[index % 4]:
            _render_lead_card(row)

    with st.expander("Open full lead portfolio", expanded=False):
        st.data_editor(
            display_df,
            use_container_width=True,
            hide_index=True,
            disabled=True,
            column_config={
                "deal_value": st.column_config.NumberColumn("Deal Value", format="$%d"),
                "weighted_value": st.column_config.NumberColumn("Weighted Value", format="$%d"),
                "lead_score": st.column_config.ProgressColumn("Lead Score", min_value=0, max_value=100),
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
