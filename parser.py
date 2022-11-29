import pandas as pd
from datetime import datetime
from typing import Set, List
from enum import Enum


TEMPLATES = {
    "col-of-rowitem": "{col_name} do {row_item} é {col_value}",
    "event-date-singular": "{evt_name} ocorre em {date}",
    "event-date-plural": "{evt_name} ocorrem em {date}",
    "event-date-undefined": "Data não definida para {evt_name}"
}


class TableParseDirection(Enum):
    ROWS_FIRST = 1
    COLS_FIRST = 2


class TableParser:
    def __init__(self, direction: TableParseDirection = TableParseDirection.COLS_FIRST):
        self._dir = direction

    def parse(self, table: pd.DataFrame, include_fields: Set[str], item_index: int = 0) -> List[str]:
        sents = list()
        for row in table.to_dict("records"):
            row = list(row.items())
            item = row[item_index][1]

            if (self._dir == TableParseDirection.COLS_FIRST):
                for i in range(0, len(row)):
                    if (i != item_index and row[i][0] in include_fields):
                        template = TEMPLATES["col-of-rowitem"]
                        sent = template.format(col_name=row[i][0], row_item=item, col_value=row[i][1])
                        if (row[i][0].lower().startswith("data")):
                            if (type(row[i][1]) == datetime):
                                date = row[i][1].date()
                            elif (type(row[i][1]) == str):
                                date = row[i][1]
                            else:
                                date = None
                            template = TEMPLATES["event-date-singular"] if date else TEMPLATES["event-date-undefined"]
                            sent = template.format(evt_name=item, date=date)
                            if (";" in row[item_index][1]):
                                template = TEMPLATES["event-date-plural"]
                                sent = template.format(evt_name=item, date=date)

                        sents.append(sent)

        return sents
