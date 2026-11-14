# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/t-vpack/. The authors are listed in prov/R2R827.jsonl.

import random
from fractions import Fraction

from t_vpack import Ble, criticalities, external_inputs, form_bles, is_legal, min_clusters, t_vpack


def random_netlist(rng: random.Random, n: int, k: int, primaries: int) -> list[Ble]:
    """BLE i reads primary inputs, outputs of earlier BLEs, and outputs of later registered BLEs."""
    registered = [rng.random() < 0.3 for _ in range(n)]
    bles = []
    for i in range(n):
        pool = [f"i{p}" for p in range(primaries)]
        pool += [f"o{j}" for j in range(i)]
        pool += [f"o{j}" for j in range(i + 1, n) if registered[j]]
        size = rng.randint(1, min(k, len(pool)))
        bles.append(Ble(tuple(sorted(rng.sample(pool, size))), f"o{i}", registered[i]))
    return bles


def brute_criticalities(bles: list[Ble]) -> dict[tuple[int, int], Fraction]:
    """Longest paths by enumerating every combinational path from scratch."""
    driver = {b.output: i for i, b in enumerate(bles)}
    edges = [(driver[x], v) for v, b in enumerate(bles) for x in b.inputs if x in driver]
    comb = [(u, v) for u, v in edges if not bles[u].registered]

    def longest_to(v: int) -> int:  # BLEs on the longest path that ends at v, v included
        return 1 + max((longest_to(u) for u, w in comb if w == v), default=0)

    def longest_from(v: int) -> int:  # BLEs on the longest path that starts at v, v included
        if bles[v].registered:
            return 1
        return 1 + max((longest_from(w) for u, w in comb if u == v), default=0)

    dmax = max(longest_to(v) for v in range(len(bles)))
    out = {}
    for u, v in edges:
        before = 0 if bles[u].registered else longest_to(u)
        through = before + longest_from(v)
        out[(u, v)] = 1 - Fraction(dmax - through, dmax)
    return out


def test_hand_example():
    # a(x, y) -> A, b(A, z) -> B, c(x, w) -> C, d(C, y) -> D with N = 2, I = 3
    bles = [
        Ble(("x", "y"), "A"),
        Ble(("A", "z"), "B"),
        Ble(("w", "x"), "C"),
        Ble(("C", "y"), "D"),
    ]
    clusters = t_vpack(bles, 2, 3)
    assert is_legal(bles, clusters, 2, 3)
    assert clusters == [[0, 1], [2, 3]]
    assert min_clusters(bles, 2, 3) == 2
    assert len(external_inputs(bles, {0, 2})) == 3
    assert len(external_inputs(bles, {1, 3})) == 4  # A, z, C, y: the other pairing is illegal


def test_suboptimal_example():
    bles = [Ble(("i0",), "o0"), Ble(("o0",), "o1"), Ble(("i0", "o0"), "o2"), Ble(("o1",), "o3")]
    crit = criticalities(bles)
    assert crit == {(0, 1): 1, (0, 2): Fraction(2, 3), (1, 3): 1}
    clusters = t_vpack(bles, 2, 2, k=2)
    assert clusters == [[0, 1], [3], [2]]
    assert is_legal(bles, clusters, 2, 2)
    assert min_clusters(bles, 2, 2) == 2
    assert t_vpack(bles, 2, 2, lam=Fraction(0), k=2) == [[0, 2], [1, 3]]


def test_form_bles():
    luts = [(("a", "b"), "x"), (("x", "c"), "y"), (("y",), "z")]
    ffs = [("x", "qx"), ("z", "qz"), ("c", "qc")]
    bles = form_bles(luts, ffs)
    # x has two readers, so its flip-flop gets a BLE of its own; z feeds only its flip-flop.
    assert Ble(("x",), "qx", True) in bles
    assert Ble(("y",), "qz", True) in bles
    assert Ble(("c",), "qc", True) in bles
    assert Ble(("a", "b"), "x", False) in bles
    assert Ble(("x", "c"), "y", False) in bles
    assert len(bles) == 5


def test_criticalities_match_path_enumeration():
    rng = random.Random(11)
    for _ in range(300):
        bles = random_netlist(rng, rng.randint(1, 7), 3, 3)
        assert criticalities(bles) == brute_criticalities(bles)


def test_legal_and_never_below_optimum():
    rng = random.Random(1)
    worse = 0
    for _ in range(600):
        k = rng.randint(1, 3)
        bles = random_netlist(rng, rng.randint(1, 8), k, rng.randint(1, 4))
        n_max = rng.randint(1, 4)
        i_max = rng.randint(k, k + 3)
        for lam in (Fraction(0), Fraction(3, 4), Fraction(1)):
            clusters = t_vpack(bles, n_max, i_max, lam=lam, k=k)
            assert is_legal(bles, clusters, n_max, i_max)
            best = min_clusters(bles, n_max, i_max)
            assert len(clusters) >= best
            assert len(clusters) >= -(-len(bles) // n_max)
            worse += len(clusters) > best
    assert worse > 0  # the greedy is a heuristic: some instances need more clusters than the optimum


def test_cluster_is_full_when_a_ble_fits():
    """A closed cluster is full, or no unclustered BLE of that moment fits in it."""
    rng = random.Random(3)
    for _ in range(300):
        k = rng.randint(1, 3)
        bles = random_netlist(rng, rng.randint(1, 8), k, 3)
        n_max, i_max = rng.randint(1, 4), rng.randint(k, k + 2)
        clusters = t_vpack(bles, n_max, i_max, k=k)
        later: set[int] = set(range(len(bles)))
        for c in clusters:
            later -= set(c)
            if len(c) < n_max:
                assert all(len(external_inputs(bles, set(c) | {b})) > i_max for b in later)


def test_rejects_too_wide_ble():
    bles = [Ble(("a", "b", "c"), "o")]
    try:
        t_vpack(bles, 2, 2)
    except ValueError:
        return
    raise AssertionError("expected ValueError")
