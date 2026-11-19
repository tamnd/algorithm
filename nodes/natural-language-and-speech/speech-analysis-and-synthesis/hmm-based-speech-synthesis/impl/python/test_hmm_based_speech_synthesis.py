# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hmm-based-speech-synthesis/. The authors are listed in prov/VMKZVY.jsonl.

import itertools
import math
import random

import pytest

from hmm_based_speech_synthesis import (
    front_end,
    mlpg_1d,
    rho_for_total,
    state_durations,
    synthesize,
    tree_lookup,
)

VOWELS = {"a", "i"}

TREES = {
    # Vowels last longer; the middle state of every phone is the longest.
    "dur": ("q", "phone", VOWELS,
            ("q", "state", {2}, ("leaf", (6.0, 4.0)), ("leaf", (3.0, 1.0))),
            ("q", "state", {2}, ("leaf", (3.0, 1.0)), ("leaf", (2.0, 0.5)))),
    "spec": ("q", "phone", VOWELS,
             ("leaf", (0.8, 0.05, 0.0, 0.01)),
             ("q", "right", VOWELS, ("leaf", (0.3, 0.1, 0.0, 0.02)), ("leaf", (0.1, 0.1, 0.0, 0.02)))),
    "f0": ("q", "phone", {"s"},
           ("leaf", (0.0, 0.0, 1.0, 0.0, 1.0)),
           ("leaf", (1.0, math.log(120.0), 0.01, 0.0, 0.001))),
}


def dur_loglik(d, m, v):
    return sum(-0.5 * math.log(2 * math.pi * vk) - (dk - mk) ** 2 / (2 * vk) for dk, mk, vk in zip(d, m, v))


def test_page_duration_example():
    m, v = [3.0, 5.0, 2.0], [1.0, 4.0, 1.0]
    assert state_durations(m, v, 0.0) == [3, 5, 2]
    rho = rho_for_total(m, v, 16)
    assert rho == 1.0
    assert state_durations(m, v, rho) == [4, 9, 3]
    rho = rho_for_total(m, v, 7)
    assert rho == -0.5
    assert [mk + rho * vk for mk, vk in zip(m, v)] == [2.5, 3.0, 1.5]


def test_duration_rule_is_the_constrained_maximum():
    # The real-valued d_k = m_k + rho v_k beats every integer vector with the same total.
    rng = random.Random(4)
    for _ in range(30):
        n = rng.randint(1, 4)
        m = [float(rng.randint(1, 5)) for _ in range(n)]
        v = [float(rng.randint(1, 4)) for _ in range(n)]
        T = rng.randint(n, 14)
        rho = rho_for_total(m, v, T)
        best_real = dur_loglik([mk + rho * vk for mk, vk in zip(m, v)], m, v)
        for d in itertools.product(range(0, T + 1), repeat=n):
            if sum(d) == T:
                assert dur_loglik(d, m, v) <= best_real + 1e-12


def test_mlpg_page_example():
    c = mlpg_1d([0, 0, 0, 1, 1, 1], [1] * 6, [0] * 6, [0.25] * 6)
    for x, y in zip(c, [0.2, 0.3, 0.3, 0.7, 0.7, 0.8]):
        assert math.isclose(x, y, abs_tol=1e-12)


def test_mlpg_is_a_maximum():
    rng = random.Random(8)
    T = 9
    mu_s = [rng.uniform(-1, 1) for _ in range(T)]
    var_s = [rng.uniform(0.5, 2) for _ in range(T)]
    mu_d = [rng.uniform(-0.2, 0.2) for _ in range(T)]
    var_d = [rng.uniform(0.1, 1) for _ in range(T)]

    def obj(c):
        s = 0.0
        for t in range(T):
            d = 0.5 * (c[min(t + 1, T - 1)] - c[max(t - 1, 0)])
            s -= (c[t] - mu_s[t]) ** 2 / (2 * var_s[t]) + (d - mu_d[t]) ** 2 / (2 * var_d[t])
        return s

    c = mlpg_1d(mu_s, var_s, mu_d, var_d)
    base = obj(c)
    for _ in range(50):
        e = [rng.gauss(0, 0.05) for _ in range(T)]
        assert obj([a + b for a, b in zip(c, e)]) < base


def test_front_end_and_trees():
    labels = front_end(["s", "a"])
    assert labels == [{"left": "#", "phone": "s", "right": "a"}, {"left": "s", "phone": "a", "right": "#"}]
    assert tree_lookup(TREES["dur"], labels[1], 2) == (6.0, 4.0)
    assert tree_lookup(TREES["dur"], labels[0], 0) == (2.0, 0.5)
    assert tree_lookup(TREES["spec"], labels[0], 0) == (0.3, 0.1, 0.0, 0.02)


def test_synthesize_toy_utterance():
    y, fr = synthesize(["s", "a", "n", "i"], TREES, hop=40, fs=8000, seed=1)
    d = fr["durations"]
    assert len(d) == 4 * 5
    T = sum(d)
    assert len(y) == 40 * T
    assert len(fr["spec"]) == T
    # "s" is unvoiced, the others are voiced; pitch exists exactly on voiced frames.
    n_s = sum(d[:5])
    assert fr["voiced"][:n_s] == [False] * n_s and all(fr["voiced"][n_s:])
    assert all(x is None for x in fr["logf0"][:n_s])
    assert all(abs(math.exp(x) - 120.0) < 1.0 for x in fr["logf0"][n_s:])
    # The trajectory is smoother than the step of state means.
    jumps = lambda s: max(abs(s[t + 1] - s[t]) for t in range(len(s) - 1))
    assert jumps(fr["spec"]) < jumps(fr["spec_means"])
    assert all(math.isfinite(s) for s in y)
    # Same seed, same output.
    assert synthesize(["s", "a", "n", "i"], TREES, hop=40, fs=8000, seed=1)[0] == y


def test_rho_slows_down():
    _, a = synthesize(["n", "a"], TREES, rho=0.0, hop=10)
    _, b = synthesize(["n", "a"], TREES, rho=1.0, hop=10)
    assert sum(b["durations"]) > sum(a["durations"])
    _, c = synthesize(["n", "a"], TREES, rho=-10.0, hop=10)
    assert min(c["durations"]) == 1


def test_singular_system():
    with pytest.raises(ValueError):
        mlpg_1d([0.0, 0.0], [math.inf, math.inf], [0.0, 0.0], [math.inf, math.inf])
