# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ancestral-sampling/. The authors are listed in prov/14H9V7.jsonl.

"""Ancestral (forward) sampling of a discrete Bayesian network.

A network is a dict with three keys:
  parents: name -> tuple of parent names
  card:    name -> number of values (the values are 0 .. card - 1)
  cpt:     name -> dict from a tuple of parent values to a list of probabilities
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
    """Return the smallest value x with u < probs[0] + ... + probs[x], for u uniform in [0, 1)."""
    u = rng.random()
    acc = 0.0
    for x, p in enumerate(probs):
        acc += p
        if u < acc:
            return x
    return max(x for x, p in enumerate(probs) if p > 0)  # rounding guard


def ancestral_sample(net: dict, rng: random.Random, order: list | None = None) -> dict:
    """One exact sample from the joint distribution of the network."""
    order = order or topological_order(net["parents"])  # @line L1
    x = {}
    for v in order:  # @line L2
        u = tuple(x[p] for p in net["parents"][v])  # @line L3
        x[v] = draw(net["cpt"][v][u], rng)  # @line L4
    return x  # @line L5


def joint_probability(net: dict, x: dict) -> float:
    """The chain rule product of the CPT entries."""
    p = 1.0
    for v, ps in net["parents"].items():
        p *= net["cpt"][v][tuple(x[q] for q in ps)][x[v]]
    return p


def enumerate_joint(net: dict) -> dict:
    """Exact joint: a dict from value tuples (in topological order) to probabilities."""
    order = topological_order(net["parents"])
    out = {}
    for vals in itertools.product(*(range(net["card"][v]) for v in order)):
        out[vals] = joint_probability(net, dict(zip(order, vals)))
    return out


def rejection_query(net: dict, query: str, evidence: dict, n: int, rng: random.Random):
    """Estimate P(query | evidence) from n ancestral samples, keeping those that agree with the evidence.

    Return (the estimate as a list, or None if no sample was kept, the number kept).
    """
    order = topological_order(net["parents"])
    counts = [0] * net["card"][query]  # @line L6
    kept = 0
    for _ in range(n):  # @line L7
        x = ancestral_sample(net, rng, order)  # @line L8
        if all(x[e] == val for e, val in evidence.items()):  # @line L9
            counts[x[query]] += 1
            kept += 1
    if kept == 0:
        return None, 0
    return [c / kept for c in counts], kept  # @line L10


def sprinkler() -> dict:
    """The cloudy, sprinkler, rain, wet grass network (Russell and Norvig, Figure 14.12 of the 3rd edition)."""
    return {
        "parents": {"C": (), "S": ("C",), "R": ("C",), "W": ("S", "R")},
        "card": {"C": 2, "S": 2, "R": 2, "W": 2},
        "cpt": {
            "C": {(): [0.5, 0.5]},
            "S": {(0,): [0.5, 0.5], (1,): [0.9, 0.1]},
            "R": {(0,): [0.8, 0.2], (1,): [0.2, 0.8]},
            "W": {(0, 0): [1.0, 0.0], (0, 1): [0.1, 0.9], (1, 0): [0.1, 0.9], (1, 1): [0.01, 0.99]},
        },
    }
