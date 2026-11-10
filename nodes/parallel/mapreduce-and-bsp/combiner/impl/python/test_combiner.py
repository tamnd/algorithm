# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/combiner/. The authors are listed in prov/1WW8S5.jsonl.

import random
from collections import defaultdict
from fractions import Fraction

from combiner import (count_reduce, identity_map, make_splits, mean_map_pairs, mean_of_means, mean_reduce,
                      mean_reduce_pairs, one_map, pair_sum_combiner, run_round, sum_reduce)


def random_records(rng, n, keys):
    return [(f"k{rng.randrange(keys)}", rng.randrange(-5, 50)) for _ in range(n)]


def by_key(records):
    groups = defaultdict(list)
    for k, v in records:
        groups[k].append(v)
    return groups


def test_page_example_mean_failure():
    assert Fraction(sum([1, 2, 3, 4, 5]), 5) == 3
    assert mean_of_means([[1, 2], [3, 4, 5]]) == Fraction(11, 4)
    recs = [("x", v) for v in [1, 2, 3, 4, 5]]
    splits = [recs[:2], recs[2:]]
    out, _ = run_round(splits, identity_map, mean_reduce, 1)
    assert out == {"x": 3}
    bad, _ = run_round(splits, identity_map, mean_reduce, 1, combiner=mean_reduce)
    assert bad == {"x": Fraction(11, 4)}
    good, sent = run_round(splits, mean_map_pairs, mean_reduce_pairs, 1, combiner=pair_sum_combiner)
    assert good == {"x": 3} and sent == 2


def test_sum_combiner_never_changes_output():
    rng = random.Random(1)
    for _ in range(300):
        recs = random_records(rng, rng.randrange(0, 40), rng.choice([1, 3, 10]))
        m, r = rng.randrange(1, 5), rng.randrange(1, 4)
        want = {k: sum(v) for k, v in by_key(recs).items()}
        plain, sent0 = run_round(make_splits(recs, m), identity_map, sum_reduce, r)
        comb, sent1 = run_round(make_splits(recs, m), identity_map, sum_reduce, r, combiner=sum_reduce, rng=rng)
        assert plain == comb == want
        assert sent1 <= sent0 == len(recs)


def test_mean_fix_never_changes_output_and_bad_combiner_fails_somewhere():
    rng = random.Random(2)
    failures = 0
    for _ in range(300):
        recs = random_records(rng, rng.randrange(1, 30), rng.choice([1, 2, 5]))
        m, r = rng.randrange(1, 5), rng.randrange(1, 3)
        want = {k: Fraction(sum(v), len(v)) for k, v in by_key(recs).items()}
        good, _ = run_round(make_splits(recs, m), mean_map_pairs, mean_reduce_pairs, r,
                            combiner=pair_sum_combiner, rng=rng)
        assert good == want
        bad, _ = run_round(make_splits(recs, m), identity_map, mean_reduce, r, combiner=mean_reduce, rng=rng)
        failures += bad != want
    assert failures > 50


def test_mapper_must_emit_the_combiner_type():
    # Mapper emits plain numbers, combiner emits (sum, count): wrong when the combiner does not run.
    recs = [("x", 4), ("x", 6)]
    try:
        run_round([recs], identity_map, mean_reduce_pairs, 1)
    except TypeError:
        pass
    else:
        raise AssertionError("the reducer must fail on values that are not pairs")


def test_count_reducer_is_not_a_combiner():
    recs = [("a", None)] * 3
    splits = [recs[:2], recs[2:]]
    out, _ = run_round(splits, one_map, count_reduce, 1)
    assert out == {"a": 3}
    bad, _ = run_round(splits, one_map, count_reduce, 1, combiner=count_reduce)
    assert bad == {"a": 2}
    good, sent = run_round(splits, one_map, sum_reduce, 1, combiner=sum_reduce)
    assert good == {"a": 3} and sent == 2


def test_empty_input_and_one_key():
    out, sent = run_round(make_splits([], 3), identity_map, sum_reduce, 2, combiner=sum_reduce)
    assert out == {} and sent == 0
    recs = [("only", 1)] * 50
    out, sent = run_round(make_splits(recs, 5), identity_map, sum_reduce, 3, combiner=sum_reduce)
    assert out == {"only": 50} and sent == 5
