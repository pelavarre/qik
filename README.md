# qik
Competently welcome you into quick casual Python work, batteries included

Except we don't have great doc yet, so please ask us questions

# First demo

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

# Coming soon

posted here in GitHub is how to do this with:  def __getattribute__

but Mastodon knows how to do it more simply, with just 3 lines of:  def keys, def __getitem__

Mastodon at https://social.vivaldi.net/@pelavarre/109972088721120368
same answer in Twitter at https://twitter.com/pelavarre/status/1632447582923550721?s=20

# Future work

Next tests could be adding Rows, adding Columns, deleting Rows, deleting Columns

Those tests won't pass yet - and maybe they shouldn't - maybe we should consciously limit Tables to be more of an outward-facing thing, usually built near to after you finish editing them - until then, switch between working the Rows and Columns as needed, work with the Rows and Columns as indices on a large shared pile of Cells, edit your Rows and Columns as you please

Meanwhile, myself I don't yet know why the '= list' and '= dict' here do work already, and I don't yet know why adding/ deleting don't work, so i guess i'll trace how we're calling 'def \_\_getattribute\_\_' more closely till i do know what's going on

## Copied from

Posted into:  https://github.com/pelavarre/qik/blob/main/README.md
<br>
Copied from:  git clone https://github.com/pelavarre/qik.git
