# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mccaskill-algorithm/. The authors are listed in prov/Y916HH.jsonl.

"""McCaskill algorithm: the partition function and the base pair probabilities of an RNA.

Model: RNA over A, C, G, U. The allowed pairs are AU, UA, GC, CG, GU and UG. A pair
(i, j) needs j - i - 1 >= m unpaired positions inside it. No pseudoknots. The energy
is a toy integer loop model (abstract units, not kcal/mol), the same as on the
Zuker algorithm page:

* hairpin with u unpaired bases: hairpin_init + u;
* stack of (i, j) on (i + 1, j - 1): -(w(i, j) + w(i + 1, j - 1)), w = 3 GC, 2 AU, 1 GU;
* bulge with u unpaired bases: bulge_init + u;
* interior loop: interior_init + u1 + u2 + |u1 - u2|, and u1 + u2 <= max_loop;
* multiloop: a + b * (branches, with the closing pair) + c * (unpaired bases);
* exterior loop: 0.

The Boltzmann weight of a structure of energy E is z ** E, where z = exp(-1 / RT) in
real units. Pass z as a Fraction for exact arithmetic, or as a float.
"""

import random
from dataclasses import dataclass
from fractions import Fraction

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


def hairpin_energy(s: str, i: int, j: int, model: Model):
    u = j - i - 1
    return None if u < model.m else model.hairpin_init + u


def internal_energy(s: str, i: int, j: int, k: int, l: int, model: Model):
    u1, u2 = k - i - 1, j - l - 1
    if u1 + u2 > model.max_loop:
        return None
    if u1 == 0 and u2 == 0:
        return -(PAIR_WEIGHT[(s[i], s[j])] + PAIR_WEIGHT[(s[k], s[l])])
    if u1 == 0 or u2 == 0:
        return model.bulge_init + u1 + u2
    return model.interior_init + u1 + u2 + abs(u1 - u2)


def inner_pairs(i: int, j: int, model: Model):
    """All (k, l) with i < k < l < j, l - k > m and (k - i - 1) + (j - l - 1) <= max_loop."""
    m, L = model.m, model.max_loop
    for k in range(i + 1, min(i + L + 2, j - m - 1)):
        u1 = k - i - 1
        for l in range(max(k + m + 1, j - 1 - (L - u1)), j):
            yield k, l


def inside(s: str, z, model: Model = Model()):
    """Return Qb, QM1, QM (n x n) and the exterior table Q (n + 1), all as weights."""
    n = len(s)
    zero = z * 0
    one = zero + 1
    Qb = [[zero] * n for _ in range(n)]
    QM1 = [[zero] * n for _ in range(n)]
    QM = [[zero] * n for _ in range(n)]
    za, zb, zc = z ** model.a, z ** model.b, z ** model.c
    for d in range(model.m + 1, n):  # @line L1: span j - i
        for i in range(0, n - d):  # @line L2
            j = i + d
            if can_pair(s[i], s[j]):
                q = z ** hairpin_energy(s, i, j, model)  # @line L3: hairpin
                for k, l in inner_pairs(i, j, model):  # @line L4: stack, bulge, interior loop
                    if Qb[k][l]:
                        q += z ** internal_energy(s, i, j, k, l, model) * Qb[k][l]
                for u in range(i + 2, j):  # @line L5: multiloop, last branch at u
                    q += za * zb * QM[i + 1][u - 1] * QM1[u][j - 1]
                Qb[i][j] = q
            QM1[i][j] = Qb[i][j] * zb + QM1[i][j - 1] * zc  # @line L6
            q = zero
            for u in range(i, j + 1):  # @line L7
                before = zc ** (u - i) + (QM[i][u - 1] if u - 1 >= i else zero)
                q += before * QM1[u][j]
            QM[i][j] = q
    Q = [one] * (n + 1)
    for j in range(1, n + 1):  # @line L8: exterior loop, prefix of length j
        q = Q[j - 1]
        for k in range(0, j - model.m - 1):
            q += Q[k] * Qb[k][j - 1]
        Q[j] = q
    return Qb, QM1, QM, Q


def partition_function(s: str, z, model: Model = Model()):
    return inside(s, z, model)[3][len(s)]


def base_pair_probabilities(s: str, z, model: Model = Model()):
    """Return Z and P with P[(i, j)] = the probability that (i, j) is a pair (0-based).

    The outside values are the derivatives of Z with respect to each inside value,
    propagated in the reverse order of the inside pass.
    """
    n = len(s)
    Qb, QM1, QM, Q = inside(s, z, model)
    zero = z * 0
    Z = Q[n]
    za, zb, zc = z ** model.a, z ** model.b, z ** model.c
    hQb = [[zero] * n for _ in range(n)]
    hQM1 = [[zero] * n for _ in range(n)]
    hQM = [[zero] * n for _ in range(n)]
    hQ = [zero] * (n + 1)
    hQ[n] = zero + 1  # @line L9: outside of Z is 1
    for j in range(n, 0, -1):  # @line L10: undo the exterior loop
        hQ[j - 1] += hQ[j]
        for k in range(0, j - model.m - 1):
            hQ[k] += hQ[j] * Qb[k][j - 1]
            hQb[k][j - 1] += hQ[j] * Q[k]
    for d in range(n - 1, model.m, -1):  # @line L11: spans in decreasing order
        for i in range(0, n - d):
            j = i + d
            h = hQM[i][j]  # @line L12: undo line L7
            if h:
                for u in range(i, j + 1):
                    before = zc ** (u - i) + (QM[i][u - 1] if u - 1 >= i else zero)
                    hQM1[u][j] += h * before
                    if u - 1 >= i:
                        hQM[i][u - 1] += h * QM1[u][j]
            h = hQM1[i][j]  # @line L13: undo line L6
            if h:
                hQb[i][j] += h * zb
                hQM1[i][j - 1] += h * zc
            h = hQb[i][j]  # @line L14: undo lines L3 to L5
            if h and Qb[i][j]:
                for k, l in inner_pairs(i, j, model):
                    if Qb[k][l]:
                        hQb[k][l] += h * z ** internal_energy(s, i, j, k, l, model)
                for u in range(i + 2, j):
                    hQM[i + 1][u - 1] += h * za * zb * QM1[u][j - 1]
                    hQM1[u][j - 1] += h * za * zb * QM[i + 1][u - 1]
    P = {}
    for i in range(n):  # @line L15: P(i, j) = Qb(i, j) * outside(i, j) / Z
        for j in range(i + 1, n):
            if Qb[i][j]:
                P[(i, j)] = Qb[i][j] * hQb[i][j] / Z
    return Z, P  # @line L16


def _pick(rng: random.Random, options):
    """Choose one (weight, action) at random in proportion to the weights."""
    total = sum(w for w, _ in options)
    r = Fraction(rng.random()) * total if isinstance(total, Fraction) else rng.random() * total
    acc = 0
    for w, action in options:
        acc += w
        if r < acc:
            return action
    for w, action in reversed(options):
        if w:
            return action
    raise ValueError("all weights are zero")


def sample(s: str, z, rng: random.Random, model: Model = Model(), tables=None) -> list[tuple[int, int]]:
    """Draw one structure from the Boltzmann distribution by stochastic traceback."""
    n = len(s)
    Qb, QM1, QM, Q = tables if tables is not None else inside(s, z, model)
    zero = z * 0
    za, zb, zc = z ** model.a, z ** model.b, z ** model.c
    pairs: list[tuple[int, int]] = []
    stack: list[tuple] = [("Q", n)]
    while stack:
        item = stack.pop()
        if item[0] == "Q":
            j = item[1]
            if j == 0:
                continue
            opts = [(Q[j - 1], ("Q", j - 1, None))]
            for k in range(0, j - model.m - 1):
                opts.append((Q[k] * Qb[k][j - 1], ("Q", k, ("B", k, j - 1))))
            act = _pick(rng, opts)
            stack.append(act[:2])
            if act[2] is not None:
                stack.append(act[2])
        elif item[0] == "B":
            i, j = item[1], item[2]
            pairs.append((i, j))
            opts = [(z ** hairpin_energy(s, i, j, model), ())]
            for k, l in inner_pairs(i, j, model):
                if Qb[k][l]:
                    opts.append((z ** internal_energy(s, i, j, k, l, model) * Qb[k][l], (("B", k, l),)))
            for u in range(i + 2, j):
                opts.append((za * zb * QM[i + 1][u - 1] * QM1[u][j - 1], (("M", i + 1, u - 1), ("M1", u, j - 1))))
            stack.extend(_pick(rng, opts))
        elif item[0] == "M1":
            i, j = item[1], item[2]
            act = _pick(rng, [(Qb[i][j] * zb, ("B", i, j)), (QM1[i][j - 1] * zc if j - 1 > i else zero, ("M1", i, j - 1))])
            stack.append(act)
        else:
            i, j = item[1], item[2]
            opts = []
            for u in range(i, j + 1):
                opts.append((zc ** (u - i) * QM1[u][j], (("M1", u, j),)))
                if u - 1 >= i:
                    opts.append((QM[i][u - 1] * QM1[u][j], (("M", i, u - 1), ("M1", u, j))))
            stack.extend(_pick(rng, opts))
    pairs.sort()
    return pairs


def children(n: int, structure: list[tuple[int, int]]) -> dict:
    partner = [-1] * n
    for i, j in structure:
        partner[i], partner[j] = j, i
    kids: dict = {None: []}
    for p in structure:
        kids[p] = []
    stack: list = [None]
    for x in range(n):
        p = partner[x]
        if p > x:
            kids[stack[-1]].append((x, p))
            stack.append((x, p))
        elif 0 <= p < x:
            stack.pop()
    return kids


def energy(s: str, structure: list[tuple[int, int]], model: Model = Model()):
    """Energy by loop decomposition, or None if a loop is not allowed."""
    kids = children(len(s), structure)
    total = 0
    for (i, j) in structure:
        inner = kids[(i, j)]
        if not inner:
            e = hairpin_energy(s, i, j, model)
        elif len(inner) == 1:
            e = internal_energy(s, i, j, inner[0][0], inner[0][1], model)
        else:
            unpaired = (j - i - 1) - sum(l - k + 1 for k, l in inner)
            e = model.a + model.b * (len(inner) + 1) + model.c * unpaired
        if e is None:
            return None
        total += e
    return total
