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


COPILOT_THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&display=swap');

html, body, [class*="css"]  {
    font-family: 'Space Grotesk', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #101318 0%, #181B22 52%, #0F1217 100%);
    color: #F4F7FB;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(13, 17, 23, 0.98), rgba(20, 25, 33, 0.96));
    border-right: 1px solid rgba(73, 214, 194, 0.18);
}

.block-container {
    padding-top: 1.3rem;
    padding-bottom: 2rem;
    max-width: 1380px;
}

.copilot-header {
    border-bottom: 1px solid rgba(73, 214, 194, 0.24);
    padding: 0.2rem 0 1rem 0;
    margin-bottom: 1rem;
}

.copilot-eyebrow {
    color: #49D6C2;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.copilot-header h1 {
    font-size: 2.3rem;
    margin: 0.15rem 0 0.2rem;
    letter-spacing: 0;
}

.copilot-header p {
    color: rgba(244, 247, 251, 0.72);
    margin: 0;
    max-width: 840px;
}

.ai-card {
    min-height: 188px;
    background: linear-gradient(150deg, rgba(26, 31, 40, 0.98), rgba(17, 21, 29, 0.96));
    border: 1px solid rgba(73, 214, 194, 0.20);
    border-radius: 8px;
    padding: 1rem;
    box-shadow: 0 18px 40px rgba(0, 0, 0, 0.22);
}

.ai-card-title {
    color: rgba(244, 247, 251, 0.72);
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

.ai-card-answer {
    color: #F4F7FB;
    font-size: 1rem;
    line-height: 1.48;
    margin-top: 0.55rem;
}

.ai-card-rationale {
    color: rgba(244, 247, 251, 0.58);
    font-size: 0.84rem;
    margin-top: 0.7rem;
}

.confidence {
    margin-top: 0.85rem;
    height: 8px;
    background: rgba(244, 247, 251, 0.10);
    border-radius: 999px;
    overflow: hidden;
}

.confidence-fill {
    height: 8px;
    background: linear-gradient(90deg, #4D96FF, #49D6C2);
    border-radius: 999px;
}

.confidence-label {
    color: rgba(244, 247, 251, 0.64);
    font-size: 0.78rem;
    margin-top: 0.35rem;
}

.signal-card {
    background: rgba(22, 27, 36, 0.92);
    border: 1px solid rgba(244, 247, 251, 0.10);
    border-radius: 8px;
    padding: 0.9rem;
    min-height: 100px;
}

.signal-label {
    color: rgba(244, 247, 251, 0.58);
    font-size: 0.76rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

.signal-value {
    color: #F4F7FB;
    font-size: 1.35rem;
    font-weight: 700;
    margin-top: 0.35rem;
}

.copilot-panel {
    background: rgba(22, 27, 36, 0.92);
    border: 1px solid rgba(244, 247, 251, 0.10);
    border-radius: 8px;
    padding: 1rem;
}

.objection-row {
    border-bottom: 1px solid rgba(244, 247, 251, 0.10);
    padding: 0.8rem 0;
}

.objection-row:last-child {
    border-bottom: 0;
}

.objection-title {
    color: #49D6C2;
    font-weight: 700;
}

.objection-response {
    color: rgba(244, 247, 251, 0.72);
    margin-top: 0.18rem;
}
</style>
"""


WORKSPACE_THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&display=swap');

html, body, [class*="css"]  {
    font-family: 'Space Grotesk', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0E1117 0%, #151A22 48%, #0B0F15 100%);
    color: #EEF4F8;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(12, 16, 23, 0.98), rgba(18, 23, 32, 0.96));
    border-right: 1px solid rgba(89, 164, 255, 0.16);
}

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

.workspace-header {
    border-bottom: 1px solid rgba(89, 164, 255, 0.20);
    padding: 0.2rem 0 1rem;
    margin-bottom: 1rem;
}

.workspace-eyebrow {
    color: #59A4FF;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.workspace-header h1 {
    font-size: 2.25rem;
    margin: 0.15rem 0 0.2rem;
    letter-spacing: 0;
}

.workspace-header p {
    color: rgba(238, 244, 248, 0.72);
    margin: 0;
    max-width: 900px;
}

.workspace-panel {
    background: rgba(21, 27, 37, 0.94);
    border: 1px solid rgba(238, 244, 248, 0.10);
    border-radius: 8px;
    padding: 1rem;
}

.lead-summary {
    background: linear-gradient(150deg, rgba(31, 39, 52, 0.98), rgba(18, 23, 32, 0.98));
    border: 1px solid rgba(89, 164, 255, 0.18);
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 0.9rem;
}

.lead-summary h2 {
    margin: 0 0 0.25rem;
    font-size: 1.45rem;
}

.muted {
    color: rgba(238, 244, 248, 0.62);
}

.badge-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.45rem;
    margin-top: 0.75rem;
}

.badge {
    border: 1px solid rgba(238, 244, 248, 0.12);
    border-radius: 999px;
    color: #EEF4F8;
    background: rgba(89, 164, 255, 0.12);
    padding: 0.28rem 0.58rem;
    font-size: 0.78rem;
}

.metric-card {
    min-height: 104px;
    background: rgba(17, 22, 31, 0.94);
    border: 1px solid rgba(238, 244, 248, 0.10);
    border-radius: 8px;
    padding: 0.8rem;
}

.metric-label {
    color: rgba(238, 244, 248, 0.58);
    font-size: 0.74rem;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

.metric-value {
    color: #EEF4F8;
    font-size: 1.22rem;
    font-weight: 700;
    margin-top: 0.35rem;
}

.progress {
    height: 8px;
    background: rgba(238, 244, 248, 0.10);
    border-radius: 999px;
    overflow: hidden;
    margin-top: 0.65rem;
}

.progress-fill {
    height: 8px;
    background: linear-gradient(90deg, #59A4FF, #55D6BE);
    border-radius: 999px;
}

.intel-card {
    background: rgba(17, 22, 31, 0.94);
    border: 1px solid rgba(85, 214, 190, 0.16);
    border-radius: 8px;
    padding: 0.9rem;
    min-height: 154px;
}

.intel-title {
    color: #55D6BE;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

.intel-body {
    color: rgba(238, 244, 248, 0.82);
    margin-top: 0.55rem;
    line-height: 1.45;
}

.field-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 0.65rem;
}

.field {
    background: rgba(13, 18, 26, 0.64);
    border: 1px solid rgba(238, 244, 248, 0.08);
    border-radius: 8px;
    padding: 0.72rem;
}

.field-label {
    color: rgba(238, 244, 248, 0.54);
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

.field-value {
    color: #EEF4F8;
    font-weight: 700;
    margin-top: 0.22rem;
}

.outreach-box {
    background: rgba(13, 18, 26, 0.68);
    border: 1px solid rgba(238, 244, 248, 0.08);
    border-radius: 8px;
    padding: 0.85rem;
    margin-bottom: 0.65rem;
}

.outreach-title {
    color: rgba(238, 244, 248, 0.60);
    font-size: 0.74rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

.outreach-copy {
    color: rgba(238, 244, 248, 0.84);
    margin-top: 0.38rem;
    white-space: pre-wrap;
    line-height: 1.42;
}

.action-item {
    display: flex;
    gap: 0.65rem;
    align-items: flex-start;
    border-bottom: 1px solid rgba(238, 244, 248, 0.08);
    padding: 0.72rem 0;
}

.action-item:last-child {
    border-bottom: 0;
}

.action-index {
    color: #0E1117;
    background: #55D6BE;
    border-radius: 999px;
    min-width: 1.65rem;
    height: 1.65rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 0.8rem;
}

.action-copy {
    color: rgba(238, 244, 248, 0.82);
    line-height: 1.42;
}

[data-testid="stRadio"] label {
    background: rgba(17, 22, 31, 0.88);
    border: 1px solid rgba(238, 244, 248, 0.10);
    border-radius: 8px;
    padding: 0.45rem 0.55rem;
    margin-bottom: 0.42rem;
}

[data-testid="stRadio"] label:hover {
    border-color: rgba(89, 164, 255, 0.42);
}
</style>
"""


PREMIUM_SAAS_CSS = """
<style>
:root {
    --saas-bg: #0B0F15;
    --saas-panel: rgba(17, 24, 39, 0.86);
    --saas-panel-strong: rgba(21, 30, 44, 0.95);
    --saas-border: rgba(226, 232, 240, 0.11);
    --saas-border-strong: rgba(96, 165, 250, 0.28);
    --saas-text: #F8FAFC;
    --saas-muted: rgba(226, 232, 240, 0.66);
    --saas-faint: rgba(226, 232, 240, 0.46);
    --saas-blue: #60A5FA;
    --saas-green: #34D399;
    --saas-amber: #FBBF24;
    --saas-red: #FB7185;
    --saas-purple: #A78BFA;
    --saas-cyan: #22D3EE;
    --saas-radius: 14px;
    --saas-shadow: 0 18px 50px rgba(2, 6, 23, 0.32);
}

.stApp {
    background:
        radial-gradient(circle at 8% 0%, rgba(96, 165, 250, 0.12), transparent 24%),
        radial-gradient(circle at 92% 5%, rgba(52, 211, 153, 0.09), transparent 22%),
        linear-gradient(135deg, #0B0F15 0%, #111827 48%, #0B0F15 100%) !important;
}

.block-container {
    padding-top: 1rem !important;
    max-width: 1480px !important;
}

h1, h2, h3, p, label, span, div {
    letter-spacing: 0 !important;
}

h2, h3 {
    color: var(--saas-text) !important;
}

.saas-header,
.hero,
.executive-header,
.copilot-header,
.workspace-header {
    min-height: unset !important;
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.70), rgba(15, 23, 42, 0.74)) !important;
    border: 1px solid var(--saas-border) !important;
    border-radius: var(--saas-radius) !important;
    padding: 0.85rem 1rem !important;
    margin-bottom: 1rem !important;
    box-shadow: 0 14px 36px rgba(2, 6, 23, 0.20) !important;
}

.saas-header {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    align-items: center;
}

.saas-header-main {
    display: flex;
    align-items: center;
    gap: 0.85rem;
}

.saas-header-icon {
    width: 2.45rem;
    height: 2.45rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 12px;
    background: rgba(96, 165, 250, 0.14);
    border: 1px solid rgba(96, 165, 250, 0.24);
    font-size: 1.15rem;
}

.saas-eyebrow {
    color: var(--saas-blue);
    font-size: 0.72rem;
    text-transform: uppercase;
    font-weight: 700;
    letter-spacing: 0.06em !important;
}

.saas-header h1,
.executive-header h1,
.copilot-header h1,
.workspace-header h1 {
    margin: 0.05rem 0 0.1rem !important;
    font-size: clamp(1.55rem, 2.1vw, 2.05rem) !important;
    line-height: 1.12 !important;
}

.saas-header p,
.hero p,
.executive-header p,
.copilot-header p,
.workspace-header p {
    color: var(--saas-muted) !important;
    margin: 0 !important;
    font-size: 0.93rem !important;
}

.saas-header-meta {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    justify-content: flex-end;
}

.saas-header-meta span {
    color: var(--saas-muted);
    border: 1px solid var(--saas-border);
    background: rgba(15, 23, 42, 0.52);
    border-radius: 999px;
    padding: 0.34rem 0.62rem;
    font-size: 0.78rem;
}

.saas-kpi,
.kpi-card,
.executive-kpi,
.signal-card,
.metric-card {
    min-height: 132px !important;
    background: linear-gradient(150deg, rgba(30, 41, 59, 0.88), rgba(15, 23, 42, 0.92)) !important;
    border: 1px solid var(--saas-border) !important;
    border-radius: var(--saas-radius) !important;
    padding: 0.95rem !important;
    box-shadow: 0 12px 34px rgba(2, 6, 23, 0.20) !important;
    transition: transform 160ms ease, box-shadow 160ms ease, border-color 160ms ease !important;
}

.saas-kpi:hover,
.kpi-card:hover,
.executive-kpi:hover,
.signal-card:hover,
.metric-card:hover,
.lead-card:hover,
.workspace-panel:hover,
.executive-panel:hover,
.copilot-panel:hover,
.ai-card:hover,
.intel-card:hover,
.stPlotlyChart:hover {
    transform: translateY(-2px);
    border-color: var(--saas-border-strong) !important;
    box-shadow: var(--saas-shadow) !important;
}

.saas-kpi-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.5rem;
}

.saas-kpi-icon {
    width: 2.05rem;
    height: 2.05rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 10px;
    background: rgba(96, 165, 250, 0.14);
    border: 1px solid rgba(96, 165, 250, 0.22);
}

.saas-trend,
.saas-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.28rem;
    border-radius: 999px;
    padding: 0.24rem 0.5rem;
    font-size: 0.74rem;
    font-weight: 700;
    border: 1px solid rgba(226, 232, 240, 0.10);
    background: rgba(148, 163, 184, 0.12);
    color: var(--saas-muted);
    white-space: nowrap;
}

.saas-kpi-metric {
    color: var(--saas-text);
    font-size: clamp(1.42rem, 2.2vw, 2rem);
    font-weight: 800;
    line-height: 1.08;
    margin-top: 0.8rem;
}

.saas-kpi-label,
.metric-value,
.signal-value {
    color: var(--saas-text) !important;
    font-weight: 800 !important;
}

.saas-kpi-label {
    margin-top: 0.28rem;
    font-size: 0.86rem;
}

.saas-kpi-description,
.metric-label,
.signal-label,
.ai-card-rationale,
.intel-body,
.muted {
    color: var(--saas-muted) !important;
}

.saas-kpi-description {
    font-size: 0.78rem;
    margin-top: 0.28rem;
}

.saas-kpi-positive .saas-kpi-icon,
.saas-badge-positive,
.saas-badge-hot,
.saas-badge-high,
.saas-badge-won,
.saas-badge-qualified {
    background: rgba(52, 211, 153, 0.16);
    color: #BBF7D0;
    border-color: rgba(52, 211, 153, 0.30);
}

.saas-kpi-warning .saas-kpi-icon,
.saas-badge-warning,
.saas-badge-warm,
.saas-badge-medium,
.saas-badge-proposal,
.saas-badge-negotiation {
    background: rgba(251, 191, 36, 0.15);
    color: #FDE68A;
    border-color: rgba(251, 191, 36, 0.28);
}

.saas-kpi-risk .saas-kpi-icon,
.saas-badge-risk,
.saas-badge-cold,
.saas-badge-low,
.saas-badge-lost {
    background: rgba(251, 113, 133, 0.14);
    color: #FECDD3;
    border-color: rgba(251, 113, 133, 0.28);
}

.saas-badge-info,
.saas-badge-new,
.saas-badge-contacted,
.saas-badge-neutral {
    background: rgba(96, 165, 250, 0.14);
    color: #BFDBFE;
    border-color: rgba(96, 165, 250, 0.25);
}

.saas-section-heading {
    margin: 1.1rem 0 0.55rem;
}

.saas-section-heading h2 {
    font-size: 1.05rem !important;
    margin: 0 !important;
}

.saas-section-heading p {
    color: var(--saas-muted);
    margin: 0.16rem 0 0;
    font-size: 0.84rem;
}

.saas-card,
.executive-panel,
.copilot-panel,
.workspace-panel,
.ai-card,
.intel-card,
.lead-summary,
.pipeline-stage,
.lead-card,
.outreach-box,
[data-testid="stDataFrame"],
.stPlotlyChart {
    background: linear-gradient(150deg, rgba(17, 24, 39, 0.92), rgba(15, 23, 42, 0.88)) !important;
    border: 1px solid var(--saas-border) !important;
    border-radius: var(--saas-radius) !important;
    box-shadow: 0 14px 36px rgba(2, 6, 23, 0.18) !important;
    transition: transform 160ms ease, box-shadow 160ms ease, border-color 160ms ease !important;
}

.stPlotlyChart {
    padding: 0.75rem !important;
}

.saas-card {
    padding: 0.95rem;
    margin-bottom: 0.75rem;
}

.saas-card-title {
    color: var(--saas-text);
    font-size: 0.85rem;
    font-weight: 800;
    letter-spacing: 0.04em !important;
    text-transform: uppercase;
}

.saas-card-body {
    color: var(--saas-muted);
    margin-top: 0.55rem;
    line-height: 1.5;
}

.saas-progress,
.confidence,
.progress {
    height: 8px !important;
    background: rgba(226, 232, 240, 0.10) !important;
    border-radius: 999px !important;
    overflow: hidden !important;
}

.saas-progress {
    margin-top: 0.62rem;
}

.saas-progress-fill,
.confidence-fill,
.progress-fill {
    height: 8px !important;
    background: linear-gradient(90deg, var(--saas-blue), var(--saas-green)) !important;
    border-radius: 999px !important;
}

.sidebar-filter-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.5rem;
    margin: 0.25rem 0 0.85rem;
    color: var(--saas-text);
    font-weight: 800;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(9, 13, 20, 0.98), rgba(15, 23, 42, 0.96)) !important;
}

[data-testid="stSidebar"] [data-testid="stExpander"] {
    border: 1px solid var(--saas-border) !important;
    border-radius: 12px !important;
    background: rgba(15, 23, 42, 0.46) !important;
    margin-bottom: 0.75rem !important;
}

.stButton > button,
[data-testid="baseButton-secondary"] {
    border-radius: 10px !important;
    border: 1px solid rgba(96, 165, 250, 0.28) !important;
    background: rgba(96, 165, 250, 0.11) !important;
    color: var(--saas-text) !important;
    transition: transform 140ms ease, border-color 140ms ease, background 140ms ease !important;
}

.stButton > button:hover,
[data-testid="baseButton-secondary"]:hover {
    transform: translateY(-1px);
    border-color: rgba(96, 165, 250, 0.58) !important;
    background: rgba(96, 165, 250, 0.18) !important;
}

.lead-card {
    border-left: 3px solid var(--saas-blue) !important;
}

.score-pill {
    display: grid;
    gap: 0.35rem;
}

.score-pill strong {
    color: var(--saas-text);
    font-size: 1.18rem;
}

@media (max-width: 900px) {
    .saas-header {
        align-items: flex-start;
        flex-direction: column;
    }

    .saas-header-meta {
        justify-content: flex-start;
    }
}
</style>
"""


DARK_THEME_CSS = DARK_THEME_CSS + PREMIUM_SAAS_CSS
EXECUTIVE_THEME_CSS = EXECUTIVE_THEME_CSS + PREMIUM_SAAS_CSS
COPILOT_THEME_CSS = COPILOT_THEME_CSS + PREMIUM_SAAS_CSS
WORKSPACE_THEME_CSS = WORKSPACE_THEME_CSS + PREMIUM_SAAS_CSS
