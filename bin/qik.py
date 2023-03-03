# forked in many packages  # missing from:  https://pypi.org

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
  # . | A |    B     | C
  # --|---|----------|---
  # 0 | 2 | three    |  5
  # 1 | 8 | thirteen | 21
  # (2 rows)
  #

  columns = dict(t1)
  print(columns)  # {'.': [0, 1], 'A': [2, 8], ... }
  print(repr(t1))  # QikTable({'.': [0, 1], 'A': [2, 8], ... })

  rows = list(t1)
  print(rows)  # [{'.': 0, 'A': 2, 'B': 'three', 'C': 5}, {'.': 1, ... }]
  print(repr(t1))  # QikTable([{'.': 0, 'A': 2, 'B': 'three', 'C': 5}, ...  }])

  rows2 = [dict(x=0, y=0, z=0), dict(x=9, y=9, z=9)]
  t2 = qik.QikTable(rows2)
  columns2 = dict(t2)
  print(columns2)  # {'x': [0, 9], 'y': [0, 9], 'z': [0, 9]}
"""

# code reviewed by people, and by Black and Flake8


_DICT_DIR_SET = set(dir(dict())) - set(dir(list()))  # keys items get update popitem
_LIST_DIR_SET = set(dir(list())) - set(dir(dict()))  # append count extend insert remove

_OBJECT_DIR_SET = set(dir(object()))


assert "__len__" not in (_DICT_DIR_SET | _LIST_DIR_SET)
assert "__getitem__" not in (_DICT_DIR_SET | _LIST_DIR_SET)


class QikTable:
    """Contain Cells indexed by Str Column Key and by Int Row Index"""

    def __init__(self, table=None):
        """Form a QikTable as a Clone of the Rows or Columns of a Table"""

        columns = None
        rows = None

        has_append = hasattr(table, "append")  # like a List
        has_keys = hasattr(table, "keys")  # like a Dict

        if has_keys and not has_append:  # like Dict but unlike List
            columns = dict(table)
        elif has_append and not has_keys:  # like List but unlike Dict
            rows = list(table)
        else:
            table_columns = table._columns
            table_rows = table._rows
            if table_rows is None:
                assert table_columns is not None  # like Dict but unlike List
                columns = dict(table_columns)
            else:
                assert columns is None  # like List but unlike Dict
                rows = list(table_rows)

        self._columns = columns
        self._rows = rows

    def __getattribute__(self, name):
        """Work like a Dict, or work like a List, else work like part or whole Self"""

        # Work like a Dict

        if name in _DICT_DIR_SET:
            assert name not in _LIST_DIR_SET, name

            self._as_new_columns()
            result = self._columns.__getattribute__(name)

            return result

        # Work like a List

        if name in _LIST_DIR_SET:
            assert name not in _DICT_DIR_SET, name

            self._as_new_rows()
            result = self._rows.__getattribute__(name)

            return result

        # Work like part of Self

        if False:

            if name not in _OBJECT_DIR_SET:
                if name not in "_columns _rows".split():
                    _columns = super().__getattribute__("_columns")
                    _rows = super().__getattribute__("_rows")

                    if _rows is None:
                        result = _columns.__getattribute__(name)
                    else:
                        assert _columns is None
                        result = _rows.__getattribute__(name)

                    return result

        # Work like Self

        result = super().__getattribute__(name)

        return result

    def _as_new_columns(self):
        """Clone as new Dict, else reshape List into new Dict"""

        _columns = self._columns
        _rows = self._rows

        # Clone as new Dict

        if _columns is not None:
            assert _rows is None
            columns = dict(_columns)
        elif not _rows:
            columns = dict()
        else:

            # Else reshape List into new Dict

            keys_lists = sorted(set(tuple(r.keys()) for r in _rows))
            if len(keys_lists) != 1:
                raise KeyError()
            keys = keys_lists[-1]

            for k in keys:
                value_lists = list(list(r[k] for r in _rows) for k in keys)
            columns = dict(zip(keys, value_lists))

        # Succeed

        self._columns = columns
        self._rows = None

        return columns

    def _as_new_rows(self):
        """Clone as new List, else reshape Dict into new List"""

        _columns = self._columns
        _rows = self._rows

        # Clone as new List

        if _rows is not None:
            assert _columns is None
            rows = list(_rows)
        elif not _columns:
            rows = list()
        else:

            # Else reshape Dict into new List

            keys = list(_columns.keys())
            value_lists = list(_columns.values())
            height = max(len(_) for _ in value_lists)

            rows = list()
            for i in range(height):
                values = list(c[i] for c in value_lists)  # may raise IndexError

                row = dict(zip(keys, values))
                rows.append(row)

        # Succeed

        self._columns = None
        self._rows = rows

        return rows

    def __len__(self):
        """Count out the Length of Rows"""

        rows = self._as_new_rows()
        result = rows.__len__()

        return result

    def __getitem__(self, key):
        """Get Item by Str from Columns, else by Int from Rows, else by Key from Self"""

        if isinstance(key, str):
            if not self._columns:
                self._as_new_columns()

        elif isinstance(key, int):
            if not self._rows:
                self._as_new_rows()

        _columns = self._columns
        _rows = self._rows

        if _rows is None:
            result = _columns[key]  # may raise KeyError
        else:
            assert _columns is None
            result = _rows[key]  # may raise IndexError

        return result

    def __repr__(self):
        """Print the Code to form a Clone of Self"""

        _columns = self._columns
        _rows = self._rows

        if _rows is None:
            obj = _columns  # rep as Dict[Key,List[Any]]
        else:
            assert _columns is None
            obj = _rows  # rep as List[Dict[Key,Any]]

        line = "QikTable({!r})".format(obj)

        return line

    def __str__(self):
        """Print a concise but loose sketch of Self"""

        _columns = self._columns
        _rows = self._rows

        if _columns is None:
            _columns = self._as_new_columns()
        else:
            assert _rows is None
            _rows = self._as_new_rows()

        # Print the Headers

        lines = list()

        widths = list(max((1 + len(str(c)) + 1) for c in v) for v in _columns.values())
        widths_by_k = dict(zip(_columns.keys(), widths))

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

        for r in _rows:

            reps = list()
            for (k, w) in widths_by_k.items():
                v = r[k]

                rep = w * " "
                if v is not None:
                    if hasattr(v, "__int__"):
                        rep = str(v).rjust(w - 2)
                    else:
                        rep = str(v).ljust(w - 2)  # todo: 'ljust' of 'bool'

                reps.append(rep)

            line = " | ".join(reps)
            lines.append(line)

        # Print the Count of Rows

        line = "({} rows)".format(len(_rows))
        lines.append(line)

        # Succeed

        chars = "\n".join(_.rstrip() for _ in lines)

        return chars


_QIK_TABLE_1 = QikTable(
    [
        {".": 0, "A": 2, "B": "three", "C": 5},  # some Prime's
        {".": 1, "A": 8, "B": "thirteen", "C": 21},  # some Fibonacci's
    ]
)


# posted into:  https://github.com/pelavarre/qik/blob/main/bin/qik.py
# copied from:  git clone https://github.com/pelavarre/qik.git
