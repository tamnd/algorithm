# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/berkeley-algorithm/. The authors are listed in prov/YCTSW0.jsonl.

import itertools
import random

from berkeley_algorithm import berkeley_round, largest_cluster


def fixed(d: float):
    return lambda rng: d


def test_page_example() -> None:
    res = berkeley_round([0.0, 25.0, -10.0, 5.0, 600.0], gamma=60.0, dmin=0.01, delay=fixed(0.01), rng=random.Random(0))
    assert {i: round(v, 9) for i, v in res["delta"].items()} == {0: 0.0, 1: 25.0, 2: -10.0, 3: 5.0, 4: 600.0}
    assert res["chosen"] == [0, 1, 2, 3]
    assert abs(res["avg"] - 5.0) < 1e-9
    corr = [round(res["corrections"][i], 9) for i in range(5)]
    assert corr == [5.0, -20.0, 15.0, 0.0, -595.0]
    assert all(abs(x - 5.0) < 1e-9 for x in res["new_offsets"])


def test_largest_cluster_against_brute_force() -> None:
    rng = random.Random(7)
    for _ in range(300):
        k = rng.randrange(1, 8)
        vals = {i: float(rng.randrange(0, 30)) for i in range(k)}
        gamma = float(rng.randrange(0, 10))
        best = max(
            len(s)
            for r in range(1, k + 1)
            for s in itertools.combinations(vals, r)
            if max(vals[i] for i in s) - min(vals[i] for i in s) <= gamma
        )
        got = largest_cluster(vals, gamma)
        assert len(got) == best
        assert max(vals[i] for i in got) - min(vals[i] for i in got) <= gamma


def test_skew_bound_after_round() -> None:
    dmin = 0.001
    for seed in range(200):
        rng = random.Random(seed)
        n = rng.randrange(2, 9)
        offsets = [rng.uniform(-0.5, 0.5) for _ in range(n)]
        res = berkeley_round(offsets, gamma=2.0, dmin=dmin, delay=lambda r: dmin + r.expovariate(200.0), rng=rng)
        err = {0: 0.0}
        for i in range(1, n):
            err[i] = res["rtt"][i] / 2 - dmin
            # The estimate error is at most RTT_i / 2 - dmin.
            assert abs(res["delta"][i] - (offsets[i] - offsets[0])) <= err[i] + 1e-12
        new = res["new_offsets"]
        for i in range(n):
            for j in range(n):
                assert abs(new[i] - new[j]) <= err[i] + err[j] + 1e-12


def test_outliers_do_not_move_the_average() -> None:
    for seed in range(100):
        rng = random.Random(500 + seed)
        good = [0.0] + [rng.uniform(-1, 1) for _ in range(5)]
        bad1 = good + [rng.choice([-1, 1]) * rng.uniform(50, 100) for _ in range(2)]
        bad2 = good + [rng.choice([-1, 1]) * rng.uniform(200, 900) for _ in range(2)]
        r1 = berkeley_round(bad1, gamma=3.0, dmin=0.0, delay=fixed(0.0), rng=random.Random(0))
        r2 = berkeley_round(bad2, gamma=3.0, dmin=0.0, delay=fixed(0.0), rng=random.Random(0))
        assert r1["chosen"] == r2["chosen"] == list(range(6))
        assert abs(r1["avg"] - r2["avg"]) < 1e-9
        # The outliers are pulled to the average too.
        assert max(r1["new_offsets"]) - min(r1["new_offsets"]) < 1e-9


def test_plain_average_is_pulled_by_an_outlier() -> None:
    res = berkeley_round([0.0, 1.0, -1.0, 1000.0], gamma=1e9, dmin=0.0, delay=fixed(0.0), rng=random.Random(0))
    assert abs(res["avg"] - 250.0) < 1e-9
