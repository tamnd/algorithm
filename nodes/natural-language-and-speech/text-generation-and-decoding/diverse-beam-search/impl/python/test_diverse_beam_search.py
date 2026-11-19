# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/diverse-beam-search/. The authors are listed in prov/K6SZXR.jsonl.

import math
import random
from collections import Counter

from diverse_beam_search import EOS, diverse_beam_search, hamming_penalty
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


def beam_search(model, max_len, width):
    """Plain beam search with the same rules: finished outputs leave the beam."""
    beam, finished = [((), 0.0)], []
    for _ in range(max_len):
        cand = []
        for y, s in beam:
            for w, lp in model(y).items():
                if lp != NEG_INF:
                    cand.append((s + lp, y + (w,)))
        order = sorted(range(len(cand)), key=lambda i: (-cand[i][0], i))
        beam = []
        for i in order[:width]:
            s, y = cand[i]
            if y[-1] == EOS:
                finished.append((list(y), s))
            else:
                beam.append((y, s))
        if not beam:
            break
    return sorted(finished, key=lambda t: -t[1])


def test_example_two_groups() -> None:
    out = diverse_beam_search(m1, 3, groups=2, width=1, lam=0.5)
    assert [(y, g) for y, _, g in out] == [(["b", EOS], 1), (["a", "a", EOS], 0)]
    assert math.isclose(math.exp(out[0][1]), 0.36)
    assert math.isclose(math.exp(out[1][1]), 0.2)
    # Below ln(0.5 / 0.4) the penalty is too weak and both groups give aa</s>.
    assert math.isclose(math.log(0.5 / 0.4), 0.22314355131420976)
    out = diverse_beam_search(m1, 3, groups=2, width=1, lam=0.2)
    assert [y for y, _, _ in out] == [["a", "a", EOS], ["a", "a", EOS]]
    out = diverse_beam_search(m1, 3, groups=2, width=1, lam=0.23)
    assert [y for y, _, _ in out] == [["b", EOS], ["a", "a", EOS]]


def test_hamming_penalty_counts_uses() -> None:
    used = Counter(["a", "a", "b"])
    assert hamming_penalty("a", used, 0.5) == 1.0
    assert hamming_penalty("b", used, 0.5) == 0.5
    assert hamming_penalty("c", used, 0.5) == 0.0


def test_one_group_is_beam_search() -> None:
    vocab = ["a", "b", "c", EOS]
    for seed in range(60):
        model = random_model(seed, vocab, 5)
        for width in (1, 2, 3):
            got = [(y, s) for y, s, _ in diverse_beam_search(model, 5, 1, width, 0.7)]
            want = beam_search(model, 5, width)
            assert [y for y, _ in got] == [y for y, _ in want]


def test_first_group_is_plain_beam_search() -> None:
    # Group 1 sees no penalty, so its outputs are those of beam search of width B'.
    vocab = ["a", "b", "c", EOS]
    for seed in range(60):
        model = random_model(seed, vocab, 5)
        out = diverse_beam_search(model, 5, 3, 2, 1.0)
        first = sorted([(y, s) for y, s, g in out if g == 0], key=lambda t: -t[1])
        want = beam_search(model, 5, 2)
        assert [y for y, _ in first] == [y for y, _ in want]
        assert out[0][1] >= want[0][1] - 1e-12


def test_zero_penalty_repeats_beam_search() -> None:
    vocab = ["a", "b", "c", EOS]
    for seed in range(40):
        model = random_model(seed, vocab, 5)
        out = diverse_beam_search(model, 5, 3, 2, 0.0)
        want = [y for y, _ in beam_search(model, 5, 2)]
        for g in range(3):
            mine = [y for y, s, gg in sorted(out, key=lambda t: -t[1]) if gg == g]
            assert mine == want


def test_wide_groups_are_exact() -> None:
    vocab = ["a", "b", EOS]
    for seed in range(40):
        model = random_model(seed, vocab, 4)
        everything = exhaustive(model, 4)
        out = diverse_beam_search(model, 4, 2, len(everything), 3.0)
        best = max(s for _, s in everything)
        assert math.isclose(out[0][1], best)
        for y, s, _ in out:
            assert any(o == y and math.isclose(sc, s) for o, sc in everything)


def test_penalty_raises_diversity() -> None:
    vocab = ["a", "b", "c", "d", EOS]
    distinct0 = distinct1 = 0
    for seed in range(60):
        model = random_model(seed, vocab, 5)
        out0 = diverse_beam_search(model, 5, 4, 1, 0.0)
        out1 = diverse_beam_search(model, 5, 4, 1, 2.0)
        distinct0 += len({tuple(y) for y, _, _ in out0})
        distinct1 += len({tuple(y) for y, _, _ in out1})
    assert distinct0 == 60
    assert distinct1 > 3 * distinct0
