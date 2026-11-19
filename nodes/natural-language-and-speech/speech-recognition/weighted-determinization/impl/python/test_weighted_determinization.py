# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weighted-determinization/. The authors are listed in prov/40YQAC.jsonl.

import itertools
import math
import random

import pytest

from nlslog import LOG_COST, TROPICAL, Semiring
from weighted_determinization import Acceptor, NotDeterminizable, determinize, string_weight

LABELS = ["a", "b"]


def all_strings(max_len: int):
    for k in range(max_len + 1):
        for x in itertools.product(LABELS, repeat=k):
            yield x


def close(u: float, v: float, tol: float = 1e-9) -> bool:
    if math.isinf(u) or math.isinf(v):
        return u == v
    return abs(u - v) <= tol


def equivalent(a: Acceptor, d: Acceptor, sr: Semiring, max_len: int = 4) -> bool:
    return all(close(string_weight(a, x, sr), string_weight(d, x, sr)) for x in all_strings(max_len))


def random_acyclic(rng: random.Random, n: int) -> Acceptor:
    a = Acceptor()
    for _ in range(n):
        a.add_state()
    for i in range(n):
        for j in range(i + 1, n):
            for c in LABELS:
                if rng.random() < 0.45:
                    a.add_arc(i, c, rng.randint(0, 8) * 0.25, j)
    a.set_final(n - 1, rng.randint(0, 2) * 0.5)
    if rng.random() < 0.5:
        a.set_final(rng.randrange(1, n), rng.randint(0, 2) * 0.5)
    a.initial = rng.randint(0, 2) * 0.5
    return a


def random_twins(rng: random.Random, n: int) -> Acceptor:
    """A cyclic acceptor with the twins property: every arc out of a state other than 0 costs c[label].

    No arc enters state 0, so any cycle reading v costs the sum of c over v, at
    every state; two cycles that read the same string have the same weight.
    """
    cost = {c: rng.randint(0, 6) * 0.5 for c in LABELS}
    a = Acceptor()
    for _ in range(n):
        a.add_state()
    for i in range(n):
        for c in LABELS:
            for _ in range(2):
                if rng.random() < 0.5:
                    w = rng.randint(0, 8) * 0.25 if i == 0 else cost[c]
                    a.add_arc(i, c, w, rng.randrange(1, n))
    for q in range(1, n):
        if rng.random() < 0.5:
            a.set_final(q, rng.randint(0, 4) * 0.5)
    return a


def two_cycles(u: float = 3.0, v: float = 4.0) -> Acceptor:
    """States 1 and 2 are both reached by a; their a-loops cost u and v."""
    a = Acceptor()
    for _ in range(4):
        a.add_state()
    a.add_arc(0, "a", 0.0, 1)
    a.add_arc(0, "a", 0.0, 2)
    a.add_arc(1, "a", u, 1)
    a.add_arc(2, "a", v, 2)
    a.add_arc(1, "b", 0.0, 3)
    a.add_arc(2, "c", 0.0, 3)
    a.set_final(3)
    return a


def test_page_example():
    a = Acceptor()
    for _ in range(4):
        a.add_state()
    a.add_arc(0, "a", 1.0, 1)
    a.add_arc(0, "a", 2.0, 2)
    a.add_arc(1, "b", 3.0, 3)
    a.add_arc(2, "b", 1.0, 3)
    a.add_arc(1, "c", 5.0, 3)
    a.set_final(3)
    d, subsets = determinize(a)
    assert subsets == [[(0, 0.0)], [(1, 0.0), (2, 1.0)], [(3, 0.0)]]
    assert d.arcs[0] == [("a", 1.0, 1)]
    assert sorted(d.arcs[1]) == [("b", 2.0, 2), ("c", 5.0, 2)]
    assert d.final == {2: 0.0}
    assert string_weight(d, "ab") == 3.0 and string_weight(d, "ac") == 6.0
    assert d.is_deterministic() and not a.is_deterministic()


def test_random_acyclic_tropical_and_log():
    rng = random.Random(1)
    for case in range(80):
        sr = LOG_COST if case % 2 else TROPICAL
        a = random_acyclic(rng, rng.randint(2, 5))
        d, _ = determinize(a, sr)
        assert d.is_deterministic()
        assert equivalent(a, d, sr)


def test_cyclic_with_twins_property():
    rng = random.Random(2)
    for _ in range(60):
        a = random_twins(rng, rng.randint(2, 5))
        d, _ = determinize(a, TROPICAL, max_states=500)
        assert d.is_deterministic()
        assert equivalent(a, d, TROPICAL)


def test_no_twins_does_not_stop():
    with pytest.raises(NotDeterminizable):
        determinize(two_cycles(3.0, 4.0), TROPICAL, max_states=50)
    # With equal loop costs the two states are twins and the result is small.
    d, subsets = determinize(two_cycles(3.0, 3.0), TROPICAL)
    assert subsets == [[(0, 0.0)], [(1, 0.0), (2, 0.0)], [(3, 0.0)]]
    assert equivalent(two_cycles(3.0, 3.0), d, TROPICAL)


def test_residuals_grow_without_twins():
    with pytest.raises(NotDeterminizable) as info:
        determinize(two_cycles(3.0, 4.0), TROPICAL, max_states=12)
    # After a^k the subset is {(1, 0), (2, k - 1)}: the residual of state 2 grows by 1 per a.
    loops = [s for s in info.value.subsets if s[0][0] == 1]
    assert len(loops) >= 5
    assert loops == [[(1, 0.0), (2, float(k))] for k in range(len(loops))]


def test_exponential_blowup():
    # (a|b)* a (a|b)^(n-1): the n-th symbol from the end is a. Weights 0.
    for n in range(1, 6):
        a = Acceptor()
        for _ in range(n + 1):
            a.add_state()
        for c in LABELS:
            a.add_arc(0, c, 0.0, 0)
        a.add_arc(0, "a", 0.0, 1)
        for i in range(1, n):
            for c in LABELS:
                a.add_arc(i, c, 0.0, i + 1)
        a.set_final(n)
        d, _ = determinize(a)
        assert d.num_states() == 2 ** n
        assert equivalent(a, d, TROPICAL)


def test_log_semiring_adds_probabilities():
    a = Acceptor()
    for _ in range(3):
        a.add_state()
    a.add_arc(0, "a", -math.log(0.5), 1)
    a.add_arc(0, "a", -math.log(0.25), 2)
    a.set_final(1)
    a.set_final(2)
    d, _ = determinize(a, LOG_COST)
    assert d.num_states() == 2
    assert close(string_weight(d, "a", LOG_COST), -math.log(0.75))
    d, _ = determinize(a, TROPICAL)
    assert close(string_weight(d, "a", TROPICAL), -math.log(0.5))
