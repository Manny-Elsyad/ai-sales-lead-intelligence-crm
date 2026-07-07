from __future__ import annotations

import pandas as pd
import streamlit as st

from src.copilot.analysis import SalesCopilotAnalysis, generate_sales_copilot_analysis
from src.data.loader import load_leads
from src.scoring.engine import score_leads
from src.scoring.metrics import apply_pipeline_probability
from src.ui.theme import COPILOT_THEME_CSS


st.set_page_config(
    page_title="AI Sales Copilot",
    page_icon="🤖",
    layout="wide",
)


def _money(value: float) -> str:
    return f"${value:,.0f}"


def _load_scored_leads() -> pd.DataFrame:
    return apply_pipeline_probability(score_leads(load_leads()))


def _lead_options(df: pd.DataFrame) -> list[str]:
    sorted_df = df.sort_values(["lead_score", "deal_value"], ascending=[False, False])
    return [
        f"{row.lead_id} | {row.company} | {row.stage} | ${row.deal_value:,.0f} | Score {int(row.lead_score)}"
        for row in sorted_df.itertuples(index=False)
    ]


def _selected_lead(df: pd.DataFrame, selected_label: str) -> pd.Series:
    lead_id = selected_label.split(" | ")[0]
    return df.loc[df["lead_id"] == lead_id].iloc[0]


def _render_confidence(confidence: int) -> None:
    st.markdown(
        f"""
        <div class="confidence">
            <div class="confidence-fill" style="width:{confidence}%;"></div>
        </div>
        <div class="confidence-label">Confidence {confidence}%</div>
        """,
        unsafe_allow_html=True,
    )


def _render_signal(label: str, value: str, confidence: int | None = None) -> None:
    confidence_markup = ""
    if confidence is not None:
        confidence_markup = f"""
        <div class="confidence">
            <div class="confidence-fill" style="width:{confidence}%;"></div>
        </div>
        <div class="confidence-label">Confidence {confidence}%</div>
        """
    st.markdown(
        f"""
        <div class="signal-card">
            <div class="signal-label">{label}</div>
            <div class="signal-value">{value}</div>
            {confidence_markup}
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_ai_card(title: str, answer: str, rationale: str, confidence: int) -> None:
    st.markdown(
        f"""
        <div class="ai-card">
            <div class="ai-card-title">{title}</div>
            <div class="ai-card-answer">{answer}</div>
            <div class="ai-card-rationale">{rationale}</div>
            <div class="confidence">
                <div class="confidence-fill" style="width:{confidence}%;"></div>
            </div>
            <div class="confidence-label">Confidence {confidence}%</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_lead_snapshot(row: pd.Series) -> None:
    st.subheader("Lead Snapshot")
    cols = st.columns(5)
    with cols[0]:
        _render_signal("Deal Value", _money(float(row["deal_value"])))
    with cols[1]:
        _render_signal("Stage", str(row["stage"]))
    with cols[2]:
        _render_signal("Lead Score", f"{int(row['lead_score'])}")
    with cols[3]:
        _render_signal("Engagement", f"{int(row['engagement_score'])}")
    with cols[4]:
        _render_signal("Days in Pipeline", f"{int(row['days_in_pipeline'])}")


def _render_copilot_signals(analysis: SalesCopilotAnalysis) -> None:
    st.subheader("Copilot Signals")
    cols = st.columns(5)
    with cols[0]:
        _render_signal("Buying Intent", analysis.buying_intent, analysis.confidence)
    with cols[1]:
        _render_signal("Deal Probability", f"{analysis.deal_probability}%", analysis.confidence)
    with cols[2]:
        _render_signal("Time to Close", analysis.estimated_time_to_close)
    with cols[3]:
        _render_signal("Follow-up Timing", analysis.follow_up_timing)
    with cols[4]:
        _render_signal("Channel", analysis.recommended_channel)


def _render_cards(analysis: SalesCopilotAnalysis) -> None:
    st.subheader("AI Analysis")
    card_columns = st.columns(2)
    for index, card in enumerate(analysis.cards):
        with card_columns[index % 2]:
            _render_ai_card(card.title, card.answer, card.rationale, card.confidence)


def _render_agenda(analysis: SalesCopilotAnalysis) -> None:
    st.subheader("Suggested Meeting Agenda")
    st.markdown("<div class='copilot-panel'>", unsafe_allow_html=True)
    for item in analysis.meeting_agenda:
        st.markdown(f"- {item}")
    st.markdown("</div>", unsafe_allow_html=True)


def _render_objections(analysis: SalesCopilotAnalysis) -> None:
    st.subheader("Objection Handling")
    st.markdown("<div class='copilot-panel'>", unsafe_allow_html=True)
    for objection in analysis.objections:
        st.markdown(
            f"""
            <div class="objection-row">
                <div class="objection-title">{objection.objection}</div>
                <div class="objection-response">{objection.response}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        _render_confidence(objection.confidence)
    st.markdown("</div>", unsafe_allow_html=True)


def render_ai_sales_copilot() -> None:
    st.markdown(COPILOT_THEME_CSS, unsafe_allow_html=True)
    st.markdown(
        """
        <div class="copilot-header">
            <div class="copilot-eyebrow">Deterministic AI-Style Guidance</div>
            <h1>AI Sales Copilot</h1>
            <p>Lead-level sales intelligence with rule-based recommendations, confidence indicators, and next-step coaching.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    leads = _load_scored_leads()
    selected_label = st.sidebar.selectbox("Select Lead", options=_lead_options(leads), index=0)
    selected = _selected_lead(leads, selected_label)
    analysis = generate_sales_copilot_analysis(selected)

    st.caption(
        f"Selected {analysis.company} ({analysis.lead_id}) · {selected['industry']} · {selected['lead_owner']}"
    )
    _render_lead_snapshot(selected)
    _render_copilot_signals(analysis)

    recommendation_col, context_col = st.columns([0.9, 1.1])
    with recommendation_col:
        _render_ai_card(
            "Executive recommendation",
            analysis.executive_recommendation,
            "Recommendation is deterministic and based on score, probability, deal size, stage, and urgency.",
            analysis.confidence,
        )
    with context_col:
        _render_ai_card(
            "Recommended communication plan",
            f"Use {analysis.recommended_channel}. Follow up {analysis.follow_up_timing.lower()}. Estimated close window: {analysis.estimated_time_to_close}.",
            "Channel and timing adjust instantly when a different lead is selected.",
            analysis.confidence,
        )

    _render_cards(analysis)

    agenda_col, objection_col = st.columns([0.9, 1.1])
    with agenda_col:
        _render_agenda(analysis)
    with objection_col:
        _render_objections(analysis)
