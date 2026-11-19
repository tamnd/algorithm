# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/speculative-decoding/. The authors are listed in prov/K824EJ.jsonl.

import math
import random
from collections import Counter, defaultdict
from fractions import Fraction as F

from speculative_decoding import (
    EOS,
    acceptance_rate,
    expected_tokens_per_step,
    residual,
    sample,
    speculative_decode,
    speculative_step,
)

P_ROWS = {
    (): {"a": F(1, 2), "b": F(2, 5), EOS: F(1, 10)},
    ("a",): {"a": F(2, 5), "b": F(3, 10), EOS: F(3, 10)},
    ("b",): {"a": F(1, 20), "b": F(1, 20), EOS: F(9, 10)},
}
Q_ROWS = {
    (): {"a": F(7, 10), "b": F(1, 5), EOS: F(1, 10)},
    ("a",): {"a": F(1, 5), "b": F(1, 2), EOS: F(3, 10)},
    ("b",): {"a": F(3, 10), "b": F(3, 10), EOS: F(2, 5)},
}
END = {"a": F(0), "b": F(0), EOS: F(1)}


def p_exact(prefix):
    return P_ROWS.get(tuple(prefix), END)


def q_exact(prefix):
    return Q_ROWS.get(tuple(prefix), END)


def as_float(model):
    cache = {}

    def m(prefix):
        if prefix not in cache:
            cache[prefix] = {w: float(v) for w, v in model(prefix).items()}
        return cache[prefix]

    return m


def step_law(prefix, target, draft, gamma, room):
    """The exact law of one step, in Fractions, enumerated over the draft and the coin flips."""
    g = min(gamma, room - 1)
    out = defaultdict(F)

    def rec(xs, prob):
        p = target(prefix + tuple(xs))
        if xs and xs[-1] == EOS:
            out[tuple(xs)] += prob
            return
        if len(xs) == g:
            for t, pt in p.items():
                if pt:
                    out[tuple(xs) + (t,)] += prob * pt
            return
        q = draft(prefix + tuple(xs))
        res = residual(p, q)
        for x, qx in q.items():
            if qx == 0:
                continue
            acc = min(F(1), p.get(x, F(0)) / qx)
            if acc:
                rec(xs + [x], prob * qx * acc)
            if acc < 1:
                for t, rt in res.items():
                    if rt:
                        out[tuple(xs) + (t,)] += prob * qx * (1 - acc) * rt

    rec([], F(1))
    return out


def output_law(target, draft, gamma, max_len, prefix=()):
    if len(prefix) == max_len or (prefix and prefix[-1] == EOS):
        return {prefix: F(1)}
    out = defaultdict(F)
    for block, pr in step_law(prefix, target, draft, gamma, max_len - len(prefix)).items():
        for seq, pr2 in output_law(target, draft, gamma, max_len, prefix + block).items():
            out[seq] += pr * pr2
    return out


def target_law(target, max_len, prefix=()):
    if len(prefix) == max_len or (prefix and prefix[-1] == EOS):
        return {prefix: F(1)}
    out = defaultdict(F)
    for t, pt in target(prefix).items():
        if pt:
            for seq, pr in target_law(target, max_len, prefix + (t,)).items():
                out[seq] += pt * pr
    return out


def random_rows(seed, vocab, n):
    def model(prefix):
        if len(prefix) >= n - 1:
            return {w: F(int(w == EOS)) for w in vocab}
        rng = random.Random(f"{seed}|{' '.join(prefix)}")
        ws = [rng.randrange(0, 6) for _ in vocab]
        ws[-1] += 1
        return {w: F(x, sum(ws)) for w, x in zip(vocab, ws)}

    return model


def test_example_numbers() -> None:
    p, q = P_ROWS[()], Q_ROWS[()]
    assert acceptance_rate(p, q) == F(4, 5)
    assert residual(p, q) == {"a": 0, "b": 1, EOS: 0}
    assert math.isclose(expected_tokens_per_step(0.8, 4), 3.3616)
    assert expected_tokens_per_step(1, 4) == 5


def test_one_step_has_the_target_law() -> None:
    # With gamma = 1 the first token of the step is distributed as p.
    law = step_law((), p_exact, q_exact, 1, 3)
    first = defaultdict(F)
    for block, pr in law.items():
        first[block[0]] += pr
    assert dict(first) == P_ROWS[()]
    assert sum(law.values()) == 1


def test_exact_output_law_equals_the_target() -> None:
    want = target_law(p_exact, 3)
    for gamma in range(0, 4):
        assert output_law(p_exact, q_exact, gamma, 3) == want
    vocab = ["a", "b", EOS]
    for seed in range(8):
        target = random_rows(seed, vocab, 4)
        draft = random_rows(seed + 100, vocab, 4)
        want = target_law(target, 4)
        for gamma in (1, 2, 3):
            assert output_law(target, draft, gamma, 4) == want


def test_sample_frequencies() -> None:
    rng = random.Random(1)
    target, draft = as_float(p_exact), as_float(q_exact)
    want = target_law(p_exact, 3)
    draws = 20000
    counts = Counter(tuple(speculative_decode(target, draft, 3, 3, rng)) for _ in range(draws))
    assert set(counts) <= set(want)
    for seq, pr in want.items():
        assert abs(counts[seq] / draws - float(pr)) < 0.01


def test_acceptance_rate_and_tokens_per_call() -> None:
    p = {"a": 0.5, "b": 0.4, "c": 0.1}
    q = {"a": 0.7, "b": 0.2, "c": 0.1}
    target = lambda prefix: p  # noqa: E731
    draft = lambda prefix: q  # noqa: E731
    rng = random.Random(2)
    stats = {}
    steps = 10000
    tokens = sum(len(speculative_step((), target, draft, 4, rng, 100, stats)) for _ in range(steps))
    assert stats["target_calls"] == steps
    assert abs(stats["accepted"] / stats["tried"] - 0.8) < 0.01
    assert abs(tokens / steps - 3.3616) < 0.05
    y = speculative_decode(target, draft, 4, 50, rng)
    assert len(y) == 50


def test_exact_mean_tokens_per_step() -> None:
    p = {"a": F(1, 2), "b": F(2, 5), "c": F(1, 10)}
    q = {"a": F(7, 10), "b": F(1, 5), "c": F(1, 10)}
    alpha = acceptance_rate(p, q)
    for gamma in range(0, 6):
        law = step_law((), lambda s: p, lambda s: q, gamma, 100)
        mean = sum(len(block) * pr for block, pr in law.items())
        assert mean == (1 - alpha ** (gamma + 1)) / (1 - alpha)


def test_equal_models_accept_everything() -> None:
    p = {"a": 0.25, "b": 0.75}
    rng = random.Random(3)
    stats = {}
    speculative_decode(lambda s: p, lambda s: p, 3, 400, rng, stats)
    assert stats["accepted"] == stats["drafted"]
    assert stats["target_calls"] == 100


def test_sample_helper() -> None:
    rng = random.Random(4)
    counts = Counter(sample({"x": 1, "y": 3, "z": 0}, rng) for _ in range(20000))
    assert counts["z"] == 0
    assert abs(counts["y"] / 20000 - 0.75) < 0.01
