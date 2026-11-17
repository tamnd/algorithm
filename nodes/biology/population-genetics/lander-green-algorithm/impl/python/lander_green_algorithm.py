# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lander-green-algorithm/. The authors are listed in prov/13J1K1.jsonl.
"""The Lander-Green algorithm: a hidden Markov model over inheritance vectors.

A pedigree maps each person to (father, mother), or to (None, None) for a
founder. The non-founders, in the order of nonfounders(ped), are n_0, ...,
n_(k-1). An inheritance vector is an integer v of 2k bits. Bit 2t says which
gene of the father n_t got (0 for the father's paternal gene, 1 for his
maternal gene), and bit 2t + 1 says the same for the mother.

Each founder i has two founder genes, (i, 0) and (i, 1). Given v, every gene
of every person is a copy of one founder gene. Marker data: markers[j] maps a
typed person to an unordered genotype (a, b) of allele indices at marker j,
and freqs[j] are the allele frequencies at marker j. Founder genes get
independent alleles with these frequencies (linkage equilibrium, and
Hardy-Weinberg proportions in founders).

thetas[j] is the recombination fraction between markers j and j + 1, the
same in both sexes. Without interference, the bits of v change
independently from one marker to the next, each with probability thetas[j].
"""

from __future__ import annotations

import math
from typing import Dict, Hashable, List, Mapping, Optional, Sequence, Tuple

Person = Hashable
Pedigree = Mapping[Person, Tuple[Optional[Person], Optional[Person]]]


def haldane_theta(d: float) -> float:
    """Recombination fraction for a map distance d in Morgans (Haldane, no interference)."""
    return 0.5 * (1.0 - math.exp(-2.0 * d))


def topological(ped: Pedigree) -> List[Person]:
    """The people with every parent before each child."""
    done, order = set(), []
    for start in ped:
        stack = [(start, False)]
        while stack:
            p, expanded = stack.pop()
            if p in done:
                continue
            f, m = ped[p]
            if expanded or f is None:
                done.add(p)
                order.append(p)
                continue
            stack.append((p, True))
            for q in (m, f):
                if q not in done:
                    stack.append((q, False))
    return order


def nonfounders(ped: Pedigree) -> List[Person]:
    return [p for p in topological(ped) if ped[p][0] is not None]


def gene_flow(ped: Pedigree, v: int, order=None, nf_index=None) -> Dict[Person, Tuple]:
    """The two founder genes (paternal, maternal) that each person carries under v."""
    order = order or topological(ped)
    if nf_index is None:
        nf_index = {p: t for t, p in enumerate(nonfounders(ped))}
    genes: Dict[Person, Tuple] = {}
    for p in order:
        f, m = ped[p]
        if f is None:
            genes[p] = ((p, 0), (p, 1))
        else:
            t = nf_index[p]
            genes[p] = (genes[f][(v >> (2 * t)) & 1], genes[m][(v >> (2 * t + 1)) & 1])
    return genes


def emission(genes: Mapping[Person, Tuple], typed: Mapping[Person, Tuple[int, int]],
             freqs: Sequence[float]) -> float:
    """P(marker genotypes | inheritance vector), by the founder gene graph.

    Each typed person is an edge between its two founder genes, labeled with
    its unordered genotype. In each connected component the allele of one
    gene fixes all the others, so a component has at most two consistent
    allele assignments. The result is the product over components of the sum
    over these assignments of the product of the allele frequencies.
    """
    adj: Dict[tuple, List[Tuple[tuple, Tuple[int, int]]]] = {}
    for p, (a, b) in typed.items():
        u, w = genes[p]
        adj.setdefault(u, []).append((w, (a, b)))
        if w != u:
            adj.setdefault(w, []).append((u, (a, b)))
    seen = set()
    prob = 1.0
    for start in adj:
        if start in seen:
            continue
        comp_total = 0.0
        for x in sorted(set(adj[start][0][1])):
            allele = {start: x}
            stack = [start]
            ok = True
            while stack and ok:
                u = stack.pop()
                xu = allele[u]
                for w, (a, b) in adj[u]:
                    if xu == a:
                        need = b
                    elif xu == b:
                        need = a
                    else:
                        ok = False
                        break
                    if w in allele:
                        if allele[w] != need:
                            ok = False
                            break
                    else:
                        allele[w] = need
                        stack.append(w)
            if ok:
                term = 1.0
                for g in allele.values():
                    term *= freqs[g]
                comp_total += term
        if comp_total == 0.0:
            return 0.0
        # Mark the whole component as seen with a plain search on adj.
        stack = [start]
        seen.add(start)
        while stack:
            u = stack.pop()
            for w, _ in adj[u]:
                if w not in seen:
                    seen.add(w)
                    stack.append(w)
        prob *= comp_total
    return prob


def transition(vec: List[float], bits: int, theta: float) -> List[float]:
    """Apply the 2^bits by 2^bits transition matrix, one bit at a time."""
    out = list(vec)
    keep = 1.0 - theta
    for b in range(bits):
        step = 1 << b
        for v in range(len(out)):
            if v & step:
                continue
            x, y = out[v], out[v | step]
            out[v] = keep * x + theta * y
            out[v | step] = theta * x + keep * y
    return out


def emissions(ped: Pedigree, markers: Sequence[Mapping[Person, Tuple[int, int]]],
              freqs: Sequence[Sequence[float]]) -> List[List[float]]:
    """e[j][v] = P(data at marker j | inheritance vector v), for all j and v."""
    order = topological(ped)
    nf = nonfounders(ped)
    nf_index = {p: t for t, p in enumerate(nf)}
    bits = 2 * len(nf)
    flows = [gene_flow(ped, v, order, nf_index) for v in range(1 << bits)]
    return [[emission(flows[v], markers[j], freqs[j]) for v in range(1 << bits)]
            for j in range(len(markers))]


def lander_green(ped: Pedigree, markers, freqs, thetas):
    """Forward and backward passes with scaling.

    Returns (log_likelihood, posterior), where posterior[j][v] is
    P(inheritance vector v at marker j | all marker data).
    """
    nf = nonfounders(ped)
    bits = 2 * len(nf)
    size = 1 << bits
    M = len(markers)
    if len(thetas) != M - 1:
        raise ValueError("need one recombination fraction between each pair of markers")
    e = emissions(ped, markers, freqs)  # @line L1
    alpha: List[List[float]] = []
    scale: List[float] = []
    cur = [e[0][v] / size for v in range(size)]  # @line L2
    for j in range(M):  # @line L3
        if j > 0:
            pred = transition(alpha[-1], bits, thetas[j - 1])  # @line L4
            cur = [pred[v] * e[j][v] for v in range(size)]  # @line L5
        c = sum(cur)
        if c == 0.0:
            raise ValueError(f"the data at marker {j} are inconsistent with Mendel's laws")
        scale.append(c)  # @line L6
        alpha.append([x / c for x in cur])
    loglik = sum(math.log(c) for c in scale)  # @line L7
    beta = [1.0] * size
    post = [None] * M
    post[M - 1] = list(alpha[M - 1])
    for j in range(M - 2, -1, -1):  # @line L8
        tmp = [e[j + 1][v] * beta[v] for v in range(size)]
        beta = transition(tmp, bits, thetas[j])
        beta = [b / scale[j + 1] for b in beta]
        post[j] = [alpha[j][v] * beta[v] for v in range(size)]  # @line L9
    return loglik, post


def ibd_distribution(ped: Pedigree, post_j: Sequence[float], a: Person, b: Person) -> List[float]:
    """P(a and b share 0, 1 or 2 founder genes) at one marker, from the posterior."""
    order = topological(ped)
    nf_index = {p: t for t, p in enumerate(nonfounders(ped))}
    out = [0.0, 0.0, 0.0]
    for v, pv in enumerate(post_j):
        if pv == 0.0:
            continue
        g = gene_flow(ped, v, order, nf_index)
        ga, gb = list(g[a]), list(g[b])
        shared = 0
        for x in ga:
            if x in gb:
                gb.remove(x)
                shared += 1
        out[shared] += pv
    return out
