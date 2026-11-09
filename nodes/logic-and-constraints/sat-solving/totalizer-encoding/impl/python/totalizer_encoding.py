# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/totalizer-encoding/. The authors are listed in prov/MT2AEY.jsonl.

"""The totalizer of Bailleux and Boufkhad (2003), upward clauses only.

totalizer(xs, cap, top) builds a balanced binary tree over the input
literals. Each inner node gets unary output variables r_1..r_m, with
m = min(number of leaves, cap), and the clauses
    (-a_i or -b_j or r_{i+j})   for 1 <= i + j <= m,
where a_0 and b_0 stand for "true" and are left out. In every model,
"at least t inputs under the node are true" forces r_t. A leaf is its own
output. Literals are DIMACS ints; new variables are top+1, top+2, ...
"""


def totalizer(xs: list[int], cap: int, top: int) -> tuple[list[list[int]], list[int], int]:
    """Return (clauses, outputs, new top). outputs[t-1] is the literal r_t."""
    clauses: list[list[int]] = []
    counter = [top]

    def build(lo: int, hi: int) -> list[int]:  # inputs xs[lo:hi], hi - lo >= 1
        if hi - lo == 1:  # @line L1
            return [xs[lo]]
        mid = (lo + hi) // 2
        a, b = build(lo, mid), build(mid, hi)  # @line L2
        m = min(len(a) + len(b), cap)  # @line L3
        r = list(range(counter[0] + 1, counter[0] + m + 1))
        counter[0] += m
        for i in range(len(a) + 1):  # @line L4
            for j in range(len(b) + 1):
                if 1 <= i + j <= m:
                    cl = [-a[i - 1]] if i else []
                    cl += [-b[j - 1]] if j else []
                    clauses.append(cl + [r[i + j - 1]])  # @line L5
        return r  # @line L6

    if not xs or cap <= 0:
        return [], [], top
    outs = build(0, len(xs))
    return clauses, outs, counter[0]


def at_most_k(xs: list[int], k: int, top: int) -> tuple[list[list[int]], int]:
    """Encode sum(xs) <= k with a totalizer truncated at k + 1 outputs."""
    if k >= len(xs):
        return [], top
    if k < 0:
        return [[]], top
    clauses, outs, top = totalizer(xs, k + 1, top)  # @line L7
    clauses.append([-outs[k]])  # @line L8
    return clauses, top


def at_least_k(xs: list[int], k: int, top: int) -> tuple[list[list[int]], int]:
    """Encode sum(xs) >= k as 'at most len(xs) - k of the negations are true'."""
    if k <= 0:
        return [], top
    return at_most_k([-x for x in xs], len(xs) - k, top)
