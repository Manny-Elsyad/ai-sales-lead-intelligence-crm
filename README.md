# AI Sales Lead Intelligence CRM (Sprint 1)

Portfolio-quality Streamlit MVP for B2B lead management and sales analytics.

## What is included

- Executive dashboard with premium dark theme
- Sidebar filters for industry, stage, owner, and lead score
- KPI cards for leads, pipeline value, weighted pipeline, and score quality
- Interactive lead table (read-only editor)
- Plotly pipeline chart
- Realistic fictional B2B lead dataset
- Test suite with `pytest`

## Project structure

```text
.
├── app.py
├── streamlit_app.py
├── data/
│   └── leads.csv
├── src/
│   ├── data/
│   ├── scoring/
│   ├── outreach/
│   ├── ui/
│   └── visualizations/
└── tests/
```

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Run tests

```bash
pytest
```

## Notes

- All leads are fictional and intended for portfolio demonstration.
- AI-powered outreach is intentionally out of scope for Sprint 1.
