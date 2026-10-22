"""AID-FLOW: illustrative community resource allocation decision-support prototype."""
from __future__ import annotations

from datetime import datetime, timezone
from io import StringIO

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="AID-FLOW | Community Decision Intelligence", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

CREATOR = "Mohd Khairul Ridhuan bin Mohd Fadzil"
DEFAULT_REQUESTS = pd.DataFrame([
    {"Request ID": "REQ-001", "Household": "Household A", "Units needed": 3, "Urgency": 3},
    {"Request ID": "REQ-002", "Household": "Household B", "Units needed": 2, "Urgency": 2},
    {"Request ID": "REQ-003", "Household": "Household C", "Units needed": 4, "Urgency": 3},
    {"Request ID": "REQ-004", "Household": "Household D", "Units needed": 2, "Urgency": 1},
    {"Request ID": "REQ-005", "Household": "Household E", "Units needed": 3, "Urgency": 2},
])

st.markdown("""<style>
#MainMenu, footer {visibility:hidden}
.block-container {padding-top:2rem;padding-bottom:3rem;max-width:1480px}
[data-testid="stSidebar"] {border-right:1px solid #2b455b}
.hero {padding:26px 30px;border-radius:16px;background:linear-gradient(115deg,#173a4a 0%,#101e32 70%);border:1px solid #31546a;margin:12px 0 24px}
.eyebrow {font-size:11px;letter-spacing:2px;color:#8acdbc;font-weight:700}
.hero h1 {font-size:clamp(30px,4vw,49px);line-height:1.13;letter-spacing:-1.5px;margin:14px 0;color:#f5fafc}
.hero h1 span {color:#65dcc3}
.hero p {color:#b4c8d8;max-width:780px;font-size:14px}
.credit {color:#a3bfcc;font-size:12px;padding-top:12px}
.card-note {border-left:3px solid #dfbd76;background:#1e2b3a;padding:13px 16px;border-radius:4px;color:#d8e3eb;font-size:13px;margin:14px 0 22px}
.section-kicker {color:#7dd8c3;font-size:12px;letter-spacing:1.3px;font-weight:700;margin:20px 0 8px}
.small-note {font-size:12px;color:#a2b9c9}
</style>""", unsafe_allow_html=True)

if "requests" not in st.session_state:
    st.session_state.requests = DEFAULT_REQUESTS.copy()
if "audit" not in st.session_state:
    st.session_state.audit = []
if "edited" not in st.session_state:
    st.session_state.edited = False
if "stock" not in st.session_state:
    st.session_state.stock = 9
if "budget" not in st.session_state:
    st.session_state.budget = 250
if "unit_cost" not in st.session_state:
    st.session_state.unit_cost = 25


def allocate(requests: pd.DataFrame, stock: int, budget: int, unit_cost: int) -> tuple[pd.DataFrame, dict]:
    """Illustrative priority-first allocation; not an eligibility/fairness algorithm."""
    capacity = min(int(stock), int(budget) // int(unit_cost))
    result = requests.copy()
    if result.empty:
        result["Allocated"] = pd.Series(dtype="int64")
        result["Unmet"] = pd.Series(dtype="int64")
        result["Status"] = pd.Series(dtype="str")
        return result, {"requested": 0, "allocated": 0, "unmet": 0, "spent": 0, "coverage": 0.0}
    result = result.sort_values(["Urgency", "Request ID"], ascending=[False, True]).reset_index(drop=True)
    allocations = []
    for needed in result["Units needed"].astype(int):
        units = min(capacity, needed)
        allocations.append(units)
        capacity -= units
    result["Allocated"] = allocations
    result["Unmet"] = result["Units needed"] - result["Allocated"]
    result["Status"] = result.apply(lambda row: "Covered" if row["Unmet"] == 0 else ("Partial" if row["Allocated"] > 0 else "Unmet"), axis=1)
    requested = int(result["Units needed"].sum())
    allocated = int(result["Allocated"].sum())
    return result, {"requested": requested, "allocated": allocated, "unmet": requested - allocated, "spent": allocated * int(unit_cost), "coverage": allocated / requested * 100 if requested else 0.0}


with st.sidebar:
    st.markdown("### ◈ AID-FLOW")
    st.caption("COMMUNITY DECISION INTELLIGENCE")
    st.divider()
    page = st.radio("Workspace", ["Overview", "Allocation Lab", "Request Register", "Decision Log", "Methodology"], label_visibility="collapsed")
    st.divider()
    st.caption("CREATED & DEVELOPED BY")
    st.markdown(f"**{CREATOR}**")
    st.caption("Malaysia 🇲🇾")
    st.divider()
    st.caption("Prototype • Session-only data • No beneficiary records")

st.markdown(f"""<div class="hero"><div class="eyebrow">AID-FLOW / COMMUNITY OPERATIONS</div>
<h1>Better decisions.<br><span>Stronger communities.</span></h1>
<p>Explore how limited inventory and budgets affect proposed aid allocation. An explainable, human-reviewed simulation for community operations.</p>
<div class="credit">Created &amp; Developed by <b>{CREATOR}</b> · Malaysia</div></div>""", unsafe_allow_html=True)
st.markdown('<div class="card-note"><b>DEMONSTRATION PROTOTYPE:</b> Initial requests are fictional. No live NGO data, beneficiary verification or proven social-impact claims. Never enter names, addresses, medical or other personal information.</div>', unsafe_allow_html=True)

if page == "Allocation Lab":
    st.markdown('<div class="section-kicker">01 / SCENARIO PARAMETERS</div>', unsafe_allow_html=True)
    a, b, c = st.columns(3)
    with a:
        st.number_input("Food packs available", min_value=0, max_value=100000, step=1, key="stock")
    with b:
        st.number_input("Budget (RM)", min_value=0, max_value=10000000, step=25, key="budget")
    with c:
        st.number_input("Cost per pack (RM)", min_value=1, max_value=100000, step=1, key="unit_cost")

allocation, metrics = allocate(st.session_state.requests, st.session_state.stock, st.session_state.budget, st.session_state.unit_cost)

if page in ["Overview", "Allocation Lab"]:
    st.markdown('<div class="section-kicker">02 / ALLOCATION PERFORMANCE</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    for col, label, value in zip(cols, ["Units requested", "Proposed allocation", "Unmet demand", "Coverage"], [str(metrics["requested"]), str(metrics["allocated"]), str(metrics["unmet"]), f'{metrics["coverage"]:.1f}%']):
        col.metric(label, value)
    left, right = st.columns([1.2, 1])
    with left:
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Proposed allocation", x=["Resource coverage"], y=[metrics["allocated"]], marker_color="#32c9b1"))
        fig.add_trace(go.Bar(name="Unmet demand", x=["Resource coverage"], y=[metrics["unmet"]], marker_color="#e7b66b"))
        fig.update_layout(barmode="stack", height=310, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#dceaf1", margin=dict(l=20, r=20, t=25, b=25), legend=dict(orientation="h", y=1.16), yaxis_title="Food packs")
        st.plotly_chart(fig, use_container_width=True)
    with right:
        st.subheader("Scenario summary")
        st.metric("Modelled expenditure", f'RM {metrics["spent"]:,}')
        st.progress(min(metrics["coverage"] / 100, 1.0))
        st.caption(f'{metrics["allocated"]} of {metrics["requested"]} requested units can be covered under current assumptions.')
        st.info("Rule: urgency 3 first, then 2, then 1. Ties are resolved by request ID. This is a demonstration rule, not a validated fairness policy.")
    if page == "Allocation Lab":
        if st.button("Record proposed allocation", type="primary", use_container_width=True):
            st.session_state.audit.append({"Timestamp (UTC)": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"), "Requests": len(allocation), "Requested": metrics["requested"], "Allocated": metrics["allocated"], "Unmet": metrics["unmet"], "Budget (RM)": st.session_state.budget, "Stock": st.session_state.stock, "Cost per unit (RM)": st.session_state.unit_cost, "Spend (RM)": metrics["spent"]})
            st.success("Scenario recorded in this browser session. It is not a verified distribution event.")
    st.markdown('<div class="section-kicker">03 / PROPOSED REQUEST ALLOCATION</div>', unsafe_allow_html=True)
    st.dataframe(allocation, use_container_width=True, hide_index=True)
    st.download_button("Download allocation CSV", allocation.to_csv(index=False).encode("utf-8-sig"), file_name="aid_flow_allocation.csv", mime="text/csv")

elif page == "Request Register":
    st.subheader("Anonymous request register")
    st.caption("For demonstration, use fictional labels only. Changes are kept within this Streamlit session.")
    with st.form("request_form", clear_on_submit=True):
        x, y, z = st.columns([2, 1, 1])
        label = x.text_input("Anonymous request label", max_chars=48, placeholder="Household F")
        units = y.number_input("Units needed", min_value=1, max_value=1000, value=2)
        urgency = z.selectbox("Urgency (illustrative)", [1, 2, 3], index=1)
        submitted = st.form_submit_button("Add request", type="primary")
        if submitted:
            if not label.strip():
                st.error("Please enter an anonymous request label.")
            else:
                ids = st.session_state.requests["Request ID"].str.extract(r"(\d+)$")[0].dropna().astype(int)
                new_id = f'REQ-{(ids.max() + 1 if not ids.empty else 1):03d}'
                row = pd.DataFrame([{"Request ID": new_id, "Household": label.strip(), "Units needed": int(units), "Urgency": int(urgency)}])
                st.session_state.requests = pd.concat([st.session_state.requests, row], ignore_index=True)
                st.session_state.edited = True
                st.rerun()
    st.dataframe(st.session_state.requests, use_container_width=True, hide_index=True)
    if not st.session_state.requests.empty:
        to_remove = st.selectbox("Select a request to remove", st.session_state.requests["Request ID"].tolist())
        confirm = st.checkbox("Confirm removal of selected request")
        if st.button("Remove selected request", disabled=not confirm):
            st.session_state.requests = st.session_state.requests[st.session_state.requests["Request ID"] != to_remove].reset_index(drop=True)
            st.session_state.edited = True
            st.rerun()
    st.download_button("Export requests CSV", st.session_state.requests.to_csv(index=False).encode("utf-8-sig"), file_name="aid_flow_requests.csv", mime="text/csv")
    if st.button("Reset demo data"):
        st.session_state.requests = DEFAULT_REQUESTS.copy()
        st.session_state.audit = []
        st.session_state.edited = False
        st.rerun()

elif page == "Decision Log":
    st.subheader("Decision snapshots")
    st.caption("This log records simulated scenarios only. Entries are session-based and disappear when the session is reset or expires.")
    if st.session_state.audit:
        log = pd.DataFrame(st.session_state.audit)
        st.dataframe(log.iloc[::-1], use_container_width=True, hide_index=True)
        st.download_button("Export decision log CSV", log.to_csv(index=False).encode("utf-8-sig"), file_name="aid_flow_decision_log.csv", mime="text/csv")
    else:
        st.info("No scenarios recorded. Open Allocation Lab and select 'Record proposed allocation'.")

elif page == "Methodology":
    st.subheader("Model methodology and limitations")
    st.markdown("""**Objective:** Illustrate the impact of supply and budget constraints on proposed distribution of identical food packs.\n\n**Capacity:** `min(available_stock, floor(available_budget / cost_per_pack))`.\n\n**Ordering:** Highest user-entered urgency first (3 → 1), with request ID as tie-breaker. Each request receives up to its requested quantity while capacity remains.\n\n**Outputs:** Requested units, allocated units, unmet units, coverage percentage and modelled spend.\n\n**Limitations:** Urgency is manually entered and unverified; the rule may not be fair or suitable for real recipients. The prototype does not verify eligibility, prevent duplicate applications, optimize for household size, or process actual disbursements. It has no authentication, persistent database or audit-grade storage. Data is session-based.\n\n**Responsible use:** A real organisation must establish safeguarding, privacy controls, eligibility and appeal policies, human approval, validation and security reviews before operational use.\n\n**Technology:** Python, Streamlit, pandas and Plotly. No generative AI model is used in allocation decisions.""")

st.divider()
st.caption(f"AID-FLOW · Created & Developed by {CREATOR} · Malaysia · Independent simulation prototype · No live beneficiary data")
