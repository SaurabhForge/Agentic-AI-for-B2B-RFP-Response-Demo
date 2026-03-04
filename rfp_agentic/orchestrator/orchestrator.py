
from dataclasses import dataclass
from pathlib import Path
from rfp_agentic.agents.sales import SalesAgent
from rfp_agentic.agents.technical import TechnicalAgent
from rfp_agentic.agents.pricing import PricingAgent
from rfp_agentic.utils.formatting import format_table


@dataclass
class Orchestrator:
    data_dir: Path = Path(__file__).resolve().parent.parent.parent / 'data'
    output_dir: Path = Path(__file__).resolve().parent.parent.parent / 'output'

    def run(self) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        sales = SalesAgent(self.data_dir)
        selected_rfp = sales.identify_and_select_rfp()

        tech = TechnicalAgent(self.data_dir)
        tech_table, scope_summary, test_summary = tech.process_rfp(selected_rfp)

        pricing = PricingAgent(self.data_dir)
        price_table = pricing.price_scope(tech_table, test_summary)

        out = self.output_dir / 'rfp_response.txt'
        content = [
            'Selected RFP: ' + selected_rfp.title,
            'Due Date: ' + selected_rfp.due_date,
            '',
            'Scope Summary:',
            scope_summary,
            '',
            'Testing Summary:',
            test_summary,
            '',
            'Technical Recommendation Table:',
            tech_table,
            '',
            'Pricing Table:',
            price_table,
        ]
        out.write_text('\n'.join(content))
        print(f'Wrote consolidated response to {out}')
