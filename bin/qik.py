#!/usr/bin/env python3

# beautiful because tiny  # forked in many packages  # missing from:  https://pypi.org

"""
usage: import qik

competently welcome you into quick casual Python work, batteries included

examples:

  git clone https://github.com/pelavarre/qik.git
  python3 -i -c ''
  import qik

  t1 = qik._QIK_TABLE_1
  print(t1)

  #
  # . |  A  |    B     |   C
  # --|-----|----------|------
  # 0 |   5 | three    | True
  # 1 | 123 | thirteen | False
  # (2 rows)
  #

  columns = dict(t1)
  print(columns)  # {'.': [0, 1], 'A': [5, 123], 'B': ['three', ... ]}

  rows = list(t1)
  print(rows)  # [{'.': 0, 'A': 5, 'B': 'three', 'C': True}, {'.': 1, ... }]

  print(repr(t1))  # QikTable({'.': [0, 1], 'A': [5, 123], 'B': ... ]})

  t11 = qik.QikTable(t1)
  t12 = qik.QikTable(columns)
  t13 = qik.QikTable(rows)

  print(columns == dict(t13))  # True
  print(rows == list(t12))  # True

  print(t1 == t11)
  print(t1 == t12)
  print(t1 == t13)
  print(t1 == columns)
  print(t1 == rows)

  print(str(t1) == str(t11))  # True
  print(str(t1) == str(t12))  # True
  print(str(t1) == str(t13))  # True

  print(repr(t1) == repr(t11))  # True
  print(repr(t1) == repr(t12))  # True
  print(repr(t1) == repr(t13))  # True

  c = t1['A']
  r = t1[-1]
  t1['Z'] = c  # TypeError: 'QikTable' object does not support item assignment
  t1.append(r)  # TypeError: 'QikTable' object defines no 'append' mutation
"""

# code reviewed by people, and by Black and Flake8


FEATURE_VPRINT = False


class QikTable:
    """Index Cells by Int Row Index and by Str|None Column Key"""

    def __init__(self, table=None):
        """Form a QikTable as a Clone, of the Columns, else of the Rows, else of Both"""

        vprint("enter '__init__'", type(table).__name__)

        has_append = hasattr(table, "append")
        has_keys = hasattr(table, "keys")

        if has_keys and not has_append:  # like Dict but unlike List
            columns = dict(table)
            rows = columns_to_rows(columns)
        elif has_append and not has_keys:  # like List but unlike Dict
            rows = list(table)
            columns = rows_to_columns(rows)
        else:
            columns = dict(table.columns)
            rows = list(table.rows)

        self.columns = columns
        self.rows = rows

    def __eq__(self, value):
        """Say if Self indexes equal Cells inside same as Value does"""

        table = QikTable(value)

        columns_eq = self.columns == table.columns
        rows_eq = self.rows == table.rows
        eq = columns_eq and rows_eq

        return eq

    def append(self, item, /):
        """Exist to mark Self as List-Like, but raise TypeError if called"""

        vprint("enter 'append'", type(item).__name__)

        raise TypeError("'QikTable' object defines no 'append' mutation")

    def keys(self):
        """Yield each Key of the Columns, else raise KeyError"""

        vprint("enter 'keys'")

        return self.columns.keys()

    def __len__(self):
        """Count the Rows, else raise ValueError"""

        vprint("enter '__len__'")

        return self.rows.__len__()

    def __getitem__(self, key):
        """Get by Str|None from Columns, else by Int from Rows, else raise TypeError"""

        vprint("enter '__getitem__'", type(key).__name__)

        if (key is None) or isinstance(key, str):
            cells = self.columns[key]  # raises TypeError when:  columns is None
            item = cells
        elif isinstance(key, int):
            row = self.rows[key]  # raises TypeError when:  rows is None
            item = row
        else:
            raise TypeError(
                "table indices must be Int|Str|None, not {!r}".format(
                    type(key).__name__
                )
            )

        return item

    def __repr__(self):
        """Form the Code to form a Clone of Self"""

        vprint("enter '__repr__'")

        rep = "QikTable({!r})".format(self.columns)  # yep
        # rep = "QikTable({!r})".format(self.rows)  # nope

        return rep

    def __str__(self):
        """Form a concise but loose sketch of the Columns and the Rows"""

        vprint("enter '__str__'")

        rep = table_str(self)

        return rep


def table_str(self):
    """Form a concise but loose sketch of the Columns and the Rows"""

    vprint("enter 'table_str'")

    columns = self.columns
    rows = self.rows

    # Print the Headers

    lines = list()

    widths = list(max((1 + len(str(c)) + 1) for c in v) for v in columns.values())
    widths_by_k = dict(zip(columns.keys(), widths))

    reps = list()
    for (k, w) in widths_by_k.items():
        rep = str(k).center(w - 2)
        reps.append(rep)

    line = " | ".join(reps)
    lines.append(line)

    # Print the Separators

    reps = list()
    for (k, w) in widths_by_k.items():
        rep = (w - 2) * "-"
        reps.append(rep)

    line = "-|-".join(reps)
    lines.append(line)

    # Print the Rows

    for r in rows:

        reps = list()
        for (k, w) in widths_by_k.items():
            v = r[k]

            rep = w * " "  # blanks out the None cells
            if v is not None:
                if (not hasattr(v, "__int__")) or (v is False) or (v is True):
                    rep = str(v).ljust(w - 2)
                else:
                    rep = str(v).rjust(w - 2)

            reps.append(rep)

        line = " | ".join(reps)
        lines.append(line)

    # Print the Count of Rows

    line = "({} rows)".format(len(rows))
    lines.append(line)

    # Succeed

    chars = "\n".join(_.rstrip() for _ in lines)

    return chars


def columns_to_rows(columns):
    """Pick the Rows out of some Columns"""

    vprint("enter 'columns_to_rows'")

    rows = list()
    if columns:
        value_lists = list(columns.values())

        heights = sorted(set(len(_) for _ in value_lists))
        if len(heights) != 1:
            raise ValueError("__len__() should return 1 height, not {}".format(heights))

        height = heights[-1]
        for i in range(height):
            rows.append(dict())

        for (k, vv) in columns.items():
            for i in range(height):
                r = rows[i]
                r[k] = vv[i]

    return rows


def rows_to_columns(rows):
    """Pick the Columns out of some Rows"""

    vprint("enter 'rows_to_columns'")

    columns = dict()
    if rows:

        key_lists = sorted(set(tuple(r.keys()) for r in rows))
        if len(key_lists) != 1:
            raise KeyError(len(key_lists), key_lists)

        key_list = key_lists[-1]
        for k in key_list:
            columns[k] = list()

        for r in rows:
            for (k, v) in r.items():
                columns[k].append(v)

    return columns


def vprint(*args, **kwargs):
    if FEATURE_VPRINT:
        print(*args, **kwargs)


_QIK_TABLE_1 = QikTable(
    [
        {".": 0, "A": 5, "B": "three", "C": True},
        {".": 1, "A": 123, "B": "thirteen", "C": False},
    ]
)


if __name__ == "__main__":  # run most of the test of this Py File's DocString

    import sys

    qik = sys.modules[__name__]

    if FEATURE_VPRINT:
        breakpoint()

    t1 = qik._QIK_TABLE_1
    print(t1)

    columns = dict(t1)
    print(columns)

    rows = list(t1)
    print(rows)

    print(repr(t1))

    t11 = qik.QikTable(t1)
    t12 = qik.QikTable(columns)
    t13 = qik.QikTable(rows)

    print(columns == dict(t13))
    print(rows == list(t12))

    print(t1 == t11)
    print(t1 == t12)
    print(t1 == t13)
    print(t1 == columns)
    print(t1 == rows)

    print(str(t1) == str(t11))
    print(str(t1) == str(t12))
    print(str(t1) == str(t13))

    print(repr(t1) == repr(t11))
    print(repr(t1) == repr(t12))
    print(repr(t1) == repr(t13))

    # don't work here to mark the test results as correct or not


# posted into:  https://github.com/pelavarre/qik/blob/main/bin/qik.py
# copied from:  git clone https://github.com/pelavarre/qik.git
