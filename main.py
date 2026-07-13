import streamlit as str
import google.generativeai as genai
import time
import random
import pandas as pd

# 1. AI Core Configuration
if "GOOGLE_API_KEY" in str.secrets:
    genai.configure(api_key=str.secrets["GOOGLE_API_KEY"])
else:
    str.warning("System Warning: GOOGLE_API_KEY missing in Streamlit Secrets.")

SYSTEM_INSTRUCTION = """
You are Galo Mestre, the industrial AI core of an automated poultry farm.
Your role is to evaluate real-time sensor streams and automated door/feeder operations, providing highly technical, safe, and actionable optimizations for tropical aviculture environments.
"""

str.set_page_config(page_title="Galo Mestre Pro", layout="wide", initial_sidebar_state="expanded")
str.title("🐓 Galo Mestre - Telemetry & Automation Hub")

# 2. Session State Initialization for Real-Time Simulation
if "sensor_history" not in str.session_state:
    str.session_state.sensor_history = pd.DataFrame(columns=["Timestamp", "Temperature", "Humidity"])
if "coop_door_locked" not in str.session_state:
    str.session_state.coop_door_locked = True
if "feeder_override" not in str.session_state:
    str.session_state.feeder_override = False

# 3. Sidebar: Hardware Controls (Automatic Lock & Feeders)
str.sidebar.header("🛡️ Hardware Actuators")

# Interactive Automatic Lock Control
str.sidebar.subheader("Automatic Door System")
if str.sidebar.button("🔓 Emergency Unlock Door" if str.session_state.coop_door_locked else "🔒 Force Lock Door"):
    str.session_state.coop_door_locked = not str.session_state.coop_door_locked
    str.sidebar.toast("Door state updated instantly!")

door_status_label = "🔴 LOCKED (Secure Mode)" if str.session_state.coop_door_locked else "🟢 UNLOCKED (Open Access)"
str.sidebar.info(f"Current Lock Status: {door_status_label}")

str.sidebar.markdown("---")

# Feeder Switch
str.session_state.feeder_override = str.sidebar.toggle("Enable Continuous Feeding Layout", value=str.session_state.feeder_override)

# 4. Main Dashboard - Real-Time Sensor Stream Simulation
str.subheader("📊 Live Telemetry Matrix")

# Generate live telemetry simulation
current_temp = round(random.uniform(24.0, 32.5), 1)
current_humidity = round(random.uniform(55.0, 75.0), 1)
water_tank = random.randint(30, 95)
silo_feed = random.randint(20, 88)

# Append to history dataframe for charts
new_data = pd.DataFrame([{"Timestamp": time.strftime("%H:%M:%S"), "Temperature": current_temp, "Humidity": current_humidity}])
str.session_state.sensor_history = pd.concat([str.session_state.sensor_history, new_data], ignore_index=True).tail(10)

# Metrics Grid
m_col1, m_col2, m_col3, m_col4 = str.columns(4)
with m_col1:
    str.metric("Ambient Temp", f"{current_temp} °C", delta="Critical High" if current_temp > 31.0 else "Optimal")
with m_col2:
    str.metric("Relative Humidity", f"{current_humidity} %")
with m_col3:
    str.metric("Water Tank Level", f"{water_tank} %", delta="-2% (Hourly Flow)")
with m_col4:
    str.metric("Automatic Silo Stock", f"{silo_feed} %")

# 5. Interactive Data Charts
str.markdown("---")
str.subheader("📈 Environmental Trend Analysis (Last 10 Cycles)")
c_col1, c_col2 = str.columns(2)
with c_col1:
    str.line_chart(str.session_state.sensor_history.set_index("Timestamp")["Temperature"])
with c_col2:
    str.line_chart(str.session_state.sensor_history.set_index("Timestamp")["Humidity"])

# 6. Industrial AI Diagnosis
str.markdown("---")
str.subheader("🧠 Galo Mestre - Real-Time AI System Diagnostics")

if str.button("🚀 Execute Full Systems Audit with Gemini"):
    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=SYSTEM_INSTRUCTION
        )
        
        telemetry_payload = f"""
        INCOMING TELEMETRY STRING:
        - Sensor Temp: {current_temp} C
        - Sensor Humidity: {current_humidity}%
        - Actuator Door Lock Status: {str.session_state.coop_door_locked}
        - Actuator Feeder Status: {str.session_state.feeder_override}
        - Resource Water Level: {water_tank}%
        - Resource Feed Level: {silo_feed}%
        
        Task: Analyze hardware locks, environmental stability, and inventory. Output a high-priority action plan.
        """
        
        with str.spinner("Analyzing active data packets..."):
            response = model.generate_content(telemetry_payload)
            str.success("Telemetry Evaluated Successfully.")
            str.markdown(response.text)
    except Exception as e:
        str.error(f"AI Stream Interrupted: Check your GOOGLE_API_KEY inside Streamlit Secrets. Error detail: {e}")

# Live Loop trigger for interactive feeling
time.sleep(2)
str.rerun()
