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
# ✅ SAFETY CHECK - Handle empty data
# ----------------------------
if filtered.empty:
    st.error("❌ No data available for the selected filters. Please try different parameters.")
    st.stop()

# ----------------------------
# ✅ FIXED KPI Metrics (Extract single values properly)
# ----------------------------
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

# Extract single values from DataFrame
demand_val = int(filtered["Demand"].values[0])
supply_val = int(filtered["Supply"].values[0])
risk_val = filtered["Risk"].values[0]

with col1:
    st.metric("Demand", demand_val)

with col2:
    st.metric("Supply", supply_val)

with col3:
    # ✅ Add color coding for risk levels
    if risk_val == "High":
        st.metric("Risk Level", risk_val, delta="⚠️ CRITICAL", delta_color="inverse")
    elif risk_val == "Medium":
        st.metric("Risk Level", risk_val, delta="⚡ Monitor", delta_color="off")
    else:
        st.metric("Risk Level", risk_val, delta="✅ Stable", delta_color="normal")

# ----------------------------
# Risk Alert Message with enhanced styling
# ----------------------------
if risk_val == "High":
    st.error("🚨 **HIGH RISK** – Stock-out detected. Immediate intervention required.")
    st.warning("📢 Suggested Action: Increase supply by 20-30% immediately.")
elif risk_val == "Medium":
    st.warning("⚠️ **MEDIUM RISK** – Supply levels should be monitored closely.")
    st.info("📊 Suggested Action: Review supply chain and optimize distribution.")
else:
    st.success("✅ **LOW RISK** – Supply is currently sufficient.")
    st.info("📈 Suggested Action: Maintain current inventory levels.")

# ----------------------------
# ✅ FIXED Visualization (Extract values properly)
# ----------------------------
st.subheader("📈 Demand vs Supply Comparison")

# Create chart data with proper values
chart_data = pd.DataFrame({
    "Quantity": [demand_val, supply_val]
}, index=["Demand", "Supply"])

# Display bar chart
st.bar_chart(chart_data)

# Add additional metrics visualization
col4, col5 = st.columns(2)

with col4:
    gap = demand_val - supply_val
    gap_percentage = (gap / demand_val) * 100 if demand_val > 0 else 0
    
    st.metric(
        "Supply-Demand Gap", 
        f"{gap} units",
        delta=f"{gap_percentage:.1f}% short" if gap > 0 else "Surplus",
        delta_color="inverse" if gap > 0 else "normal"
    )

with col5:
    coverage = (supply_val / demand_val) * 100 if demand_val > 0 else 0
    st.metric(
        "Supply Coverage", 
        f"{coverage:.1f}%",
        delta="Adequate" if coverage >= 100 else "Insufficient",
        delta_color="normal" if coverage >= 100 else "inverse"
    )

# ----------------------------
# Enhanced AI Explanation (WHY Section)
# ----------------------------
def explain_risk(demand, supply, risk_level):
    gap = demand - supply
    
    # Detailed explanation based on multiple factors
    if risk_level == "High":
        if gap > 40:
            return f"""
            🔴 **CRITICAL SHORTAGE DETECTED**
            
            • **Supply Gap:** {gap} units ({(gap/demand*100):.1f}% of demand)
            • **Root Cause:** Supply is significantly lower than demand
            • **Impact:** Immediate stock-out risk in {gap//7:.0f} days at current consumption rate
            • **Recommendation:** Emergency procurement required. Increase supply by 30% immediately.
            """
        else:
            return f"""
            🟠 **SEVERE SUPPLY CONSTRAINT**
            
            • **Supply Gap:** {gap} units ({(gap/demand*100):.1f}% shortfall)
            • **Root Cause:** Supply chain bottleneck or unexpected demand surge
            • **Impact:** Critical items may run out within 2-3 days
            • **Recommendation:** Expedite shipments and activate backup suppliers
            """
    
    elif risk_level == "Medium":
        if gap > 20:
            return f"""
            🟡 **MODERATE SHORTAGE RISK**
            
            • **Supply Gap:** {gap} units ({(gap/demand*100):.1f}% shortfall)
            • **Root Cause:** Supply moderately below demand due to distribution inefficiencies
            • **Impact:** Potential shortages if demand continues at current pace
            • **Recommendation:** Monitor daily and adjust orders for next cycle
            """
        else:
            return f"""
            🟡 **BALANCE CONCERN**
            
            • **Supply Gap:** {gap} units ({(gap/demand*100):.1f}% shortfall)
            • **Root Cause:** Minor supply-demand imbalance
            • **Impact:** Possible stock-out only if demand spikes
            • **Recommendation:** Maintain current levels but increase safety stock by 10%
            """
    
    else:  # Low risk
        if gap <= 0:
            return f"""
            🟢 **HEALTHY INVENTORY LEVELS**
            
            • **Supply Status:** Supply meets or exceeds demand ({(supply/demand*100):.1f}% coverage)
            • **Root Cause:** Well-balanced supply chain with adequate buffer stock
            • **Impact:** No immediate shortage concerns
            • **Recommendation:** Maintain current inventory strategy
            """
        else:
            return f"""
            🟢 **MINOR FLUCTUATION DETECTED**
            
            • **Supply Gap:** {gap} units ({(gap/demand*100):.1f}% shortfall)
            • **Root Cause:** Normal market fluctuations
            • **Impact:** No immediate action needed
            • **Recommendation:** Continue regular monitoring
            """

st.subheader("🧠 Why this risk? (AI Explanation)")

# Display the enhanced explanation
explanation = explain_risk(demand_val, supply_val, risk_val)
st.info(explanation)

# ----------------------------
# Additional Data Table (Optional)
# ----------------------------
with st.expander("📋 View Detailed Data Table"):
    st.dataframe(
        filtered.style.applymap(
            lambda x: 'background-color: #ff6b6b' if x == 'High' 
            else 'background-color: #ffd93d' if x == 'Medium' 
            else 'background-color: #6bcf7f' if x == 'Low' 
            else '',
            subset=['Risk']
        ),
        use_container_width=True
    )

# ----------------------------
# Regional Comparison
# ----------------------------
st.subheader("🌍 Regional Comparison")

# Show comparison across regions for selected item
region_comparison = df[df["Item"] == selected_item].copy()
region_comparison["Gap"] = region_comparison["Demand"] - region_comparison["Supply"]

col6, col7 = st.columns(2)

with col6:
    st.bar_chart(
        region_comparison.set_index("Region")[["Demand", "Supply"]],
        use_container_width=True
    )

with col7:
    # Show risk distribution
    risk_dist = region_comparison["Risk"].value_counts()
    st.write("**Risk Distribution Across Regions**")
    for risk_type, count in risk_dist.items():
        if risk_type == "High":
            st.error(f"{risk_type}: {count} region(s)")
        elif risk_type == "Medium":
            st.warning(f"{risk_type}: {count} region(s)")
        else:
            st.success(f"{risk_type}: {count} region(s)")

# ----------------------------
# Snowflake Architecture Note
# ----------------------------
st.markdown("---")
st.markdown(
    """
    ### ❄️ **Snowflake Architecture Note**
    
    In production, this Streamlit application would run natively inside Snowflake:
    
    - **Data Layer:** Inventory data resides in Snowflake tables with real-time updates
    - **AI Layer:** Risk detection powered by Snowflake Cortex / AI SQL functions
    - **Explanation Layer:** Natural language insights generated using LLM models
    - **Scale:** Handles millions of SKUs across thousands of locations
    
    **Next Steps:** Connect to Snowflake, replace synthetic data with real tables, 
    and deploy as a Snowflake Native App.
    """
)

# ----------------------------
# Footer with timestamp
# ----------------------------
st.caption(f"🔄 Last updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')} | AI for Good Initiative")
