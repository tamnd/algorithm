# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/random-boolean-network/. The authors are listed in prov/JT779F.jsonl.

import math
import random
from fractions import Fraction

from random_boolean_network import (
    attractors,
    attractors_by_image,
    hamming_spread,
    random_network,
    step,
    successor_table,
)


def bits(state, n):
    return [(state >> i) & 1 for i in range(n)]


def harmonic(k, power=1):
    return sum((Fraction(1, i ** power) for i in range(1, k + 1)), Fraction(0))


def random_map_cycle_moments(size):
    """Exact mean and variance of the number of cycles of a uniform random map on size points.

    P(k cyclic points) = (k / size) prod_{i < k} (1 - i / size); given k cyclic points, the
    cycles are those of a uniform permutation of k points, with mean H_k and variance H_k - H_k^(2).
    """
    mean = Fraction(0)
    second = Fraction(0)
    prod = Fraction(1)
    for k in range(1, size + 1):
        pk = Fraction(k, size) * prod
        prod *= 1 - Fraction(k, size)
        h1, h2 = harmonic(k), harmonic(k, 2)
        mean += pk * h1
        second += pk * (h1 - h2 + h1 * h1)
    return mean, second - mean * mean


def test_step_reads_the_old_state():
    rng = random.Random(1)
    for _ in range(50):
        n = rng.randint(1, 7)
        net = random_network(rng, n, rng.randint(0, n), rng.random())
        s = rng.randrange(1 << n)
        x = bits(s, n)
        want = [table[sum(x[g] << r for r, g in enumerate(inputs))] for inputs, table in net]
        assert bits(step(net, s), n) == want


def test_worked_example_of_the_page():
    # A' = B, B' = A, C' = A and B; gene i is bit i of the state
    net = [((1,), [0, 1]), ((0,), [0, 1]), ((0, 1), [0, 0, 0, 1])]
    cycles, basin, label = attractors(successor_table(net))
    assert cycles == [[0], [1, 2], [7]]
    assert label[4] == 0 and label[5] == label[6] == 1 and label[3] == 2
    got = sorted((tuple(c), b) for c, b in zip(cycles, basin))
    assert got == [((0,), 2), ((1, 2), 4), ((7,), 2)]


def test_attractors_match_a_second_method_up_to_n_12():
    rng = random.Random(2)
    cases = [(n, k) for n in range(1, 9) for k in range(0, min(n, 4) + 1)] + [(10, 2), (11, 3), (12, 2), (12, 1)]
    for n, k in cases:
        for p in (0.5, 0.2):
            net = random_network(rng, n, k, p)
            succ = successor_table(net)
            cycles, basin, label = attractors(succ)
            cycles2, basin2 = attractors_by_image(succ)
            assert sorted(cycles) == cycles2
            assert {c[0]: b for c, b in zip(cycles, basin)} == basin2
            assert sum(basin) == 1 << n
            cyclic = {u: a for a, c in enumerate(cycles) for u in c}
            for s in range(1 << n):
                # label[s] is the attractor that s reaches
                t = s
                while t not in cyclic:
                    t = succ[t]
                assert cyclic[t] == label[s]


def test_exact_random_map_moments_small_cases():
    # by enumeration of all maps on 3 points: 27 maps
    import itertools

    size = 3
    counts = []
    for f in itertools.product(range(size), repeat=size):
        cycles, _, _ = attractors(list(f))
        counts.append(len(cycles))
    mean = Fraction(sum(counts), len(counts))
    var = Fraction(sum(c * c for c in counts), len(counts)) - mean * mean
    assert (mean, var) == random_map_cycle_moments(size)


def test_k_equal_n_is_a_uniform_random_map():
    # measured mean number of attractors against the exact mean, 2000 networks with n = K = 4
    rng = random.Random(3)
    n, reps = 4, 2000
    mean, var = random_map_cycle_moments(1 << n)
    total = 0
    for _ in range(reps):
        cycles, _, _ = attractors(successor_table(random_network(rng, n, n, 0.5)))
        total += len(cycles)
    z = (total / reps - float(mean)) / math.sqrt(float(var) / reps)
    assert abs(z) < 4


def test_expected_number_of_fixed_points_is_one():
    rng = random.Random(4)
    reps = 1000
    for n, k, p in ((5, 2, 0.3), (4, 4, 0.5)):
        xs = []
        for _ in range(reps):
            succ = successor_table(random_network(rng, n, k, p))
            xs.append(sum(1 for s, t in enumerate(succ) if s == t))
        m = sum(xs) / reps
        sd = math.sqrt(sum((x - m) ** 2 for x in xs) / (reps - 1))
        assert abs(m - 1.0) < 4 * sd / math.sqrt(reps)


def test_one_step_spread_is_2p_1_minus_p_k():
    rng = random.Random(5)
    reps = 3000
    for n, k, p in ((10, 2, 0.5), (8, 3, 0.2)):
        xs = []
        for _ in range(reps):
            net = random_network(rng, n, k, p)
            xs.append(hamming_spread(net, rng.randrange(1 << n), rng.randrange(n)))
        m = sum(xs) / reps
        sd = math.sqrt(sum((x - m) ** 2 for x in xs) / (reps - 1))
        assert abs(m - 2 * p * (1 - p) * k) < 4 * sd / math.sqrt(reps)
