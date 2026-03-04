## Agentic AI for B2B RFP Response (Demo)

This repository contains a minimal, end-to-end framework demonstrating a multi-agent system used to automate the B2B Request For Proposal (RFP) response process. Built with a robust combination of Python and FastAPI, this application streamlines RFP identification, Technical Specifications matching, and Proposal Pricing consolidation by leveraging intelligent, autonomous agents.

### Structure
- `rfp_agentic/`: Python package
  - `agents/`: Sales, Technical, Pricing agents
  - `orchestrator/`: Main orchestrator
  - `models/`: RFP, datasheet, matching, pricing utilities
  - `utils/`: spec parsing and table formatting
- `data/`: Synthetic demo data
  - `rfp_pages/`: RFP listing page(s)
  - `rfps/`: RFP JSONs
  - `datasheets/`: OEM product specs (JSON)
  - `pricing/`: Product and test price CSVs
- `output/`: Generated consolidated response
- `app.py`: FastAPI server application
- `static/`: Frontend web interface

### Quickstart & Running Locally (Localhost)

If you have downloaded this repository and wish to run it on your local machine, follow these steps:

1. **Verify Prerequisites**
   Ensure you have Python 3.10 or higher installed on your computer.

2. **Create a Virtual Environment (Recommended)**
   It's best practice to create an isolated environment for dependencies:
   ```bash
   python -m venv venv
   
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   Install all the required Python packages into your environment:
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the Local Server**
   Run the FastAPI application via `uvicorn`:
   ```bash
   uvicorn app:app --reload --port 8000
   ```
   
5. **View the Application**
   Open your preferred web browser and navigate to:
   [http://localhost:8000/](http://localhost:8000/)

### CLI Quickstart (Script Mode)

You can also run the agentic workflow purely from the command line without the web server. From the root directory:
```bash
python3 - <<'PY'
from rfp_agentic.main import run
run()
PY
```
Output is written to `output/rfp_response.txt`.

### How it works
- **Sales Agent** scans `data/rfp_pages/index.html`, extracts RFPs, and selects those due within 90 days.
- **Technical Agent** parses RFP scope items, computes a spec match metric against `data/datasheets/*.json`, and prepares a comparison table with Top 3 SKUs and match %.
- **Pricing Agent** assigns prices from `data/pricing/products.csv` and test prices from `data/pricing/tests.csv`, consolidating totals.
- **Orchestrator** composes contextual summaries and collates outputs.

### Extending
- Add more RFPs under `data/rfps/NAME/rfp.json` and list them in `data/rfp_pages/index.html`.
- Populate more datasheets in `data/datasheets/` with fields: `sku, conductor, insulation, voltage_kv, cores, area_sqmm`.
- Adjust pricing CSVs in `data/pricing/`.

