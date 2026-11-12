# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nussinov-algorithm/. The authors are listed in prov/6XRW3C.jsonl.

"""Nussinov algorithm: a secondary structure with the largest number of base pairs.

Model: RNA over A, C, G, U. The allowed pairs are the Watson-Crick pairs AU and GC
and the wobble pair GU. A pair (i, j) needs j - i - 1 >= m unpaired positions
inside it (the hairpin minimum, m = 3 by default). No pseudoknots.
"""

PAIRS = frozenset({("A", "U"), ("U", "A"), ("G", "C"), ("C", "G"), ("G", "U"), ("U", "G")})


def can_pair(a: str, b: str, pairs: frozenset = PAIRS) -> bool:
    return (a, b) in pairs


def nussinov_table(s: str, m: int = 3, pairs: frozenset = PAIRS) -> list[list[int]]:
    """Return N with N[i][j] = the largest number of pairs in s[i..j] (0-based, inclusive).

    N[i][i - 1] is the empty interval, with value 0. The table has n + 1 rows so that
    N[i + 1][i] exists for i = n - 1.
    """
    n = len(s)
    N = [[0] * (n + 1) for _ in range(n + 1)]
    for d in range(1, n):  # @line L1: span j - i
        for i in range(0, n - d):  # @line L2
            j = i + d  # @line L3
            best = N[i][j - 1]  # @line L4: j is unpaired
            for k in range(i, j - m):  # @line L5: j pairs with k, k <= j - m - 1
                if can_pair(s[k], s[j], pairs):  # @line L6
                    left = N[i][k - 1] if k > i else 0
                    v = left + 1 + N[k + 1][j - 1]
                    if v > best:
                        best = v
            N[i][j] = best
    return N


def nussinov(s: str, m: int = 3, pairs: frozenset = PAIRS) -> tuple[int, list[tuple[int, int]]]:
    """Return the largest number of pairs and one optimal structure as 0-based pairs (i, j)."""
    n = len(s)
    if n == 0:
        return 0, []
    N = nussinov_table(s, m, pairs)

    def val(i: int, j: int) -> int:
        return N[i][j] if i <= j else 0

    structure: list[tuple[int, int]] = []
    stack = [(0, n - 1)]  # @line L7: traceback with an explicit stack
    while stack:  # @line L8
        i, j = stack.pop()  # @line L9
        if j - i < 1:
            continue
        if val(i, j) == val(i, j - 1):  # @line L10
            stack.append((i, j - 1))
        else:  # @line L11
            for k in range(i, j - m):  # @line L12
                if can_pair(s[k], s[j], pairs) and val(i, j) == val(i, k - 1) + 1 + val(k + 1, j - 1):
                    structure.append((k, j))  # @line L13
                    stack.append((i, k - 1))
                    stack.append((k + 1, j - 1))
                    break
    structure.sort()
    return N[0][n - 1], structure  # @line L14


def to_dot_bracket(n: int, structure: list[tuple[int, int]]) -> str:
    out = ["."] * n
    for i, j in structure:
        out[i], out[j] = "(", ")"
    return "".join(out)


def is_secondary_structure(s: str, structure: list[tuple[int, int]], m: int = 3, pairs: frozenset = PAIRS) -> bool:
    """Check the definition: allowed pairs, hairpin minimum, no shared base, no crossing."""
    used: set[int] = set()
    for i, j in structure:
        if not (0 <= i < j < len(s)) or j - i - 1 < m or not can_pair(s[i], s[j], pairs):
            return False
        if i in used or j in used:
            return False
        used.update((i, j))
    for i, j in structure:
        for k, l in structure:
            if i < k < j < l:
                return False
    return True
