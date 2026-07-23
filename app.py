import io
import pandas as pd
import streamlit as st

# -----------------------------------------------------------------------------
# 1. Page Configuration & Title
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Marketing Strategy & ROI Dashboard",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Marketing Strategy & ROI Dashboard")
st.caption("Track performance, spend efficiency, and campaign conversions.")

# -----------------------------------------------------------------------------
# 2. Sample Data Loading
# -----------------------------------------------------------------------------
csv_data = """Date, Campaign, Spend, Clicks, Conversions, Revenue
2026-07-01, Google Search, 1200, 340, 28, 4200
2026-07-02, Meta Retargeting, 850, 210, 19, 2850
2026-07-03, Google Search, 1350, 390, 31, 4650
2026-07-04, Meta Retargeting, 900, 230, 22, 3300
2026-07-05, TikTok Awareness, 500, 450, 8, 800
2026-07-06, Google Search, 1100, 310, 25, 3750
2026-07-07, Meta Retargeting, 800, 190, 18, 2700"""

df = pd.read_csv(io.StringIO(csv_data))

# Clean column names and data types
df.columns = df.columns.str.strip()
df["Date"] = pd.to_datetime(df["Date"])
df["Campaign"] = df["Campaign"].str.strip()

# -----------------------------------------------------------------------------
# 3. Sidebar Filter
# -----------------------------------------------------------------------------
st.sidebar.header("Filter Options")

all_campaigns = df["Campaign"].unique().tolist()
selected_campaigns = st.sidebar.multiselect(
    "Select Campaign(s):",
    options=all_campaigns,
    default=all_campaigns,
)

# Filter dataset based on multi-select
if selected_campaigns:
    filtered_df = df[df["Campaign"].isin(selected_campaigns)]
else:
    filtered_df = df.iloc[0:0]  # Empty DataFrame if nothing selected

# -----------------------------------------------------------------------------
# 4. Top KPI Cards
# -----------------------------------------------------------------------------
if not filtered_df.empty:
    total_spend = filtered_df["Spend"].sum()
    total_revenue = filtered_df["Revenue"].sum()
    total_conversions = filtered_df["Conversions"].sum()
    overall_roi = total_revenue / total_spend if total_spend > 0 else 0.0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(label="Total Spend", value=f"${total_spend:,.2f}")
    with col2:
        st.metric(label="Total Revenue", value=f"${total_revenue:,.2f}")
    with col3:
        st.metric(label="Total Conversions", value=f"{total_conversions:,}")
    with col4:
        st.metric(label="Overall ROI", value=f"{overall_roi:.2f}x")
else:
    st.warning("Please select at least one campaign from the sidebar filter.")

st.divider()

# -----------------------------------------------------------------------------
# 5. Visualizations
# -----------------------------------------------------------------------------
if not filtered_df.empty:
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("Daily Revenue vs. Spend")
        # Aggregating by Date in case multiple campaigns share dates
        daily_perf = (
            filtered_df.groupby("Date")[["Revenue", "Spend"]].sum().reset_index()
        )
        daily_perf = daily_perf.set_index("Date")
        st.line_chart(daily_perf)

    with col_chart2:
        st.subheader("Conversions by Campaign")
        campaign_conversions = (
            filtered_df.groupby("Campaign")["Conversions"].sum().reset_index()
        )
        campaign_conversions = campaign_conversions.set_index("Campaign")
        st.bar_chart(campaign_conversions)

    st.divider()

    # -----------------------------------------------------------------------------
    # 6. Interactive Data Table
    # -----------------------------------------------------------------------------
    st.subheader("Filtered Raw Data")

    # Format Date column for display
    display_df = filtered_df.copy()
    display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )
