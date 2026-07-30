import streamlit as st
import math

# -----------------------------
# HERO HEADER
# -----------------------------
st.markdown("""
<div style="padding: 25px; background-color:#1f2937; border-radius:12px; margin-bottom:20px;">
    <h1 style="color:white; text-align:center; margin-bottom:5px;">NPC Staffing Calculator v2</h1>
    <p style="color:#d1d5db; text-align:center; font-size:16px;">
        Dual‑Mode • Pallet‑Based & Unit‑Based • Nights / Days / Combined
    </p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# SIDEBAR SETTINGS
# -----------------------------
st.sidebar.header("Settings")

# Shift toggle (NEW)
shift_mode = st.sidebar.radio(
    "Shift Dataset",
    ["Nights", "Days (Beta)", "Combined"],
    help="Uses validated rates from Week 6 observations."
)

# Buffer target slider (NEW)
buffer_target_pct = st.sidebar.slider(
    "Buffer Clearance Target (%)",
    min_value=0,
    max_value=100,
    value=75,
    step=5,
    help="Choose how much of the buffer you want to clear this shift."
)
BUFFER_TARGET = buffer_target_pct / 100

# Barrier / Jam factor (NEW)
disruption_factor = st.sidebar.slider(
    "Barrier / Jam Factor (Operational Reliability)",
    min_value=0.50,
    max_value=1.00,
    value=1.00,
    step=0.05,
    help="Use ~0.70 when tote takeaway or jams slow the line."
)

st.sidebar.markdown("---")
st.sidebar.write("**Shift Hours:** 9 productive hours")

# -----------------------------
# SHIFT RATE SELECTION (NEW)
# -----------------------------
if shift_mode == "Nights":
    PALLET_RATE = 0.49
    UNITS_PER_PALLET = 188
    BLENDED_UPH = 93.8

elif shift_mode == "Days (Beta)":
    PALLET_RATE = 0.65
    UNITS_PER_PALLET = 161
    BLENDED_UPH = 87.4  # from Days dataset

else:  # Combined
    PALLET_RATE = 0.53
    UNITS_PER_PALLET = 176
    BLENDED_UPH = 90.0

SHIFT_HOURS = 9

# -----------------------------
# MODE SELECTOR
# -----------------------------
mode = st.radio(
    "Choose Calculator Mode",
    ["📦 Pallet-Based (Floor / PA)", "📊 Unit-Based (Ops / Area Manager)"],
    horizontal=True
)

st.markdown("---")

# ============================================================
# PALLET MODE
# ============================================================
if mode == "📦 Pallet-Based (Floor / PA)":

    st.markdown("""
    <div style="padding: 20px; border-radius:12px; background-color:#f3f4f6; border:1px solid #e5e7eb;">
        <h2 style="color:#1f2937;">Pallet-Based NPC Calculator</h2>
        <p style="color:#4b5563;">For PAs and floor-level associates</p>
    </div>
    """, unsafe_allow_html=True)

    buffer_pallets = st.number_input("Buffer Depth (pallets)", min_value=0.0, step=1.0)
    inflow_pallets_hr = st.number_input("Inflow Rate (pallets/hour)", min_value=0.0, step=0.1)

    pct_light = st.number_input("Percent Light Pallets (%)", min_value=0.0, max_value=100.0, value=30.0)
    pct_heavy = 100 - pct_light

    st.caption(f"Blended Rate (auto): {PALLET_RATE:.2f} pal/hr • Units/Pallet: {UNITS_PER_PALLET}")

    if st.button("Calculate HC (Pallet Mode)"):

        blended_rate = PALLET_RATE
        effective_rate = blended_rate * disruption_factor

        buffer_workload = buffer_pallets * BUFFER_TARGET
        inflow_workload = inflow_pallets_hr * SHIFT_HOURS
        total_workload = buffer_workload + inflow_workload

        per_associate_output = effective_rate * SHIFT_HOURS

        if per_associate_output <= 0:
            st.error("Effective rate is zero. Check inputs.")
        else:
            hc_raw = total_workload / per_associate_output
            hc_recommended = math.ceil(hc_raw)

            st.markdown(f"""
            <div style="background-color:#d1fae5; padding:15px; border-radius:10px; margin-top:20px;">
                <h2 style="color:#065f46; text-align:center;">Recommended HC: {hc_recommended}</h2>
            </div>
            """, unsafe_allow_html=True)

            with st.expander("Show Calculation Details"):
                st.write(f"Total Workload: {total_workload:.2f} pallets")
                st.write(f"Buffer Contribution ({buffer_target_pct}%): {buffer_workload:.2f} pallets")
                st.write(f"Inflow Contribution (9 hrs): {inflow_workload:.2f} pallets")
                st.write(f"Blended Rate: {blended_rate:.3f} pallets/hr")
                st.write(f"Effective Rate (after barrier): {effective_rate:.3f} pallets/hr")
                st.write(f"Per-Associate Output: {per_associate_output:.2f} pallets/shift")
                st.write(f"Raw HC: {hc_raw:.2f} associates")

# ============================================================
# UNIT MODE
# ============================================================
else:

    st.markdown("""
    <div style="padding: 20px; border-radius:12px; background-color:#f3f4f6; border:1px solid #e5e7eb;">
        <h2 style="color:#1f2937;">Unit-Based NPC Calculator</h2>
        <p style="color:#4b5563;">For Ops Managers and Area Managers</p>
    </div>
    """, unsafe_allow_html=True)

    buffer_units = st.number_input("Buffer Depth (units)", min_value=0.0, step=10.0)
    inflow_units_hr = st.number_input("Inflow Rate (units/hour)", min_value=0.0, step=10.0)

    uph = st.number_input("UPH (units/hour per associate)", min_value=0.0, value=BLENDED_UPH)

    if st.button("Calculate HC (Unit Mode)"):

        effective_uph = uph * disruption_factor

        buffer_workload_units = buffer_units * BUFFER_TARGET
        inflow_workload_units = inflow_units_hr * SHIFT_HOURS
        total_workload_units = buffer_workload_units + inflow_workload_units

        per_associate_output_units = effective_uph * SHIFT_HOURS

        if per_associate_output_units <= 0:
            st.error("Effective UPH is zero. Check inputs.")
        else:
            hc_raw = total_workload_units / per_associate_output_units
            hc_recommended = math.ceil(hc_raw)

            st.markdown(f"""
            <div style="background-color:#dbeafe; padding:15px; border-radius:10px; margin-top:20px;">
                <h2 style="color:#1e3a8a; text-align:center;">Recommended HC: {hc_recommended}</h2>
            </div>
            """, unsafe_allow_html=True)

            with st.expander("Show Calculation Details"):
                st.write(f"Total Workload: {total_workload_units:.2f} units")
                st.write(f"Buffer Contribution ({buffer_target_pct}%): {buffer_workload_units:.2f} units")
                st.write(f"Inflow Contribution (9 hrs): {inflow_workload_units:.2f} units")
                st.write(f"UPH: {uph:.2f} units/hr")
                st.write(f"Effective UPH: {effective_uph:.2f} units/hr")
                st.write(f"Per-Associate Output: {per_associate_output_units:.2f} units/shift")
                st.write(f"Raw HC: {hc_raw:.2f} associates")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("""
<hr>
<p style="text-align:center; color:#6b7280;">
NPC Staffing Calculator • v2.0<br>
Created by Forestall Sabino
</p>
""", unsafe_allow_html=True)
