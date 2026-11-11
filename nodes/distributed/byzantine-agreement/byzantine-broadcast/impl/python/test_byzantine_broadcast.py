# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/byzantine-broadcast/. The authors are listed in prov/NQ3YET.jsonl.

from itertools import combinations, product

from byzantine_broadcast import (
    STRATEGIES,
    VALUES,
    agreement,
    broadcast_from_consensus,
    broadcast_from_ic,
    consensus_from_ic,
    ic_ok,
    interactive_consistency,
    strong_validity,
    weak_consensus,
    weak_validity,
)


def sets(n: int, k: int):
    for size in range(k + 1):
        yield from (frozenset(c) for c in combinations(range(n), size))


def test_ic_from_n_broadcasts() -> None:
    for n in (3, 4, 5):
        t = n - 2
        for faulty in sets(n, t):
            for name, strategy in STRATEGIES.items():
                for seed in range(2 if name == "random" else 1):
                    inputs = {p: VALUES[(3 * p + seed) % 3] for p in range(n)}
                    res = interactive_consistency(n, t, inputs, faulty, strategy, seed)
                    assert ic_ok(res, inputs, faulty), (n, faulty, name)
                    assert res["rounds"] == t + 1


def test_broadcast_from_ic() -> None:
    n, t = 4, 2
    for faulty in sets(n, t):
        for name, strategy in STRATEGIES.items():
            for value in VALUES:
                dec = broadcast_from_ic(n, t, 0, value, faulty, strategy)
                assert agreement(dec)
                if 0 not in faulty:
                    assert set(dec.values()) == {value}


def test_consensus_from_ic_needs_n_greater_than_2t() -> None:
    n, t = 5, 2
    for faulty in sets(n, t):
        for name, strategy in STRATEGIES.items():
            for bits in product((0, 1), repeat=n):
                inputs = dict(enumerate(bits))
                dec = consensus_from_ic(n, t, inputs, faulty, strategy)
                assert agreement(dec)
                assert strong_validity(dec, inputs, faulty), (faulty, name, bits)
    # n = 4, t = 2: the correct processes have input 1, the faulty ones 0
    inputs = {0: 0, 1: 0, 2: 1, 3: 1}
    dec = consensus_from_ic(4, 2, inputs, frozenset({0, 1}))
    assert dec == {2: 0, 3: 0}
    assert not strong_validity(dec, inputs, frozenset({0, 1}))


def test_broadcast_from_consensus() -> None:
    n, t = 5, 2
    for faulty in sets(n, t):
        for value in (1, 2):
            sent = {q: VALUES[q % 3] for q in range(n)}
            for name, strategy in STRATEGIES.items():
                dec = broadcast_from_consensus(n, t, value, faulty, sent, strategy)
                assert agreement(dec)
                if 0 not in faulty:
                    assert set(dec.values()) == {value}


def test_separation_of_strong_and_weak_validity() -> None:
    # n = 4, t = 1: process 0 is faulty with input 1, all correct inputs are 0.
    inputs, faulty = {0: 1, 1: 0, 2: 0, 3: 0}, frozenset({0})
    weak = weak_consensus(4, 1, inputs, faulty)
    assert weak == {1: 1, 2: 1, 3: 1}
    assert weak_validity(weak, inputs, faulty)
    assert not strong_validity(weak, inputs, faulty)
    strong = consensus_from_ic(4, 1, inputs, faulty)
    assert strong == {1: 0, 2: 0, 3: 0}
    assert strong_validity(strong, inputs, faulty)


def test_weak_consensus_any_t() -> None:
    n = 4
    for faulty in sets(n, n - 1):
        for bits in product((0, 1), repeat=n):
            inputs = dict(enumerate(bits))
            for name, strategy in STRATEGIES.items():
                dec = weak_consensus(n, n - 1, inputs, faulty, strategy)
                assert agreement(dec) and weak_validity(dec, inputs, faulty)
