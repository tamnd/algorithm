# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/automated-mechanism-design/. The authors are listed in prov/JG4KT0.jsonl.

import random
from fractions import Fraction
from itertools import product

from automated_mechanism_design import design, profiles

F = Fraction
SEED = 20251120


def auction(values_per_agent):
    """Single-item auction: outcome i means agent i gets the item, outcome n means no sale."""
    n = len(values_per_agent)
    outcomes = list(range(n + 1))
    value = [{s: {o: (F(s) if o == i else F(0)) for o in outcomes} for s in values_per_agent[i]} for i in range(n)]
    return outcomes, value


def independent_prior(types, probs):
    prior = {}
    for t in product(*types):
        p = F(1)
        for i, s in enumerate(t):
            p *= probs[i][s]
        prior[t] = p
    return prior


def random_distribution(rng, k, low=1, high=12):
    vals = sorted(rng.sample(range(low, high + 1), k))
    weights = [rng.randint(1, 5) for _ in range(k)]
    total = sum(weights)
    return vals, {v: F(w, total) for v, w in zip(vals, weights)}


def utility(value, outcomes, mech, i, s, t):
    lottery, pay = mech[t]
    return sum((lottery[j] * F(value[i][s][o]) for j, o in enumerate(outcomes)), F(0)) - pay[i]


def interim(types, prior, value, outcomes, mech, i, s, r):
    """Expected utility times Pr(t_i = s) of agent i of type s who reports r."""
    total = F(0)
    for t in profiles(types):
        if t[i] == s:
            total += prior[t] * utility(value, outcomes, mech, i, s, t[:i] + (r,) + t[i + 1:])
    return total


def ironed_reference(vals, probs):
    """Discrete ironed virtual values from the upper concave hull of the revenue curve."""
    k = len(vals)
    q = [sum(probs[vals[l]] for l in range(j, k)) for j in range(k)] + [F(0)]
    pts = sorted([(F(0), F(0))] + [(q[j], vals[j] * q[j]) for j in range(k)])
    hull = []
    for p in pts:
        while len(hull) >= 2:
            (x1, y1), (x2, y2) = hull[-2], hull[-1]
            if (y2 - y1) * (p[0] - x1) <= (p[1] - y1) * (x2 - x1):
                hull.pop()
            else:
                break
        hull.append(p)

    def H(x):
        for (x1, y1), (x2, y2) in zip(hull, hull[1:]):
            if x1 <= x <= x2:
                return y1 + (y2 - y1) * (x - x1) / (x2 - x1)
        raise AssertionError

    return {vals[j]: (H(q[j]) - H(q[j + 1])) / probs[vals[j]] for j in range(k)}


def myerson_revenue(types, probs):
    phis = [ironed_reference(sorted(types[i]), probs[i]) for i in range(len(types))]
    prior = independent_prior(types, probs)
    return sum(prior[t] * max([F(0)] + [phis[i][s] for i, s in enumerate(t)]) for t in prior)


def test_single_buyer_posted_price():
    rng = random.Random(SEED)
    for _ in range(6):
        vals, pr = random_distribution(rng, rng.randint(1, 4))
        outcomes, value = auction([vals])
        prior = {(v,): pr[v] for v in vals}
        status, rev, _ = design([vals], prior, outcomes, value)
        best_price = max(v * sum(pr[w] for w in vals if w >= v) for v in vals)
        assert status == "optimal" and rev == best_price


def test_matches_myerson_two_bidders():
    rng = random.Random(SEED + 1)
    for trial in range(4):
        types, probs = [], []
        for _ in range(2):
            vals, pr = random_distribution(rng, rng.randint(2, 3))
            types.append(vals)
            probs.append(pr)
        outcomes, value = auction(types)
        prior = independent_prior(types, probs)
        ic, ir = ("bic", "interim") if trial % 2 == 0 else ("dsic", "ex_post")
        status, rev, _ = design(types, prior, outcomes, value, ic=ic, ir=ir)
        assert status == "optimal" and rev == myerson_revenue(types, probs)


def test_solution_meets_constraints_exactly():
    rng = random.Random(SEED + 2)
    for _ in range(3):
        types = [[0, 1], [0, 1, 2]]
        outcomes = ["x", "y", "z"]
        value = [{s: {o: F(rng.randint(0, 6)) for o in outcomes} for s in types[i]} for i in range(2)]
        weights = {t: rng.randint(1, 4) for t in product(*types)}
        total = sum(weights.values())
        prior = {t: F(w, total) for t, w in weights.items()}
        g = [F(rng.randint(-2, 2)) for _ in outcomes]
        status, val, mech = design(types, prior, outcomes, value, g=g, a=1, b=1)
        assert status == "optimal"
        for t, (lottery, pay) in mech.items():
            assert all(p >= 0 for p in lottery) and sum(lottery) == 1
        for i in range(2):
            for s in types[i]:
                assert interim(types, prior, value, outcomes, mech, i, s, s) >= 0
                for r in types[i]:
                    assert interim(types, prior, value, outcomes, mech, i, s, s) >= interim(types, prior, value, outcomes, mech, i, s, r)
        objective = F(0)
        for t, (lottery, pay) in mech.items():
            for j, o in enumerate(outcomes):
                objective += prior[t] * lottery[j] * (g[j] + sum(value[i][t[i]][o] for i in range(2)))
            objective += prior[t] * sum(pay)
        assert objective == val


def test_cremer_mclean_full_extraction():
    types = [[1, 2], [1, 2]]
    outcomes, value = auction(types)
    prior = {(1, 1): F(1, 3), (2, 2): F(1, 3), (1, 2): F(1, 6), (2, 1): F(1, 6)}
    status, rev, _ = design(types, prior, outcomes, value)
    assert status == "optimal" and rev == F(5, 3)  # the full expected surplus
    half = {1: F(1, 2), 2: F(1, 2)}
    status, rev_ind, _ = design(types, independent_prior(types, [half, half]), outcomes, value)
    assert rev_ind == myerson_revenue(types, [half, half]) and rev_ind < F(7, 4)


def deterministic_best(types, prior, outcomes, value, g, a):
    """Brute force over every deterministic rule without payments for one agent."""
    best = None
    for choice in product(range(len(outcomes)), repeat=len(types[0])):
        rule = dict(zip(types[0], choice))
        if all(value[0][s][outcomes[rule[s]]] >= value[0][s][outcomes[rule[r]]] for s in types[0] for r in types[0]):
            v = sum(prior[(s,)] * (g[rule[s]] + a * value[0][s][outcomes[rule[s]]]) for s in types[0])
            best = v if best is None else max(best, v)
    return best


def test_randomization_helps():
    types = [["L", "H"]]
    prior = {("L",): F(1, 2), ("H",): F(1, 2)}
    outcomes = ["a", "b", "c"]
    value = [{"L": {"a": 3, "b": 4, "c": 0}, "H": {"a": 1, "b": 5, "c": 0}}]
    g = [0, -3, -1]
    status, val, mech = design(types, prior, outcomes, value, g=g, a=1, b=0, ic="dsic", ir="none", payments=False)
    assert status == "optimal" and val == F(17, 8)
    assert mech[("L",)][0] == [1, 0, 0] and mech[("H",)][0] == [0, F(3, 4), F(1, 4)]
    assert deterministic_best(types, prior, outcomes, value, g, 1) == 2


def test_lp_at_least_deterministic_without_payments():
    rng = random.Random(SEED + 3)
    for _ in range(8):
        types = [["s0", "s1", "s2"][: rng.randint(2, 3)]]
        weights = [rng.randint(1, 4) for _ in types[0]]
        prior = {(s,): F(w, sum(weights)) for s, w in zip(types[0], weights)}
        outcomes = ["a", "b", "c"]
        value = [{s: {o: rng.randint(0, 5) for o in outcomes} for s in types[0]}]
        g = [rng.randint(-3, 3) for _ in outcomes]
        a = rng.randint(0, 1)
        status, val, mech = design(types, prior, outcomes, value, g=g, a=a, b=0, ic="dsic", ir="none", payments=False)
        assert status == "optimal" and val >= deterministic_best(types, prior, outcomes, value, g, a)
        for s in types[0]:
            for r in types[0]:
                assert utility(value, outcomes, mech, 0, s, (s,)) >= utility(value, outcomes, mech, 0, s, (r,))


def test_outcome_only_objective_pools():
    rng = random.Random(SEED + 4)
    for _ in range(3):
        types = [[0, 1], [0, 1]]
        outcomes = ["a", "b", "c"]
        value = [{s: {o: rng.randint(0, 4) for o in outcomes} for s in types[i]} for i in range(2)]
        prior = independent_prior(types, [{0: F(1, 3), 1: F(2, 3)}, {0: F(1, 2), 1: F(1, 2)}])
        g = [F(rng.randint(-3, 3)) for _ in outcomes]
        status, val, _ = design(types, prior, outcomes, value, g=g, a=0, b=0, ir="none", payments=False)
        assert status == "optimal" and val == max(g)


def test_bad_arguments():
    outcomes, value = auction([[1]])
    for kwargs in ({"ic": "nash"}, {"ir": "always"}):
        try:
            design([[1]], {(1,): F(1)}, outcomes, value, **kwargs)
        except ValueError:
            continue
        raise AssertionError("expected ValueError")
