import streamlit as st
import pandas as pd

import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.parser import parse_log_file
from core.analytics import (
    calculate_total_requests,
    get_top_ips,
    get_status_code_distribution,
    get_top_endpoints,
    get_requests_per_minute
)


st.set_page_config(page_title="Log Analyzer Dashboard", layout="wide")

st.title("🔍 Log Analyzer Dashboard (v2.0)")
st.markdown("---")


# Upload log file
uploaded_file = st.file_uploader("Upload Log File", type=["log"])

if uploaded_file is not None:

    # Save uploaded file temporarily
    with open("temp.log", "wb") as f:
        f.write(uploaded_file.getbuffer())

    logs = parse_log_file("temp.log")

    st.success("Log file parsed successfully!")

    # ---------- METRICS ----------
    total_requests = calculate_total_requests(logs)
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Requests", total_requests)
    col2.metric("Unique IPs", len(set(log["ip"] for log in logs)))
    col3.metric("Unique Endpoints", len(set(log["endpoint"] for log in logs)))

    st.markdown("---")

    # ---------- TOP IPs ----------
    st.subheader("Top IP Addresses")
    top_ips = get_top_ips(logs)
    df_ips = pd.DataFrame(top_ips, columns=["IP Address", "Requests"])
    st.bar_chart(df_ips.set_index("IP Address"))

    # ---------- STATUS CODES ----------
    st.subheader("Status Code Distribution")
    status_dist = get_status_code_distribution(logs)
    df_status = pd.DataFrame(
        list(status_dist.items()),
        columns=["Status Code", "Count"]
    )
    st.bar_chart(df_status.set_index("Status Code"))

    # ---------- REQUESTS PER MINUTE ----------
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