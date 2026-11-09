# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tseitin-transformation/. The authors are listed in prov/69B3GH.jsonl.

"""Tseitin transformation of a Boolean circuit into an equisatisfiable CNF.

A circuit has the inputs 1..n. Gate i (0-based) defines the variable n + 1 + i
as ("and", lits), ("or", lits) or ("xor", [a, b]) of earlier literals. A literal
is a nonzero int in DIMACS style, so -v is the negation of v and NOT gates need
no variable. The output is a literal. Time and size O(n + total fan-in).
"""

Gate = tuple[str, list[int]]


def tseitin(n: int, gates: list[Gate], out: int) -> list[list[int]]:
    """Return the CNF: the definition of each gate, then the unit clause [out]."""
    clauses: list[list[int]] = []
    for i, (op, args) in enumerate(gates):  # @line L1
        y = n + 1 + i  # @line L2
        clauses.extend(define(op, y, args))  # @line L3
    clauses.append([out])  # @line L4
    return clauses


def define(op: str, y: int, args: list[int]) -> list[list[int]]:
    """Clauses of y <-> op(args)."""
    if op == "and":  # @line L5
        return [[-y, a] for a in args] + [[y] + [-a for a in args]]
    if op == "or":  # @line L6
        return [[y, -a] for a in args] + [[-y] + list(args)]
    if op == "xor":  # @line L7
        a, b = args
        return [[-y, a, b], [-y, -a, -b], [y, -a, b], [y, a, -b]]
    raise ValueError(f"unknown gate {op!r}")


def evaluate(n: int, gates: list[Gate], inputs: list[bool]) -> list[bool]:
    """Return the value of every variable 1..n+len(gates); index 0 is unused."""
    val = [False] + list(inputs)

    def lit(a: int) -> bool:
        return val[a] if a > 0 else not val[-a]

    for op, args in gates:
        if op == "and":
            val.append(all(lit(a) for a in args))
        elif op == "or":
            val.append(any(lit(a) for a in args))
        else:
            val.append(lit(args[0]) != lit(args[1]))
    return val
