import pandas as pd
import streamlit as st

from src.analytics.executive import executive_insights, executive_kpis, executive_summary, top_opportunities
from src.data.loader import load_leads
from src.scoring.engine import score_leads
from src.scoring.metrics import apply_pipeline_probability
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
    st.sidebar.header("Executive Filters")

    industries = st.sidebar.multiselect(
        "Industry",
        options=sorted(df["industry"].unique()),
        default=sorted(df["industry"].unique()),
    )
    stages = st.sidebar.multiselect(
        "Pipeline Stage",
        options=sorted(df["stage"].unique()),
        default=sorted(df["stage"].unique()),
    )
    owners = st.sidebar.multiselect(
        "Lead Owner",
        options=sorted(df["lead_owner"].unique()),
        default=sorted(df["lead_owner"].unique()),
    )
    sources = st.sidebar.multiselect(
        "Lead Source",
        options=sorted(df["source"].unique()),
        default=sorted(df["source"].unique()),
    )
    regions = st.sidebar.multiselect(
        "Region",
        options=sorted(df["region"].unique()),
        default=sorted(df["region"].unique()),
    )
    min_score, max_score = st.sidebar.slider(
        "Lead Score Range", min_value=0, max_value=100, value=(50, 100)
    )
    min_deal_value = st.sidebar.slider(
        "Minimum Deal Value",
        min_value=0,
        max_value=int(df["deal_value"].max()),
        value=0,
        step=5000,
        format="$%d",
    )

    return df[
        (df["industry"].isin(industries))
        & (df["stage"].isin(stages))
        & (df["lead_owner"].isin(owners))
        & (df["source"].isin(sources))
        & (df["region"].isin(regions))
        & (df["lead_score"].between(min_score, max_score))
        & (df["deal_value"] >= min_deal_value)
    ].copy()


def _render_kpi(label: str, value: str, caption: str) -> None:
    st.markdown(
        f"""
        <div class="executive-kpi">
            <div class="label">{label}</div>
            <div class="value">{value}</div>
            <div class="caption">{caption}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_kpis(kpis: dict[str, float]) -> None:
    first_row = st.columns(4)
    second_row = st.columns(4)

    with first_row[0]:
        _render_kpi("Total Pipeline Value", _money(kpis["total_pipeline_value"]), "Open opportunity value")
    with first_row[1]:
        _render_kpi("Expected Revenue", _money(kpis["expected_revenue"]), "Probability-weighted forecast")
    with first_row[2]:
        _render_kpi("Average Deal Size", _money(kpis["average_deal_size"]), "Mean opportunity value")
    with first_row[3]:
        _render_kpi("Win Rate", f"{kpis['win_rate']:.1%}", "Weighted conversion outlook")

    with second_row[0]:
        _render_kpi("Qualified Leads", f"{int(kpis['qualified_leads']):,}", "Qualified stage or later")
    with second_row[1]:
        _render_kpi("Average Lead Score", f"{kpis['average_lead_score']:.1f}", "Fit, engagement, and urgency")
    with second_row[2]:
        _render_kpi("Hot Leads", f"{int(kpis['hot_leads']):,}", "Score of 75 or higher")
    with second_row[3]:
        _render_kpi("Pipeline Velocity", _money(kpis["pipeline_velocity"]), "Expected revenue per pipeline day")


def _render_insights(df: pd.DataFrame) -> None:
    st.subheader("Business Insights")
    st.markdown("<div class='executive-panel'>", unsafe_allow_html=True)
    for insight in executive_insights(df):
        st.markdown(
            f"""
            <div class="insight-row">
                <div class="insight-title">{insight.title} · {insight.priority} Priority</div>
                <div class="insight-value">{insight.value}</div>
                <div class="insight-detail">{insight.detail}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)


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
    st.markdown(
        """
        <div class="executive-header">
            <div class="executive-eyebrow">Morning Revenue Command Center</div>
            <h1>Executive Analytics</h1>
            <p>Board-ready pipeline health, forecast quality, sales risk, and account priorities for VP-level operating rhythm.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    leads = apply_pipeline_probability(score_leads(load_leads()))
    filtered = _apply_executive_filters(leads)
    kpis = executive_kpis(filtered)

    st.caption(f"Showing {len(filtered):,} opportunities after filters.")
    _render_kpis(kpis)

    if filtered.empty:
        st.warning("No opportunities match the current filters. Broaden the filters to restore executive analytics.")
        _render_insights(filtered)
        _render_summary(filtered)
        return

    st.subheader("Visualizations")
    funnel_col, industry_col = st.columns([1, 1])
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

    insight_col, summary_col = st.columns([0.95, 1.05])
    with insight_col:
        _render_insights(filtered)
    with summary_col:
        _render_summary(filtered)

    st.subheader("Top Opportunities")
    _render_opportunities_table(filtered)
