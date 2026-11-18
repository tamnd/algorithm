# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/conditional-functional-dependency/. The authors are listed in prov/CYNKMP.jsonl.

"""Conditional functional dependencies and the detection of their violations.

A row is a tuple of values. A CFD is a triple (X, Y, tableau): X and Y are
lists of attribute positions and each pattern of the tableau is a pair
(px, py) of tuples, one entry per attribute of X and of Y. An entry is a
constant or the wildcard "_". A value v matches an entry e if e is "_" or
e == v. Set semantics: the rows are distinct.
"""

WILD = "_"


def matches(values, pattern):
    return all(e == WILD or e == v for v, e in zip(values, pattern))


def project(row, attrs):
    return tuple(row[a] for a in attrs)


def pair_violates(s, t, cfd):
    """The definition, for one pair (s, t), which may be the same row twice."""
    xs, ys, tableau = cfd
    for px, py in tableau:
        sx, tx = project(s, xs), project(t, xs)
        if sx == tx and matches(sx, px):
            sy, ty = project(s, ys), project(t, ys)
            if not (sy == ty and matches(sy, py)):
                return True
    return False


def violations_brute(rows, cfd):
    """The rows that take part in a violation, by checking every pair of rows."""
    out = set()
    for i, s in enumerate(rows):
        for j, t in enumerate(rows):
            if pair_violates(s, t, cfd):
                out.update((i, j))
    return out


def violations(rows, cfd):
    """The same set, found with one scan and one grouping per pattern."""
    xs, ys, tableau = cfd
    out = set()  # @line L1
    for px, py in tableau:  # @line L2
        hit = [i for i, r in enumerate(rows) if matches(project(r, xs), px)]  # @line L3
        out.update(i for i in hit if not matches(project(rows[i], ys), py))  # @line L4
        groups = {}
        for i in hit:  # @line L5
            groups.setdefault(project(rows[i], xs), []).append(i)
        for members in groups.values():
            if len({project(rows[i], ys) for i in members}) > 1:  # @line L6
                out.update(members)
    return out  # @line L7


def satisfies(rows, cfds):
    return all(not violations(rows, c) for c in cfds)


def from_fd(xs, ys):
    """A functional dependency X -> Y as the CFD with one all-wildcard pattern."""
    return (list(xs), list(ys), [((WILD,) * len(xs), (WILD,) * len(ys))])
