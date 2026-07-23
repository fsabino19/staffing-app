import streamlit as st
import math

st.title("NPC Staffing Calculator (Dual-Mode: Pallets & Units)")

mode = st.radio(
    "Select calculation mode",
    ["Pallet-based (floor / PA)", "Unit-based (Ops / Area Manager)"]
)

SHIFT_HOURS = 9
BUFFER_TARGET = 0.75
LIGHT_RATE = 0.74  # pallets/hr
HEAVY_RATE = 0.43  # pallets/hr

st.markdown("---")

if mode == "Pallet-based (floor / PA)":
    st.header("Pallet-Based NPC HC (Floor-Level)")

    buffer_pallets = st.number_input("Buffer Depth (pallets)", min_value=0.0, step=1.0)
    inflow_pallets_hr = st.number_input("Inflow Rate (pallets/hour)", min_value=0.0, step=0.1)

    pct_light = st.number_input("Percent Light Pallets (%)", min_value=0.0, max_value=100.0, value=40.0, step=1.0)
    pct_heavy = st.number_input("Percent Heavy Pallets (%)", min_value=0.0, max_value=100.0, value=60.0, step=1.0)

    st.caption("Light Rate = 0.74 pal/hr (spices, clothes, skin care, organizers)")
    st.caption("Heavy Rate = 0.43 pal/hr (water, oil, rice, cans, clamato)")

    disruption_factor = st.slider(
        "Disruption Factor (line jams, downstacking, etc.)",
        min_value=0.5,
        max_value=1.0,
        value=1.0,
        step=0.05,
        help="Use ~0.70 when tote takeaway keeps failing (30% jam penalty)."
    )

    if st.button("Calculate HC (Pallet Mode)"):
        # Blended rate
        light_share = pct_light / 100.0
        heavy_share = pct_heavy / 100.0

        blended_rate = (light_share * LIGHT_RATE) + (heavy_share * HEAVY_RATE)
        effective_rate = blended_rate * disruption_factor

        # Numerator: total pallets to process this shift
        buffer_workload = buffer_pallets * BUFFER_TARGET
        inflow_workload = inflow_pallets_hr * SHIFT_HOURS
        total_workload = buffer_workload + inflow_workload

        # Denominator: pallets per associate per shift
        per_associate_output = effective_rate * SHIFT_HOURS

        if per_associate_output <= 0:
            st.error("Effective rate is zero or negative. Check inputs.")
        else:
            hc_raw = total_workload / per_associate_output
            hc_recommended = math.ceil(hc_raw)

            st.metric("Recommended HC (Pallet Mode)", hc_recommended)
            st.write(f"Total Workload: {total_workload:.2f} pallets")
            st.write(f"Buffer Contribution (75%): {buffer_workload:.2f} pallets")
            st.write(f"Inflow Contribution (9 hrs): {inflow_workload:.2f} pallets")
            st.write(f"Blended Rate: {blended_rate:.3f} pallets/hr")
            st.write(f"Effective Rate (after disruption): {effective_rate:.3f} pallets/hr")
            st.write(f"Per-Associate Output: {per_associate_output:.2f} pallets/shift")
            st.write(f"Raw HC: {hc_raw:.2f} associates")

else:
    st.header("Unit-Based NPC HC (System / UPH)")

    buffer_units = st.number_input("Buffer Depth (units)", min_value=0.0, step=10.0)
    inflow_units_hr = st.number_input("Inflow Rate (units/hour)", min_value=0.0, step=10.0)
    uph = st.number_input("UPH (units/hour per associate)", min_value=0.0, step=1.0)

    disruption_factor = st.slider(
        "Disruption Factor (line jams, downstacking, etc.)",
        min_value=0.5,
        max_value=1.0,
        value=1.0,
        step=0.05,
        help="Use ~0.70 when operational reliability is low."
    )

    if st.button("Calculate HC (Unit Mode)"):
        effective_uph = uph * disruption_factor

        buffer_workload_units = buffer_units * BUFFER_TARGET
        inflow_workload_units = inflow_units_hr * SHIFT_HOURS
        total_workload_units = buffer_workload_units + inflow_workload_units

        per_associate_output_units = effective_uph * SHIFT_HOURS

        if per_associate_output_units <= 0:
            st.error("Effective UPH is zero or negative. Check inputs.")
        else:
            hc_raw = total_workload_units / per_associate_output_units
            hc_recommended = math.ceil(hc_raw)

            st.metric("Recommended HC (Unit Mode)", hc_recommended)
            st.write(f"Total Workload: {total_workload_units:.2f} units")
            st.write(f"Buffer Contribution (75%): {buffer_workload_units:.2f} units")
            st.write(f"Inflow Contribution (9 hrs): {inflow_workload_units:.2f} units")
            st.write(f"UPH: {uph:.2f} units/hr")
            st.write(f"Effective UPH (after disruption): {effective_uph:.2f} units/hr")
            st.write(f"Per-Associate Output: {per_associate_output_units:.2f} units/shift")
            st.write(f"Raw HC: {hc_raw:.2f} associates")
