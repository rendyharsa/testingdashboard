import io
import pandas as pd
import plotly.express as px
import streamlit as st

# -----------------------------------------------------------------------------
# 1. Corporate Brand Palette Configuration
# -----------------------------------------------------------------------------
CORP_ORANGE = "#F26522"  # MPM Corporate Primary Orange
CORP_LIGHT_BLUE = "#38BDF8"  # Corporate Accent Light Blue
CORP_DARK_BLUE = "#0F172A"  # Slate Dark Background
CORP_CARD_BG = "#1E293B"  # Card Background
CORP_BORDER = "#334155"  # Card Border

BRAND_PALETTE = {
    "Google Search": CORP_ORANGE,
    "Meta Retargeting": CORP_LIGHT_BLUE,
    "TikTok Awareness": "#A855F7",  # Soft Purple Accent
}

# -----------------------------------------------------------------------------
# 2. Page Configuration & Custom Corporate Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Marketing Strategy & ROI Dashboard",
    page_icon="🟧",
    layout="wide",
)

st.markdown(
    f"""
    <style>
        /* Card Container Styling with Corporate Accent Borders */
        div[data-testid="stMetric"] {{
            background-color: {CORP_CARD_BG};
            border-left: 4px solid {CORP_ORANGE};
            border-top: 1px solid {CORP_BORDER};
            border-right: 1px solid {CORP_BORDER};
            border-bottom: 1px solid {CORP_BORDER};
            padding: 18px 22px;
            border-radius: 8px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        }}
        
        /* Metric Label Styling */
        div[data-testid="stMetricLabel"] {{
            font-size: 0.85rem !important;
            font-weight: 600 !important;
            color: #94A3B8 !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        /* Metric Value Styling */
        div[data-testid="stMetricValue"] {{
            font-size: 1.8rem !important;
            font-weight: 700 !important;
            color: #F8FAFC !important;
        }}

        /* Expander Custom Border Accent */
        div[data-testid="stExpander"] {{
            border: 1px solid {CORP_BORDER};
            border-left: 4px solid {CORP_LIGHT_BLUE};
            border-radius: 8px;
            background-color: {CORP_CARD_BG};
        }}

        /* Section Dividers */
        hr {{
            margin-top: 1.5rem;
            margin-bottom: 1.5rem;
            border-color: {CORP_BORDER};
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 3. Data Loading & Preprocessing
# -----------------------------------------------------------------------------
csv_data = """Date, Campaign, Spend, Clicks, Conversions, Revenue
2026-07-01, Google Search, 1200, 340, 28, 4200
2026-07-02, Meta Retargeting, 850, 210, 19, 2850
2026-07-03, Google Search, 1350, 390, 31, 4650
2026-07-04, Meta Retargeting, 900, 230, 22, 3300
2026-07-05, TikTok Awareness, 500, 450, 8, 800
2026-07-06, Google Search, 1100, 310, 25, 3750
2026-07-07, Meta Retargeting, 800, 190, 18, 2700"""


@st.cache_data
def load_data():
    df = pd.read_csv(io.StringIO(csv_data))
    df.columns = df.columns.str.strip()
    df["Date"] = pd.to_datetime(df["Date"])
    df["Campaign"] = df["Campaign"].str.strip()
    return df


df = load_data()

# -----------------------------------------------------------------------------
# 4. Sidebar Filters & Data Export
# -----------------------------------------------------------------------------
st.sidebar.title("🎛️ Control Panel")
st.sidebar.markdown("---")

all_campaigns = df["Campaign"].unique().tolist()
selected_campaigns = st.sidebar.multiselect(
    "Filter by Campaign:",
    options=all_campaigns,
    default=all_campaigns,
)

filtered_df = (
    df[df["Campaign"].isin(selected_campaigns)] if selected_campaigns else df.iloc[0:0]
)

st.sidebar.markdown("---")
st.sidebar.subheader("📥 Executive Export")

if not filtered_df.empty:
    csv_bytes = filtered_df.to_csv(index=False).encode("utf-8")
    st.sidebar.download_button(
        label="Download Report (CSV)",
        data=csv_bytes,
        file_name="marketing_performance_report.csv",
        mime="text/csv",
        use_container_width=True,
    )
else:
    st.sidebar.info("Select at least one campaign to enable export.")

# -----------------------------------------------------------------------------
# 5. Header & AI Executive Summary
# -----------------------------------------------------------------------------
st.title("📈 Marketing Strategy & ROI Dashboard")
st.caption("Corporate Performance & Campaign Intelligence Dashboard")

if not filtered_df.empty:
    top_revenue_campaign = (
        filtered_df.groupby("Campaign")["Revenue"].sum().idxmax()
    )
    total_spend = filtered_df["Spend"].sum()
    total_revenue = filtered_df["Revenue"].sum()
    avg_roi = total_revenue / total_spend if total_spend > 0 else 0

    with st.expander("🤖 AI Executive Summary & Insights", expanded=True):
        st.markdown(
            f"""
        - **Top Revenue Driver:** **{top_revenue_campaign}** generated the highest total return within the selected filters.
        - **Return on Investment:** The filtered portfolio achieved an overall ROI of **{avg_roi:.2f}x**, generating **${total_revenue:,.2f}** from **${total_spend:,.2f}** spent.
        - **Strategic Note:** High top-of-funnel engagement provides balanced coverage alongside retargeting performance.
        """
        )

st.divider()

# -----------------------------------------------------------------------------
# 6. Top KPI Cards with Period-over-Period Deltas
# -----------------------------------------------------------------------------
if not filtered_df.empty:
    unique_dates = sorted(filtered_df["Date"].unique())
    midpoint = len(unique_dates) // 2

    if midpoint > 0:
        first_half_dates = unique_dates[:midpoint]
        second_half_dates = unique_dates[midpoint:]

        p1_df = filtered_df[filtered_df["Date"].isin(first_half_dates)]
        p2_df = filtered_df[filtered_df["Date"].isin(second_half_dates)]

        spend_p1, spend_p2 = p1_df["Spend"].sum(), p2_df["Spend"].sum()
        spend_delta = (
            ((spend_p2 - spend_p1) / spend_p1 * 100) if spend_p1 > 0 else 0
        )

        rev_p1, rev_p2 = p1_df["Revenue"].sum(), p2_df["Revenue"].sum()
        rev_delta = ((rev_p2 - rev_p1) / rev_p1 * 100) if rev_p1 > 0 else 0

        conv_p1, conv_p2 = p1_df["Conversions"].sum(), p2_df["Conversions"].sum()
        conv_delta = ((conv_p2 - conv_p1) / conv_p1 * 100) if conv_p1 > 0 else 0

        roi_p1 = rev_p1 / spend_p1 if spend_p1 > 0 else 0
        roi_p2 = rev_p2 / spend_p2 if spend_p2 > 0 else 0
        roi_delta = ((roi_p2 - roi_p1) / roi_p1 * 100) if roi_p1 > 0 else 0
    else:
        spend_delta = rev_delta = conv_delta = roi_delta = 0.0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Total Spend",
            value=f"${total_spend:,.2f}",
            delta=f"{spend_delta:+.1f}% vs prior period",
            delta_color="inverse",
        )
    with col2:
        st.metric(
            label="Total Revenue",
            value=f"${total_revenue:,.2f}",
            delta=f"{rev_delta:+.1f}% vs prior period",
        )
    with col3:
        st.metric(
            label="Total Conversions",
            value=f"{filtered_df['Conversions'].sum():,}",
            delta=f"{conv_delta:+.1f}% vs prior period",
        )
    with col4:
        st.metric(
            label="Overall ROI",
            value=f"{avg_roi:.2f}x",
            delta=f"{roi_delta:+.1f}% vs prior period",
        )

    st.divider()

    # -----------------------------------------------------------------------------
    # 7. Interactive Corporate Visualizations
    # -----------------------------------------------------------------------------
    col_chart1, col_chart2 = st.columns(2)

    # Chart 1: Daily Revenue vs Spend Line Chart
    with col_chart1:
        st.subheader("Daily Revenue Trend")
        daily_df = (
            filtered_df.groupby(["Date", "Campaign"])[["Revenue", "Spend"]]
            .sum()
            .reset_index()
        )

        fig_line = px.line(
            daily_df,
            x="Date",
            y="Revenue",
            color="Campaign",
            markers=True,
            color_discrete_map=BRAND_PALETTE,
            hover_data={"Spend": ":$,.2f", "Revenue": ":$,.2f", "Date": "|%B %d, %Y"},
            labels={"Revenue": "Revenue ($)", "Date": "Date"},
        )
        fig_line.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
            ),
            hovermode="x unified",
            margin=dict(l=10, r=10, t=30, b=10),
        )
        st.plotly_chart(fig_line, use_container_width=True)

    # Chart 2: Conversions by Campaign Bar Chart
    with col_chart2:
        st.subheader("Conversions by Campaign")
        camp_df = (
            filtered_df.groupby("Campaign")[["Conversions", "Spend", "Revenue"]]
            .sum()
            .reset_index()
        )

        fig_bar = px.bar(
            camp_df,
            x="Campaign",
            y="Conversions",
            color="Campaign",
            color_discrete_map=BRAND_PALETTE,
            text_auto=True,
            hover_data={"Spend": ":$,.2f", "Revenue": ":$,.2f"},
            labels={"Conversions": "Total Conversions"},
        )
        fig_bar.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            margin=dict(l=10, r=10, t=30, b=10),
        )
        fig_bar.update_traces(
            textposition="outside",
            marker_line_color=CORP_ORANGE,
            marker_line_width=1.5,
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    st.divider()

    # -----------------------------------------------------------------------------
    # 8. Filtered Raw Data Table
    # -----------------------------------------------------------------------------
    st.subheader("📋 Filtered Raw Data")

    display_df = filtered_df.copy()
    display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Spend": st.column_config.NumberColumn("Spend", format="$%d"),
            "Revenue": st.column_config.NumberColumn("Revenue", format="$%d"),
            "Clicks": st.column_config.NumberColumn("Clicks", format="%d"),
            "Conversions": st.column_config.NumberColumn("Conversions", format="%d"),
        },
    )

else:
    st.warning("⚠️ No data available. Please select at least one campaign from the sidebar.")
