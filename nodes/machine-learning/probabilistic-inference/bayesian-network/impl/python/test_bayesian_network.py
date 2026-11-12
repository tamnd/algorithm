# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bayesian-network/. The authors are listed in prov/BFMEF2.jsonl.

import random
from fractions import Fraction as F
from itertools import product

from bayesian_network import BayesianNetwork


def bern(p):
    return [1 - p, p]


def sprinkler() -> BayesianNetwork:
    card = {"C": 2, "S": 2, "R": 2, "W": 2}
    parents = {"C": [], "S": ["C"], "R": ["C"], "W": ["S", "R"]}
    cpt = {
        "C": {(): bern(F(1, 2))},
        "S": {(0,): bern(F(1, 2)), (1,): bern(F(1, 10))},
        "R": {(0,): bern(F(1, 5)), (1,): bern(F(4, 5))},
        "W": {(0, 0): bern(F(0)), (1, 0): bern(F(9, 10)), (0, 1): bern(F(9, 10)), (1, 1): bern(F(99, 100))},
    }
    return BayesianNetwork(card, parents, cpt)


def random_network(rng: random.Random, n: int) -> BayesianNetwork:
    names = [f"X{i}" for i in range(n)]
    card = {v: rng.randint(2, 3) for v in names}
    parents = {}
    for i, v in enumerate(names):
        parents[v] = [names[j] for j in range(i) if rng.random() < 0.5][:3]
    cpt = {}
    for v in names:
        cpt[v] = {}
        for u in product(*(range(card[p]) for p in parents[v])):
            w = [rng.randint(1, 9) for _ in range(card[v])]
            cpt[v][u] = [F(x, sum(w)) for x in w]
    return BayesianNetwork(card, parents, cpt)


def independent(bn: BayesianNetwork, a: str, b_set, given) -> bool:
    """a _||_ b_set | given, checked by P(a, B, G) P(G) = P(a, G) P(B, G) for all values."""
    b_set, given = sorted(b_set), sorted(given)
    tab = {}
    for x in bn.assignments():
        key = (x[a], tuple(x[v] for v in b_set), tuple(x[v] for v in given))
        tab[key] = tab.get(key, 0) + bn.joint(x)
    def m(fa=None, fb=None, fg=None):
        return sum((p for (va, vb, vg), p in tab.items() if (fa is None or va == fa) and (fb is None or vb == fb) and vg == fg), F(0))
    for va in range(bn.card[a]):
        for vb in product(*(range(bn.card[v]) for v in b_set)):
            for vg in product(*(range(bn.card[v]) for v in given)):
                if m(va, vb, vg) * m(fg=vg) != m(fa=va, fg=vg) * m(fb=vb, fg=vg):
                    return False
    return True


def test_sprinkler_numbers() -> None:
    bn = sprinkler()
    assert bn.free_parameters() == 9 and 2 ** 4 - 1 == 15
    assert bn.probability({"W": 1}) == F(6471, 10000)
    assert bn.query("R", {"W": 1})[1] == F(509, 719)
    assert bn.query("S", {"W": 1})[1] == F(309, 719)
    # explaining away: rain makes the sprinkler less likely once the grass is wet
    assert bn.query("S", {"W": 1, "R": 1})[1] == F(99, 509)
    assert bn.query("S", {"W": 1, "R": 1})[1] < bn.query("S", {"W": 1})[1]


def test_joint_sums_to_one_and_returns_the_cpts() -> None:
    rng = random.Random(1988)
    for _ in range(15):
        bn = random_network(rng, rng.randint(3, 5))
        assert sum(bn.joint(x) for x in bn.assignments()) == 1
        for v in bn.order:
            pa = bn.parents[v]
            for u in product(*(range(bn.card[p]) for p in pa)):
                assert bn.query(v, dict(zip(pa, u))) == list(bn.cpt[v][u])


def test_local_markov_property() -> None:
    rng = random.Random(7)
    for _ in range(8):
        bn = random_network(rng, 4)
        for v in bn.order:
            others = set(bn.card) - {v} - bn.descendants(v) - set(bn.parents[v])
            if others:
                assert independent(bn, v, others, bn.parents[v])


def test_a_non_independence() -> None:
    bn = sprinkler()
    # S and R are independent given C, but dependent given C and W (W is a common child)
    assert independent(bn, "S", {"R"}, {"C"})
    assert not independent(bn, "S", {"R"}, {"C", "W"})


def test_rejects_cycles_and_bad_rows() -> None:
    for parents in ({"A": ["B"], "B": ["A"]},):
        try:
            BayesianNetwork({"A": 2, "B": 2}, parents, {})
        except ValueError:
            pass
        else:
            raise AssertionError("cycle accepted")
    try:
        BayesianNetwork({"A": 2}, {"A": []}, {"A": {(): [F(1, 2), F(1, 3)]}})
    except ValueError:
        pass
    else:
        raise AssertionError("bad row accepted")
