"""
BuffettVision – L'Investisseur Patient
Application d'analyse d'actions dans le style Warren Buffett
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import requests
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# CONFIGURATION DE LA PAGE
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="BuffettVision – L'Investisseur Patient",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# CSS PERSONNALISÉ – Design élégant vert/blanc
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Source+Sans+3:wght@300;400;600&display=swap');

:root {
    --green-dark:  #1a3a2a;
    --green-mid:   #2d6a4f;
    --green-light: #52b788;
    --gold:        #c9a84c;
    --cream:       #f8f5ef;
    --text-dark:   #1c1c1c;
    --text-light:  #f0ede6;
    --card-bg:     #ffffff;
    --border:      #e0ddd5;
    --red:         #c0392b;
    --yellow:      #d4a017;
}

html, body, [class*="css"] {
    font-family: 'Source Sans 3', sans-serif;
    background-color: var(--cream);
    color: var(--text-dark);
}

/* HEADER */
.bv-header {
    background: linear-gradient(135deg, var(--green-dark) 0%, var(--green-mid) 100%);
    padding: 2.5rem 3rem;
    border-radius: 0 0 24px 24px;
    margin-bottom: 2rem;
    text-align: center;
    box-shadow: 0 4px 24px rgba(26,58,42,0.18);
}
.bv-header h1 {
    font-family: 'Playfair Display', serif;
    color: var(--text-light);
    font-size: 2.6rem;
    margin: 0;
    letter-spacing: 1px;
}
.bv-header .subtitle {
    color: var(--gold);
    font-size: 1.05rem;
    margin-top: 0.4rem;
    font-style: italic;
    opacity: 0.92;
}
.bv-header .tagline {
    color: rgba(240,237,230,0.7);
    font-size: 0.88rem;
    margin-top: 0.2rem;
}

/* CARDS */
.bv-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem 1.8rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.055);
}
.bv-card h2 {
    font-family: 'Playfair Display', serif;
    color: var(--green-dark);
    font-size: 1.35rem;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid var(--green-light);
}
.bv-card h3 {
    font-family: 'Playfair Display', serif;
    color: var(--green-mid);
    font-size: 1.1rem;
    margin-bottom: 0.7rem;
}

/* METRIC TILES */
.metric-tile {
    background: linear-gradient(135deg, #f8f5ef, #ffffff);
    border: 1px solid var(--border);
    border-left: 4px solid var(--green-light);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    text-align: center;
}
.metric-tile .label {
    font-size: 0.78rem;
    color: #777;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 0.25rem;
}
.metric-tile .value {
    font-size: 1.55rem;
    font-weight: 700;
    color: var(--green-dark);
    line-height: 1.1;
}
.metric-tile .sub {
    font-size: 0.8rem;
    color: #888;
    margin-top: 0.2rem;
}

/* SCORE BUFFETT */
.buffett-score {
    background: linear-gradient(135deg, var(--green-dark), var(--green-mid));
    color: white;
    border-radius: 16px;
    padding: 1.8rem 2rem;
    text-align: center;
    margin-bottom: 1rem;
}
.buffett-score .score-number {
    font-family: 'Playfair Display', serif;
    font-size: 4.5rem;
    font-weight: 700;
    color: var(--gold);
    line-height: 1;
}
.buffett-score .score-label {
    font-size: 1.1rem;
    opacity: 0.9;
    margin-top: 0.3rem;
}

/* RECOMMANDATIONS */
.reco-buy {
    background: linear-gradient(135deg, #1a3a2a, #2d6a4f);
    color: white;
    border-radius: 16px;
    padding: 2rem 2.5rem;
    border-left: 6px solid var(--gold);
    margin-bottom: 1rem;
}
.reco-hold {
    background: linear-gradient(135deg, #4a3a00, #7a6010);
    color: white;
    border-radius: 16px;
    padding: 2rem 2.5rem;
    border-left: 6px solid #f0c040;
    margin-bottom: 1rem;
}
.reco-avoid {
    background: linear-gradient(135deg, #3a1010, #7a2020);
    color: white;
    border-radius: 16px;
    padding: 2rem 2.5rem;
    border-left: 6px solid #ff6b6b;
    margin-bottom: 1rem;
}
.reco-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    margin-bottom: 0.8rem;
}
.reco-text {
    font-size: 1.05rem;
    opacity: 0.92;
    line-height: 1.6;
}

/* MARGE DE SÉCURITÉ */
.margin-positive { color: var(--green-light); font-weight: 700; font-size: 1.4rem; }
.margin-neutral   { color: var(--yellow);      font-weight: 700; font-size: 1.4rem; }
.margin-negative  { color: #ff6b6b;            font-weight: 700; font-size: 1.4rem; }

/* CHECKLIST */
.check-item {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    padding: 0.5rem 0;
    border-bottom: 1px solid #f0ede6;
    font-size: 0.95rem;
}
.check-yes { color: var(--green-light); font-size: 1.2rem; }
.check-no  { color: #ff6b6b;            font-size: 1.2rem; }
.check-mid { color: var(--gold);        font-size: 1.2rem; }

/* TOOLTIP PEDAGOGIQUE */
.tooltip-box {
    background: #f0faf5;
    border: 1px solid var(--green-light);
    border-radius: 8px;
    padding: 0.7rem 1rem;
    font-size: 0.85rem;
    color: var(--green-dark);
    margin-top: 0.5rem;
    line-height: 1.5;
}

/* BADGE SECTEUR */
.sector-badge {
    display: inline-block;
    background: var(--green-mid);
    color: white;
    border-radius: 20px;
    padding: 0.25rem 0.9rem;
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    margin-bottom: 0.5rem;
}

/* SÉPARATEUR DORÉ */
.gold-divider {
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
    margin: 1.5rem 0;
    border: none;
}

/* TABLE STYLED */
.styled-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.9rem;
}
.styled-table th {
    background: var(--green-dark);
    color: white;
    padding: 0.6rem 0.8rem;
    text-align: left;
    font-weight: 600;
}
.styled-table td {
    padding: 0.5rem 0.8rem;
    border-bottom: 1px solid #f0ede6;
}
.styled-table tr:nth-child(even) td { background: #fafaf7; }

/* HIDE STREAMLIT BITS */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
.stDeployButton { display: none; }

/* SLIDERS */
.stSlider > div > div > div > div { background: var(--green-mid) !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="bv-header">
    <h1>🏦 BuffettVision</h1>
    <div class="subtitle">« Le prix est ce que vous payez. La valeur est ce que vous obtenez. »</div>
    <div class="tagline">Analyse fondamentale long terme · Style Warren Buffett · Valeur intrinsèque · Marge de sécurité</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HELPERS – DONNÉES
# ─────────────────────────────────────────────

KNOWN_TICKERS = {
    "apple": "AAPL", "microsoft": "MSFT", "amazon": "AMZN", "alphabet": "GOOGL",
    "google": "GOOGL", "meta": "META", "tesla": "TSLA", "berkshire": "BRK-B",
    "johnson": "JNJ", "coca cola": "KO", "coca-cola": "KO", "pepsi": "PEP",
    "pepsico": "PEP", "nike": "NKE", "visa": "V", "mastercard": "MA",
    "procter": "PG", "p&g": "PG", "walmart": "WMT", "disney": "DIS",
    "netflix": "NFLX", "nvidia": "NVDA", "intel": "INTC", "amd": "AMD",
    "jpmorgan": "JPM", "jp morgan": "JPM", "bank of america": "BAC",
    "wells fargo": "WFC", "goldman": "GS", "morgan stanley": "MS",
    "exxon": "XOM", "chevron": "CVX", "total": "TTE", "shell": "SHEL",
    "lvmh": "MC.PA", "hermes": "RMS.PA", "kering": "KER.PA", "airbus": "AIR.PA",
    "sanofi": "SAN.PA", "loreal": "OR.PA", "l'oreal": "OR.PA",
    "asml": "ASML", "nestle": "NESN.SW", "roche": "ROG.SW", "novartis": "NOVN.SW",
    "samsung": "005930.KS", "toyota": "7203.T", "sony": "6758.T",
}

@st.cache_data(ttl=1800, show_spinner=False)
def load_ticker_data(ticker: str):
    """Charge toutes les données yfinance pour un ticker."""
    t = yf.Ticker(ticker)
    info = t.info or {}
    hist_1y  = t.history(period="1y")
    hist_5y  = t.history(period="5y")
    hist_max = t.history(period="max")
    financials   = t.financials
    balance      = t.balance_sheet
    cashflow     = t.cashflow
    quarterly_cf = t.quarterly_cashflow
    news         = t.news or []
    return info, hist_1y, hist_5y, hist_max, financials, balance, cashflow, quarterly_cf, news

def resolve_ticker(query: str) -> str:
    """Résout un nom d'entreprise ou un ticker en ticker yfinance."""
    q = query.strip().upper()
    q_lower = query.strip().lower()
    for name, sym in KNOWN_TICKERS.items():
        if name in q_lower:
            return sym
    return q  # Suppose que c'est directement un ticker

def fmt_big(n, currency="$"):
    """Formate un grand nombre en milliards/millions."""
    if n is None or (isinstance(n, float) and np.isnan(n)):
        return "N/A"
    abs_n = abs(n)
    sign  = "-" if n < 0 else ""
    if abs_n >= 1e12: return f"{sign}{currency}{abs_n/1e12:.2f}T"
    if abs_n >= 1e9:  return f"{sign}{currency}{abs_n/1e9:.2f}B"
    if abs_n >= 1e6:  return f"{sign}{currency}{abs_n/1e6:.2f}M"
    return f"{sign}{currency}{abs_n:,.0f}"

def fmt_pct(n):
    """Formate en pourcentage."""
    if n is None or (isinstance(n, float) and np.isnan(n)):
        return "N/A"
    return f"{n*100:.1f}%"

def safe_get(d, *keys, default=None):
    """Récupère une clé imbriquée sans exception."""
    for k in keys:
        if isinstance(d, dict):
            d = d.get(k, default)
        else:
            return default
    return d if d is not None else default

def get_financial_series(df, row_names):
    """Extrait une ligne d'un DataFrame financier, essaie plusieurs noms."""
    if df is None or df.empty:
        return pd.Series(dtype=float)
    for name in row_names:
        if name in df.index:
            return df.loc[name].sort_index()
    return pd.Series(dtype=float)

# ─────────────────────────────────────────────
# BARRE DE RECHERCHE
# ─────────────────────────────────────────────
col_search, col_fmp = st.columns([3, 1])

with col_search:
    st.markdown("### 🔍 Rechercher une entreprise")
    search_input = st.text_input(
        "",
        placeholder="Ex : AAPL, Apple, KO, Coca-Cola, LVMH, MC.PA, Berkshire...",
        label_visibility="collapsed",
        key="search_input"
    )

with col_fmp:
    st.markdown("### 🔑 Clé API FMP (optionnel)")
    fmp_key = st.text_input(
        "",
        placeholder="Clé Financial Modeling Prep",
        type="password",
        label_visibility="collapsed",
        key="fmp_key"
    )
    st.caption("Données plus précises avec FMP. Fonctionne très bien sans clé.")

# Suggestions rapides
st.markdown("""
<div style="display:flex;flex-wrap:wrap;gap:0.5rem;margin-bottom:1.5rem;margin-top:-0.5rem;">
<span style="font-size:0.82rem;color:#888;align-self:center;">Suggestions :</span>
</div>
""", unsafe_allow_html=True)

suggestions = ["AAPL", "KO", "BRK-B", "MSFT", "MC.PA", "NVDA", "JNJ", "V"]
cols = st.columns(len(suggestions))
for i, s in enumerate(suggestions):
    with cols[i]:
        if st.button(s, key=f"sug_{s}", use_container_width=True):
            st.session_state["search_input"] = s
            st.rerun()

if not search_input:
    st.markdown("""
    <div class="bv-card" style="text-align:center;padding:3rem;">
        <div style="font-size:3rem;margin-bottom:1rem;">🦅</div>
        <h2 style="border:none;text-align:center;font-size:1.6rem;">Bienvenue dans BuffettVision</h2>
        <p style="color:#666;font-size:1.05rem;max-width:600px;margin:0 auto;line-height:1.7;">
            Entrez le <strong>ticker</strong> ou le <strong>nom</strong> d'une entreprise pour obtenir
            une analyse complète dans le pur style Warren Buffett : valeur intrinsèque,
            marge de sécurité, moat économique et recommandation claire.
        </p>
        <div class="gold-divider" style="max-width:300px;margin:1.5rem auto;"></div>
        <p style="color:#999;font-size:0.9rem;font-style:italic;">
            « Achetez de merveilleuses entreprises à un prix raisonnable. » — Warren Buffett
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ─────────────────────────────────────────────
# CHARGEMENT DES DONNÉES
# ─────────────────────────────────────────────
ticker_sym = resolve_ticker(search_input)

with st.spinner(f"⏳ Chargement des données pour **{ticker_sym}**..."):
    try:
        info, hist_1y, hist_5y, hist_max, financials, balance, cashflow, quarterly_cf, news = load_ticker_data(ticker_sym)
    except Exception as e:
        st.error(f"❌ Impossible de charger les données : {e}")
        st.stop()

if not info or info.get("regularMarketPrice") is None and hist_1y.empty:
    st.error(f"❌ Ticker **{ticker_sym}** introuvable. Vérifiez le symbole (ex : AAPL, MC.PA, BRK-B).")
    st.stop()

# ─────────────────────────────────────────────
# EXTRACTION DES INFOS DE BASE
# ─────────────────────────────────────────────
company_name  = info.get("longName") or info.get("shortName") or ticker_sym
sector        = info.get("sector", "Secteur inconnu")
industry      = info.get("industry", "")
summary       = info.get("longBusinessSummary", "Description non disponible.")
currency      = info.get("currency", "USD")
curr_sym      = "€" if currency in ("EUR",) else ("£" if currency == "GBP" else "$")

current_price = (
    info.get("regularMarketPrice") or
    info.get("currentPrice") or
    (hist_1y["Close"].iloc[-1] if not hist_1y.empty else None)
)
prev_close     = info.get("previousClose") or info.get("regularMarketPreviousClose")
change_1d      = ((current_price - prev_close) / prev_close * 100) if current_price and prev_close else None
market_cap     = info.get("marketCap")
shares_out     = info.get("sharesOutstanding") or info.get("impliedSharesOutstanding")
pe_ratio       = info.get("trailingPE") or info.get("forwardPE")
pb_ratio       = info.get("priceToBook")
ps_ratio       = info.get("priceToSalesTrailing12Months")
div_yield      = info.get("dividendYield")
beta           = info.get("beta")
week52_high    = info.get("fiftyTwoWeekHigh")
week52_low     = info.get("fiftyTwoWeekLow")
logo_url       = info.get("logo_url") or ""

# ─────────────────────────────────────────────
# EN-TÊTE ENTREPRISE
# ─────────────────────────────────────────────
st.markdown('<div class="bv-card">', unsafe_allow_html=True)

h_col1, h_col2 = st.columns([2, 1])
with h_col1:
    if logo_url:
        st.image(logo_url, width=80)
    st.markdown(f"<h1 style='font-family:Playfair Display,serif;font-size:2rem;color:#1a3a2a;margin-bottom:0.2rem;'>{company_name}</h1>", unsafe_allow_html=True)
    st.markdown(f"<div class='sector-badge'>{sector}</div>", unsafe_allow_html=True)
    if industry:
        st.caption(f"🏭 {industry} · 📊 {ticker_sym} · 💱 {currency}")
    st.markdown(f"<p style='color:#555;font-size:0.93rem;line-height:1.6;max-width:700px;'>{summary[:500]}{'...' if len(summary)>500 else ''}</p>", unsafe_allow_html=True)

with h_col2:
    if current_price:
        color_1d = "green" if (change_1d or 0) >= 0 else "red"
        arrow    = "▲" if (change_1d or 0) >= 0 else "▼"
        st.markdown(f"""
        <div style="text-align:right;">
            <div style="font-family:'Playfair Display',serif;font-size:2.5rem;color:#1a3a2a;font-weight:700;">
                {curr_sym}{current_price:,.2f}
            </div>
            <div style="color:{color_1d};font-size:1.1rem;font-weight:600;">
                {arrow} {abs(change_1d or 0):.2f}% aujourd'hui
            </div>
            <div style="color:#888;font-size:0.85rem;margin-top:0.4rem;">
                Cap. boursière : {fmt_big(market_cap, curr_sym)}<br>
                52 sem. : {curr_sym}{week52_low:,.2f} – {curr_sym}{week52_high:,.2f}
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# GRAPHIQUE DES PRIX
# ─────────────────────────────────────────────
st.markdown('<div class="bv-card">', unsafe_allow_html=True)
st.markdown('<h2>📈 Évolution du cours</h2>', unsafe_allow_html=True)

period_choice = st.radio(
    "Période :", ["1 an", "5 ans", "Max"],
    horizontal=True, key="period"
)
hist_map = {"1 an": hist_1y, "5 ans": hist_5y, "Max": hist_max}
hist_df  = hist_map[period_choice]

if not hist_df.empty:
    fig_price = go.Figure()
    fig_price.add_trace(go.Scatter(
        x=hist_df.index, y=hist_df["Close"],
        mode="lines",
        line=dict(color="#2d6a4f", width=2.5),
        fill="tozeroy",
        fillcolor="rgba(82,183,136,0.12)",
        name="Prix de clôture",
        hovertemplate=f"<b>%{{x|%d/%m/%Y}}</b><br>Prix : {curr_sym}%{{y:,.2f}}<extra></extra>"
    ))
    # Moyenne mobile 50j
    if len(hist_df) >= 50:
        ma50 = hist_df["Close"].rolling(50).mean()
        fig_price.add_trace(go.Scatter(
            x=hist_df.index, y=ma50,
            mode="lines", line=dict(color="#c9a84c", width=1.5, dash="dot"),
            name="Moyenne 50j", opacity=0.8
        ))
    fig_price.update_layout(
        height=380, plot_bgcolor="#fafaf7", paper_bgcolor="#fafaf7",
        margin=dict(l=10, r=10, t=20, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(showgrid=False, linecolor="#ddd"),
        yaxis=dict(showgrid=True, gridcolor="#eee", linecolor="#ddd",
                   tickprefix=curr_sym),
        hovermode="x unified",
    )
    st.plotly_chart(fig_price, use_container_width=True)
else:
    st.warning("Données historiques de prix non disponibles.")

st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SANTÉ FINANCIÈRE
# ─────────────────────────────────────────────
st.markdown('<div class="bv-card">', unsafe_allow_html=True)
st.markdown('<h2>💰 Santé Financière (style Buffett)</h2>', unsafe_allow_html=True)
st.markdown('<div class="tooltip-box">📚 <strong>Pourquoi ces chiffres ?</strong> Warren Buffett analyse la régularité et la croissance des bénéfices sur 10 ans. Une entreprise «merveilleuse» a des revenus croissants, des marges stables et peu de dettes.</div>', unsafe_allow_html=True)

# Extraction séries financières
rev_series    = get_financial_series(financials, ["Total Revenue", "Revenue", "Revenues"])
ni_series     = get_financial_series(financials, ["Net Income", "Net Income Common Stockholders"])
ocf_series    = get_financial_series(cashflow, ["Operating Cash Flow", "Total Cash From Operating Activities"])
capex_series  = get_financial_series(cashflow, ["Capital Expenditure", "Capital Expenditures", "Purchase Of Plant And Equipment"])
eq_series     = get_financial_series(balance, ["Stockholders Equity", "Total Stockholder Equity", "Common Stock Equity"])

# FCF = OCF + CapEx (CapEx est négatif dans yfinance)
if not ocf_series.empty and not capex_series.empty:
    common_idx = ocf_series.index.intersection(capex_series.index)
    fcf_series = (ocf_series[common_idx] + capex_series[common_idx]).sort_index()
else:
    fcf_series = pd.Series(dtype=float)

# Affichage graphiques financiers
has_rev  = not rev_series.empty
has_ni   = not ni_series.empty
has_fcf  = not fcf_series.empty

if has_rev or has_ni or has_fcf:
    fig_fin = make_subplots(
        rows=1, cols=3,
        subplot_titles=("Chiffre d'affaires", "Bénéfice net", "Free Cash Flow"),
        horizontal_spacing=0.08
    )
    colors = ["#2d6a4f", "#52b788", "#c9a84c"]
    for i, (series, has_data) in enumerate([(rev_series, has_rev), (ni_series, has_ni), (fcf_series, has_fcf)], 1):
        if has_data:
            sorted_s = series.sort_index()
            bar_colors = [colors[i-1] if v >= 0 else "#c0392b" for v in sorted_s.values]
            fig_fin.add_trace(
                go.Bar(
                    x=[str(d)[:4] for d in sorted_s.index],
                    y=sorted_s.values / 1e9,
                    marker_color=bar_colors,
                    hovertemplate="%{x} : %{y:.2f}B " + currency + "<extra></extra>",
                    showlegend=False,
                ),
                row=1, col=i
            )
    fig_fin.update_layout(
        height=300, plot_bgcolor="#fafaf7", paper_bgcolor="#fafaf7",
        margin=dict(l=10, r=10, t=40, b=10),
    )
    fig_fin.update_yaxes(ticksuffix="B")
    st.plotly_chart(fig_fin, use_container_width=True)
else:
    st.info("Données financières historiques limitées pour cet actif.")

# ─── RATIOS CLÉS ───
st.markdown("<h3>Ratios clés</h3>", unsafe_allow_html=True)

roe       = info.get("returnOnEquity")
roic      = info.get("returnOnAssets")  # proxy si ROIC non dispo
op_margin = info.get("operatingMargins")
net_margin= info.get("profitMargins")
debt_eq   = info.get("debtToEquity")
current_r = info.get("currentRatio")
fcf_yield_val = None

if not fcf_series.empty and current_price and shares_out:
    latest_fcf = fcf_series.iloc[-1] if not fcf_series.empty else None
    if latest_fcf and shares_out:
        fcf_per_share = latest_fcf / shares_out
        fcf_yield_val = fcf_per_share / current_price

metrics_r = [
    ("ROE", fmt_pct(roe), "Rentabilité des capitaux propres. Buffett cherche > 15%"),
    ("ROIC", fmt_pct(roic), "Rentabilité du capital investi"),
    ("Marge opérationnelle", fmt_pct(op_margin), "Part des revenus conservée comme profit opérationnel. > 20% = très bien"),
    ("Marge nette", fmt_pct(net_margin), "Bénéfice net / Chiffre d'affaires. > 10% est positif"),
    ("Dettes / Capitaux propres", f"{debt_eq/100:.2f}" if debt_eq else "N/A", "Niveau d'endettement. < 1 est idéal"),
    ("Ratio de liquidité", f"{current_r:.2f}" if current_r else "N/A", "Capacité à rembourser les dettes court terme. > 1.5 = solide"),
    ("FCF Yield", fmt_pct(fcf_yield_val), "Free Cash Flow / Prix. > 5% indique une bonne valeur"),
    ("P/E ratio", f"{pe_ratio:.1f}x" if pe_ratio else "N/A", "Prix / Bénéfice. Comparer avec la moyenne historique"),
    ("P/B ratio", f"{pb_ratio:.2f}x" if pb_ratio else "N/A", "Prix / Valeur comptable"),
]

ratio_cols = st.columns(3)
for idx, (label, value, tooltip) in enumerate(metrics_r):
    with ratio_cols[idx % 3]:
        st.markdown(f"""
        <div class="metric-tile" title="{tooltip}">
            <div class="label">{label}</div>
            <div class="value">{value}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("")

st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ANALYSE MOAT & BUFFETT SCORE
# ─────────────────────────────────────────────
st.markdown('<div class="bv-card">', unsafe_allow_html=True)
st.markdown('<h2>🏰 Moat Économique & Buffett Score</h2>', unsafe_allow_html=True)
st.markdown('<div class="tooltip-box">📚 <strong>Qu\'est-ce qu\'un Moat ?</strong> Un "fossé économique" est l\'avantage concurrentiel durable qui protège une entreprise de ses concurrents – comme les marques fortes, les effets de réseau, les coûts de changement élevés ou les économies d\'échelle. C\'est LE critère numéro 1 de Warren Buffett.</div>', unsafe_allow_html=True)

# Calcul automatique du Buffett Score
score_details = {}

# 1. Rentabilité (ROE > 15% = 15 pts)
if roe is not None:
    s = 15 if roe > 0.20 else (10 if roe > 0.15 else (5 if roe > 0.10 else 0))
    score_details["ROE élevé (>15%)"] = (s, 15, "✅" if s >= 10 else ("⚠️" if s > 0 else "❌"))

# 2. Marge nette (>10% = 15 pts)
if net_margin is not None:
    s = 15 if net_margin > 0.20 else (10 if net_margin > 0.10 else (5 if net_margin > 0.05 else 0))
    score_details["Marges élevées (>10%)"] = (s, 15, "✅" if s >= 10 else ("⚠️" if s > 0 else "❌"))

# 3. Croissance revenus (si dispo)
if not rev_series.empty and len(rev_series) >= 3:
    rev_sorted = rev_series.sort_index()
    rev_growth = (rev_sorted.iloc[-1] / rev_sorted.iloc[0]) ** (1/(len(rev_sorted)-1)) - 1
    s = 15 if rev_growth > 0.10 else (10 if rev_growth > 0.05 else (5 if rev_growth > 0 else 0))
    score_details[f"Croissance CA ({rev_growth*100:.1f}%/an)"] = (s, 15, "✅" if s >= 10 else ("⚠️" if s > 0 else "❌"))

# 4. FCF positif
if not fcf_series.empty:
    latest_fcf_val = fcf_series.sort_index().iloc[-1]
    s = 15 if latest_fcf_val > 0 else 0
    score_details["Free Cash Flow positif"] = (s, 15, "✅" if s > 0 else "❌")

# 5. Endettement faible
if debt_eq is not None:
    dq = debt_eq / 100
    s = 10 if dq < 0.5 else (7 if dq < 1.0 else (3 if dq < 2.0 else 0))
    score_details["Endettement faible"] = (s, 10, "✅" if s >= 7 else ("⚠️" if s > 0 else "❌"))

# 6. Secteur défensif / moat sectoriel
moat_sectors = {
    "Consumer Defensive": 15, "Healthcare": 12, "Financial Services": 10,
    "Technology": 10, "Communication Services": 8, "Industrials": 8,
    "Consumer Cyclical": 6, "Basic Materials": 5, "Energy": 5, "Utilities": 7
}
moat_s = moat_sectors.get(sector, 5)
score_details[f"Secteur favorable ({sector})"] = (moat_s, 15, "✅" if moat_s >= 10 else ("⚠️" if moat_s >= 7 else "❌"))

# 7. Liquidité
if current_r is not None:
    s = 10 if current_r >= 2 else (7 if current_r >= 1.5 else (4 if current_r >= 1 else 0))
    score_details["Liquidité suffisante"] = (s, 10, "✅" if s >= 7 else ("⚠️" if s > 0 else "❌"))

total_score    = sum(v[0] for v in score_details.values())
total_max      = sum(v[1] for v in score_details.values())
buffett_score  = int(total_score / total_max * 100) if total_max > 0 else 0

moat_score     = int(buffett_score / 10)  # /10

bs_col1, bs_col2 = st.columns([1, 2])
with bs_col1:
    score_color = "#52b788" if buffett_score >= 70 else ("#c9a84c" if buffett_score >= 45 else "#e74c3c")
    st.markdown(f"""
    <div class="buffett-score">
        <div style="font-size:0.9rem;opacity:0.7;margin-bottom:0.3rem;">BUFFETT SCORE</div>
        <div class="score-number" style="color:{score_color};">{buffett_score}</div>
        <div class="score-label">/ 100</div>
        <div style="margin-top:0.8rem;font-size:0.85rem;opacity:0.75;">
            {'🌟 Entreprise exceptionnelle' if buffett_score >= 75 else
             ('👍 Bonne entreprise' if buffett_score >= 55 else
              ('⚠️ Qualité moyenne' if buffett_score >= 35 else '❌ À éviter'))}
        </div>
    </div>
    <div class="buffett-score" style="margin-top:0.8rem;">
        <div style="font-size:0.9rem;opacity:0.7;margin-bottom:0.3rem;">FORCE DU MOAT</div>
        <div class="score-number" style="color:{score_color};">{moat_score}</div>
        <div class="score-label">/ 10</div>
    </div>
    """, unsafe_allow_html=True)

with bs_col2:
    st.markdown("<h3>Checklist Buffett détaillée</h3>", unsafe_allow_html=True)
    for criterion, (pts, max_pts, icon) in score_details.items():
        pct = pts / max_pts * 100 if max_pts > 0 else 0
        bar_color = "#52b788" if pct >= 70 else ("#c9a84c" if pct >= 40 else "#e74c3c")
        st.markdown(f"""
        <div class="check-item">
            <span style="font-size:1.1rem;">{icon}</span>
            <span style="flex:1;">{criterion}</span>
            <span style="color:{bar_color};font-weight:600;min-width:60px;text-align:right;">{pts}/{max_pts} pts</span>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# VALEUR INTRINSÈQUE & DCF
# ─────────────────────────────────────────────
st.markdown('<div class="bv-card">', unsafe_allow_html=True)
st.markdown('<h2>🎯 Valeur Intrinsèque – Modèle DCF Buffett</h2>', unsafe_allow_html=True)
st.markdown('<div class="tooltip-box">📚 <strong>Comment fonctionne ce calcul ?</strong> La «Valeur Intrinsèque» est ce que vaut vraiment l\'entreprise, indépendamment de son cours de bourse. On estime les flux de trésorerie futurs (Owner Earnings) et on les actualise pour obtenir leur valeur aujourd\'hui. Si le prix actuel est bien inférieur à cette valeur = opportunité d\'achat !</div>', unsafe_allow_html=True)

# Récupération Owner Earnings (FCF le plus récent ou bénéfice net)
owner_earnings_base = None
if not fcf_series.empty:
    owner_earnings_base = fcf_series.sort_index().iloc[-1]
elif not ni_series.empty:
    owner_earnings_base = ni_series.sort_index().iloc[-1]

# Paramètres DCF
st.markdown("#### ⚙️ Hypothèses du modèle (modifiables)")
dcf_col1, dcf_col2, dcf_col3 = st.columns(3)

with dcf_col1:
    growth_rate_1 = st.slider(
        "Taux de croissance (5 premières années) %",
        min_value=0, max_value=25, value=8, step=1, key="gr1"
    ) / 100
    st.caption("Conservateur = 5-8% · Optimiste = 10-15%")

with dcf_col2:
    growth_rate_2 = st.slider(
        "Taux de croissance (années 6-10) %",
        min_value=0, max_value=20, value=5, step=1, key="gr2"
    ) / 100
    st.caption("Ralentissement naturel après 5 ans")

with dcf_col3:
    discount_rate = st.slider(
        "Taux d'actualisation %",
        min_value=6, max_value=15, value=10, step=1, key="dr"
    ) / 100
    st.caption("Rendement minimum exigé. Buffett utilise ~9-10%")

terminal_growth = st.slider(
    "Taux de croissance perpétuelle (terminal) %",
    min_value=1, max_value=5, value=3, step=1, key="tg"
) / 100

# Calcul DCF
if owner_earnings_base and shares_out and current_price:
    oe_per_share = owner_earnings_base / shares_out

    # Projection 10 ans
    projected_oe = []
    oe = oe_per_share
    for yr in range(1, 11):
        rate = growth_rate_1 if yr <= 5 else growth_rate_2
        oe = oe * (1 + rate)
        projected_oe.append(oe)

    # Valeur terminale (Gordon Growth Model)
    terminal_value = projected_oe[-1] * (1 + terminal_growth) / (discount_rate - terminal_growth)

    # Actualisation
    dcf_total = sum(oe / (1 + discount_rate) ** yr for yr, oe in enumerate(projected_oe, 1))
    dcf_total += terminal_value / (1 + discount_rate) ** 10

    intrinsic_value = dcf_total
    margin_of_safety = (intrinsic_value - current_price) / intrinsic_value * 100

    # Affichage résultats
    dcf_res_col1, dcf_res_col2, dcf_res_col3 = st.columns(3)

    with dcf_res_col1:
        st.markdown(f"""
        <div class="metric-tile">
            <div class="label">Valeur intrinsèque par action</div>
            <div class="value">{curr_sym}{intrinsic_value:,.2f}</div>
            <div class="sub">Selon le modèle DCF Buffett</div>
        </div>
        """, unsafe_allow_html=True)

    with dcf_res_col2:
        st.markdown(f"""
        <div class="metric-tile">
            <div class="label">Prix actuel</div>
            <div class="value">{curr_sym}{current_price:,.2f}</div>
            <div class="sub">{'Sous-évalué 👍' if current_price < intrinsic_value else 'Sur-évalué ⚠️'}</div>
        </div>
        """, unsafe_allow_html=True)

    with dcf_res_col3:
        mos_class = "margin-positive" if margin_of_safety > 20 else ("margin-neutral" if margin_of_safety > 0 else "margin-negative")
        mos_icon  = "🟢" if margin_of_safety > 20 else ("🟡" if margin_of_safety > 0 else "🔴")
        st.markdown(f"""
        <div class="metric-tile">
            <div class="label">Marge de sécurité</div>
            <div class="value {mos_class}">{mos_icon} {margin_of_safety:+.1f}%</div>
            <div class="sub">{'Excellent achat !' if margin_of_safety > 30 else ('Acceptable' if margin_of_safety > 10 else ('Faible' if margin_of_safety > 0 else 'Titre sur-évalué'))}</div>
        </div>
        """, unsafe_allow_html=True)

    # Graphique DCF
    st.markdown("<br>", unsafe_allow_html=True)
    years_label = [f"An {y}" for y in range(1, 11)]
    fig_dcf = go.Figure()
    fig_dcf.add_trace(go.Bar(
        x=years_label,
        y=projected_oe,
        marker_color=["#52b788" if i < 5 else "#c9a84c" for i in range(10)],
        name="Owner Earnings projetés / action",
        hovertemplate="An %{x} : " + curr_sym + "%{y:.2f}<extra></extra>"
    ))
    fig_dcf.add_hline(
        y=current_price, line_dash="dot", line_color="#e74c3c",
        annotation_text=f"Prix actuel : {curr_sym}{current_price:.2f}",
        annotation_position="right"
    )
    fig_dcf.update_layout(
        height=280, plot_bgcolor="#fafaf7", paper_bgcolor="#fafaf7",
        margin=dict(l=10, r=10, t=20, b=10),
        title=dict(text=f"Projection des Owner Earnings · Valeur intrinsèque : {curr_sym}{intrinsic_value:.2f}", font=dict(size=13)),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#eee", tickprefix=curr_sym),
    )
    st.plotly_chart(fig_dcf, use_container_width=True)

    # Comparaison multiples
    st.markdown("<h3>📊 Comparaison des multiples de valorisation</h3>", unsafe_allow_html=True)
    mult_data = {
        "Métrique": ["P/E actuel", "P/B actuel", "P/S actuel", "FCF Yield"],
        "Valeur":   [
            f"{pe_ratio:.1f}x" if pe_ratio else "N/A",
            f"{pb_ratio:.2f}x" if pb_ratio else "N/A",
            f"{ps_ratio:.2f}x" if ps_ratio else "N/A",
            f"{fcf_yield_val*100:.1f}%" if fcf_yield_val else "N/A"
        ],
        "Interprétation": [
            "Faible = potentiellement sous-évalué" if pe_ratio and pe_ratio < 15 else ("Élevé = croissance attendue" if pe_ratio and pe_ratio > 30 else "Modéré"),
            "< 1 = potentiellement sous-évalué" if pb_ratio and pb_ratio < 1 else ("Normal" if pb_ratio and pb_ratio < 3 else "Élevé"),
            "Normal" if ps_ratio and ps_ratio < 3 else "Élevé",
            "> 5% = bonne valeur" if fcf_yield_val and fcf_yield_val > 0.05 else "Faible FCF Yield"
        ]
    }
    st.table(pd.DataFrame(mult_data).set_index("Métrique"))

else:
    st.warning("⚠️ Données insuffisantes pour calculer la valeur intrinsèque (Owner Earnings non disponibles pour cet actif).")
    margin_of_safety = None
    intrinsic_value  = None

st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# RECOMMANDATION FINALE
# ─────────────────────────────────────────────
st.markdown('<div class="bv-card">', unsafe_allow_html=True)
st.markdown('<h2>🏆 Recommandation Finale</h2>', unsafe_allow_html=True)

# Décision
if margin_of_safety is not None:
    if buffett_score >= 60 and margin_of_safety >= 20:
        reco_class = "reco-buy"
        reco_emoji = "🟢"
        reco_title = "✅ Excellent Achat Long Terme"
        reco_text  = (f"<strong>{company_name}</strong> présente les caractéristiques d'une entreprise "
                      f"«merveilleuse» selon les critères de Warren Buffett. Avec un Buffett Score de "
                      f"<strong>{buffett_score}/100</strong> et une marge de sécurité de "
                      f"<strong>{margin_of_safety:.1f}%</strong>, ce titre offre une opportunité "
                      f"d'achat solide pour un investisseur patient sur 10-20 ans. "
                      f"Le prix actuel ({curr_sym}{current_price:.2f}) est significativement inférieur "
                      f"à la valeur intrinsèque estimée ({curr_sym}{intrinsic_value:.2f}).")
    elif buffett_score >= 45 and margin_of_safety >= 0:
        reco_class = "reco-buy"
        reco_emoji = "🟢"
        reco_title = "👍 Bon Achat – Potentiel Long Terme"
        reco_text  = (f"<strong>{company_name}</strong> est une entreprise de qualité correcte (score {buffett_score}/100) "
                      f"avec une marge de sécurité de {margin_of_safety:.1f}%. "
                      f"Convenable pour un investissement long terme, mais attendez idéalement une légère baisse du cours pour sécuriser davantage votre marge de sécurité.")
    elif buffett_score >= 55 and margin_of_safety < 0:
        reco_class = "reco-hold"
        reco_emoji = "🟡"
        reco_title = "⏳ Excellente Entreprise – Prix Trop Élevé"
        reco_text  = (f"<strong>{company_name}</strong> est une entreprise de grande qualité (score {buffett_score}/100), "
                      f"mais le cours actuel ({curr_sym}{current_price:.2f}) dépasse la valeur intrinsèque estimée "
                      f"({curr_sym}{intrinsic_value:.2f}). Ajoutez-la à votre liste de suivi et attendez une correction "
                      f"pour acheter avec une marge de sécurité suffisante (> 20%).")
    elif margin_of_safety < -20:
        reco_class = "reco-avoid"
        reco_emoji = "🔴"
        reco_title = "❌ Éviter – Titre Sur-Évalué"
        reco_text  = (f"<strong>{company_name}</strong> se négocie {abs(margin_of_safety):.1f}% au-dessus de sa valeur "
                      f"intrinsèque estimée. Même avec un score de qualité de {buffett_score}/100, l'absence de marge de "
                      f"sécurité rend cet investissement risqué selon les principes Buffett. Patience !")
    else:
        reco_class = "reco-hold"
        reco_emoji = "🟡"
        reco_title = "⚖️ Prix Correct – Surveiller"
        reco_text  = (f"<strong>{company_name}</strong> (score {buffett_score}/100) se négocie proche de sa valeur intrinsèque. "
                      f"Pas de marge de sécurité significative. À surveiller : une baisse de 15-20% serait idéale pour entrer.")
else:
    if buffett_score >= 65:
        reco_class = "reco-buy"
        reco_emoji = "🟢"
        reco_title = "👍 Entreprise de Qualité"
        reco_text  = (f"<strong>{company_name}</strong> affiche un excellent Buffett Score de {buffett_score}/100. "
                      f"Les données financières disponibles suggèrent une entreprise solide. "
                      f"La valeur intrinsèque n'a pu être calculée précisément — complétez l'analyse avec une clé API FMP.")
    else:
        reco_class = "reco-hold"
        reco_emoji = "🟡"
        reco_title = "⚠️ Analyse Incomplète"
        reco_text  = f"Données insuffisantes pour une recommandation complète. Score partiel : {buffett_score}/100."

st.markdown(f"""
<div class="{reco_class}">
    <div class="reco-title">{reco_title}</div>
    <div class="reco-text">{reco_text}</div>
    <div style="margin-top:1rem;padding-top:1rem;border-top:1px solid rgba(255,255,255,0.2);font-size:0.85rem;opacity:0.75;font-style:italic;">
        ⚠️ Ceci est une analyse automatique à titre éducatif, basée sur des données publiques. 
        Elle ne constitue pas un conseil en investissement. Faites toujours votre propre analyse.
    </div>
</div>
""", unsafe_allow_html=True)

# Citation Buffett
buffett_quotes = [
    "« Notre période de détention préférée est : pour toujours. »",
    "« Le risque vient de ne pas savoir ce que l'on fait. »",
    "« Achetez des actions comme vous achetez des légumes, pas comme du parfum. »",
    "« Peu importe à quelle hauteur les eaux montent, si vous avez un bon bateau. »",
    "« La règle n°1 : ne jamais perdre d'argent. Règle n°2 : ne jamais oublier la règle n°1. »",
]
import random
q = buffett_quotes[hash(ticker_sym) % len(buffett_quotes)]
st.markdown(f"""
<div style="text-align:center;margin-top:1.5rem;padding:1rem;background:rgba(201,168,76,0.08);border-radius:10px;">
    <span style="font-style:italic;color:#7a6010;font-size:1rem;">{q} — <strong>Warren Buffett</strong></span>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# RISQUES PRINCIPAUX
# ─────────────────────────────────────────────
st.markdown('<div class="bv-card">', unsafe_allow_html=True)
st.markdown('<h2>⚠️ Risques Principaux</h2>', unsafe_allow_html=True)

risks = []
if beta and beta > 1.5:   risks.append(f"📉 **Forte volatilité** : Beta de {beta:.2f} (> 1.5 = titre très sensible aux mouvements du marché)")
if beta and beta > 0:     pass
if debt_eq and debt_eq/100 > 2: risks.append(f"💳 **Endettement élevé** : Ratio dettes/capitaux propres de {debt_eq/100:.2f} – surveiller la capacité de remboursement")
if pe_ratio and pe_ratio > 35:  risks.append(f"📊 **Valorisation élevée** : P/E de {pe_ratio:.1f}x – laisse peu de marge en cas de déception")
if op_margin and op_margin < 0.05: risks.append("📉 **Marges faibles** : Marge opérationnelle < 5% – entreprise vulnérable aux chocs de coûts")
if current_r and current_r < 1: risks.append(f"💧 **Liquidité tendue** : Ratio courant de {current_r:.2f} – risque de difficulté à court terme")
if sector in ("Energy", "Basic Materials"): risks.append("🛢️ **Secteur cyclique** : Sensible aux cycles économiques et aux prix des matières premières")
if sector == "Technology" and pe_ratio and pe_ratio > 40: risks.append("💻 **Valorisation tech agressive** : Le secteur tech est souvent sujet à des corrections brutales")

general_risks = [
    "🌍 **Risque macroéconomique** : Hausse des taux, inflation, récession peuvent affecter tous les secteurs",
    "🏛️ **Risque réglementaire** : Changements législatifs pouvant impacter l'activité",
    "🔄 **Disruption technologique** : Même les entreprises solides peuvent être challengées",
]
risks.extend(general_risks)

for risk in risks:
    st.markdown(f"- {risk}")

st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ACTUALITÉS RÉCENTES
# ─────────────────────────────────────────────
if news:
    st.markdown('<div class="bv-card">', unsafe_allow_html=True)
    st.markdown('<h2>📰 Actualités Récentes</h2>', unsafe_allow_html=True)

    for article in news[:5]:
        title    = article.get("title", "")
        pub_time = article.get("providerPublishTime", 0)
        link     = article.get("link", "#")
        publisher= article.get("publisher", "")
        if pub_time:
            pub_date = datetime.fromtimestamp(pub_time).strftime("%d/%m/%Y")
        else:
            pub_date = "Date inconnue"
        st.markdown(f"""
        <div style="padding:0.6rem 0;border-bottom:1px solid #f0ede6;">
            <a href="{link}" target="_blank" style="color:var(--green-dark);font-weight:600;text-decoration:none;font-size:0.95rem;">
                {title}
            </a>
            <div style="color:#888;font-size:0.8rem;margin-top:0.2rem;">{publisher} · {pub_date}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# EXPORT PDF
# ─────────────────────────────────────────────
st.markdown('<div class="bv-card">', unsafe_allow_html=True)
st.markdown('<h2>📄 Exporter le Rapport</h2>', unsafe_allow_html=True)

def generate_pdf_report():
    """Génère un rapport PDF simple avec ReportLab."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
        from reportlab.lib import colors
        from reportlab.lib.units import cm
        import io

        buffer = io.BytesIO()
        doc    = SimpleDocTemplate(buffer, pagesize=A4,
                                   leftMargin=2*cm, rightMargin=2*cm,
                                   topMargin=2*cm, bottomMargin=2*cm)
        styles = getSampleStyleSheet()

        green_dark  = colors.HexColor("#1a3a2a")
        green_light = colors.HexColor("#52b788")
        gold        = colors.HexColor("#c9a84c")
        cream       = colors.HexColor("#f8f5ef")

        title_style = ParagraphStyle("Title", parent=styles["Title"],
                                     textColor=green_dark, fontSize=22, spaceAfter=6)
        h2_style    = ParagraphStyle("H2", parent=styles["Heading2"],
                                     textColor=green_dark, fontSize=14, spaceBefore=14, spaceAfter=4)
        body_style  = ParagraphStyle("Body", parent=styles["Normal"],
                                     fontSize=10, leading=16)
        label_style = ParagraphStyle("Label", parent=styles["Normal"],
                                     fontSize=9, textColor=colors.grey)

        story = []

        # Titre
        story.append(Paragraph("🏦 BuffettVision", title_style))
        story.append(Paragraph(f"Rapport d'analyse – {company_name} ({ticker_sym})", h2_style))
        story.append(Paragraph(f"Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}", label_style))
        story.append(HRFlowable(width="100%", thickness=2, color=gold, spaceAfter=12))

        # Infos de base
        story.append(Paragraph("Informations Générales", h2_style))
        base_data = [
            ["Entreprise", company_name],
            ["Secteur", sector],
            ["Prix actuel", f"{curr_sym}{current_price:.2f}" if current_price else "N/A"],
            ["Capitalisation", fmt_big(market_cap, curr_sym)],
            ["P/E ratio", f"{pe_ratio:.1f}x" if pe_ratio else "N/A"],
        ]
        t = Table(base_data, colWidths=[5*cm, 10*cm])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (0,-1), cream),
            ("TEXTCOLOR", (0,0), (0,-1), green_dark),
            ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
            ("GRID", (0,0), (-1,-1), 0.5, colors.lightgrey),
            ("PADDING", (0,0), (-1,-1), 6),
        ]))
        story.append(t)
        story.append(Spacer(1, 0.4*cm))

        # Buffett Score
        story.append(Paragraph("Buffett Score & Analyse", h2_style))
        story.append(Paragraph(f"<b>Score global : {buffett_score}/100</b>", body_style))
        story.append(Spacer(1, 0.2*cm))
        for crit, (pts, max_pts, icon) in score_details.items():
            story.append(Paragraph(f"{icon} {crit} : {pts}/{max_pts} pts", body_style))

        story.append(Spacer(1, 0.4*cm))

        # Valeur intrinsèque
        story.append(Paragraph("Valeur Intrinsèque (DCF Buffett)", h2_style))
        if intrinsic_value and current_price:
            iv_data = [
                ["Valeur intrinsèque estimée", f"{curr_sym}{intrinsic_value:.2f}"],
                ["Prix actuel", f"{curr_sym}{current_price:.2f}"],
                ["Marge de sécurité", f"{margin_of_safety:+.1f}%"],
            ]
            t2 = Table(iv_data, colWidths=[7*cm, 8*cm])
            t2.setStyle(TableStyle([
                ("BACKGROUND", (0,0), (0,-1), cream),
                ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
                ("GRID", (0,0), (-1,-1), 0.5, colors.lightgrey),
                ("PADDING", (0,0), (-1,-1), 6),
            ]))
            story.append(t2)
        else:
            story.append(Paragraph("Données insuffisantes pour le calcul DCF.", body_style))

        story.append(Spacer(1, 0.4*cm))

        # Recommandation
        story.append(Paragraph("Recommandation Finale", h2_style))
        story.append(Paragraph(f"<b>{reco_title}</b>", body_style))
        clean_text = reco_text.replace("<strong>","<b>").replace("</strong>","</b>")
        story.append(Paragraph(clean_text, body_style))

        story.append(Spacer(1, 0.8*cm))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.lightgrey))
        story.append(Paragraph("⚠️ Ce rapport est fourni à titre éducatif uniquement et ne constitue pas un conseil en investissement.", label_style))

        doc.build(story)
        return buffer.getvalue()

    except ImportError:
        return None

pdf_bytes = generate_pdf_report()
if pdf_bytes:
    st.download_button(
        label="📥 Télécharger le rapport PDF complet",
        data=pdf_bytes,
        file_name=f"BuffettVision_{ticker_sym}_{datetime.now().strftime('%Y%m%d')}.pdf",
        mime="application/pdf",
        use_container_width=True,
    )
else:
    st.info("📦 Installez `reportlab` pour activer l'export PDF : `pip install reportlab`")

st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="gold-divider"></div>
<div style="text-align:center;color:#aaa;font-size:0.82rem;padding:1rem 0 2rem;">
    🏦 <strong>BuffettVision</strong> · Analyse fondamentale long terme · Données : Yahoo Finance (yfinance) · 
    <em>Aucun conseil en investissement – À titre éducatif uniquement</em>
</div>
""", unsafe_allow_html=True)
