# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/truthfinder/. The authors are listed in prov/HNKC9H.jsonl.
"""TruthFinder (Yin, Han and Yu): iterate between source trust and fact confidence.

A claim is a triple (source, object, value). A fact is a pair (object, value).
imp(obj, v1, v2) is the implication from the fact (obj, v1) to the fact
(obj, v2), a number in [-1, 1]; the default is 0 for every pair, which gives
the plain version without similar facts. The defaults rho = 0.5, gamma = 0.3,
t0 = 0.9 and delta = 1e-5 (0.001%) are the values that the paper uses.
"""

import math


def facts_of(claims):
    """Return (sources, facts, providers of each fact, facts of each source)."""
    providers = {}
    by_source = {}
    for w, o, v in claims:
        f = (o, v)
        providers.setdefault(f, set()).add(w)
        by_source.setdefault(w, set()).add(f)
    sources = sorted(by_source, key=repr)
    facts = sorted(providers, key=repr)
    return sources, facts, providers, by_source


def cosine(a, b):
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    if na == 0 or nb == 0:
        return 1.0
    return sum(x * y for x, y in zip(a, b)) / (na * nb)


def no_implication(obj, v1, v2):
    return 0.0


def exclusive_implication(base_sim=0.5):
    """imp = sim - base_sim with sim = 0 for two different values: each value counts against the others."""

    def imp(obj, v1, v2):
        return (1.0 if v1 == v2 else 0.0) - base_sim

    return imp


def truthfinder(claims, imp=no_implication, t0=0.9, rho=0.5, gamma=0.3, delta=1e-5, max_iter=100):
    """Return (confidence of each fact, trust of each source, number of iterations)."""
    sources, facts, providers, by_source = facts_of(claims)
    same_object = {}
    for o, v in facts:
        same_object.setdefault(o, []).append(v)
    t = {w: t0 for w in sources}  # @line L1
    s = {}
    it = 0
    while True:  # @line L2
        it += 1
        tau = {w: -math.log(max(1e-300, 1.0 - t[w])) for w in sources}  # @line L3
        sigma = {f: sum(tau[w] for w in providers[f]) for f in facts}  # @line L4
        sigma_star = {}
        for o, v in facts:  # @line L5
            adj = sum(sigma[(o, u)] * imp(o, u, v) for u in same_object[o] if u != v)  # @line L5
            sigma_star[(o, v)] = sigma[(o, v)] + rho * adj  # @line L5
        s = {f: 1.0 / (1.0 + math.exp(-gamma * sigma_star[f])) for f in facts}  # @line L6
        old = [t[w] for w in sources]  # @line L7
        t = {w: sum(s[f] for f in by_source[w]) / len(by_source[w]) for w in sources}  # @line L7
        new = [t[w] for w in sources]
        if 1.0 - cosine(old, new) < delta or it >= max_iter:  # @line L8
            break
    return s, t, it


def answers(confidence):
    """For each object, the value with the largest confidence (ties go to the smallest repr)."""
    best = {}
    for (o, v), c in sorted(confidence.items(), key=lambda kv: repr(kv[0])):  # @line L9
        if o not in best or c > best[o][1]:  # @line L9
            best[o] = (v, c)  # @line L9
    return {o: v for o, (v, c) in best.items()}


def voting(claims):
    """The baseline: for each object, the value that most sources claim."""
    count = {}
    for w, o, v in set(claims):
        count[(o, v)] = count.get((o, v), 0) + 1
    return answers({f: float(c) for f, c in count.items()})
