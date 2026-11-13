# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/belovs-k-distinctness/. The authors are listed in prov/KK9NWR.jsonl.
"""Belovs's learning graph for k-distinctness (FOCS 2012): the construction and its cost.

A learning graph gives a feasible solution of the dual adversary bound, and the adversary
bound is the bounded-error quantum query complexity up to a constant factor. That last step
is not simulated here. This file computes:
  exponents, sizes, weights, stage_costs: the parameters and the objective (12) of the paper;
  load: the classical loading procedure of Table 2 for one positive input and one choice of
    the internal randomness;
  DualK2: for k = 2, where the construction has no covered elements, the explicit entries of
    the matrices X_j, so that the constraints of the dual adversary bound can be checked on
    every pair of inputs of a small domain.
"""

import math
from fractions import Fraction
from itertools import combinations

STAR = None  # the value of a covered element


def exponents(k: int) -> list[Fraction]:
    """rho_1, ..., rho_(k-1) with r_i = n^(rho_i). rho_1 is the exponent of the query count."""
    rho = [1 - Fraction(2 ** (k - 2), 2**k - 1)]  # @line L1
    for _ in range(k - 2):
        rho.append((1 + rho[-1]) / 2)  # @line L2
    return rho


def sizes(n: float, k: int) -> list[float]:
    return [n ** float(p) for p in exponents(k)]  # @line L3


def weights(n: float, k: int, r: list[float]) -> dict:
    """The arc weights of Section 5.2: w on stages I.1 and II.s, (w0, w1) on stages I.s, s > 1."""
    w = {("I", 1): 1.0}  # @line L6
    for s in range(2, k):
        prod = math.prod(r[: s - 1])
        w[("I", s)] = (math.sqrt(n ** (s - 1) / prod), math.sqrt(prod / n ** (s - 1)))
    for s in range(1, k + 1):
        w[("II", s)] = 1 / math.sqrt(n**s / math.prod(r[: s - 1]))
    return w


def stage_costs(n: float, k: int, r: list[float]) -> list[float]:
    """The terms of (12): stages I.1, ..., I.(k-1), then stage II.k."""
    terms = [r[0]]
    for s in range(2, k):
        terms.append(r[s - 1] * math.sqrt(math.prod(r[: s - 1]) / n ** (s - 1)))
    terms.append(math.sqrt(n**k / math.prod(r)))
    return terms


def term_exponents(k: int) -> list[Fraction]:
    """The exact exponents of n in the terms of stage_costs, for r_i = n^(rho_i)."""
    rho = exponents(k)
    out = [rho[0]]
    for s in range(2, k):
        out.append(rho[s - 1] + (sum(rho[: s - 1]) - (s - 1)) / 2)
    out.append((k - sum(rho)) / 2)
    return out


def query_bound(n: float, k: int) -> float:
    """The objective (12) for the sizes of L3. It is k * n^(rho_1)."""
    r = sizes(n, k)
    return sum(stage_costs(n, k, r))  # @line L8


def ambainis_bound(n: float, k: int) -> float:
    """The learning graph of Table 1 (Ambainis's walk): r + sqrt(n^k / r^(k-1)) at r = n^(k/(k+1))."""
    r = n ** (k / (k + 1))
    return r + math.sqrt(n**k / r ** (k - 1))


# ---------- the loading procedure of Table 2 ----------


def load(x: list, k: int, cert: list[int], parts: list[list[int]]):
    """Load the sets S_1, ..., S_(k-1) (= parts), then a_1, ..., a_k (= cert).

    Returns (assignment, uncovered counts per part before stage II). The assignment maps each
    loaded index to its value, or to STAR if it stays covered.
    """
    if set(cert) & {i for p in parts for i in p}:
        raise ValueError("the randomness must avoid the certificate")
    alpha = {}
    shown = []  # the set of values of the uncovered elements of each part
    for s, part in enumerate(parts):  # @line L4
        vals = set()
        for t in part:
            if s == 0 or x[t] in shown[s - 1]:
                alpha[t] = x[t]
                vals.add(x[t])
            else:
                alpha[t] = STAR
        shown.append(vals)
    counts = [sum(alpha[t] is not STAR for t in p) for p in parts]
    for s, a in enumerate(cert[:-1]):  # @line L5
        if s == 0 or x[a] in shown[s - 1]:
            alpha[a] = x[a]
            shown[s].add(x[a])
        else:
            alpha[a] = STAR
    alpha[cert[-1]] = x[cert[-1]]
    return alpha, counts


def is_certificate(alpha: dict, k: int) -> bool:
    """Do the uncovered values contain k equal values?"""
    seen = {}
    for v in alpha.values():
        if v is not STAR:
            seen[v] = seen.get(v, 0) + 1
            if seen[v] >= k:
                return True  # @line L9
    return False


# ---------- the dual adversary solution for k = 2 ----------


class DualK2:
    """The matrices X_j of the learning graph for k = 2 on n variables, with r_1 = r.

    The randomness is a set R of size r; stage I.1 loads R in increasing order, stage II.1
    loads a_1 = min(M), stage II.2 loads a_2 = max(M), where M is the pair of equal values.
    Each arc is (stage, origin set, loaded index). X_j = sum of q psi psi^* over the arcs that
    load j and the assignments on their origin, so X_j is positive semidefinite.
    """

    def __init__(self, n: int, r: int):
        self.n, self.r = n, r
        self.q = 1 / math.comb(n - 2, r)
        self.w = {1: 1.0, 2: n**-0.5, 3: math.sqrt(r) / n}  # I.1, II.1, II.2
        arcs = []
        for big_r in combinations(range(n), r):
            for ell in range(r):
                arcs.append((1, big_r, frozenset(big_r[:ell]), big_r[ell]))
            for j in range(n):
                if j not in big_r:
                    arcs.append((2, big_r, frozenset(big_r), j))
        for s in combinations(range(n), r + 1):
            for j in range(n):
                if j not in s:
                    arcs.append((3, None, frozenset(s), j))
        self.arcs = arcs  # @line L7

    @staticmethod
    def pair(z):
        pos = {}
        for i, v in enumerate(z):
            pos.setdefault(v, []).append(i)
        p = [ps for ps in pos.values() if len(ps) >= 2]
        return tuple(p[0]) if p else None

    def takes(self, arc, x) -> bool:
        """Is the arc taken for the positive input x for some choice of the randomness?"""
        stage, big_r, origin, j = arc
        a1, a2 = self.pair(x)
        if stage == 1:
            return a1 not in big_r and a2 not in big_r
        if stage == 2:
            return j == a1 and a2 not in big_r and a1 not in big_r
        return j == a2 and a1 in origin and a2 not in origin

    def entry(self, x, y) -> float:
        """sum over j with x_j != y_j of X_j[x, y], for f(x) = 1 and f(y) = 0."""
        total = 0.0
        for arc in self.arcs:
            _, _, origin, j = arc
            if x[j] != y[j] and all(x[i] == y[i] for i in origin) and self.takes(arc, x):
                total += self.q
        return total

    def diagonal(self, z) -> float:
        """sum over j of X_j[z, z]."""
        if self.pair(z) is None:
            return sum(self.q * self.w[a[0]] for a in self.arcs)
        return sum(self.q / self.w[a[0]] for a in self.arcs if self.takes(a, z))

    def formula(self):
        return k2_objective(self.n, self.r)


def k2_objective(n: int, r: int) -> tuple[float, float]:
    """(negative, positive) diagonal sums of DualK2(n, r) in closed form.

    The negative sum is q times the sum of the weights of all arcs, the positive sum is
    r + 1/w(II.1) + 1/w(II.2). Here c = C(n, r) / C(n - 2, r) = n(n - 1) / ((n - r)(n - r - 1)).
    """
    w2, w3 = n**-0.5, math.sqrt(r) / n
    c = n * (n - 1) / ((n - r) * (n - r - 1))
    neg = c * (r + (n - r) * w2 + (n - r - 1) * (n - r) / (r + 1) * w3)
    pos = r + 1 / w2 + 1 / w3
    return neg, pos
