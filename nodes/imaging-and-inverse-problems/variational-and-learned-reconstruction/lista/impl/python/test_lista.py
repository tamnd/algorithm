# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lista/. The authors are listed in prov/KG5S6M.jsonl.

import random

from lista import (
    ista,
    ista_weights,
    lasso_objective,
    lista,
    lista_loss_and_grad,
    matvec,
    soft,
    train_tied,
)

A = [[1.0, 0.0, 0.6], [0.0, 1.0, 0.8]]
Y = [0.6, 0.8]
LAM = 0.1
LIP = 2.0  # ||A||^2: the eigenvalues of A A^T are 2 and 1


def close(u, v, tol):
    return all(abs(a - b) <= tol for a, b in zip(u, v)) and len(u) == len(v)


def random_problem(rng, m, n):
    a = [[rng.gauss(0.0, 0.5) for _ in range(n)] for _ in range(m)]
    v = [1.0] * n
    nv = 1.0
    for _ in range(200):
        w = [sum(a[i][j] * sum(a[i][k] * v[k] for k in range(n)) for i in range(m)) for j in range(n)]
        nv = sum(t * t for t in w) ** 0.5
        v = [t / nv for t in w]
    return a, 1.01 * nv


def test_soft_thresholding():
    assert soft([0.3, -0.3, 0.05, -2.0], [0.1] * 4) == [0.3 - 0.1, -0.3 + 0.1, 0.0, -1.9]


def test_first_ista_step_of_the_example():
    x = lista(Y, [ista_weights(A, LAM, LIP)])
    assert close(x, [0.25, 0.35, 0.45], 1e-12)


def test_lista_with_ista_weights_is_ista():
    rng = random.Random(1)
    a, lip = random_problem(rng, 5, 8)
    y = [rng.gauss(0.0, 1.0) for _ in range(5)]
    w = ista_weights(a, 0.2, lip)
    for k in range(1, 12):
        assert close(lista(y, [w] * k), ista(a, y, 0.2, lip, k), 1e-12)


def test_ista_objective_does_not_increase():
    x = [0.0, 0.0, 0.0]
    f = lasso_objective(A, Y, LAM, x)
    for _ in range(60):
        x = ista(A, Y, LAM, LIP, 1, x)
        f_new = lasso_objective(A, Y, LAM, x)
        assert f_new <= f + 1e-15
        f = f_new
    assert abs(f - 0.095) < 1e-6


def test_example_ista_needs_46_steps_for_the_support():
    w = ista_weights(A, LAM, LIP)
    assert lista(Y, [w] * 45)[1] > 0.0
    x46 = lista(Y, [w] * 46)
    assert x46[0] == 0.0 and x46[1] == 0.0
    err50 = sum((a - b) ** 2 for a, b in zip(lista(Y, [w] * 50), [0.0, 0.0, 0.9])) ** 0.5
    err49 = sum((a - b) ** 2 for a, b in zip(lista(Y, [w] * 49), [0.0, 0.0, 0.9])) ** 0.5
    assert err50 < 1e-3 < err49


def test_one_hand_made_layer_is_exact_on_its_family_only():
    layer = ([[0.0, 0.0], [0.0, 0.0], [0.6, 0.8]], [[0.0] * 3 for _ in range(3)], [0.0, 0.0, 0.1])
    for t in (0.3, 0.9, 1.0, 2.5):
        y = [0.6 * t, 0.8 * t]
        assert close(lista(y, [layer]), [0.0, 0.0, t - 0.1], 1e-12)
        assert close(ista(A, y, LAM, LIP, 3000), [0.0, 0.0, t - 0.1], 1e-9)
    # Off the family the same layer is wrong: the lasso solution for y = (1, 0) is (0.9, 0, 0).
    assert close(ista(A, [1.0, 0.0], LAM, LIP, 3000), [0.9, 0.0, 0.0], 1e-9)
    assert close(lista([1.0, 0.0], [layer]), [0.0, 0.0, 0.5], 1e-12)


def test_backpropagation_matches_finite_differences():
    rng = random.Random(3)
    m, n, k = 3, 4, 3
    layers = []
    for _ in range(k):
        w_e = [[rng.gauss(0.0, 0.5) for _ in range(m)] for _ in range(n)]
        s = [[rng.gauss(0.0, 0.3) for _ in range(n)] for _ in range(n)]
        theta = [rng.uniform(0.05, 0.2) for _ in range(n)]
        layers.append((w_e, s, theta))
    y = [rng.gauss(0.0, 1.0) for _ in range(m)]
    target = [rng.gauss(0.0, 1.0) for _ in range(n)]
    _, grads = lista_loss_and_grad(y, layers, target)
    h = 1e-6

    def loss_with(layer, part, i, j, delta):
        new = [(list(map(list, w)), list(map(list, s)), list(t)) for w, s, t in layers]
        if part == 2:
            new[layer][2][i] += delta
        else:
            new[layer][part][i][j] += delta
        return lista_loss_and_grad(y, new, target)[0]

    for layer in range(k):
        for part, rows, cols in ((0, n, m), (1, n, n), (2, n, 1)):
            for i in range(rows):
                for j in range(cols):
                    fd = (loss_with(layer, part, i, j, h) - loss_with(layer, part, i, j, -h)) / (2 * h)
                    g = grads[layer][part][i] if part == 2 else grads[layer][part][i][j]
                    assert abs(fd - g) < 1e-6 * (1.0 + abs(g))


def test_training_beats_ista_with_the_same_depth():
    rng = random.Random(7)
    m, n, k, lam = 4, 6, 3, 0.1
    a, lip = random_problem(rng, m, n)
    data = []
    for _ in range(20):
        xt = [0.0] * n
        for j in rng.sample(range(n), 2):
            xt[j] = rng.choice([-1.0, 1.0]) * rng.uniform(0.5, 1.5)
        y = matvec(a, xt)
        data.append((y, ista(a, y, lam, lip, 2000)))

    def mean_loss(w):
        return sum(lista_loss_and_grad(y, [w] * k, t)[0] for y, t in data) / len(data)

    start = ista_weights(a, lam, lip)
    trained = train_tied(data, k, start, 0.2, 150)
    assert mean_loss(trained) < 0.25 * mean_loss(start)
