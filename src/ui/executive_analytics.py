import pandas as pd
import streamlit as st

from src.analytics.executive import executive_insights, executive_kpis, executive_summary, top_opportunities
from src.data.loader import load_leads
from src.scoring.engine import score_leads
from src.scoring.metrics import apply_pipeline_probability
from src.ui.components import badge, card, kpi_card, money, page_header, section_heading, sidebar_filter_header
from src.ui.theme import EXECUTIVE_THEME_CSS
from src.visualizations.charts import (
    executive_lead_score_distribution_chart,
    executive_sales_funnel_chart,
    monthly_pipeline_trend_chart,
    pipeline_stage_breakdown_chart,
    revenue_by_industry_chart,
    revenue_by_source_chart,
    top_opportunities_chart,
)


st.set_page_config(
    page_title="Executive Analytics",
    page_icon="📈",
    layout="wide",
)


def _money(value: float) -> str:
    return f"${value:,.0f}"


def _apply_executive_filters(df: pd.DataFrame) -> pd.DataFrame:
    industry_options = sorted(df["industry"].unique())
    stage_options = sorted(df["stage"].unique())
    owner_options = sorted(df["lead_owner"].unique())
    source_options = sorted(df["source"].unique())
    region_options = sorted(df["region"].unique())

    if st.sidebar.button("Reset Filters", use_container_width=True, key="executive_reset"):
        st.session_state["exec_industries"] = industry_options
        st.session_state["exec_stages"] = stage_options
        st.session_state["exec_owners"] = owner_options
        st.session_state["exec_sources"] = source_options
        st.session_state["exec_regions"] = region_options
        st.session_state["exec_score_range"] = (50, 100)
        st.session_state["exec_min_deal"] = 0

    active_count = 0
    active_count += int(st.session_state.get("exec_industries", industry_options) != industry_options)
    active_count += int(st.session_state.get("exec_stages", stage_options) != stage_options)
    active_count += int(st.session_state.get("exec_owners", owner_options) != owner_options)
    active_count += int(st.session_state.get("exec_sources", source_options) != source_options)
    active_count += int(st.session_state.get("exec_regions", region_options) != region_options)
    active_count += int(st.session_state.get("exec_score_range", (50, 100)) != (50, 100))
    active_count += int(st.session_state.get("exec_min_deal", 0) != 0)
    sidebar_filter_header(active_count)

    with st.sidebar.expander("🏢 Market", expanded=True):
        industries = st.multiselect("Industry", options=industry_options, default=industry_options, key="exec_industries")
        regions = st.multiselect("Region", options=region_options, default=region_options, key="exec_regions")
    with st.sidebar.expander("🧭 Pipeline", expanded=True):
        stages = st.multiselect("Pipeline Stage", options=stage_options, default=stage_options, key="exec_stages")
        min_score, max_score = st.slider("Lead Score Range", min_value=0, max_value=100, value=(50, 100), key="exec_score_range")
        min_deal_value = st.slider(
            "Minimum Deal Value",
            min_value=0,
            max_value=int(df["deal_value"].max()),
            value=0,
            step=5000,
            format="$%d",
            key="exec_min_deal",
        )
    with st.sidebar.expander("👤 Source & Owner", expanded=False):
        owners = st.multiselect("Lead Owner", options=owner_options, default=owner_options, key="exec_owners")
        sources = st.multiselect("Lead Source", options=source_options, default=source_options, key="exec_sources")

    return df[
        (df["industry"].isin(industries))
        & (df["stage"].isin(stages))
        & (df["lead_owner"].isin(owners))
        & (df["source"].isin(sources))
        & (df["region"].isin(regions))
        & (df["lead_score"].between(min_score, max_score))
        & (df["deal_value"] >= min_deal_value)
    ].copy()


def _render_kpis(kpis: dict[str, float]) -> None:
    first_row = st.columns(4)
    second_row = st.columns(4)

    with first_row[0]:
        kpi_card("◈", money(kpis["total_pipeline_value"]), "Total Pipeline Value", "Open opportunity value", "▲ Pipeline", "positive")
    with first_row[1]:
        kpi_card("◆", money(kpis["expected_revenue"]), "Expected Revenue", "Probability-weighted forecast", "▲ Forecast", "positive")
    with first_row[2]:
        kpi_card("◎", money(kpis["average_deal_size"]), "Average Deal Size", "Mean opportunity value", "● ACV", "neutral")
    with first_row[3]:
        kpi_card("◉", f"{kpis['win_rate']:.1%}", "Win Rate", "Weighted conversion outlook", "▲ Outlook", "positive", kpis["win_rate"] * 100)

    with second_row[0]:
        kpi_card("✓", f"{int(kpis['qualified_leads']):,}", "Qualified Leads", "Qualified stage or later", "● Coverage", "neutral")
    with second_row[1]:
        kpi_card("▲", f"{kpis['average_lead_score']:.1f}", "Average Lead Score", "Fit, engagement, and urgency", "● Quality", "warning", kpis["average_lead_score"])
    with second_row[2]:
        kpi_card("🔥", f"{int(kpis['hot_leads']):,}", "Hot Leads", "Score of 75 or higher", "▲ Priority", "positive")
    with second_row[3]:
        kpi_card("↗", money(kpis["pipeline_velocity"]), "Pipeline Velocity", "Expected revenue per pipeline day", "● Velocity", "neutral")


def _render_executive_brief(df: pd.DataFrame) -> None:
    section_heading("Executive Brief", "Priority signals translated into management action.")
    insights = {insight.title: insight for insight in executive_insights(df)}
    summary = executive_summary(df)
    health = next((point for point in summary if "Pipeline health" in point), "Pipeline health is being evaluated from current filters.")
    outlook = next((point for point in summary if "probability-weighted expected revenue" in point), "Revenue outlook updates with filters.")
    brief_items = [
        ("◆", "Biggest opportunity", insights.get("Largest opportunity"), "positive"),
        ("▲", "Highest priority follow-up", insights.get("Highest priority follow-ups"), "warning"),
        ("●", "Pipeline health", None, "neutral"),
        ("◈", "Revenue outlook", None, "positive"),
        ("!", "Biggest risk", insights.get("Biggest pipeline risk"), "risk"),
        ("✓", "Recommended action", None, "info"),
    ]
    cols = st.columns(2)
    for index, (icon, title, insight, variant) in enumerate(brief_items):
        if insight is not None:
            body = f"{badge(insight.priority + ' priority', variant)}<br/><strong>{insight.value}</strong><br/>{insight.detail}"
        elif title == "Pipeline health":
            body = f"{badge('Health', variant)}<br/>{health}"
        elif title == "Revenue outlook":
            body = f"{badge('Forecast', variant)}<br/>{outlook}"
        else:
            body = f"{badge('Action', variant)}<br/>{summary[-3] if len(summary) >= 3 else summary[-1]}"
        with cols[index % 2]:
            card(title, body, icon=icon, variant=variant)


def _render_summary(df: pd.DataFrame) -> None:
    st.subheader("Executive Summary")
    st.markdown("<div class='executive-panel'>", unsafe_allow_html=True)
    for point in executive_summary(df):
        st.markdown(f"- {point}")
    st.markdown("</div>", unsafe_allow_html=True)


def _render_opportunities_table(df: pd.DataFrame) -> None:
    opportunities = top_opportunities(df)
    st.dataframe(
        opportunities,
        hide_index=True,
        use_container_width=True,
        column_config={
            "deal_value": st.column_config.NumberColumn("Deal Value", format="$%d"),
            "weighted_value": st.column_config.NumberColumn("Expected Revenue", format="$%d"),
            "lead_score": st.column_config.NumberColumn("Lead Score", format="%d"),
            "last_contact_date": st.column_config.DateColumn("Last Contact"),
            "days_in_pipeline": st.column_config.NumberColumn("Days in Pipeline", format="%d"),
        },
    )


def render_executive_analytics() -> None:
    st.markdown(EXECUTIVE_THEME_CSS, unsafe_allow_html=True)

    leads = apply_pipeline_probability(score_leads(load_leads()))
    filtered = _apply_executive_filters(leads)
    kpis = executive_kpis(filtered)

    page_header(
        "Executive Analytics",
        "Board-ready pipeline health, forecast quality, sales risk, and account priorities.",
        len(filtered),
        "📈",
    )
    _render_kpis(kpis)

    if filtered.empty:
        st.warning("No opportunities match the current filters. Broaden the filters to restore executive analytics.")
        _render_executive_brief(filtered)
        _render_summary(filtered)
        return

    section_heading("Visualizations", "Sales funnel is prioritized, with revenue mix and stage quality below.")
    funnel_col, industry_col = st.columns([1.25, 0.75])
    with funnel_col:
        st.plotly_chart(executive_sales_funnel_chart(filtered), use_container_width=True)
    with industry_col:
        st.plotly_chart(revenue_by_industry_chart(filtered), use_container_width=True)

    source_col, stage_col = st.columns([1, 1])
    with source_col:
        st.plotly_chart(revenue_by_source_chart(filtered), use_container_width=True)
    with stage_col:
        st.plotly_chart(pipeline_stage_breakdown_chart(filtered), use_container_width=True)

    score_col, trend_col = st.columns([1, 1])
    with score_col:
        st.plotly_chart(executive_lead_score_distribution_chart(filtered), use_container_width=True)
    with trend_col:
        st.plotly_chart(monthly_pipeline_trend_chart(filtered), use_container_width=True)

    st.plotly_chart(top_opportunities_chart(filtered), use_container_width=True)

    _render_executive_brief(filtered)

    section_heading("Top Opportunities", "Compact ranked opportunities with the detailed dataframe retained.")
    _render_opportunities_table(filtered)
