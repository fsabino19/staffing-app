import streamlit as st
import math

st.title("Amazon Building-Level HC Staffing Model")

# Inputs
total_buffer = st.number_input("Total Buffer Depth (totes)", min_value=0)
total_inflow = st.number_input("Total Inflow Rate (totes/hour)", min_value=0.0)
processing_rate = st.number_input("Processing Rate per Worker (totes/hour)", min_value=0.0)
shift_length = st.number_input("Shift Length (hours)", min_value=1)

if st.button("Calculate HC"):
    # Total workload this shift
    total_workload = total_buffer + (total_inflow * shift_length)

    # Worker capacity
    worker_capacity = processing_rate * shift_length

    # Required HC
    hc = total_workload / worker_capacity
    recommended_hc = math.ceil(hc)

    # Per-person load
    per_person_load = total_workload / recommended_hc

    # Clearance capability
    clearance_pct = (worker_capacity * recommended_hc) / total_workload

    # Backlog risk
    if clearance_pct < 1:
        backlog_msg = "⚠️ Backlog will grow"
    elif clearance_pct == 1:
        backlog_msg = "⚠️ No clearance — workers only keep up"
    else:
        backlog_msg = "✅ Buffer will shrink"

    # Outputs
    st.metric("Recommended Headcount", recommended_hc)
    st.write(f"Total Workload: {total_workload:.2f} totes")
    st.write(f"Per-Person Load: {per_person_load:.2f} totes")
    st.write(f"Clearance Capability: {clearance_pct:.2f}x")
    st.write(backlog_msg)