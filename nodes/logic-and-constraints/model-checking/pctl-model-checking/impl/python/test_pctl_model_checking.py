# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pctl-model-checking/. The authors are listed in prov/7T9702.jsonl.

import random
from fractions import Fraction as F

from pctl_model_checking import check, prob_bounded_until, prob_next, prob_until

HALF = F(1, 2)


def knuth_yao():
    """The Knuth-Yao die: a fair coin simulates a fair six-sided die.
    States 0..6 are coin states, 7..12 are the faces 1..6."""
    t = {0: (1, 2), 1: (3, 4), 2: (5, 6), 3: (1, 7), 4: (8, 9), 5: (10, 11), 6: (12, 2)}
    P = []
    for s in range(13):
        if s in t:
            a, b = t[s]
            P.append({a: HALF, b: HALF})
        else:
            P.append({s: F(1)})
    L = [set() for _ in range(13)]
    for face in range(1, 7):
        L[6 + face] = {f"d{face}", "done"}
    return {"P": P, "L": L}


def random_chain(rng, n):
    P = []
    for _ in range(n):
        k = rng.randint(1, min(3, n))
        targets = rng.sample(range(n), k)
        weights = [rng.randint(1, 4) for _ in targets]
        tot = sum(weights)
        P.append({t: F(w, tot) for t, w in zip(targets, weights)})
    L = [{a for a in "abc" if rng.random() < 0.4} for _ in range(n)]
    return {"P": P, "L": L}


def value_iteration(chain, phi, psi, steps):
    """Pr(phi U psi) by iterating x <- P x on phi-and-not-psi states, in floats,
    until the change is tiny or the step budget runs out. The iterates grow
    toward the answer from below."""
    n = len(chain["P"])
    x = [1.0 if s in psi else 0.0 for s in range(n)]
    live = phi - psi
    for _ in range(steps):
        y = [sum(float(p) * x[t] for t, p in chain["P"][s].items()) if s in live else x[s] for s in range(n)]
        done = max(abs(a - b) for a, b in zip(x, y)) < 1e-14
        x = y
        if done:
            break
    return x


def enumerate_paths(chain, phi, psi, k):
    """Pr(phi U<=k psi) by listing every path of length at most k."""
    n = len(chain["P"])
    out = []
    for s0 in range(n):
        total = F(0)
        frontier = [(s0, F(1))]
        for step in range(k + 1):
            nxt = []
            for s, pr in frontier:
                if s in psi:
                    total += pr
                elif s in phi and step < k:
                    nxt.extend((t, pr * p) for t, p in chain["P"][s].items())
            frontier = nxt
        out.append(total)
    return out


def sat(chain, a):
    return {s for s in range(len(chain["P"])) if a in chain["L"][s]}


def test_knuth_yao_die() -> None:
    m = knuth_yao()
    n = len(m["P"])
    every = set(range(n))
    for face in range(1, 7):
        x = prob_until(m, every, sat(m, f"d{face}"))
        assert x[0] == F(1, 6)
    assert prob_until(m, every, sat(m, "done"))[0] == 1
    # the die ends within 3 flips with probability 3/4
    assert prob_bounded_until(m, every, sat(m, "done"), 3)[0] == F(3, 4)
    six = ("ap", "d6")
    assert 0 in check(m, ("P", ">=", F(1, 6), ("U", ("true",), six)))
    assert 0 not in check(m, ("P", ">", F(1, 6), ("U", ("true",), six)))
    # almost surely done, although an infinite path avoids it
    assert 0 in check(m, ("P", ">=", F(1), ("U", ("true",), ("ap", "done"))))


def test_exact_matches_value_iteration_and_enumeration() -> None:
    rng = random.Random(51)
    for _ in range(300):
        m = random_chain(rng, rng.randint(1, 7))
        n = len(m["P"])
        phi = sat(m, "a") | (set(range(n)) if rng.random() < 0.3 else set())
        psi = sat(m, "b")
        exact = prob_until(m, phi, psi)
        assert all(0 <= v <= 1 for v in exact)
        approx = value_iteration(m, phi, psi, 100000)
        assert all(a <= float(e) + 1e-12 and float(e) - a < 1e-9 for e, a in zip(exact, approx))
        for k in (0, 1, 2, 5):
            bounded = prob_bounded_until(m, phi, psi, k)
            assert bounded == enumerate_paths(m, phi, psi, k)
            assert all(b <= e for b, e in zip(bounded, exact))
        # the precomputed sets: probability 0 exactly when psi cannot be reached through phi
        for s in range(n):
            reach = enumerate_paths(m, phi, psi, n)[s] > 0
            assert (exact[s] > 0) == reach


def test_solution_is_the_least_fixed_point() -> None:
    rng = random.Random(52)
    for _ in range(200):
        m = random_chain(rng, rng.randint(1, 6))
        n = len(m["P"])
        phi, psi = sat(m, "a"), sat(m, "b")
        x = prob_until(m, phi, psi)
        for s in range(n):
            if s in psi:
                assert x[s] == 1
            elif s not in phi:
                assert x[s] == 0
            else:
                assert x[s] == sum(p * x[t] for t, p in m["P"][s].items())


def test_next_and_nesting() -> None:
    rng = random.Random(53)
    for _ in range(200):
        m = random_chain(rng, rng.randint(1, 6))
        n = len(m["P"])
        a, b = ("ap", "a"), ("ap", "b")
        nx = prob_next(m, sat(m, "a"))
        assert check(m, ("P", ">", F(1, 2), ("X", a))) == {s for s in range(n) if nx[s] > HALF}
        # duality: P>=p (X a) iff not P>1-p (X not a)
        for p in (F(0), F(1, 3), F(1, 2), F(1)):
            left = check(m, ("P", ">=", p, ("X", a)))
            right = check(m, ("not", ("P", ">", 1 - p, ("X", ("not", a)))))
            assert left == right
        # a nested formula, computed by hand from the inner satisfaction set
        inner = ("P", ">=", F(1, 2), ("BU", ("true",), b, 2))
        inner_sat = check(m, inner)
        outer = check(m, ("P", ">", F(0), ("U", a, inner)))
        want = {s for s, v in enumerate(prob_until(m, sat(m, "a"), inner_sat)) if v > 0}
        assert outer == want


def test_edge_cases() -> None:
    # one absorbing state
    m = {"P": [{0: F(1)}], "L": [{"a"}]}
    assert prob_until(m, {0}, set()) == [0]
    assert prob_until(m, set(), {0}) == [1]
    # a two-state cycle that never reaches psi
    m = {"P": [{1: F(1)}, {0: F(1)}], "L": [set(), set()]}
    assert prob_until(m, {0, 1}, set()) == [0, 0]
    # gambler's ruin with p = 1/3 up from the middle of 0..3
    P = [{0: F(1)}, {0: F(2, 3), 2: F(1, 3)}, {1: F(2, 3), 3: F(1, 3)}, {3: F(1)}]
    m = {"P": P, "L": [set(), set(), set(), {"win"}]}
    x = prob_until(m, {0, 1, 2, 3}, {3})
    # ((q/p)^i - 1) / ((q/p)^3 - 1) with q/p = 2
    assert x[1] == F(1, 7) and x[2] == F(3, 7)
