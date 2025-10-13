
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime, timedelta
import re
from rfp_agentic.models.rfp import RFP


@dataclass
class SalesAgent:
    data_dir: Path

    def identify_and_select_rfp(self) -> RFP:
        # Scan synthetic web page for RFPs and select one due within 90 days
        page = (self.data_dir / 'rfp_pages' / 'index.html').read_text()
        # Example format: "... Due 2025-12-15 - link: rfps/sample_rfp_1"
        candidates = []
        for m in re.finditer(r"Due\s+(\d{4}-\d{2}-\d{2}).*?link:\s*([\w\-/]+)", page):
            due_str, link = m.group(1), m.group(2)
            due_date = datetime.strptime(due_str, "%Y-%m-%d").date()
            candidates.append((due_date, link))
        candidates.sort()
        today = datetime.utcnow().date()
        horizon = today + timedelta(days=90)
        for due_date, link in candidates:
            if today <= due_date <= horizon:
                return RFP.load_from_dir(self.data_dir / link)
        # Fallback: pick the first
        if candidates:
            return RFP.load_from_dir(self.data_dir / candidates[0][1])
        # Default synthetic
        return RFP.load_from_dir(self.data_dir / 'rfps' / 'sample_rfp_1')
