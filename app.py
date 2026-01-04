import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="AI for Good – Stock-Out Risk Monitor",
    layout="wide"
)

# ----------------------------
# Title & Description
# ----------------------------
st.title("🧠 AI-Driven Stock-Out Risk Monitor")
st.caption(
    "AI-for-Good prototype to predict shortages of essential goods "
    "and support proactive decision-making."
)

# ----------------------------
# Generate Synthetic Dataset
# ----------------------------
np.random.seed(42)

regions = ["North", "South", "East", "West"]
items = ["Rice", "Wheat", "Medicine", "Water"]

records = []

for region in regions:
    for item in items:
        demand = np.random.randint(80, 200)
        supply = demand - np.random.randint(-40, 60)

        if supply < demand - 20:
            risk = "High"
        elif supply < demand:
            risk = "Medium"
        else:
            risk = "Low"

        records.append([region, item, demand, supply, risk])

df = pd.DataFrame(
    records,
    columns=["Region", "Item", "Demand", "Supply", "Risk"]
)

# ----------------------------
# Sidebar Filters
# ----------------------------
st.sidebar.header("🔍 Select Parameters")

selected_region = st.sidebar.selectbox("Region", regions)
selected_item = st.sidebar.selectbox("Item", items)

filtered = df[
    (df["Region"] == selected_region) &
    (df["Item"] == selected_item)
]

# ----------------------------
# KPI Metrics
# ----------------------------
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Demand", int(filtered["Demand"]))

with col2:
    st.metric("Supply", int(filtered["Supply"]))

with col3:
    st.metric("Risk Level", filtered["Risk"].values[0])

# ----------------------------
# Risk Alert Message
# ----------------------------
risk = filtered["Risk"].values[0]

if risk == "High":
    st.error("🚨 High risk of stock-out detected. Immediate intervention required.")
elif risk == "Medium":
    st.warning("⚠️ Medium risk. Supply levels should be monitored closely.")
else:
    st.success("✅ Low risk. Supply is currently sufficient.")

# ----------------------------
# Visualization
# ----------------------------
st.subheader("📈 Demand vs Supply Comparison")

fig, ax = plt.subplots()
ax.bar(
    ["Demand", "Supply"],
    [filtered["Demand"].values[0], filtered["Supply"].values[0]]
)
ax.set_ylabel("Quantity")
ax.set_title("Demand vs Supply")
st.pyplot(fig)

# ----------------------------
# AI Explanation (WHY Section)
# ----------------------------
def explain_risk(demand, supply):
    gap = demand - supply

    if gap > 40:
        return (
            "Supply is significantly lower than demand, indicating a severe shortage risk. "
            "Immediate redistribution or replenishment is recommended."
        )
    elif gap > 20:
        return (
            "Supply is moderately below demand, suggesting potential distribution or logistics issues."
        )
    elif gap > 0:
        return (
            "Supply is slightly below demand. Minor fluctuations may lead to short-term shortages."
        )
    else:
        return (
            "Supply meets or exceeds demand. No immediate shortage risk detected."
        )

st.subheader("🧠 Why this risk? (AI Explanation)")

demand_val = filtered["Demand"].values[0]
supply_val = filtered["Supply"].values[0]

st.info(explain_risk(demand_val, supply_val))

# ----------------------------
# Snowflake Architecture Note
# ----------------------------
st.markdown("---")
st.markdown(
    """
    **Snowflake Architecture Note:**  
    In a production deployment, this application would run natively inside Snowflake using Streamlit.  
    Inventory data would reside in Snowflake tables, while AI-driven risk detection and explanations
    would be powered by Snowflake Intelligence (Cortex / AI SQL).
    """
)
