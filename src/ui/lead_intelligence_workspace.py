from __future__ import annotations

import html

import pandas as pd
import streamlit as st

from src.copilot.analysis import CopilotCard, SalesCopilotAnalysis, generate_sales_copilot_analysis
from src.data.loader import load_leads
from src.outreach.generator import generate_outreach_for_lead
from src.scoring.engine import score_leads
from src.scoring.metrics import apply_pipeline_probability
from src.ui.components import badge, kpi_card, money, page_header, section_heading
from src.ui.theme import WORKSPACE_THEME_CSS
from src.workspace.lead_workspace import (
    enrich_workspace_leads,
    get_workspace_lead,
    recommend_workspace_actions,
    search_workspace_leads,
)


st.set_page_config(
    page_title="Lead Intelligence Workspace",
    page_icon="🧠",
    layout="wide",
)


def _money(value: float) -> str:
    return f"${value:,.0f}"


def _escape(value: object) -> str:
    return html.escape(str(value))


def _load_workspace_leads() -> pd.DataFrame:
    return enrich_workspace_leads(apply_pipeline_probability(score_leads(load_leads())))


def _lead_label(row: pd.Series) -> str:
    return (
        f"{row['company']} · {row['contact_name']} · Score {int(row['lead_score'])} · "
        f"{row['lead_label']} · {row['stage']} · {_money(float(row['deal_value']))}"
    )


def _render_field(label: str, value: object) -> str:
    return f"""
    <div class="field">
        <div class="field-label">{_escape(label)}</div>
        <div class="field-value">{_escape(value)}</div>
    </div>
    """


def _render_metric(label: str, value: str, progress: int | None = None) -> None:
    progress_markup = ""
    if progress is not None:
        progress_markup = f"""
        <div class="progress">
            <div class="progress-fill" style="width:{max(0, min(100, progress))}%;"></div>
        </div>
        """
    value_markup = value if str(value).startswith("<") else _escape(value)
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{_escape(label)}</div>
            <div class="metric-value">{value_markup}</div>
            {progress_markup}
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_intel_card(card: CopilotCard) -> None:
    st.markdown(
        f"""
        <div class="intel-card">
            <div class="intel-title">{_escape(card.title)}</div>
            <div class="intel-body">{_escape(card.answer)}</div>
            <div class="progress">
                <div class="progress-fill" style="width:{card.confidence}%;"></div>
            </div>
            <div class="muted" style="font-size:0.78rem; margin-top:0.35rem;">Confidence {card.confidence}%</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_overview(row: pd.Series) -> None:
    section_heading("Company Overview", "Account context, ownership, and acquisition source.")
    fields = [
        ("Company", row["company"]),
        ("Contact", row["contact_name"]),
        ("Industry", row["industry"]),
        ("Company Size", row["company_size"]),
        ("Lead Source", row["source"]),
        ("Owner", row["lead_owner"]),
    ]
    st.markdown(
        "<div class='workspace-panel'><div class='field-grid'>"
        + "".join(_render_field(label, value) for label, value in fields)
        + "</div></div>",
        unsafe_allow_html=True,
    )


def _render_deal_profile(row: pd.Series, analysis: SalesCopilotAnalysis) -> None:
    section_heading("Deal Profile", "Value, stage, urgency, score, probability, and timing.")
    cols = st.columns(4)
    with cols[0]:
        kpi_card("◈", money(float(row["deal_value"])), "Estimated Deal Value", "Open opportunity", "● Value", "neutral")
    with cols[1]:
        _render_metric("Pipeline Stage", badge(str(row["stage"])))
    with cols[2]:
        _render_metric("Urgency", badge(str(row["urgency_level"])))
    with cols[3]:
        _render_metric("Lead Label", badge(str(row["lead_label"])), int(row["lead_score"]))

    cols = st.columns(4)
    with cols[0]:
        _render_metric("Lead Score", f"{int(row['lead_score'])}/100", int(row["lead_score"]))
    with cols[1]:
        _render_metric("Deal Probability", f"{analysis.deal_probability}%", analysis.deal_probability)
    with cols[2]:
        _render_metric("Expected Close Timing", analysis.estimated_time_to_close)
    with cols[3]:
        _render_metric("Buying Intent", analysis.buying_intent)


def _card_by_title(analysis: SalesCopilotAnalysis, title: str) -> CopilotCard:
    return next(card for card in analysis.cards if card.title == title)


def _render_insights(analysis: SalesCopilotAnalysis) -> None:
    section_heading("AI-Style Insight Panel", "Reused deterministic Copilot guidance for the selected account.")
    cards = [
        _card_by_title(analysis, "Why this lead is valuable"),
        _card_by_title(analysis, "Biggest risks"),
        _card_by_title(analysis, "Next best action"),
        CopilotCard(
            "Suggested communication channel",
            f"Use {analysis.recommended_channel}. Follow up {analysis.follow_up_timing.lower()}.",
            analysis.confidence,
            "Channel is determined by stage, engagement, source, and pipeline age.",
        ),
        CopilotCard(
            "Buying intent",
            analysis.buying_intent,
            analysis.confidence,
            "Intent combines score, engagement, and stage maturity.",
        ),
    ]
    cols = st.columns(2)
    for index, card in enumerate(cards):
        with cols[index % 2]:
            _render_intel_card(card)


def _render_outreach(row: pd.Series) -> None:
    section_heading("Outreach Preview", "Executive-tone copy generated from existing deterministic outreach logic.")
    outreach = generate_outreach_for_lead(row, tone="Executive")
    st.markdown(
        f"""
        <div class="workspace-panel">
            <div class="outreach-box">
                <div class="outreach-title">Subject Line</div>
                <div class="outreach-copy">{_escape(outreach['subject_line'])}</div>
            </div>
            <div class="outreach-box">
                <div class="outreach-title">Short Email Preview</div>
                <div class="outreach-copy">{_escape(outreach['short_email'])}</div>
            </div>
            <div class="outreach-box">
                <div class="outreach-title">LinkedIn Message Preview</div>
                <div class="outreach-copy">{_escape(outreach['linkedin_message'])}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_actions(row: pd.Series, analysis: SalesCopilotAnalysis) -> None:
    section_heading("Recommended Actions", "Action plan based on score, urgency, stage, and risk signals.")
    actions = recommend_workspace_actions(row, analysis)
    action_markup = []
    for index, action in enumerate(actions, start=1):
        action_markup.append(
            f"""
            <div class="action-item">
                <span class="action-index">{index}</span>
                <div class="action-copy">{_escape(action)}</div>
            </div>
            """
        )
    st.markdown(
        "<div class='workspace-panel'>" + "".join(action_markup) + "</div>",
        unsafe_allow_html=True,
    )


def _render_selected_header(row: pd.Series, analysis: SalesCopilotAnalysis) -> None:
    st.markdown(
        f"""
        <div class="lead-summary">
            <h2>{_escape(row['company'])}</h2>
            <div class="muted">{_escape(row['contact_name'])} · {_escape(row['industry'])} · Owned by {_escape(row['lead_owner'])}</div>
            <div class="badge-row">
                {badge(row['lead_label'])}
                {badge(f"Score {int(row['lead_score'])}", "info")}
                {badge(row['stage'])}
                {badge(_money(float(row['deal_value'])), "neutral")}
                {badge(f"{analysis.deal_probability}% probability", "high")}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_lead_intelligence_workspace() -> None:
    st.markdown(WORKSPACE_THEME_CSS, unsafe_allow_html=True)

    leads = _load_workspace_leads()
    page_header(
        "Lead Intelligence Workspace",
        "Search, inspect, prioritize, and act on pipeline opportunities from a focused CRM command center.",
        len(leads),
        "🧠",
    )
    left_col, right_col = st.columns([0.36, 0.64], gap="large")

    with left_col:
        section_heading("Lead List", "Search by company, contact, industry, or owner.")
        query = st.text_input("Search leads", placeholder="Company, contact, industry, or owner")
        filtered = search_workspace_leads(leads, query)
        st.caption(f"{len(filtered)} leads found")

        if filtered.empty:
            st.info("No leads match the current search.")
            return

        options = filtered["lead_id"].tolist()
        selected_lead_id = st.radio(
            "Select a lead",
            options=options,
            format_func=lambda lead_id: _lead_label(get_workspace_lead(filtered, lead_id)),
            label_visibility="collapsed",
        )

    selected = get_workspace_lead(leads, selected_lead_id)
    analysis = generate_sales_copilot_analysis(selected)

    with right_col:
        _render_selected_header(selected, analysis)
        overview_col, action_col = st.columns([0.95, 1.05])
        with overview_col:
            _render_overview(selected)
        with action_col:
            _render_actions(selected, analysis)
        _render_deal_profile(selected, analysis)
        _render_insights(analysis)
        _render_outreach(selected)
