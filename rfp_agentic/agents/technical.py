
from dataclasses import dataclass
from pathlib import Path
from rfp_agentic.models.rfp import RFP
from rfp_agentic.models.datasheet import ProductSpec
from rfp_agentic.utils.spec_parser import parse_item_spec
from rfp_agentic.models.match import top_matches
from rfp_agentic.utils.formatting import format_table


@dataclass
class TechnicalAgent:
    data_dir: Path

    def process_rfp(self, rfp: RFP):
        # Summaries for orchestrator
        scope_summary = '\n'.join(
            f"- {item['item']}: {item['quantity']} units" for item in rfp.scope_of_supply
        )
        test_summary = '\n'.join(f"- {t['name']}" for t in rfp.tests)

        # Load product specs repository
        products = ProductSpec.load_all(self.data_dir / 'datasheets')

        # Build recommendation table with spec match metric
        # Include quantity so downstream pricing can use real quantities
        headers = ['Item', 'Qty', 'Top1 SKU', 'Match %', 'Top2 SKU', 'Match %', 'Top3 SKU', 'Match %']
        rows = []
        for item in rfp.scope_of_supply:
            spec = parse_item_spec(item['item'])
            matches = top_matches(spec, products, 3)
            # Ensure at least placeholders if no products
            while len(matches) < 3:
                from rfp_agentic.models.match import MatchScore
                matches.append(MatchScore(sku='N/A', score_percent=0, detail={}))
            rows.append([
                item['item'],
                str(item.get('quantity', 1)),
                matches[0].sku, str(matches[0].score_percent),
                matches[1].sku, str(matches[1].score_percent),
                matches[2].sku, str(matches[2].score_percent),
            ])
        tech_table = format_table(headers, rows)
        return tech_table, scope_summary, test_summary
