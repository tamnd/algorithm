# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ibm-model-3/. The authors are listed in prov/2CTGQ5.jsonl.

"""IBM Model 3 (Brown et al. 1993, Section 4.4, Equation 32), its exact E step by
enumeration for small pairs, and the approximate E step by hill climbing and pegging.

A pair is (f, e): the generated sentence f = f_1 .. f_m and the given sentence
e = e_1 .. e_l, with the null word e_0. An alignment is a list a of length m with
a[j - 1] = a_j in 0 .. l. The parameters are a dict with

    t[(f_word, e_word)]   t(f | e), e_word may be NULL
    n[(phi, e_word)]      n(phi | e) for phi = 0 .. phi_max
    d[(j, i, l, m)]       d(j | i, l, m) for i >= 1
    p1                    the probability of a null word after each real word

    p(f, a | e) = C(m - phi_0, phi_0) p0^(m - 2 phi_0) p1^phi_0
                  * prod_{i>=1} phi_i! n(phi_i | e_i)
                  * prod_j t(f_j | e_{a_j}) * prod_{j: a_j > 0} d(j | a_j, l, m)

The arithmetic follows the type of the values: with Fraction values it is exact.
"""

import math
from collections import defaultdict
from fractions import Fraction
from itertools import product
from typing import Dict, List, Sequence, Set, Tuple

NULL = "<null>"
Pair = Tuple[Sequence[str], Sequence[str]]


def fertilities(a: Sequence[int], l: int) -> List[int]:
    phi = [0] * (l + 1)
    for i in a:
        phi[i] += 1
    return phi


def structure_prob(a: Sequence[int], e: Sequence[str], m: int, params: dict):
    """Equation 32 without the factors t: the fertility, null and distortion part."""
    l = len(e)
    phi = fertilities(a, l)
    phi0 = phi[0]
    if 2 * phi0 > m:
        return 0 * params["p1"]
    p1 = params["p1"]
    p0 = 1 - p1
    w = math.comb(m - phi0, phi0) * p0 ** (m - 2 * phi0) * p1 ** phi0
    for i in range(1, l + 1):
        w *= math.factorial(phi[i]) * params["n"].get((phi[i], e[i - 1]), 0)
    for j, i in enumerate(a, start=1):
        if i > 0:
            w *= params["d"].get((j, i, l, m), 0)
    return w


def prob(f: Sequence[str], e: Sequence[str], a: Sequence[int], params: dict):
    """p(f, a | e), Equation 32."""
    es = [NULL] + list(e)
    w = structure_prob(a, e, len(f), params)
    for j, i in enumerate(a):
        w *= params["t"].get((f[j], es[i]), 0)
    return w


def log_prob(f: Sequence[str], e: Sequence[str], a: Sequence[int], params: dict) -> float:
    """ln p(f, a | e) as a sum of logs, for sentences whose product would underflow.

    Returns -inf if a factor is 0.
    """
    l, m = len(e), len(f)
    es = [NULL] + list(e)
    phi = fertilities(a, l)
    phi0 = phi[0]
    p1 = float(params["p1"])
    factors = [float(params["t"].get((f[j], es[i]), 0)) for j, i in enumerate(a)]
    factors += [float(params["n"].get((phi[i], e[i - 1]), 0)) for i in range(1, l + 1)]
    factors += [float(params["d"].get((j, i, l, m), 0)) for j, i in enumerate(a, start=1) if i > 0]
    if 2 * phi0 > m or min(factors, default=1.0) <= 0 or (phi0 and p1 <= 0) or (m > 2 * phi0 and p1 >= 1):
        return -math.inf
    s = math.log(math.comb(m - phi0, phi0)) + phi0 * (math.log(p1) if phi0 else 0.0)
    s += (m - 2 * phi0) * (math.log(1 - p1) if m > 2 * phi0 else 0.0)
    s += sum(math.lgamma(phi[i] + 1) for i in range(1, l + 1))
    return s + sum(math.log(x) for x in factors)


def all_alignments(m: int, l: int):
    return product(range(l + 1), repeat=m)


def neighbours(a: Sequence[int], l: int, peg: Tuple[int, int] = None):
    """All alignments one move (change one a_j) or one swap (exchange a_j and a_j') away.

    With peg = (i, j), only neighbours with a_j = i are returned.
    """
    a = list(a)
    m = len(a)
    out = []
    for j in range(m):
        for i in range(l + 1):
            if i != a[j]:
                b = a[:]
                b[j] = i
                out.append(tuple(b))
    for j in range(m):
        for k in range(j + 1, m):
            if a[j] != a[k]:
                b = a[:]
                b[j], b[k] = b[k], b[j]
                out.append(tuple(b))
    if peg is not None:
        i, j = peg
        out = [b for b in out if b[j - 1] == i]
    return out


def hill_climb(f, e, a, params, peg=None) -> Tuple[int, ...]:
    """Go to the best neighbour while it is strictly better; the first of equal neighbours wins."""
    a = tuple(a)
    pa = prob(f, e, a, params)
    while True:  # @line L9
        best, pb = a, pa
        for b in neighbours(a, len(e), peg):  # @line L10
            w = prob(f, e, b, params)
            if w > pb:
                best, pb = b, w
        if best == a:  # @line L11
            return a
        a, pa = best, pb  # @line L12


def start_alignment(f, e, params) -> Tuple[int, ...]:
    """For each j, the i with the largest t(f_j | e_i) d(j | i, l, m), or t(f_j | NULL) p1 for i = 0."""
    es = [NULL] + list(e)
    l, m = len(e), len(f)
    out = []
    for j, x in enumerate(f, start=1):
        def score(i):
            t = params["t"].get((x, es[i]), 0)
            return t * (params["p1"] if i == 0 else params["d"].get((j, i, l, m), 0))
        out.append(max(range(l + 1), key=lambda i: (score(i), -i)))
    return tuple(out)


def pegged_set(f, e, params) -> Set[Tuple[int, ...]]:
    """The set S of Brown et al.: the neighbourhoods of the hill-climbed alignment and of the
    best alignment found with each link (i, j) pegged."""
    l, m = len(e), len(f)
    a0 = start_alignment(f, e, params)  # @line L1
    a = hill_climb(f, e, a0, params)  # @line L2
    s = {a, *neighbours(a, l)}  # @line L3
    for i in range(l + 1):  # @line L4
        for j in range(1, m + 1):
            b = list(a0)
            b[j - 1] = i
            b = hill_climb(f, e, b, params, peg=(i, j))  # @line L5
            s.add(b)  # @line L6
            s.update(neighbours(b, l))
    return s


def viterbi_brute(f, e, params) -> Tuple[Tuple[int, ...], object]:
    best, pb = None, None
    for a in all_alignments(len(f), len(e)):
        w = prob(f, e, a, params)
        if pb is None or w > pb:
            best, pb = a, w
    return best, pb


def expected_counts(corpus: Sequence[Pair], params: dict, exact: bool = True):
    """The E step. exact=True sums over all (l + 1)^m alignments; exact=False over the set S."""
    zero = 0 * params["p1"]
    c = {"t": defaultdict(lambda: zero), "n": defaultdict(lambda: zero), "d": defaultdict(lambda: zero),
         "p0": zero, "p1": zero}
    for f, e in corpus:
        l, m = len(e), len(f)
        es = [NULL] + list(e)
        cands = all_alignments(m, l) if exact else pegged_set(f, e, params)
        weights = [(a, prob(f, e, a, params)) for a in cands]  # @line L7
        z = sum(w for _, w in weights)
        for a, w in weights:  # @line L8
            if not w:
                continue
            q = w / z
            phi = fertilities(a, l)
            for j, i in enumerate(a, start=1):
                c["t"][(f[j - 1], es[i])] += q
                if i > 0:
                    c["d"][(j, i, l, m)] += q
            for i in range(1, l + 1):
                c["n"][(phi[i], es[i])] += q
            c["p1"] += phi[0] * q
            c["p0"] += (m - 2 * phi[0]) * q
    return c


def _normalize(old: dict, counts: dict, group) -> dict:
    tot = defaultdict(int)
    for k, v in counts.items():
        tot[group(k)] += v
    return {k: (counts.get(k, 0) / tot[group(k)] if tot[group(k)] else v) for k, v in old.items()}


def em_step(corpus: Sequence[Pair], params: dict, exact: bool = True) -> dict:
    """One EM round: the E step, then the M step for t, n, d and p1."""
    c = expected_counts(corpus, params, exact)
    total = c["p0"] + c["p1"]
    return {
        "t": _normalize(params["t"], c["t"], lambda k: k[1]),
        "n": _normalize(params["n"], c["n"], lambda k: k[1]),
        "d": _normalize(params["d"], c["d"], lambda k: k[1:]),
        "p1": c["p1"] / total if total else params["p1"],
    }


def log_likelihood(corpus: Sequence[Pair], params: dict) -> float:
    """sum over the pairs of ln p(f | e), with p(f | e) summed over all alignments."""
    s = 0.0
    for f, e in corpus:
        s += math.log(sum(prob(f, e, a, params) for a in all_alignments(len(f), len(e))))
    return s


def uniform_params(corpus: Sequence[Pair], phi_max: int = 2, p1=Fraction(1, 5)) -> dict:
    """t uniform over the source words, n uniform over 0 .. phi_max, d uniform over 1 .. m."""
    vf = sorted({x for f, _ in corpus for x in f})
    ve = sorted({y for _, e in corpus for y in e})
    t = {(x, y): Fraction(1, len(vf)) for x in vf for y in ve + [NULL]}
    n = {(k, y): Fraction(1, phi_max + 1) for k in range(phi_max + 1) for y in ve}
    d = {}
    for f, e in corpus:
        l, m = len(e), len(f)
        for i in range(1, l + 1):
            for j in range(1, m + 1):
                d[(j, i, l, m)] = Fraction(1, m)
    return {"t": t, "n": n, "d": d, "p1": p1}
