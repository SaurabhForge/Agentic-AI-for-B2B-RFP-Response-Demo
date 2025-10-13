
from dataclasses import dataclass
from pathlib import Path
import json


@dataclass
class RFP:
    title: str
    due_date: str
    scope_of_supply: list
    tests: list

    @staticmethod
    def load_from_dir(dir_path: Path) -> 'RFP':
        data = json.loads((dir_path / 'rfp.json').read_text())
        return RFP(
            title=data['title'],
            due_date=data['due_date'],
            scope_of_supply=data['scope_of_supply'],
            tests=data['tests'],
        )
