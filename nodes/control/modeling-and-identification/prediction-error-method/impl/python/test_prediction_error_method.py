# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/prediction-error-method/. The authors are listed in prov/R82NR4.jsonl.

import random

from prediction_error_method import (_gradients, _psi, first_sample, is_schur, pem, pem_loss,
                                     prediction_errors, simulate_general)

A_TRUE = [-1.5, 0.7]
B_TRUE = [1.0, 0.5]
C_TRUE = [-1.0, 0.2]


def _data(n, seed, c=(), f=None):
    rng = random.Random(seed)
    u = [rng.choice((-1.0, 1.0)) for _ in range(n)]
    e = [rng.gauss(0.0, 1.0) for _ in range(n)]
    if f is None:
        y = simulate_general(A_TRUE, B_TRUE, list(c), [], [], 1, u, e)
    else:
        y = simulate_general([], B_TRUE, [], [], f, 1, u, e)
    return y, u, e


def test_worked_example_armax():
    y, u, e = _data(2000, 1, c=C_TRUE)
    r = pem(y, u, 2, 2, nc=2)
    want = [-1.5129, 0.7130, 1.0326, 0.4604, -0.9801, 0.1883]
    assert all(abs(p - q) < 2e-4 for p, q in zip(r["theta"], want))
    assert abs(r["loss"] - 1.04079) < 1e-4
    true_loss = pem_loss(A_TRUE + B_TRUE + C_TRUE, y, u, 2, 2, 2)
    assert r["loss"] <= true_loss
    assert is_schur([1.0] + r["c"])


def _det(m):
    if len(m) == 1:
        return m[0][0]
    return sum((-1) ** j * m[0][j] * _det([row[:j] + row[j + 1:] for row in m[1:]]) for j in range(len(m)))


def _ls_oracle(y, u, na, nb, nk):
    # Normal equations solved by Cramer's rule.
    d = na + nb
    r = [[0.0] * d for _ in range(d)]
    g = [0.0] * d
    for t in range(max(na, nk + nb - 1), len(y)):
        phi = [-y[t - i] for i in range(1, na + 1)] + [u[t - nk - j] for j in range(nb)]
        for i in range(d):
            g[i] += phi[i] * y[t]
            for j in range(d):
                r[i][j] += phi[i] * phi[j]
    dr = _det(r)
    out = []
    for k in range(d):
        m = [row[:k] + [g[i]] + row[k + 1:] for i, row in enumerate(r)]
        out.append(_det(m) / dr)
    return out, dr


def test_random_arx_case_is_least_squares():
    # For ARX the prediction error is linear in theta, so one Gauss-Newton
    # step from any start gives the least squares solution.
    rng = random.Random(7)
    done = 0
    while done < 500:
        na = rng.randint(0, 1)
        nb = rng.randint(1, 2)
        nk = rng.randint(0, 1)
        n = rng.randint(15, 30)
        u = [rng.uniform(-1, 1) for _ in range(n)]
        y = [rng.uniform(-1, 1) for _ in range(n)]
        want, dr = _ls_oracle(y, u, na, nb, nk)
        if abs(dr) < 1e-3:
            continue
        theta0 = [rng.uniform(-2, 2) for _ in range(na + nb)]
        r = pem(y, u, na, nb, nk=nk, theta0=theta0)
        assert r["iterations"] >= 1
        assert all(abs(p - q) < 1e-8 for p, q in zip(r["theta"], want))
        done += 1


def test_output_error_noise_free_is_exact():
    rng = random.Random(3)
    u = [rng.choice((-1.0, 1.0)) for _ in range(300)]
    y = simulate_general([], B_TRUE, [], [], A_TRUE, 1, u, [0.0] * 300)
    r = pem(y, u, 0, 2, nf=2)
    assert all(abs(p - q) < 1e-6 for p, q in zip(r["b"] + r["f"], B_TRUE + A_TRUE))
    assert r["loss"] < 1e-12


def test_output_error_consistent_with_colored_noise():
    # OE data with an output error that is not white still gives G.
    rng = random.Random(9)
    n = 3000
    u = [rng.choice((-1.0, 1.0)) for _ in range(n)]
    e = [rng.gauss(0.0, 1.0) for _ in range(n)]
    w = simulate_general([], B_TRUE, [], [], A_TRUE, 1, u, [0.0] * n)
    col = [e[t] + 0.9 * (e[t - 1] if t else 0.0) for t in range(n)]
    y = [p + q for p, q in zip(w, col)]
    r = pem(y, u, 0, 2, nf=2)
    assert all(abs(p - q) < 0.08 for p, q in zip(r["b"] + r["f"], B_TRUE + A_TRUE))


def test_gradient_matches_finite_differences():
    rng = random.Random(5)
    n = 60
    u = [rng.uniform(-1, 1) for _ in range(n)]
    y = [rng.uniform(-1, 1) for _ in range(n)]
    na, nb, nc, nd, nf, nk = 1, 2, 1, 1, 1, 1
    theta = [0.3, 0.8, -0.4, 0.5, -0.2, 0.6]
    eps, w, v = prediction_errors(theta, y, u, na, nb, nc, nd, nf, nk)
    sig = _gradients(theta, y, u, eps, w, v, na, nb, nc, nd, nf, nk)
    h = 1e-6
    for i in range(len(theta)):
        tp = list(theta)
        tm = list(theta)
        tp[i] += h
        tm[i] -= h
        ep, _, _ = prediction_errors(tp, y, u, na, nb, nc, nd, nf, nk)
        em, _, _ = prediction_errors(tm, y, u, na, nb, nc, nd, nf, nk)
        for t in range(first_sample(na, nb, nc, nd, nf, nk), n):
            fd = -(ep[t] - em[t]) / (2 * h)
            assert abs(_psi(t, sig, na, nb, nc, nd, nf, nk)[i] - fd) < 1e-6


def test_cost_does_not_increase():
    y, u, _ = _data(800, 2, c=C_TRUE)
    losses = [pem(y, u, 2, 2, nc=2, maxiter=k)["loss"] for k in range(6)]
    assert all(b <= a for a, b in zip(losses, losses[1:]))


def test_bad_arguments():
    y, u, _ = _data(50, 4)
    for kwargs in ({"na": 1, "nb": 0}, {"na": -1, "nb": 1}):
        try:
            pem(y, u, **kwargs)
        except ValueError:
            continue
        raise AssertionError("expected ValueError")
    try:
        pem(y, u, 1, 1, nc=1, theta0=[0.0, 1.0, 2.0])
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for a C that is not Schur")
    try:
        pem([1.0] * 50, [1.0] * 50, 0, 2)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for a constant input")
