# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fw-cadis/. The authors are listed in prov/GNWTPH.jsonl.
import random

import pytest

from fw_cadis import bin_totals, fw_cadis_parameters, relative_errors, run_monte_carlo, sn_solve

L, M, B, C = 16.0, 64, 16, 0.5
H = L / M
Q = [1.0 if 30 <= i < 34 else 0.0 for i in range(M)]  # source in [7.5, 8.5]


def reference_bins():
    """Bin totals on a mesh 4 times finer with S_32, per source particle."""
    m = 4 * M
    q = [1.0 if 120 <= i < 136 else 0.0 for i in range(m)]  # density 1 on [7.5, 8.5]
    return bin_totals(sn_solve(q, L, 1.0, C, order=32), L / m, B)


def test_adjoint_source_is_the_inverse_forward_estimate():
    p = fw_cadis_parameters(Q, L, 1.0, C, B)
    t = p["bin_estimate"]
    assert t == pytest.approx(bin_totals(p["forward"], H, B))
    assert t[0] == pytest.approx(t[-1], rel=1e-9) and t[7] == pytest.approx(t[8], rel=1e-9)  # symmetric
    # the adjoint solve with q+ = 1 / T_j reproduces R = <q, phi+> = <q+, phi> = number of bins
    q_adj = [1.0 / t[i // (M // B)] for i in range(M)]
    forward = sum(a * f * H for a, f in zip(q_adj, p["forward"]))
    assert p["response"] == pytest.approx(forward, rel=1e-9)
    assert forward == pytest.approx(B, rel=1e-12)


def test_consistent_birth_weights():
    p = fw_cadis_parameters(Q, L, 1.0, C, B)
    assert sum(p["source_pdf"]) == pytest.approx(1.0, abs=1e-12)
    for i in range(M):
        assert p["birth_weight"][i] * p["source_pdf"][i] == pytest.approx(p["q"][i] * H, abs=1e-15)
        assert p["lower"][i] < p["target"][i] < p["upper"][i]


def test_deterministic_estimate_close_to_fine_reference():
    p = fw_cadis_parameters(Q, L, 1.0, C, B)
    for a, b in zip(p["bin_estimate"], reference_bins()):
        assert a == pytest.approx(b, rel=0.06)


def test_means_agree_with_reference():
    ref = reference_bins()
    p = fw_cadis_parameters(Q, L, 1.0, C, B)
    m, e, _ = run_monte_carlo(3000, L, 1.0, C, B, random.Random(21), params=p)
    for j in range(B):
        assert abs(m[j] - ref[j]) < 4.0 * e[j] + 0.01 * ref[j]
    m, e, _ = run_monte_carlo(20000, L, 1.0, C, B, random.Random(22), q=Q)
    for j in range(B):
        assert abs(m[j] - ref[j]) < 4.0 * e[j] + 0.01 * ref[j]


def test_more_uniform_errors_than_analog():
    # Measured with fixed seeds: the worst bin has a far better figure of merit with FW-CADIS.
    p = fw_cadis_parameters(Q, L, 1.0, C, B)
    m_f, e_f, fl_f = run_monte_carlo(3000, L, 1.0, C, B, random.Random(5), params=p)
    m_a, e_a, fl_a = run_monte_carlo(20000, L, 1.0, C, B, random.Random(5), q=Q)
    r_f, r_a = relative_errors(m_f, e_f), relative_errors(m_a, e_a)
    assert max(r_f) / min(r_f) < max(r_a) / min(r_a) / 3.0
    assert 1.0 / (max(r_f) ** 2 * fl_f) > 5.0 / (max(r_a) ** 2 * fl_a)
