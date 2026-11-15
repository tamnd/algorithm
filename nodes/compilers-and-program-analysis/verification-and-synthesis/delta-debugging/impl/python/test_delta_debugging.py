# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/delta-debugging/. The authors are listed in prov/25NQX4.jsonl.

import itertools
import math
import random

import toyir
from delta_debugging import FAIL, PASS, UNRESOLVED, ddmin, is_one_minimal, program_test, split


def bound(n):
    """The worst-case number of tests proved in the proof file."""
    return (3 * n - 2) * (n - 1) if n >= 2 else 0


def brute_force_minimum(items, test):
    """A failing sub-list of the smallest size, the first one in the order of
    itertools.combinations."""
    for k in range(len(items) + 1):
        for comb in itertools.combinations(items, k):
            if test(list(comb)) == FAIL:
                return list(comb)
    return None


def check(items, test):
    """Run ddmin and check what the page promises. Returns (result, minimum)."""
    res, calls = ddmin(items, test)
    assert test(res) == FAIL
    it = iter(items)
    assert all(x in it for x in res)  # a sub-list, in the original order
    assert is_one_minimal(res, test)
    assert calls <= bound(len(items))
    m = brute_force_minimum(items, test)
    assert len(m) <= len(res)
    return res, m


def test_split():
    for size in range(1, 30):
        c = list(range(size))
        for n in range(1, size + 1):
            parts = split(c, n)
            assert len(parts) == n
            assert [x for p in parts for x in p] == c
            sizes = [len(p) for p in parts]
            assert max(sizes) - min(sizes) <= 1 and min(sizes) >= 1


def test_one_minimal_is_not_minimum():
    def t(s):
        return FAIL if {0, 1} <= set(s) or 6 in s else PASS

    log = []

    def logged(s):
        out = t(s)
        log.append((list(s), out))
        return out

    res, calls = ddmin(list(range(8)), logged)
    assert res == [0, 1] and calls == 4
    assert log == [([0, 1, 2, 3], FAIL), ([0, 1], FAIL), ([0], PASS), ([1], PASS)]
    assert is_one_minimal(res, t)
    assert brute_force_minimum(list(range(8)), t) == [6]


def test_single_culprit_set_is_found_exactly():
    # With a monotone test that fails exactly on the supersets of K, the only
    # 1-minimal failing set is K, so ddmin must return it.
    rng = random.Random(1)
    for n in range(1, 13):
        for _ in range(20):
            k = rng.randint(1, n)
            K = set(rng.sample(range(n), k))
            res, m = check(list(range(n)), lambda s: FAIL if K <= set(s) else PASS)
            assert set(res) == K and len(m) == k


def test_against_brute_force_up_to_12():
    rng = random.Random(2)
    larger = 0
    for n in range(1, 13):
        for _ in range(12):
            # Monotone: fails when the input contains one of a few culprit sets.
            culprits = [set(rng.sample(range(n), rng.randint(1, min(n, 4)))) for _ in range(rng.randint(1, 3))]
            culprits.append(set(range(n)))

            def mono(s, culprits=culprits):
                return FAIL if any(c <= set(s) for c in culprits) else PASS

            res, m = check(list(range(n)), mono)
            larger += len(res) > len(m)

            # Not monotone, with UNRESOLVED outcomes: a random fixed table.
            table = {}

            def chaos(s, table=table, n=n):
                key = frozenset(s)
                if not key:
                    return PASS
                if len(key) == n:
                    return FAIL
                if key not in table:
                    r = rng.random()
                    table[key] = FAIL if r < 0.15 else (UNRESOLVED if r < 0.5 else PASS)
                return table[key]

            check(list(range(n)), chaos)
    assert larger > 0


def test_every_test_function_up_to_4():
    for n in range(1, 5):
        full = frozenset(range(n))
        middle = [frozenset(c) for k in range(1, n) for c in itertools.combinations(range(n), k)]
        for mask in range(1 << len(middle)):
            fails = {middle[i] for i in range(len(middle)) if mask >> i & 1} | {full}
            res, calls = ddmin(list(range(n)), lambda s: FAIL if frozenset(s) in fails else PASS)
            assert frozenset(res) in fails
            assert all(frozenset(res) - {x} not in fails for x in res)
            assert calls <= bound(n)


def test_best_case_is_logarithmic():
    for k in range(1, 11):
        n = 1 << k
        for culprit in (0, n // 3, n - 1):
            res, calls = ddmin(list(range(n)), lambda s: FAIL if culprit in s else PASS)
            assert res == [culprit]
            assert calls <= 2 * math.log2(n)


def test_all_unresolved_keeps_the_input():
    for n in range(1, 13):
        res, calls = ddmin(list(range(n)), lambda s: FAIL if len(s) == n else UNRESOLVED)
        assert res == list(range(n))
        assert calls <= bound(n)


PROGRAM = """
entry:
  a = 5
  b = 3
  x = a * 7
  c = a - b
  y = x + b
  d = c * 2
  e = b + 1
  z = y - 1
  f = d - 4
  w = z / e
  g = e / f
  h = g + a
  ret 0
"""


def test_toy_ir_program():
    prog = toyir.parse(PROGRAM)
    assert toyir.run(prog, []) == ("trap",)
    instrs = prog.blocks["entry"].instrs
    test = program_test(instrs, 0, lambda out: out == ("trap",))
    outcomes = []

    def logged(s):
        out = test(s)
        outcomes.append(out)
        return out

    res, calls = ddmin(instrs, logged)
    assert [toyir.defs(i) for i in res] == ["a", "b", "c", "d", "e", "f", "g"]
    assert calls == 124
    assert outcomes.count(UNRESOLVED) > outcomes.count(PASS)
    small = toyir.Program([], {"entry": toyir.Block(res, ("ret", 0))})
    assert toyir.run(small, []) == ("trap",)
    assert len(brute_force_minimum(instrs, test)) == len(res)
    assert calls <= bound(len(instrs))


def test_bad_outcome_is_rejected():
    try:
        ddmin([1, 2, 3], lambda s: True)
    except ValueError:
        return
    raise AssertionError("expected ValueError")
