import streamlit as st
import math

st.title("Amazon Building-Level HC Staffing Model (Units-Based)")

# Inputs
units_per_tote = st.number_input("Average Units per Tote", min_value=1.0)
total_buffer_totes = st.number_input("Total Buffer (totes)", min_value=0)
total_inflow_totes = st.number_input("Total Inflow (totes/hour)", min_value=0.0)
processing_rate_totes = st.number_input("Processing Rate per Worker (totes/hour)", min_value=0.0)
shift_length = st.number_input("Shift Length (hours)", min_value=1)

if st.button("Calculate HC"):
    # Convert everything to units
    total_buffer_units = total_buffer_totes * units_per_tote
    total_inflow_units = total_inflow_totes * units_per_tote
    worker_capacity_units = processing_rate_totes * units_per_tote

    # Total workload this shift (units)
    total_workload_units = total_buffer_units + (total_inflow_units * shift_length)

    # Required HC
    hc = total_workload_units / (worker_capacity_units * shift_length)
    recommended_hc = math.ceil(hc)

    # Per-person load (units)
    per_person_load_units = total_workload_units / recommended_hc

    # Clearance capability
    clearance_pct = (worker_capacity_units * recommended_hc * shift_length) / total_workload_units

    # Backlog risk
    if clearance_pct < 1:
        backlog_msg = "⚠️ Backlog will grow"
    elif clearance_pct == 1:
        backlog_msg = "⚠️ No clearance — workers only keep up"
    else:
        backlog_msg = "✅ Buffer will shrink"

    # Outputs
    st.metric("Recommended Headcount", recommended_hc)
    st.write(f"Total Workload: {total_workload_units:.2f} units")
    st.write(f"Per-Person Load: {per_person_load_units:.2f} units")
    st.write(f"Clearance Capability: {clearance_pct:.2f}x")
    st.write(backlog_msg)
