
from typing import List


def format_table(headers: List[str], rows: List[List[str]]) -> str:
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))

    def fmt_row(cells):
        return ' | '.join(str(cells[i]).ljust(col_widths[i]) for i in range(len(headers)))

    lines = [fmt_row(headers), '-+-'.join('-' * w for w in col_widths)]
    for row in rows:
        lines.append(fmt_row(row))
    return '\n'.join(lines)
