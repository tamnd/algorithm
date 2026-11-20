# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ensemble-kalman-filter/. The authors are listed in prov/JS3602.jsonl.

import math
import random

import scimat
from ensemble_kalman_filter import enkf_analysis, enkf_forecast, ensemble_moments, observation_perturbations


def kalman(ens, yo, H, R):
    n = len(ens[0])
    xbar, P = ensemble_moments(ens)
    PHt = scimat.matmul(P, scimat.transpose(H))
    S = scimat.add(scimat.matmul(H, PHt), R)
    K = scimat.transpose(scimat.solve(S, scimat.transpose(PHt)))
    xa = scimat.add(xbar, scimat.matvec(K, scimat.sub(yo, scimat.matvec(H, xbar))))
    Pa = scimat.matmul(scimat.sub(scimat.eye(n), scimat.matmul(K, H)), P)
    return K, xa, Pa


def test_page_example():
    out = enkf_analysis([[-1.0], [1.0]], [1.0], lambda x: x, [[1.0]], eps=[[-0.5], [0.5]])
    assert abs(out[0][0] - 0.0) < 1e-12
    assert abs(out[1][0] - 4 / 3) < 1e-12
    mean, P = ensemble_moments(out)
    assert abs(mean[0] - 2 / 3) < 1e-12
    assert abs(P[0][0] - 8 / 9) < 1e-12


def test_exact_when_perturbations_match_R_and_are_orthogonal():
    # eps has sample variance R and no sample covariance with the prior, so the
    # analysis has exactly the Kalman mean and variance.
    R = 0.7
    c = math.sqrt(R / 3)
    ens = [[-1.0], [0.0], [1.0]]
    out = enkf_analysis(ens, [2.0], lambda x: x, [[R]], eps=[[c], [-2 * c], [c]])
    _, xa, Pa = kalman(ens, [2.0], [[1.0]], [[R]])
    mean, P = ensemble_moments(out)
    assert abs(mean[0] - xa[0]) < 1e-12
    assert abs(P[0][0] - Pa[0][0]) < 1e-12


def test_scalar_check_value_in_expectation():
    s = 1 / math.sqrt(2.0)
    rng = random.Random(7)
    trials, m_sum, v_sum = 20000, 0.0, 0.0
    for _ in range(trials):
        out = enkf_analysis([[-s], [s]], [1.0], lambda x: x, [[1.0]], rng=rng)
        mean, P = ensemble_moments(out)
        m_sum += mean[0]
        v_sum += P[0][0]
    assert abs(m_sum / trials - 0.5) < 0.01
    assert abs(v_sum / trials - 0.5) < 0.01


def test_mean_is_kalman_mean_plus_gain_times_mean_perturbation():
    rng = random.Random(8)
    for _ in range(40):
        n, p, N = rng.randint(1, 4), rng.randint(1, 4), rng.randint(2, 8)
        ens = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(N)]
        H = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(p)]
        L = [[rng.uniform(-1, 1) for _ in range(p)] for _ in range(p)]
        R = scimat.add(scimat.matmul(L, scimat.transpose(L)), scimat.scale(0.3, scimat.eye(p)))
        yo = [rng.gauss(0, 2) for _ in range(p)]
        eps = observation_perturbations(R, N, rng)
        out = enkf_analysis(ens, yo, lambda x: scimat.matvec(H, x), R, eps=eps)
        K, xa, _ = kalman(ens, yo, H, R)
        ebar = [sum(e[k] for e in eps) / N for k in range(p)]
        want = scimat.add(xa, scimat.matvec(K, ebar))
        mean, _ = ensemble_moments(out)
        for a in range(n):
            assert abs(mean[a] - want[a]) < 1e-9 * (1 + abs(want[a]))


def test_covariance_is_kalman_in_expectation():
    rng = random.Random(9)
    ens = [[0.0, 1.0], [1.0, 3.0], [2.0, 2.0], [0.5, -1.0]]
    H = [[1.0, 0.0]]
    R = [[0.5]]
    _, _, Pa = kalman(ens, [1.0], H, R)
    trials = 6000
    acc = [[0.0, 0.0], [0.0, 0.0]]
    for _ in range(trials):
        out = enkf_analysis(ens, [1.0], lambda x: [x[0]], R, rng=rng)
        _, P = ensemble_moments(out)
        for a in range(2):
            for b in range(2):
                acc[a][b] += P[a][b] / trials
    for a in range(2):
        for b in range(2):
            assert abs(acc[a][b] - Pa[a][b]) < 0.04


def test_observation_perturbations_have_covariance_R():
    rng = random.Random(10)
    R = [[2.0, 0.6], [0.6, 1.0]]
    eps = observation_perturbations(R, 40000, rng)
    _, C = ensemble_moments(eps)
    for a in range(2):
        for b in range(2):
            assert abs(C[a][b] - R[a][b]) < 0.05


def test_localization_weights_one_change_nothing_and_zero_freezes():
    rng = random.Random(11)
    ens = [[rng.gauss(0, 1) for _ in range(3)] for _ in range(6)]
    h = lambda x: [x[0], x[1]]
    R = [[0.5, 0.0], [0.0, 0.8]]
    eps = observation_perturbations(R, 6, rng)
    a = enkf_analysis(ens, [1.0, -1.0], h, R, eps=eps)
    ones_xy = [[1.0, 1.0] for _ in range(3)]
    ones_yy = [[1.0, 1.0], [1.0, 1.0]]
    b = enkf_analysis(ens, [1.0, -1.0], h, R, eps=eps, loc_xy=ones_xy, loc_yy=ones_yy)
    assert all(abs(u - v) < 1e-12 for x, z in zip(a, b) for u, v in zip(x, z))
    zero_last = [[1.0, 1.0], [1.0, 1.0], [0.0, 0.0]]
    c = enkf_analysis(ens, [1.0, -1.0], h, R, eps=eps, loc_xy=zero_last, loc_yy=ones_yy)
    for x, z in zip(ens, c):
        assert z[2] == x[2]


def l96(x, F=8.0):
    n = len(x)
    return [(x[(j + 1) % n] - x[j - 2]) * x[j - 1] - x[j] + F for j in range(n)]


def rk4(x, dt):
    k1 = l96(x)
    k2 = l96([a + 0.5 * dt * b for a, b in zip(x, k1)])
    k3 = l96([a + 0.5 * dt * b for a, b in zip(x, k2)])
    k4 = l96([a + dt * b for a, b in zip(x, k3)])
    return [a + dt * (b + 2 * c + 2 * d + e) / 6 for a, b, c, d, e in zip(x, k1, k2, k3, k4)]


def gaspari_cohn(r, c):
    z = abs(r) / c
    if z <= 1:
        return -z**5 / 4 + z**4 / 2 + 5 * z**3 / 8 - 5 * z**2 / 3 + 1
    if z < 2:
        return z**5 / 12 - z**4 / 2 + 5 * z**3 / 8 + 5 * z**2 / 3 - 5 * z + 4 - 2 / (3 * z)
    return 0.0


def test_lorenz96_twin_tracks_the_truth():
    n, N, dt, rho, c = 40, 10, 0.05, 1.1, 4.0
    rng, prng = random.Random(1), random.Random(101)
    x = [8.0] * n
    x[0] += 0.01
    for _ in range(1000):
        x = rk4(x, dt)
    ens, z = [], list(x)
    for _ in range(N):
        for _ in range(50):
            z = rk4(z, dt)
        ens.append(list(z))
    free = [list(e) for e in ens]
    obs = list(range(0, n, 2))
    p = len(obs)
    dist = lambda a, b: min(abs(a - b), n - abs(a - b))
    lxy = [[gaspari_cohn(dist(j, q), c) for q in obs] for j in range(n)]
    lyy = [[gaspari_cohn(dist(q, q2), c) for q2 in obs] for q in obs]
    R = [[1.0 if a == b else 0.0 for b in range(p)] for a in range(p)]
    model = lambda s: rk4(s, dt)
    errs, ferrs = [], []
    for _ in range(150):
        x = rk4(x, dt)
        ens = enkf_forecast(ens, model)
        free = enkf_forecast(free, model)
        m = [sum(e[j] for e in ens) / N for j in range(n)]
        ens = [[m[j] + math.sqrt(rho) * (e[j] - m[j]) for j in range(n)] for e in ens]
        yo = [x[k] + rng.gauss(0, 1) for k in obs]
        ens = enkf_analysis(ens, yo, lambda s: [s[k] for k in obs], R, rng=prng, loc_xy=lxy, loc_yy=lyy)
        for e_list, out in ((ens, errs), (free, ferrs)):
            m = [sum(e[j] for e in e_list) / N for j in range(n)]
            out.append(math.sqrt(sum((m[j] - x[j]) ** 2 for j in range(n)) / n))
    assert sum(errs[50:]) / 100 < 0.7
    assert sum(ferrs[50:]) / 100 > 2.0
