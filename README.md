## Agentic AI for B2B RFP Response (Demo)

This repo contains a minimal end-to-end demo of a multi-agent system to automate B2B RFP identification, SKU matching, and pricing consolidation.

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

### Quickstart
Prereqs: Python 3.10+

Run end-to-end demo:
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

