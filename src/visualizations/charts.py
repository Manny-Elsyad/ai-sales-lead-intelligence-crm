import plotly.express as px
import pandas as pd


STAGE_ORDER = ["New", "Qualified", "Proposal", "Negotiation"]
CRM_STAGE_ORDER = ["New", "Contacted", "Qualified", "Proposal", "Won", "Lost"]
EXECUTIVE_COLORS = ["#D6A94A", "#2CB67D", "#4D96FF", "#FF7A59", "#8B8CF6", "#24C6DC", "#A3E635"]


def _executive_layout(fig, showlegend: bool = True):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Space Grotesk, sans-serif", "color": "#F5F1E8"},
        margin={"l": 24, "r": 24, "t": 58, "b": 28},
        legend_title_text="",
        showlegend=showlegend,
    )
    fig.update_xaxes(gridcolor="rgba(245,241,232,0.08)", zerolinecolor="rgba(245,241,232,0.12)")
    fig.update_yaxes(gridcolor="rgba(245,241,232,0.08)", zerolinecolor="rgba(245,241,232,0.12)")
    return fig


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


def pipeline_funnel_chart(df: pd.DataFrame):
    grouped = (
        df.groupby("crm_stage", as_index=False)["lead_id"]
        .count()
        .rename(columns={"lead_id": "lead_count"})
    )
    grouped["crm_stage"] = pd.Categorical(
        grouped["crm_stage"], categories=CRM_STAGE_ORDER, ordered=True
    )
    grouped = grouped.sort_values("crm_stage")

    fig = px.funnel(
        grouped,
        y="crm_stage",
        x="lead_count",
        title="CRM Pipeline Funnel",
        color="crm_stage",
        color_discrete_sequence=["#6C8EEF", "#23A6D5", "#00B894", "#F4B942", "#5CD67C", "#E76F51"],
        labels={"crm_stage": "Stage", "lead_count": "Lead Count"},
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Space Grotesk, sans-serif", "color": "#E9F0F7"},
        margin={"l": 20, "r": 20, "t": 56, "b": 20},
        showlegend=False,
    )
    return fig


def executive_sales_funnel_chart(df: pd.DataFrame):
    grouped = (
        df.groupby("stage", as_index=False)
        .agg(lead_count=("lead_id", "count"), deal_value=("deal_value", "sum"))
        .assign(stage=lambda d: pd.Categorical(d["stage"], categories=STAGE_ORDER, ordered=True))
        .sort_values("stage")
    )

    fig = px.funnel(
        grouped,
        y="stage",
        x="deal_value",
        title="Sales Funnel",
        color="stage",
        color_discrete_sequence=EXECUTIVE_COLORS,
        labels={"stage": "Stage", "deal_value": "Pipeline Value"},
        hover_data={"lead_count": True, "deal_value": ":$,.0f"},
    )
    fig.update_traces(texttemplate="$%{x:,.0f}")
    fig.update_xaxes(tickprefix="$", separatethousands=True)
    return _executive_layout(fig, showlegend=False)


def revenue_by_industry_chart(df: pd.DataFrame):
    grouped = (
        df.groupby("industry", as_index=False)["weighted_value"]
        .sum()
        .sort_values("weighted_value", ascending=False)
    )
    fig = px.bar(
        grouped,
        x="weighted_value",
        y="industry",
        orientation="h",
        title="Revenue by Industry",
        color="industry",
        color_discrete_sequence=EXECUTIVE_COLORS,
        labels={"weighted_value": "Expected Revenue", "industry": "Industry"},
    )
    fig.update_xaxes(tickprefix="$", separatethousands=True)
    fig.update_yaxes(categoryorder="total ascending")
    return _executive_layout(fig, showlegend=False)


def revenue_by_source_chart(df: pd.DataFrame):
    grouped = (
        df.groupby("source", as_index=False)["weighted_value"]
        .sum()
        .sort_values("weighted_value", ascending=False)
    )
    fig = px.bar(
        grouped,
        x="source",
        y="weighted_value",
        title="Revenue by Lead Source",
        color="source",
        color_discrete_sequence=EXECUTIVE_COLORS,
        labels={"source": "Lead Source", "weighted_value": "Expected Revenue"},
    )
    fig.update_yaxes(tickprefix="$", separatethousands=True)
    return _executive_layout(fig, showlegend=False)


def pipeline_stage_breakdown_chart(df: pd.DataFrame):
    grouped = (
        df.groupby("stage", as_index=False)["deal_value"]
        .sum()
        .assign(stage=lambda d: pd.Categorical(d["stage"], categories=STAGE_ORDER, ordered=True))
        .sort_values("stage")
    )
    fig = px.pie(
        grouped,
        names="stage",
        values="deal_value",
        title="Pipeline Stage Breakdown",
        color_discrete_sequence=EXECUTIVE_COLORS,
        hole=0.46,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    return _executive_layout(fig)


def executive_lead_score_distribution_chart(df: pd.DataFrame):
    bins = [0, 50, 65, 75, 85, 101]
    labels = ["0-49", "50-64", "65-74", "75-84", "85-100"]

    scored = df.copy()
    scored["score_bucket"] = pd.cut(
        scored["lead_score"], bins=bins, labels=labels, right=False, include_lowest=True
    )
    grouped = (
        scored.groupby("score_bucket", as_index=False, observed=False)
        .agg(lead_count=("lead_id", "count"), pipeline=("deal_value", "sum"))
    )

    fig = px.bar(
        grouped,
        x="score_bucket",
        y="lead_count",
        title="Lead Score Distribution",
        color="score_bucket",
        color_discrete_sequence=EXECUTIVE_COLORS,
        labels={"score_bucket": "Lead Score", "lead_count": "Lead Count"},
        hover_data={"pipeline": ":$,.0f"},
    )
    return _executive_layout(fig, showlegend=False)


def monthly_pipeline_trend_chart(df: pd.DataFrame):
    trended = df.copy()
    trended["pipeline_month"] = trended["last_contact_date"].dt.to_period("M").dt.to_timestamp()
    grouped = (
        trended.groupby("pipeline_month", as_index=False)
        .agg(deal_value=("deal_value", "sum"), weighted_value=("weighted_value", "sum"))
        .sort_values("pipeline_month")
    )
    long_df = grouped.melt(
        id_vars="pipeline_month",
        value_vars=["deal_value", "weighted_value"],
        var_name="metric",
        value_name="value",
    )
    long_df["metric"] = long_df["metric"].map(
        {"deal_value": "Total Pipeline", "weighted_value": "Expected Revenue"}
    )

    fig = px.line(
        long_df,
        x="pipeline_month",
        y="value",
        color="metric",
        markers=True,
        title="Monthly Pipeline Trend",
        color_discrete_sequence=["#D6A94A", "#2CB67D"],
        labels={"pipeline_month": "Month", "value": "Value", "metric": ""},
    )
    fig.update_yaxes(tickprefix="$", separatethousands=True)
    return _executive_layout(fig)


def top_opportunities_chart(df: pd.DataFrame):
    chart_df = df.sort_values(["deal_value", "lead_score"], ascending=False).head(10)
    fig = px.bar(
        chart_df,
        x="deal_value",
        y="company",
        orientation="h",
        title="Top 10 Highest Value Opportunities",
        color="lead_score",
        color_continuous_scale=["#4D96FF", "#2CB67D", "#D6A94A"],
        labels={"deal_value": "Deal Value", "company": "Company", "lead_score": "Lead Score"},
        hover_data={"stage": True, "lead_owner": True, "weighted_value": ":$,.0f"},
    )
    fig.update_xaxes(tickprefix="$", separatethousands=True)
    fig.update_yaxes(categoryorder="total ascending")
    return _executive_layout(fig)
