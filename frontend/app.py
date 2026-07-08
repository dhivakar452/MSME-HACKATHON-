"""
AI Powered MSME Smart Decision Support System — Streamlit Frontend
Run with:  streamlit run frontend/app.py
"""

import sys
import os

# Allow running from project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import date
import random

# ─── Try to import api_client; fall back gracefully ───────────────────────
try:
    from frontend.api_client import APIClient
except ImportError:
    try:
        from api_client import APIClient
    except ImportError:
        APIClient = None

# ─────────────────────────── Page Config ──────────────────────────────────
st.set_page_config(
    page_title="MSME Smart Decision Hub",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────── Custom CSS ───────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
.stApp { background: #0a0e1a; }
#MainMenu, footer, header { visibility: hidden; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1117 0%, #161b27 100%) !important;
    border-right: 1px solid rgba(99,102,241,0.2);
}

.metric-card {
    background: linear-gradient(135deg, #161b27 0%, #1e2538 100%);
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 16px;
    padding: 1.4rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #6366f1, #8b5cf6, #06b6d4);
}
.metric-label  { color: #8b92a5; font-size: 0.78rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.35rem; }
.metric-value  { color: #f1f5f9; font-size: 1.6rem; font-weight: 700; line-height: 1; }
.metric-delta  { font-size: 0.78rem; margin-top: 0.3rem; }
.delta-positive { color: #10b981; }
.delta-negative { color: #ef4444; }

.section-header {
    color: #f1f5f9; font-size: 1.2rem; font-weight: 700;
    margin-bottom: 1rem; padding-bottom: 0.5rem;
    border-bottom: 2px solid rgba(99,102,241,0.3);
}

.rec-card {
    background: linear-gradient(135deg, #0f172a 0%, #1e2538 100%);
    border-left: 4px solid #6366f1;
    border-radius: 0 12px 12px 0;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.7rem;
    color: #cbd5e1; font-size: 0.88rem; line-height: 1.5;
}
.rec-card.warning { border-left-color: #f59e0b; }
.rec-card.success { border-left-color: #10b981; }
.rec-card.danger  { border-left-color: #ef4444; }

.health-container {
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    padding: 1.5rem;
    background: linear-gradient(135deg, #161b27 0%, #1e2538 100%);
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 16px;
}
.health-score-text {
    font-size: 3rem; font-weight: 800;
    background: linear-gradient(90deg,#6366f1,#06b6d4);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}

.logo-text {
    font-size: 1.8rem; font-weight: 800;
    background: linear-gradient(90deg,#6366f1,#8b5cf6,#06b6d4);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center; margin-bottom: 0.3rem;
}
.logo-sub { text-align: center; color: #64748b; font-size: 0.85rem; margin-bottom: 2rem; }

.stButton > button {
    background: linear-gradient(135deg,#6366f1,#8b5cf6) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important; font-weight: 600 !important;
    padding: 0.6rem 2rem !important; width: 100% !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

.stTabs [data-baseweb="tab-list"] {
    background: #161b27; border-radius: 12px; gap: 4px; padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent; border-radius: 8px; color: #64748b; font-weight: 500;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg,#6366f1,#8b5cf6) !important; color: white !important;
}
</style>
""", unsafe_allow_html=True)

CHART_LAYOUT = dict(
    plot_bgcolor="#0a0e1a", paper_bgcolor="#161b27",
    font_color="#f1f5f9", title_font_size=14,
    xaxis=dict(gridcolor="#1e2538", showgrid=True),
    yaxis=dict(gridcolor="#1e2538", showgrid=True),
    margin=dict(l=20, r=20, t=50, b=20),
    legend=dict(bgcolor="rgba(0,0,0,0)"),
)

# ──────────────────── Session State Init ──────────────────────────────────
defaults = {
    "token": None, "username": "", "factory_records": [],
    "client": APIClient() if APIClient else None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────── Demo / Synthetic Data ────────────────────────────
@st.cache_data
def generate_demo_data(n: int = 12) -> pd.DataFrame:
    random.seed(42)
    base = 40_000
    months = pd.date_range(end=date.today(), periods=n, freq="MS")
    rows = []
    for i, m in enumerate(months):
        t = 1 + 0.02 * i
        ns = random.uniform(0.9, 1.1)
        rows.append({
            "date": m.date(),
            "sales": round(random.uniform(90_000, 160_000) * t * ns, 2),
            "production": round(random.uniform(800, 1400) * t, 1),
            "electricity_bill": round(random.uniform(4_000, 9_000) * ns, 2),
            "raw_material_cost": round(random.uniform(30_000, 70_000) * ns, 2),
            "salary": round(random.uniform(18_000, 28_000), 2),
            "inventory": round(random.uniform(200, 600) * ns, 0),
            "machine_running_hours": round(random.uniform(160, 240), 1),
            "machine_downtime": round(random.uniform(2, 15), 1),
            "profit": round(base * t * ns, 2),
        })
    return pd.DataFrame(rows)

# ─────────────────────── ML Helpers ───────────────────────────────────────
def predict_profit(df: pd.DataFrame, months_ahead: int = 6) -> pd.DataFrame:
    df = df.sort_values("date").reset_index(drop=True)
    X = np.arange(len(df), dtype=float)
    y = df["profit"].values.astype(float)
    coefs = np.polyfit(X, y, 1)
    fut_X = np.arange(len(df), len(df) + months_ahead, dtype=float)
    fut_y = np.polyval(coefs, fut_X)
    last = pd.Timestamp(df["date"].iloc[-1])
    fut_dates = pd.date_range(last + pd.DateOffset(months=1), periods=months_ahead, freq="MS")
    return pd.DataFrame({"date": fut_dates.date, "profit": np.maximum(fut_y, 0)})


def compute_health_score(df: pd.DataFrame) -> dict:
    if df.empty:
        return {"score": 0, "grade": "N/A", "color": "#64748b", "details": {}}
    latest = df.sort_values("date").iloc[-1]
    score = 0
    details = {}

    margin = (latest["profit"] / latest["sales"] * 100) if latest.get("sales", 0) > 0 else 0
    pm_score = min(30, max(0, margin * 1.5))
    score += pm_score
    details["Profit Margin"] = f"{margin:.1f}%"

    run = latest.get("machine_running_hours", 0) or 0
    down = latest.get("machine_downtime", 0) or 0
    eff = (run / (run + down + 0.001)) * 100
    score += min(25, eff * 0.25)
    details["Machine Efficiency"] = f"{eff:.1f}%"

    inv = latest.get("inventory", 0) or 0
    score += min(20, (inv / 600) * 20)
    details["Inventory Level"] = f"{inv:.0f} units"

    elec = latest.get("electricity_bill", 0) or 0
    cost_ratio = elec / (latest.get("sales", 1) + 0.001)
    score += min(15, max(0, (1 - cost_ratio * 10) * 15))
    details["Electricity Cost"] = f"₹{elec:,.0f}"

    if len(df) >= 3:
        trend = df["profit"].iloc[-1] - df["profit"].iloc[-3]
        score += min(10, max(0, trend / 5000))
        details["3-Month Trend"] = "📈 Positive" if trend > 0 else "📉 Declining"

    score = round(min(100, max(0, score)))
    if score >= 80:
        grade, color = "Excellent 🌟", "#10b981"
    elif score >= 60:
        grade, color = "Good 👍", "#6366f1"
    elif score >= 40:
        grade, color = "Fair ⚠️", "#f59e0b"
    else:
        grade, color = "Poor 🔴", "#ef4444"
    return {"score": score, "grade": grade, "color": color, "details": details}


def generate_recommendations(df: pd.DataFrame) -> list:
    if df.empty:
        return [{"type": "info", "icon": "ℹ️", "msg": "Add factory data to receive AI recommendations."}]
    latest = df.sort_values("date").iloc[-1]
    recs = []

    sales = latest.get("sales", 0) or 1
    profit = latest.get("profit", 0) or 0
    margin = profit / sales * 100

    run = latest.get("machine_running_hours", 0) or 0
    down = latest.get("machine_downtime", 0) or 0
    downtime_pct = down / (run + down + 0.001) * 100

    inv = latest.get("inventory", 0) or 0
    elec = latest.get("electricity_bill", 0) or 0
    elec_ratio = elec / sales * 100

    if margin < 15:
        recs.append({"type": "danger", "icon": "🔴", "msg": f"Profit margin is critically low at {margin:.1f}%. Review pricing and cut overhead costs immediately."})
    elif margin < 25:
        recs.append({"type": "warning", "icon": "🟡", "msg": f"Profit margin ({margin:.1f}%) is below recommended 25%. Renegotiate supplier contracts."})
    else:
        recs.append({"type": "success", "icon": "🟢", "msg": f"Excellent profit margin of {margin:.1f}%! Reinvest surplus into capacity expansion."})

    if downtime_pct > 10:
        recs.append({"type": "danger", "icon": "🔴", "msg": f"Machine downtime is {downtime_pct:.1f}% — schedule preventive maintenance immediately."})
    elif downtime_pct > 5:
        recs.append({"type": "warning", "icon": "🟡", "msg": f"Machine downtime ({downtime_pct:.1f}%) is elevated. Service machines this month."})
    else:
        recs.append({"type": "success", "icon": "🟢", "msg": "Machine efficiency is excellent. Maintain current maintenance schedule."})

    if inv < 200:
        recs.append({"type": "danger", "icon": "🔴", "msg": "Inventory critically low! Place purchase orders within 48 hrs to avoid production stoppage."})
    elif inv < 350:
        recs.append({"type": "warning", "icon": "🟡", "msg": "Inventory declining. Initiate restocking this week."})

    if elec_ratio > 8:
        recs.append({"type": "warning", "icon": "🟡", "msg": f"Electricity costs are {elec_ratio:.1f}% of sales. Consider an energy audit or solar investment."})

    if len(df) >= 3:
        trend = df["profit"].iloc[-1] - df["profit"].iloc[-3]
        if trend > 5000:
            recs.append({"type": "success", "icon": "🟢", "msg": f"3-month profit trending strongly upward (+₹{trend:,.0f}). Great momentum — consider expansion."})
        elif trend < -5000:
            recs.append({"type": "danger", "icon": "🔴", "msg": f"3-month profit declining by ₹{abs(trend):,.0f}. Conduct an urgent cost-revenue analysis."})

    return recs

# ──────────────────────── AUTH PAGE ───────────────────────────────────────
def login_page():
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown('<div class="logo-text">🏭 MSME Hub</div>', unsafe_allow_html=True)
        st.markdown('<div class="logo-sub">AI-Powered Smart Decision Support System</div>', unsafe_allow_html=True)

        tab_login, tab_reg = st.tabs(["🔑 Login", "📝 Register"])

        with tab_login:
            st.markdown("<br>", unsafe_allow_html=True)
            username = st.text_input("Username", key="login_user", placeholder="Enter username")
            password = st.text_input("Password", type="password", key="login_pass", placeholder="Enter password")
            st.markdown("<br>", unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                if st.button("🎭 Demo Mode", key="btn_demo"):
                    st.session_state.token = "demo"
                    st.session_state.username = "Demo Owner"
                    st.session_state.factory_records = generate_demo_data(12).to_dict("records")
                    st.rerun()
            with c2:
                if st.button("Login →", key="btn_login"):
                    if username and password and st.session_state.client:
                        result = st.session_state.client.login(username, password)
                        if result["status"] == 200:
                            st.session_state.token = result["data"]["access_token"]
                            st.session_state.username = username
                            st.session_state.factory_records = st.session_state.client.get_factory_data()
                            st.success("✅ Login successful!")
                            st.rerun()
                        else:
                            st.error("❌ Invalid credentials. Try Demo Mode.")
                    elif not st.session_state.client:
                        st.warning("Backend offline — use Demo Mode.")
                    else:
                        st.warning("Please fill in all fields.")

        with tab_reg:
            st.markdown("<br>", unsafe_allow_html=True)
            reg_user = st.text_input("Username", key="reg_user", placeholder="Choose a username")
            reg_email = st.text_input("Email", key="reg_email", placeholder="your@email.com")
            reg_pass = st.text_input("Password", type="password", key="reg_pass", placeholder="Min 6 characters")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Create Account →", key="btn_register"):
                if reg_user and reg_pass and len(reg_pass) >= 6 and st.session_state.client:
                    result = st.session_state.client.register(reg_user, reg_pass, reg_email)
                    if result["status"] == 200:
                        st.success("✅ Account created! Please login.")
                    else:
                        st.error(f"Registration failed: {result['data'].get('detail', 'Unknown error')}")
                else:
                    st.warning("Fill all fields. Password must be ≥ 6 characters.")


# ──────────────────────── SIDEBAR ─────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown(f"""
        <div style='text-align:center;padding:1rem 0;'>
            <div style='font-size:2.5rem;'>🏭</div>
            <div style='font-size:1.1rem;font-weight:700;
                background:linear-gradient(90deg,#6366f1,#06b6d4);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;'>
                MSME Hub
            </div>
            <div style='color:#64748b;font-size:0.75rem;'>Smart Decision Support</div>
        </div>
        <hr style='border-color:rgba(99,102,241,0.2);margin:0.5rem 0;'>
        <div style='background:rgba(99,102,241,0.1);border-radius:10px;padding:0.75rem;margin-bottom:1rem;'>
            <div style='color:#8b92a5;font-size:0.75rem;'>Logged in as</div>
            <div style='color:#f1f5f9;font-weight:600;'>👤 {st.session_state.username}</div>
        </div>
        """, unsafe_allow_html=True)

        page = st.radio("Navigation", [
            "📊 Dashboard",
            "➕ Add Data",
            "📈 Analytics",
            "🤖 AI Insights",
            "📥 Upload CSV",
            "📄 Reports",
        ], label_visibility="collapsed")

        st.markdown("<hr style='border-color:rgba(99,102,241,0.2);'>", unsafe_allow_html=True)
        if st.button("🚪 Logout", key="logout_btn"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

        is_demo = st.session_state.token == "demo"
        color = "#f59e0b" if is_demo else "#10b981"
        label = "🎭 Demo Mode" if is_demo else "🟢 API Connected"
        st.markdown(f"<div style='color:{color};font-size:0.78rem;margin-top:0.5rem;'>{label}</div>",
                    unsafe_allow_html=True)
    return page

# ──────────────────────── PAGE: Dashboard ─────────────────────────────────
def page_dashboard(df: pd.DataFrame):
    st.markdown('<div class="section-header">📊 Business Overview Dashboard</div>', unsafe_allow_html=True)
    if df.empty:
        st.info("No data yet. Add records or go to **➕ Add Data** to get started.")
        st.markdown('<div style="text-align:center;padding:3rem;color:#64748b;">'
                    '<div style="font-size:4rem;">🏭</div>'
                    '<div style="font-size:1.1rem;margin-top:1rem;">Your dashboard awaits your first data entry.</div>'
                    '</div>', unsafe_allow_html=True)
        return

    df = df.sort_values("date").reset_index(drop=True)
    latest = df.iloc[-1]
    prev = df.iloc[-2] if len(df) >= 2 else latest

    def delta(now, prev_val):
        d = now - prev_val
        sign = "+" if d >= 0 else ""
        cls = "delta-positive" if d >= 0 else "delta-negative"
        return f"{sign}₹{d:,.0f}", cls

    kpis = [
        ("💰 Profit", f"₹{latest['profit']:,.0f}", *delta(latest['profit'], prev['profit'])),
        ("📦 Sales",  f"₹{latest.get('sales', 0):,.0f}", *delta(latest.get('sales', 0), prev.get('sales', 0))),
        ("🏗️ Production", f"{latest.get('production', 0):,.0f} u", "", ""),
        ("📋 Inventory", f"{latest.get('inventory', 0):,.0f} u", "", ""),
    ]
    cols = st.columns(4)
    for col, (label, value, delta_v, cls) in zip(cols, kpis):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-delta {cls}">{delta_v}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        fig = px.area(df, x="date", y="profit", title="📈 Profit Trend",
                      color_discrete_sequence=["#6366f1"])
        fig.update_traces(fillcolor="rgba(99,102,241,0.15)", line_color="#6366f1")
        fig.update_layout(**CHART_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        cols_avail = [c for c in ["sales", "profit"] if c in df.columns]
        fig2 = px.bar(df.tail(6), x="date", y=cols_avail,
                      title="📊 Sales vs Profit (Last 6 Months)", barmode="group",
                      color_discrete_map={"sales": "#06b6d4", "profit": "#8b5cf6"})
        fig2.update_layout(**CHART_LAYOUT)
        st.plotly_chart(fig2, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        if "machine_downtime" in df.columns:
            fig3 = px.line(df, x="date", y="machine_downtime",
                           title="🔧 Machine Downtime (hrs)",
                           color_discrete_sequence=["#f59e0b"], markers=True)
            fig3.update_layout(**CHART_LAYOUT)
            st.plotly_chart(fig3, use_container_width=True)

    with c4:
        if "production" in df.columns and "machine_running_hours" in df.columns:
            fig4 = px.scatter(df, x="production", y="profit",
                              color="machine_running_hours",
                              title="🔬 Production vs Profit",
                              color_continuous_scale="Viridis",
                              size_max=15)
            fig4.update_layout(**CHART_LAYOUT)
            st.plotly_chart(fig4, use_container_width=True)

# ──────────────────────── PAGE: Add Data ──────────────────────────────────
def page_add_data():
    st.markdown('<div class="section-header">➕ Add Factory Data Record</div>', unsafe_allow_html=True)

    with st.form("factory_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            entry_date     = st.date_input("📅 Date", value=date.today())
            sales          = st.number_input("💰 Sales Revenue (₹)",        min_value=0.0, value=120000.0, step=1000.0, format="%.2f")
            production     = st.number_input("🏗️ Production Volume (units)", min_value=0.0, value=1000.0,   step=10.0)
            electricity    = st.number_input("⚡ Electricity Bill (₹)",      min_value=0.0, value=6000.0,   step=100.0, format="%.2f")
            raw_material   = st.number_input("🧱 Raw Material Cost (₹)",     min_value=0.0, value=45000.0,  step=500.0, format="%.2f")
        with c2:
            salary         = st.number_input("👷 Salary Expenses (₹)",       min_value=0.0, value=22000.0,  step=500.0, format="%.2f")
            inventory      = st.number_input("📦 Inventory (units)",          min_value=0.0, value=400.0,    step=10.0)
            machine_hours  = st.number_input("⚙️ Machine Running Hours",     min_value=0.0, value=200.0,    step=1.0)
            downtime       = st.number_input("🔧 Machine Downtime (hrs)",     min_value=0.0, value=5.0,      step=0.5)
            profit_auto    = max(0.0, sales - electricity - raw_material - salary)
            profit         = st.number_input("📈 Profit (₹)",                 min_value=0.0, value=round(profit_auto, 2), step=100.0, format="%.2f")

        submitted = st.form_submit_button("✅ Save Record", use_container_width=True)

    if submitted:
        record = {
            "date": str(entry_date), "sales": sales,
            "production": production, "electricity_bill": electricity,
            "raw_material_cost": raw_material, "salary": salary,
            "inventory": inventory, "machine_running_hours": machine_hours,
            "machine_downtime": downtime, "profit": profit,
        }
        if st.session_state.token != "demo" and st.session_state.client:
            api_payload = {**record, "user_id": 1,
                           "production_volume": production,
                           "utility_cost": electricity,
                           "downtime_hours": downtime}
            result = st.session_state.client.add_factory_data(api_payload)
            if result["status"] in (200, 201):
                st.success("✅ Data saved to backend!")
                st.session_state.factory_records = st.session_state.client.get_factory_data()
            else:
                st.error(f"Save failed: {result['data']}")
        else:
            st.session_state.factory_records.append(record)
            st.success("✅ Record added (Demo Mode).")

# ──────────────────────── PAGE: Analytics ─────────────────────────────────
def page_analytics(df: pd.DataFrame):
    st.markdown('<div class="section-header">📈 Advanced Analytics & Forecasting</div>', unsafe_allow_html=True)
    if df.empty:
        st.info("No data to analyse. Add records first.")
        return

    df = df.sort_values("date").reset_index(drop=True)

    # Forecast
    st.subheader("🔮 Profit Forecast — Next 6 Months (AI Linear Regression)")
    forecast_df = predict_profit(df, 6)
    hist  = df[["date", "profit"]].assign(Series="Historical")
    fore  = forecast_df.assign(Series="Forecast")
    combined = pd.concat([hist, fore], ignore_index=True)
    fig = px.line(combined, x="date", y="profit", color="Series",
                  color_discrete_map={"Historical": "#6366f1", "Forecast": "#10b981"},
                  markers=True, title="Historical + AI Forecast")
    fig.update_layout(**CHART_LAYOUT)
    st.plotly_chart(fig, use_container_width=True)

    # Cost breakdown pie
    st.subheader("💸 Cost Breakdown (Latest Record)")
    latest = df.iloc[-1]
    cost_cats = {
        "Raw Material": latest.get("raw_material_cost", 0),
        "Salary":       latest.get("salary", 0),
        "Electricity":  latest.get("electricity_bill", 0),
        "Other":        max(0, latest.get("sales", 0) - latest.get("profit", 0)
                            - latest.get("raw_material_cost", 0)
                            - latest.get("salary", 0)
                            - latest.get("electricity_bill", 0)),
    }
    cost_df = pd.DataFrame(list(cost_cats.items()), columns=["Category", "Amount"])
    fig2 = px.pie(cost_df, values="Amount", names="Category",
                  color_discrete_sequence=["#6366f1", "#8b5cf6", "#06b6d4", "#f59e0b"],
                  hole=0.4)
    fig2.update_layout(paper_bgcolor="#161b27", font_color="#f1f5f9",
                        margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig2, use_container_width=True)

    # Table
    st.subheader("📋 Historical Data Table")
    fmt = {c: "₹{:,.0f}" for c in ["profit", "sales", "electricity_bill", "salary", "raw_material_cost"] if c in df.columns}
    st.dataframe(df.sort_values("date", ascending=False).style.format(fmt), use_container_width=True)

# ──────────────────────── PAGE: AI Insights ───────────────────────────────
def page_ai_insights(df: pd.DataFrame):
    st.markdown('<div class="section-header">🤖 AI Insights & Business Health</div>', unsafe_allow_html=True)
    if df.empty:
        st.info("Add factory data first to see AI insights.")
        return

    df = df.sort_values("date").reset_index(drop=True)
    health = compute_health_score(df)
    recs   = generate_recommendations(df)

    col_score, col_details = st.columns([1, 2])

    with col_score:
        st.markdown(f"""
        <div class="health-container">
            <div style='color:#8b92a5;font-size:0.85rem;margin-bottom:0.5rem;'>Business Health Score</div>
            <div class="health-score-text">{health['score']}</div>
            <div style='font-size:1rem;font-weight:600;color:{health["color"]};margin-top:0.3rem;'>{health['grade']}</div>
            <div style='color:#64748b;font-size:0.8rem;'>out of 100</div>
        </div>""", unsafe_allow_html=True)

        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=health["score"],
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#64748b"},
                "bar": {"color": health["color"]},
                "steps": [
                    {"range": [0, 40],  "color": "rgba(239,68,68,0.15)"},
                    {"range": [40, 60], "color": "rgba(245,158,11,0.15)"},
                    {"range": [60, 80], "color": "rgba(99,102,241,0.15)"},
                    {"range": [80, 100],"color": "rgba(16,185,129,0.15)"},
                ],
                "bgcolor": "#161b27", "bordercolor": "rgba(99,102,241,0.3)",
            },
            number={"font": {"color": "#f1f5f9"}},
        ))
        gauge.update_layout(paper_bgcolor="#0a0e1a", font_color="#f1f5f9",
                             height=220, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(gauge, use_container_width=True)

    with col_details:
        st.markdown("**📊 Score Breakdown**")
        for k, v in health["details"].items():
            st.markdown(f"""
            <div style='display:flex;justify-content:space-between;padding:0.55rem 0;
                        border-bottom:1px solid rgba(99,102,241,0.1);'>
                <span style='color:#8b92a5;font-size:0.88rem;'>{k}</span>
                <span style='color:#f1f5f9;font-weight:600;font-size:0.88rem;'>{v}</span>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("💡 AI-Generated Recommendations")
    for rec in recs:
        st.markdown(f'<div class="rec-card {rec["type"]}">{rec["icon"]} {rec["msg"]}</div>',
                    unsafe_allow_html=True)

# ──────────────────────── PAGE: Upload CSV ────────────────────────────────
def page_upload_csv():
    st.markdown('<div class="section-header">📥 Bulk Data Upload via CSV</div>', unsafe_allow_html=True)
    st.markdown("""
    Upload a CSV file with your historical factory data.  
    Required columns (extra columns are ignored):
    """)
    required = ["date", "sales", "production", "electricity_bill",
                "raw_material_cost", "salary", "inventory",
                "machine_running_hours", "machine_downtime", "profit"]
    st.code(", ".join(required))

    uploaded = st.file_uploader("Choose a CSV file", type=["csv"])
    if uploaded:
        try:
            raw = pd.read_csv(uploaded)
            raw.columns = [c.strip().lower().replace(" ", "_") for c in raw.columns]
            if "date" in raw.columns:
                raw["date"] = pd.to_datetime(raw["date"], errors="coerce").dt.date
            raw = raw.dropna(subset=["date", "profit"])
            st.success(f"✅ {len(raw)} valid rows loaded after cleaning.")
            st.dataframe(raw.head(10), use_container_width=True)
            if st.button("📤 Import to Dashboard"):
                st.session_state.factory_records = raw.to_dict("records")
                st.success("✅ Imported! Switch to 📊 Dashboard to view.")
        except Exception as e:
            st.error(f"Error reading CSV: {e}")

    st.markdown("---")
    sample_csv = generate_demo_data(3).to_csv(index=False).encode()
    st.download_button("📥 Download Sample CSV Template", data=sample_csv,
                       file_name="msme_sample_data.csv", mime="text/csv")

# ──────────────────────── PAGE: Reports ───────────────────────────────────
def page_reports(df: pd.DataFrame):
    st.markdown('<div class="section-header">📄 Reports & Exports</div>', unsafe_allow_html=True)
    if df.empty:
        st.info("No data available for reports. Add factory records first.")
        return

    df = df.sort_values("date").reset_index(drop=True)

    # Monthly summary
    st.subheader("📅 Monthly Summary Report")
    df["month"] = pd.to_datetime(df["date"]).dt.to_period("M").astype(str)
    agg = {
        "total_sales":   ("sales", "sum"),
        "total_profit":  ("profit", "sum"),
        "avg_downtime":  ("machine_downtime", "mean"),
        "avg_inventory": ("inventory", "mean"),
    }
    # only aggregate columns that exist
    agg = {k: v for k, v in agg.items() if v[0] in df.columns}
    monthly = df.groupby("month").agg(**agg).reset_index()
    fmt = {}
    if "total_sales"   in monthly.columns: fmt["total_sales"]   = "₹{:,.0f}"
    if "total_profit"  in monthly.columns: fmt["total_profit"]  = "₹{:,.0f}"
    if "avg_downtime"  in monthly.columns: fmt["avg_downtime"]  = "{:.1f} hrs"
    if "avg_inventory" in monthly.columns: fmt["avg_inventory"] = "{:.0f} units"
    st.dataframe(monthly.style.format(fmt), use_container_width=True)
    st.download_button("📥 Download Monthly Report (CSV)",
                       data=monthly.to_csv(index=False).encode(),
                       file_name="msme_monthly_report.csv", mime="text/csv")

    st.subheader("📋 Full Data Export")
    st.download_button("📥 Download All Records (CSV)",
                       data=df.drop(columns=["month"], errors="ignore").to_csv(index=False).encode(),
                       file_name="msme_all_records.csv", mime="text/csv")

# ──────────────────────── MAIN ────────────────────────────────────────────
def main():
    if not st.session_state.token:
        login_page()
        return

    page = render_sidebar()

    # Build DataFrame
    records = st.session_state.factory_records
    if records:
        df = pd.DataFrame(records)
        num_cols = ["sales", "production", "electricity_bill", "raw_material_cost",
                    "salary", "inventory", "machine_running_hours", "machine_downtime", "profit"]
        for col in num_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
            df = df.dropna(subset=["date"]).sort_values("date").reset_index(drop=True)
    else:
        df = pd.DataFrame()

    # Route
    if   page == "📊 Dashboard":  page_dashboard(df)
    elif page == "➕ Add Data":    page_add_data()
    elif page == "📈 Analytics":   page_analytics(df)
    elif page == "🤖 AI Insights": page_ai_insights(df)
    elif page == "📥 Upload CSV":  page_upload_csv()
    elif page == "📄 Reports":     page_reports(df)


if __name__ == "__main__":
    main()
