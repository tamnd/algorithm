# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/random-peer-sampling/. The authors are listed in prov/F8JAYE.jsonl.

import random

from random_peer_sampling import preferential_graph, sample, step_probabilities, total_variation, walk_law


def test_rows_are_distributions_and_mh_is_symmetric():
    adj = preferential_graph(60, 2, 1)
    rows = [step_probabilities(adj, i, "mh") for i in range(60)]
    for kind in ("srw", "mh"):
        for i in range(60):
            assert abs(sum(step_probabilities(adj, i, kind).values()) - 1) < 1e-12
    for i in range(60):
        for j, p in rows[i].items():
            assert abs(rows[j][i] - p) < 1e-12


def test_stationary_laws():
    adj = preferential_graph(60, 2, 1)
    n = len(adj)
    deg = [len(a) for a in adj]
    assert max(deg) >= 4 * min(deg)
    uniform = [1 / n] * n
    by_degree = [d / sum(deg) for d in deg]
    srw = walk_law(adj, 0, 2000, "srw")
    mh = walk_law(adj, 0, 2000, "mh")
    assert total_variation(srw, by_degree) < 1e-6
    assert total_variation(mh, uniform) < 1e-6
    assert total_variation(srw, uniform) > 0.15


def test_mh_samples_are_uniform():
    adj = preferential_graph(30, 2, 2)
    n = len(adj)
    rng = random.Random(3)
    runs = 6000
    counts = [0] * n
    for _ in range(runs):
        counts[sample(adj, 0, 200, "mh", rng)] += 1
    exp = runs / n
    chi2 = sum((c - exp) ** 2 / exp for c in counts)
    assert chi2 < 70          # 29 degrees of freedom; the 0.9999 quantile is about 66


def test_short_walks_are_biased_to_the_start():
    adj = preferential_graph(60, 2, 1)
    law = walk_law(adj, 0, 3, "mh")
    assert law[0] > 10 / 60
