# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/extended-finite-element-method/. The authors are listed in prov/R1XMNZ.jsonl.

import random

import scimat
from extended_finite_element_method import XFEM1D, exact_piecewise_linear


def uniform(n):
    return [i / n for i in range(n + 1)]


def max_error(model, u, c):
    pts = [j / 97 for j in range(98)]
    return max(abs(model.value(x)[0] - u(x)) for x in pts if abs(x - c) > 1e-12)


def interface_load_solution(c, e1, e2):
    """Exact derivative for -(E u')' = 1, u(0) = u(1) = 0, with a material interface at c."""
    s0 = (c * c / (2 * e1) + (1 - c * c) / (2 * e2)) / (c / e1 + (1 - c) / e2)
    return lambda x: (s0 - x) / (e1 if x < c else e2)


def test_hand_example_one_element_cohesive_crack():
    model = XFEM1D([0.0, 1.0], 0.5, "crack", 1.0, 1.0, u0=0.0, uL=1.0, k=2.0)
    assert all(abs(a - b) < 1e-15 for a, b in zip(model.u, [0.0, 1.0, 1 / 3, 1 / 3]))
    k = model.stiffness
    assert abs(k[2][2] - 1.0) < 1e-15 and abs(k[2][3] - 0.5) < 1e-15 and abs(k[2][1] + 0.5) < 1e-15
    # the jump of the solution is sigma / k with sigma = 2/3
    left, right = model.value(0.5 - 1e-12)[0], model.value(0.5 + 1e-12)[0]
    assert abs(right - left - 1 / 3) < 1e-10


def test_hand_example_two_elements_interface():
    exact, _, sigma = exact_piecewise_linear(0.3, 1.0, 4.0, 0.0, 1.0)
    assert abs(sigma - 40 / 19) < 1e-14
    xfem = XFEM1D([0.0, 0.5, 1.0], 0.3, "interface", 1.0, 4.0, u0=0.0, uL=1.0)
    plain = XFEM1D([0.0, 0.5, 1.0], 0.3, "none", 1.0, 4.0, u0=0.0, uL=1.0)
    assert abs(xfem.u[1] - 14 / 19) < 1e-14
    assert abs(plain.u[1] - 20 / 31) < 1e-14
    assert max_error(xfem, exact, 0.3) < 1e-14


def test_piecewise_linear_solutions_are_exact_for_any_position():
    rng = random.Random(11)
    for _ in range(40):
        n = rng.randint(2, 30)
        c = rng.uniform(0.02, 0.98)
        if min(abs(c - i / n) for i in range(n + 1)) < 1e-6:
            continue
        e1, e2 = rng.uniform(0.5, 5), rng.uniform(0.5, 5)
        u0, ul = rng.uniform(-1, 1), rng.uniform(-1, 1)
        for kind, k in (("interface", None), ("crack", rng.uniform(0.5, 10))):
            exact, du, _ = exact_piecewise_linear(c, e1, e2, u0, ul, k=k)
            model = XFEM1D(uniform(n), c, kind, e1, e2, u0=u0, uL=ul, k=k)
            assert max_error(model, exact, c) < 1e-12
            assert model.energy_error(du) < 1e-11


def test_shifted_enrichment_keeps_nodal_values():
    c, k = 0.43, 2.5
    exact, _, _ = exact_piecewise_linear(c, 2.0, 1.0, 0.0, 1.0, k=k)
    model = XFEM1D(uniform(7), c, "crack", 2.0, 1.0, u0=0.0, uL=1.0, k=k)
    for i, x in enumerate(uniform(7)):
        assert abs(model.u[i] - exact(x)) < 1e-14


def test_only_the_cut_element_carries_enrichment():
    model = XFEM1D(uniform(6), 0.4, "interface", 1.0, 3.0, u0=0.0, uL=1.0)
    assert model.cut == 2 and model.enriched == [2, 3] and model.ndof == 9
    for e in range(6):
        dofs, _, _ = model._functions(e, (e + 0.5) / 6)
        assert (len(dofs) == 4) == (e == 2)


def test_standard_elements_lose_accuracy_at_the_interface():
    c, e1, e2 = 1 / 3, 1.0, 10.0
    exact, du, _ = exact_piecewise_linear(c, e1, e2, 0.0, 1.0)
    errs = [XFEM1D(uniform(n), c, "none", e1, e2, u0=0.0, uL=1.0).energy_error(du) for n in (4, 16, 64, 256)]
    rates = [r / 2 for r in scimat.observed_order(errs)]
    assert all(abs(r - 0.5) < 0.06 for r in rates)
    assert errs[-1] > 0.07


def test_convergence_with_a_load():
    c, e1, e2 = 1 / 3, 1.0, 10.0
    du = interface_load_solution(c, e1, e2)
    xfem, plain = [], []
    for n in (4, 16, 64, 256):
        nodes = uniform(n)
        xfem.append(XFEM1D(nodes, c, "interface", e1, e2, f=lambda x: 1.0).energy_error(du))
        plain.append(XFEM1D(nodes, c, "none", e1, e2, f=lambda x: 1.0).energy_error(du))
    rx = [r / 2 for r in scimat.observed_order(xfem)]
    rp = [r / 2 for r in scimat.observed_order(plain)]
    assert rx[-1] > 0.98 and rp[-1] < 0.6
    assert plain[-1] > 3 * xfem[-1]


def test_cohesive_crack_with_a_load():
    c, e1, e2, k = 1 / 3, 1.0, 10.0, 5.0
    s1 = (c * c / (2 * e1) + (1 - c * c) / (2 * e2) + c / k) / (c / e1 + (1 - c) / e2 + 1 / k)

    def du(x):
        return (s1 - x) / (e1 if x < c else e2)

    errs = [XFEM1D(uniform(n), c, "crack", e1, e2, f=lambda x: 1.0, k=k).energy_error(du) for n in (4, 16, 64)]
    rates = [r / 2 for r in scimat.observed_order(errs)]
    assert rates[-1] > 0.95
    model = XFEM1D(uniform(64), c, "crack", e1, e2, f=lambda x: 1.0, k=k)
    jump = model.value(c + 1e-12)[0] - model.value(c - 1e-12)[0]
    assert abs(jump - (s1 - c) / k) < 1e-6


def test_stiffness_is_symmetric():
    model = XFEM1D(uniform(5), 0.47, "crack", 1.0, 2.0, u0=0.0, uL=1.0, k=4.0)
    kmat = model.stiffness
    n = len(kmat)
    assert all(abs(kmat[i][j] - kmat[j][i]) < 1e-14 for i in range(n) for j in range(n))


def test_conditioning_degrades_near_a_node():
    diag, errs = [], []
    for eps in (1e-2, 1e-6, 1e-10):
        c = 0.5 + eps
        exact, _, _ = exact_piecewise_linear(c, 1.0, 10.0, 0.0, 1.0)
        model = XFEM1D(uniform(4), c, "interface", 1.0, 10.0, u0=0.0, uL=1.0)
        diag.append(model.stiffness[6][6])
        errs.append(max_error(model, exact, c))
    assert diag[0] > 1e-3 and diag[-1] < 1e-17
    assert errs[0] < 1e-14 and errs[-1] > 1e-11
