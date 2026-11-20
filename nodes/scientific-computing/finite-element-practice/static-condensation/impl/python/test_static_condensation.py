# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/static-condensation/. The authors are listed in prov/G6BEQJ.jsonl.

import random

import scimat
import static_condensation as SC


def random_spd(n, rng):
    a = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
    m = scimat.matmul(scimat.transpose(a), a)
    for i in range(n):
        m[i][i] += 0.5
    return m


def test_hand_example_p2_condenses_to_p1():
    h = 0.25
    K, F = SC.p2_element(h)
    boundary, S, g, XK, XF = SC.condense(K, F, [2])
    assert boundary == [0, 1]
    want = [[1 / h, -1 / h], [-1 / h, 1 / h]]
    assert max(abs(S[i][j] - want[i][j]) for i in range(2) for j in range(2)) < 1e-12
    assert max(abs(v - h / 2) for v in g) < 1e-15
    # the middle value is the mean of the ends plus h^2 f / 8
    assert abs(SC.recover(XK, XF, [1.0, 3.0])[0] - (2.0 + h * h / 8)) < 1e-14


def test_p2_mesh_matches_full_solve_and_exact_solution():
    for n in (1, 3, 8):
        ndof, elements = SC.p2_mesh(n)
        fixed = {0: 0.0, n: 0.0}
        a = SC.solve_condensed(ndof, elements, fixed)
        b = SC.solve_full(ndof, elements, fixed)
        assert max(abs(x - y) for x, y in zip(a, b)) < 1e-12
        for e in range(n + 1):  # vertices
            x = e / n
            assert abs(a[e] - x * (1 - x) / 2) < 1e-12
        for e in range(n):  # midpoints: P2 is exact for the quadratic solution
            x = (e + 0.5) / n
            assert abs(a[n + 1 + e] - x * (1 - x) / 2) < 1e-12


def test_random_elements_match_full_solve():
    rng = random.Random(7)
    for _ in range(20):
        ne = rng.randint(1, 5)
        # a chain: element e has boundary unknowns e and e + 1 and its own interior ones
        ndof = ne + 1
        elements = []
        for e in range(ne):
            ni = rng.randint(0, 4)
            dofs = [e, e + 1] + list(range(ndof, ndof + ni))
            ndof += ni
            K = random_spd(2 + ni, rng)
            F = [rng.uniform(-1, 1) for _ in range(2 + ni)]
            elements.append((dofs, K, F, list(range(2, 2 + ni))))
        fixed = {0: rng.uniform(-1, 1)}
        a = SC.solve_condensed(ndof, elements, fixed)
        b = SC.solve_full(ndof, elements, fixed)
        assert max(abs(x - y) for x, y in zip(a, b)) < 1e-9


def test_schur_complement_is_spd_and_minimizes_energy():
    rng = random.Random(1)
    K = random_spd(6, rng)
    F = [0.0] * 6
    boundary, S, _, XK, XF = SC.condense(K, F, [3, 4, 5])
    scimat.cholesky(S)  # raises if S is not positive definite
    uB = [rng.uniform(-1, 1) for _ in boundary]
    uI = SC.recover(XK, XF, uB)
    u = uB + uI  # boundary = [0, 1, 2], interior = [3, 4, 5]

    def energy(v):
        return scimat.dot(v, scimat.matvec(K, v))

    sb = scimat.dot(uB, scimat.matvec(S, uB))
    assert abs(energy(u) - sb) < 1e-12
    for _ in range(20):  # any other interior values give a larger energy
        other = uB + [x + rng.uniform(-0.1, 0.1) for x in uI]
        assert energy(other) > sb
