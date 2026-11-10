# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dense-max-cut-ptas/. The authors are listed in prov/SEQDJG.jsonl.

import random
from fractions import Fraction
from math import sqrt

from dense_max_cut_ptas import cut_value, dense_max_cut, draw_samples, parameters, place, split


def random_graph(rng, n, p):
    adj = [set() for _ in range(n)]
    for u in range(n):
        for v in range(u + 1, n):
            if rng.random() < p:
                adj[u].add(v)
                adj[v].add(u)
    return adj


def brute_max_cut(adj):
    n = len(adj)
    best, arg = -1, None
    for mask in range(1 << max(n - 1, 0)):
        side = [mask >> v & 1 for v in range(n)]
        c = cut_value(adj, side)
        if c > best:
            best, arg = c, side
    return best, arg


EDGES = [(0, 1), (0, 2), (0, 5), (0, 6), (1, 3), (1, 4), (1, 7), (2, 3), (2, 4), (2, 7), (3, 5), (3, 6),
         (4, 5), (4, 6), (5, 7), (6, 7), (0, 3), (4, 7)]


def example_graph():
    adj = [set() for _ in range(8)]
    for u, v in EDGES:
        adj[u].add(v)
        adj[v].add(u)
    return adj


def hybrid(adj, parts, samples, opt_side):
    """Run the hybrid H_0 = OPT, H_j = H_(j-1) with V_j placed from samples labelled by H_(j-1).

    Return the labels, the cut values of H_0, ..., H_ell and the bounds of each step."""
    n = len(adj)
    h = list(opt_side)
    labels, values, bounds = [], [cut_value(adj, h)], []
    for j, part in enumerate(parts):
        inside = set(part)
        lab = [h[u] for u in samples[j]]
        labels.append(lab)
        big_n, t = n - len(part), len(samples[j])
        err = Fraction(0)
        for v in part:
            g = sum(1 if h[u] == 0 else -1 for u in adj[v] if u not in inside)
            a0 = sum(1 for u, s in zip(samples[j], lab) if u in adj[v] and s == 0)
            a1 = sum(1 for u, s in zip(samples[j], lab) if u in adj[v] and s == 1)
            err += abs(Fraction(big_n, t) * (a0 - a1) - g)
        inner = sum(1 for u in part for v in adj[u] if v in inside and u < v)
        new = place(adj, parts, samples, labels + [[0] * len(s) for s in samples[j + 1:]])
        for v in part:
            h[v] = new[v]
        values.append(cut_value(adj, h))
        bounds.append(err + inner)
    return labels, values, bounds


def test_example() -> None:
    adj = example_graph()
    opt, _ = brute_max_cut(adj)
    assert opt == 16
    st = {}
    side = dense_max_cut(adj, 2, 2, random.Random(0), st)
    assert st["guesses"] == 16 and st["parts"] == [[0, 1, 2, 3], [4, 5, 6, 7]]
    assert st["samples"] == [[7, 7], [0, 2]]
    assert side == [1, 0, 0, 1, 1, 0, 0, 1] and cut_value(adj, side) == 16
    # labels 7 -> 1, 0 -> 1, 2 -> 0 give this cut
    assert place(adj, st["parts"], st["samples"], [[1, 1], [1, 0]]) == side
    # a poor draw: no sample is adjacent to 1 or 2, and the ties put them on side 1
    st = {}
    side = dense_max_cut(adj, 2, 2, random.Random(4), st)
    assert st["samples"] == [[5, 6], [0, 3]] and cut_value(adj, side) == 8


def test_hybrid_steps() -> None:
    rng = random.Random(1996)
    for _ in range(40):
        n = rng.randint(4, 11)
        adj = random_graph(rng, n, rng.choice([0.5, 0.7, 0.9]))
        opt, opt_side = brute_max_cut(adj)
        for ell, t in ((2, 1), (2, 2), (2, 3), (3, 2)):
            parts = split(n, ell)
            samples = draw_samples(n, parts, t, rng)
            labels, values, bounds = hybrid(adj, parts, samples, opt_side)
            for j in range(ell):
                assert values[j + 1] >= values[j] - bounds[j]
            # the labelling of the hybrid is one of those tried, so the algorithm is at least as good
            side = place(adj, parts, samples, labels)
            assert cut_value(adj, side) == values[-1]


def test_expected_error() -> None:
    rng = random.Random(1999)
    for ell, t in ((2, 2), (2, 4), (3, 3)):
        total = Fraction(0)
        runs = 30
        n = 10
        for _ in range(runs):
            adj = random_graph(rng, n, 0.6)
            _, opt_side = brute_max_cut(adj)
            parts = split(n, ell)
            samples = draw_samples(n, parts, t, rng)
            _, _, bounds = hybrid(adj, parts, samples, opt_side)
            total += sum(bounds)
        assert total / runs <= n * n / sqrt(t) + Fraction(n * n, 2 * ell)


def test_algorithm_and_guess_count() -> None:
    rng = random.Random(1998)
    for _ in range(25):
        n = rng.randint(3, 10)
        adj = random_graph(rng, n, 0.7)
        opt, opt_side = brute_max_cut(adj)
        for ell, t in ((2, 3), (2, 2), (3, 2)):
            seed = rng.random()
            parts = split(n, ell)
            samples = draw_samples(n, parts, t, random.Random(seed))
            _, values, _ = hybrid(adj, parts, samples, opt_side)
            st = {}
            side = dense_max_cut(adj, ell, t, random.Random(seed), st)
            assert st["guesses"] == 2 ** (ell * t) and st["samples"] == samples
            # the best guess is at least as good as the hybrid H_ell, and no cut beats OPT
            assert values[-1] <= cut_value(adj, side) <= opt


def test_parameters_meet_the_bound() -> None:
    for eps in (0.5, 0.25, 0.1):
        for delta in (0.5, 0.25, 0.1):
            ell, t = parameters(eps, delta)
            # OPT >= m / 2 >= delta n^2 / 2, so this error is at most eps OPT
            assert 1 / sqrt(t) + 1 / (2 * ell) <= eps * delta / 2 + 1e-12
