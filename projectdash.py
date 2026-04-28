import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Customer Marketing Dashboard",
    page_icon="📊",
    layout="wide"
)

# Load data
df = pd.read_excel("marketing_campaign_cleaned.xlsx")

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.hero {
    background: linear-gradient(135deg, #f0f4ff 0%, #fafafa 100%);
    border: 1px solid #e0e7ff;
    border-left: 4px solid #2563eb;
    border-radius: 12px;
    padding: 1.4rem 1.8rem;
    margin-bottom: 1.5rem;
}
.hero h1 { font-size: 1.6rem; font-weight: 700; color: #111; margin: 0 0 0.4rem 0; }
.hero p  { font-size: 0.88rem; color: #555; line-height: 1.7; margin: 0; }
.hero .meta { font-size: 0.75rem; color: #888; margin-top: 0.6rem; }
.hero .meta b { color: #2563eb; }
</style>

<div class="hero">
  <h1>📊 Customer Behavior & Marketing Campaign Dashboard</h1>
  <p>
    This dashboard explores customer purchasing behavior and campaign response patterns
    for a retail company across <b>2,237 customers</b>. The dataset covers demographics
    (age, education, income, marital status), spending across product categories
    (wine, meat, fish, sweets, gold), and purchase channels (web, store, catalog).
    Use the sidebar filters to segment customers and explore trends.
  </p>
  <div class="meta">
    <b>Dataset:</b> Customer Marketing Campaign &nbsp;·&nbsp;
    <b>Customers:</b> 2,237 &nbsp;·&nbsp;
    <b>Variables:</b> Demographics, Spending, Channels, Campaign Response
  </div>
</div>
""", unsafe_allow_html=True)

# ── Sidebar Filters ───────────────────────────────────────────────────────────
st.sidebar.header("Filters")

age_range = st.sidebar.slider(
    "Age Range",
    int(df["Age"].min()), int(df["Age"].max()),
    (int(df["Age"].min()), int(df["Age"].max()))
)

income_range = st.sidebar.slider(
    "Income Range ($)",
    int(df["Income"].min()), int(df["Income"].max()),
    (int(df["Income"].min()), int(df["Income"].max()))
)

education_filter = st.sidebar.multiselect(
    "Education Level",
    df["Education"].unique(),
    default=list(df["Education"].unique())
)

marital_filter = st.sidebar.multiselect(
    "Marital Status",
    df["Marital_Status"].unique(),
    default=list(df["Marital_Status"].unique())
)

# ── Apply Filters ─────────────────────────────────────────────────────────────
filtered_df = df[
    (df["Age"].between(age_range[0], age_range[1])) &
    (df["Income"].between(income_range[0], income_range[1])) &
    (df["Education"].isin(education_filter)) &
    (df["Marital_Status"].isin(marital_filter))
]

st.markdown(f"**{len(filtered_df):,} customers** match the current filters.")

if len(filtered_df) == 0:
    st.error("No data found for the selected filters. Try adjusting your selections.")
    st.stop()

# ── KPI Row ───────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
k1.metric("Customers", f"{len(filtered_df):,}")
k2.metric("Avg Income", f"${filtered_df['Income'].mean():,.0f}")
k3.metric("Avg Total Spent", f"${filtered_df['TotalSpent'].mean():,.0f}")
k4.metric("Avg Age", f"{filtered_df['Age'].mean():.0f} yrs")

st.markdown("---")

# ── Chart 1: Spending by Education ───────────────────────────────────────────
st.subheader("1. Average Spending by Education Level")
st.caption("Higher education levels tend to correlate with higher total spending across all product categories.")

bar_data = filtered_df.groupby("Education")["TotalSpent"].mean().reset_index()
bar_data = bar_data.sort_values(by="TotalSpent", ascending=False)

fig_bar = px.bar(
    bar_data, x="Education", y="TotalSpent",
    title="Average Total Spending by Education Level",
    labels={"TotalSpent": "Avg Total Spent ($)", "Education": "Education Level"}
)
fig_bar.update_traces(
    marker=dict(color=bar_data["TotalSpent"], colorscale="Blues"),
    texttemplate='$%{y:.0f}', textposition='outside'
)
avg_spending = bar_data["TotalSpent"].mean()
fig_bar.add_hline(y=avg_spending, line_dash="dot", line_color="red",
                  annotation_text=f"Avg: ${avg_spending:.0f}", annotation_position="top right")
fig_bar.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig_bar, use_container_width=True)

# ── Chart 2: Purchases by Age ─────────────────────────────────────────────────
st.subheader("2. Total Purchases by Age")
st.caption("Tracks the average number of purchases (web + store + catalog) across different customer age groups.")

filtered_df = filtered_df.copy()
filtered_df["TotalPurchases"] = (
    filtered_df["NumWebPurchases"] +
    filtered_df["NumStorePurchases"] +
    filtered_df["NumCatalogPurchases"]
)

line_data = filtered_df.groupby("Age")["TotalPurchases"].mean().reset_index()

fig_line = px.line(
    line_data, x="Age", y="TotalPurchases",
    title="Average Total Purchases by Age",
    labels={"TotalPurchases": "Avg Purchases", "Age": "Customer Age"}
)
fig_line.update_traces(line_shape="spline", line_color="#2563eb")

peak_idx = line_data["TotalPurchases"].idxmax()
fig_line.add_scatter(
    x=[line_data.loc[peak_idx, "Age"]],
    y=[line_data.loc[peak_idx, "TotalPurchases"]],
    mode="markers+text",
    text=[f"Peak: Age {line_data.loc[peak_idx, 'Age']}"],
    textposition="top center",
    marker=dict(size=12, color="red"),
    showlegend=False
)
fig_line.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig_line, use_container_width=True)

# ── Charts 3 & 4 side by side ─────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("3. Customer Marital Status Breakdown")
    st.caption("Distribution of customers by marital status within the filtered segment.")

    marital_counts = filtered_df["Marital_Status"].value_counts().reset_index()
    marital_counts.columns = ["Marital_Status", "Count"]
    marital_counts = marital_counts.sort_values(by="Count", ascending=False)

    show_legend = st.checkbox("Show Legend", value=True)

    fig_donut = px.pie(
        marital_counts, names="Marital_Status", values="Count",
        hole=0.5, title="Marital Status Distribution"
    )
    fig_donut.update_traces(
        marker=dict(colors=['#3b82f6','#f59e0b','#10b981','#ef4444','#8b5cf6']),
        pull=[0.05] + [0] * (len(marital_counts) - 1),
        textinfo="percent+label"
    )
    fig_donut.update_layout(showlegend=show_legend,
                            paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_donut, use_container_width=True)

with col2:
    st.subheader("4. Income vs. Total Spending")
    st.caption("Higher-income customers spend more overall. Each color represents a different education level.")

    fig_scatter = px.scatter(
        filtered_df, x="Income", y="TotalSpent",
        color="Education", opacity=0.65,
        trendline="ols",
        title="Income vs Total Spending by Education",
        labels={"TotalSpent": "Total Spent ($)", "Income": "Annual Income ($)"}
    )
    fig_scatter.update_layout(
        xaxis=dict(rangeslider=dict(visible=True)),
        hovermode="closest",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("---")
st.markdown("<div style='text-align:center; color:#aaa; font-size:0.75rem'>Customer Marketing Campaign Dataset · Joseph Nagothu · Analytics Portfolio</div>", unsafe_allow_html=True)
