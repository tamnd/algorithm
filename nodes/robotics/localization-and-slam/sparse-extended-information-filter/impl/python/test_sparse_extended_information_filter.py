# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sparse-extended-information-filter/. The authors are listed in prov/1KKHWC.jsonl.

import copy
import math
import random

import rbm
import robest
from sparse_extended_information_filter import Seif, measure, motion_offset, sparsify_info

ALPHAS = (0.01, 0.005, 0.005, 0.01)
Q = [[0.01, 0.0], [0.0, 0.0009]]
LANDMARKS = [[2.0, 2.0], [4.0, -1.0], [6.0, 2.5], [8.0, -1.5], [10.0, 2.0], [5.0, 4.0], [3.0, -3.0], [9.0, 4.0], [1.0, -2.0], [7.0, 0.5]]


def max_abs_diff(a, b):
    if isinstance(a[0], list):
        return max(abs(x - y) for ra, rb in zip(a, b) for x, y in zip(ra, rb))
    return max(abs(x - y) for x, y in zip(a, b))


def small_filter(max_active=10):
    f = Seif([0.0, 0.0, 0.1], [[0.01, 0.0, 0.0], [0.0, 0.01, 0.0], [0.0, 0.0, 0.01]], max_active, ALPHAS, Q)
    f.update([[2.0, 0.5], [3.0, -0.4], [2.5, 0.1], [1.5, 1.0]], [0, 1, 2, 3])
    f.recover_mean_exact()
    return f


def pose_links(f):
    """Return the slots of the landmarks that Omega links to the pose."""
    out = []
    for s in range(len(f.ids)):
        j = f.index(s)
        if any(f.omega[a][c] != 0.0 for a in range(3) for c in (j, j + 1)):
            out.append(s)
    return out


def test_motion_equals_the_dense_information_filter_prediction():
    f = small_filter()
    omega, mu = copy.deepcopy(f.omega), list(f.mu)
    n = len(mu)
    u = (0.5, 0.2)
    f.motion(u, 1.0)
    delta, g, vj = motion_offset(mu, u, 1.0)
    v, w = u
    m = [[ALPHAS[0] * v * v + ALPHAS[1] * w * w, 0.0], [0.0, ALPHAS[2] * v * v + ALPHAS[3] * w * w]]
    r = rbm.mul(rbm.mul(vj, m), rbm.transpose(vj))
    big_g, big_r = rbm.eye(n), rbm.zeros(n, n)
    for a in range(3):
        for b in range(3):
            big_g[a][b] = g[a][b]
            big_r[a][b] = r[a][b]
    want = rbm.inv(rbm.add(rbm.mul(rbm.mul(big_g, rbm.inv(omega)), rbm.transpose(big_g)), big_r))
    mu_bar = [mu[i] + (delta[i] if i < 3 else 0.0) for i in range(n)]
    assert max_abs_diff(f.omega, want) < 1e-10
    assert max_abs_diff(f.xi, rbm.matvec(want, mu_bar)) < 1e-10
    assert max_abs_diff(f.mu, mu_bar) == 0.0


def test_update_changes_only_the_pose_and_the_landmark():
    f = small_filter()
    f.motion((0.5, 0.2), 1.0)
    before, xi = copy.deepcopy(f.omega), list(f.xi)
    f.update([[2.4, 0.2]], [1])
    touched = {0, 1, 2, f.index(1), f.index(1) + 1}
    n = len(f.mu)
    for r in range(n):
        for c in range(n):
            if r not in touched or c not in touched:
                assert f.omega[r][c] == before[r][c]
        if r not in touched:
            assert f.xi[r] == xi[r]


def marginal_info(m, idx_out, n):
    """Full size: M - M[:, out] M[out, out]^(-1) M[out, :], the information after the variables out are removed."""
    if not idx_out:
        return [list(row) for row in m]
    moo = [[m[r][c] for c in idx_out] for r in idx_out]
    mxo = [[m[r][c] for c in idx_out] for r in range(n)]
    sol = rbm.solve(moo, rbm.transpose(mxo))
    return rbm.sub(m, rbm.mul(mxo, sol))


def test_sparsification_matches_the_textbook_formula():
    rng = random.Random(1)
    n = 3 + 2 * 6
    x, mp, m0 = [0, 1, 2], [11, 12, 13, 14], [7, 8, 9, 10]
    for _ in range(10):
        a = [[rng.gauss(0.0, 1.0) for _ in range(n)] for _ in range(n)]
        om = rbm.add(rbm.mul(a, rbm.transpose(a)), rbm.eye(n))
        for j in (3, 4, 5, 6):  # landmarks 0 and 1 are passive
            for i in x:
                om[i][j] = om[j][i] = 0.0
        mu = [rng.gauss(0.0, 1.0) for _ in range(n)]
        xi = rbm.matvec(om, mu)
        s = x + mp + m0
        om0 = [[om[r][c] if r in s and c in s else 0.0 for c in range(n)] for r in range(n)]
        # with om0, removing a variable that om0 does not hold is the same as fixing it
        o1 = marginal_info(om0, m0, n)
        o2 = marginal_info(om0, x + m0, n)
        o3 = marginal_info(om, x, n)
        want = rbm.add(rbm.sub(o1, o2), o3)
        got_om, got_xi = copy.deepcopy(om), list(xi)
        sparsify_info(got_om, got_xi, mu, x, mp, m0)
        assert max_abs_diff(got_om, want) < 1e-10
        assert max_abs_diff(got_xi, rbm.add(xi, rbm.matvec(rbm.sub(want, om), mu))) < 1e-9


def test_sparsification_cuts_the_links_and_keeps_the_mean():
    f = small_filter()
    f.motion((0.5, 0.2), 1.0)
    f.recover_mean_exact()
    before = copy.deepcopy(f.omega)
    mu = list(f.mu)
    f.max_active = 2
    m0 = f.sparsify()
    assert m0 == [0, 1]
    assert pose_links(f) == [2, 3]
    assert max_abs_diff(rbm.solve(f.omega, f.xi), mu) < 1e-9
    rbm.cholesky(f.omega)  # still positive definite
    n = len(mu)
    # no landmark is passive here, so the marginal of the map and the marginal of the pose with m+ do not change
    s_old, s_new = rbm.inv(before), rbm.inv(f.omega)
    mp = [0, 1, 2] + [f.index(2), f.index(2) + 1, f.index(3), f.index(3) + 1]
    assert max(abs(s_old[r][c] - s_new[r][c]) for r in mp for c in mp) < 1e-9
    lm = list(range(3, n))
    assert max(abs(s_old[r][c] - s_new[r][c]) for r in lm for c in lm) < 1e-9
    # but the covariance between the pose and the removed landmarks changes
    assert max(abs(s_old[r][c] - s_new[r][c]) for r in range(3) for c in range(3, 7)) > 1e-4


def simulate(seed, max_active, exact, steps=30, extra=2):
    rng = random.Random(seed)
    f = Seif([0.0, 0.0, 0.0], [[1e-4, 0.0, 0.0], [0.0, 1e-4, 0.0], [0.0, 0.0, 1e-4]], max_active, ALPHAS, Q)
    x = [0.0, 0.0, 0.0]
    links = []
    for t in range(steps):
        u = (0.5, 0.08 if t < steps // 2 else -0.08)
        v, w = u
        m = [[ALPHAS[0] * v * v + ALPHAS[1] * w * w, 0.0], [0.0, ALPHAS[2] * v * v + ALPHAS[3] * w * w]]
        noisy = robest.gauss_sample(rng, list(u), m)
        d, _, _ = motion_offset(x, noisy, 1.0)
        x = [x[i] + d[i] for i in range(3)]
        zs, ids = [], []
        for i, lm in enumerate(LANDMARKS):
            z = measure(x, lm)
            if z[0] < 4.0 and abs(z[1]) < 1.4:
                zs.append([z[0] + rng.gauss(0.0, 0.1), z[1] + rng.gauss(0.0, 0.03)])
                ids.append(i)
        f.motion(u, 1.0)
        f.update(zs, ids)
        f.sparsify()
        if exact:
            f.recover_mean_exact()
        else:
            f.recover_mean(extra)
        links.append(len(pose_links(f)))
    return f, x, links


def landmark_stats(f):
    sigma = rbm.inv(f.omega)
    mu = rbm.solve(f.omega, f.xi)
    nees, err = [], []
    for s, lid in enumerate(f.ids):
        j = f.index(s)
        e = [mu[j] - LANDMARKS[lid][0], mu[j + 1] - LANDMARKS[lid][1]]
        cov = [[sigma[j][j], sigma[j][j + 1]], [sigma[j + 1][j], sigma[j + 1][j + 1]]]
        nees.append(robest.mahalanobis2(e, [0.0, 0.0], cov))
        err.append(math.hypot(*e))
    return sum(nees) / len(nees), sum(err) / len(err)


def test_the_active_set_stays_bounded():
    for seed in (1, 2):
        f, _, links = simulate(seed, 3, exact=False, steps=20)
        assert max(links) <= 3
        assert len(f.ids) >= 5


def energy(f):
    """0.5 mu^T Omega mu - xi^T mu, which block coordinate descent never increases."""
    w = rbm.matvec(f.omega, f.mu)
    return 0.5 * sum(a * b for a, b in zip(f.mu, w)) - sum(a * b for a, b in zip(f.xi, f.mu))


def test_mean_recovery_descends_and_converges_slowly():
    f, _, _ = simulate(3, 3, exact=False, steps=15)
    exact = rbm.solve(f.omega, f.xi)
    last, errors = energy(f), []
    for _ in range(400):
        f.recover_mean(extra=len(f.ids))
        e = energy(f)
        assert e <= last + 1e-9
        last = e
        errors.append(max_abs_diff(f.mu, exact))
    # linear convergence, but slow: the map is strongly correlated
    assert errors[9] > 0.05
    assert errors[-1] < 2e-3
    # the exact mean is a fixed point
    f.mu = list(exact)
    f.recover_mean(extra=len(f.ids), joint=False)
    assert max_abs_diff(f.mu, exact) < 1e-9


def test_sparsification_makes_the_map_overconfident_in_simulation():
    """A measurement, not a theorem: 6 runs of 30 steps with 10 landmarks.

    Without sparsification (max_active = 100) the filter is the EIF, and the
    mean normalized landmark error is near 2, the dimension. With at most 3
    active landmarks it is larger: the reported covariance is too small for
    the real error.
    """
    full, sparse, err_full, err_sparse = [], [], [], []
    for seed in range(6):
        nees, err = landmark_stats(simulate(seed, 100, exact=True)[0])
        full.append(nees)
        err_full.append(err)
        nees, err = landmark_stats(simulate(seed, 3, exact=False)[0])
        sparse.append(nees)
        err_sparse.append(err)
    mean_full, mean_sparse = sum(full) / 6, sum(sparse) / 6
    assert 1.0 < mean_full < 4.0
    assert mean_sparse > mean_full
    assert sum(err_sparse) / 6 < 2.0 * sum(err_full) / 6


def test_example_of_the_page():
    """The state (x, A, B) on a line after the example of the EIF page; B is deactivated."""
    om = [[85.0, -35.0, -10.0], [-35.0, 47.5, -2.5], [-10.0, -2.5, 22.5]]
    xi = [-33.75, 46.25, 97.5]
    mu = rbm.solve(om, xi)
    before = rbm.inv(om)
    sparsify_info(om, xi, mu, [0], [1], [2])
    want = [[80.5556, -36.1111, 0.0], [-36.1111, 49.2760, -6.6176], [0.0, -6.6176, 21.3235]]
    assert max_abs_diff(om, want) < 1e-4
    assert max_abs_diff(rbm.solve(om, xi), mu) < 1e-12
    after = rbm.inv(om)
    for i in range(3):
        assert abs(after[i][i] - before[i][i]) < 1e-12  # no passive landmark: the variances stay
    assert abs(before[0][2] - 0.01) < 1e-9
    assert abs(after[0][2] - 0.0045) < 1e-4
