# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/forced-alignment/. The authors are listed in prov/4HHCES.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

import nlslog
from forced_alignment import align_transcript, expand_transcript, forced_align, segments
from nlslog import (
    BOOLEAN,
    COUNTING,
    LOG,
    LOG_COST,
    NEG_INF,
    POS_INF,
    PROB,
    TROPICAL,
    VITERBI,
    argmax,
    log_add,
    log_normalize,
    log_softmax,
    log_sum,
    safe_log,
    softmax,
    sr_prod,
    sr_sum,
)

# ---------------------------------------------------------------- the shared helper nlslog.py


def test_helper_header():
    with open(nlslog.__file__, encoding="utf-8") as f:
        lines = f.read().splitlines()
    assert lines[1] == "# Shared helper of the natural-language-and-speech pages of https://algorithm.tamnd.com/. The authors are listed in prov/."


def test_safe_log():
    assert safe_log(0) == NEG_INF
    assert safe_log(1) == 0.0
    assert safe_log(F(1, 2)) == pytest.approx(math.log(0.5), abs=1e-15)
    with pytest.raises(ValueError):
        safe_log(-0.1)


def test_log_add_check_value():
    v = log_add(math.log(0.5), math.log(0.25))
    assert v == pytest.approx(math.log(0.75), abs=1e-12)
    assert round(v, 6) == -0.287682


def test_log_add_edges():
    assert log_add(NEG_INF, NEG_INF) == NEG_INF
    assert log_add(NEG_INF, -3.0) == -3.0
    assert log_add(-3.0, NEG_INF) == -3.0
    assert log_add(-1000.0, -1000.0) == pytest.approx(-1000.0 + math.log(2), abs=1e-12)
    assert log_add(1000.0, 999.0) == pytest.approx(1000.0 + math.log1p(math.exp(-1.0)), abs=1e-9)
    assert log_add(POS_INF, 0.0) == POS_INF


def test_log_sum():
    assert log_sum([]) == NEG_INF
    assert log_sum([NEG_INF, NEG_INF]) == NEG_INF
    assert log_sum([-1000.0] * 1000) == pytest.approx(-1000.0 + math.log(1000), abs=1e-9)
    rng = random.Random(1)
    xs = [rng.uniform(-5, 5) for _ in range(20)]
    assert log_sum(xs) == pytest.approx(math.log(sum(math.exp(x) for x in xs)), abs=1e-12)
    acc = NEG_INF
    for x in xs:
        acc = log_add(acc, x)
    assert acc == pytest.approx(log_sum(xs), abs=1e-12)


def test_log_normalize_and_log_softmax():
    xs = [math.log(3.0), math.log(1.0), NEG_INF]
    ys = log_normalize(xs)
    assert [math.exp(y) for y in ys] == pytest.approx([0.75, 0.25, 0.0], abs=1e-15)
    assert sum(math.exp(y) for y in log_softmax([2.0, 1.0, 0.0])) == pytest.approx(1.0, abs=1e-15)
    assert log_softmax([-2000.0, -2001.0]) == pytest.approx(log_normalize([0.0, -1.0]), abs=1e-12)
    with pytest.raises(ValueError):
        log_normalize([NEG_INF, NEG_INF])


def test_softmax_temperature_check_values():
    assert softmax([2, 1, 0]) == pytest.approx([0.66524, 0.24473, 0.09003], abs=5e-6)
    assert softmax([2, 1, 0], temperature=0.5) == pytest.approx([0.86681, 0.11731, 0.01588], abs=5e-6)
    assert softmax([2, 1, 0], temperature=2) == pytest.approx([0.50648, 0.30720, 0.18632], abs=5e-6)
    assert softmax([1000.0, 999.0, NEG_INF]) == pytest.approx(softmax([1.0, 0.0])[:2] + [0.0], abs=1e-15)
    with pytest.raises(ValueError):
        softmax([1.0], temperature=0)


def test_argmax_first_on_ties():
    assert argmax([1, 3, 3, 2]) == 1
    assert argmax([NEG_INF, NEG_INF]) == 0
    assert argmax([F(1, 3), F(2, 3), F(2, 3)]) == 1
    with pytest.raises(ValueError):
        argmax([])


SAMPLES = {
    "probability": [0, 1, F(1, 2), F(1, 3), F(5, 4)],
    "log": [NEG_INF, 0.0, -0.5, -2.0, 1.25],
    "viterbi": [NEG_INF, 0.0, -0.5, -2.0, 1.25],
    "tropical": [POS_INF, 0.0, 0.5, 2.0, -1.25],
    "log-cost": [POS_INF, 0.0, 0.5, 2.0, -1.25],
    "boolean": [False, True],
    "counting": [0, 1, 2, 3, 7],
}


def same(a, b):
    if isinstance(a, float) and isinstance(b, float):
        if math.isinf(a) or math.isinf(b):
            return a == b
        return abs(a - b) <= 1e-12 * max(1.0, abs(a), abs(b))
    return a == b


@pytest.mark.parametrize("sr", [PROB, LOG, VITERBI, TROPICAL, LOG_COST, BOOLEAN, COUNTING], ids=lambda s: s.name)
def test_semiring_axioms(sr):
    xs = SAMPLES[sr.name]
    for a in xs:
        assert same(sr.plus(a, sr.zero), a)
        assert same(sr.plus(sr.zero, a), a)
        assert same(sr.times(a, sr.one), a)
        assert same(sr.times(sr.one, a), a)
        assert same(sr.times(a, sr.zero), sr.zero)
        assert same(sr.times(sr.zero, a), sr.zero)
        if sr.idempotent:
            assert same(sr.plus(a, a), a)
        for b in xs:
            assert same(sr.plus(a, b), sr.plus(b, a))
            for c in xs:
                assert same(sr.plus(sr.plus(a, b), c), sr.plus(a, sr.plus(b, c)))
                assert same(sr.times(sr.times(a, b), c), sr.times(a, sr.times(b, c)))
                assert same(sr.times(a, sr.plus(b, c)), sr.plus(sr.times(a, b), sr.times(a, c)))
                assert same(sr.times(sr.plus(a, b), c), sr.plus(sr.times(a, c), sr.times(b, c)))
    if not sr.idempotent:
        assert any(not same(sr.plus(a, a), a) for a in xs)


def test_semirings_agree_on_one_sum():
    ps = [F(1, 2), F(1, 4), F(1, 8)]
    assert sr_sum(PROB, ps) == F(7, 8)
    assert sr_prod(PROB, ps) == F(1, 64)
    assert sr_sum(LOG, [math.log(p) for p in ps]) == pytest.approx(math.log(7 / 8), abs=1e-12)
    assert sr_sum(VITERBI, [math.log(p) for p in ps]) == pytest.approx(math.log(0.5), abs=1e-15)
    assert sr_sum(TROPICAL, [-math.log(p) for p in ps]) == pytest.approx(-math.log(0.5), abs=1e-15)
    assert sr_sum(LOG_COST, [-math.log(p) for p in ps]) == pytest.approx(-math.log(7 / 8), abs=1e-12)
    assert sr_prod(LOG, [math.log(p) for p in ps]) == pytest.approx(math.log(1 / 64), abs=1e-12)
    assert sr_sum(BOOLEAN, [False, True]) is True
    assert sr_prod(BOOLEAN, [True, False]) is False
    assert sr_sum(COUNTING, [2, 3]) == 5
    assert sr_sum(LOG, []) == NEG_INF
    assert sr_prod(TROPICAL, []) == 0.0


# ---------------------------------------------------------------- forced alignment


def compositions(T, S):
    """All ways to give S states durations >= 1 that sum to T."""
    if S == 1:
        yield (T,)
        return
    for d in range(1, T - S + 2):
        for rest in compositions(T - d, S - 1):
            yield (d,) + rest


def path_of(durs):
    return [j for j, d in enumerate(durs) for _ in range(d)]


def path_score(path, log_emit, log_self, log_next):
    s = log_emit[0][path[0]]
    for t in range(1, len(path)):
        i, j = path[t - 1], path[t]
        s += (log_self[i] if i == j else log_next[i]) + log_emit[t][j]
    return s


def random_chain(rng, T, S):
    log_emit = [[math.log(rng.uniform(0.01, 1.0)) for _ in range(S)] for _ in range(T)]
    ps = [rng.uniform(0.1, 0.9) for _ in range(S)]
    return log_emit, [math.log(p) for p in ps], [math.log(1 - p) for p in ps]


def test_number_of_segmentations():
    from math import comb

    for T in range(1, 9):
        for S in range(1, T + 1):
            assert sum(1 for _ in compositions(T, S)) == comb(T - 1, S - 1)


def test_against_brute_force():
    rng = random.Random(7)
    for _ in range(150):
        S = rng.randint(1, 4)
        T = rng.randint(S, 8)
        le, ls, ln = random_chain(rng, T, S)
        path, score = forced_align(le, ls, ln)
        best = max(compositions(T, S), key=lambda d: path_score(path_of(d), le, ls, ln))
        assert score == pytest.approx(path_score(path_of(best), le, ls, ln), abs=1e-9)
        assert path_score(path, le, ls, ln) == pytest.approx(score, abs=1e-9)
        assert path == path_of(best)
        assert path[0] == 0 and path[-1] == S - 1
        assert all(path[t] - path[t - 1] in (0, 1) for t in range(1, T))


def test_tie_keeps_the_self_loop():
    le = [[0.0, 0.0]] * 3
    ls = [math.log(0.5)] * 2
    path, score = forced_align(le, ls, ls)
    # Both paths score 2 log 0.5; the traceback stays, so the last state keeps more frames.
    assert path == [0, 1, 1]
    assert score == pytest.approx(2 * math.log(0.5), abs=1e-12)
    # Exact ties in integers: the rule gives the optimum whose reversed path is largest.
    rng = random.Random(2)
    for _ in range(100):
        S = rng.randint(1, 3)
        T = rng.randint(S, 7)
        le = [[float(rng.randint(-2, 0)) for _ in range(S)] for _ in range(T)]
        ls = [-1.0] * S
        ln = [-1.0] * S
        path, score = forced_align(le, ls, ln)
        best = max(compositions(T, S), key=lambda d: (path_score(path_of(d), le, ls, ln), path_of(d)[::-1]))
        assert path == path_of(best)


def test_errors():
    with pytest.raises(ValueError):
        forced_align([[0.0, 0.0]], [0.0, 0.0], [0.0, 0.0])
    with pytest.raises(ValueError):
        forced_align([[0.0, NEG_INF], [0.0, NEG_INF]], [0.0, 0.0], [0.0, 0.0])


LEX = {"a": [["ah"], ["ey"]], "cat": [["k", "ae", "t"]], "sat": [["s", "ae", "t"]]}


def test_expand_and_segments():
    labels = expand_transcript(["a", "cat"], LEX, states_per_phone=2)
    assert [l[3] for l in labels] == ["ah", "ah", "k", "k", "ae", "ae", "t", "t"]
    path = [0, 1, 1, 2, 3, 4, 4, 5, 6, 7]
    assert segments(path, labels, "word") == [("a", 0, 3), ("cat", 3, 10)]
    assert segments(path, labels, "phone") == [("ah", 0, 3), ("k", 3, 5), ("ae", 5, 8), ("t", 8, 10)]
    assert len(segments(path, labels, "state")) == 8
    with pytest.raises(KeyError):
        expand_transcript(["dog"], LEX)


def planted(rng, phones, durs, sd=0.3):
    """Frames from a 1-D Gaussian per phone, with the phone durations given."""
    means = {ph: float(i) for i, ph in enumerate(sorted(set(phones)))}
    xs = []
    for ph, d in zip(phones, durs):
        xs += [rng.gauss(means[ph], sd) for _ in range(d)]
    return xs, means


def gauss_log(x, m, sd):
    return -0.5 * math.log(2 * math.pi * sd * sd) - (x - m) ** 2 / (2 * sd * sd)


def test_recovers_planted_boundaries():
    rng = random.Random(3)
    words = ["a", "cat", "sat"]
    phones = ["ah", "k", "ae", "t", "s", "ae", "t"]
    durs = [9, 6, 12, 5, 8, 10, 7]
    xs, means = planted(rng, phones, durs, sd=0.1)
    spans, _ = align_transcript(words, LEX, lambda t, ph, s: gauss_log(xs[t], means[ph], 0.1), len(xs), states_per_phone=1)
    ends = [e for _, _, e in spans]
    assert [p for p, _, _ in spans] == phones
    assert ends == [sum(durs[: i + 1]) for i in range(len(durs))]
    wspans, _ = align_transcript(words, LEX, lambda t, ph, s: gauss_log(xs[t], means[ph], 0.1), len(xs), states_per_phone=1, level="word")
    assert wspans == [("a", 0, 9), ("cat", 9, 32), ("sat", 32, 57)]


def naive_product_align(log_emit, log_self, log_next):
    """The same recursion with plain products of probabilities (no logs)."""
    T, S = len(log_emit), len(log_self)
    d = [math.exp(log_emit[0][0])] + [0.0] * (S - 1)
    for t in range(1, T):
        d = [max(d[j] * math.exp(log_self[j]), d[j - 1] * math.exp(log_next[j - 1]) if j else 0.0) * math.exp(log_emit[t][j]) for j in range(S)]
    return d[S - 1]


def test_long_utterance_underflows_without_logs():
    rng = random.Random(11)
    words = ["cat", "sat"]
    phones = ["k", "ae", "t", "s", "ae", "t"]
    durs = [30, 40, 25, 35, 40, 30]  # 200 frames
    xs, means = planted(rng, phones, durs, sd=0.2)
    # A discrete-like score: each frame gets probability at most 0.02.
    def log_b(t, ph, s):
        return math.log(0.02) + gauss_log(xs[t], means[ph], 0.2) - gauss_log(means[ph], means[ph], 0.2)

    labels = expand_transcript(words, LEX, 1)
    le = [[log_b(t, l[3], l[4]) for l in labels] for t in range(len(xs))]
    ls = [math.log(0.9)] * len(labels)
    ln = [math.log(0.1)] * len(labels)
    assert naive_product_align(le, ls, ln) == 0.0
    path, score = forced_align(le, ls, ln)
    assert score > -1500 and math.isfinite(score)
    spans = segments(path, labels, "phone")
    assert [e for _, _, e in spans] == [sum(durs[: i + 1]) for i in range(len(durs))]


def test_one_state_per_frame_is_forced():
    rng = random.Random(5)
    le, ls, ln = random_chain(rng, 4, 4)
    path, _ = forced_align(le, ls, ln)
    assert path == [0, 1, 2, 3]
