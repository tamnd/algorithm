# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bayesian-network-structure-learning/. The authors are listed in prov/RJFQX2.jsonl.

"""Score-based structure learning of discrete Bayesian networks: the BIC and
BDeu local scores, and the exact dynamic programming over subsets of
Silander and Myllymaki (2006).

data is a list of samples, each a tuple of n integers; arity[v] is the number
of states of variable v. Sets of variables are bit masks.
"""

import math
from collections import Counter


def counts(data, v: int, parents: list[int]):
    """N_ijk as a Counter over (parent values, value of v)."""
    return Counter((tuple(x[u] for u in parents), x[v]) for x in data)


def bic(data, arity, v: int, parents: list[int]) -> float:
    """Log-likelihood at the maximum likelihood tables minus (log s / 2) times the number of parameters."""
    s = len(data)
    nijk = counts(data, v, parents)
    nij = Counter()
    for (j, _), c in nijk.items():
        nij[j] += c
    ll = sum(c * math.log(c / nij[j]) for (j, _), c in nijk.items())
    q = math.prod(arity[u] for u in parents)
    return ll - 0.5 * math.log(s) * q * (arity[v] - 1)


def bdeu(data, arity, v: int, parents: list[int], ess: float = 1.0) -> float:
    """Log BDeu local score with equivalent sample size ess (Heckerman, Geiger and Chickering 1995)."""
    q = math.prod(arity[u] for u in parents)
    r = arity[v]
    a_j, a_jk = ess / q, ess / (q * r)
    nijk = counts(data, v, parents)
    nij = Counter()
    for (j, _), c in nijk.items():
        nij[j] += c
    out = sum(math.lgamma(a_j) - math.lgamma(a_j + c) for c in nij.values())
    out += sum(math.lgamma(a_jk + c) - math.lgamma(a_jk) for c in nijk.values())
    return out


def members(mask: int) -> list[int]:
    return [i for i in range(mask.bit_length()) if mask >> i & 1]


def local_scores(data, arity, n: int, score) -> list[dict[int, float]]:
    """ls[v][C] = score(v, parents C) for every C not containing v."""
    ls = []
    for v in range(n):
        d = {}
        for c in range(1 << n):
            if not c >> v & 1:
                d[c] = score(data, arity, v, members(c))
        ls.append(d)
    return ls


def silander_myllymaki(n: int, ls: list[dict[int, float]]):
    """Exact score-maximizing DAG. Returns (score, parents) with parents[v] a bit mask."""
    full = (1 << n) - 1
    # step 1: bps[v][C] = the best parent set of v inside C, and its score
    bps = []
    for v in range(n):
        best = {}
        for c in sorted(ls[v], key=lambda m: bin(m).count("1")):
            cand = (ls[v][c], c)
            for u in members(c):
                prev = best[c & ~(1 << u)]
                if prev[0] > cand[0]:
                    cand = prev
            best[c] = cand
        bps.append(best)
    # step 2: best network on each subset W, by choosing its sink
    score = {0: 0.0}
    sink = {}
    for w in range(1, full + 1):
        score[w] = -math.inf
        for v in members(w):
            rest = w & ~(1 << v)
            val = score[rest] + bps[v][rest][0]
            if val > score[w]:
                score[w], sink[w] = val, v
    # step 3: peel off the sinks to get an order, then take the best parents among the predecessors
    parents = [0] * n
    w = full
    while w:
        v = sink[w]
        w &= ~(1 << v)
        parents[v] = bps[v][w][1]
    return score[full], parents


def network_score(ls, parents) -> float:
    return sum(ls[v][p] for v, p in enumerate(parents))
