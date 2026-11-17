# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/em-isoform-quantification/. The authors are listed in prov/QSYASY.jsonl.

import random

from em_isoform_quantification import (effective_length, em, equivalence_classes,
                                       log_likelihood, tpm, transcript_fractions)


def random_case(rng: random.Random, m: int, n_classes: int):
    eff_len = [float(rng.randint(50, 2000)) for _ in range(m)]
    classes = []
    for _ in range(n_classes):
        e = tuple(sorted(rng.sample(range(m), rng.randint(1, m))))
        classes.append((e, rng.randint(1, 50)))
    return classes, eff_len


def test_tpm_check_values():
    # Lengths 1000, 2000 and 500 with 100 reads each: alpha is 1/3 each.
    out = tpm([1 / 3, 1 / 3, 1 / 3], [1000, 2000, 500])
    assert [round(x) for x in out] == [285714, 142857, 571429]
    assert abs(sum(out) - 1e6) < 1e-6


def test_unique_reads_give_the_counts():
    # Every read is unique to one transcript: EM returns the read fractions.
    alpha = em([((0,), 30), ((1,), 50), ((2,), 20)], [100.0, 200.0, 300.0])
    assert all(abs(a - b) < 1e-9 for a, b in zip(alpha, [0.3, 0.5, 0.2]))


def test_worked_example():
    # The example of the page: A has length 1000, B has length 500.
    classes = [((0,), 30), ((0, 1), 40), ((1,), 30)]
    trace = []
    alpha = em(classes, [1000.0, 500.0], trace=trace)
    assert abs(alpha[0] - 0.4) < 1e-6 and abs(alpha[1] - 0.6) < 1e-6
    assert [round(x) for x in tpm(alpha, [1000.0, 500.0])] == [250000, 750000]
    assert abs(trace[0] - log_likelihood([0.5, 0.5], classes, [1000.0, 500.0])) < 1e-12


def test_two_transcripts_against_ternary_search():
    rng = random.Random(1)
    for _ in range(300):
        classes, eff_len = random_case(rng, 2, 3)
        alpha = em(classes, eff_len, max_iter=3000)
        f = lambda x: log_likelihood([x, 1 - x], classes, eff_len)
        lo, hi = 0.0, 1.0
        for _ in range(200):
            a, b = lo + (hi - lo) / 3, hi - (hi - lo) / 3
            if f(a) < f(b):
                lo = a
            else:
                hi = b
        best = max(f(lo), f(0.0), f(1.0))
        assert log_likelihood(alpha, classes, eff_len) >= best - 1e-6


def test_three_transcripts_against_a_grid():
    rng = random.Random(2)
    steps = 40
    grid = [(i / steps, j / steps, (steps - i - j) / steps)
            for i in range(steps + 1) for j in range(steps + 1 - i)]
    for _ in range(150):
        classes, eff_len = random_case(rng, 3, 4)
        alpha = em(classes, eff_len, max_iter=3000)
        best = max(log_likelihood(g, classes, eff_len) for g in grid)
        assert log_likelihood(alpha, classes, eff_len) >= best - 1e-6
        assert abs(sum(alpha) - 1.0) < 1e-9 and min(alpha) >= 0.0


def test_likelihood_never_decreases():
    rng = random.Random(3)
    for _ in range(200):
        classes, eff_len = random_case(rng, rng.randint(2, 6), rng.randint(1, 8))
        trace = []
        em(classes, eff_len, max_iter=200, trace=trace)
        for a, b in zip(trace, trace[1:]):
            assert b >= a - 1e-9 * max(1.0, abs(a))


def test_ridge_when_classes_do_not_separate():
    # Every read fits both transcripts and the lengths are equal: every split is a maximum.
    classes = [((0, 1), 100)]
    alpha = em(classes, [500.0, 500.0])
    assert alpha == [0.5, 0.5]
    assert abs(log_likelihood([0.2, 0.8], classes, [500.0, 500.0])
               - log_likelihood(alpha, classes, [500.0, 500.0])) < 1e-9


def test_simulated_reads():
    # Segments of the genome and the transcripts that contain each of them.
    segments = [(300, (0, 1)), (200, (0,)), (400, (1, 2)), (100, (2,))]
    lengths = [sum(n for n, ts in segments if t in ts) for t in range(3)]
    true_alpha = [0.5, 0.2, 0.3]
    rng = random.Random(4)
    reads = []
    for _ in range(20000):
        u, t = rng.random(), 0
        while u >= sum(true_alpha[:t + 1]):
            t += 1
        x = rng.random() * lengths[t]
        for n, ts in segments:
            if t in ts:
                if x < n:
                    reads.append(ts)
                    break
                x -= n
    classes = equivalence_classes(reads)
    assert [e for e, _ in classes] == [(0,), (0, 1), (1, 2), (2,)]
    alpha = em(classes, [float(x) for x in lengths])
    assert all(abs(a - b) < 0.02 for a, b in zip(alpha, true_alpha))


def test_helpers():
    assert effective_length(1000, 200) == 801.0
    assert effective_length(150, 200) == 1.0
    assert equivalence_classes([[1, 0], [0, 1], [2], []]) == [((), 1), ((0, 1), 2), ((2,), 1)]
    assert abs(sum(transcript_fractions([0.2, 0.8], [10.0, 40.0])) - 1.0) < 1e-12
