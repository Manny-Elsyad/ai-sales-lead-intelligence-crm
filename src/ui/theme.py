DARK_THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&display=swap');

html, body, [class*="css"]  {
    font-family: 'Space Grotesk', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 20%, rgba(35, 166, 213, 0.20), transparent 28%),
        radial-gradient(circle at 90% 10%, rgba(0, 184, 148, 0.18), transparent 30%),
        linear-gradient(135deg, #0F172A 0%, #111827 45%, #0B1020 100%);
    color: #E9F0F7;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(10, 16, 34, 0.95), rgba(14, 25, 49, 0.92));
    border-right: 1px solid rgba(255, 255, 255, 0.08);
}

.block-container {
    padding-top: 1.5rem;
}

.hero {
    background: linear-gradient(120deg, rgba(18, 34, 58, 0.9), rgba(25, 47, 76, 0.75));
    border: 1px solid rgba(255, 255, 255, 0.09);
    border-radius: 18px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
}

.kpi-card {
    background: linear-gradient(150deg, rgba(15, 26, 48, 0.90), rgba(20, 36, 65, 0.86));
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 0.7rem;
}

[data-testid="stDataFrame"] {
    border: 1px solid rgba(255, 255, 255, 0.10);
    border-radius: 14px;
    overflow: hidden;
}

.stPlotlyChart {
    border: 1px solid rgba(255, 255, 255, 0.10);
    border-radius: 14px;
    background: rgba(13, 24, 45, 0.75);
    padding: 0.35rem;
}

.pipeline-stage {
    background: linear-gradient(150deg, rgba(12, 22, 41, 0.95), rgba(19, 33, 59, 0.90));
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 0.6rem;
    margin-bottom: 0.5rem;
}

.lead-card {
    background: rgba(21, 37, 67, 0.82);
    border: 1px solid rgba(255, 255, 255, 0.10);
    border-left: 4px solid #23A6D5;
    border-radius: 10px;
    padding: 0.55rem;
    margin: 0.35rem 0;
}
</style>
"""


EXECUTIVE_THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&display=swap');

html, body, [class*="css"]  {
    font-family: 'Space Grotesk', sans-serif;
}

.stApp {
    background:
        linear-gradient(135deg, #111417 0%, #171A1F 48%, #101215 100%);
    color: #F5F1E8;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(19, 21, 25, 0.98), rgba(34, 32, 28, 0.94));
    border-right: 1px solid rgba(214, 169, 74, 0.20);
}

.block-container {
    padding-top: 1.4rem;
    padding-bottom: 2rem;
    max-width: 1440px;
}

.executive-header {
    border-bottom: 1px solid rgba(214, 169, 74, 0.28);
    padding: 0.2rem 0 1rem 0;
    margin-bottom: 1rem;
}

.executive-eyebrow {
    color: #D6A94A;
    font-size: 0.78rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-weight: 700;
}

.executive-header h1 {
    font-size: 2.35rem;
    margin: 0.15rem 0 0.2rem;
    letter-spacing: 0;
}

.executive-header p {
    color: rgba(245, 241, 232, 0.78);
    margin: 0;
    max-width: 820px;
}

.executive-kpi {
    min-height: 132px;
    background: linear-gradient(150deg, rgba(36, 38, 42, 0.98), rgba(22, 24, 28, 0.96));
    border: 1px solid rgba(214, 169, 74, 0.22);
    border-radius: 8px;
    padding: 1rem;
    box-shadow: 0 16px 34px rgba(0, 0, 0, 0.22);
}

.executive-kpi .label {
    color: rgba(245, 241, 232, 0.66);
    font-size: 0.82rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

.executive-kpi .value {
    color: #F5F1E8;
    font-size: 1.75rem;
    font-weight: 700;
    margin-top: 0.4rem;
    line-height: 1.15;
}

.executive-kpi .caption {
    color: rgba(245, 241, 232, 0.58);
    font-size: 0.82rem;
    margin-top: 0.45rem;
}

.executive-panel {
    background: rgba(24, 26, 30, 0.92);
    border: 1px solid rgba(245, 241, 232, 0.10);
    border-radius: 8px;
    padding: 1rem;
}

.insight-row {
    border-bottom: 1px solid rgba(245, 241, 232, 0.10);
    padding: 0.75rem 0;
}

.insight-row:last-child {
    border-bottom: 0;
}

.insight-title {
    color: rgba(245, 241, 232, 0.68);
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

.insight-value {
    color: #F5F1E8;
    font-size: 1.08rem;
    font-weight: 700;
    margin-top: 0.1rem;
}

.insight-detail {
    color: rgba(245, 241, 232, 0.68);
    font-size: 0.9rem;
    margin-top: 0.15rem;
}

.stPlotlyChart {
    border: 1px solid rgba(245, 241, 232, 0.10);
    border-radius: 8px;
    background: rgba(22, 24, 28, 0.92);
    padding: 0.35rem;
}

[data-testid="stDataFrame"] {
    border: 1px solid rgba(245, 241, 232, 0.12);
    border-radius: 8px;
    overflow: hidden;
}
</style>
"""
