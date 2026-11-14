# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unate-recursive-paradigm/. The authors are listed in prov/VCCME7.jsonl.

"""The unate recursive paradigm on covers of cubes: tautology, complement, containment.

A cube over n variables is a string over '0', '1' and '-'. A cover is
a list of cubes and stands for the OR of its cubes.
"""

Cube = str
Cover = list[Cube]


def universal(n: int) -> Cube:
    return "-" * n


def cofactor(cover: Cover, i: int, b: str) -> Cover:
    """The cofactor of the cover by x_{i+1} = b, with b in '01'."""
    out = []
    for c in cover:
        if c[i] == "-" or c[i] == b:
            out.append(c[:i] + "-" + c[i + 1:])
    return out


def cube_cofactor(cover: Cover, d: Cube) -> Cover:
    """The cofactor of the cover by the cube d (fix every literal of d)."""
    out = []
    for c in cover:
        if any(x != "-" and y != "-" and x != y for x, y in zip(c, d)):
            continue  # c and d are disjoint
        out.append("".join("-" if y != "-" else x for x, y in zip(c, d)))
    return out


def column_counts(cover: Cover, n: int) -> list[tuple[int, int]]:
    """For each variable, the number of cubes with the literal x' and with the literal x."""
    zeros = [0] * n
    ones = [0] * n
    for c in cover:
        for i, ch in enumerate(c):
            if ch == "0":
                zeros[i] += 1
            elif ch == "1":
                ones[i] += 1
    return list(zip(zeros, ones))


def is_unate(cover: Cover, n: int) -> bool:
    """True if no variable appears in both polarities in the cover."""
    return all(z == 0 or o == 0 for z, o in column_counts(cover, n))


def splitting_variable(cover: Cover, n: int) -> int:
    """The most binate variable: in the most cubes, then the most balanced.

    If the cover is unate, the variable in the most cubes. Returns -1 if
    no variable appears.
    """
    best, key = -1, None
    for i, (z, o) in enumerate(column_counts(cover, n)):
        if z + o == 0:
            continue
        k = (z > 0 and o > 0, z + o, -abs(z - o), -i)
        if key is None or k > key:
            best, key = i, k
    return best


def tautology(cover: Cover, n: int) -> bool:
    """True if the cover is 1 on every point of {0,1}^n."""
    if not cover:  # @line L1
        return False
    if universal(n) in cover:  # @line L2
        return True
    if is_unate(cover, n):  # @line L3: a unate cover is a tautology only with the universal cube
        return False
    if sum(2 ** c.count("-") for c in cover) < 2 ** n:  # @line L4: too few minterms
        return False
    i = splitting_variable(cover, n)  # @line L5
    return tautology(cofactor(cover, i, "0"), n) and tautology(cofactor(cover, i, "1"), n)  # @line L6


def contains(cover: Cover, d: Cube) -> bool:
    """True if the cube d lies inside the cover."""
    return tautology(cube_cofactor(cover, d), len(d))


def _single_cube_complement(c: Cube) -> Cover:
    """De Morgan: the complement of one cube, one cube per literal."""
    n = len(c)
    out = []
    for i, ch in enumerate(c):
        if ch != "-":
            out.append("-" * i + ("1" if ch == "0" else "0") + "-" * (n - i - 1))
    return out


def _drop_contained(cover: Cover) -> Cover:
    """Remove repeated cubes and cubes that lie in a single other cube."""
    def inside(a: Cube, b: Cube) -> bool:
        return all(y == "-" or x == y for x, y in zip(a, b))
    out: Cover = []
    for k, a in enumerate(cover):
        if any(j != k and inside(a, b) and (a != b or j < k) for j, b in enumerate(cover)):
            continue
        out.append(a)
    return out


def complement(cover: Cover, n: int) -> Cover:
    """A cover of the complement of the cover."""
    if not cover:  # @line L7
        return [universal(n)]
    if universal(n) in cover:  # @line L8
        return []
    if len(cover) == 1:  # @line L9
        return _single_cube_complement(cover[0])
    i = splitting_variable(cover, n)  # @line L10
    lo = complement(cofactor(cover, i, "0"), n)  # @line L11
    hi = complement(cofactor(cover, i, "1"), n)
    both = set(lo) & set(hi)  # @line L12: merge, a cube in both halves needs no literal
    out = sorted(both)
    out += [c[:i] + "0" + c[i + 1:] for c in lo if c not in both]
    out += [c[:i] + "1" + c[i + 1:] for c in hi if c not in both]
    return _drop_contained(out)  # @line L13
