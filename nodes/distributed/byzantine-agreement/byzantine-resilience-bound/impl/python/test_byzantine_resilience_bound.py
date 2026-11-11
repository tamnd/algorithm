# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/byzantine-resilience-bound/. The authors are listed in prov/NNA88Z.jsonl.

from byzantine_resilience_bound import PROTOCOLS, RING, hexagon, neighbour, three_runs


def test_ring_shape() -> None:
    for c in RING:
        ns = {neighbour(c, q) for q in "ABC" if q != c[0]}
        assert len(ns) == 2
        assert all(n[0] != c[0] for n in ns)
    assert neighbour("A0", "C") == "C1" and neighbour("A0", "B") == "B0"


def test_views_match_and_some_run_fails() -> None:
    for name, proto in PROTOCOLS.items():
        runs = three_runs(proto)
        assert all(r["views_match"] for r in runs), name
        assert any(not (r["agreement"] and r["validity"]) for r in runs), name


def test_majority_decisions() -> None:
    _, dec = hexagon(PROTOCOLS["majority"])
    assert dec == {"A0": 0, "B0": 0, "C0": 0, "A1": 1, "B1": 1, "C1": 1}
    runs = three_runs(PROTOCOLS["majority"])
    assert [r["decisions"] for r in runs] == [{"B": 0, "C": 0}, {"A": 1, "B": 1}, {"C": 0, "A": 1}]
    assert [r["agreement"] for r in runs] == [True, True, False]


def test_flood_min_breaks_validity() -> None:
    runs = three_runs(PROTOCOLS["flood-min"])
    assert [r["validity"] for r in runs] == [True, False, True]
