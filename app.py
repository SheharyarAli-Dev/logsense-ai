import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from services.parser import parse_log_content
from services.classifier import classify_log_message
from services.analyzer import analyze_root_cause, analyze_trends
from services.solutions import suggest_solution

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LogSense AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CUSTOM CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* General */
    [data-testid="stAppViewContainer"] { background: #f7f9fc; }
    [data-testid="stSidebar"] { background: #1a1f2e; }
    [data-testid="stSidebar"] * { color: #e0e0e0 !important; }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2 { color: #ffffff !important; }

    /* Metric cards */
    [data-testid="metric-container"] {
        background: white;
        border: 1px solid #e4e8f0;
        border-radius: 10px;
        padding: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

    /* Header */
    .app-header {
        background: linear-gradient(135deg, #1a1f2e 0%, #2e3a59 100%);
        color: white;
        padding: 32px 40px;
        border-radius: 12px;
        margin-bottom: 28px;
    }
    .app-header h1 { color: white; margin: 0; font-size: 2.2rem; font-weight: 700; }
    .app-header p  { color: #a0aec0; margin: 6px 0 0; font-size: 1rem; }

    /* Severity badges */
    .badge {
        display: inline-block;
        padding: 4px 14px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.85rem;
        letter-spacing: 0.05em;
    }
    .badge-critical { background: #fee2e2; color: #991b1b; }
    .badge-high     { background: #ffedd5; color: #9a3412; }
    .badge-medium   { background: #fef9c3; color: #854d0e; }
    .badge-low      { background: #dcfce7; color: #166534; }

    /* Cards */
    .card {
        background: white;
        border: 1px solid #e4e8f0;
        border-radius: 10px;
        padding: 24px;
        margin-bottom: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .card h3 { margin-top: 0; color: #1a1f2e; font-size: 1rem; font-weight: 600; }

    /* Fix list */
    .fix-item {
        background: #f0f7ff;
        border-left: 4px solid #2563eb;
        border-radius: 0 6px 6px 0;
        padding: 10px 14px;
        margin-bottom: 8px;
        font-size: 0.92rem;
        color: #1e3a5f;
    }

    /* Issue count chips */
    .issue-chip {
        display: inline-block;
        background: #f1f5f9;
        border: 1px solid #cbd5e1;
        border-radius: 6px;
        padding: 4px 12px;
        margin: 4px;
        font-size: 0.82rem;
        color: #334155;
        font-weight: 600;
    }

    /* Section title */
    .section-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1a1f2e;
        border-bottom: 2px solid #e4e8f0;
        padding-bottom: 8px;
        margin-bottom: 16px;
    }

    /* Dataframe header fix */
    [data-testid="stDataFrame"] { border-radius: 8px; overflow: hidden; }

    /* Upload area */
    [data-testid="stFileUploader"] {
        background: white;
        border-radius: 10px;
        border: 2px dashed #cbd5e1;
        padding: 8px;
    }
    button[kind="primary"] {
        background: #2563eb !important;
        border: none !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# ── SEVERITY HELPERS ─────────────────────────────────────────────────────────
SEVERITY_CONFIG = {
    "Critical": {"badge": "badge-critical", "icon": "🔴", "color": "#991b1b"},
    "High":     {"badge": "badge-high",     "icon": "🟠", "color": "#9a3412"},
    "Medium":   {"badge": "badge-medium",   "icon": "🟡", "color": "#854d0e"},
    "Low":      {"badge": "badge-low",      "icon": "🟢", "color": "#166534"},
}

LEVEL_COLORS = {
    "INFO":     "#22c55e",
    "WARNING":  "#f59e0b",
    "ERROR":    "#ef4444",
    "CRITICAL": "#7c3aed",
}

CATEGORY_COLORS = {
    "Normal":        "#64748b",
    "Memory Issue":  "#f59e0b",
    "Crash Issue":   "#ef4444",
    "Disk Issue":    "#8b5cf6",
    "Network Issue": "#3b82f6",
    "General Error": "#f97316",
}

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📊 LogSense AI")
    st.markdown("---")
    st.markdown("### About")
    st.markdown(
        "Upload any `.log` file to instantly get:\n"
        "- 🔍 Root cause analysis\n"
        "- 🚦 Severity assessment\n"
        "- 💡 Fix suggestions\n"
        "- 📈 Issue trends over time\n"
        "- 📋 Parsed log table"
    )
    st.markdown("---")
    st.markdown("### Log Format")
    st.code("YYYY-MM-DD HH:MM:SS LEVEL message", language=None)
    st.markdown("Accepted levels: `INFO` `WARNING` `ERROR` `CRITICAL`")
    st.markdown("---")
    st.markdown("### Settings")
    trend_interval = st.selectbox("Trend bucket size", [5, 10, 15, 30], index=1, help="Time interval in minutes for the trends chart")
    show_all_logs  = st.checkbox("Show all parsed logs", value=False, help="By default only 15 sample logs are shown")
    st.markdown("---")
    st.caption("v1.0 · Built with Streamlit")

# ── HEADER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <h1>📊 LogSense AI</h1>
    <p>Intelligent log analysis — root cause, severity, trends & fixes in seconds.</p>
</div>
""", unsafe_allow_html=True)

# ── FILE UPLOAD ───────────────────────────────────────────────────────────────
uploaded_file = st.file_uploader(
    "Upload a .log file to begin analysis",
    type=["log"],
    help="File must follow the format: YYYY-MM-DD HH:MM:SS LEVEL message"
)

# ── MAIN LOGIC ────────────────────────────────────────────────────────────────
if uploaded_file is not None:

    # Read & parse
    content = uploaded_file.read().decode("utf-8", errors="ignore")
    parsed_logs = parse_log_content(content)

    if not parsed_logs:
        st.error("⚠️ No parseable log entries found. Check that your file follows the expected format: `YYYY-MM-DD HH:MM:SS LEVEL message`")
        st.stop()

    # Classify
    for log in parsed_logs:
        log["category"] = classify_log_message(log["message"])

    # Analyse
    analysis  = analyze_root_cause(parsed_logs)
    solutions = suggest_solution(analysis["root_cause"])
    trends    = analyze_trends(parsed_logs, interval_minutes=trend_interval)

    root_cause = analysis["root_cause"]
    severity   = analysis["severity"]
    sev_cfg    = SEVERITY_CONFIG.get(severity, SEVERITY_CONFIG["Low"])

    # ── KPI ROW ──────────────────────────────────────────────────────────────
    st.markdown("---")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("📄 Total Log Entries",  len(parsed_logs))
    k2.metric("🔍 Root Cause",         root_cause)
    k3.metric("🚦 Severity",           severity)
    issue_count = analysis.get("issue_count", {})
    k4.metric("⚠️ Issues Found", sum(issue_count.values()) if issue_count else 0)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── ANALYSIS + FIXES ─────────────────────────────────────────────────────
    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown('<div class="section-title">🔍 Analysis Summary</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="card">
            <h3>Root Cause</h3>
            <p style="font-size:1.3rem;font-weight:700;color:#1a1f2e;margin:0 0 12px">{root_cause}</p>
            <h3>Severity</h3>
            <span class="badge {sev_cfg['badge']}">{sev_cfg['icon']} {severity}</span>
            <h3 style="margin-top:16px">Issue Breakdown</h3>
            <div>
                {''.join(f'<span class="issue-chip">{cat}: {cnt}</span>' for cat, cnt in issue_count.items()) if issue_count else '<span style="color:#64748b">No issues classified</span>'}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="section-title">💡 Suggested Fixes</div>', unsafe_allow_html=True)
        fixes_html = "".join(f'<div class="fix-item">✅ {fix}</div>' for fix in solutions)
        st.markdown(f'<div class="card">{fixes_html}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── CHARTS ROW ───────────────────────────────────────────────────────────
    chart_left, chart_right = st.columns([1, 1], gap="large")

    with chart_left:
        st.markdown('<div class="section-title">🍩 Log Category Distribution</div>', unsafe_allow_html=True)
        cat_counts = {}
        for log in parsed_logs:
            cat_counts[log["category"]] = cat_counts.get(log["category"], 0) + 1

        fig_donut = px.pie(
            names=list(cat_counts.keys()),
            values=list(cat_counts.values()),
            hole=0.55,
            color=list(cat_counts.keys()),
            color_discrete_map=CATEGORY_COLORS,
        )
        fig_donut.update_traces(textposition="outside", textinfo="percent+label")
        fig_donut.update_layout(
            margin=dict(t=10, b=10, l=10, r=10),
            legend=dict(orientation="h", yanchor="bottom", y=-0.25),
            showlegend=True,
            height=340,
            paper_bgcolor="white",
            plot_bgcolor="white",
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    with chart_right:
        st.markdown('<div class="section-title">📊 Log Level Distribution</div>', unsafe_allow_html=True)
        level_counts = {}
        for log in parsed_logs:
            level_counts[log["level"]] = level_counts.get(log["level"], 0) + 1

        ordered_levels = [l for l in ["INFO", "WARNING", "ERROR", "CRITICAL"] if l in level_counts]
        fig_bar = px.bar(
            x=ordered_levels,
            y=[level_counts[l] for l in ordered_levels],
            color=ordered_levels,
            color_discrete_map=LEVEL_COLORS,
            labels={"x": "Log Level", "y": "Count"},
            text_auto=True,
        )
        fig_bar.update_layout(
            margin=dict(t=10, b=10, l=10, r=10),
            showlegend=False,
            height=340,
            paper_bgcolor="white",
            plot_bgcolor="#fafafa",
            yaxis=dict(gridcolor="#e4e8f0"),
            xaxis=dict(linecolor="#e4e8f0"),
        )
        fig_bar.update_traces(textfont_size=13, textposition="outside")
        st.plotly_chart(fig_bar, use_container_width=True)

    # ── TRENDS CHART ─────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">📈 Issue Trends Over Time</div>', unsafe_allow_html=True)

    if trends:
        all_categories = set()
        for bucket_data in trends.values():
            all_categories.update(bucket_data.keys())

        time_labels = sorted(trends.keys())
        fig_trends = go.Figure()

        for cat in sorted(all_categories):
            y_vals = [trends[t].get(cat, 0) for t in time_labels]
            fig_trends.add_trace(go.Scatter(
                x=time_labels,
                y=y_vals,
                name=cat,
                mode="lines+markers",
                line=dict(width=2.5, color=CATEGORY_COLORS.get(cat, "#94a3b8")),
                marker=dict(size=6),
                fill="tozeroy",
                fillcolor=CATEGORY_COLORS.get(cat, "#94a3b8") + "18",
            ))

        fig_trends.update_layout(
            height=360,
            paper_bgcolor="white",
            plot_bgcolor="#fafafa",
            margin=dict(t=10, b=40, l=10, r=10),
            legend=dict(orientation="h", yanchor="bottom", y=-0.3),
            xaxis=dict(title=f"Time ({trend_interval}-min buckets)", gridcolor="#e4e8f0", linecolor="#e4e8f0"),
            yaxis=dict(title="Count", gridcolor="#e4e8f0", rangemode="tozero"),
            hovermode="x unified",
        )
        st.plotly_chart(fig_trends, use_container_width=True)
    else:
        st.info("No trend data available.")

    # ── LOG TABLE ─────────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    display_count = len(parsed_logs) if show_all_logs else min(15, len(parsed_logs))
    st.markdown(
        f'<div class="section-title">📋 Parsed Log Entries '
        f'<span style="font-weight:400;font-size:0.85rem;color:#64748b">'
        f'(showing {display_count} of {len(parsed_logs)})</span></div>',
        unsafe_allow_html=True
    )

    df = pd.DataFrame(parsed_logs[:display_count])

    def color_level(val):
        colors = {"INFO": "#dcfce7", "WARNING": "#fef9c3", "ERROR": "#fee2e2", "CRITICAL": "#ede9fe"}
        return f"background-color: {colors.get(val, 'white')}"

    def color_category(val):
        colors = {
            "Normal": "#f1f5f9", "Memory Issue": "#fef9c3",
            "Crash Issue": "#fee2e2", "Disk Issue": "#f5f3ff",
            "Network Issue": "#eff6ff", "General Error": "#fff7ed"
        }
        return f"background-color: {colors.get(val, 'white')}"

    styled_df = df.style.applymap(color_level, subset=["level"]) \
                        .applymap(color_category, subset=["category"])
    st.dataframe(styled_df, use_container_width=True, height=420)

    # ── DOWNLOAD ──────────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    csv = pd.DataFrame(parsed_logs).to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Full Analysis as CSV",
        data=csv,
        file_name=f"{uploaded_file.name.replace('.log', '')}_analysis.csv",
        mime="text/csv",
    )

else:
    # ── EMPTY STATE ───────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="card" style="text-align:center">
            <div style="font-size:2rem">🔍</div>
            <h3>Root Cause Detection</h3>
            <p style="color:#64748b;font-size:0.9rem">Automatically identifies the dominant failure type from your logs using weighted keyword analysis.</p>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="card" style="text-align:center">
            <div style="font-size:2rem">📈</div>
            <h3>Trend Analysis</h3>
            <p style="color:#64748b;font-size:0.9rem">Visualises how issues evolve over time using configurable time buckets.</p>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="card" style="text-align:center">
            <div style="font-size:2rem">💡</div>
            <h3>Fix Suggestions</h3>
            <p style="color:#64748b;font-size:0.9rem">Returns curated remediation steps matched to the identified root cause.</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("👆 Upload a `.log` file above to get started. A sample file is available at `backend/logs/test.log`.")
