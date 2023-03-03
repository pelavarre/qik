# qik
Competently welcome you into quick casual Python work, batteries included

Except we don't have great doc yet, so please ask us questions

First demo

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

Next tests could be adding Rows, adding Columns, deleting Rows, deleting Columns

Those tests won't pass yet

Myself I don't immediately know why the '= list' and '= dict' here work already

## Copied from

Posted into:  https://github.com/pelavarre/qik/blob/main/README.md
<br>
Copied from:  git clone https://github.com/pelavarre/qik.git
