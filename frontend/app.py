import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Non-Flow Process Calculator",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* ---- Google Font ---- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ---- Global reset ---- */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ---- App background ---- */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        min-height: 100vh;
    }

    /* ---- Sidebar ---- */
    section[data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(16px);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    section[data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stNumberInput label,
    section[data-testid="stSidebar"] .stSlider label {
        font-weight: 500;
        letter-spacing: 0.02em;
    }

    /* ---- Sidebar header ---- */
    section[data-testid="stSidebar"] h2 {
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        color: #a78bfa !important;
        margin-bottom: 1.2rem !important;
    }

    /* ---- Sidebar selectbox / inputs ---- */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        background: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(167,139,250,0.35) !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
    }

    /* ---- Page title ---- */
    .page-title {
        font-size: 2.4rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.2rem;
    }
    .page-subtitle {
        font-size: 0.95rem;
        color: rgba(226,232,240,0.55);
        font-weight: 400;
        margin-bottom: 2rem;
    }

    /* ---- Info / description card ---- */
    .info-card {
        background: rgba(167, 139, 250, 0.10);
        border: 1px solid rgba(167, 139, 250, 0.30);
        border-radius: 14px;
        padding: 1rem 1.4rem;
        color: #c4b5fd;
        font-size: 0.92rem;
        font-weight: 450;
        line-height: 1.6;
        margin-bottom: 1.6rem;
    }

    /* ---- Calculate button ---- */
    div.stButton > button {
        background: linear-gradient(135deg, #7c3aed, #2563eb);
        color: #ffffff;
        border: none;
        border-radius: 12px;
        padding: 0.65rem 2.2rem;
        font-size: 1rem;
        font-weight: 600;
        letter-spacing: 0.03em;
        cursor: pointer;
        transition: all 0.25s ease;
        box-shadow: 0 4px 20px rgba(124, 58, 237, 0.45);
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 28px rgba(124, 58, 237, 0.6);
        filter: brightness(1.12);
    }

    /* ---- Chart cards ---- */
    .chart-card {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 1.2rem;
        backdrop-filter: blur(10px);
    }

    /* ---- Section subheaders ---- */
    h3 {
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        color: #a78bfa !important;
        letter-spacing: 0.04em !important;
        text-transform: uppercase !important;
        margin-bottom: 0.6rem !important;
    }

    /* ---- Download button ---- */
    div.stDownloadButton > button {
        background: rgba(52, 211, 153, 0.15) !important;
        color: #34d399 !important;
        border: 1px solid rgba(52, 211, 153, 0.40) !important;
        border-radius: 10px !important;
        padding: 0.5rem 1.6rem !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }
    div.stDownloadButton > button:hover {
        background: rgba(52, 211, 153, 0.28) !important;
        box-shadow: 0 4px 16px rgba(52,211,153,0.3) !important;
        transform: translateY(-1px) !important;
    }

    /* ---- Spinner ---- */
    .stSpinner > div {
        border-top-color: #a78bfa !important;
    }

    /* ---- Error / success alerts ---- */
    div[data-testid="stAlert"] {
        border-radius: 12px !important;
    }

    /* ---- Divider ---- */
    hr {
        border-color: rgba(255,255,255,0.08) !important;
    }

    /* ---- Scrollbar ---- */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb {
        background: rgba(167,139,250,0.4);
        border-radius: 4px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Plotly dark template shared config ────────────────────────────────────────
CHART_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255,255,255,0.03)",
    font=dict(family="Inter, sans-serif", color="#e2e8f0"),
    margin=dict(l=40, r=20, t=50, b=40),
    xaxis=dict(
        gridcolor="rgba(255,255,255,0.06)",
        linecolor="rgba(255,255,255,0.12)",
        tickfont=dict(size=11),
    ),
    yaxis=dict(
        gridcolor="rgba(255,255,255,0.06)",
        linecolor="rgba(255,255,255,0.12)",
        tickfont=dict(size=11),
    ),
    title=dict(font=dict(size=15, weight=700), x=0.02),
)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<p class="page-title">⚙️ Non-Flow Process Calculator</p>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">Thermodynamic state-point analysis powered by CoolProp</p>', unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🛠 Process Inputs")
    st.markdown("---")

    PROCESS_LABELS = {
        "constant_volume": "Constant Volume",
        "constant_pressure": "Constant Pressure",
        "isothermal": "Isothermal",
        "adiabatic": "Adiabatic",
        "polytropic": "Polytropic",
    }
    process_key = st.selectbox(
        "Process Type",
        list(PROCESS_LABELS.keys()),
        format_func=lambda k: PROCESS_LABELS[k],
    )
    st.markdown("")
    T0 = st.number_input("Initial Temperature (K)", value=300.0, min_value=1.0)
    V0 = st.number_input("Initial Specific Volume (m³/kg)", value=1.0, min_value=0.0001, format="%.4f")
    n_points = st.slider("Number of State Points", min_value=5, max_value=50, value=20)
    st.markdown("---")
    calc_clicked = st.button("⚡ Calculate", use_container_width=True)

# ── Process description card ──────────────────────────────────────────────────
PROCESS_DESCRIPTIONS = {
    "constant_volume": "🔒 <b>Isochoric Process</b> — Volume is held constant. Pressure varies directly with temperature.",
    "constant_pressure": "📏 <b>Isobaric Process</b> — Pressure is held constant. Volume changes proportionally with temperature.",
    "isothermal": "🌡️ <b>Isothermal Process</b> — Temperature is constant. Pressure decreases as volume increases.",
    "adiabatic": "❄️ <b>Adiabatic Process</b> — No heat transfer. P·Vᵞ = constant.",
    "polytropic": "🔄 <b>Polytropic Process</b> — Generalized process: P·Vⁿ = constant.",
}
st.markdown(
    f'<div class="info-card">{PROCESS_DESCRIPTIONS[process_key]}</div>',
    unsafe_allow_html=True,
)

# ── Calculation & results ────────────────────────────────────────────────────
if calc_clicked:
    api_url = (
        f"http://127.0.0.1:8000/process/{process_key}"
        f"?T0={T0}&V0={V0}&n_points={n_points}"
    )

    with st.spinner("Fetching state points from backend…"):
        try:
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as exc:
            st.error(f"⚠️ Backend error: {exc}")
            data = []

    if data:
        df = pd.DataFrame(data)

        col1, col2 = st.columns(2, gap="medium")

        # ── T-s Chart ──
        with col1:
            st.subheader("T-s Diagram")
            fig1 = go.Figure()
            fig1.add_trace(
                go.Scatter(
                    x=df["s"],
                    y=df["T"],
                    mode="lines+markers",
                    name="T-s",
                    line=dict(color="#a78bfa", width=2.5),
                    marker=dict(size=6, color="#c4b5fd", line=dict(width=1, color="#7c3aed")),
                    hovertemplate="s = %{x:.4f}<br>T = %{y:.2f} K<extra></extra>",
                )
            )
            fig1.update_layout(
                title="Temperature vs. Entropy",
                xaxis_title="Specific Entropy s (kJ/kg·K)",
                yaxis_title="Temperature T (K)",
                **CHART_LAYOUT,
            )
            st.plotly_chart(fig1, use_container_width=True)

        # ── P-v Chart ──
        with col2:
            st.subheader("P-v Diagram")
            fig2 = go.Figure()
            fig2.add_trace(
                go.Scatter(
                    x=df["v"],
                    y=df["P"],
                    mode="lines+markers",
                    name="P-v",
                    line=dict(color="#34d399", width=2.5),
                    marker=dict(size=6, color="#6ee7b7", line=dict(width=1, color="#059669")),
                    hovertemplate="v = %{x:.4f}<br>P = %{y:.2f} Pa<extra></extra>",
                )
            )
            fig2.update_layout(
                title="Pressure vs. Specific Volume",
                xaxis_title="Specific Volume v (m³/kg)",
                yaxis_title="Pressure P (Pa)",
                **CHART_LAYOUT,
            )
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("---")

        # ── Summary metrics ──
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Points", len(df))
        m2.metric("T min → max (K)", f"{df['T'].min():.1f} → {df['T'].max():.1f}")
        m3.metric("P min → max (Pa)", f"{df['P'].min():.1f} → {df['P'].max():.1f}")
        m4.metric("v min → max (m³/kg)", f"{df['v'].min():.4f} → {df['v'].max():.4f}")

        st.markdown("")

        # ── Download ──
        csv = df.to_csv(index=False)
        st.download_button(
            label="⬇️  Download State Points as CSV",
            data=csv,
            file_name="process_points.csv",
            mime="text/csv",
        )
