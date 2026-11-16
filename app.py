"""
Interactive Link Budget Calculator - Streamlit Web Application

This script provides a web-based interactive calculator for determining the maximum
communication distance in wireless link budget analysis. It computes path loss and
distance based on RF parameters including transmit power, antenna gains, cable losses,
receiver sensitivity, and propagation models.

Key Features:
- Real-time calculation of maximum communication distance
- Support for two path loss models:
  * Classic Model (1 km reference) - for outdoor/long-range links
  * Log-distance Model (1m reference) - for indoor/short-range analysis
- Interactive visualization showing impact of path loss exponent on range
- Multiple unit conversions (kilometers, meters, miles, feet)
- Adjustable path loss exponent (n) for different environments; n = 2 is free space (FSPL)

How to Run:
    streamlit run app.py

Usage:
1. Adjust parameters in the left sidebar:
   - Transmit power, antenna gains, cable losses
   - Operating frequency
   - Receiver sensitivity
   - Fade margin and miscellaneous losses
   - Path loss exponent (2.0 for free space, lower for indoor line-of-sight,
     higher for obstructed environments)
2. Select the appropriate path loss model
3. View calculated maximum distances in multiple units
4. Observe the interactive plot showing distance vs. path loss exponent relationship

Requirements:
- streamlit
- numpy
- matplotlib
"""

import streamlit as st
import math
import numpy as np
import matplotlib.pyplot as plt

# Minimum positive value for log scale compatibility
MIN_POSITIVE_VALUE = 1e-10

# Path loss exponent range offered by the UI and swept by the plot.
# 1.5 reaches the indoor line-of-sight (waveguiding) regime, n = 2 is free space.
N_MIN = 1.5
N_MAX = 10.0

# Free-space loss unit constants, exact to 4 dp: 20*log10(4*pi*d*f/c) for d in km / m and f in MHz.
# They must differ by exactly 60 dB so both reference distances agree at n = 2.
FSPL_CONST_KM = 32.4478
FSPL_CONST_M = -27.5522

def calculate_max_path_loss(p_tx, g_tx, l_tx, g_rx, l_rx, l_fade, l_misc, p_rx_sensitivity):
    """Calculates the maximum allowable path loss in the link budget."""
    return p_tx + g_tx + g_rx - l_tx - l_rx - l_fade - l_misc - p_rx_sensitivity

def calculate_distance_from_pl(max_path_loss, freq_mhz, n, model_choice):
    """Calculates distance based on path loss, frequency, exponent, and model choice.

    Uses the log-distance model PL(d) = FSPL(d0) + 10*n*log10(d/d0), where FSPL(d0)
    is free-space loss at the reference distance. The exponent scales only the
    distance ratio beyond d0, never the frequency term.
    """
    if max_path_loss < 0:
        return None, None

    try:
        if model_choice == "1m":
            # d0 = 1 m: PL(d) = (20log10(f) + FSPL_CONST_M) + 10n*log10(d_m)
            log_term = (max_path_loss - 20 * math.log10(freq_mhz) - FSPL_CONST_M) / (10 * n)
            distance_m = 10 ** log_term
            distance_km = distance_m / 1000
        else: # "1km"
            # d0 = 1 km: PL(d) = (20log10(f) + FSPL_CONST_KM) + 10n*log10(d_km)
            log_term = (max_path_loss - 20 * math.log10(freq_mhz) - FSPL_CONST_KM) / (10 * n)
            distance_km = 10 ** log_term

        return distance_km
    except (ValueError, ZeroDivisionError):
        return None

def create_plot(max_path_loss, freq_mhz, current_n, current_dist_ft, model_choice, x_scale='linear', y_scale='linear'):
    """Creates and returns a matplotlib figure of distance vs. FSPL exponent."""
    fig, ax = plt.subplots(figsize=(6, 4))

    n_values = np.linspace(N_MIN, N_MAX, 100)
    distances_ft = []

    for n_val in n_values:
        dist_km = calculate_distance_from_pl(max_path_loss, freq_mhz, n_val, model_choice)
        if dist_km is not None and dist_km > 0:
            distances_ft.append(dist_km * 1000 * 3.28084)
        else:
            # Use MIN_POSITIVE_VALUE for log scale compatibility
            distances_ft.append(MIN_POSITIVE_VALUE)

    ax.plot(n_values, distances_ft, label="Max Distance vs. Path Loss Exponent")
    if current_dist_ft is not None:
        ax.plot(current_n, current_dist_ft, 'ro', label=f'Current: {current_dist_ft:,.0f} ft')

    ax.set_xlabel("Path Loss Exponent (n)")
    ax.set_ylabel("Maximum Distance (ft)")
    ax.set_title("Impact of Path Loss Exponent on Range")
    
    # Apply scale settings
    ax.set_xscale(x_scale)
    ax.set_yscale(y_scale)
    
    ax.grid(True, which='both', linestyle='--')
    ax.legend()
    fig.tight_layout()
    return fig

# --- Streamlit App Layout ---

st.set_page_config(layout="centered")
st.title("Interactive Link Budget Calculator")

# Documentation button - opens in new tab using HTML link styled as button
doc_url = "https://victorious-glacier-05b5d831e.2.azurestaticapps.net"

# Create styled link that opens in new tab
st.markdown(
    f'''
    <a href="{doc_url}" target="_blank" rel="noopener noreferrer" 
       aria-label="Open documentation in new tab"
       style="
           display: inline-block;
           background-color: #0068c9;
           color: white;
           padding: 0.5rem 1rem;
           border-radius: 0.25rem;
           text-decoration: none;
           font-size: 1rem;
           cursor: pointer;
       ">
        📚 Documentation
    </a>
    ''',
    unsafe_allow_html=True
)

# --- Sidebar for Inputs ---
st.sidebar.header("Parameters")

p_tx = st.sidebar.number_input("Transmit Power (dBm)", value=20.0, step=0.2, format="%.1f")
g_tx = st.sidebar.number_input("Transmit Antenna Gain (dBi)", value=0.0, step=0.2, format="%.1f")
l_tx = st.sidebar.number_input("Transmit Cable Loss (dB)", value=0.0, step=0.2, format="%.1f")
freq_mhz = st.sidebar.number_input("Frequency (MHz)", value=2400.0, step=10.0, format="%.1f")
g_rx = st.sidebar.number_input("Receiver Antenna Gain (dBi)", value=0.0, step=0.2, format="%.1f")
l_rx = st.sidebar.number_input("Receiver Cable Loss (dB)", value=0.0, step=0.2, format="%.1f")
l_fade = st.sidebar.number_input("Fade Margin (dB)", value=0.0, step=0.2, format="%.1f")
l_misc = st.sidebar.number_input("Misc. Losses (dB)", value=0.0, step=0.2, format="%.1f")
p_rx_sensitivity = st.sidebar.number_input("Receiver Sensitivity (dBm)", value=-95.0, step=0.2, format="%.1f")

n = st.sidebar.slider("Path Loss Exponent (n)", min_value=N_MIN, max_value=N_MAX, value=2.0, step=0.1)

st.sidebar.subheader("Path Loss Model")
model_choice_label = st.sidebar.radio(
    "Select Model:",
    ("Classic Model (1 km reference)", "Log-distance Model (1m reference)"),
    index=1
)
model_choice = "1m" if "1m reference" in model_choice_label else "1km"

# --- Main Page for Outputs ---

# Perform Calculations
if freq_mhz <= 0:
    st.error("Frequency must be a positive number.")
    st.stop()

max_pl = calculate_max_path_loss(p_tx, g_tx, l_tx, g_rx, l_rx, l_fade, l_misc, p_rx_sensitivity)
dist_km = calculate_distance_from_pl(max_pl, freq_mhz, n, model_choice)

st.header("Maximum Communication Distance")

if dist_km is not None:
    # Unit Conversions
    dist_m = dist_km * 1000
    dist_mi = dist_km * 0.621371
    dist_ft = dist_m * 3.28084

    # Display results in columns
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Kilometers", f"{dist_km:.2f}")
    col2.metric("Meters", f"{dist_m:,.2f}")
    col3.metric("Miles", f"{dist_mi:.2f}")
    col4.metric("Feet", f"{dist_ft:,.2f}")

    # Plot axis scale toggles
    st.subheader("Plot Settings")
    toggle_col1, toggle_col2 = st.columns(2)
    with toggle_col1:
        x_scale = st.radio("X-axis Scale", ("Linear", "Logarithmic"), index=0, key="x_scale")
    with toggle_col2:
        y_scale = st.radio("Y-axis Scale", ("Linear", "Logarithmic"), index=0, key="y_scale")
    
    # Convert to matplotlib scale values
    x_scale_value = 'log' if x_scale == "Logarithmic" else 'linear'
    y_scale_value = 'log' if y_scale == "Logarithmic" else 'linear'

    # Create and display the plot
    st.pyplot(create_plot(max_pl, freq_mhz, n, dist_ft, model_choice, x_scale_value, y_scale_value))

else:
    st.warning("Link cannot be established with the current parameters (Path Loss < 0).")


st.markdown("---")
st.info("""
**How to Use:**
- Adjust the parameters in the sidebar on the left.
- The results and plot will update automatically.
- **Path Loss Exponent (n):** Represents how quickly the signal fades with distance. `2.0` is free space (true FSPL); `1.6-1.8` indoor line-of-sight (corridor waveguiding); `2.7-3.5` urban cellular; `3-5` shadowed urban; `4-6` indoor obstructed.
- **Path Loss Model:** Choose the reference distance `d0` for the log-distance model `PL(d) = FSPL(d0) + 10*n*log10(d/d0)`. The 1km reference is common for outdoor/long-range links, while the 1m reference is often used for indoor/short-range analysis. Both agree exactly at n = 2.
- **Fade Margin** stays separate from `n`: the exponent sets the mean loss trend with distance, while the fade margin covers variation around that mean (log-normal shadowing, typically 4-12 dB, and multipath fading).
""")