# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/denial-constraint/. The authors are listed in prov/HJ9YV3.jsonl.

"""Denial constraints and the detection of their violations.

A row is a tuple of values. A term is (1, a) for attribute a of the first
tuple variable, (2, a) for attribute a of the second, or ("c", v) for the
constant v. A predicate is (left, op, right) with op one of =, !=, <, <=, >,
>=, and left is a term of a tuple variable. A denial constraint is a list of
predicates and says that no assignment of rows to the tuple variables makes
all of them true. A constraint that mentions only (1, a) terms has one tuple
variable; otherwise it has two, and the two rows must be different rows.
Set semantics: the rows are distinct.
"""

OPS = {
    "=": lambda x, y: x == y,
    "!=": lambda x, y: x != y,
    "<": lambda x, y: x < y,
    "<=": lambda x, y: x <= y,
    ">": lambda x, y: x > y,
    ">=": lambda x, y: x >= y,
}


def _value(term, s, t):
    k, a = term
    if k == "c":
        return a
    return s[a] if k == 1 else t[a]


def holds(pred, s, t):
    left, op, right = pred
    return OPS[op](_value(left, s, t), _value(right, s, t))


def arity(dc):
    """The number of tuple variables of a constraint: 1 or 2."""
    terms = [p[0] for p in dc] + [p[2] for p in dc]
    return 2 if any(k == 2 for k, _ in terms) else 1


def violations_brute(rows, dc):
    """The violations by the definition: each row i (one variable) or each
    ordered pair (i, j) of different rows (two variables) that makes all predicates true."""
    if arity(dc) == 1:
        return {(i,) for i, s in enumerate(rows) if all(holds(p, s, s) for p in dc)}
    return {
        (i, j)
        for i, s in enumerate(rows)
        for j, t in enumerate(rows)
        if i != j and all(holds(p, s, t) for p in dc)
    }


def violations(rows, dc):
    """The same set as violations_brute, found by hashing on the equality
    predicates between the two tuple variables."""
    if arity(dc) == 1:
        return violations_brute(rows, dc)
    joins, rest = [], []  # @line L1
    for left, op, right in dc:
        if op == "=" and {left[0], right[0]} == {1, 2}:
            if left[0] == 2:
                left, right = right, left
            joins.append((left[1], right[1]))
        else:
            rest.append((left, op, right))
    table = {}  # @line L2
    for j, t in enumerate(rows):  # @line L3
        table.setdefault(tuple(t[b] for _, b in joins), []).append(j)
    out = set()
    for i, s in enumerate(rows):  # @line L4
        for j in table.get(tuple(s[a] for a, _ in joins), ()):  # @line L5
            if i != j and all(holds(p, s, rows[j]) for p in rest):  # @line L6
                out.add((i, j))
    return out


def from_fd(lhs, rhs):
    """The denial constraints of the functional dependency lhs -> rhs, one per attribute of rhs."""
    return [[((1, a), "=", (2, a)) for a in lhs] + [((1, b), "!=", (2, b))] for b in rhs]


def satisfies(rows, dcs):
    return all(not violations(rows, dc) for dc in dcs)
