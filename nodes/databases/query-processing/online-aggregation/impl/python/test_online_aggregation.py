# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/online-aggregation/. The authors are listed in prov/NT88SJ.jsonl.

import itertools
import random
from fractions import Fraction

from online_aggregation import online_aggregate

G = lambda t: t[0]
X = lambda t: t[1]
T_EX = [("a", 4), ("b", 10), ("a", 6), ("a", 2), ("b", 14), ("a", 8), ("b", 12), ("a", 5), ("a", 7), ("b", 8)]


def exact(rows):
    out = {}
    for g, x in rows:
        c, s = out.get(g, (0, 0))
        out[g] = (c + 1, s + x)
    return {g: {"count": c, "sum": s, "avg": Fraction(s, c)} for g, (c, s) in out.items()}


def test_example() -> None:
    snaps = online_aggregate(T_EX, G, X, every=2, rng=random.Random(1), bounds=(0, 20))
    assert [i for i, _ in snaps] == [2, 4, 6, 8, 10]
    assert [e["a"]["avg"] for _, e in snaps] == [7, 6, Fraction(11, 2), Fraction(26, 5), Fraction(16, 3)]
    assert [e["b"]["avg"] for _, e in snaps] == [12, 10, 10, Fraction(34, 3), 11]
    assert [e["b"]["sum"] for _, e in snaps] == [60, 50, Fraction(100, 3), Fraction(85, 2), 44]
    last = snaps[-1][1]
    assert last["b"]["half_clt"] == 0.0 and last["b"]["half_hoeffding"] == 0.0


def test_exact_at_the_end() -> None:
    rng = random.Random(4)
    for trial in range(40):
        rows = [(rng.randrange(rng.choice([1, 3, 5])), rng.randrange(-5, 50)) for _ in range(rng.randrange(1, 120))]
        i, est = online_aggregate(rows, G, X, every=7, rng=random.Random(trial))[-1]
        assert i == len(rows)
        want = exact(rows)
        assert est.keys() == want.keys()
        for g in want:
            assert {k: est[g][k] for k in ("count", "sum", "avg")} == want[g]


def test_unbiased_over_all_orders() -> None:
    rows = [("a", 4), ("b", 10), ("a", 6), ("a", 2), ("b", 14), ("a", 9), ("c", 1)]
    want = exact(rows)
    n = len(rows)
    sums = {(i, g): Fraction(0) for i in range(1, n + 1) for g in want}
    counts = dict(sums)
    avg_sum = dict(sums)
    avg_n = {k: 0 for k in sums}
    orders = 0
    for perm in itertools.permutations(rows):
        orders += 1
        for i, est in online_aggregate(list(perm), G, X):
            for g in want:
                e = est.get(g)
                if e is not None:
                    sums[i, g] += e["sum"]
                    counts[i, g] += e["count"]
                    avg_sum[i, g] += e["avg"]
                    avg_n[i, g] += 1
    for (i, g), total in sums.items():
        assert total / orders == want[g]["sum"]
        assert counts[i, g] / orders == want[g]["count"]
        # AVG is unbiased given that the group has been seen.
        assert avg_sum[i, g] / avg_n[i, g] == want[g]["avg"]


def test_interval_coverage() -> None:
    rng = random.Random(9)
    rows = [(rng.randrange(3), rng.randrange(0, 100)) for _ in range(200)]
    mu = {g: e["avg"] for g, e in exact(rows).items()}
    for at in (50, 100):
        clt = hoeff = total = 0
        for t in range(150):
            i, est = online_aggregate(rows, G, X, every=at, rng=random.Random(t), bounds=(0, 99))[0]
            assert i == at
            for g, e in est.items():
                err = abs(e["avg"] - mu[g])
                total += 1
                clt += err <= e["half_clt"]
                hoeff += err <= e["half_hoeffding"]
        assert hoeff >= 0.95 * total
        assert clt >= 0.85 * total
