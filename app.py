import streamlit as st
import streamlit.components.v1 as components
import os
import requests
import urllib.parse
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dotenv import load_dotenv
from google import genai
from datetime import datetime, date, timedelta

# ─────────────────────────────────────────────
# Config & Setup
# ─────────────────────────────────────────────
load_dotenv()

st.set_page_config(
    page_title="Voyanta AI — Generative AI Travel Intelligence",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# Ultra-Modern Glassmorphic CSS Design System
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    :root {
        --primary: #6366f1;
        --primary-dark: #4f46e5;
        --secondary: #ec4899;
        --accent: #06b6d4;
        --bg-glass: rgba(255, 255, 255, 0.85);
        --border-glass: rgba(226, 232, 240, 0.8);
        --text-main: #0f172a;
        --text-muted: #64748b;
    }

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Animated Hero Header */
    .hero-container {
        position: relative;
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 40%, #4338ca 70%, #6366f1 100%);
        padding: 3rem 2.5rem 2.5rem;
        border-radius: 24px;
        color: white;
        margin-bottom: 2rem;
        overflow: hidden;
        box-shadow: 0 20px 45px -15px rgba(49, 46, 129, 0.5), 0 0 0 1px rgba(255, 255, 255, 0.1);
    }
    .hero-container::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(236, 72, 153, 0.25) 0%, transparent 70%);
        border-radius: 50%;
        pointer-events: none;
    }
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        margin: 0;
        background: linear-gradient(to right, #ffffff, #e0e7ff, #fbcfe8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.15;
    }
    .hero-subtitle {
        font-size: 1.15rem;
        font-weight: 400;
        color: #c7d2fe;
        margin-top: 0.75rem;
        max-width: 680px;
        line-height: 1.6;
    }

    /* Live Status Badges in Hero */
    .status-strip {
        display: flex;
        flex-wrap: wrap;
        gap: 0.6rem;
        margin-top: 1.4rem;
    }
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        padding: 0.35rem 0.85rem;
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 500;
        color: #f1f5f9;
    }
    .pulse-dot {
        width: 8px;
        height: 8px;
        background: #10b981;
        border-radius: 50%;
        box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
        100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }

    /* Metric Cards */
    .metric-card {
        background: white;
        border-radius: 18px;
        padding: 1.3rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.05);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        display: flex;
        align-items: center;
        gap: 1.1rem;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 25px -4px rgba(99, 102, 241, 0.15);
        border-color: #cbd5e1;
    }
    .metric-icon-wrap {
        width: 52px;
        height: 52px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.6rem;
    }
    .metric-info h4 {
        margin: 0;
        font-size: 1.4rem;
        font-weight: 700;
        color: #0f172a;
    }
    .metric-info p {
        margin: 0;
        font-size: 0.82rem;
        font-weight: 500;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    /* Boarding Pass Card */
    .boarding-pass {
        background: white;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.08);
        overflow: hidden;
        margin-bottom: 2rem;
        position: relative;
    }
    .boarding-pass-header {
        background: linear-gradient(135deg, #4338ca, #6366f1);
        color: white;
        padding: 1.2rem 1.8rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .boarding-pass-body {
        padding: 1.8rem;
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
        gap: 1.2rem;
        border-bottom: 2px dashed #e2e8f0;
    }
    .pass-field label {
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        color: #94a3b8;
        letter-spacing: 0.06em;
        display: block;
        margin-bottom: 0.2rem;
    }
    .pass-field span {
        font-size: 1.05rem;
        font-weight: 700;
        color: #0f172a;
    }
    .boarding-pass-footer {
        padding: 1rem 1.8rem;
        background: #f8fafc;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.85rem;
        color: #64748b;
    }

    /* Weather Card */
    .weather-showcase {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 50%, #075985 100%);
        color: white;
        border-radius: 20px;
        padding: 1.6rem;
        box-shadow: 0 10px 25px -5px rgba(2, 132, 199, 0.4);
        position: relative;
        overflow: hidden;
    }
    .weather-showcase::after {
        content: '⛅';
        position: absolute;
        right: 15px;
        bottom: 10px;
        font-size: 6rem;
        opacity: 0.15;
        pointer-events: none;
    }
    .weather-main-temp {
        font-size: 3.2rem;
        font-weight: 800;
        line-height: 1;
        margin: 0.6rem 0;
    }
    .weather-badge-row {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        margin-top: 1rem;
    }
    .weather-sub-badge {
        background: rgba(255, 255, 255, 0.18);
        backdrop-filter: blur(8px);
        padding: 0.35rem 0.75rem;
        border-radius: 10px;
        font-size: 0.82rem;
        font-weight: 500;
    }

    /* Section Cards */
    .glass-section {
        background: white;
        border-radius: 20px;
        padding: 1.6rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.05);
        margin-bottom: 1.5rem;
    }
    .section-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.85rem 1.8rem;
        font-size: 1.05rem;
        font-weight: 700;
        letter-spacing: -0.01em;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 14px 0 rgba(79, 70, 229, 0.35);
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px 0 rgba(79, 70, 229, 0.45);
        background: linear-gradient(135deg, #4338ca 0%, #6d28d9 100%);
        color: white;
    }

    /* Chips for Popular Destinations */
    .chip-btn {
        display: inline-block;
        padding: 0.4rem 0.9rem;
        border-radius: 9999px;
        background: #f1f5f9;
        color: #334155;
        font-size: 0.85rem;
        font-weight: 600;
        border: 1px solid #e2e8f0;
        cursor: pointer;
        transition: all 0.2s;
        text-decoration: none;
    }
    .chip-btn:hover {
        background: #e0e7ff;
        color: #4338ca;
        border-color: #c7d2fe;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 8px 16px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Helpers: Live APIs
# ─────────────────────────────────────────────
def get_weather(city: str, api_key: str) -> dict | None:
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        r = requests.get(url, timeout=8)
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None

def get_forecast(city: str, api_key: str) -> dict | None:
    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric&cnt=8"
        r = requests.get(url, timeout=8)
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None

def get_coordinates(city: str) -> tuple[float, float]:
    try:
        url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(city)}&format=json&limit=1"
        headers = {"User-Agent": "VoyantaAI-TravelIntelligence/2.0"}
        r = requests.get(url, headers=headers, timeout=8)
        data = r.json()
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])
    except Exception:
        pass
    return 20.5937, 78.9629

def get_exchange_rates(base: str = "USD") -> dict:
    try:
        r = requests.get(f"https://open.er-api.com/v6/latest/{base}", timeout=8)
        data = r.json()
        return data.get("rates", {})
    except Exception:
        return {"INR": 83.5, "EUR": 0.92, "GBP": 0.79, "AED": 3.67, "JPY": 155.0}

# ─────────────────────────────────────────────
# Gemini AI Itinerary Generator
# ─────────────────────────────────────────────
def generate_itinerary(
    destination: str,
    days: int,
    budget: str,
    interests: list[str],
    travel_style: str,
    start_date: date,
    weather_info: str,
    gemini_api_key: str,
):
    client = genai.Client(api_key=gemini_api_key)
    interests_str = ", ".join(interests) if interests else "Sightseeing & Exploration"

    prompt = f"""
You are Voyanta AI, an elite Generative AI Travel Intelligence system designing precision itineraries.
Create a polished, highly specific travel dossier with the following specs:

- **Destination:** {destination}
- **Trip Duration:** {days} Days (Starting {start_date.strftime('%d %B %Y')})
- **Budget Tier:** {budget}
- **Travel Persona:** {travel_style}
- **Special Interests:** {interests_str}
- **Current Ground Weather:** {weather_info}

Structure your response with clean Markdown:

### 🌟 Executive Trip Summary
(A concise, vibrant overview of the journey, optimal vibe, and highlight reel)

### 📅 Day-by-Day Masterplan
For each day (Day 1 to Day {days}):
- **Morning (09:00 - 12:30):** Landmark / Activity name, practical timing, entry cost in ₹ (INR) and $ (USD).
- **Afternoon (13:00 - 17:00):** Hidden gem or experience, lunch spot recommendation.
- **Evening & Night (18:00 onwards):** Sunset / Nightlife / Fine dining spot with dish recommendation.
- **💡 Insider Tip:** 1 actionable secret for that specific day.

### 🍽️ Curated Culinary Guide (Top 5 Local Eats)
(5 authentic dishes / iconic eateries with price ranges)

### 💰 Categorized Budget Matrix
(Estimated total breakdown for Stay, Dining, Transit, Activities & Contingency)

### 🎒 Weather-Smart Packing List
(Specific gear, clothing, and footwear recommended for {destination}'s current climate)

### 🚨 Safety & Local Etiquette Protocol
(Key local laws, scam warnings, emergency dial numbers, and etiquette tips)
"""

    for event in client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt,
        stream=True,
    ):
        if event.event_type == "step.delta" and event.delta.type == "text":
            yield event.delta.text

# ─────────────────────────────────────────────
# Visual Charts
# ─────────────────────────────────────────────
def build_budget_chart(budget_level: str, days: int) -> go.Figure:
    mult = {"Budget (₹4k–₹8k/day)": 1.0, "Comfort (₹8k–₹18k/day)": 2.2, "Luxury Elite (₹20k+/day)": 4.5}
    base = mult.get(budget_level, 1.5)
    categories = ["🏨 Accommodation", "🍽️ Gastronomy", "🚗 Local Transit", "🎟️ Experiences", "🛍️ Shopping & Perks"]
    daily = [2200 * base, 1400 * base, 850 * base, 1100 * base, 700 * base]
    totals = [round(v * days) for v in daily]

    colors = ["#6366f1", "#8b5cf6", "#ec4899", "#06b6d4", "#10b981"]

    fig = go.Figure(go.Bar(
        x=categories,
        y=totals,
        marker=dict(color=colors, line=dict(width=0)),
        text=[f"₹{v:,.0f}" for v in totals],
        textposition="outside",
        textfont=dict(family="Plus Jakarta Sans", size=13, color="#0f172a"),
    ))
    fig.update_layout(
        title=dict(text=f"<b>Estimated Expense Allocation ({days} Days)</b>", font=dict(size=16, color="#0f172a")),
        yaxis=dict(title="Estimated Cost (INR ₹)", gridcolor="#f1f5f9"),
        xaxis=dict(gridcolor="#f1f5f9"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans"),
        margin=dict(l=10, r=10, t=40, b=10),
        height=320,
    )
    return fig

def build_forecast_chart(forecast_data: dict) -> go.Figure | None:
    if not forecast_data or "list" not in forecast_data:
        return None
    items = forecast_data["list"][:8]
    dates = [i["dt_txt"][11:16] for i in items]
    temps = [round(i["main"]["temp"], 1) for i in items]
    feels = [round(i["main"]["feels_like"], 1) for i in items]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, y=temps, name="Temp (°C)",
        line=dict(color="#38bdf8", width=3),
        mode="lines+markers+text",
        text=[f"{t}°" for t in temps],
        textposition="top center",
        fill="tozeroy",
        fillcolor="rgba(56, 189, 248, 0.15)",
    ))
    fig.add_trace(go.Scatter(
        x=dates, y=feels, name="Feels Like (°C)",
        line=dict(color="#f43f5e", width=2, dash="dot"),
    ))
    fig.update_layout(
        title=dict(text="<b>Hourly Weather Trajectory</b>", font=dict(size=14, color="#ffffff")),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        xaxis=dict(showgrid=False, tickfont=dict(color="#ffffff")),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans"),
        legend=dict(orientation="h", font=dict(color="#ffffff"), yanchor="bottom", y=1.02),
        margin=dict(l=10, r=10, t=40, b=10),
        height=210,
    )
    return fig

def build_geo_map(city: str, lat: float, lon: float) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scattergeo(
        lat=[lat], lon=[lon],
        mode="markers+text",
        text=[f"📍 {city}"],
        textposition="top center",
        marker=dict(size=18, color="#6366f1", symbol="circle", line=dict(width=3, color="white")),
        name=city,
        textfont=dict(family="Plus Jakarta Sans", size=14, color="#1e1b4b"),
    ))
    fig.update_layout(
        geo=dict(
            showland=True, landcolor="#f8fafc",
            showocean=True, oceancolor="#e0f2fe",
            showcountries=True, countrycolor="#cbd5e1",
            showcoastlines=True, coastlinecolor="#94a3b8",
            projection_type="natural earth",
            center=dict(lat=lat, lon=lon),
            projection_scale=7,
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=380,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
    )
    return fig

# ─────────────────────────────────────────────
# Sidebar: Control Center
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:0.5rem;">
        <span style="font-size:2rem;">✈️</span>
        <div>
            <h2 style="margin:0; font-size:1.4rem; font-weight:800; color:#1e1b4b;">Voyanta AI</h2>
            <p style="margin:0; font-size:0.72rem; color:#64748b; font-weight:600; text-transform:uppercase;">Generative AI Travel Intelligence</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    # API Keys Configuration
    default_gemini = os.getenv("GEMINI_API_KEY", "")
    if default_gemini == "your_gemini_api_key_here":
        default_gemini = ""
    default_weather = os.getenv("OPENWEATHER_API_KEY", "")
    if default_weather == "your_openweather_api_key_here":
        default_weather = ""

    with st.expander("🔑 API Credentials", expanded=not bool(default_gemini)):
        gemini_key = st.text_input(
            "Gemini AI Key",
            value=default_gemini,
            type="password",
            help="Free key from https://aistudio.google.com",
        )
        if default_gemini:
            st.caption("🟢 Gemini API connected from `.env`")

        weather_key = st.text_input(
            "OpenWeather Key",
            value=default_weather,
            type="password",
            help="Free key from https://openweathermap.org/api",
        )
        if default_weather:
            st.caption("🟢 Weather API connected from `.env`")

    st.markdown("### 🎯 Trip Specifications")

    # Quick selection chips
    st.markdown("<p style='font-size:0.75rem; font-weight:600; color:#64748b; margin-bottom:0.3rem;'>POPULAR DESTINATIONS</p>", unsafe_allow_html=True)
    chip_cols = st.columns(4)
    quick_dest = None
    if chip_cols[0].button("Goa"): quick_dest = "Goa"
    if chip_cols[1].button("Paris"): quick_dest = "Paris"
    if chip_cols[2].button("Bali"): quick_dest = "Bali"
    if chip_cols[3].button("Tokyo"): quick_dest = "Tokyo"

    chip_cols2 = st.columns(4)
    if chip_cols2[0].button("Manali"): quick_dest = "Manali"
    if chip_cols2[1].button("Dubai"): quick_dest = "Dubai"
    if chip_cols2[2].button("Jaipur"): quick_dest = "Jaipur"
    if chip_cols2[3].button("London"): quick_dest = "London"

    current_dest_val = quick_dest or st.session_state.get("target_destination", "")
    destination = st.text_input("📍 Destination City / Country", value=current_dest_val, placeholder="e.g. Rome, Srinagar, Kyoto...")
    st.session_state["target_destination"] = destination

    col_d1, col_d2 = st.columns(2)
    with col_d1:
        start_date = st.date_input("🛫 Start Date", value=date.today() + timedelta(days=7))
    with col_d2:
        days = st.slider("📅 Duration (Days)", 1, 14, 4)

    budget = st.selectbox(
        "💰 Budget Tier",
        ["Budget (₹4k–₹8k/day)", "Comfort (₹8k–₹18k/day)", "Luxury Elite (₹20k+/day)"],
        index=1,
    )
    travel_style = st.selectbox(
        "🎒 Travel Persona",
        ["Cultural & Heritage", "Adventure & Adrenaline", "Romantic & Leisure",
         "Culinary & Street Food Explorer", "Solo Backpacker", "Family & Kids"],
    )
    interests = st.multiselect(
        "✨ Curated Interests",
        ["Hidden Gems", "Iconic Landmarks", "Sunset Viewpoints", "Art & Museums",
         "Cafes & Nightlife", "Trekking & Nature", "Local Markets", "Beach Clubs", "Photography"],
        default=["Hidden Gems", "Local Markets", "Sunset Viewpoints"],
    )

    generate_btn = st.button("✨ Architect My Itinerary")

    st.markdown("---")
    # Live Currency Converter Widget
    with st.expander("💱 Live Forex Calculator", expanded=False):
        rates = get_exchange_rates("USD")
        inr_rate = rates.get("INR", 83.5)
        eur_rate = rates.get("EUR", 0.92)
        gbp_rate = rates.get("GBP", 0.79)
        usd_amount = st.number_input("Amount in USD ($)", value=100, step=25)
        st.markdown(f"""
        - **INR (₹):** `₹{usd_amount * inr_rate:,.2f}`
        - **EUR (€):** `€{usd_amount * eur_rate:,.2f}`
        - **GBP (£):** `£{usd_amount * gbp_rate:,.2f}`
        """)

# ─────────────────────────────────────────────
# Main View: Dynamic Hero Banner
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="hero-container">
    <h1 class="hero-title">Voyanta AI</h1>
    <p class="hero-subtitle">Generative AI Travel Intelligence with real-time satellite telemetry, street view navigation, live meteorology, and dynamic budgeting.</p>
    <div class="status-strip">
        <div class="status-pill"><div class="pulse-dot"></div> Gemini 3.8 Flash Engine</div>
        <div class="status-pill">📡 OpenWeather Live Feed</div>
        <div class="status-pill">🛰️ Google Satellite Stream</div>
        <div class="status-pill">💱 Real-Time Forex</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Landing State or Active Destination State
# ─────────────────────────────────────────────
if not destination:
    # Showcase Cards on Initial Load
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="glass-section" style="text-align:center;">
            <div style="font-size:2.5rem; margin-bottom:0.5rem;">🤖</div>
            <h3 style="font-size:1.2rem; font-weight:700; color:#1e1b4b;">Autonomous Planner</h3>
            <p style="color:#64748b; font-size:0.9rem;">Powered by Google Gemini 3.8 Flash with live contextual prompts, cost estimation, and daily agendas.</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="glass-section" style="text-align:center;">
            <div style="font-size:2.5rem; margin-bottom:0.5rem;">🗺️</div>
            <h3 style="font-size:1.2rem; font-weight:700; color:#1e1b4b;">360° Street View & Satellite</h3>
            <p style="color:#64748b; font-size:0.9rem;">Seamless Google Road, high-res satellite photography, and 360° street view previews right on screen.</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="glass-section" style="text-align:center;">
            <div style="font-size:2.5rem; margin-bottom:0.5rem;">📊</div>
            <h3 style="font-size:1.2rem; font-weight:700; color:#1e1b4b;">Smart Financial Matrix</h3>
            <p style="color:#64748b; font-size:0.9rem;">Visual cost modeling in ₹ INR & $ USD with currency conversion and expense category breakdown.</p>
        </div>
        """, unsafe_allow_html=True)

    st.info("👈 **Select a popular destination** or type any city in the sidebar to start your journey!")
    st.stop()

# ─────────────────────────────────────────────
# Fetch Real-Time Data
# ─────────────────────────────────────────────
with st.spinner(f"🌐 Gathering real-time satellite & weather telemetry for {destination}..."):
    lat, lon = get_coordinates(destination)
    rates = get_exchange_rates("USD")
    current_inr = rates.get("INR", 83.5)
    weather_data = get_weather(destination, weather_key) if weather_key else None
    forecast_data = get_forecast(destination, weather_key) if weather_key else None

end_date = start_date + timedelta(days=days)

# ─────────────────────────────────────────────
# Component 1: Authentic Boarding Pass Mockup
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="boarding-pass">
    <div class="boarding-pass-header">
        <div style="display:flex; align-items:center; gap:0.8rem;">
            <span style="font-size:1.6rem;">✈️</span>
            <div>
                <strong style="font-size:1.1rem; letter-spacing:0.02em;">VOYANTA AI ITINERARY PASS</strong>
                <div style="font-size:0.75rem; opacity:0.85;">CONFIRMED EXPEDITION DOSSIER</div>
            </div>
        </div>
        <div style="text-align:right;">
            <span style="background:rgba(255,255,255,0.2); padding:0.3rem 0.8rem; border-radius:9999px; font-size:0.8rem; font-weight:700;">EXP-{''.join([c for c in destination.upper() if c.isalnum()][:3])}{days}D</span>
        </div>
    </div>
    <div class="boarding-pass-body">
        <div class="pass-field">
            <label>Destination</label>
            <span>{destination.title()}</span>
        </div>
        <div class="pass-field">
            <label>Duration</label>
            <span>{days} Days ({days-1} Nights)</span>
        </div>
        <div class="pass-field">
            <label>Dates</label>
            <span>{start_date.strftime('%b %d')} - {end_date.strftime('%b %d, %Y')}</span>
        </div>
        <div class="pass-field">
            <label>Travel Persona</label>
            <span>{travel_style.split('&')[0].strip()}</span>
        </div>
        <div class="pass-field">
            <label>Budget Tier</label>
            <span>{budget.split('(')[0].strip()}</span>
        </div>
        <div class="pass-field">
            <label>Geo Coordinates</label>
            <span style="font-family:'JetBrains Mono',monospace; font-size:0.95rem;">{lat:.2f}°, {lon:.2f}°</span>
        </div>
    </div>
    <div class="boarding-pass-footer">
        <span><b>Passenger:</b> MCA AI & DS Explorer</span>
        <span style="font-family:'JetBrains Mono',monospace; letter-spacing:0.15em;">||| | ||||| || |||| ||| ||||</span>
        <span><b>Exchange Ref:</b> 1 USD ≈ ₹{current_inr:.2f}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Component 2: 4 Real-Time Metrics Strip
# ─────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon-wrap" style="background:#e0e7ff; color:#4338ca;">📍</div>
        <div class="metric-info">
            <h4>{destination.title()}</h4>
            <p>Target City</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon-wrap" style="background:#fce7f3; color:#db2777;">📅</div>
        <div class="metric-info">
            <h4>{days} Days</h4>
            <p>Scheduled Plan</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon-wrap" style="background:#ccfbf1; color:#0d9488;">💱</div>
        <div class="metric-info">
            <h4>₹{current_inr:.2f}</h4>
            <p>Live USD to INR</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    weather_temp_label = f"{weather_data['main']['temp']:.1f}°C" if weather_data and "main" in weather_data else "Telemetry OK"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon-wrap" style="background:#e0f2fe; color:#0284c7;">🌤️</div>
        <div class="metric-info">
            <h4>{weather_temp_label}</h4>
            <p>Atmosphere</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Component 3: Live Weather Showcase & Google Maps
# ─────────────────────────────────────────────
col_weather, col_map = st.columns([1, 1])

with col_weather:
    st.markdown("<div class='section-title'>🌤️ Live Meteorological Conditions</div>", unsafe_allow_html=True)
    if weather_data and weather_data.get("main"):
        temp = weather_data["main"]["temp"]
        feels = weather_data["main"]["feels_like"]
        humidity = weather_data["main"]["humidity"]
        desc = weather_data["weather"][0]["description"].title()
        icon = weather_data["weather"][0]["icon"]
        icon_url = f"https://openweathermap.org/img/wn/{icon}@2x.png"
        wind = weather_data.get("wind", {}).get("speed", 0)

        st.markdown(f"""
        <div class="weather-showcase">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <span style="text-transform:uppercase; font-size:0.8rem; font-weight:700; letter-spacing:0.05em; opacity:0.85;">Current Surface Weather</span>
                    <div class="weather-main-temp">{temp:.1f}°C</div>
                    <div style="font-size:1.15rem; font-weight:600;">{desc}</div>
                </div>
                <img src="{icon_url}" width="95" style="filter: drop-shadow(0 4px 10px rgba(0,0,0,0.2));">
            </div>
            <div class="weather-badge-row">
                <span class="weather-sub-badge">🌡️ Feels like {feels:.1f}°C</span>
                <span class="weather-sub-badge">💧 Humidity: {humidity}%</span>
                <span class="weather-sub-badge">💨 Wind: {wind} m/s</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        weather_prompt_context = f"{desc}, {temp:.1f}°C, humidity {humidity}%, wind speed {wind} m/s"

        if forecast_data:
            fc_fig = build_forecast_chart(forecast_data)
            if fc_fig:
                st.plotly_chart(fc_fig, use_container_width=True)
    else:
        st.info("💡 Add your OpenWeatherMap key in the sidebar for live temperature & 8-hour trajectory forecasts.")
        weather_prompt_context = "Pleasant seasonal conditions"

with col_map:
    st.markdown("<div class='section-title'>🗺️ Google Maps, Street & Satellite View</div>", unsafe_allow_html=True)
    encoded_dest = urllib.parse.quote(destination)
    google_maps_url = f"https://maps.google.com/maps?q={encoded_dest}&t=&z=14&ie=UTF8&iwloc=&output=embed"
    google_sat_url = f"https://maps.google.com/maps?q={encoded_dest}&t=k&z=15&ie=UTF8&iwloc=&output=embed"
    street_view_embed = f"https://maps.google.com/maps?q=&layer=c&cbll={lat},{lon}&cbp=11,0,0,0,0&output=svembed"

    tab_road, tab_sat, tab_street, tab_globe = st.tabs([
        "🗺️ Road & Streets",
        "🛰️ Satellite Imagery",
        "🚶 360° Street View",
        "🌐 Geo Globe",
    ])

    with tab_road:
        components.html(
            f"""<iframe width="100%" height="340" style="border:0; border-radius:14px; box-shadow:0 4px 14px rgba(0,0,0,0.08);" loading="lazy" allowfullscreen src="{google_maps_url}"></iframe>""",
            height=350,
        )
        st.markdown(f"[🔗 Open in Google Maps Fullscreen](https://www.google.com/maps/search/?api=1&query={encoded_dest})")

    with tab_sat:
        components.html(
            f"""<iframe width="100%" height="340" style="border:0; border-radius:14px; box-shadow:0 4px 14px rgba(0,0,0,0.08);" loading="lazy" allowfullscreen src="{google_sat_url}"></iframe>""",
            height=350,
        )
        st.caption("🛰️ High-resolution orbital imagery from Google Maps.")

    with tab_street:
        components.html(
            f"""<iframe width="100%" height="300" style="border:0; border-radius:14px; box-shadow:0 4px 14px rgba(0,0,0,0.08);" loading="lazy" allowfullscreen src="{street_view_embed}"></iframe>""",
            height=310,
        )
        c_sv1, c_sv2 = st.columns(2)
        with c_sv1:
            st.link_button("🚶 Open 360° Street View", f"https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={lat},{lon}")
        with c_sv2:
            st.link_button("🌍 View on Google Earth 3D", f"https://earth.google.com/web/search/{encoded_dest}")

    with tab_globe:
        globe_map = build_geo_map(destination, lat, lon)
        st.plotly_chart(globe_map, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Component 4: Budget Modeling Chart
# ─────────────────────────────────────────────
st.markdown("<div class='section-title'>💰 Smart Expense Modeling</div>", unsafe_allow_html=True)
budget_fig = build_budget_chart(budget, days)
st.plotly_chart(budget_fig, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Component 5: AI Itinerary Dossier
# ─────────────────────────────────────────────
st.markdown("<div class='section-title'>🤖 Autonomous AI Travel Dossier</div>", unsafe_allow_html=True)

if generate_btn:
    if not gemini_key:
        st.error("❌ Please provide a valid Gemini API Key in the sidebar.")
    else:
        with st.spinner("🧠 Gemini 3.8 Flash is architecting your personalized dossier..."):
            itinerary_placeholder = st.empty()
            full_text = ""
            try:
                for chunk in generate_itinerary(
                    destination=destination,
                    days=days,
                    budget=budget,
                    interests=interests,
                    travel_style=travel_style,
                    start_date=start_date,
                    weather_info=weather_prompt_context,
                    gemini_api_key=gemini_key,
                ):
                    full_text += chunk
                    itinerary_placeholder.markdown(full_text)

                st.session_state["itinerary"] = full_text
                st.session_state["itinerary_dest"] = destination
                st.success("✅ Master itinerary architected successfully!")
            except Exception as e:
                st.error(f"❌ Error generating itinerary: {e}")

if "itinerary" in st.session_state and st.session_state.get("itinerary_dest") == destination:
    # Render Itinerary Tabs
    plan_text = st.session_state["itinerary"]

    t_plan, t_checklist, t_export = st.tabs(["📋 Complete Itinerary", "🎒 Interactive Packing Checklist", "📥 Export & Print"])

    with t_plan:
        st.markdown(plan_text)

    with t_checklist:
        st.markdown("#### ✅ Interactive Traveler Packing Checklist")
        st.caption("Check off items as you pack for your voyage:")
        c_chk1, c_chk2 = st.columns(2)
        with c_chk1:
            st.checkbox("🛂 Passport / Govt Identity Cards & Visa", key="chk_pass")
            st.checkbox("✈️ Flight, Hotel & Train Booking Confirmations", key="chk_tickets")
            st.checkbox("💳 Forex Card / Credit Cards & Cash Reserve", key="chk_cards")
            st.checkbox("🔌 Universal Power Adapter & Heavy-Duty Powerbank", key="chk_power")
            st.checkbox("📱 Local eSIM / Roaming Activated", key="chk_esim")
        with c_chk2:
            st.checkbox(f"👕 Weather-Appropriate Outfits for {destination}", key="chk_clothes")
            st.checkbox("💊 Emergency First-Aid & Prescription Medicines", key="chk_meds")
            st.checkbox("🧴 Sunscreen SPF 50+, Lip Balm & Bug Repellent", key="chk_toiletries")
            st.checkbox("👟 Broken-in Walking Sneakers / Trail Shoes", key="chk_shoes")
            st.checkbox("🎧 Noise-Cancelling Headphones / Travel Pillow", key="chk_headset")

    with t_export:
        st.markdown("#### 📥 Export Your Custom Travel Dossier")
        col_exp1, col_exp2 = st.columns(2)
        with col_exp1:
            st.download_button(
                label="📄 Download Clean Text File (.txt)",
                data=plan_text,
                file_name=f"VoyantaAI_{destination.replace(' ', '_')}_{days}Days.txt",
                mime="text/plain",
            )
        with col_exp2:
            st.download_button(
                label="📑 Download Formatted Markdown (.md)",
                data=plan_text,
                file_name=f"VoyantaAI_{destination.replace(' ', '_')}_{days}Days.md",
                mime="text/markdown",
            )
elif not generate_btn:
    st.info("👈 Click **'Architect My Itinerary'** in the sidebar to run the Gemini 3.8 Flash model!")

# ─────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#94a3b8; font-size:0.85rem; padding:1.5rem 0;">
    ✈️ <b>Voyanta AI</b> — Generative AI Travel Intelligence &nbsp;•&nbsp;
    Engineered for <b>MCA (AI & DS)</b> Capstone Showcase<br>
    Powered by <b>Google Gemini 3.8 Flash</b> • <b>OpenWeatherMap</b> • <b>Google Maps Street View</b> • <b>Plotly</b>
</div>
""", unsafe_allow_html=True)
