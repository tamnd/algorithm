# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/variable-size-caching/. The authors are listed in prov/3V56B1.jsonl.

import random

import pytest

from variable_size_caching import (
    belady_rule_cost,
    belady_rule_trace,
    bit_costs,
    fault_costs,
    optimal_cost,
)

SIZE = {"a": 1, "b": 2, "c": 2}
TRACE = list("abcba")


def test_counterexample_fault_model() -> None:
    cost = fault_costs("abc")
    assert optimal_cost(TRACE, SIZE, cost, 3) == 4
    assert belady_rule_cost(TRACE, SIZE, cost, 3) == 5


def test_counterexample_bit_model() -> None:
    cost = bit_costs(SIZE)
    assert optimal_cost(TRACE, SIZE, cost, 3) == 7
    assert belady_rule_cost(TRACE, SIZE, cost, 3) == 8


def test_counterexample_steps() -> None:
    rows = belady_rule_trace(TRACE, SIZE, 3)
    assert [hit for _, hit, _, _ in rows] == [False, False, False, False, False]
    assert rows[2][2] == ["a", "b"]  # the request for c evicts a, then b
    assert rows[2][3] == ["c"]


def test_unit_sizes_and_costs_belady_is_optimal() -> None:
    rng = random.Random(7)
    for _ in range(300):
        items = "abcde"[: rng.randint(2, 5)]
        k = rng.randint(1, 3)
        trace = [rng.choice(items) for _ in range(rng.randint(1, 12))]
        size = {x: 1 for x in items}
        cost = fault_costs(items)
        assert optimal_cost(trace, size, cost, k) == belady_rule_cost(trace, size, cost, k)


def test_belady_never_beats_optimum() -> None:
    rng = random.Random(11)
    for _ in range(400):
        items = "abcd"[: rng.randint(2, 4)]
        cap = rng.randint(2, 5)
        size = {x: rng.randint(1, cap) for x in items}
        trace = [rng.choice(items) for _ in range(rng.randint(1, 9))]
        for cost in (fault_costs(items), bit_costs(size)):
            o = optimal_cost(trace, size, cost, cap)
            b = belady_rule_cost(trace, size, cost, cap)
            assert o <= b


def test_optional_model_is_never_worse() -> None:
    rng = random.Random(3)
    for _ in range(200):
        items = "abcd"
        cap = rng.randint(2, 4)
        size = {x: rng.randint(1, cap) for x in items}
        cost = {x: rng.randint(1, 5) for x in items}
        trace = [rng.choice(items) for _ in range(rng.randint(1, 8))]
        assert optimal_cost(trace, size, cost, cap, optional=True) <= optimal_cost(trace, size, cost, cap)


def test_optional_bypass_helps() -> None:
    # A large item requested once would push out two small items that come back.
    size = {"a": 1, "b": 1, "z": 2}
    cost = fault_costs("abz")
    trace = list("abzab")
    assert optimal_cost(trace, size, cost, 2) == 5
    assert optimal_cost(trace, size, cost, 2, optional=True) == 3


def test_rejects_items_larger_than_the_cache() -> None:
    with pytest.raises(ValueError):
        optimal_cost(["a"], {"a": 4}, {"a": 1}, 3)
