import streamlit as st
import pandas as pd
import numpy as np

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
# ✅ SAFETY CHECK
# ----------------------------
if filtered.empty:
    st.error("❌ No data available for the selected filters.")
    st.stop()

# ----------------------------
# ✅ FIXED KPI Metrics
# ----------------------------
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

demand_val = int(filtered["Demand"].values[0])
supply_val = int(filtered["Supply"].values[0])
risk_val = filtered["Risk"].values[0]

with col1:
    st.metric("Demand", demand_val)

with col2:
    st.metric("Supply", supply_val)

with col3:
    if risk_val == "High":
        st.metric("Risk Level", risk_val, delta="⚠️ CRITICAL")
    elif risk_val == "Medium":
        st.metric("Risk Level", risk_val, delta="⚡ Monitor")
    else:
        st.metric("Risk Level", risk_val, delta="✅ Stable")

# ----------------------------
# Risk Alert Message
# ----------------------------
if risk_val == "High":
    st.error("🚨 High risk of stock-out detected. Immediate intervention required.")
elif risk_val == "Medium":
    st.warning("⚠️ Medium risk. Supply levels should be monitored closely.")
else:
    st.success("✅ Low risk. Supply is currently sufficient.")

# ----------------------------
# ✅ FIXED Visualization
# ----------------------------
st.subheader("📈 Demand vs Supply Comparison")

chart_data = pd.DataFrame({
    "Quantity": [demand_val, supply_val]
}, index=["Demand", "Supply"])

st.bar_chart(chart_data)

# ----------------------------
# AI Explanation
# ----------------------------
def explain_risk(demand, supply):
    gap = demand - supply

    if gap > 40:
        return "Supply is significantly lower than demand, indicating a severe shortage risk."
    elif gap > 20:
        return "Supply is moderately below demand, suggesting potential distribution issues."
    elif gap > 0:
        return "Supply is slightly below demand. Minor fluctuations may cause shortages."
    else:
        return "Supply meets or exceeds demand. No immediate shortage detected."

st.subheader("🧠 Why this risk? (AI Explanation)")

st.info(explain_risk(demand_val, supply_val))

# ----------------------------
# ✅ FIXED Data Table (No styling issues)
# ----------------------------
with st.expander("📋 View Detailed Data Table"):
    # Simple dataframe - guaranteed to work
    st.dataframe(filtered, use_container_width=True)
    
    # Optional: Safe risk breakdown using columns
    st.markdown("**Risk Summary:**")
    risk_counts = filtered["Risk"].value_counts()
    
    r1, r2, r3 = st.columns(3)
    with r1:
        if "High" in risk_counts:
            st.error(f"🔴 High: {risk_counts['High']}")
    with r2:
        if "Medium" in risk_counts:
            st.warning(f"🟠 Medium: {risk_counts['Medium']}")
    with r3:
        if "Low" in risk_counts:
            st.success(f"🟢 Low: {risk_counts['Low']}")

# ----------------------------
# Snowflake Architecture Note
# ----------------------------
st.markdown("---")
st.markdown(
    """
    **Snowflake Architecture Note:**  
    In production, this Streamlit application would run natively inside Snowflake.  
    Inventory data would reside in Snowflake tables, while AI-driven risk detection
    and explanations would be powered by Snowflake Intelligence (Cortex / AI SQL).
    """
)
