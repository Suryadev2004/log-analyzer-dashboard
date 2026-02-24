import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd

from core.parser import parse_log_file
from core.analytics import (
    calculate_total_requests,
    get_top_ips,
    get_status_code_distribution,
    get_top_endpoints,
    get_requests_per_minute
)

from detectors.brute_force import detect_brute_force
from detectors.spike_detector import detect_404_spike
from detectors.rate_detector import detect_high_request_rate


st.set_page_config(page_title="Log Analyzer Dashboard", layout="wide")

st.title("🔍 Log Analyzer Dashboard (v3.0)")
st.markdown("---")


uploaded_file = st.file_uploader("Upload Log File", type=["log"])

if uploaded_file is not None:

    with open("temp.log", "wb") as f:
        f.write(uploaded_file.getbuffer())

    logs = parse_log_file("temp.log")

    # ======================
    # 🚨 SECURITY ALERTS
    # ======================

    brute_force_alerts = detect_brute_force(logs)
    recon_alerts = detect_404_spike(logs)
    rate_alerts = detect_high_request_rate(logs)

    all_alerts = brute_force_alerts + recon_alerts + rate_alerts

    st.subheader("🚨 Security Alerts")

    if all_alerts:
        st.error(f"{len(all_alerts)} Security Threat(s) Detected")

        for alert in all_alerts:
            if alert["type"] == "Brute Force Attempt":
                st.warning(
                    f"🔐 Brute Force from {alert['ip']} "
                    f"({alert['failed_attempts']} failed attempts)"
                )

            elif alert["type"] == "Possible Reconnaissance (404 Spike)":
                st.warning(
                    f"🕵️ Recon Activity from {alert['ip']} "
                    f"({alert['404_count']} 404 errors)"
                )

            elif alert["type"] == "High Request Rate":
                st.warning(
                    f"⚡ High Traffic from {alert['ip']} "
                    f"at {alert['minute']} "
                    f"({alert['request_count']} requests in one minute)"
                )
    else:
        st.success("No security threats detected.")

    st.markdown("---")

    # ======================
    # 📊 METRICS
    # ======================

    total_requests = calculate_total_requests(logs)

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Requests", total_requests)
    col2.metric("Unique IPs", len(set(log["ip"] for log in logs)))
    col3.metric("Unique Endpoints", len(set(log["endpoint"] for log in logs)))

    st.markdown("---")

    # ======================
    # 📊 TOP IPs
    # ======================

    st.subheader("Top IP Addresses")
    top_ips = get_top_ips(logs)
    df_ips = pd.DataFrame(top_ips, columns=["IP Address", "Requests"])
    st.bar_chart(df_ips.set_index("IP Address"))

    # ======================
    # 📊 STATUS CODES
    # ======================

    st.subheader("Status Code Distribution")
    status_dist = get_status_code_distribution(logs)
    df_status = pd.DataFrame(
        list(status_dist.items()),
        columns=["Status Code", "Count"]
    )
    st.bar_chart(df_status.set_index("Status Code"))

    # ======================
    # 📈 REQUESTS PER MINUTE
    # ======================

    st.subheader("Requests Per Minute")
    rpm = get_requests_per_minute(logs)
    df_rpm = pd.DataFrame(
        list(rpm.items()),
        columns=["Minute", "Requests"]
    )
    df_rpm.set_index("Minute", inplace=True)
    st.line_chart(df_rpm)

else:
    st.info("Please upload a log file to begin analysis.")