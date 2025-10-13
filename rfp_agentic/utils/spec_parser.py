from dataclasses import dataclass
import re
from typing import Optional


@dataclass(frozen=True)
class ParsedSpec:
    item_name: str
    conductor: Optional[str]
    insulation: Optional[str]
    voltage_kv: Optional[float]
    cores: Optional[float]
    area_sqmm: Optional[float]


def parse_item_spec(item_text: str) -> ParsedSpec:
    text = item_text.strip()
    # Extract conductor material (Cu/Al)
    conductor = None
    if re.search(r"\bcu\b", text, re.IGNORECASE):
        conductor = "Cu"
    elif re.search(r"\bal\b|\baluminium\b|\baluminum\b", text, re.IGNORECASE):
        conductor = "Al"

    # Insulation PVC/XLPE
    insulation = None
    if re.search(r"\bpvc\b", text, re.IGNORECASE):
        insulation = "PVC"
    if re.search(r"\bxlpe\b", text, re.IGNORECASE):
        insulation = "XLPE"

    # Voltage like 1.1kV or 11 kV
    voltage_kv = None
    m = re.search(r"(\d+(?:\.\d+)?)\s*k\s*v", text, re.IGNORECASE)
    if m:
        voltage_kv = float(m.group(1))

    # Cores like 4C, 3.5C
    cores = None
    m = re.search(r"(\d+(?:\.\d+)?)\s*[cC]\b", text)
    if m:
        cores = float(m.group(1))

    # Area like 16 sqmm, 120 mm2
    area_sqmm = None
    m = re.search(r"(\d+(?:\.\d+)?)\s*(sq\s*mm|mm2|mm\^2)", text, re.IGNORECASE)
    if m:
        area_sqmm = float(m.group(1))

    return ParsedSpec(
        item_name=text,
        conductor=conductor,
        insulation=insulation,
        voltage_kv=voltage_kv,
        cores=cores,
        area_sqmm=area_sqmm,
    )
