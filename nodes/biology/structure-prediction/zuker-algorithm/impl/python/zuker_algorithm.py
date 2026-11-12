# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zuker-algorithm/. The authors are listed in prov/V18HE3.jsonl.

"""Zuker algorithm: a minimum free energy RNA secondary structure in a loop energy model.

Model: RNA over A, C, G, U. The allowed pairs are AU, UA, GC, CG, GU and UG. A pair
(i, j) needs j - i - 1 >= m unpaired positions inside it. No pseudoknots. The energy
of a structure is the sum of the energies of its loops, in a toy integer version of
the nearest-neighbor model (the units are abstract, not kcal/mol):

* a hairpin with u unpaired bases costs hairpin_init + u;
* a stack of the pairs (i, j) and (i + 1, j - 1) costs -(w(i, j) + w(i + 1, j - 1)),
  with w = 3 for GC, 2 for AU and 1 for GU;
* a bulge with u unpaired bases costs bulge_init + u;
* an interior loop with u1 and u2 unpaired bases costs
  interior_init + u1 + u2 + |u1 - u2|;
* bulges and interior loops with u1 + u2 > max_loop are not allowed;
* a multiloop costs a + b * (branches, with the closing pair) + c * (unpaired bases);
* the exterior loop costs 0.
"""

from dataclasses import dataclass

INF = float("inf")

PAIR_WEIGHT = {
    ("G", "C"): 3, ("C", "G"): 3,
    ("A", "U"): 2, ("U", "A"): 2,
    ("G", "U"): 1, ("U", "G"): 1,
}


@dataclass(frozen=True)
class Model:
    m: int = 3
    hairpin_init: int = 3
    bulge_init: int = 2
    interior_init: int = 1
    a: int = 3
    b: int = 1
    c: int = 0
    max_loop: int = 30


def can_pair(x: str, y: str) -> bool:
    return (x, y) in PAIR_WEIGHT


def hairpin(s: str, i: int, j: int, model: Model) -> float:
    u = j - i - 1
    if u < model.m:
        return INF
    return model.hairpin_init + u


def internal(s: str, i: int, j: int, k: int, l: int, model: Model) -> float:
    """Energy of the loop closed by (i, j) with the single inner pair (k, l)."""
    u1 = k - i - 1
    u2 = j - l - 1
    if u1 + u2 > model.max_loop:
        return INF
    if u1 == 0 and u2 == 0:
        return -(PAIR_WEIGHT[(s[i], s[j])] + PAIR_WEIGHT[(s[k], s[l])])
    if u1 == 0 or u2 == 0:
        return model.bulge_init + u1 + u2
    return model.interior_init + u1 + u2 + abs(u1 - u2)


def zuker_tables(s: str, model: Model = Model()):
    """Fill V, WM1, WM (0-based, inclusive intervals) and the exterior table F.

    V[i][j]   minimum energy of the part inside (i, j), given that i and j pair;
    WM1[i][j] minimum energy of one branch that starts at i, then unpaired bases to j;
    WM[i][j]  minimum energy of a part of a multiloop with at least one branch;
    F[j]      minimum energy of the prefix s[0 .. j - 1].
    """
    n = len(s)
    V = [[INF] * n for _ in range(n)]
    WM1 = [[INF] * n for _ in range(n)]
    WM = [[INF] * n for _ in range(n)]
    a, b, c, m, L = model.a, model.b, model.c, model.m, model.max_loop
    for d in range(m + 1, n):  # @line L1: span j - i
        for i in range(0, n - d):  # @line L2
            j = i + d
            if can_pair(s[i], s[j]):  # @line L3
                best = hairpin(s, i, j, model)  # @line L4
                for k in range(i + 1, min(i + L + 2, j - m - 1)):  # @line L5: inner pair (k, l)
                    u1 = k - i - 1
                    for l in range(max(k + m + 1, j - 1 - (L - u1)), j):
                        if V[k][l] < INF:
                            e = internal(s, i, j, k, l, model) + V[k][l]
                            if e < best:
                                best = e
                for u in range(i + 2, j):  # @line L6: multiloop, last branch starts at u
                    e = a + b + WM[i + 1][u - 1] + WM1[u][j - 1]
                    if e < best:
                        best = e
                V[i][j] = best
            WM1[i][j] = min(V[i][j] + b, WM1[i][j - 1] + c)  # @line L7
            best = INF
            for u in range(i, j + 1):  # @line L8
                before = c * (u - i)
                if u - 1 >= i and WM[i][u - 1] < before:
                    before = WM[i][u - 1]
                e = before + WM1[u][j]
                if e < best:
                    best = e
            WM[i][j] = best
    F = [0] * (n + 1)
    for j in range(1, n + 1):  # @line L9: exterior loop, prefix of length j
        best = F[j - 1]
        for k in range(0, j - m - 1):
            e = F[k] + V[k][j - 1]
            if e < best:
                best = e
        F[j] = best
    return V, WM1, WM, F


def zuker(s: str, model: Model = Model()) -> tuple[float, list[tuple[int, int]]]:
    """Return the minimum free energy and one optimal structure as 0-based pairs."""
    n = len(s)
    V, WM1, WM, F = zuker_tables(s, model)
    a, b, c, m, L = model.a, model.b, model.c, model.m, model.max_loop
    pairs: list[tuple[int, int]] = []
    stack: list[tuple] = [("F", n)]  # @line L10: traceback with an explicit stack
    while stack:
        item = stack.pop()
        kind = item[0]
        if kind == "F":
            j = item[1]
            if j == 0:
                continue
            if F[j] == F[j - 1]:
                stack.append(("F", j - 1))
                continue
            for k in range(0, j - m - 1):
                if V[k][j - 1] < INF and F[j] == F[k] + V[k][j - 1]:
                    stack.append(("F", k))
                    stack.append(("V", k, j - 1))
                    break
            else:
                raise AssertionError("no exterior split")
        elif kind == "V":
            i, j = item[1], item[2]
            pairs.append((i, j))
            if V[i][j] == hairpin(s, i, j, model):
                continue
            found = False
            for k in range(i + 1, min(i + L + 2, j - m - 1)):
                u1 = k - i - 1
                for l in range(max(k + m + 1, j - 1 - (L - u1)), j):
                    if V[k][l] < INF and V[i][j] == internal(s, i, j, k, l, model) + V[k][l]:
                        stack.append(("V", k, l))
                        found = True
                        break
                if found:
                    break
            if found:
                continue
            for u in range(i + 2, j):
                if V[i][j] == a + b + WM[i + 1][u - 1] + WM1[u][j - 1]:
                    stack.append(("WM", i + 1, u - 1))
                    stack.append(("WM1", u, j - 1))
                    found = True
                    break
            if not found:
                raise AssertionError("no case for V")
        elif kind == "WM1":
            i, j = item[1], item[2]
            if WM1[i][j] == V[i][j] + b:
                stack.append(("V", i, j))
            else:
                stack.append(("WM1", i, j - 1))
        else:  # WM
            i, j = item[1], item[2]
            for u in range(i, j + 1):
                if WM[i][j] == c * (u - i) + WM1[u][j]:
                    stack.append(("WM1", u, j))
                    break
                if u - 1 >= i and WM[i][j] == WM[i][u - 1] + WM1[u][j]:
                    stack.append(("WM", i, u - 1))
                    stack.append(("WM1", u, j))
                    break
            else:
                raise AssertionError("no case for WM")
    pairs.sort()
    return F[n], pairs  # @line L11


def children(n: int, structure: list[tuple[int, int]]) -> dict:
    """Map each pair (and None for the exterior loop) to the pairs directly inside it."""
    partner = [-1] * n
    for i, j in structure:
        partner[i], partner[j] = j, i
    kids: dict = {None: []}
    for i, j in structure:
        kids[(i, j)] = []
    stack: list = [None]
    for x in range(n):
        p = partner[x]
        if p > x:
            kids[stack[-1]].append((x, p))
            stack.append((x, p))
        elif 0 <= p < x:
            stack.pop()
    return kids


def energy(s: str, structure: list[tuple[int, int]], model: Model = Model()) -> float:
    """Energy of a secondary structure by loop decomposition (INF if a loop is not allowed)."""
    kids = children(len(s), structure)
    total = 0
    for (i, j) in structure:
        inner = kids[(i, j)]
        if not inner:
            total += hairpin(s, i, j, model)
        elif len(inner) == 1:
            k, l = inner[0]
            total += internal(s, i, j, k, l, model)
        else:
            paired = sum(l - k + 1 for k, l in inner)
            unpaired = (j - i - 1) - paired
            total += model.a + model.b * (len(inner) + 1) + model.c * unpaired
    return total


def to_dot_bracket(n: int, structure: list[tuple[int, int]]) -> str:
    out = ["."] * n
    for i, j in structure:
        out[i], out[j] = "(", ")"
    return "".join(out)
