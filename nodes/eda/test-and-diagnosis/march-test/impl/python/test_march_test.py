# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/march-test/. The authors are listed in prov/G5W6E7.jsonl.
"""March tests against exhaustive fault injection in a small memory."""

from __future__ import annotations

import random

import pytest

from march_test import (
    ANY,
    DOWN,
    MARCH_C_MINUS,
    MATS,
    MATS_PLUS,
    MATS_PLUS_PLUS,
    UP,
    GoodMemory,
    addresses,
    consistent,
    operation_count,
    parse,
    run_march,
    show,
)
from ram_faults import FaultyMemory, all_faults, initial_states


def detected(test, fault, n) -> bool:
    """A fault counts as detected when the test fails from every initial content."""
    return all(run_march(FaultyMemory(n, fault, s), test, n) is not None for s in initial_states(n))


class CountingMemory(GoodMemory):
    def __init__(self, n):
        super().__init__(n)
        self.ops = 0

    def read(self, address):
        self.ops += 1
        return super().read(address)

    def write(self, address, value):
        self.ops += 1
        super().write(address, value)


def read_trace(memory, test, n):
    """Reference run: every value read, without stopping at a mismatch."""
    out = []
    for order, ops in test:
        for a in addresses(order, n):
            for kind, v in ops:
                if kind == "w":
                    memory.write(a, v)
                else:
                    out.append(memory.read(a))
    return out


def expected_trace(test, n):
    out = []
    for _, ops in test:
        for _ in range(n):
            for kind, v in ops:
                if kind == "r":
                    out.append(v)
    return out


def random_test(rng):
    test = [(ANY, (("w", rng.randint(0, 1)),))]
    for _ in range(rng.randint(1, 4)):
        ops = tuple((rng.choice("rw"), rng.randint(0, 1)) for _ in range(rng.randint(1, 3)))
        test.append((rng.choice([UP, DOWN, ANY]), ops))
    return test


def test_parse_and_show():
    assert show(MARCH_C_MINUS) == "any(w0); up(r0,w1); up(r1,w0); down(r0,w1); down(r1,w0); any(r0)"
    assert parse(show(MATS_PLUS)) == MATS_PLUS
    with pytest.raises(ValueError):
        parse("up(r2)")


@pytest.mark.parametrize("n", range(1, 9))
def test_operation_counts(n):
    assert operation_count(MARCH_C_MINUS, n) == 10 * n
    assert operation_count(MATS_PLUS, n) == 5 * n
    assert operation_count(MATS_PLUS_PLUS, n) == 6 * n
    for test in (MATS, MATS_PLUS, MATS_PLUS_PLUS, MARCH_C_MINUS):
        m = CountingMemory(n)
        assert run_march(m, test, n) is None
        assert m.ops == operation_count(test, n)


def test_standard_tests_are_consistent():
    for test in (MATS, MATS_PLUS, MATS_PLUS_PLUS, MARCH_C_MINUS):
        assert consistent(test)


@pytest.mark.parametrize("seed", range(40))
def test_consistent_iff_good_memory_always_passes(seed):
    rng = random.Random(seed)
    test = random_test(rng)
    if rng.random() < 0.3:
        test = test[1:]  # may read before any write
    n = 3
    passes = all(run_march(GoodMemory(n, s), test, n) is None for s in initial_states(n))
    assert passes == consistent(test)


@pytest.mark.parametrize("seed", range(25))
def test_runner_matches_reference_trace(seed):
    rng = random.Random(100 + seed)
    test = random_test(rng)
    n = 3
    expect = expected_trace(test, n)
    for faults in all_faults(n).values():
        for f in faults:
            for s in initial_states(n):
                fails = run_march(FaultyMemory(n, f, s), test, n) is not None
                assert fails == (read_trace(FaultyMemory(n, f, s), test, n) != expect)


@pytest.mark.parametrize("n", [2, 3, 4, 5])
def test_march_c_minus_detects_every_fault(n):
    for cls, faults in all_faults(n).items():
        for f in faults:
            assert detected(MARCH_C_MINUS, f, n), (cls, f)


def coverage(test, n):
    return {cls: sum(detected(test, f, n) for f in faults) for cls, faults in all_faults(n).items()}


def test_coverage_table_n4():
    assert coverage(MATS, 4) == {"SAF": 8, "TF": 4, "CFin": 12, "CFid": 12, "CFst": 36, "AF": 38}
    assert coverage(MATS_PLUS, 4) == {"SAF": 8, "TF": 4, "CFin": 18, "CFid": 18, "CFst": 36, "AF": 44}
    assert coverage(MATS_PLUS_PLUS, 4) == {"SAF": 8, "TF": 8, "CFin": 18, "CFid": 18, "CFst": 36, "AF": 44}
    assert coverage(MARCH_C_MINUS, 4) == {"SAF": 8, "TF": 8, "CFin": 24, "CFid": 48, "CFst": 48, "AF": 44}


def test_mats_plus_misses():
    n = 4
    missed_tf = [f for f in all_faults(n)["TF"] if not detected(MATS_PLUS, f, n)]
    assert missed_tf == [("TF", i, "down") for i in range(n)]
    # the coupling of the memory coupling fault page: a rise of i > j sets j to 1
    assert not detected(MATS_PLUS, ("CFid", 1, 0, "up", 1), n)
    assert detected(MATS_PLUS, ("CFid", 0, 1, "up", 1), n)


def test_good_memory_never_fails():
    for n in range(1, 6):
        for s in initial_states(n):
            assert run_march(GoodMemory(n, s), MARCH_C_MINUS, n) is None


def test_failure_report():
    n = 4
    got = run_march(FaultyMemory(n, ("SAF", 2, 1), (0,) * n), MARCH_C_MINUS, n)
    assert got == (1, 2, 0, 1)  # element 1, address 2, its r0 read 1
