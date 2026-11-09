# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/xor-gaussian-elimination/. The authors are listed in prov/Q97DPS.jsonl.

"""Gauss-Jordan elimination over GF(2) for XOR-SAT.

An XOR clause is a pair (vars, b): the XOR of the variables in vars must be b.
A variable listed twice cancels, since x XOR x = 0. The variables are 1 .. n.
Each row is a Python int: bit v - 1 holds the coefficient of the variable v.
"""


def eliminate(n: int, equations: list[tuple[list[int], int]]) -> tuple[list[int], list[int], list[int]]:
    """Bring the system to reduced row echelon form.

    Returns (rows, rhs, pivots): rows[i] and rhs[i] are the rows after the
    elimination, and pivots[i] is the pivot column of row i for i < rank.
    The rows from index rank on are zero.
    """
    rows: list[int] = []
    rhs: list[int] = []
    for vs, b in equations:
        mask = 0
        for v in vs:
            mask ^= 1 << (v - 1)
        rows.append(mask)
        rhs.append(b & 1)
    pivots: list[int] = []
    r = 0  # @line L1
    for col in range(n):  # @line L2
        bit = 1 << col
        i = next((i for i in range(r, len(rows)) if rows[i] & bit), -1)  # @line L3
        if i == -1:
            continue
        rows[r], rows[i] = rows[i], rows[r]  # @line L4
        rhs[r], rhs[i] = rhs[i], rhs[r]
        for j in range(len(rows)):  # @line L5
            if j != r and rows[j] & bit:
                rows[j] ^= rows[r]  # @line L6
                rhs[j] ^= rhs[r]
        pivots.append(col)  # @line L7
        r += 1
    return rows, rhs, pivots


def xor_gaussian_elimination(n: int, equations: list[tuple[list[int], int]]) -> list[bool] | None:
    """Decide a system of XOR clauses over the variables 1 .. n.

    Returns a solution as a list x of n booleans, where x[v - 1] is the value
    of the variable v, with each free variable set to false; or None when the
    system has no solution. Time O(min(m, n) * m) row operations of n bits.
    """
    rows, rhs, pivots = eliminate(n, equations)
    rank = len(pivots)
    for j in range(rank, len(rows)):  # @line L8
        if rhs[j] == 1:
            return None  # @line L9
    x = [False] * n  # @line L10
    for i, col in enumerate(pivots):  # @line L11
        x[col] = rhs[i] == 1
    return x  # @line L12


def xor_solution_count(n: int, equations: list[tuple[list[int], int]]) -> int:
    """The number of solutions: 0, or 2^(n - rank)."""
    rows, rhs, pivots = eliminate(n, equations)
    if any(rhs[j] for j in range(len(pivots), len(rows))):
        return 0
    return 1 << (n - len(pivots))
