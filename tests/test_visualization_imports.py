import importlib

from src.data.loader import load_leads
from src.scoring.engine import score_leads
from src.scoring.metrics import apply_pipeline_probability
from src.visualizations import charts


def test_dashboard_modules_import_without_eager_plotly_import():
    importlib.import_module("src.ui.dashboard")
    importlib.import_module("src.ui.executive_analytics")


def test_chart_function_falls_back_when_plotly_unavailable(monkeypatch):
    real_import_module = charts.import_module

    def fake_import_module(name):
        if name == "plotly.express":
            raise ModuleNotFoundError("No module named 'plotly'")
        return real_import_module(name)

    monkeypatch.setattr(charts, "import_module", fake_import_module)
    monkeypatch.setattr(charts, "_chart_unavailable", lambda chart_name, error: None)

    df = apply_pipeline_probability(score_leads(load_leads()))

    assert charts.pipeline_by_stage_chart(df) is None
