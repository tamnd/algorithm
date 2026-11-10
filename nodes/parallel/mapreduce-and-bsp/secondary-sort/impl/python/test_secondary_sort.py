# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/secondary-sort/. The authors are listed in prov/1NTC06.jsonl.

import random
from collections import Counter, defaultdict
from fractions import Fraction

from secondary_sort import (emit_series, make_splits, natural_partitioner, relative_frequencies,
                            run_round, sensor_series_reducer_sort, sensor_series_secondary_sort,
                            value_to_key_map)


def random_readings(rng, n, sensors):
    times = rng.sample(range(10 * n + 10), n)
    return [(f"s{rng.randrange(sensors)}", t, rng.randrange(100)) for t in times]


def truth(readings):
    by = defaultdict(list)
    for s, t, x in readings:
        by[s].append((t, x))
    return {s: [x for _, x in sorted(v)] for s, v in by.items()}


def test_page_example():
    readings = [("m1", 3, 30), ("m2", 1, 11), ("m1", 1, 10), ("m1", 2, 20), ("m2", 2, 12)]
    assert sensor_series_secondary_sort(readings, 2, 2) == {"m1": [10, 20, 30], "m2": [11, 12]}


def test_matches_in_memory_sort_on_seeded_inputs():
    rng = random.Random(4)
    for _ in range(200):
        readings = random_readings(rng, rng.randrange(0, 40), rng.choice([1, 2, 6]))
        m, r = rng.randrange(1, 5), rng.randrange(1, 5)
        want = truth(readings)
        assert sensor_series_secondary_sort(readings, m, r, rng=rng) == want
        assert sensor_series_reducer_sort(readings, m, r, rng=rng) == want


def test_one_reduce_call_per_natural_key():
    rng = random.Random(5)
    readings = random_readings(rng, 60, 7)
    outputs, calls = run_round(make_splits(readings, 3), value_to_key_map, emit_series, 4,
                               partitioner=natural_partitioner, group_key=lambda k: k[0])
    assert sum(calls) == len({s for s, _, _ in readings})


def test_pitfalls_full_key_partitioner_or_grouping_splits_groups():
    readings = [("m1", t, t) for t in range(20)]
    # Grouping on the whole composite key: one reduce call per reading.
    _, calls = run_round([readings], value_to_key_map, emit_series, 2, partitioner=natural_partitioner)
    assert sum(calls) == 20
    # Partitioning on the whole composite key: the sensor is spread over both reducers.
    outputs, calls = run_round([readings], value_to_key_map, emit_series, 2, group_key=lambda k: k[0])
    assert sum(calls) == 2 and all(calls)
    assert sorted(len(series) for out in outputs for _, series in out) != [20]


def test_order_inversion_relative_frequencies():
    rng = random.Random(6)
    for _ in range(100):
        docs = [(d, " ".join(rng.choice("abcd") for _ in range(rng.randrange(0, 8)))) for d in range(rng.randrange(0, 6))]
        pairs, marg = Counter(), Counter()
        for _, t in docs:
            ws = t.split()
            for i, w in enumerate(ws):
                for j in (i - 1, i + 1):
                    if 0 <= j < len(ws):
                        pairs[(w, ws[j])] += 1
                        marg[w] += 1
        want = {k: Fraction(c, marg[k[0]]) for k, c in pairs.items()}
        assert relative_frequencies(docs, rng.randrange(1, 4), rng.randrange(1, 4), rng=rng) == want
