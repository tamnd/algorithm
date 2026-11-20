# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/goldstein-branch-cut/. The authors are listed in prov/5RF5DV.jsonl.

from itertools import combinations, product
import math
import random

from goldstein_branch_cut import (branch_cuts, cut_components, flood_fill_unwrap, goldstein_unwrap, l0_cost, residues,
                                  wrap)

TWO_PI = 2.0 * math.pi


def _random_psi(rng, m, n):
    return [[rng.uniform(-math.pi, math.pi) for _ in range(n)] for _ in range(m)]


def _min_l0(psi):
    """Exact minimum L0 cost over all congruent unwrappings of a tiny image.

    A congruent unwrapping changes the wrapped difference of edge e by 2 pi n_e
    with integers n_e whose sum around every square cancels its residue. Search
    the supports of increasing size with n_e in {-2, -1, 1, 2}.
    """
    m, n = len(psi), len(psi[0])
    q = residues(psi)
    edges = [('h', i, j) for i in range(m) for j in range(n - 1)] + [('v', i, j) for i in range(m - 1) for j in range(n)]
    faces = []
    for r in range(m - 1):
        for c in range(n - 1):
            faces.append(({('h', r, c): 1, ('v', r, c + 1): 1, ('h', r + 1, c): -1, ('v', r, c): -1}, -q[r][c]))
    for size in range(len(edges) + 1):
        for support in combinations(edges, size):
            for values in product((-2, -1, 1, 2), repeat=size):
                nmap = dict(zip(support, values))
                if all(sum(sgn * nmap.get(e, 0) for e, sgn in f.items()) == want for f, want in faces):
                    return size
    raise AssertionError("unreachable")


def test_wrap() -> None:
    assert abs(wrap(3 * math.pi / 2) + math.pi / 2) < 1e-15
    assert abs(wrap(-math.pi) - math.pi) < 1e-15


def test_a_vortex_has_one_residue() -> None:
    psi = [[math.atan2(i - 1.5, j - 1.5) for j in range(4)] for i in range(4)]
    q = residues(psi)
    assert q[1][1] == 1
    assert sum(abs(v) for row in q for v in row) == 1


def test_no_residues_gives_the_true_phase() -> None:
    m, n = 7, 8
    true = [[0.8 * j - 0.6 * i + 1.2 * math.cos(0.5 * i) * math.sin(0.4 * j) + 5.0 for j in range(n)] for i in range(m)]
    psi = [[wrap(v) for v in row] for row in true]
    phi, blocked, _ = goldstein_unwrap(psi)
    assert not blocked
    k = (phi[0][0] - true[0][0]) / TWO_PI
    assert abs(k - round(k)) < 1e-12
    for i in range(m):
        for j in range(n):
            assert abs(phi[i][j] - true[i][j] - TWO_PI * round(k)) < 1e-9


def test_free_edges_keep_the_wrapped_difference_and_the_result_is_congruent() -> None:
    for seed in range(7401, 7406):
        rng = random.Random(seed)
        m, n = 8, 9
        psi = _random_psi(rng, m, n)
        phi, blocked, region = goldstein_unwrap(psi)
        for i in range(m):
            for j in range(n):
                k = (phi[i][j] - psi[i][j]) / TWO_PI
                assert abs(k - round(k)) < 1e-9
                if j + 1 < n and ('h', i, j) not in blocked:
                    assert region[i][j] == region[i][j + 1]
                    assert abs(phi[i][j + 1] - phi[i][j] - wrap(psi[i][j + 1] - psi[i][j])) < 1e-9
                if i + 1 < m and ('v', i, j) not in blocked:
                    assert abs(phi[i + 1][j] - phi[i][j] - wrap(psi[i + 1][j] - psi[i][j])) < 1e-9


def test_every_cut_component_is_balanced_or_touches_the_border() -> None:
    for seed in range(7411, 7416):
        rng = random.Random(seed)
        psi = _random_psi(rng, 9, 9)
        q = residues(psi)
        for max_box in (1, 2, None):
            blocked = branch_cuts(q, max_box)
            comps = cut_components(q, blocked)
            assert comps
            for charge, border, _ in comps:
                assert charge == 0 or border


def test_box_size_decides_between_a_pair_cut_and_border_cuts() -> None:
    # Two vortices of opposite sign, four squares apart, in a 9 x 12 image.
    m, n = 9, 12
    psi = [[wrap(math.atan2(i - 4.5, j - 3.5) - math.atan2(i - 4.5, j - 7.5)) for j in range(n)] for i in range(m)]
    q = residues(psi)
    assert q[4][3] == 1 and q[4][7] == -1
    assert sum(abs(v) for row in q for v in row) == 2
    pair = branch_cuts(q, None)
    assert len(pair) == 4
    border = branch_cuts(q, 1)
    assert len(border) == 8
    for blocked in (pair, border):
        phi, _ = flood_fill_unwrap(psi, blocked)
        assert l0_cost(phi, psi) <= len(blocked)


def test_an_adjacent_dipole_is_cut_optimally() -> None:
    # The edge between (1, 2) and (2, 2) has the true difference 4, which wraps to
    # 4 - 2 pi: the two squares beside it get charges -1 and +1.
    psi = [[0.0] * 5 for _ in range(4)]
    psi[1][2], psi[2][2] = -2.0, 2.0
    q = residues(psi)
    assert q[1][1] == -1 and q[1][2] == 1
    assert sum(abs(v) for row in q for v in row) == 2
    phi, blocked, _ = goldstein_unwrap(psi)
    assert blocked == {('v', 1, 2)}
    assert l0_cost(phi, psi) == 1 == _min_l0(psi)
    assert abs(phi[2][2] - phi[1][2] - 4.0) < 1e-12


def test_never_below_the_brute_force_minimum_on_tiny_grids() -> None:
    rng = random.Random(7421)
    checked = 0
    while checked < 12:
        psi = _random_psi(rng, 3, 4)
        if all(v == 0 for row in residues(psi) for v in row):
            continue
        phi, _, _ = goldstein_unwrap(psi)
        assert l0_cost(phi, psi) >= _min_l0(psi) >= 1
        checked += 1


def test_greedy_pairing_is_not_optimal() -> None:
    # Residues +1 at (0, 2), -1 at (1, 1) and +1 at (1, 0). Goldstein pairs (0, 2)
    # with (1, 1) by a cut of two edges and sends (1, 0) to the border with one
    # more; pairing (1, 0) with (1, 1) and (0, 2) with the top border needs two.
    psi = [[1.86, -1.67, 1.17, -0.71], [-2.62, -0.43, -1.89, 2.2], [2.24, 1.74, 2.19, 2.8]]
    assert residues(psi) == [[0, 0, 1], [1, -1, 0]]
    phi, blocked, _ = goldstein_unwrap(psi)
    assert blocked == {('h', 1, 2), ('v', 1, 2), ('h', 2, 0)}
    assert l0_cost(phi, psi) == 3
    assert _min_l0(psi) == 2


def test_another_seed_order_changes_each_region_by_a_constant() -> None:
    rng = random.Random(7431)
    m, n = 8, 8
    psi = _random_psi(rng, m, n)
    phi, blocked, region = goldstein_unwrap(psi)
    seeds = [(i, j) for i in range(m - 1, -1, -1) for j in range(n - 1, -1, -1)]
    phi2, region2 = flood_fill_unwrap(psi, blocked, seeds)
    offset = {}
    for i in range(m):
        for j in range(n):
            d = phi2[i][j] - phi[i][j]
            assert abs(d / TWO_PI - round(d / TWO_PI)) < 1e-9
            lab = region[i][j]
            offset.setdefault(lab, d)
            assert abs(offset[lab] - d) < 1e-9
            assert (region2[i][j] == region2[0][0]) == (lab == region[0][0])
