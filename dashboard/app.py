import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
pio.templates["ak_light"] = pio.templates["plotly_white"]
pio.templates["ak_light"].layout.font.color = "#211F1A"
pio.templates["ak_light"].layout.title.font.color = "#211F1A"
pio.templates["ak_light"].layout.legend.font.color = "#211F1A"
pio.templates["ak_light"].layout.xaxis.title.font.color = "#211F1A"
pio.templates["ak_light"].layout.yaxis.title.font.color = "#211F1A"
pio.templates.default = "ak_light"

st.set_page_config(page_title="Arabian Kitchen — Analytics", layout="wide", page_icon="🍽️")

ACCENT = "#B24A1E"
ACCENT2 = "#2C5F58"
PAPER = "#EFECE3"
CARD = "#F7F5EE"
RULE = "#D9D5C7"
INK = "#211F1A"
INK_SOFT = "#5B584E"

CHART_MARGIN = dict(l=10, r=10, t=10, b=10)

def style_chart(fig, height=380, legend=False):
    fig.update_layout(
        font_color=INK,
        font_family="IBM Plex Sans, sans-serif",
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=legend,
        height=height,
        margin=CHART_MARGIN,
        xaxis=dict(gridcolor=RULE, zeroline=False),
        yaxis=dict(gridcolor=RULE, zeroline=False),
    )
    return fig

st.html(f"""
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@500&display=swap" rel="stylesheet">
<style>
html, body, .stApp {{
    background-color: {PAPER};
    color: {INK};
    font-family: 'IBM Plex Sans', sans-serif;
}}
.stApp, .stApp p, .stApp span, .stApp label, .stApp div {{ color: {INK}; }}

/* page padding */
.block-container {{ padding-top: 2.5rem; padding-bottom: 3rem; max-width: 1200px; }}

/* headline / title */
h1 {{
    font-family: 'Fraunces', serif !important;
    font-weight: 600 !important;
    font-size: 2.1rem !important;
    letter-spacing: -0.01em;
    margin-bottom: 0.2rem !important;
}}
[data-testid="stCaptionContainer"] {{
    color: {INK_SOFT} !important;
    font-size: 0.95rem;
    margin-bottom: 2rem;
}}

/* section subheaders */
h3 {{
    font-family: 'Fraunces', serif !important;
    font-weight: 500 !important;
    font-size: 1.15rem !important;
    color: {INK} !important;
    margin-bottom: 0.8rem !important;
}}

/* dividers -> thin hairlines with breathing room */
hr {{ border-color: {RULE} !important; margin: 2.2rem 0 !important; }}

/* sidebar */
section[data-testid="stSidebar"] {{ background-color: #E6E2D6; border-right: 1px solid {RULE}; }}
section[data-testid="stSidebar"] * {{ color: {INK} !important; }}
section[data-testid="stSidebar"] h2 {{
    font-family: 'Fraunces', serif !important;
    font-size: 1.1rem !important;
    margin-bottom: 1rem !important;
}}
section[data-testid="stSidebar"] .block-container {{ padding-top: 2rem; }}

/* KPI metric cards */
[data-testid="stMetric"] {{
    background-color: {CARD};
    border: 1px solid {RULE};
    padding: 18px 20px;
    border-radius: 2px;
}}
[data-testid="stMetricValue"] {{
    color: {ACCENT} !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 1.6rem !important;
}}
[data-testid="stMetricLabel"] {{
    color: {INK_SOFT} !important;
    font-size: 0.82rem !important;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}}

/* dataframe / expander */
.stDataFrame, .stExpander, .stExpander * {{ color: {INK} !important; }}
.stExpander {{ border: 1px solid {RULE} !important; background-color: {CARD}; }}

/* multiselect / selectbox chips and text */
[data-baseweb="select"] * {{ color: {INK} !important; }}
[data-baseweb="tag"] {{ color: white !important; background-color: {ACCENT} !important; }}

/* remove default streamlit top padding on charts wrapper */
[data-testid="stVerticalBlock"] {{ gap: 0.6rem; }}
</style>
""")


@st.cache_data
def load_data():
    df = pd.read_csv("../data/clean/arabian_kitchen_orders_clean.csv")
    df["datetime"] = pd.to_datetime(df["datetime"])
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

st.title("Arabian Kitchen — Sales & Operations Dashboard")
st.caption("Chennai · Arabian/Middle Eastern restaurant · Order-level analytics")


st.sidebar.header("Filters")

start_date, end_date = st.sidebar.columns(2)
with start_date:
    date_start = st.date_input(
        "From",
        value=df["date"].min(),
        min_value=df["date"].min(),
        max_value=df["date"].max(),
    )
with end_date:
    date_end = st.date_input(
        "To",
        value=df["date"].max(),
        min_value=df["date"].min(),
        max_value=df["date"].max(),
    )

if date_start > date_end:
    st.sidebar.warning("Start date is after end date — showing no data for that range.")

order_types = st.sidebar.multiselect(
    "Order type",
    options=sorted(df["order_type"].unique()),
    default=sorted(df["order_type"].unique()),
)

payment_modes = st.sidebar.multiselect(
    "Payment mode",
    options=sorted(df["payment_mode"].unique()),
    default=sorted(df["payment_mode"].unique()),
)


mask = (
    (df["date"] >= pd.to_datetime(date_start))
    & (df["date"] <= pd.to_datetime(date_end))
    & (df["order_type"].isin(order_types))
    & (df["payment_mode"].isin(payment_modes))
)
fdf = df[mask]


col1, col2, col3, col4 = st.columns(4)
col1.metric("Total revenue", f"₹{fdf['revenue'].sum():,.0f}")
col2.metric("Orders", f"{fdf['order_id'].nunique():,}")
col3.metric("Avg order value", f"₹{fdf.groupby('order_id')['revenue'].sum().mean():,.0f}")
col4.metric("Line items sold", f"{fdf['quantity'].sum():,.0f}")

st.divider()


c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("Revenue by menu item")
    item_rev = fdf.groupby("item_name")["revenue"].sum().sort_values(ascending=True)
    fig = px.bar(item_rev, orientation="h", labels={"value": "Revenue (₹)", "item_name": ""})
    fig.update_traces(marker_color=ACCENT)
    style_chart(fig, height=520)
    st.plotly_chart(fig, width='stretch', theme=None)

with c2:
    st.subheader("Order type split")
    ot = fdf.groupby("order_type")["revenue"].sum()
    fig2 = px.pie(values=ot.values, names=ot.index, color_discrete_sequence=[ACCENT, ACCENT2, "#8A8672"], hole=0.45)
    style_chart(fig2, height=520, legend=True)
    fig2.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.15))
    st.plotly_chart(fig2, width='stretch', theme=None)

st.divider()


c3, c4 = st.columns(2)

with c3:
    st.subheader("Revenue by hour of day")
    hourly = fdf.groupby("hour")["revenue"].sum()
    fig3 = px.bar(hourly, labels={"value": "Revenue (₹)", "hour": "Hour"})
    fig3.update_traces(marker_color=ACCENT2)
    style_chart(fig3)
    st.plotly_chart(fig3, width='stretch', theme=None)

with c4:
    st.subheader("Revenue by day of week")
    dow_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    dow = fdf.groupby("day_of_week")["revenue"].sum().reindex(dow_order)
    fig4 = px.bar(dow, labels={"value": "Revenue (₹)", "day_of_week": ""})
    fig4.update_traces(marker_color=ACCENT)
    style_chart(fig4)
    st.plotly_chart(fig4, width='stretch', theme=None)

st.divider()


st.subheader("Monthly revenue trend")
monthly = fdf.groupby("month")["revenue"].sum().reset_index()
fig5 = px.line(monthly, x="month", y="revenue", markers=True, labels={"revenue": "Revenue (₹)", "month": ""})
fig5.update_traces(line_color=ACCENT, line_width=2.5, marker_size=7, marker_color=ACCENT)
style_chart(fig5, height=340)
st.plotly_chart(fig5, width='stretch', theme=None)

st.divider()

c5, c6 = st.columns(2)

with c5:
    st.subheader("Payment mode breakdown")
    pay = fdf.groupby("payment_mode")["revenue"].sum().sort_values(ascending=False)
    fig6 = px.bar(pay, labels={"value": "Revenue (₹)", "payment_mode": ""})
    fig6.update_traces(marker_color=ACCENT2)
    style_chart(fig6)
    st.plotly_chart(fig6, width='stretch', theme=None)

with c6:
    st.subheader("Delivery platform breakdown")
    delivery = fdf[fdf["order_type"] == "Delivery"]
    if len(delivery) > 0:
        plat = delivery.groupby("platform")["revenue"].sum().sort_values(ascending=False)
        fig7 = px.bar(plat, labels={"value": "Revenue (₹)", "platform": ""})
        fig7.update_traces(marker_color=ACCENT)
        style_chart(fig7)
        st.plotly_chart(fig7, width='stretch', theme=None)
    else:
        st.info("No delivery orders in the selected filter range.")

st.divider()

# ---------------------------------------------------------------
# Raw data explorer
# ---------------------------------------------------------------
with st.expander("View filtered raw data"):
    st.dataframe(fdf.sort_values("datetime", ascending=False), width='stretch')
