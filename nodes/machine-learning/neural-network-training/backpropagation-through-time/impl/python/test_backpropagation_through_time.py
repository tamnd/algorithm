# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/backpropagation-through-time/. The authors are listed in prov/W0KS2M.jsonl.

import copy
import math
import random

from backpropagation_through_time import bptt, loss, step, truncated_bptt


def rand_params(rng, H, D, O, s=0.8):
    m = lambda r, c: [[rng.uniform(-s, s) for _ in range(c)] for _ in range(r)]
    return {"W": m(H, H), "U": m(H, D), "b": [rng.uniform(-s, s) for _ in range(H)],
            "V": m(O, H), "c": [rng.uniform(-s, s) for _ in range(O)]}


def rand_seq(rng, T, D, O):
    xs = [[rng.uniform(-1, 1) for _ in range(D)] for _ in range(T)]
    ys = [[rng.uniform(-1, 1) for _ in range(O)] for _ in range(T)]
    return xs, ys


def entries(g):
    out = []
    for key in ("W", "U", "b", "V", "c"):
        v = g[key]
        for row in v:
            out.extend(row if isinstance(row, list) else [row])
    return out


def numeric(f, p, h=1e-6):
    """Central differences of f(p) for every parameter entry (the oracle)."""
    out = []
    for key in ("W", "U", "b", "V", "c"):
        v = p[key]
        idx = [(i, j) for i in range(len(v)) for j in range(len(v[i]))] if isinstance(v[0], list) \
            else [(i, None) for i in range(len(v))]
        for i, j in idx:
            q1, q2 = copy.deepcopy(p), copy.deepcopy(p)
            if j is None:
                q1[key][i] += h
                q2[key][i] -= h
            else:
                q1[key][i][j] += h
                q2[key][i][j] -= h
            out.append((f(q1) - f(q2)) / (2 * h))
    return out


def close(a, b, rtol=1e-6, atol=1e-8):
    return all(abs(p - q) <= atol + rtol * abs(q) for p, q in zip(a, b))


def test_worked_example():
    p = {"W": [[0.5]], "U": [[1.0]], "b": [0.0], "V": [[1.0]], "c": [0.0]}
    xs, ys = [[1.0], [0.0], [0.0]], [[0.5], [0.5], [0.0]]
    g, dh0, stored = bptt(p, [0.0], xs, ys)
    assert math.isclose(g["W"][0][0], 0.0303897, abs_tol=1e-7)
    assert math.isclose(g["U"][0][0], 0.1008156, abs_tol=1e-7)
    assert math.isclose(g["b"][0], 0.2316517, abs_tol=1e-7)
    assert math.isclose(dh0[0], 0.0504078, abs_tol=1e-7)
    assert stored == 4
    # with window 1 the estimate of dL/dW even has the wrong sign
    gt, _, _ = truncated_bptt(p, [0.0], xs, ys, 1)
    assert math.isclose(gt["W"][0][0], -0.0270928, abs_tol=1e-7)


def test_full_bptt_matches_central_differences():
    rng = random.Random(1)
    for trial in range(12):
        H, D, O, T = rng.randint(1, 3), rng.randint(1, 2), rng.randint(1, 2), rng.randint(1, 8)
        p = rand_params(rng, H, D, O)
        h0 = [rng.uniform(-0.5, 0.5) for _ in range(H)]
        xs, ys = rand_seq(rng, T, D, O)
        g, dh0, _ = bptt(p, h0, xs, ys)
        assert close(entries(g), numeric(lambda q: loss(q, h0, xs, ys), p)), trial
        for i in range(H):
            a, b = list(h0), list(h0)
            a[i] += 1e-6
            b[i] -= 1e-6
            n = (loss(p, a, xs, ys) - loss(p, b, xs, ys)) / 2e-6
            assert abs(dh0[i] - n) <= 1e-8 + 1e-6 * abs(n)


def test_window_at_least_T_is_full_bptt():
    rng = random.Random(2)
    p = rand_params(rng, 3, 2, 2)
    xs, ys = rand_seq(rng, 7, 2, 2)
    full, _, _ = bptt(p, [0.0] * 3, xs, ys)
    for k in (7, 8, 100):
        tr, _, _ = truncated_bptt(p, [0.0] * 3, xs, ys, k)
        assert entries(tr) == entries(full)


def test_truncated_is_gradient_of_chunk_loss():
    # truncated BPTT is the exact gradient of the sum of chunk losses in which
    # each chunk starts from the carried hidden state, held constant
    rng = random.Random(3)
    for k in (1, 2, 3):
        p = rand_params(rng, 2, 2, 1)
        xs, ys = rand_seq(rng, 7, 2, 1)
        starts, h = [], [0.1, -0.2]
        for s in range(0, 7, k):
            starts.append(list(h))
            for x in xs[s:s + k]:
                h = step(p, h, x)
        surrogate = lambda q: sum(loss(q, h0, xs[s:s + k], ys[s:s + k])
                                  for h0, s in zip(starts, range(0, 7, k)))
        tr, hT, _ = truncated_bptt(p, [0.1, -0.2], xs, ys, k)
        assert hT == h
        assert close(entries(tr), numeric(surrogate, p))
        full, _, _ = bptt(p, [0.1, -0.2], xs, ys)
        assert max(abs(a - b) for a, b in zip(entries(tr), entries(full))) > 1e-6


def test_memory_is_linear_in_T_and_k():
    rng = random.Random(4)
    p = rand_params(rng, 2, 1, 1)
    for T in (1, 5, 40):
        xs, ys = rand_seq(rng, T, 1, 1)
        assert bptt(p, [0.0, 0.0], xs, ys)[2] == T + 1
        for k in (1, 3, 10):
            assert truncated_bptt(p, [0.0, 0.0], xs, ys, k)[2] == min(k, T) + 1
