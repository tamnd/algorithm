# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-decoding/. The authors are listed in prov/61Q9XF.jsonl.

import math
import random

from greedy_decoding import EOS, greedy_decode
from nlslog import NEG_INF, log_normalize, safe_log

M1 = {
    (): {"a": 0.5, "b": 0.4, EOS: 0.1},
    ("a",): {"a": 0.4, "b": 0.3, EOS: 0.3},
    ("b",): {"a": 0.05, "b": 0.05, EOS: 0.9},
}


def m1(prefix):
    probs = M1.get(tuple(prefix), {"a": 0.0, "b": 0.0, EOS: 1.0})
    return {w: safe_log(p) for w, p in probs.items()}


def random_model(seed, vocab, n):
    """A model whose outputs have at most n tokens: "</s>" is forced at position n."""

    def model(prefix):
        if len(prefix) >= n - 1:
            return {w: (0.0 if w == EOS else NEG_INF) for w in vocab}
        rng = random.Random(f"{seed}|{' '.join(prefix)}")
        raw = [math.log(rng.random() ** 2 + 1e-3) for _ in vocab]
        return dict(zip(vocab, log_normalize(raw)))

    return model


def exhaustive(model, n):
    """Every output of at most n tokens that ends with "</s>", with its log probability."""
    out = []

    def rec(prefix, s):
        for w, lp in model(tuple(prefix)).items():
            if lp == NEG_INF:
                continue
            if w == EOS:
                out.append((prefix + [w], s + lp))
            elif len(prefix) + 1 < n:
                rec(prefix + [w], s + lp)

    rec([], 0.0)
    return out


def test_example_greedy_misses_the_mode() -> None:
    y, s = greedy_decode(m1, 3)
    assert y == ["a", "a", EOS]
    assert math.isclose(math.exp(s), 0.2)
    best = max(exhaustive(m1, 3), key=lambda t: t[1])
    assert best[0] == ["b", EOS]
    assert math.isclose(math.exp(best[1]), 0.36)
    total = math.fsum(math.exp(s) for _, s in exhaustive(m1, 3))
    assert math.isclose(total, 1.0)


def test_follows_the_greedy_rule() -> None:
    vocab = ["a", "b", "c", EOS]
    for seed in range(200):
        model = random_model(seed, vocab, 5)
        y, s = greedy_decode(model, 5)
        assert y[-1] == EOS and EOS not in y[:-1]
        total = 0.0
        for t, w in enumerate(y):
            logp = model(tuple(y[:t]))
            assert logp[w] == max(logp.values())
            total += logp[w]
        assert math.isclose(s, total)


def test_against_exhaustive_search() -> None:
    vocab = ["a", "b", "c", EOS]
    misses = 0
    for seed in range(200):
        model = random_model(seed, vocab, 5)
        y, s = greedy_decode(model, 5)
        outputs = exhaustive(model, 5)
        best = max(sc for _, sc in outputs)
        assert s <= best + 1e-12
        assert any(o == y and math.isclose(sc, s) for o, sc in outputs)
        if s < best - 1e-12:
            misses += 1
    assert 0 < misses < 200


def test_ratio_can_be_tiny() -> None:
    # p(a) = 1/2 + delta, p(b) = 1/2 - delta; after b the output ends, after a
    # it runs on through L uniform steps over 4 tokens.
    delta, length = 0.01, 6
    vocab = ["a", "b", "c", "d", EOS]

    def model(prefix):
        if not prefix:
            return {"a": math.log(0.5 + delta), "b": math.log(0.5 - delta), "c": NEG_INF, "d": NEG_INF, EOS: NEG_INF}
        if prefix == ("b",) or len(prefix) > length:
            return {w: (0.0 if w == EOS else NEG_INF) for w in vocab}
        return {w: (NEG_INF if w == EOS else math.log(0.25)) for w in vocab}

    y, s = greedy_decode(model, length + 2)
    assert y[0] == "a"
    assert math.isclose(math.exp(s), (0.5 + delta) * 0.25 ** length)
    assert math.exp(s) / (0.5 - delta) < 0.001


def test_no_end_token_within_the_limit() -> None:
    def model(prefix):
        return {"a": math.log(0.9), EOS: math.log(0.1)}

    y, s = greedy_decode(model, 4)
    assert y == ["a", "a", "a", "a"]
    assert math.isclose(s, 4 * math.log(0.9))


def test_ties_take_the_first_token() -> None:
    def model(prefix):
        if prefix:
            return {"x": NEG_INF, "y": NEG_INF, EOS: 0.0}
        return {"x": math.log(0.5), "y": math.log(0.5), EOS: NEG_INF}

    assert greedy_decode(model, 3)[0] == ["x", EOS]


def test_log_space_does_not_underflow() -> None:
    vocab = ["a", "b", "c", "d", "e", EOS]
    probs = [0.25, 0.175, 0.175, 0.175, 0.175, 0.05]
    steps = 600

    def model(prefix):
        if len(prefix) >= steps:
            return {w: (0.0 if w == EOS else NEG_INF) for w in vocab}
        return {w: math.log(p) for w, p in zip(vocab, probs)}

    y, s = greedy_decode(model, steps + 1)
    assert y == ["a"] * steps + [EOS]
    assert math.prod([0.25] * steps) == 0.0
    assert math.isclose(s, steps * math.log(0.25))
