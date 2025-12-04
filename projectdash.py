"""
ISTM 635 – Project 2

- 4+ business-focused visualizations
- Sidebar filters (Age, Education, Marital Status, Income Range)
- AI-generated enhancements (labeled clearly)
- Student-generated enhancements (labeled clearly)
- Fully auto-updating (all charts respond to filters)

Dataset: marketing_campaign_cleaned.xlsx
"""

import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_excel("marketing_campaign_cleaned.xlsx")

# ===============================
# SIDEBAR FILTERS
# ===============================
st.sidebar.header("Filters")

age_range = st.sidebar.slider("Select Age Range", 
                              int(df["Age"].min()), 
                              int(df["Age"].max()), 
                              (int(df["Age"].min()), int(df["Age"].max()))
                             )

income_range = st.sidebar.slider("Select Income Range",
                                 int(df["Income"].min()),
                                 int(df["Income"].max()),
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

# ===============================
# APPLY FILTERS
# ===============================
filtered_df = df[
    (df["Age"].between(age_range[0], age_range[1])) &
    (df["Income"].between(income_range[0], income_range[1])) &
    (df["Education"].isin(education_filter)) &
    (df["Marital_Status"].isin(marital_filter))
]

st.title("📊 Marketing Campaign Interactive Dashboard")
st.write(f"### Dataset after filtering: {len(filtered_df)} customers")

# ===================================================================
# VISUALIZATION 1 – Bar Chart: Average Total Spending by Education
# ===================================================================
st.subheader("1. Average Spending by Education Level")

fig_bar = px.bar(filtered_df.groupby("Education")["TotalSpent"].mean().reset_index(),
                 x="Education",
                 y="TotalSpent",
                 title="Average Total Spending by Education")

# ---- AI-GENERATED ENHANCEMENT ----
fig_bar.update_traces(marker=dict(color=filtered_df.groupby("Education")["TotalSpent"].mean(),
                                  colorscale="Blues"))

# ---- STUDENT-GENERATED ENHANCEMENT ----
fig_bar.update_traces(texttemplate='%{y:.2f}', textposition='outside')

st.plotly_chart(fig_bar, use_container_width=True)

# === Enhancement Info Box ===
with st.expander("Enhancements for Bar Chart"):
    st.write("**AI Enhancement:** Automatic color scale applied based on TotalSpent.")
    st.write("**Student Enhancement:** Data labels added above each bar for readability.")

# ===================================================================
# VISUALIZATION 2 – Line Chart: Total Purchases by Age
# ===================================================================
st.subheader("2. Total Purchases by Age")

filtered_df["TotalPurchases"] = (
    filtered_df["NumWebPurchases"] +
    filtered_df["NumStorePurchases"] +
    filtered_df["NumCatalogPurchases"]
)

fig_line = px.line(
    filtered_df.groupby("Age")["TotalPurchases"].mean().reset_index(),
    x="Age",
    y="TotalPurchases",
    title="Average Total Purchases by Age"
)

# ---- AI-GENERATED ENHANCEMENT ----
fig_line.update_traces(line_shape="spline")

# ---- STUDENT-GENERATED ENHANCEMENT ----
peak_age = filtered_df.groupby("Age")["TotalPurchases"].mean().idxmax()
peak_value = filtered_df.groupby("Age")["TotalPurchases"].mean().max()
fig_line.add_scatter(
    x=[peak_age], 
    y=[peak_value],
    mode="markers+text",
    text=["Peak"],
    marker=dict(size=12, color="red")
)

st.plotly_chart(fig_line, use_container_width=True)

with st.expander("Enhancements for Line Chart"):
    st.write("**AI Enhancement:** Smooth spline line for better visual interpretation.")
    st.write("**Student Enhancement:** Highlighted the peak purchase age with a red marker.")

# ===================================================================
# VISUALIZATION 3 – Donut Chart: Marital Status Distribution
# ===================================================================
st.subheader("3. Customer Marital Status Breakdown")

marital_counts = filtered_df["Marital_Status"].value_counts().reset_index()
marital_counts.columns = ["Marital_Status", "Count"]

fig_donut = px.pie(
    marital_counts,
    names="Marital_Status",
    values="Count",
    hole=0.5,
    title="Marital Status Distribution"
)

# ---- AI-GENERATED ENHANCEMENT ----
fig_donut.update_traces(textposition="inside", textinfo="percent+label")

# ---- STUDENT-GENERATED ENHANCEMENT ----
fig_donut.update_traces(marker=dict(colors=['#FF9999', '#66B2FF', '#99FF99', '#FFCC66']))

st.plotly_chart(fig_donut, use_container_width=True)

with st.expander("Enhancements for Donut Chart"):
    st.write("**AI Enhancement:** Added percentage labels inside each slice.")
    st.write("**Student Enhancement:** Applied custom color palette for visual clarity.")

# ===================================================================
# VISUALIZATION 4 – Scatter Plot: Income vs Total Spending
# ===================================================================
st.subheader("4. Income vs Total Spending")

fig_scatter = px.scatter(
    filtered_df,
    x="Income",
    y="TotalSpent",
    color="Education",
    title="Income vs Total Spending (Colored by Education)",
    opacity=0.7,
    trendline="ols"
)

# ---- STUDENT-GENERATED ENHANCEMENT ----
fig_scatter.update_traces(
    hovertemplate="<br>".join([
        "Income: %{x}",
        "Total Spent: %{y}",
        "Education: %{marker.color}"
    ])
)

st.plotly_chart(fig_scatter, use_container_width=True)

with st.expander("Enhancements for Scatter Plot"):
    st.write("**AI Enhancement:** Added regression trendline (OLS) to show spending pattern.")
    st.write("**Student Enhancement:** Custom hover tooltip with detailed information.")
