# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/psipred/. The authors are listed in prov/RQVJG1.jsonl.

import random
from math import exp, isclose

from psipred import Layer, WindowNet, logistic, psipred_forward, random_net, window_input


def direct(rows, net):
    """Build the full window vector for each centre and apply the two layers."""
    out = []
    for j in range(len(rows)):
        x = window_input(rows, j, net.w, net.f)
        hid = [1 / (1 + exp(-(sum(a * b for a, b in zip(row, x)) + bias)))
               for row, bias in zip(net.hidden.W, net.hidden.b)]
        out.append([1 / (1 + exp(-(sum(a * b for a, b in zip(row, hid)) + bias)))
                    for row, bias in zip(net.out.W, net.out.b)])
    return out


def close(a, b):
    return all(isclose(u, v, rel_tol=0, abs_tol=1e-12) for ra, rb in zip(a, b) for u, v in zip(ra, rb))


def test_example() -> None:
    # Window 3, one feature, one hidden unit; hand-computed values.
    net = WindowNet(3, 1, Layer([[1.0, 0.0, 2.0, 0.0, -1.0, 0.5]], [0.0]), Layer([[1.0], [-1.0], [0.0]], [0.0, 0.0, 0.0]))
    rows = [[0.5], [1.0]]
    out = net.forward(rows)
    # Centre 0: left end flag (weight 0), 2 * 0.5, -1 * 1.0 -> pre 0.
    assert isclose(out[0][0], logistic(0.5))
    # Centre 1: 1 * 0.5, 2 * 1.0, right end flag 0.5 -> pre 3.
    assert isclose(out[1][0], logistic(logistic(3.0)))
    assert close(out, direct(rows, net))


def test_logistic() -> None:
    assert logistic(0) == 0.5
    assert isclose(logistic(2) + logistic(-2), 1.0)
    assert logistic(-1000) == 0.0 and logistic(1000) == 1.0


def test_small_against_direct() -> None:
    rng = random.Random(1999)
    for _ in range(20):
        w = rng.choice([1, 3, 5])
        net1 = random_net(w, 20, rng.randint(1, 6), rng)
        net2 = random_net(w, 3, rng.randint(1, 6), rng)
        n = rng.randint(1, 12)
        pssm = [[rng.randint(-7, 7) for _ in range(20)] for _ in range(n)]
        s1, s2, pred = psipred_forward(pssm, net1, net2)
        rows = [[logistic(v) for v in r] for r in pssm]
        want1 = direct(rows, net1)
        want2 = direct(want1, net2)
        assert close(s1, want1) and close(s2, want2)
        assert len(pred) == n and set(pred) <= set("HEC")
        for o, p in zip(s2, pred):
            assert o["HEC".index(p)] == max(o)


def test_psipred_sizes() -> None:
    rng = random.Random(292)
    net1 = random_net(15, 20, 75, rng, 0.1)
    net2 = random_net(15, 3, 60, rng, 0.1)
    assert len(net1.hidden.W[0]) == 315 and len(net2.hidden.W[0]) == 60
    pssm = [[rng.randint(-7, 7) for _ in range(20)] for _ in range(20)]
    s1, s2, _ = psipred_forward(pssm, net1, net2)
    assert close(s2, direct(direct([[logistic(v) for v in r] for r in pssm], net1), net2))
