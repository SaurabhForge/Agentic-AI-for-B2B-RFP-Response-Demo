
from dataclasses import dataclass
from pathlib import Path
from typing import List
from rfp_agentic.utils.formatting import format_table
from rfp_agentic.models.pricing import ProductPrice, TestPrice, compute_item_pricing


@dataclass
class PricingAgent:
    data_dir: Path

    def price_scope(self, tech_table: str, test_summary: str) -> str:
        # Parse the technical table to extract chosen Top1 SKU per item
        lines = [ln for ln in tech_table.splitlines() if ln.strip()]
        # Header + separator line, then data rows
        data_rows = [ln for ln in lines[2:]]
        records: List[tuple[str, str, float]] = []  # (item_name, sku, qty)
        for row in data_rows:
            parts = [p.strip() for p in row.split('|')]
            # Expect: Item | Qty | Top1 SKU | ...
            if len(parts) >= 3:
                item_name = parts[0]
                qty_str = parts[1]
                top1_sku = parts[2]
                try:
                    qty_val = float(qty_str)
                except ValueError:
                    qty_val = 1.0
                records.append((item_name, top1_sku, qty_val))

        product_price = ProductPrice.load(self.data_dir / 'pricing' / 'products.csv')
        test_price = TestPrice.load(self.data_dir / 'pricing' / 'tests.csv')
        # Collect test names
        test_names = []
        for ln in test_summary.splitlines():
            stripped = ln.strip()
            if stripped.startswith('- '):
                test_names.append(stripped[2:])

        headers = ['Item', 'Chosen SKU', 'Qty', 'Unit Price', 'Tests Price', 'Material Total', 'Grand Total']
        rows = []
        for item_name, sku, qty in records:
            pricing = compute_item_pricing(item_name=item_name, chosen_sku=sku, quantity=qty,
                                           product_price=product_price, test_names=test_names, test_price=test_price)
            rows.append([
                item_name,
                sku,
                f"{qty:.0f}",
                f"{pricing.unit_price:.2f}",
                f"{pricing.tests_price:.2f}",
                f"{pricing.material_total:.2f}",
                f"{pricing.total:.2f}",
            ])
        return format_table(headers, rows)
