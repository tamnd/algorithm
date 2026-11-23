# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sparse-vector-technique/. The authors are listed in prov/QVW2C4.jsonl.

import itertools
import math
import random

import dpkit
from sparse_vector_technique import above_threshold, accuracy_alpha, laplace_noise, sparse

UNIVERSE = (0, 1, 2)


def _counting_queries() -> list:
    # Counting queries have sensitivity 1 under add/remove.
    return [
        lambda x: sum(1 for r in x if r == 0),
        lambda x: sum(1 for r in x if r <= 1),
        lambda x: sum(1 for r in x if r == 2),
        lambda x: len(x),
    ]


def _lap_cdf(z: float, b: float) -> float:
    return 0.5 * math.exp(z / b) if z < 0 else 1.0 - 0.5 * math.exp(-z / b)


def _lap_pdf(z: float, b: float) -> float:
    return math.exp(-abs(z) / b) / (2.0 * b)


def _simpson(g, lo: float, hi: float, n: int) -> float:
    if hi <= lo:
        return 0.0
    n += n % 2
    h = (hi - lo) / n
    s = g(lo) + g(hi)
    for j in range(1, n):
        s += (4 if j % 2 else 2) * g(lo + j * h)
    return s * h / 3.0


def exact_pmf(answers: tuple, threshold: float, epsilon: float) -> dict:
    """The exact pmf of the halting index of AboveThreshold, by numerical integration.

    Output k in 0..m-1 means a top at query k; output m means all bottoms.
    The integrand is smooth between the break points T and a_i, so Simpson's
    rule on each piece is accurate to about 1e-10 here.
    """
    bt, bq = 2.0 / epsilon, 4.0 / epsilon
    m = len(answers)
    lo, hi = threshold - 40 * bt, threshold + 40 * bt
    cuts = sorted({lo, hi, threshold, *[a for a in answers if lo < a < hi]})
    pmf = {}
    for k in range(m + 1):
        def g(t: float, k: int = k) -> float:
            v = _lap_pdf(t - threshold, bt)
            for i in range(min(k, m)):
                v *= _lap_cdf(t - answers[i], bq)  # P(a_i + nu_i < t)
            if k < m:
                v *= 1.0 - _lap_cdf(t - answers[k], bq)  # P(a_k + nu_k >= t)
            return v
        pmf[k] = sum(_simpson(g, a, b, max(40, int(40 * (b - a) / bt))) for a, b in zip(cuts, cuts[1:]))
    return pmf


def _all_datasets(max_n: int) -> list:
    out = []
    for n in range(max_n + 1):
        out.extend(itertools.combinations_with_replacement(UNIVERSE, n))
    return out


def test_laplace_noise_moments() -> None:
    rng = random.Random(1)
    b = 2.0
    zs = [laplace_noise(b, rng) for _ in range(2000)]
    # P(|Z| > 2 ln 10) = 0.1 for b = 2 (a check value of the area).
    frac = sum(1 for z in zs if abs(z) > 2 * math.log(10)) / len(zs)
    assert abs(frac - 0.1) <= dpkit.hoeffding_margin(len(zs), 1e-6)


def test_exact_pmf_is_a_pmf() -> None:
    pmf = exact_pmf((1, 3, 0), 2.0, 1.0)
    assert abs(sum(pmf.values()) - 1.0) < 1e-8
    assert all(p > 0 for p in pmf.values())


def test_above_threshold_is_epsilon_dp_on_all_pairs() -> None:
    epsilon, threshold = 1.0, 1.5
    qs = _counting_queries()
    cache: dict = {}

    def mech_pmf(x: tuple) -> dict:
        key = tuple(q(x) for q in qs)
        if key not in cache:
            cache[key] = exact_pmf(key, threshold, epsilon)
        return cache[key]

    pairs = [(x, y) for x in _all_datasets(2) for y in dpkit.neighbors_add_remove(x, UNIVERSE)]
    assert len(pairs) > 30
    assert dpkit.is_pure_dp(mech_pmf, pairs, epsilon, tol=1e-6)
    worst = max(dpkit.max_privacy_loss(mech_pmf(x), mech_pmf(y)) for x, y in pairs)
    assert 0.3 < worst <= epsilon + 1e-6  # the bound holds and the loss is not trivial


def test_variant_without_query_noise_is_not_private() -> None:
    # A variant that drops line L3 and does not halt after a top (Lyu, Su and Li
    # 2017 study such variants). On x = (0,) the answers are (1, 0) and on its
    # add/remove neighbor x' = (0, 1) they are (1, 1). The output (top, bottom)
    # needs a_1 >= T_hat > a_2, which has probability 0 on x', so no finite
    # epsilon holds. We compute both probabilities from the threshold noise alone.
    bt = 2.0

    def p_top_bottom(a1: float, a2: float, t: float = 0.5) -> float:
        if a1 <= a2:
            return 0.0
        return _lap_cdf(a1 - t, bt) - _lap_cdf(a2 - t, bt)

    p = {"tb": p_top_bottom(1, 0)}
    q = {"tb": p_top_bottom(1, 1)}
    assert p["tb"] > 0.1
    assert dpkit.max_privacy_loss(p, q) == math.inf


def _oracle(answers: list, threshold: float, epsilon: float, rng: random.Random) -> list:
    """An independent restatement: draw all noise first, then find the first index with a_i + nu_i >= T_hat."""
    t_hat = threshold + laplace_noise(2.0 / epsilon, rng)
    hits = []
    for i, a in enumerate(answers):
        nu = laplace_noise(4.0 / epsilon, rng)
        hits.append(a + nu >= t_hat)
        if hits[-1]:
            break
    return hits


def test_against_oracle_on_random_inputs() -> None:
    gen = random.Random(7)
    for trial in range(600):
        m = gen.randrange(0, 8)
        answers = [gen.randrange(-3, 12) for _ in range(m)]
        threshold = gen.uniform(0, 10)
        epsilon = gen.choice([0.25, 0.5, 1.0, 2.0])
        qs = [lambda x, a=a: a for a in answers]
        got = above_threshold(None, qs, threshold, 1.0, epsilon, random.Random(trial))
        want = _oracle(answers, threshold, epsilon, random.Random(trial))
        assert got == want
        assert got.count(True) <= 1
        assert not got or got[-1] or len(got) == m


def test_adaptive_queries_are_allowed() -> None:
    # The next query may depend on the earlier outputs; here it moves the bar.
    rng = random.Random(3)
    data = (0, 0, 1, 2, 2, 2)
    out: list = []

    def stream():
        for v in UNIVERSE:
            yield (lambda x, v=v: sum(1 for r in x if r == v))

    out = above_threshold(data, stream(), 2.5, 1.0, 50.0, rng)
    assert out == [False, False, True]  # with tiny noise the count 3 of value 2 is the first above 2.5


def test_empirical_halting_matches_exact_pmf() -> None:
    answers, threshold, epsilon = (0, 2, 1), 1.0, 1.0
    pmf = exact_pmf(answers, threshold, epsilon)
    rng = random.Random(11)
    n = 3000
    qs = [lambda x, a=a: a for a in answers]
    counts = [0] * (len(answers) + 1)
    for _ in range(n):
        out = above_threshold(None, qs, threshold, 1.0, epsilon, rng)
        counts[len(out) - 1 if out and out[-1] else len(answers)] += 1
    margin = dpkit.hoeffding_margin(n, 1e-6)
    for k, c in enumerate(counts):
        assert abs(c / n - pmf[k]) <= margin


def test_accuracy_theorem_3_24() -> None:
    k, beta, epsilon, threshold = 20, 0.1, 1.0, 100.0
    alpha = accuracy_alpha(k, beta, epsilon)
    rng = random.Random(5)
    answers = [threshold - alpha - 1] * (k - 1) + [threshold + alpha + 1]
    qs = [lambda x, a=a: a for a in answers]
    runs, bad = 1000, 0
    for _ in range(runs):
        out = above_threshold(None, qs, threshold, 1.0, epsilon, rng)
        wrong = any((o and a < threshold - alpha) or (not o and a > threshold + alpha) for o, a in zip(out, answers))
        bad += wrong
    assert bad / runs <= beta + dpkit.hoeffding_margin(runs, 1e-6)


def test_sparse_stops_after_cutoff() -> None:
    rng = random.Random(9)
    answers = [50, 0, 50, 50, 0, 50, 50]
    qs = [lambda x, a=a: a for a in answers]
    for _ in range(200):
        out = sparse(None, qs, 25.0, 2, 1.0, 20.0, rng)
        assert out.count(True) <= 2
        if out.count(True) == 2:
            assert out[-1]


def test_bad_parameters() -> None:
    rng = random.Random(0)
    for args in [(0.0, 1.0), (1.0, 0.0)]:
        try:
            above_threshold(None, [], 0.0, args[0], args[1], rng)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError")
    assert above_threshold(None, [], 0.0, 1.0, 1.0, rng) == []
