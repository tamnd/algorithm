# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multiscale-finite-element-method/. The authors are listed in prov/6V214F.jsonl.
import math
import random
from fractions import Fraction

from multiscale_finite_element_method import energy_norm, fine_solve_1d, local_basis, msfem_1d


def oscillating(N, eps):
    return [2 + math.sin(2 * math.pi * (j + 0.5) / N / eps) for j in range(N)]


def test_coarse_values_equal_the_fine_solution_exactly():
    rng = random.Random(11)
    N, M = 12, 3
    a = [Fraction(rng.randint(1, 20), rng.randint(1, 5)) for _ in range(N)]
    f = [Fraction(rng.randint(-5, 5), rng.randint(1, 3)) for _ in range(N + 1)]
    U, u_fine = msfem_1d(a, f, M)
    ref = fine_solve_1d(a, f)
    n = N // M
    assert U == [ref[i * n] for i in range(M + 1)]
    assert u_fine[0] == 0 and u_fine[N] == 0


def test_local_basis_is_discrete_harmonic_with_constant_flux():
    a = [Fraction(1), Fraction(4), Fraction(1), Fraction(4)]
    h = Fraction(1, 8)
    phi = local_basis(a, h)
    flux = [a[k] * (phi[k + 1] - phi[k]) / h for k in range(4)]
    assert phi[0] == 0 and phi[-1] == 1
    assert len(set(flux)) == 1
    # the flux is the harmonic mean over the element divided by its length
    assert flux[0] == Fraction(8, 5) / (4 * h)


def test_energy_error_is_of_order_H_and_below_the_bound():
    N, eps = 512, 1 / 32
    a = oscillating(N, eps)
    f = [1.0] * (N + 1)
    ref = fine_solve_1d(a, f)
    errors = []
    for M in (4, 8, 16, 32):
        _, u = msfem_1d(a, f, M)
        err = energy_norm(a, [u[j] - ref[j] for j in range(N + 1)])
        bound = (1 / M) / (math.pi * math.sqrt(min(a))) * 1.0
        assert err <= bound
        errors.append(err)
    for e1, e2 in zip(errors, errors[1:]):
        assert 1.8 < e1 / e2 < 2.2


def test_standard_p1_on_a_coarse_mesh_is_wrong_and_msfem_is_not():
    N, eps, M = 512, 1 / 16, 8
    a = oscillating(N, eps)
    f = [1.0] * (N + 1)
    ref = fine_solve_1d(a, f)
    n = N // M
    U_ms, _ = msfem_1d(a, f, M)
    U_p1, _ = msfem_1d(a, f, M, kind="linear")
    err_ms = max(abs(U_ms[i] - ref[i * n]) for i in range(M + 1))
    err_p1 = max(abs(U_p1[i] - ref[i * n]) for i in range(M + 1))
    assert err_ms < 1e-12
    # P1 sees the arithmetic mean 2 instead of the harmonic mean sqrt(3)
    assert abs(U_p1[M // 2] / ref[N // 2] - math.sqrt(3) / 2) < 1e-3
    assert err_p1 > 0.005


def test_basis_is_a_partition_of_unity_and_monotone():
    rng = random.Random(5)
    a = [rng.uniform(0.1, 10.0) for _ in range(16)]
    phi = local_basis(a, 1 / 64)
    assert all(phi[k] < phi[k + 1] for k in range(16))
    U, u = msfem_1d(a * 4, [0.0] * 65, 4)
    assert U == [0.0] * 5 and u == [0.0] * 65
