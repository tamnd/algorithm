# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/oral-messages-algorithm/. The authors are listed in prov/SEB968.jsonl.

from oral_messages_algorithm import (
    RETREAT,
    STRATEGIES,
    VALUES,
    check,
    flip,
    hexagon,
    hexagon_runs,
    ic2,
    majority,
    om,
    om_messages,
    traitor_sets,
)


def test_majority() -> None:
    assert majority([1, 1, 2]) == 1
    assert majority([1, 2]) == RETREAT
    assert majority([2, 1, 2, 0]) == RETREAT
    assert majority([2]) == 2


def test_page_examples() -> None:
    # LSP Figure 3: n = 4, lieutenant 3 a traitor that sends 2 everywhere.
    res = om(4, 1, 1, frozenset({3}), lambda *a: 2)
    assert res["decisions"] == {1: 1, 2: 1}
    # LSP Figure 4: the commander sends 1, 2, 0 and the lieutenants agree.
    def traitor(rng, r, s, q, path, x):
        return {1: 1, 2: 2, 3: 0}[q] if r == 1 else x

    res = om(4, 1, None, frozenset({0}), traitor)
    assert res["decisions"] == {1: RETREAT, 2: RETREAT, 3: RETREAT}
    # n = 3: a loyal commander with value 1 and a lying lieutenant break IC2.
    res = om(3, 1, 1, frozenset({2}), flip)
    assert res["decisions"] == {1: RETREAT}


def test_rounds_and_messages() -> None:
    assert [om_messages(n, m) for n, m in [(4, 1), (7, 2), (10, 3)]] == [9, 156, 3609]
    for n, m in [(4, 1), (5, 1), (7, 2), (8, 2), (10, 3)]:
        res = om(n, m, 1)
        assert res["rounds"] == m + 1
        assert res["messages"] == om_messages(n, m)
        assert res["messages"] <= n ** (m + 1)


def test_ic1_ic2_all_traitor_sets() -> None:
    # every traitor set of size at most m, every strategy, every value
    for n, m in [(4, 1), (5, 1), (6, 1), (7, 2)]:
        for traitors in traitor_sets(n, m):
            for name, strategy in STRATEGIES.items():
                for value in VALUES:
                    for seed in range(3 if name == "random" else 1):
                        assert check(n, m, value, traitors, strategy, seed), (n, m, traitors, name)


def test_m3_seeded() -> None:
    for seed in range(4):
        for traitors in [frozenset({0, 4, 7}), frozenset({1, 2, 3}), frozenset({9})]:
            assert check(10, 3, 2, traitors, STRATEGIES["random"], seed)
            assert check(10, 3, 1, traitors, STRATEGIES["equivocate"], seed)


def test_lemma_1_ic2_with_fewer_traitors() -> None:
    # OM(m) gives IC2 when n > 2k + m and at most k generals are traitors:
    # n = 5, m = 2, k = 1 is below 3m + 1 = 7 but enough for IC2.
    for traitors in traitor_sets(5, 1):
        if 0 in traitors:
            continue
        for name, strategy in STRATEGIES.items():
            for value in VALUES:
                for seed in range(3):
                    res = om(5, 2, value, traitors, strategy, seed)
                    assert ic2(res["decisions"], True, value)


def test_hexagon_attack_breaks_n_equal_3m() -> None:
    for m in (1, 2):
        for values in [(0, 1), (1, 2)]:
            runs = hexagon_runs(m, values)
            assert all(r["views_match"] for r in runs)
            assert any(not r["ok"] for r in runs)
    # the copies of the case m = 1 with commander values 0 and 1
    _, dec = hexagon(1)
    assert dec[(1, 0)] == 0 and dec[(2, 0)] == 0
    assert [r["ok"] for r in hexagon_runs(1)] == [True, True, False]


def test_n_equal_3m_simple_strategies_fail() -> None:
    for m in (1, 2):
        n = 3 * m
        fails = sum(
            not check(n, m, v, t, s, 0) for t in traitor_sets(n, m) for s in STRATEGIES.values() for v in (1, 2)
        )
        assert fails > 0
