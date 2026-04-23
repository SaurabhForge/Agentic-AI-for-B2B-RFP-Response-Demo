## Agentic AI for B2B RFP Response (Demo)

This repository contains a minimal, end-to-end framework demonstrating a multi-agent system used to automate the B2B Request For Proposal (RFP) response process. Built with a robust combination of AI agents (Sales, Technical, and Pricing), this system intelligently processes RFP documents, matches them against product specifications, and generates comprehensive, data-driven responses.

**Key Features:**
- **Multi-Agent Architecture**: Sales Agent identifies opportunities, Technical Agent performs spec matching, Pricing Agent calculates costs
- **Intelligent RFP Processing**: Automated extraction and analysis of RFP requirements
- **Specification Matching**: Advanced algorithm that compares RFP scope against product datasheets
- **Web UI & CLI Support**: Both FastAPI web interface and command-line script modes available
- **Extensible Design**: Easy to add new RFPs, datasheets, and pricing data

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

#### Prerequisites
- **Python 3.10 or higher**: Ensure you have Python installed on your system
- **Git** (optional): For cloning the repository
- **pip**: Python package manager (typically bundled with Python)

#### Step-by-Step Setup

1. **Clone or Download the Repository**
   ```bash
   git clone https://github.com/SaurabhForge/Agentic-AI-for-B2B-RFP-Response-Demo.git
   cd Agentic-AI-for-B2B-RFP-Response-Demo
   ```

2. **Create a Virtual Environment (Recommended)**
   Creating an isolated environment keeps your project dependencies separate from system packages:
   ```bash
   python -m venv venv
   
   # On Windows:
   .\venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   Install all required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables (if needed)**
   If the application requires API keys or configuration settings, create a `.env` file in the root directory and add the necessary variables.

5. **Start the Local Server**
   Run the FastAPI application with auto-reload enabled:
   ```bash
   uvicorn app:app --reload --port 8000
   ```
   You should see output indicating the server is running on `http://127.0.0.1:8000`

6. **Access the Application**
   Open your preferred web browser and navigate to:
   - **Main Application**: [http://localhost:8000/](http://localhost:8000/)
   - **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI)
   - **Alternative API Docs**: [http://localhost:8000/redoc](http://localhost:8000/redoc) (ReDoc)

#### Troubleshooting

- **Port 8000 already in use**: Change the port with `uvicorn app:app --reload --port 8001`
- **Python not found**: Make sure Python is installed and added to your system PATH
- **Dependencies installation fails**: Try upgrading pip: `pip install --upgrade pip`
- **Virtual environment activation issues**: Refer to [Python venv documentation](https://docs.python.org/3/tutorial/venv.html)

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