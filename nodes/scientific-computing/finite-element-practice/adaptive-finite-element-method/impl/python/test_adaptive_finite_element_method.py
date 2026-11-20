# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adaptive-finite-element-method/. The authors are listed in prov/ZK2C1A.jsonl.

import itertools
import math
import random

from adaptive_finite_element_method import (afem, dorfler_mark, energy_error, estimate,
                                            l_shape_exact, l_shape_gradient, l_shape_mesh,
                                            refine_nvb, solve_p1, square_mesh)


def zero(x, y):
    return 0.0


def one(x, y):
    return 1.0


def free_nodes(coords, boundary):
    return len(coords) - len({v for e in boundary for v in e})


def conforming(elements, boundary):
    count = {}
    for z in elements:
        for r in range(3):
            a, b = z[r], z[(r + 1) % 3]
            e = (min(a, b), max(a, b))
            count[e] = count.get(e, 0) + 1
    bset = {(min(a, b), max(a, b)) for a, b in boundary}
    return all(c == 2 or (c == 1 and e in bset) for e, c in count.items()) and \
        all(count.get(e) == 1 for e in bset)


def fitted_slope(history):
    pts = []
    for coords, elements, boundary, U, _ in history:
        n = free_nodes(coords, boundary)
        if n > 30:
            pts.append((math.log(n), math.log(energy_error(coords, elements, U, l_shape_gradient))))
    mx = sum(p[0] for p in pts) / len(pts)
    my = sum(p[1] for p in pts) / len(pts)
    return sum((x - mx) * (y - my) for x, y in pts) / sum((x - mx) ** 2 for x, _ in pts)


def test_hand_example_one_free_node():
    coords, elements, boundary = square_mesh()
    coords, elements, boundary = refine_nvb(coords, elements, boundary, [0, 1])
    assert coords[4] == (0.5, 0.5) and len(elements) == 4
    U = solve_p1(coords, elements, boundary, one, zero)
    assert abs(U[4] - 1 / 12) < 1e-14
    eta2 = estimate(coords, elements, U, one)
    assert all(abs(v - (1 / 16 + math.sqrt(2) / 36)) < 1e-14 for v in eta2)
    assert len(dorfler_mark(eta2, 0.5)) == 2  # four equal indicators: two reach one half


def test_linear_solution_is_reproduced_and_estimator_vanishes():
    def u(x, y):
        return 1 + 2 * x - 3 * y

    mesh = square_mesh()
    rng = random.Random(5)
    coords, elements, boundary = mesh
    for _ in range(5):
        marked = [t for t in range(len(elements)) if rng.random() < 0.4] or [0]
        coords, elements, boundary = refine_nvb(coords, elements, boundary, marked)
    U = solve_p1(coords, elements, boundary, zero, u, tol=1e-13)
    assert max(abs(U[v] - u(*coords[v])) for v in range(len(coords))) < 1e-10
    assert max(estimate(coords, elements, U, zero)) < 1e-18


def test_dorfler_mark_is_minimal_against_brute_force():
    rng = random.Random(11)
    for _ in range(60):
        n = rng.randint(1, 8)
        eta2 = [rng.random() ** 3 for _ in range(n)]
        theta = rng.choice([0.2, 0.5, 0.8, 0.95])
        marked = dorfler_mark(eta2, theta)
        assert len(set(marked)) == len(marked)
        assert sum(eta2[t] for t in marked) >= theta * sum(eta2) - 1e-15
        best = min(k for k in range(1, n + 1)
                   for s in itertools.combinations(range(n), k)
                   if sum(eta2[t] for t in s) >= theta * sum(eta2))
        assert len(marked) == best


def test_meshes_stay_conforming_and_area_is_kept():
    history = afem(l_shape_mesh(), zero, l_shape_exact, theta=0.5, max_nodes=300)
    for coords, elements, boundary, _, eta2 in history:
        assert conforming(elements, boundary)
        assert len(eta2) == len(elements)
        total = 0.0
        for z in elements:
            (x0, y0), (x1, y1), (x2, y2) = (coords[v] for v in z)
            total += abs((x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)) / 2
        assert abs(total - 3.0) < 1e-12


def test_l_shape_adaptive_rate_beats_uniform():
    uniform = afem(l_shape_mesh(), zero, l_shape_exact, theta=1.0, max_nodes=600)
    adaptive = afem(l_shape_mesh(), zero, l_shape_exact, theta=0.5, max_nodes=600)
    su, sa = fitted_slope(uniform), fitted_slope(adaptive)
    assert -0.36 < su < -0.26  # theory for uniform meshes: N^(-1/3)
    assert -0.56 < sa < -0.44  # optimal for P1 in 2D: N^(-1/2)
    for coords, elements, boundary, U, eta2 in adaptive:
        err = energy_error(coords, elements, U, l_shape_gradient)
        assert 1.0 < math.sqrt(sum(eta2)) / err < 4.5  # measured effectivity 2.6 to 3.7
