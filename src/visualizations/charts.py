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
