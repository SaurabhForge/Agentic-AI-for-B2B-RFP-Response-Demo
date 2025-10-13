from dataclasses import dataclass
from pathlib import Path
import json
from typing import List


@dataclass(frozen=True)
class ProductSpec:
    sku: str
    conductor: str  # 'Cu' or 'Al'
    insulation: str  # 'PVC' or 'XLPE'
    voltage_kv: float
    cores: float  # allow 3.5
    area_sqmm: float

    @staticmethod
    def load_all(dir_path: Path) -> List["ProductSpec"]:
        products: List[ProductSpec] = []
        if not dir_path.exists():
            return products
        for p in sorted(dir_path.glob("*.json")):
            data = json.loads(p.read_text())
            products.append(ProductSpec(
                sku=data["sku"],
                conductor=data["conductor"],
                insulation=data["insulation"],
                voltage_kv=float(data["voltage_kv"]),
                cores=float(data["cores"]),
                area_sqmm=float(data["area_sqmm"]),
            ))
        return products
