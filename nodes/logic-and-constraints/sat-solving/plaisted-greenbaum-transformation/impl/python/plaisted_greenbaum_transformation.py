# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/plaisted-greenbaum-transformation/. The authors are listed in prov/KVGY32.jsonl.

"""Plaisted-Greenbaum transformation: a Tseitin encoding that keeps, for each
gate, only the directions of y <-> op(args) that its polarity needs.

The circuit format is the one of the Tseitin page: inputs 1..n, gate i defines
variable n + 1 + i as ("and", lits), ("or", lits) or ("xor", [a, b]), and the
output is a literal. Time and size O(n + total fan-in).
"""

Gate = tuple[str, list[int]]
POS, NEG = 1, 2  # bit flags of the polarity set


def polarities(n: int, gates: list[Gate], out: int) -> list[int]:
    """Return pol[v] for v in 1..n+len(gates): a subset of {POS, NEG} as flags."""
    pol = [0] * (n + len(gates) + 1)
    pol[abs(out)] = POS if out > 0 else NEG  # @line L1
    for i in range(len(gates) - 1, -1, -1):  # @line L2
        op, args = gates[i]
        p = pol[n + 1 + i]
        if p == 0:
            continue
        for a in args:  # @line L3
            if op == "xor":
                q = POS | NEG  # @line L4
            else:
                q = p if a > 0 else ((p & POS) << 1) | ((p & NEG) >> 1)  # @line L5
            pol[abs(a)] |= q
    return pol


def plaisted_greenbaum(n: int, gates: list[Gate], out: int) -> list[list[int]]:
    """Return the one-sided definitional CNF and the unit clause [out]."""
    pol = polarities(n, gates, out)
    clauses: list[list[int]] = []
    for i, (op, args) in enumerate(gates):  # @line L6
        y = n + 1 + i
        if pol[y] & POS:  # @line L7
            clauses.extend(upward(op, y, args))
        if pol[y] & NEG:  # @line L8
            clauses.extend(downward(op, y, args))
    clauses.append([out])  # @line L9
    return clauses


def upward(op: str, y: int, args: list[int]) -> list[list[int]]:
    """Clauses of y -> op(args)."""
    if op == "and":
        return [[-y, a] for a in args]
    if op == "or":
        return [[-y] + list(args)]
    a, b = args
    return [[-y, a, b], [-y, -a, -b]]


def downward(op: str, y: int, args: list[int]) -> list[list[int]]:
    """Clauses of op(args) -> y."""
    if op == "and":
        return [[y] + [-a for a in args]]
    if op == "or":
        return [[y, -a] for a in args]
    a, b = args
    return [[y, -a, b], [y, a, -b]]
