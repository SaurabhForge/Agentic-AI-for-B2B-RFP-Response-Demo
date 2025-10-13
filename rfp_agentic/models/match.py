from dataclasses import dataclass
from typing import Dict, List, Tuple
from rfp_agentic.utils.spec_parser import ParsedSpec
from rfp_agentic.models.datasheet import ProductSpec


@dataclass(frozen=True)
class MatchScore:
    sku: str
    score_percent: int
    detail: Dict[str, float]


def _score_numeric(target: float | None, value: float | None) -> float:
    if target is None or value is None:
        return 0.0
    if target == 0:
        return 0.0
    # Score 1.0 for exact match; degrade linearly with relative error up to 50% diff
    rel_err = abs(value - target) / target
    return max(0.0, 1.0 - min(rel_err, 0.5) / 0.5)


def _score_exact(target: str | None, value: str | None) -> float:
    if target is None or value is None:
        return 0.0
    return 1.0 if target.lower() == value.lower() else 0.0


def calculate_match(rfp: ParsedSpec, product: ProductSpec) -> MatchScore:
    detail: Dict[str, float] = {}
    # Equal weightage across required specs present in RFP
    weights: List[Tuple[str, float]] = []

    if rfp.conductor is not None:
        s = _score_exact(rfp.conductor, product.conductor)
        detail["conductor"] = s
        weights.append(("conductor", 1.0))
    if rfp.insulation is not None:
        s = _score_exact(rfp.insulation, product.insulation)
        detail["insulation"] = s
        weights.append(("insulation", 1.0))
    if rfp.voltage_kv is not None:
        s = _score_numeric(rfp.voltage_kv, product.voltage_kv)
        detail["voltage_kv"] = s
        weights.append(("voltage_kv", 1.0))
    if rfp.cores is not None:
        s = _score_numeric(rfp.cores, product.cores)
        detail["cores"] = s
        weights.append(("cores", 1.0))
    if rfp.area_sqmm is not None:
        s = _score_numeric(rfp.area_sqmm, product.area_sqmm)
        detail["area_sqmm"] = s
        weights.append(("area_sqmm", 1.0))

    if not weights:
        overall = 0.0
    else:
        overall = sum(detail[name] for name, _ in weights) / len(weights)

    return MatchScore(sku=product.sku, score_percent=int(round(overall * 100)), detail=detail)


def top_matches(rfp: ParsedSpec, products: List[ProductSpec], n: int = 3) -> List[MatchScore]:
    scores = [calculate_match(rfp, p) for p in products]
    scores.sort(key=lambda s: s.score_percent, reverse=True)
    return scores[:n]
