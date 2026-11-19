# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/grid-beam-search/. The authors are listed in prov/ZN2NZT.jsonl.

import math
import random

from grid_beam_search import EOS, grid_beam_search
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
    def model(prefix):
        if len(prefix) >= n - 1:
            return {w: (0.0 if w == EOS else NEG_INF) for w in vocab}
        rng = random.Random(f"{seed}|{' '.join(prefix)}")
        raw = [math.log(rng.random() ** 2 + 1e-3) for _ in vocab]
        return dict(zip(vocab, log_normalize(raw)))

    return model


def exhaustive(model, n):
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


def holds(tokens, phrases):
    """True if the phrases fit at disjoint contiguous places of tokens (without "</s>")."""
    body = tokens[:-1]

    def place(i, used):
        if i == len(phrases):
            return True
        p = phrases[i]
        for s in range(len(body) - len(p) + 1):
            span = set(range(s, s + len(p)))
            if body[s : s + len(p)] == p and not (span & used) and place(i + 1, used | span):
                return True
        return False

    return place(0, frozenset())


def best_constrained(model, phrases, n):
    good = [(y, s) for y, s in exhaustive(model, n) if holds(y, phrases)]
    return max(good, key=lambda t: t[1]) if good else None


def test_example() -> None:
    stats = {}
    y, s = grid_beam_search(m1, [["a"]], 3, 1, stats)
    assert y == ["a", "a", EOS]
    assert math.isclose(math.exp(s), 0.2)
    assert stats["calls"] == 4
    assert best_constrained(m1, [["a"]], 3)[0] == ["a", "a", EOS]
    # Without the constraint the best output is b</s>.
    assert max(exhaustive(m1, 3), key=lambda t: t[1])[0] == ["b", EOS]
    y, s = grid_beam_search(m1, [["b"]], 3, 1)
    assert y == ["b", EOS] and math.isclose(math.exp(s), 0.36)


def test_holds() -> None:
    assert holds(["x", "a", "b", EOS], [["a", "b"]])
    assert not holds(["a", "x", "b", EOS], [["a", "b"]])
    assert not holds(["a", EOS], [["a"], ["a"]])
    assert holds(["a", "a", EOS], [["a"], ["a"]])
    assert holds(["a", "b", "a", EOS], [["b", "a"], ["a"]])


def test_wide_grid_is_exact() -> None:
    vocab = ["a", "b", "c", EOS]
    cases = [[["a"]], [["b", "c"]], [["a"], ["c"]], [["c", "a"], ["b"]], [["a"], ["a"]], []]
    for seed in range(25):
        model = random_model(seed, vocab, 5)
        for phrases in cases:
            got = grid_beam_search(model, phrases, 5, 10**6)
            want = best_constrained(model, phrases, 5)
            assert math.isclose(got[1], want[1])
            assert holds(got[0], phrases)


def test_narrow_grid_can_fail() -> None:
    vocab = ["a", "b", "c", EOS]
    phrases = [["b", "c"]]
    model = random_model(0, vocab, 5)
    got = grid_beam_search(model, phrases, 5, 1)
    want = best_constrained(model, phrases, 5)
    assert got[0] == ["b", "c", EOS]
    assert want[0] == ["a", "c", "b", "c", EOS]
    assert got[1] < want[1] - 2.0
    assert math.isclose(grid_beam_search(model, phrases, 5, 10**6)[1], want[1])
    fails = 0
    for seed in range(40):
        model = random_model(seed, vocab, 5)
        got = grid_beam_search(model, phrases, 5, 1)
        want = best_constrained(model, phrases, 5)
        assert holds(got[0], phrases) and got[1] <= want[1] + 1e-12
        fails += got[1] < want[1] - 1e-12
    assert 0 < fails < 40


def test_model_calls_are_at_most_n_k_c() -> None:
    vocab = ["a", "b", "c", EOS]
    for seed in range(20):
        model = random_model(seed, vocab, 6)
        for phrases in ([["a"]], [["a", "b"], ["c"]]):
            total = sum(len(p) for p in phrases)
            for width in (1, 2, 4):
                stats = {}
                grid_beam_search(model, phrases, 6, width, stats)
                assert stats["calls"] <= 6 * width * (total + 1)


def test_no_room_for_the_constraints() -> None:
    vocab = ["a", "b", EOS]
    model = random_model(1, vocab, 3)
    assert grid_beam_search(model, [["a", "b", "a"]], 3, 4) is None
    assert best_constrained(model, [["a", "b", "a"]], 3) is None
