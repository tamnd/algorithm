# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/likelihood-weighting/. The authors are listed in prov/S0B2H9.jsonl.

"""Likelihood weighting on a discrete Bayesian network.

A network is a dict with three keys:
  parents: name -> tuple of parent names
  card:    name -> number of values (the values are 0 .. card - 1)
  cpt:     name -> dict from a tuple of parent values to a list of probabilities
The CPT entries may be floats or fractions.Fraction values.
"""

import itertools
import random


def topological_order(parents: dict) -> list:
    """Kahn's algorithm. Raise ValueError if the graph has a directed cycle."""
    children = {v: [] for v in parents}
    indeg = {v: len(parents[v]) for v in parents}
    for v, ps in parents.items():
        for p in ps:
            children[p].append(v)
    ready = sorted(v for v in parents if indeg[v] == 0)
    order = []
    while ready:
        v = ready.pop(0)
        order.append(v)
        for c in children[v]:
            indeg[c] -= 1
            if indeg[c] == 0:
                ready.append(c)
    if len(order) != len(parents):
        raise ValueError("the graph has a directed cycle")
    return order


def draw(probs: list, rng: random.Random) -> int:
    """Inverse transform draw from a finite distribution."""
    u = rng.random()
    acc = 0.0
    for x, p in enumerate(probs):
        acc += float(p)
        if u < acc:
            return x
    return max(x for x, p in enumerate(probs) if p > 0)


def weighted_sample(net: dict, evidence: dict, rng: random.Random, order: list):
    """One pass of lines L4 to L8: a sample of the mutilated network and its weight."""
    w = 1  # @line L4
    x = {}
    for v in order:  # @line L5
        u = tuple(x[p] for p in net["parents"][v])  # @line L6
        row = net["cpt"][v][u]
        if v in evidence:  # @line L7
            x[v] = evidence[v]
            w = w * row[x[v]]
        else:
            x[v] = draw(row, rng)  # @line L8
    return x, w


def likelihood_weighting(net: dict, query: str, evidence: dict, s: int, rng: random.Random):
    """Return (the estimate of P(query | evidence) as a list, the estimate of P(evidence), the weights)."""
    order = topological_order(net["parents"])  # @line L1
    total = [0.0] * net["card"][query]  # @line L2
    weights = []
    for _ in range(s):  # @line L3
        x, w = weighted_sample(net, evidence, rng, order)
        total[x[query]] += float(w)  # @line L9
        weights.append(float(w))
    z = sum(total)
    post = None if z == 0 else [t / z for t in total]  # @line L10
    return post, z / s, weights


def effective_sample_size(weights: list) -> float:
    """Kish's effective sample size (sum w)^2 / sum w^2."""
    s1 = sum(weights)
    s2 = sum(w * w for w in weights)
    return 0.0 if s2 == 0 else s1 * s1 / s2


def proposal_distribution(net: dict, evidence: dict):
    """Exact list of (assignment, proposal probability, weight) over all samples of the mutilated network.

    This enumerates what weighted_sample can return; it is for tests and small networks only.
    """
    order = topological_order(net["parents"])
    free = [v for v in order if v not in evidence]
    out = []
    for vals in itertools.product(*(range(net["card"][v]) for v in free)):
        x = dict(evidence)
        x.update(zip(free, vals))
        q, w = 1, 1
        for v in order:
            p = net["cpt"][v][tuple(x[a] for a in net["parents"][v])][x[v]]
            if v in evidence:
                w = w * p
            else:
                q = q * p
        out.append((x, q, w))
    return out


def exact_posterior(net: dict, query: str, evidence: dict):
    """P(query | evidence) and P(evidence) by summing the joint."""
    order = topological_order(net["parents"])
    tot = [0] * net["card"][query]
    for vals in itertools.product(*(range(net["card"][v]) for v in order)):
        x = dict(zip(order, vals))
        if any(x[e] != val for e, val in evidence.items()):
            continue
        p = 1
        for v in order:
            p = p * net["cpt"][v][tuple(x[a] for a in net["parents"][v])][x[v]]
        tot[x[query]] += p
    z = sum(tot)
    return [t / z for t in tot], z


def sprinkler(num=float) -> dict:
    """The cloudy, sprinkler, rain, wet grass network; num=Fraction gives exact entries."""
    def r(a, b):
        return [num(a) / num(b), 1 - num(a) / num(b)]
    return {
        "parents": {"C": (), "S": ("C",), "R": ("C",), "W": ("S", "R")},
        "card": {"C": 2, "S": 2, "R": 2, "W": 2},
        "cpt": {
            "C": {(): r(1, 2)},
            "S": {(0,): r(1, 2), (1,): r(9, 10)},
            "R": {(0,): r(8, 10), (1,): r(2, 10)},
            "W": {(0, 0): r(1, 1), (0, 1): r(1, 10), (1, 0): r(1, 10), (1, 1): r(1, 100)},
        },
    }
