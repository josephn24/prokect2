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

# ── Styles ────────────────────────────────────────────────────────────────────
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
    margin-bottom: 1rem;
}
.hero h1 { font-size: 1.6rem; font-weight: 700; color: #111; margin: 0 0 0.4rem 0; }
.hero p  { font-size: 0.88rem; color: #555; line-height: 1.7; margin: 0; }
.hero .meta { font-size: 0.75rem; color: #888; margin-top: 0.6rem; }
.hero .meta b { color: #2563eb; }

.about-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
    margin-bottom: 1rem;
}
.about-card {
    background: #f8faff;
    border: 1px solid #e0e7ff;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
}
.about-label {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #2563eb;
    margin-bottom: 0.6rem;
}
.about-text {
    font-size: 0.84rem;
    color: #444;
    line-height: 1.8;
    margin: 0;
}
.about-text b { color: #111; }

.tab-row {
    display: flex;
    flex-direction: column;
    gap: 0.45rem;
}
.tab-item {
    font-size: 0.82rem;
    color: #555;
    line-height: 1.6;
}
.tab-item span {
    color: #2563eb;
    font-weight: 700;
}

.meta-strip {
    background: #f8faff;
    border: 1px solid #e0e7ff;
    border-radius: 12px;
    padding: 0.9rem 1.5rem;
    margin-bottom: 1.6rem;
    display: flex;
    gap: 2.5rem;
    flex-wrap: wrap;
    align-items: center;
}
.meta-item-label {
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #aab;
    margin-bottom: 0.2rem;
}
.meta-item-value {
    font-size: 0.82rem;
    color: #444;
}
</style>
""", unsafe_allow_html=True)

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>📊 Customer Behavior & Marketing Campaign Dashboard</h1>
  <p>
    Retail customer analytics dashboard exploring purchasing behavior, campaign response patterns,
    and demographic-driven spending across <b>2,237 customers</b>.
  </p>
  <div class="meta">
    <b>Dataset:</b> Customer Marketing Campaign &nbsp;·&nbsp;
    <b>Customers:</b> 2,237 &nbsp;·&nbsp;
    <b>Variables:</b> Demographics, Spending, Channels, Campaign Response
  </div>
</div>
""", unsafe_allow_html=True)

# ── About Panel ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="about-grid">
  <div class="about-card">
    <div class="about-label">What This Dashboard Analyzes</div>
    <p class="about-text">
      This dashboard explores how <b>demographics, income, and education</b> shape purchasing behavior
      across a retail customer base of <b>2,237 people</b>. It breaks down spending across product
      categories — wine, meat, fish, sweets, and gold — and tracks how customers engage across
      three purchase channels: <b>web, in-store, and catalog</b>.<br><br>
      The goal is to surface which customer segments spend the most, which channels they prefer,
      and where marketing campaigns are most likely to land — giving a marketing or analytics team
      a clear picture of where to focus acquisition and retention efforts.
    </p>
  </div>
  <div class="about-card">
    <div class="about-label">How To Use It</div>
    <p class="about-text" style="margin-bottom: 0.7rem;">
      Use the <b>sidebar filters</b> to slice the data by age range, income range, education level,
      and marital status. All charts update in real time to reflect your selected segment.
    </p>
    <div class="tab-row">
      <div class="tab-item"><span>KPI Row</span> — Live counts of customers, average income, average total spend, and average age for the filtered segment.</div>
      <div class="tab-item"><span>Chart 1</span> — Average spending by education level, with a dotted average benchmark line to spot above/below-average groups.</div>
      <div class="tab-item"><span>Chart 2</span> — Total purchases (web + store + catalog) by customer age, with the peak purchase age annotated.</div>
      <div class="tab-item"><span>Chart 3</span> — Marital status breakdown as a donut chart for the filtered segment.</div>
      <div class="tab-item"><span>Chart 4</span> — Income vs. total spending scatter plot, colored by education level, with an OLS trend line.</div>
    </div>
  </div>
</div>

<div class="meta-strip">
  <div>
    <div class="meta-item-label">Dataset</div>
    <div class="meta-item-value">Customer Marketing Campaign</div>
  </div>
  <div>
    <div class="meta-item-label">Customers</div>
    <div class="meta-item-value">2,237</div>
  </div>
  <div>
    <div class="meta-item-label">Analysis Type</div>
    <div class="meta-item-value">Demographic segmentation · Channel attribution</div>
  </div>
  <div>
    <div class="meta-item-label">Key Metrics</div>
    <div class="meta-item-value">Avg spend · Purchase volume · Income correlation</div>
  </div>
  <div>
    <div class="meta-item-label">Tools</div>
    <div class="meta-item-value">Python · Streamlit · Plotly · Pandas</div>
  </div>
  <div>
    <div class="meta-item-label">Built By</div>
    <div class="meta-item-value">Joseph Nagothu · Analytics Portfolio</div>
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
