# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/trapdoor-sampling-lattices/. The authors are listed in prov/M0ZP5R.jsonl.
# There are no standard test vectors for lattice trapdoors. These tests
# check the defining equations on toy parameters with fixed seeds.

import math
import random

from trapdoor_sampling_lattices import GadgetTrapdoor


def make(seed=1):
    return GadgetTrapdoor(n=2, k=8, mbar=16, rng=random.Random(seed))


def test_a_times_trapdoor_is_gadget():
    td = make()
    g = td.gadget()
    for j in range(td.w):
        col = [row[j] for row in td.t]
        assert td.mul_a(col) == [g[i][j] % td.q for i in range(td.n)]


def test_gadget_inverse_is_binary_preimage():
    td = make()
    rng = random.Random(2)
    g = td.gadget()
    for _ in range(50):
        u = [rng.randrange(td.q) for _ in range(td.n)]
        x = td.gadget_inverse(u)
        assert set(x) <= {0, 1}
        assert [sum(a * b for a, b in zip(row, x)) % td.q for row in g] == u


def test_sample_g_hits_target():
    td = make()
    rng = random.Random(3)
    g = td.gadget()
    for _ in range(50):
        u = [rng.randrange(td.q) for _ in range(td.n)]
        x = td.sample_g(u, rng)
        assert [sum(a * b for a, b in zip(row, x)) % td.q for row in g] == u
        assert max(abs(v) for v in x) < 6 * td.s_g


def test_preimage_is_correct_and_short():
    td = make()
    rng = random.Random(4)
    bound = td.s * math.sqrt(td.m)  # tail bound for D_{Z^m, s}
    for _ in range(100):
        u = [rng.randrange(td.q) for _ in range(td.n)]
        x = td.sample_pre(u, rng)
        assert td.mul_a(x) == u
        assert math.sqrt(sum(v * v for v in x)) <= bound
    # a random solution of A x = u mod q is not short: about q/sqrt(12) per entry
    assert bound < td.q / math.sqrt(12) * math.sqrt(td.m)


def _cross_covariance_correlation(td, sampler, rng, count):
    """Correlate the top-bottom cross covariance of the samples with R."""
    acc = [[0.0] * td.w for _ in range(td.mbar)]
    for _ in range(count):
        u = [rng.randrange(td.q) for _ in range(td.n)]
        x = sampler(u, rng)
        top, bottom = x[: td.mbar], x[td.mbar :]
        for i in range(td.mbar):
            ti = top[i]
            row = acc[i]
            for j in range(td.w):
                row[j] += ti * bottom[j]
    est = [v / count for row in acc for v in row]
    ref = [v for row in td.r for v in row]
    me, mr = sum(est) / len(est), sum(ref) / len(ref)
    cov = sum((a - me) * (b - mr) for a, b in zip(est, ref))
    return cov / math.sqrt(sum((a - me) ** 2 for a in est) * sum((b - mr) ** 2 for b in ref))


def test_perturbation_hides_the_trapdoor():
    td = make(5)
    leak = _cross_covariance_correlation(td, td.sample_pre_no_perturbation, random.Random(6), 1200)
    hidden = _cross_covariance_correlation(td, td.sample_pre, random.Random(7), 1200)
    # without the perturbation, E[x_top x_bottom^T] = (s_g^2 / 2 pi) R, so R leaks
    assert leak > 0.9
    # with it, the output is spherical and the estimate is noise
    assert abs(hidden) < 0.3
