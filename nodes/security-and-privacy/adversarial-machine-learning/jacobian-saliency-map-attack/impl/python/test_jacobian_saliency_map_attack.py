# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jacobian-saliency-map-attack/. The authors are listed in prov/NXJN7D.jsonl.

"""Tests of JSMA, on seeded synthetic models only."""

import itertools
import random

import mlkit as m
from jacobian_saliency_map_attack import jsma, saliency_pair

# The worked example of the page: three classes, six features, target class 1.
WE = [
    [-0.5, 0.5, 1.0, 0.0, 0.0, 0.0],
    [1.0, -1.0, -0.5, 0.0, 0.5, 0.0],
    [1.0, 0.0, 0.5, -1.0, -1.0, -1.0],
]
BE = [1.0, 0.0, 0.0]
XE = [0.2, 0.0, 0.0, 0.5, 0.2, 0.4]


def affine(w, b):
    return (lambda u: [m.dot(r, u) + bi for r, bi in zip(w, b)]), (lambda u: w)


def brute_pair(jz, target, domain):
    """Independent oracle: score every pair from scratch and keep the first best one."""
    best, best_s = None, 0.0
    for p, q in itertools.combinations(domain, 2):
        alpha = jz[target][p] + jz[target][q]
        beta = sum(jz[j][p] + jz[j][q] for j in range(len(jz)) if j != target)
        if alpha > 0 and beta < 0 and -alpha * beta > best_s + 1e-12:
            best, best_s = (p, q), -alpha * beta
    return best, best_s


def smallest_set(lg, x, target):
    """Independent oracle: the size of the smallest set of features that, set to 1, gives the target, or None."""
    d = len(x)
    free = [i for i in range(d) if x[i] < 1.0]
    for size in range(len(free) + 1):
        for s in itertools.combinations(free, size):
            u = list(x)
            for i in s:
                u[i] = 1.0
            if m.argmax(lg(u)) == target:
                return size
    return None


def test_page_example() -> None:
    lg, jac = affine(WE, BE)
    assert m.argmax(lg(XE)) == 0
    assert saliency_pair(WE, 1, [0, 1, 2, 3, 4, 5]) == (3, 4)
    xa, ok, changed = jsma(lg, jac, XE, 1)
    assert ok and changed == [3, 4, 0, 5]
    assert xa == [1.0, 0.0, 0.0, 1.0, 1.0, 1.0]
    assert [round(t, 9) for t in lg(xa)] == [0.5, 1.5, -2.0]
    # with a budget of 3 of the 6 features only one pair fits, and the attack fails
    xa, ok, changed = jsma(lg, jac, XE, 1, max_distortion=0.5)
    assert not ok and changed == [3, 4]


def test_edges() -> None:
    lg, jac = affine(WE, BE)
    assert jsma(lg, jac, XE, 0) == (XE, True, [])  # already the target
    assert jsma(lg, jac, [1.0] * 6, 1)[2] == []  # nothing below 1, empty domain
    assert jsma(lg, jac, XE, 1, max_distortion=0.2)[2] == []  # a budget of one feature fits no pair
    assert saliency_pair(WE, 1, [0]) is None


def test_pair_choice_against_brute_force() -> None:
    rng = random.Random(7501)
    for _ in range(500):
        d, k = rng.randint(2, 7), rng.randint(2, 5)
        jz = [[rng.choice([-1.0, -0.5, 0.0, 0.5, 1.0, rng.uniform(-1, 1)]) for _ in range(d)] for _ in range(k)]
        target = rng.randrange(k)
        domain = sorted(rng.sample(range(d), rng.randint(0, d)))
        got = saliency_pair(jz, target, domain)
        want, score = brute_pair(jz, target, domain)
        if want is None:
            assert got is None
        else:
            p, q = got
            alpha = jz[target][p] + jz[target][q]
            beta = sum(jz[j][p] + jz[j][q] for j in range(k) if j != target)
            assert alpha > 0 and beta < 0
            assert abs(-alpha * beta - score) < 1e-9


def test_linear_models_against_exhaustive_search() -> None:
    # On an affine model with theta = 1 the output sets the changed features to 1, so any
    # success is a set that the exhaustive search also finds, and it can only be larger.
    rng = random.Random(7502)
    wins = 0
    for _ in range(500):
        d, k = rng.randint(2, 7), rng.randint(2, 4)
        w = [[rng.uniform(-1, 1) for _ in range(d)] for _ in range(k)]
        b = [rng.uniform(-0.5, 0.5) for _ in range(k)]
        x = [rng.choice([0.0, rng.uniform(0, 1), 1.0]) for _ in range(d)]
        lg, jac = affine(w, b)
        y = m.argmax(lg(x))
        target = rng.choice([j for j in range(k) if j != y])
        xa, ok, changed = jsma(lg, jac, x, target)
        assert ok == (m.argmax(lg(xa)) == target)
        assert len(changed) == len(set(changed)) and len(changed) % 2 == 0
        assert all(xa[i] == 1.0 for i in changed)
        assert all(xa[i] == x[i] for i in range(d) if i not in changed)
        best = smallest_set(lg, x, target)
        if ok:
            wins += 1
            assert best is not None and best <= len(changed)
        if best is None:
            assert not ok
    assert wins > 50


def test_relu_nets_respect_box_and_budget() -> None:
    rng = random.Random(7503)
    for _ in range(300):
        d, h, k = rng.randint(2, 6), rng.randint(2, 6), rng.randint(2, 4)
        net = m.tiny_relu_net(rng, d, h, k)
        lg = lambda u: m.forward(net, u)
        jac = lambda u: m.logits_jacobian(net, u)
        x = [rng.uniform(0, 1) for _ in range(d)]
        target = rng.randrange(k)
        theta = rng.choice([0.3, 1.0])
        gamma = rng.choice([0.5, 1.0])
        xa, ok, changed = jsma(lg, jac, x, target, theta=theta, max_distortion=gamma)
        assert all(0.0 <= a <= 1.0 for a in xa)
        assert len(changed) <= int(gamma * d)
        assert sum(1 for a, b in zip(xa, x) if a != b) <= len(changed)
        assert all(xa[i] >= x[i] for i in range(d))
        assert ok == (m.argmax(lg(xa)) == target)
