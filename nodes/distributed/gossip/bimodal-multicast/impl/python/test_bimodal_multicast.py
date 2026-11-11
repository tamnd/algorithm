# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bimodal-multicast/. The authors are listed in prov/A2XR3K.jsonl.

import math
import random

from bimodal_multicast import delivery_distribution, delivery_sample, latency_recurrence, pbcast


def test_no_loss_needs_no_repair() -> None:
    counts, retrans = pbcast(30, 10, random.Random(0))
    assert counts == [30] * 10 and retrans == 0


def test_anti_entropy_repairs_heavy_loss() -> None:
    # 20% loss on every packet, and one multicast that reaches nobody.
    for seed in range(3):
        counts, retrans = pbcast(50, 20, random.Random(seed), loss=0.2, multicast_fails=frozenset({3}))
        assert counts == [50] * 20
        assert retrans < 50 * 20


def test_short_buffers_give_almost_all_or_almost_none() -> None:
    counts, _ = pbcast(100, 30, random.Random(2), loss=0.2, keep=3, limit=1, multicast_fails=frozenset({0}))
    assert counts[0] < 10
    assert sum(c >= 85 for c in counts[1:]) >= 27


def test_deterministic() -> None:
    assert pbcast(40, 8, random.Random(9), loss=0.1) == pbcast(40, 8, random.Random(9), loss=0.1)


def test_distribution_is_bimodal() -> None:
    n = 50
    d = delivery_distribution(n, 5, 0.05, 12)
    assert abs(sum(d) - 1) < 1e-9 and d[0] == 0
    low, mid, high = sum(d[:6]), sum(d[6:45]), sum(d[45:])
    assert high > 0.99 and 1e-3 < low < 0.01 and mid < 1e-4
    # Nobody hears the sender: about exp(-fanout (1 - eps)).
    assert abs(d[1] - (1 - 5 / n * 0.95) ** (n - 1)) < 1e-12
    # The curve falls from both ends to a deep minimum in the middle.
    assert min(d[10:40]) < 1e-12


def test_more_fanout_moves_mass_to_the_top() -> None:
    tops = [sum(delivery_distribution(40, f, 0.05, 10)[36:]) for f in (2, 3, 5)]
    assert tops[0] < tops[1] < tops[2]


def test_distribution_matches_simulation() -> None:
    n, fanout, eps, rounds = 50, 3, 0.05, 12
    d = delivery_distribution(n, fanout, eps, rounds)
    runs = [delivery_sample(n, fanout, eps, rounds, random.Random(s)) for s in range(400)]
    assert abs(sum(runs) / 400 - sum(k * d[k] for k in range(n + 1))) < 1.5
    assert abs(sum(x <= 5 for x in runs) / 400 - sum(d[:6])) < 0.04


def test_latency_peak_near_log_of_n() -> None:
    n = 1000
    w = latency_recurrence(n, 1, 0.05, 0.001, 40)
    peak = 1 + max(range(40), key=lambda t: w[t])
    assert abs(peak - math.log(n, 1.95)) <= 2
    assert abs(sum(w) - 1) < 0.02
