# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/effect-cause-diagnosis/. The authors are listed in prov/4MRNNQ.jsonl.

import random

import pytest

from effect_cause_diagnosis import diagnose, fanin_cone
from td3net import Circuit, random_circuit


def page_circuit() -> Circuit:
    return Circuit(["a", "b", "c"], [("z", "AND", ["a", "b"]), ("y", "OR", ["b", "c"])], ["z", "y"])


TESTS = [(1, 1, 0), (0, 1, 0), (1, 0, 0), (0, 0, 1)]


def names(c, faults):
    return sorted(c.fault_name(f) for f in faults)


def brute_force(c, tests, responses):
    """Simulate every single stuck-at fault and keep those that reproduce the responses."""
    want = [tuple(r) for r in responses]
    return [f for f in c.faults() if [c.outputs(t, f) for t in tests] == want]


def test_page_example_y_stuck_at_0():
    c = page_circuit()
    seen = [c.outputs(t, (c.index["y"], 0)) for t in TESTS]
    kept, simulated = diagnose(c, TESTS, seen)
    assert names(c, kept) == ["y/0"]
    assert simulated == 1  # one candidate simulated instead of 14 faults


def test_page_example_z_stuck_at_0():
    c = page_circuit()
    seen = [c.outputs(t, (c.index["z"], 0)) for t in TESTS]
    kept, simulated = diagnose(c, TESTS, seen)
    assert names(c, kept) == ["a/0", "b>z/0", "z/0"]
    assert simulated == 4  # a/0, b/0, b>z/0, z/0; b/0 also fails y and is dropped


def test_cone():
    c = page_circuit()
    assert names(c, [(x, 0) for x in fanin_cone(c, c.index["y"])]) == ["b/0", "b>y/0", "c/0", "y/0"]


def test_edge_cases():
    c = page_circuit()
    good = [c.outputs(t) for t in TESTS]
    assert diagnose(c, TESTS, good) == ([], 0)
    assert diagnose(c, [], []) == ([], 0)
    with pytest.raises(ValueError):
        diagnose(c, TESTS, good[:2])
    # A response no single stuck-at fault gives: z fails on test 0 and y fails on test 3.
    odd = [(0, 1), (0, 1), (0, 0), (0, 0)]
    kept, _ = diagnose(c, TESTS, odd)
    assert kept == [] and brute_force(c, TESTS, odd) == []


def test_against_exhaustive_fault_simulation():
    rng = random.Random(41)
    cases = 0
    for _ in range(50):
        ni = rng.randint(2, 6)
        c = random_circuit(rng, ni, rng.randint(1, 10))
        tests = [tuple(rng.randint(0, 1) for _ in range(ni)) for _ in range(rng.randint(1, 8))]
        good = [c.outputs(t) for t in tests]
        raw = {g: [c.outputs(t, g) for t in tests] for g in c.faults()}
        for f in c.faults():
            seen = raw[f]
            kept, simulated = diagnose(c, tests, seen)
            if seen == good:
                assert (kept, simulated) == ([], 0)
                continue
            assert f in kept  # the true fault is never lost
            assert sorted(kept) == sorted(g for g in c.faults() if raw[g] == seen)
            assert simulated <= 2 * c.n_lines
            cases += 1
    assert cases >= 500


def test_random_responses_against_brute_force():
    # Arbitrary tester data, most of it not produced by any single fault.
    rng = random.Random(42)
    for _ in range(300):
        ni = rng.randint(2, 5)
        c = random_circuit(rng, ni, rng.randint(1, 8))
        tests = [tuple(rng.randint(0, 1) for _ in range(ni)) for _ in range(rng.randint(1, 5))]
        good = [c.outputs(t) for t in tests]
        seen = [tuple(v ^ (rng.random() < 0.2) for v in g) for g in good]
        kept, _ = diagnose(c, tests, seen)
        if seen == good:
            assert kept == []
        else:
            assert sorted(kept) == sorted(brute_force(c, tests, seen))
