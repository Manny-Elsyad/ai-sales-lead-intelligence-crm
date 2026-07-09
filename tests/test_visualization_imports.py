import importlib

import plotly.graph_objects as go

from src.data.loader import load_leads
from src.scoring.engine import score_leads
from src.scoring.metrics import apply_pipeline_probability
from src.visualizations.charts import pipeline_by_stage_chart


def test_dashboard_modules_import_with_plotly_available():
    importlib.import_module("src.ui.dashboard")
    importlib.import_module("src.ui.executive_analytics")


def test_chart_function_returns_interactive_plotly_figure():
    df = apply_pipeline_probability(score_leads(load_leads()))

    fig = pipeline_by_stage_chart(df)

    assert isinstance(fig, go.Figure)
    assert len(fig.data) > 0
