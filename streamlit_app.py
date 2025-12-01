import streamlit as st
import pandas as pd
import json
import os
from agent_logic import agent_1, agent_2, agent_3, orchestrator


st.set_page_config(page_title="LeadFlow AI", layout="wide")

st.title(" LeadFlow AI — Multi-Agent Lead Scoring System")
st.write("Upload your company info + CSV → Agents will validate + score each lead.")


# ---------------------------------------
# SECTION 1 — COMPANY INFO
# ---------------------------------------
st.header(" Step 1 — Enter Company Information")

company_text = st.text_area(
    "Describe your company, industry, audience, and conversion goal:",
    placeholder="Example: We are an EdTech SaaS selling to US universities..."
)

if st.button("Run Agent 1 (Understand Company)"):
    if not company_text.strip():
        st.error("Please enter company info first.")
    else:
        with st.spinner("Running Agent 1..."):
            result = agent_1.run(company_text)

        st.success("Agent 1 Completed!")
        st.json(result)
        st.session_state.agent1_data = result



# ---------------------------------------
# SECTION 2 — FILE UPLOAD + VALIDATION
# ---------------------------------------
st.header("Step 2 — Upload CSV & Validate Dataset")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if st.button("Run Agent 2 (Validate Columns)"):
    if "agent1_data" not in st.session_state:
        st.error("Please run Agent 1 first.")
    elif uploaded_file is None:
        st.error("Upload a CSV first!")
    else:
        df = pd.read_csv(uploaded_file)
        st.write("Preview of uploaded dataset:")
        st.dataframe(df.head())

        with st.spinner("Running Agent 2..."):
            result = agent_2.run({
                "agent1": st.session_state.agent1_data,
                "uploaded_columns": df.columns.tolist()
            })

        st.success("Agent 2 Completed!")
        st.json(result)

        st.session_state.agent2_data = result
        st.session_state.leads_df = df



# ---------------------------------------
# SECTION 3 — LEAD SCORING
# ---------------------------------------
st.header(" Step 3 — Run Lead Scoring")

if st.button("Run Agent 3 (Score Leads)"):
    if "agent2_data" not in st.session_state:
        st.error("Please run Agent 2 first!")
    else:
        with st.spinner("Scoring leads..."):
            result = agent_3.run({
                "agent1": st.session_state.agent1_data,
                "agent2": st.session_state.agent2_data,
                "data_summary": st.session_state.leads_df.head().to_dict()
            })

        st.success("Agent 3 Completed!")
        st.subheader(" Scored Leads")
        st.json(result)

        # convert JSON list to DataFrame
        if "scored_leads" in result:
            scored_df = pd.DataFrame(result["scored_leads"])
            st.dataframe(scored_df)

            # Downloadable CSV
            csv = scored_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download Scored Leads CSV",
                csv,
                "scored_leads.csv",
                "text/csv"
            )
