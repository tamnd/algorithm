# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/anti-entropy/. The authors are listed in prov/E24PC5.jsonl.

import math
import random

from anti_entropy import (Replica, converged, merkle_diff, one_round_residue, round_of_sessions,
                          session, spread_rounds)


def mean_rounds(n: int, mode: str, trials: int = 30) -> float:
    rng = random.Random(n * 7 + len(mode))
    return sum(spread_rounds(n, mode, rng) for _ in range(trials)) / trials


def test_merkle_diff_finds_exactly_the_differing_keys() -> None:
    for seed in range(100):
        rng = random.Random(seed)
        a, b = Replica(0, depth=rng.choice([0, 2, 4, 6])), Replica(1)
        b.depth = a.depth
        for i in range(rng.randrange(0, 150)):
            a.write(f"k{i}", rng.randrange(5), 1)
            b.data[f"k{i}"] = a.data[f"k{i}"]
        for _ in range(rng.randrange(0, 10)):
            k = f"k{rng.randrange(200)}"
            side = rng.choice([a, b])
            side.write(k, "new", rng.randrange(2, 9))
        b._tree = None
        keys = a.data.keys() | b.data.keys()
        expect = {k for k in keys if a.data.get(k) != b.data.get(k)}
        assert merkle_diff(a, b) == expect, seed
        assert merkle_diff(b, a) == expect, seed


def test_merkle_diff_compares_few_nodes_when_few_keys_differ() -> None:
    a, b = Replica(0, depth=8), Replica(1, depth=8)
    for i in range(2000):
        a.write(f"k{i}", i, 1)
        b.data[f"k{i}"] = a.data[f"k{i}"]
    b._tree = None
    stats: dict = {}
    assert merkle_diff(a, b, stats) == set() and stats["compared"] == 1
    a.write("k5", "changed", 2)
    stats = {}
    assert merkle_diff(a, b, stats) == {"k5"}
    assert stats["compared"] == 1 + 2 * 8  # one path to the leaf, and the siblings on it


def test_sessions_converge_to_the_last_writer_wins_state() -> None:
    for seed in range(20):
        rng = random.Random(seed)
        n = 16
        reps = [Replica(i) for i in range(n)]
        latest: dict = {}
        for t in range(1, 60):
            r = rng.choice(reps)
            k = f"k{rng.randrange(12)}"
            v = None if rng.random() < 0.2 else t  # None is a tombstone
            r.write(k, v, t)
            latest[k] = ((t, r.rid), v)
        rounds = 0
        while not converged(reps):
            round_of_sessions(reps, "push-pull", rng)
            rounds += 1
            assert rounds < 30, seed
        assert reps[0].data == latest, seed


def test_session_modes_move_data_in_the_stated_direction() -> None:
    p, q = Replica(0), Replica(1)
    p.write("x", 1, 5)
    q.write("y", 2, 5)
    session(p, q, "push")
    assert "x" in q.data and "y" not in p.data
    p, q = Replica(0), Replica(1)
    p.write("x", 1, 5)
    q.write("y", 2, 5)
    session(p, q, "pull")
    assert "y" in p.data and "x" not in q.data
    session(p, q, "push-pull")
    assert p.data == q.data


def test_push_takes_about_log2_n_plus_ln_n_rounds() -> None:
    for n in (128, 512):
        m = mean_rounds(n, "push")
        assert math.log2(n) + math.log(n) - 1 < m < math.log2(n) + math.log(n) + 3, (n, m)


def test_push_pull_rounds_grow_like_log_n() -> None:
    means = {n: mean_rounds(n, "push-pull") for n in (32, 128, 512)}
    assert means[32] < means[128] < means[512]
    for n, m in means.items():
        assert 1.0 < m / math.log(n) < 1.8, (n, m)
        assert m < mean_rounds(n, "push")


def test_one_round_residue_matches_the_recurrences() -> None:
    rng = random.Random(3)
    n, p = 4000, 0.3

    def avg(mode: str) -> float:
        return sum(one_round_residue(n, p, mode, rng) for _ in range(10)) / 10

    assert abs(avg("pull") - p * p) < 0.01  # p_{i+1} = p_i^2
    assert abs(avg("push") - p * math.exp(-(1 - p))) < 0.01  # p (1 - 1/n)^(n(1-p))
    assert abs(avg("push-pull") - p * p * math.exp(-(1 - p))) < 0.01
