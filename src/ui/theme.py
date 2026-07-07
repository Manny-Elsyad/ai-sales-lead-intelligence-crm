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
</style>
"""
