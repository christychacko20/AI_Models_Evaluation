from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="AI Technology Evaluation",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

ACCENT = "#5b4bdb"
CYAN = "#1687a7"
GREEN = "#17835b"
AMBER = "#b7791f"
BG = "#f4f6f8"

DEFAULT_MODELS = pd.DataFrame(
    [
        {
            "Model": "GPT-4o",
            "Provider": "OpenAI",
            "Accuracy": 94,
            "Latency (ms)": 820,
            "Reliability": 97,
            "Cost / 1K requests ($)": 18.40,
            "Best for": "Complex reasoning",
            "Summary": "Highest quality for nuanced, high-stakes workflows.",
        },
        {
            "Model": "Claude 3.5 Sonnet",
            "Provider": "Anthropic",
            "Accuracy": 93,
            "Latency (ms)": 690,
            "Reliability": 96,
            "Cost / 1K requests ($)": 14.20,
            "Best for": "Analysis & writing",
            "Summary": "Strong reasoning with excellent long-form business writing.",
        },
        {
            "Model": "Gemini 1.5 Pro",
            "Provider": "Google",
            "Accuracy": 90,
            "Latency (ms)": 760,
            "Reliability": 94,
            "Cost / 1K requests ($)": 11.80,
            "Best for": "Multimodal tasks",
            "Summary": "Flexible multimodal model with a strong cost-to-quality ratio.",
        },
        {
            "Model": "Llama 3.1 70B",
            "Provider": "Meta",
            "Accuracy": 87,
            "Latency (ms)": 460,
            "Reliability": 91,
            "Cost / 1K requests ($)": 5.60,
            "Best for": "High-volume automation",
            "Summary": "Fast, economical option for scalable internal workflows.",
        },
    ]
)

USE_CASES = pd.DataFrame(
    [
        {
            "Use case": "Customer support copilot",
            "Priority": "High",
            "Accuracy need": 88,
            "Speed need": 80,
            "Cost sensitivity": 65,
            "Recommended": "Claude 3.5 Sonnet",
            "Rationale": "Balances accurate answers, tone, and response speed for agent assistance.",
        },
        {
            "Use case": "Contract & policy review",
            "Priority": "High",
            "Accuracy need": 95,
            "Speed need": 55,
            "Cost sensitivity": 40,
            "Recommended": "GPT-4o",
            "Rationale": "Best fit where nuanced reasoning and low error rates outweigh latency.",
        },
        {
            "Use case": "Document extraction",
            "Priority": "Medium",
            "Accuracy need": 86,
            "Speed need": 75,
            "Cost sensitivity": 75,
            "Recommended": "Gemini 1.5 Pro",
            "Rationale": "Multimodal flexibility supports diverse document formats at a reasonable cost.",
        },
        {
            "Use case": "Internal knowledge search",
            "Priority": "High",
            "Accuracy need": 90,
            "Speed need": 88,
            "Cost sensitivity": 70,
            "Recommended": "Llama 3.1 70B",
            "Rationale": "Fast, economical responses make it suitable for high-volume employee queries.",
        },
        {
            "Use case": "Executive insight generation",
            "Priority": "Medium",
            "Accuracy need": 92,
            "Speed need": 60,
            "Cost sensitivity": 45,
            "Recommended": "Claude 3.5 Sonnet",
            "Rationale": "Strong synthesis and writing quality produce decision-ready narratives.",
        },
    ]
)


def inject_styles() -> None:
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
        html, body, [class*="css"] {{ font-family: 'DM Sans', sans-serif; }}
        .stApp {{ background: {BG}; color: #182230; }}
        [data-testid="stSidebar"] {{ background: #ffffff; border-right: 1px solid #e1e5ea; }}
        .block-container {{ padding: 4rem 3rem 4rem; max-width: 1500px; }}
        h1, h2, h3 {{ font-family: 'Space Grotesk', sans-serif; color: #172033; letter-spacing: -0.03em; }}
        h1 {{ font-size: 2.7rem !important; }}
        h2 {{ margin-top: 1.3rem; }}
        [data-testid="stMetric"] {{
            background: #ffffff;
            border: 1px solid #e1e5ea; border-radius: 14px; padding: 16px 18px;
            box-shadow: 0 4px 16px rgba(30, 41, 59, .05);
        }}
        [data-testid="stMetricLabel"] {{ color: #64748b; }}
        [data-testid="stMetricValue"] {{ color: #172033; font-family: 'Space Grotesk'; }}
        .eyebrow {{ color: {CYAN}; text-transform: uppercase; font-weight: 700; font-size: .75rem; letter-spacing: .16em; }}
        .hero {{ padding: 1.2rem 0 1rem; }}
        .hero p {{ color: #64748b; font-size: 1.05rem; max-width: 750px; line-height: 1.65; }}
        .pill {{ display: inline-block; background: #f8fafc; border: 1px solid #d7dee7; border-radius: 999px; padding: 5px 11px; margin: 3px 4px 0 0; color: #475569; font-size: .8rem; }}
        .insight {{ border-left: 3px solid {ACCENT}; background: #ffffff; border-radius: 0 12px 12px 0; padding: 12px 16px; margin: 8px 0; color: #334155; box-shadow: 0 3px 12px rgba(30, 41, 59, .05); }}
        .rec-card {{ background: #ffffff; border: 1px solid #e1e5ea; border-radius: 16px; padding: 19px; height: 100%; box-shadow: 0 4px 16px rgba(30, 41, 59, .05); }}
        .rec-card strong {{ color: #172033; font-size: 1.05rem; }}
        .rec-card small {{ color: #64748b; }}
        .stTabs [data-baseweb="tab-list"] {{ gap: 8px; }}
        .stTabs [data-baseweb="tab"] {{ background: #e9edf2; border-radius: 10px; padding: 8px 18px; color: #475569; }}
        .stTabs [aria-selected="true"] {{ background: #ffffff !important; color: {ACCENT} !important; }}
        div[data-testid="stDataFrame"] {{ border: 1px solid #dfe5eb; border-radius: 10px; background: #ffffff; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def load_data() -> pd.DataFrame:
    uploaded = st.sidebar.file_uploader(
        "Upload benchmark CSV",
        type=["csv"],
        help="Expected columns: Model, Provider, Accuracy, Latency (ms), Reliability, Cost / 1K requests ($).",
    )
    if uploaded is None:
        return DEFAULT_MODELS.copy()
    try:
        data = pd.read_csv(uploaded)
        required = set(DEFAULT_MODELS.columns[:6])
        missing = required.difference(data.columns)
        if missing:
            st.sidebar.error(f"Missing columns: {', '.join(sorted(missing))}")
            return DEFAULT_MODELS.copy()
        for column in ["Accuracy", "Latency (ms)", "Reliability", "Cost / 1K requests ($)"]:
            data[column] = pd.to_numeric(data[column], errors="coerce")
        data = data.dropna(subset=list(required)).reset_index(drop=True)
        if data.empty:
            st.sidebar.error("The uploaded file contains no valid benchmark rows.")
            return DEFAULT_MODELS.copy()
        for column, default in [("Best for", "Custom evaluation"), ("Summary", "Uploaded benchmark result.")]:
            if column not in data.columns:
                data[column] = default
        return data
    except (pd.errors.ParserError, UnicodeDecodeError) as exc:
        st.sidebar.error(f"Could not read CSV: {exc}")
        return DEFAULT_MODELS.copy()


def calculate_scores(data: pd.DataFrame, weights: dict[str, float]) -> pd.DataFrame:
    scored = data.copy()
    scored["Speed"] = 100 * (
        (scored["Latency (ms)"].max() - scored["Latency (ms)"])
        / (scored["Latency (ms)"].max() - scored["Latency (ms)"].min() or 1)
    )
    scored["Value"] = 100 * (
        (scored["Cost / 1K requests ($)"].max() - scored["Cost / 1K requests ($)"])
        / (
            scored["Cost / 1K requests ($)"].max()
            - scored["Cost / 1K requests ($)"].min()
            or 1
        )
    )
    scored["Overall score"] = (
        scored["Accuracy"] * weights["Accuracy"]
        + scored["Speed"] * weights["Speed"]
        + scored["Reliability"] * weights["Reliability"]
        + scored["Value"] * weights["Value"]
    ).round(1)
    return scored.sort_values("Overall score", ascending=False).reset_index(drop=True)


def score_chart(scored: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    for metric, color in [
        ("Accuracy", CYAN),
        ("Speed", ACCENT),
        ("Reliability", GREEN),
        ("Value", AMBER),
    ]:
        fig.add_trace(
            go.Bar(
                name=metric,
                x=scored["Model"],
                y=scored[metric],
                marker_color=color,
                hovertemplate="%{x}<br>" + metric + ": %{y:.1f}<extra></extra>",
            )
        )
    fig.update_layout(
        barmode="group",
        height=390,
        margin=dict(l=10, r=10, t=30, b=10),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#334155"),
        legend=dict(orientation="h", y=1.12),
        yaxis=dict(range=[0, 105], gridcolor="#e2e8f0", title="Normalized score"),
        xaxis=dict(title=None),
    )
    return fig


inject_styles()
data = load_data()

st.markdown('<div class="eyebrow">Generative AI Decision Intelligence</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero"><h1>AI Technology Evaluation<br><span style="color:#8b5cf6">and Business Transformation</span></h1>'
    "<p>A decision dashboard for comparing generative AI models across quality, speed, reliability, and business value — turning technical benchmarks into an adoption roadmap.</p></div>",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### Evaluation priorities")
    st.caption("Adjust the weighting to match your organization's strategy.")
    accuracy_weight = st.slider("Accuracy", 0, 100, 35)
    speed_weight = st.slider("Latency / speed", 0, 100, 20)
    reliability_weight = st.slider("Reliability", 0, 100, 30)
    value_weight = st.slider("Cost efficiency", 0, 100, 15)
    total_weight = accuracy_weight + speed_weight + reliability_weight + value_weight
    if total_weight == 0:
        st.error("Increase at least one priority weight.")
        total_weight = 1
    weights = {
        "Accuracy": accuracy_weight / total_weight,
        "Speed": speed_weight / total_weight,
        "Reliability": reliability_weight / total_weight,
        "Value": value_weight / total_weight,
    }
    st.divider()
    st.markdown("### Benchmark scope")
    st.markdown(
        '<span class="pill">4 models</span><span class="pill">5 use cases</span><span class="pill">2026 snapshot</span>',
        unsafe_allow_html=True,
    )
    st.caption("Replace the scores with any evaluation set you hold using the CSV uploader.")

scored = calculate_scores(data, weights)
leader = scored.iloc[0]
median_latency = data["Latency (ms)"].median()
avg_accuracy = data["Accuracy"].mean()
avg_reliability = data["Reliability"].mean()

metrics = st.columns(4)
metrics[0].metric("Top-ranked model", leader["Model"], f"{leader['Overall score']:.1f} / 100")
metrics[1].metric("Average accuracy", f"{avg_accuracy:.1f}%", "Across benchmark set")
metrics[2].metric("Average reliability", f"{avg_reliability:.1f}%", "Production readiness")
metrics[3].metric("Median latency", f"{median_latency:,.0f} ms", "Response-time baseline")

tab_overview, tab_models, tab_use_cases, tab_recommendations = st.tabs(
    ["Overview", "Model comparison", "Business use cases", "Transformation roadmap"]
)

with tab_overview:
    left, right = st.columns([1.35, 1])
    with left:
        st.subheader("Performance landscape")
        st.plotly_chart(score_chart(scored), use_container_width=True, config={"displayModeBar": False})
    with right:
        st.subheader("Executive readout")
        st.markdown(
            f'<div class="insight"><b>{leader["Model"]}</b> leads the current weighted score at <b>{leader["Overall score"]:.1f}</b>, driven by its {leader["Accuracy"]}% accuracy and {leader["Reliability"]}% reliability.</div>',
            unsafe_allow_html=True,
        )
        best_value = scored.sort_values("Value", ascending=False).iloc[0]
        fastest = scored.sort_values("Latency (ms)").iloc[0]
        st.markdown(
            f'<div class="insight"><b>{best_value["Model"]}</b> is the value leader, costing ${best_value["Cost / 1K requests ($)"]:.2f} per 1K requests — a strong candidate for scale.</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="insight"><b>{fastest["Model"]}</b> is fastest at {fastest["Latency (ms)"]:.0f} ms, making it a good fit for interactive, high-volume automation.</div>',
            unsafe_allow_html=True,
        )
        st.subheader("Evaluation methodology")
        st.caption(
            "Models are scored on a common 0–100 scale. Accuracy and reliability use benchmark percentages; speed and value are normalized relative to the evaluated models. The final score is recalculated from the sidebar priorities."
        )

with tab_models:
    st.subheader("Ranked model comparison")
    display = scored[
        [
            "Model",
            "Provider",
            "Overall score",
            "Accuracy",
            "Reliability",
            "Latency (ms)",
            "Cost / 1K requests ($)",
            "Best for",
        ]
    ].copy()
    st.dataframe(
        display.style.format(
            {
                "Overall score": "{:.1f}",
                "Accuracy": "{:.0f}%",
                "Reliability": "{:.0f}%",
                "Latency (ms)": "{:.0f}",
                "Cost / 1K requests ($)": "${:.2f}",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )
    st.subheader("Quality, speed, and cost trade-off")
    scatter = px.scatter(
        data,
        x="Latency (ms)",
        y="Accuracy",
        size="Reliability",
        color="Model",
        hover_data=["Provider", "Cost / 1K requests ($)"],
        template="plotly_white",
        height=430,
    )
    scatter.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_gridcolor="#e2e8f0",
        yaxis_gridcolor="#e2e8f0",
        legend_title=None,
    )
    st.plotly_chart(scatter, use_container_width=True, config={"displayModeBar": False})

with tab_use_cases:
    st.subheader("Where each model creates business value")
    selected_priority = st.multiselect(
        "Filter by priority",
        options=["High", "Medium"],
        default=["High", "Medium"],
    )
    filtered_use_cases = USE_CASES[USE_CASES["Priority"].isin(selected_priority)]
    for start in range(0, len(filtered_use_cases), 2):
        columns = st.columns(2)
        for column, (_, row) in zip(columns, filtered_use_cases.iloc[start : start + 2].iterrows()):
            with column:
                st.markdown(
                    f'<div class="rec-card"><small>{row["Priority"].upper()} PRIORITY</small><br><strong>{row["Use case"]}</strong><p style="color:#aab4d0">{row["Rationale"]}</p><span class="pill">Recommended: {row["Recommended"]}</span></div>',
                    unsafe_allow_html=True,
                )
    st.subheader("Use-case fit matrix")
    matrix = USE_CASES.pivot(index="Use case", columns="Recommended", values="Priority").fillna("—")
    st.dataframe(matrix, use_container_width=True)

with tab_recommendations:
    st.subheader("Recommended adoption sequence")
    roadmap = [
        ("01", "Start with governed copilots", "Launch customer support and internal knowledge search with human review, feedback capture, and clear escalation paths.", "0–3 months", CYAN),
        ("02", "Scale repeatable workflows", "Automate document extraction and executive insight generation using confidence thresholds and monitoring.", "3–6 months", ACCENT),
        ("03", "Reserve frontier quality for risk", "Route contracts, policy decisions, and other high-stakes tasks to the highest-accuracy model with audit trails.", "6–12 months", GREEN),
    ]
    for number, title, detail, timeline, color in roadmap:
        st.markdown(
            f'<div class="rec-card" style="border-left:4px solid {color}; margin:10px 0"><small>{number} · {timeline}</small><br><strong>{title}</strong><p style="color:#aab4d0; margin-bottom:0">{detail}</p></div>',
            unsafe_allow_html=True,
        )
    st.subheader("Operating principles")
    principles = st.columns(3)
    principles[0].markdown("**Measure before scaling**  \nUse task-specific test sets, not generic benchmarks, and track quality drift over time.")
    principles[1].markdown("**Route by risk and value**  \nMatch model capability and cost to the consequence of an incorrect answer.")
    principles[2].markdown("**Keep humans in the loop**  \nDesign review, feedback, and rollback into every business-critical workflow.")

st.divider()
st.caption("AI Technology Evaluation Dashboard " \
# "Benchmark data is illustrative and designed for demonstration purposes." \
"")
