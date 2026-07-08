from __future__ import annotations

import html
from datetime import datetime
from zoneinfo import ZoneInfo

import streamlit as st


STATUS_VARIANTS = {
    "Hot Lead": "hot",
    "Warm Lead": "warm",
    "Cold Lead": "cold",
    "New": "new",
    "Contacted": "contacted",
    "Qualified": "qualified",
    "Proposal": "proposal",
    "Negotiation": "negotiation",
    "Won": "won",
    "Lost": "lost",
    "High": "high",
    "Medium": "medium",
    "Low": "low",
}


def escape(value: object) -> str:
    return html.escape(str(value))


def money(value: float) -> str:
    return f"${value:,.0f}"


def last_updated_label() -> str:
    now = datetime.now(ZoneInfo("America/New_York"))
    return now.strftime("%b %-d, %Y · %-I:%M %p ET")


def badge(label: object, variant: str | None = None) -> str:
    variant_name = variant or STATUS_VARIANTS.get(str(label), "neutral")
    return f"<span class='saas-badge saas-badge-{escape(variant_name)}'>{escape(label)}</span>"


def progress_bar(value: float, class_name: str = "") -> str:
    clamped = max(0, min(100, int(round(value))))
    return (
        f"<div class='saas-progress {escape(class_name)}'>"
        f"<div class='saas-progress-fill' style='width:{clamped}%;'></div>"
        "</div>"
    )


def page_header(title: str, subtitle: str, record_count: int, icon: str = "◆") -> None:
    st.markdown(
        f"""
        <div class="saas-header">
            <div class="saas-header-main">
                <div class="saas-header-icon">{escape(icon)}</div>
                <div>
                    <div class="saas-eyebrow">Revenue Intelligence</div>
                    <h1>{escape(title)}</h1>
                    <p>{escape(subtitle)}</p>
                </div>
            </div>
            <div class="saas-header-meta">
                <span>{escape(last_updated_label())}</span>
                <span>{record_count:,} records</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(
    icon: str,
    metric: str,
    label: str,
    description: str,
    trend: str = "● Stable",
    status: str = "neutral",
    progress: float | None = None,
) -> None:
    progress_markup = progress_bar(progress) if progress is not None else ""
    st.markdown(
        f"""
        <div class="saas-kpi saas-kpi-{escape(status)}">
            <div class="saas-kpi-top">
                <span class="saas-kpi-icon">{escape(icon)}</span>
                <span class="saas-trend saas-trend-{escape(status)}">{escape(trend)}</span>
            </div>
            <div class="saas-kpi-metric">{escape(metric)}</div>
            <div class="saas-kpi-label">{escape(label)}</div>
            <div class="saas-kpi-description">{escape(description)}</div>
            {progress_markup}
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_heading(title: str, subtitle: str = "") -> None:
    subtitle_markup = f"<p>{escape(subtitle)}</p>" if subtitle else ""
    st.markdown(
        f"""
        <div class="saas-section-heading">
            <h2>{escape(title)}</h2>
            {subtitle_markup}
        </div>
        """,
        unsafe_allow_html=True,
    )


def card(title: str, body: str, icon: str = "◆", variant: str = "neutral") -> None:
    st.markdown(
        f"""
        <div class="saas-card saas-card-{escape(variant)}">
            <div class="saas-card-title">{escape(icon)} {escape(title)}</div>
            <div class="saas-card-body">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def sidebar_filter_header(active_count: int) -> None:
    st.sidebar.markdown(
        f"""
        <div class="sidebar-filter-header">
            <span>⚙ Filters</span>
            {badge(f"{active_count} active", "info")}
        </div>
        """,
        unsafe_allow_html=True,
    )


def lead_score_pill(score: int, label: str) -> str:
    return (
        f"<div class='score-pill'>{badge(label)}"
        f"<strong>{score}</strong>{progress_bar(score)}</div>"
    )
