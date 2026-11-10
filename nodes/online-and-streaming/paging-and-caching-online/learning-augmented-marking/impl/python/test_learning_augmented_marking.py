# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/learning-augmented-marking/. The authors are listed in prov/9E8GB1.jsonl.

import random
from fractions import Fraction

from learning_augmented_marking import harmonic, next_arrivals, prediction_error, predictive_marker


def belady_misses(requests, k):
    cache, misses = set(), 0
    nxt = next_arrivals(requests)
    when = {}
    for t, x in enumerate(requests):
        when[x] = nxt[t]
        if x in cache:
            continue
        misses += 1
        if len(cache) == k:
            cache.remove(max(sorted(cache), key=lambda p: when[p]))
        cache.add(x)
    return misses


def phases(requests, k):
    """The k-phase partition, computed from the sequence alone: phase[i] for each request."""
    out, cur, r = [], set(), 1
    for x in requests:
        if x not in cur and len(cur) == k:
            cur, r = set(), r + 1
        cur.add(x)
        out.append(r)
    return out


def random_case(rng):
    k = rng.randint(1, 6)
    u = rng.randint(1, 3 * k + 1)
    seq = [rng.randrange(u) for _ in range(rng.randint(0, 120))]
    return k, seq


def test_example() -> None:
    seq = list("abcdeabcab")
    y = next_arrivals(seq)
    assert y == [5, 6, 7, 10, 10, 8, 9, 10, 10, 10]
    misses, log = predictive_marker(seq, 4, y)
    assert misses == 5 == belady_misses(seq, 4)
    assert [e["evict"] for e in log if e["evict"] is not None] == ["d"]
    wrong = list(y)
    wrong[3] = 5  # predict that d comes back at time 5, not never
    assert prediction_error(seq, wrong) == 5
    misses, log = predictive_marker(seq, 4, wrong)
    assert misses == 6
    assert [(e["page"], e["kind"], e["evict"], e["how"]) for e in log if e["evict"] is not None] == [
        ("e", "clean", "c", "pred"),
        ("c", "stale", "d", "pred"),
    ]
    assert harmonic(4) == Fraction(25, 12)


def test_marking_and_k_bound() -> None:
    rng = random.Random(2018)
    for _ in range(300):
        k, seq = random_case(rng)
        preds = [rng.randint(0, len(seq) + 3) for _ in seq]
        misses, log = predictive_marker(seq, k, preds, random.Random(rng.random()))
        ph = phases(seq, k)
        assert [e["phase"] for e in log] == ph
        for i, e in enumerate(log):
            if e["evict"] is not None:
                # Never evict a page that was requested before in the same phase (a marked page).
                assert all(not (seq[j] == e["evict"] and ph[j] == ph[i]) for j in range(i))
        n_phases = ph[-1] if ph else 0
        assert misses <= k * n_phases
        assert misses <= k * belady_misses(seq, k)


def test_phase_cost_is_sum_of_chains() -> None:
    rng = random.Random(5)
    for _ in range(300):
        k, seq = random_case(rng)
        preds = [rng.randint(0, len(seq)) for _ in seq]
        _, log = predictive_marker(seq, k, preds, random.Random(rng.random()))
        hk = harmonic(k)
        for r in set(e["phase"] for e in log):
            evs = [e for e in log if e["phase"] == r and e["evict"] is not None]
            chains = {}
            for e in evs:
                chains[e["chain"]] = chains.get(e["chain"], 0) + 1
                # A random eviction happens only after the chain is longer than H_k.
                assert (e["how"] == "random") == (chains[e["chain"]] > hk)
                assert (e["kind"] == "clean") == (chains[e["chain"]] == 1)
            clean = sum(1 for e in evs if e["kind"] == "clean")
            assert len(chains) == clean


def test_perfect_predictions_are_2_competitive() -> None:
    rng = random.Random(11)
    for _ in range(400):
        k, seq = random_case(rng)
        y = next_arrivals(seq)
        misses, log = predictive_marker(seq, k, y)
        assert all(e["kind"] != "stale" for e in log)
        assert all(e["how"] in (None, "pred") for e in log)
        assert misses <= 2 * belady_misses(seq, k)


def test_bad_predictions_stay_bounded() -> None:
    # Reversed predictions: the page that comes back soonest looks the farthest.
    rng = random.Random(3)
    for _ in range(40):
        k, seq = random_case(rng)
        n = len(seq)
        bad = [n - t for t in next_arrivals(seq)]
        opt = belady_misses(seq, k)
        runs = [predictive_marker(seq, k, bad, random.Random(s))[0] for s in range(50)]
        assert max(runs) <= k * opt
        assert sum(runs) / len(runs) <= 4 * float(harmonic(k)) * opt


def follow_predictions(requests, k, predictions):
    """Evict the page with the largest prediction, with no marking. Not robust."""
    cache, pred, misses = {}, {}, 0
    for i, x in enumerate(requests):
        pred[x] = predictions[i]
        if x in cache:
            continue
        misses += 1
        if len(cache) == k:
            del cache[max(cache, key=lambda p: pred[p])]
        cache[x] = None
    return misses


def test_blind_following_is_not_robust() -> None:
    for m in (10, 100):
        seq = ["a", "b", "c"] + ["a", "b"] * m
        n = len(seq)
        preds = [0 if x == "c" else n + 1 for x in seq]
        assert follow_predictions(seq, 2, preds) == n
        assert belady_misses(seq, 2) == 4
        assert predictive_marker(seq, 2, preds)[0] == 6


def test_edges() -> None:
    assert predictive_marker([], 2, []) == (0, [])
    assert predictive_marker([7, 7, 7], 1, [1, 2, 3])[0] == 1
    assert predictive_marker([1, 2, 1, 2], 1, [2, 3, 4, 4])[0] == 4
    for bad in (([1], 0, [0]), ([1, 2], 2, [0])):
        try:
            predictive_marker(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("bad input must be rejected")
