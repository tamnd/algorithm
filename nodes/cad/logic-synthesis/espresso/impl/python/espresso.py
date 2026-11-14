# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/espresso/. The authors are listed in prov/70F55E.jsonl.

"""The Espresso loop: expand, irredundant cover and reduce, on covers of cubes.

A cube over n variables is a string over '0', '1' and '-'; a cover is
a list of cubes. F is the on-set cover and D the don't-care cover. This
version has the three main steps and the cost loop. It leaves out the
essential-prime step, LAST_GASP and MAKE_SPARSE of the full program.
"""

Cube = str
Cover = list[Cube]


# ------------------------------------------------------------ cube operations


def literals(c: Cube) -> int:
    return sum(ch != "-" for ch in c)


def cost(cover: Cover) -> tuple[int, int]:
    return len(cover), sum(literals(c) for c in cover)


def inside(a: Cube, b: Cube) -> bool:
    """True if cube a lies in cube b."""
    return all(y == "-" or x == y for x, y in zip(a, b))


def disjoint(a: Cube, b: Cube) -> bool:
    return any(x != "-" and y != "-" and x != y for x, y in zip(a, b))


def intersect(a: Cube, b: Cube) -> Cube:
    return "".join(y if x == "-" else x for x, y in zip(a, b))


def supercube(cubes: Cover) -> Cube:
    """The smallest cube that contains every cube of the list (the list is not empty)."""
    out = list(cubes[0])
    for c in cubes[1:]:
        for i, ch in enumerate(c):
            if out[i] != ch:
                out[i] = "-"
    return "".join(out)


def cube_cofactor(cover: Cover, d: Cube) -> Cover:
    return ["".join("-" if y != "-" else x for x, y in zip(c, d)) for c in cover if not disjoint(c, d)]


# ------------------------------------------------- unate recursive paradigm


def _cofactor(cover: Cover, i: int, b: str) -> Cover:
    return [c[:i] + "-" + c[i + 1:] for c in cover if c[i] in ("-", b)]


def _split(cover: Cover, n: int) -> int:
    best, key = -1, None
    for i in range(n):
        z = sum(c[i] == "0" for c in cover)
        o = sum(c[i] == "1" for c in cover)
        if z + o:
            k = (z > 0 and o > 0, z + o, -abs(z - o), -i)
            if key is None or k > key:
                best, key = i, k
    return best


def tautology(cover: Cover, n: int) -> bool:
    if not cover:
        return False
    if "-" * n in cover:
        return True
    i = _split(cover, n)
    if not any(c[i] == "0" for c in cover) or not any(c[i] == "1" for c in cover):
        # The most binate variable is unate, so the cover is unate.
        return False
    return tautology(_cofactor(cover, i, "0"), n) and tautology(_cofactor(cover, i, "1"), n)


def covered(cover: Cover, d: Cube) -> bool:
    """True if the cube d lies inside the cover."""
    return tautology(cube_cofactor(cover, d), len(d))


def complement(cover: Cover, n: int) -> Cover:
    if not cover:
        return ["-" * n]
    if "-" * n in cover:
        return []
    if len(cover) == 1:
        c = cover[0]
        return ["-" * i + ("1" if ch == "0" else "0") + "-" * (n - i - 1) for i, ch in enumerate(c) if ch != "-"]
    i = _split(cover, n)
    lo = complement(_cofactor(cover, i, "0"), n)
    hi = complement(_cofactor(cover, i, "1"), n)
    both = set(lo) & set(hi)
    out = sorted(both) + [c[:i] + "0" + c[i + 1:] for c in lo if c not in both]
    out += [c[:i] + "1" + c[i + 1:] for c in hi if c not in both]
    keep = []
    for k, a in enumerate(out):
        if not any(j != k and inside(a, b) and (a != b or j < k) for j, b in enumerate(out)):
            keep.append(a)
    return keep


# ------------------------------------------------------------------- EXPAND


def expand(F: Cover, R: Cover) -> Cover:
    """Make every cube prime, raising literals while the cube stays off R."""
    order = sorted(range(len(F)), key=lambda k: (literals(F[k]), k))  # big cubes first
    out: Cover = []
    for k in order:
        c = F[k]
        if any(inside(c, e) for e in out):  # @line L8: covered by a cube expanded before
            continue
        while True:
            raises = []
            for i, ch in enumerate(c):
                if ch != "-":
                    t = c[:i] + "-" + c[i + 1:]
                    if all(disjoint(t, r) for r in R):  # @line L9: still an implicant
                        gain = sum(inside(F[j], t) for j in order if j != k)
                        raises.append((-gain, i, t))
            if not raises:
                break  # @line L10: no literal can go, so c is prime
            c = min(raises)[2]  # @line L11: the raise that covers the most other cubes
        out.append(c)
    return [c for k, c in enumerate(out) if not any(j != k and inside(c, e) and (c != e or j < k) for j, e in enumerate(out))]


# -------------------------------------------------------------- IRREDUNDANT


def irredundant(F: Cover, D: Cover) -> Cover:
    """Drop cubes until no cube lies in the union of the others and D."""
    essential = [c for k, c in enumerate(F) if not covered(F[:k] + F[k + 1:] + D, c)]  # @line L12
    rest = [c for c in F if c not in essential and not covered(essential + D, c)]  # @line L13
    keep = list(rest)
    for c in sorted(rest, key=lambda c: (-literals(c), c)):  # @line L14: small cubes first
        others = [e for e in keep if e != c]
        if covered(essential + others + D, c):
            keep = others
    return essential + keep


# ------------------------------------------------------------------- REDUCE


def reduce(F: Cover, D: Cover, n: int) -> Cover:
    """Shrink each cube, in turn, to the smallest cube that still covers its own part."""
    F = list(F)
    order = sorted(range(len(F)), key=lambda k: (literals(F[k]), k))
    gone = set()
    for k in order:
        c = F[k]
        others = [F[j] for j in range(len(F)) if j != k and j not in gone] + D
        free = complement(cube_cofactor(others, c), n)  # @line L15: points of c no other cube covers
        if not free:
            gone.add(k)  # @line L16
            continue
        F[k] = intersect(c, supercube(free))  # @line L17
    return [F[k] for k in range(len(F)) if k not in gone]


# --------------------------------------------------------------------- loop


def espresso(n: int, F: Cover, D: Cover = ()) -> Cover:
    """A prime and irredundant cover G with F <= G <= F + D, by the Espresso loop."""
    F, D = list(F), list(D)
    if not F:
        return []
    R = complement(F + D, n)  # @line L1: the off-set
    F = expand(F, R)  # @line L2
    F = irredundant(F, D)  # @line L3
    while True:
        before = cost(F)  # @line L4
        G = reduce(F, D, n)  # @line L5
        G = expand(G, R)  # @line L6
        G = irredundant(G, D)
        if cost(G) >= before:  # @line L7: stop when the cost does not fall
            return sorted(F)
        F = G
