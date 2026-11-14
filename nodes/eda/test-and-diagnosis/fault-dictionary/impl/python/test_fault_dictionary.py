# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fault-dictionary/. The authors are listed in prov/4SH7E3.jsonl.

import random

import pytest

from fault_dictionary import FaultDictionary
from td3net import Circuit, random_circuit


def page_circuit() -> Circuit:
    # z = a AND b, y = b OR c; b feeds both gates, so it has two branch lines.
    return Circuit(["a", "b", "c"], [("z", "AND", ["a", "b"]), ("y", "OR", ["b", "c"])], ["z", "y"])


PAGE_TESTS = [(1, 1, 0), (0, 1, 0), (1, 0, 0), (0, 0, 1)]


def names(c, faults):
    return sorted(c.fault_name(f) for f in faults)


def test_page_example():
    c = page_circuit()
    d = FaultDictionary(c, PAGE_TESTS).build()
    assert d.check_invariant()
    assert d.size_bits_full() == 14 * 4 * 2 == 112
    assert d.size_bits_pass_fail() == 14 * 4 == 56
    assert d.classes_full() == 10
    assert d.classes_pass_fail() == 7
    # The tester sees z = 0 on test 0 and nothing else: an equivalence class of three faults.
    seen = [(0, 1), (0, 1), (0, 0), (0, 1)]
    assert names(c, d.lookup_full(d.observe(seen))) == ["a/0", "b>z/0", "z/0"]
    # b/0 and b>y/0 fail the same tests but on different outputs.
    obs = d.response[(c.index["b"], 0)]
    assert names(c, d.lookup_full(obs)) == ["b/0"]
    assert names(c, d.lookup_pass_fail(obs)) == ["b/0", "b>y/0"]
    # Only test 2 fails: five faults in the pass-fail dictionary, split three ways by the full one.
    obs = d.response[(c.index["c"], 1)]
    assert names(c, d.lookup_pass_fail(obs)) == ["b/1", "b>y/1", "b>z/1", "c/1", "y/1"]
    assert names(c, d.lookup_full(obs)) == ["b>y/1", "c/1", "y/1"]


def test_unknown_response_and_nearest():
    c = page_circuit()
    d = FaultDictionary(c, PAGE_TESTS).build()
    # z fails on test 0 and y fails on test 3: no single stuck-at fault does this.
    obs = (1, 0, 0, 2)
    assert d.lookup_full(obs) == []
    dist, near = d.nearest(obs)
    assert dist == 1
    assert names(c, near) == ["a/0", "b>z/0", "c/0", "z/0"]


def test_edge_cases():
    c = page_circuit()
    d = FaultDictionary(c, []).build()
    assert d.classes_full() == 1 and d.size_bits_full() == 0
    assert len(d.lookup_full(())) == 14
    d = FaultDictionary(c, PAGE_TESTS)
    assert d.lookup_full((0, 0, 0, 0)) == [] and d.nearest((0, 0, 0, 0)) == (0, [])
    d.add_fault((0, 0))
    d.add_fault((0, 0))
    assert d.check_invariant() and len(d.response) == 1
    with pytest.raises(ValueError):
        d.observe([(0, 0)])


def brute_candidates(c, tests, raw, true_fault):
    """Every fault whose output vectors equal those of the true fault, by plain simulation."""
    return {g for g in c.faults() if raw[g] == raw[true_fault]}


def test_against_exhaustive_fault_simulation():
    rng = random.Random(31)
    cases = 0
    total_full = total_pf = 0
    for _ in range(80):
        ni = rng.randint(2, 6)
        c = random_circuit(rng, ni, rng.randint(1, 12))
        tests = [tuple(rng.randint(0, 1) for _ in range(ni)) for _ in range(rng.randint(1, 10))]
        d = FaultDictionary(c, tests).build()
        assert d.check_invariant()
        assert d.size_bits_full() == len(c.faults()) * len(tests) * len(c.po)
        assert d.size_bits_pass_fail() == len(c.faults()) * len(tests)
        assert d.classes_pass_fail() <= d.classes_full()
        raw = {g: tuple(c.outputs(t, g) for t in tests) for g in c.faults()}
        for f in c.faults():
            seen = [c.outputs(t, f) for t in tests]  # the tester data of a chip with fault f
            obs = d.observe(seen)
            full = set(d.lookup_full(obs))
            pf = set(d.lookup_pass_fail(obs))
            assert f in full
            assert full == brute_candidates(c, tests, raw, f)
            assert full <= pf
            assert d.nearest(obs) == (0, d.lookup_full(obs))
            cases += 1
            total_full += len(full)
            total_pf += len(pf)
    assert cases >= 500
    assert total_full <= total_pf


def test_random_operation_sequences_against_model():
    # Faults added in random order, with repeats; after each step every lookup agrees with a plain dict.
    rng = random.Random(21)
    for _ in range(40):
        ni = rng.randint(2, 5)
        c = random_circuit(rng, ni, rng.randint(1, 8))
        tests = [tuple(rng.randint(0, 1) for _ in range(ni)) for _ in range(rng.randint(1, 6))]
        good = [c.outputs(t) for t in tests]
        d = FaultDictionary(c, tests)
        model = {}
        for _ in range(30):
            f = rng.choice(c.faults())
            d.add_fault(f)
            model[f] = tuple(sum(1 << k for k, (a, b) in enumerate(zip(g, c.outputs(t, f))) if a != b) for t, g in zip(tests, good))
            assert d.check_invariant()
            probe = model[rng.choice(list(model))]
            assert sorted(d.lookup_full(probe)) == sorted(g for g, r in model.items() if r == probe)
            fails = [bool(w) for w in probe]
            assert sorted(d.lookup_pass_fail(probe)) == sorted(g for g, r in model.items() if [bool(w) for w in r] == fails)
        assert d.size_bits_full() == len(model) * len(tests) * len(c.po)


def test_noisy_observation_nearest_contains_true_fault_within_distance():
    # One flipped tester bit: the true fault is at distance 1, so the nearest distance is at most 1.
    rng = random.Random(12)
    for _ in range(100):
        ni = rng.randint(2, 5)
        c = random_circuit(rng, ni, rng.randint(2, 8))
        tests = [tuple(rng.randint(0, 1) for _ in range(ni)) for _ in range(rng.randint(2, 6))]
        d = FaultDictionary(c, tests).build()
        f = rng.choice(c.faults())
        obs = list(d.response[f])
        j = rng.randrange(len(tests))
        obs[j] ^= 1 << rng.randrange(len(c.po))
        dist, near = d.nearest(tuple(obs))
        assert dist <= 1
        if dist == 1:
            assert f in near
