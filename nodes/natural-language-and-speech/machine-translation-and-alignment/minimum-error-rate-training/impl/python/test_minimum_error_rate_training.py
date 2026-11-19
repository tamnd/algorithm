# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimum-error-rate-training/. The authors are listed in prov/P668TA.jsonl.

import math
import random

from minimum_error_rate_training import (
    bleu,
    bleu_stats,
    choose,
    corpus_value,
    dot,
    line_search,
    mert,
    upper_envelope,
)


def errors(stats: tuple) -> float:
    return -stats[0]


EXAMPLE = [
    [((-1.0, 0.0), (2,)), ((-2.0, 1.0), (0,)), ((-4.0, 2.0), (1,))],
    [((-1.0, 0.0), (1,)), ((-2.5, 2.0), (0,)), ((-5.0, 4.0), (2,))],
]


def test_example() -> None:
    w, d = (1.0, 0.0), (0.0, 1.0)
    envs = [upper_envelope([(dot(d, h), dot(w, h), c) for c, (h, _) in enumerate(cs)]) for cs in EXAMPLE]
    assert envs[0] == [(-math.inf, 0), (1.0, 1), (2.0, 2)]
    assert envs[1] == [(-math.inf, 0), (0.75, 1), (1.25, 2)]
    gamma, value = line_search(w, d, EXAMPLE, errors)
    assert gamma == 1.125 and value == 0
    assert [corpus_value((1.0, g), EXAMPLE, errors) for g in (0.5, 0.9, 1.1, 1.5, 2.5)] == [-3, -2, 0, -2, -3]
    w2, v2 = mert(EXAMPLE, w, errors)
    assert v2 == 0 and corpus_value(w2, EXAMPLE, errors) == 0


def test_bleu_check_values() -> None:
    st = bleu_stats("the cat sat on the mat".split(), ["the cat sat on the red mat".split()])
    assert st == (6, 4, 3, 2, 6, 5, 4, 3, 6, 7)
    assert math.isclose(bleu(st), 0.673182, abs_tol=1e-6)
    st = bleu_stats("the the the the the the the".split(), ["the cat is on the mat".split()], max_n=1)
    assert st[:2] == (2, 7)
    assert bleu((1, 0, 0, 0, 1, 0, 0, 0, 1, 1)) == 0.0


def test_envelope_against_brute_force() -> None:
    rng = random.Random(160)
    for _ in range(300):
        n = rng.randint(1, 8)
        lines = [(rng.randint(-4, 4) * 0.5, rng.randint(-6, 6) * 0.5, c) for c in range(n)]
        env = upper_envelope(lines)
        starts = [s for s, _ in env]
        assert starts == sorted(starts) and starts[0] == -math.inf
        for _ in range(30):
            g = rng.uniform(-20, 20)
            if any(abs(g - s) < 1e-9 for s in starts):
                continue
            want = max(lines, key=lambda x: (x[1] + x[0] * g, -x[2]))
            k = max(i for i, s in enumerate(starts) if s < g)
            got = lines[env[k][1]]
            assert math.isclose(got[1] + got[0] * g, want[1] + want[0] * g, abs_tol=1e-12)


def random_nbest(rng: random.Random, sents: int, n: int, dim: int) -> list:
    refs = [[rng.choice("abcde") for _ in range(rng.randint(4, 7))] for _ in range(sents)]
    nbest = []
    for r in refs:
        cands = []
        for _ in range(n):
            hyp = [rng.choice("abcde") if rng.random() < 0.4 else x for x in r]
            if rng.random() < 0.5:
                hyp = hyp[: rng.randint(2, len(hyp))]
            h = [rng.uniform(-3, 3) for _ in range(dim)]
            cands.append((h, bleu_stats(hyp, [r])))
        nbest.append(cands)
    return nbest


def smoothed_bleu(stats: tuple) -> float:
    """Add-one smoothing on the precisions, so that the grid sees small changes."""
    s = list(stats)
    for k in range(4):
        s[k] += 1
        s[4 + k] += 1
    return bleu(tuple(s))


def test_line_search_against_fine_grid() -> None:
    rng = random.Random(2003)
    for _ in range(6):
        nbest = random_nbest(rng, 4, 5, 3)
        w = [rng.uniform(-1, 1) for _ in range(3)]
        d = [rng.uniform(-1, 1) for _ in range(3)]
        for metric in (bleu, smoothed_bleu):
            gamma, value = line_search(w, d, nbest, metric)
            at = corpus_value([x + gamma * y for x, y in zip(w, d)], nbest, metric)
            assert math.isclose(at, value, abs_tol=1e-12)
            grid = max(
                corpus_value([x + (k / 100) * y for x, y in zip(w, d)], nbest, metric)
                for k in range(-1000, 1001)
            )
            assert value >= grid - 1e-12


def test_mert_never_decreases() -> None:
    rng = random.Random(4)
    for _ in range(10):
        nbest = random_nbest(rng, 5, 6, 3)
        w0 = [rng.uniform(-1, 1) for _ in range(3)]
        start = corpus_value(w0, nbest, smoothed_bleu)
        w, v = mert(nbest, w0, smoothed_bleu, extra_directions=[[1.0, 1.0, 0.0]])
        assert v >= start
        assert math.isclose(corpus_value(w, nbest, smoothed_bleu), v, abs_tol=1e-12)
        # each line through the result gives no further gain on the unit directions
        for j in range(3):
            d = [1.0 if k == j else 0.0 for k in range(3)]
            assert line_search(w, d, nbest, smoothed_bleu)[1] <= v + 1e-12


def test_choose_ties() -> None:
    cands = [((1.0,), (0,)), ((1.0,), (1,))]
    assert choose((2.0,), cands) == 0
