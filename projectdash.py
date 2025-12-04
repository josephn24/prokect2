##ISTM 635 Project 2 Interactive Dashboard


import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_excel("marketing_campaign_cleaned.xlsx")

# SIDEBAR FILTERS

st.sidebar.header("Filters")

age_range = st.sidebar.slider(
    "Select Age Range",
    int(df["Age"].min()),
    int(df["Age"].max()),
    (int(df["Age"].min()), int(df["Age"].max()))
)

income_range = st.sidebar.slider(
    "Select Income Range",
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

# APPLY FILTERS

filtered_df = df[
    (df["Age"].between(age_range[0], age_range[1])) &
    (df["Income"].between(income_range[0], income_range[1])) &
    (df["Education"].isin(education_filter)) &
    (df["Marital_Status"].isin(marital_filter))
]

st.title("📊 Marketing Campaign Interactive Dashboard")
st.write(f"### Filtered dataset contains **{len(filtered_df)} customers**")

# No-data message
if len(filtered_df) == 0:
    st.error("⚠️ No data found… you're cooked 💀 Try adjusting your filters.")
    st.stop()




# VISUALIZATION 1 – BAR CHART

st.subheader("1. Average Spending by Education Level")

# Student enhancement: sort categories highest→lowest
bar_data = filtered_df.groupby("Education")["TotalSpent"].mean().reset_index()
bar_data = bar_data.sort_values(by="TotalSpent", ascending=False)

fig_bar = px.bar(
    bar_data,
    x="Education",
    y="TotalSpent",
    title="Average Total Spending by Education Level"
)

# Copilot enhancement
fig_bar.update_traces(
    marker=dict(
        color=bar_data["TotalSpent"],
        colorscale="Blues"
    )
)

# Student enhancement: add average reference line + labels
avg_spending = bar_data["TotalSpent"].mean()
fig_bar.add_hline(y=avg_spending, line_dash="dot", line_color="red")

fig_bar.update_traces(
    texttemplate='%{y:.2f}',
    textposition='outside'
)

st.plotly_chart(fig_bar, use_container_width=True)

with st.expander("Enhancements for Bar Chart"):
    st.write("**AI Enhancement:** Copilot added a spending-based color scale.")
    st.write("**Student Enhancement:** Sorted bars, added average reference line, and added value labels.")





# VISUALIZATION 2 – LINE CHART

st.subheader("2. Total Purchases by Age")

filtered_df["TotalPurchases"] = (
    filtered_df["NumWebPurchases"] +
    filtered_df["NumStorePurchases"] +
    filtered_df["NumCatalogPurchases"]
)

line_data = filtered_df.groupby("Age")["TotalPurchases"].mean().reset_index()

fig_line = px.line(
    line_data,
    x="Age",
    y="TotalPurchases",
    title="Average Total Purchases by Age"
)

# Copilot enhancement
fig_line.update_traces(line_shape="spline")

# Student enhancement: highlight peak purchase point
peak_age = line_data["TotalPurchases"].idxmax()
fig_line.add_scatter(
    x=[line_data.loc[peak_age, "Age"]],
    y=[line_data.loc[peak_age, "TotalPurchases"]],
    mode="markers+text",
    text=["Peak"],
    marker=dict(size=12, color="red")
)

st.plotly_chart(fig_line, use_container_width=True)

with st.expander("Enhancements for Line Chart"):
    st.write("**AI Enhancement:** Copilot applied a smooth spline curve.")
    st.write("**Student Enhancement:** I identified and highlighted the peak age.")






# VISUALIZATION 3 – DONUT CHART

st.subheader("3. Customer Marital Status Breakdown")

marital_counts = (
    filtered_df["Marital_Status"].value_counts().reset_index()
)
marital_counts.columns = ["Marital_Status", "Count"]

# Student Enhancement: sort categories largest→smallest
marital_counts = marital_counts.sort_values(by="Count", ascending=False)

# Student Enhancement: add checkbox to toggle legend visibility
show_legend = st.checkbox("Show Legend", value=True)

fig_donut = px.pie(
    marital_counts,
    names="Marital_Status",
    values="Count",
    hole=0.5,
    title="Marital Status Distribution"
)

# Student Enhancement: custom colors + small pull-out interaction
fig_donut.update_traces(
    marker=dict(colors=['#FF9999', '#66B2FF', '#99FF99', '#FFCC66']),
    pull=[0.05] + [0]*(len(marital_counts)-1)
)

# Student Enhancement: apply legend toggle
fig_donut.update_layout(
    showlegend=show_legend
)

st.plotly_chart(fig_donut, use_container_width=True)


# Copilot enhancement
fig_donut.update_traces(textinfo="percent+label")







# VISUALIZATION 4 – SCATTER PLOT

st.subheader("4. Income vs Total Spending")

fig_scatter = px.scatter(
    filtered_df,
    x="Income",
    y="TotalSpent",
    color="Education",
    opacity=0.7,
    title="Income vs Total Spending (Colored by Education)"
)

# Copilot enhancement
fig_scatter = px.scatter(
    filtered_df,
    x="Income",
    y="TotalSpent",
    color="Education",
    opacity=0.7,
    trendline="ols",
    title="Income vs Total Spending with Regression Trendline"
)

# Student enhancement: zoom slider + improved hover for dense cluster analysis
fig_scatter.update_layout(
    xaxis=dict(rangeslider=dict(visible=True)),
    hovermode="closest"
)

st.plotly_chart(fig_scatter, use_container_width=True)

with st.expander("Enhancements for Scatterplot"):
    st.write("**AI Enhancement:** Copilot added a regression trendline.")
    st.write("**Student Enhancement:** Added zoom slider and improved hover for close inspection.")
