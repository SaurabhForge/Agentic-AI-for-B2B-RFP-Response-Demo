from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List
import csv


@dataclass(frozen=True)
class ProductPrice:
    sku_to_price: Dict[str, float]

    @staticmethod
    def load(path: Path) -> "ProductPrice":
        mapping: Dict[str, float] = {}
        with path.open() as f:
            reader = csv.DictReader(f)
            for row in reader:
                mapping[row["SKU"]] = float(row["UnitPrice"])
        return ProductPrice(mapping)


@dataclass(frozen=True)
class TestPrice:
    test_to_price: Dict[str, float]

    @staticmethod
    def load(path: Path) -> "TestPrice":
        mapping: Dict[str, float] = {}
        with path.open() as f:
            reader = csv.DictReader(f)
            for row in reader:
                mapping[row["Test"]] = float(row["Price"])
        return TestPrice(mapping)


@dataclass(frozen=True)
class ItemPricing:
    item_name: str
    chosen_sku: str
    quantity: float
    unit_price: float
    tests_price: float

    @property
    def material_total(self) -> float:
        return self.unit_price * self.quantity

    @property
    def total(self) -> float:
        return self.material_total + self.tests_price


def compute_item_pricing(item_name: str, chosen_sku: str, quantity: float,
                         product_price: ProductPrice, test_names: List[str], test_price: TestPrice) -> ItemPricing:
    unit_price = product_price.sku_to_price.get(chosen_sku, 0.0)
    # Assume tests are per-item (lot) fixed costs (not per unit)
    tests_price = sum(test_price.test_to_price.get(name, 0.0) for name in test_names)
    return ItemPricing(
        item_name=item_name,
        chosen_sku=chosen_sku,
        quantity=quantity,
        unit_price=unit_price,
        tests_price=tests_price,
    )
