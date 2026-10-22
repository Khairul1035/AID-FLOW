# AID-FLOW — Community Decision Intelligence

**Created & Developed by Mohd Khairul Ridhuan bin Mohd Fadzil · Malaysia**

A standalone, Python/Streamlit decision-support **prototype** that demonstrates how stock and budget constraints affect the allocation of identical food packages.

## Features
- Premium dark-themed responsive dashboard
- Scenario analysis: stock, budget and cost per pack
- Explainable, priority-first allocation and unmet-demand metrics
- Anonymous request register (fictional demonstration records)
- Scenario snapshots and CSV exports
- Model assumptions and limitations page

## Run locally

1. Install Python 3.10 or newer.
2. In a terminal inside this folder:

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL shown in the terminal, typically http://localhost:8501.

## Deploy independently via GitHub + Streamlit Community Cloud

1. Create a GitHub repository named `aid-flow`.
2. Upload `app.py`, `requirements.txt`, `README.md` and the `.streamlit/config.toml` file, preserving the `.streamlit` folder.
3. Open https://share.streamlit.io/ and sign in with GitHub.
4. Select **Create app** → **Deploy a public app from GitHub**.
5. Choose the repository and branch (`main`), and set main file path to `app.py`.
6. Choose an available custom subdomain and deploy.
7. Test the public URL in an incognito browser before sharing on LinkedIn.

**Note:** Streamlit Community Cloud will display Streamlit platform controls/branding, but the link will not use the ChatGPT referral parameter unless opened via a source that adds it. A paid domain or different hosting stack may be needed for full white-label presentation.

## How allocation works

`capacity = min(stock, budget // cost_per_pack)`

Requests are sorted by user-entered urgency (3 highest) and then request ID. The model allocates each request up to its demand until capacity runs out. This deterministic rule is **not** a validated fairness or eligibility policy.

## Data, privacy and scope

- Initial records are synthetic and illustrative, not actual beneficiaries.
- Do not enter personally identifying or sensitive information.
- Streamlit `session_state` is temporary, not durable multiuser storage.
- Decision log entries represent **proposals**, not actual aid distributions.
- No verified community impact is claimed.
- There is no authentication, server-side database, or audited operational workflow.

## Technology

Python · Streamlit · pandas · Plotly
