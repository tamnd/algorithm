# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/desroziers-diagnostics/. The authors are listed in prov/YFJDYK.jsonl.

import random
from fractions import Fraction

import scimat
from desroziers_diagnostics import desroziers, expected_statistics, tune


def frac(rng, lo=-2, hi=2, den=4):
    return Fraction(rng.randint(lo * den, hi * den), den)


def frac_spd(rng, n):
    L = [[frac(rng, -1, 1) for _ in range(n)] for _ in range(n)]
    S = scimat.matmul(L, scimat.transpose(L))
    for i in range(n):
        S[i][i] += Fraction(1, 2)
    return S


def max_abs_diff(a, b):
    return max(abs(x - y) for ra, rb in zip(a, b) for x, y in zip(ra, rb))


def twin(rng, H, B, R, count):
    """Innovations d = H e_b + e_o with e_b ~ N(0, B) and e_o ~ N(0, R)."""
    LB, LR = scimat.cholesky(B), scimat.cholesky(R)
    n, p = len(B), len(R)
    out = []
    for _ in range(count):
        eb = scimat.matvec(LB, [rng.gauss(0, 1) for _ in range(n)])
        eo = scimat.matvec(LR, [rng.gauss(0, 1) for _ in range(p)])
        out.append(scimat.add(scimat.matvec(H, eb), eo))
    return out


H = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [0.5, 0.5, 0.0]]
B = [[1.0, 0.5, 0.2], [0.5, 1.0, 0.5], [0.2, 0.5, 1.0]]
R = [[0.5, 0.0, 0.0, 0.0], [0.0, 0.5, 0.1, 0.0], [0.0, 0.1, 0.5, 0.0], [0.0, 0.0, 0.0, 0.3]]
HBHT = scimat.matmul(scimat.matmul(H, B), scimat.transpose(H))


def test_expected_values_are_exact_with_correct_statistics():
    rng = random.Random(81)
    for _ in range(20):
        n, p = rng.randint(1, 3), rng.randint(1, 4)
        Hm = [[frac(rng) for _ in range(n)] for _ in range(p)]
        Bm, Rm = frac_spd(rng, n), frac_spd(rng, p)
        hbht = scimat.matmul(scimat.matmul(Hm, Bm), scimat.transpose(Hm))
        oa_ob, ab_ob, ab_oa, ob_ob = expected_statistics(hbht, Rm, hbht, Rm)
        # Brute force: the analysis error covariance A = (I - K H) B with K = B H^T S^-1.
        S = scimat.add(hbht, Rm)
        K = scimat.transpose(scimat.solve(S, scimat.matmul(Hm, Bm)))
        A = scimat.sub(Bm, scimat.matmul(K, scimat.matmul(Hm, Bm)))
        hah = scimat.matmul(scimat.matmul(Hm, A), scimat.transpose(Hm))
        assert oa_ob == Rm and ab_ob == hbht and ab_oa == hah and ob_ob == S


def test_sample_estimates_recover_r_and_hbht():
    rng = random.Random(82)
    ds = twin(rng, H, B, R, 10000)
    r, hb, ha, s = desroziers(ds, HBHT, R)
    assert max_abs_diff(r, R) < 0.05
    assert max_abs_diff(hb, HBHT) < 0.05
    assert max_abs_diff(s, scimat.add(HBHT, R)) < 0.08
    _, _, hah, _ = expected_statistics(HBHT, R, HBHT, R)
    assert max_abs_diff(ha, hah) < 0.05


def test_sample_estimates_follow_the_formula_with_wrong_statistics():
    # The analysis uses R twice too large; the estimate converges to Rt St^-1 S, not to R.
    rng = random.Random(83)
    ds = twin(rng, H, B, R, 10000)
    r_wrong = scimat.scale(2.0, R)
    r_est, hb_est, _, _ = desroziers(ds, HBHT, r_wrong)
    oa_ob, ab_ob, _, _ = expected_statistics(HBHT, R, HBHT, r_wrong)
    assert max_abs_diff(r_est, oa_ob) < 0.05 and max_abs_diff(hb_est, ab_ob) < 0.05
    assert max_abs_diff(oa_ob, R) > 0.2


def test_scalar_iteration_with_correct_b():
    # HBH^T = R = 1 and the first guess of R is 2: R_j = 2^(j+1) / (2^(j+1) - 1).
    steps = tune([[1]], [[1]], [[1]], [[Fraction(2)]], 6)
    for j, (_, r) in enumerate(steps):
        assert r[0][0] == Fraction(2 ** (j + 1), 2 ** (j + 1) - 1)


def test_wrong_b_gives_a_wrong_r():
    # Tuning R alone with HBH^T assumed 3/2 instead of 1 converges to R = S - 3/2 = 1/2,
    # with the error multiplied by about 3/4 per step.
    steps = tune([[1]], [[1]], [[1.5]], [[1.0]], 150)
    assert abs(steps[-1][1][0][0] - 0.5) < 1e-12


def test_joint_tuning_keeps_the_ratio_of_the_first_guess():
    # Scalar case: one joint step makes HBH^T + R equal to S and keeps the ratio HBH^T : R.
    steps = tune([[1]], [[1]], [[Fraction(3)]], [[Fraction(1)]], 4, tune_b=True)
    for hb, r in steps[1:]:
        assert hb[0][0] + r[0][0] == 2 and hb[0][0] == 3 * r[0][0]


def test_matrix_iteration_converges_with_correct_b():
    hbht = [[2.0, 1.0], [1.0, 2.0]]
    r_true = [[1.0, 0.0], [0.0, 0.5]]
    steps = tune(hbht, r_true, hbht, [[3.0, 0.0], [0.0, 3.0]], 200)
    assert max_abs_diff(steps[-1][1], r_true) < 1e-9
