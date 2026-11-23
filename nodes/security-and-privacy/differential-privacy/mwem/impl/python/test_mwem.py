# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mwem/. The authors are listed in prov/R361Z0.jsonl.

import itertools
import math
import random

import dpkit
from mwem import (
    evaluate,
    exponential_mechanism_pmf,
    laplace_noise,
    max_error,
    mw_update,
    mwem,
    sample_index,
)

DOMAIN = (0, 1, 2)


def _hist(records, N=len(DOMAIN)):
    h = [0] * N
    for r in records:
        h[r] += 1
    return h


def _all_subset_queries(N):
    return [[1 if (mask >> x) & 1 else 0 for x in range(N)] for mask in range(1, 2 ** N)]


def _kl(p, q):
    return sum(a * math.log(a / b) for a, b in zip(p, q) if a > 0)


def test_selection_step_is_epsilon0_dp_on_all_replace_pairs() -> None:
    queries = _all_subset_queries(3)
    A = [4 / 3] * 3  # the synthetic data does not depend on the private data in round 1
    eps0 = 0.8

    def mech_pmf(records):
        B = _hist(records)
        scores = [abs(evaluate(q, A) - evaluate(q, B)) for q in queries]
        return dict(enumerate(exponential_mechanism_pmf(scores, eps0)))

    datasets = list(itertools.combinations_with_replacement(DOMAIN, 4))
    pairs = [(x, y) for x in datasets for y in dpkit.neighbors_replace(x, DOMAIN)]
    assert len(pairs) > 40
    assert dpkit.is_pure_dp(mech_pmf, pairs, eps0)
    worst = max(dpkit.max_privacy_loss(mech_pmf(x), mech_pmf(y)) for x, y in pairs)
    assert 0.2 < worst <= eps0 + 1e-12


def test_exponential_mechanism_pmf_against_direct_formula() -> None:
    rng = random.Random(1)
    for _ in range(500):
        scores = [rng.uniform(0, 20) for _ in range(rng.randrange(1, 8))]
        eps0 = rng.uniform(0.01, 3)
        z = sum(math.exp(eps0 * s / 2) for s in scores)
        want = [math.exp(eps0 * s / 2) / z for s in scores]
        got = exponential_mechanism_pmf(scores, eps0)
        assert all(math.isclose(a, b, rel_tol=1e-9) for a, b in zip(got, want))


def test_sampling_matches_pmf() -> None:
    rng = random.Random(2)
    pmf = exponential_mechanism_pmf([0.0, 1.0, 3.0, 2.0], 1.0)
    n = 4000
    emp = dpkit.empirical_pmf(sample_index(pmf, rng) for _ in range(n))
    margin = dpkit.hoeffding_margin(n, 1e-6)
    assert all(abs(emp.get(i, 0.0) - p) <= margin for i, p in enumerate(pmf))


def test_mw_update_matches_formula_and_keeps_total() -> None:
    rng = random.Random(3)
    for _ in range(500):
        N = rng.randrange(1, 7)
        A = [rng.uniform(0.1, 5) for _ in range(N)]
        n = sum(A)
        q = [rng.randrange(2) for _ in range(N)]
        m = rng.uniform(-n, 2 * n)
        got = mw_update(A, q, m, n)
        qa = sum(w * a for w, a in zip(q, A))
        raw = [a * math.exp(w * (m - qa) / (2 * n)) for a, w in zip(A, q)]
        want = [n * r / sum(raw) for r in raw]
        assert all(math.isclose(g, w, rel_tol=1e-9) for g, w in zip(got, want))
        assert math.isclose(sum(got), n, rel_tol=1e-12)


def test_kl_drop_of_one_update() -> None:
    # With b = B/n, a = A/n, u = q(A), v = q(B) and |m - u| <= 2n:
    # KL(b||a) - KL(b||a') >= ((u - v)^2 - (m - v)^2) / (4 n^2), the lemma of the proof.
    rng = random.Random(4)
    for _ in range(500):
        N = rng.randrange(2, 7)
        B = [rng.randrange(0, 6) for _ in range(N)]
        if sum(B) == 0:
            B[0] = 1
        n = sum(B)
        A = [rng.uniform(0.1, 3) for _ in range(N)]
        A = [n * a / sum(A) for a in A]
        q = [rng.randrange(2) for _ in range(N)]
        u, v = evaluate(q, A), evaluate(q, B)
        for m in (v, v + rng.uniform(-n, n)):
            m = max(u - 2 * n, min(u + 2 * n, m))
            A2 = mw_update(A, q, m, n)
            drop = _kl([b / n for b in B], [a / n for a in A]) - _kl([b / n for b in B], [a / n for a in A2])
            bound = ((u - v) ** 2 - (m - v) ** 2) / (4 * n * n)
            assert drop >= bound - 1e-12


def _oracle_mwem(B, queries, T, epsilon, rng):
    """An independent restatement in log space with explicit weights over the domain."""
    n = sum(B)
    N = len(B)
    logw = [0.0] * N
    avg = [0.0] * N

    def synth():
        top = max(logw)
        e = [math.exp(v - top) for v in logw]
        s = sum(e)
        return [n * v / s for v in e]

    for _ in range(T):
        A = synth()
        avg = [a + b / T for a, b in zip(avg, A)]
        weights = [math.exp(epsilon / (4 * T) * abs(sum(q[x] * (A[x] - B[x]) for x in range(N)))) for q in queries]
        u, acc, pick = rng.random() * sum(weights), 0.0, len(queries) - 1
        for i, w in enumerate(weights):
            acc += w
            if u < acc:
                pick = i
                break
        q = queries[pick]
        m = sum(q[x] * B[x] for x in range(N)) + laplace_noise(2 * T / epsilon, rng)
        qa = sum(q[x] * A[x] for x in range(N))
        logw = [logw[x] + q[x] * (m - qa) / (2 * n) for x in range(N)]
    return avg, synth()


def test_against_oracle_on_random_inputs() -> None:
    gen = random.Random(5)
    agree = 0
    for trial in range(500):
        N = gen.randrange(2, 6)
        B = [gen.randrange(0, 8) for _ in range(N)]
        B[gen.randrange(N)] += 1
        queries = [[gen.randrange(2) for _ in range(N)] for _ in range(gen.randrange(1, 6))]
        T = gen.randrange(1, 5)
        epsilon = gen.choice([0.5, 1.0, 4.0])
        got = mwem(B, queries, T, epsilon, random.Random(trial))
        last = mwem(B, queries, T, epsilon, random.Random(trial), return_last=True)
        want, want_last = _oracle_mwem(B, queries, T, epsilon, random.Random(trial))
        # The two pick a query by the same uniform draw; a different pick can only come
        # from a rounding tie at a boundary of the inverse CDF.
        agree += all(math.isclose(a, b, rel_tol=1e-7, abs_tol=1e-9) for a, b in zip(got + last, want + want_last))
        assert math.isclose(sum(got), sum(B), rel_tol=1e-9)
    assert agree >= 498


def test_error_within_theorem_2_2() -> None:
    rng = random.Random(6)
    N = 16
    queries = [[1 if i <= x <= j else 0 for x in range(N)] for i in range(N) for j in range(i, N)]
    B = [rng.randrange(0, 4000) * (x % 3 == 0) for x in range(N)]
    n = sum(B)
    T, epsilon = 40, 1.0
    bound = 2 * n * math.sqrt(math.log(N) / T) + 10 * T * math.log(len(queries)) / epsilon
    start = max_error(B, [n / N] * N, queries)
    errs = [max_error(B, mwem(B, queries, T, epsilon, rng), queries) for _ in range(5)]
    assert all(e <= bound for e in errs)
    assert max(errs) < start / 2  # and it is a real gain over the uniform start


def test_noise_free_limit_converges() -> None:
    # With a huge epsilon, MWEM is plain multiplicative weights with exact
    # measurements, and the averaged error is at most 2n sqrt(ln N / T).
    rng = random.Random(7)
    N = 8
    queries = _all_subset_queries(N)
    B = [rng.randrange(0, 50) for _ in range(N)]
    n = sum(B)
    for T in (10, 40, 160):
        e = max_error(B, mwem(B, queries, T, 1e9, rng), queries)
        assert e <= 2 * n * math.sqrt(math.log(N) / T)


def test_laplace_tail_check_value() -> None:
    rng = random.Random(8)
    zs = [laplace_noise(2.0, rng) for _ in range(2000)]
    frac = sum(1 for z in zs if abs(z) > 2 * math.log(10)) / len(zs)
    assert abs(frac - 0.1) <= dpkit.hoeffding_margin(len(zs), 1e-6)


def test_bad_parameters() -> None:
    rng = random.Random(9)
    for args in [([1, 2], [[1, 0]], 0, 1.0), ([1, 2], [[1, 0]], 1, 0.0), ([0, 0], [[1, 0]], 1, 1.0), ([1], [], 1, 1.0)]:
        try:
            mwem(*args, rng)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError")
