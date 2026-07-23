import streamlit as st

st.title("Amazon HC Staffing Model")

buffer_depth = st.number_input("Buffer Depth", min_value=0)
inflow_rate = st.number_input("Inflow Rate", min_value=0.0)
processing_rate = st.number_input("Processing Rate", min_value=0.0, value=0.59)
target_clearance_rate = st.number_input("Target Clearance Rate", min_value=0.0, value=0.75)
shift_length = st.number_input("Shift Length (hours)", min_value=1, value=9)

if st.button("Calculate HC"):
    numerator = (buffer_depth * target_clearance_rate) + (inflow_rate * shift_length)
    denominator = processing_rate * shift_length

    hc = numerator / denominator
    recommended_hc = int(hc) if hc.is_integer() else int(hc) + 1

    st.metric("Recommended Headcount", recommended_hc)
    st.write(f"Raw Output: {hc}")

