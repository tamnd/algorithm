# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lossless-join-test/. The authors are listed in prov/R7WCET.jsonl.
"""The tableau test of Aho, Beeri and Ullman (1979) for a lossless join under functional dependencies.

A tableau is a list of rows, one row per part of the decomposition. Each entry is a
symbol of its column: 0 is the distinguished symbol, and the positive integer i is the
symbol that row i - 1 has at the start. Symbols of different columns are never compared.
"""


def start_tableau(attrs, parts):
    """Row i has 0 in each column of parts[i] and the symbol i + 1 in each other column."""
    return [[0 if a in p else i + 1 for a in attrs] for i, p in enumerate(parts)]  # @line L1


def chase_fds(tableau, fds):
    """Apply the FD rule until no FD is violated, in place.

    fds holds pairs (lhs, rhs) of lists of column indexes. Returns the number of rounds,
    the last round included (it changes nothing).
    """
    rounds = 0
    changed = True
    while changed:  # @line L2
        changed = False  # @line L3
        rounds += 1
        for lhs, rhs in fds:  # @line L4
            groups = {}
            for row in tableau:  # @line L5: group the rows by their symbols on X
                groups.setdefault(tuple(row[j] for j in lhs), []).append(row)
            for key in sorted(groups):
                rows = groups[key]
                for j in rhs:  # @line L6
                    syms = {row[j] for row in rows}
                    if len(syms) > 1:
                        s = min(syms)  # @line L7
                        for row in tableau:  # @line L8: rename in the whole column
                            if row[j] in syms:
                                row[j] = s
                        changed = True
    return rounds  # @line L9: the last round changed nothing


def lossless_join_test(attrs, fds, parts):
    """Decide whether the decomposition parts of the attributes attrs is lossless under fds.

    attrs: a sequence of distinct attribute names, the columns in order.
    fds: a sequence of pairs (lhs, rhs); each side is an iterable of attribute names.
    parts: a nonempty sequence of iterables of attribute names whose union is attrs.
    Returns (lossless, tableau). If lossless is False, the final tableau, read as a relation
    with one tuple per row, satisfies fds and is not the join of its projections on the parts.
    """
    attrs = list(attrs)
    col = {a: j for j, a in enumerate(attrs)}
    if len(col) != len(attrs):
        raise ValueError("the attribute names must be distinct")
    ps = [frozenset(p) for p in parts]
    if not ps or frozenset().union(*ps) != frozenset(attrs):
        raise ValueError("the parts must cover exactly the attributes")
    idx = []
    for lhs, rhs in fds:
        names = set(lhs) | set(rhs)
        if not names <= col.keys():
            raise ValueError("an FD uses an unknown attribute")
        idx.append((sorted(col[a] for a in set(lhs)), sorted(col[a] for a in set(rhs))))
    tableau = start_tableau(attrs, ps)
    chase_fds(tableau, idx)
    for row in tableau:
        if all(x == 0 for x in row):  # @line L10
            return True, tableau
    return False, tableau  # @line L11
