import plotly.express as px
import pandas as pd


STAGE_ORDER = ["New", "Qualified", "Proposal", "Negotiation"]


def pipeline_by_stage_chart(df: pd.DataFrame):
    grouped = (
        df.groupby("stage", as_index=False)["deal_value"]
        .sum()
        .assign(stage=lambda d: pd.Categorical(d["stage"], categories=STAGE_ORDER, ordered=True))
        .sort_values("stage")
    )

    fig = px.bar(
        grouped,
        x="stage",
        y="deal_value",
        title="Pipeline Value by Stage",
        color="stage",
        color_discrete_sequence=["#23A6D5", "#00B894", "#F4B942", "#FF6B6B"],
        labels={"stage": "Stage", "deal_value": "Pipeline Value (USD)"},
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Space Grotesk, sans-serif", "color": "#E9F0F7"},
        margin={"l": 20, "r": 20, "t": 56, "b": 20},
        legend_title_text="",
    )
    fig.update_yaxes(tickprefix="$", separatethousands=True)
    return fig


def lead_score_distribution_chart(df: pd.DataFrame):
    bins = [0, 25, 50, 75, 101]
    labels = ["0-24", "25-49", "50-74", "75-100"]

    scored = df.copy()
    scored["score_bucket"] = pd.cut(
        scored["lead_score"], bins=bins, labels=labels, right=False, include_lowest=True
    )
    grouped = (
        scored.groupby("score_bucket", as_index=False, observed=False)["lead_id"]
        .count()
        .rename(columns={"lead_id": "lead_count"})
    )

    fig = px.bar(
        grouped,
        x="score_bucket",
        y="lead_count",
        title="Lead Score Distribution",
        color="score_bucket",
        color_discrete_sequence=["#44506A", "#3E7CB1", "#00B894", "#F4B942"],
        labels={"score_bucket": "Score Range", "lead_count": "Leads"},
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Space Grotesk, sans-serif", "color": "#E9F0F7"},
        margin={"l": 20, "r": 20, "t": 56, "b": 20},
        showlegend=False,
    )
    return fig
