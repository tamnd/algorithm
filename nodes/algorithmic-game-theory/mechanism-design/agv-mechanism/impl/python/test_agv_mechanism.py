# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/agv-mechanism/. The authors are listed in prov/KNJ3AG.jsonl.

import random
from fractions import Fraction
from itertools import product

from agv_mechanism import (
    agv,
    agv_payments,
    efficient_outcome,
    expected_externalities,
    interim_utility,
)


def random_instance(rng, n, k, m):
    types = [list(range(k)) for _ in range(n)]
    probs = []
    for _ in range(n):
        w = [rng.randint(1, 5) for _ in range(k)]
        s = sum(w)
        probs.append({t: Fraction(w[t], s) for t in range(k)})
    outcomes = list(range(m))
    value = [
        {t: {o: rng.randint(-5, 10) for o in outcomes} for t in range(k)}
        for _ in range(n)
    ]
    return types, probs, outcomes, value


def instances():
    rng = random.Random(20251120)
    out = []
    for n in (2, 3):
        for k in (1, 2, 3):
            for m in (1, 2, 3, 4):
                for _ in range(3):
                    out.append(random_instance(rng, n, k, m))
    return out


def welfare(value, profile, o):
    return sum(Fraction(value[i][t][o]) for i, t in enumerate(profile))


def h_direct(types, probs, outcomes, value):
    # A second formula for h: for each agent and type, loop over the others only.
    n = len(types)
    h = []
    for i in range(n):
        hi = {}
        for t in types[i]:
            acc = Fraction(0)
            others = [types[j] for j in range(n) if j != i]
            for rest in product(*others):
                prof = list(rest[:i]) + [t] + list(rest[i:])
                pr = Fraction(1)
                for j in range(n):
                    if j != i:
                        pr *= probs[j][prof[j]]
                o = efficient_outcome(outcomes, value, prof)
                acc += pr * sum(Fraction(value[j][prof[j]][o]) for j in range(n) if j != i)
            hi[t] = acc
        h.append(hi)
    return h


def public_project():
    types = [[10, 35]] * 3
    probs = [{10: Fraction(1, 2), 35: Fraction(1, 2)}] * 3
    outcomes = ["no", "build"]
    value = [{t: {"no": 0, "build": t - 20} for t in (10, 35)} for _ in range(3)]
    return types, probs, outcomes, value


def test_efficient_against_brute_force():
    for types, probs, outcomes, value in instances():
        for prof in product(*types):
            o, _ = agv(types, probs, outcomes, value, prof)
            best = max(welfare(value, prof, q) for q in outcomes)
            assert welfare(value, prof, o) == best


def test_h_matches_second_formula():
    for types, probs, outcomes, value in instances():
        assert expected_externalities(types, probs, outcomes, value) == h_direct(
            types, probs, outcomes, value
        )


def test_strong_budget_balance_on_every_profile():
    for types, probs, outcomes, value in instances():
        for prof in product(*types):
            _, pay = agv(types, probs, outcomes, value, prof)
            assert sum(pay) == 0


def test_bayesian_incentive_compatible():
    for types, probs, outcomes, value in instances():
        for i in range(len(types)):
            for t in types[i]:
                truth = interim_utility(types, probs, outcomes, value, i, t, t)
                for r in types[i]:
                    assert truth >= interim_utility(types, probs, outcomes, value, i, t, r)


def test_public_project_numbers():
    types, probs, outcomes, value = public_project()
    h = expected_externalities(types, probs, outcomes, value)
    assert h == [{10: Fraction(15, 2), 35: Fraction(10)}] * 3
    o, pay = agv(types, probs, outcomes, value, (10, 35, 35))
    assert o == "build"
    assert pay == [Fraction(5, 2), Fraction(-5, 4), Fraction(-5, 4)]
    assert interim_utility(types, probs, outcomes, value, 0, 10, 10) == Fraction(-15, 4)
    assert interim_utility(types, probs, outcomes, value, 0, 35, 35) == Fraction(25, 2)


def test_not_interim_individually_rational():
    # The low type of the public project expects a loss, so interim IR fails.
    types, probs, outcomes, value = public_project()
    assert interim_utility(types, probs, outcomes, value, 0, 10, 10) < 0
    # Bilateral trade: seller cost in {0, 2}, buyer value in {1, 3}.
    types = [[0, 2], [1, 3]]
    probs = [{0: Fraction(1, 2), 2: Fraction(1, 2)}, {1: Fraction(1, 2), 3: Fraction(1, 2)}]
    outcomes = ["no", "trade"]
    value = [{c: {"no": 0, "trade": -c} for c in (0, 2)}, {v: {"no": 0, "trade": v} for v in (1, 3)}]
    assert interim_utility(types, probs, outcomes, value, 1, 1, 1) == Fraction(-5, 4)


def test_not_dominant_strategy_incentive_compatible():
    types, probs, outcomes, value = public_project()
    h = expected_externalities(types, probs, outcomes, value)

    def ex_post(true_t, prof):
        o = efficient_outcome(outcomes, value, prof)
        return value[0][true_t][o] - agv_payments(h, prof)[0]

    assert ex_post(10, (10, 35, 35)) == Fraction(-25, 2)
    assert ex_post(10, (35, 35, 35)) == Fraction(-10)
    assert ex_post(10, (35, 35, 35)) > ex_post(10, (10, 35, 35))


def test_expected_welfare_is_shared_exactly():
    # Budget balance means the interim utilities add up to the expected welfare.
    for types, probs, outcomes, value in instances():
        n = len(types)
        exp_w = Fraction(0)
        for prof in product(*types):
            pr = Fraction(1)
            for j in range(n):
                pr *= probs[j][prof[j]]
            exp_w += pr * welfare(value, prof, efficient_outcome(outcomes, value, prof))
        total = Fraction(0)
        for i in range(n):
            for t in types[i]:
                total += probs[i][t] * interim_utility(types, probs, outcomes, value, i, t, t)
        assert total == exp_w


def test_needs_two_agents():
    try:
        agv_payments([{0: Fraction(0)}], (0,))
    except ValueError:
        return
    raise AssertionError("expected ValueError")
