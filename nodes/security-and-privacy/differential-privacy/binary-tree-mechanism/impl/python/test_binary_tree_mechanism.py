# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/binary-tree-mechanism/. The authors are listed in prov/6G5Z3M.jsonl.

import itertools
import math
import random

import dpkit
from binary_tree_mechanism import (
    binary_tree_counter,
    binary_tree_counter_with_noise,
    error_variance,
    laplace_noise,
    levels,
    node_interval,
    node_vector,
)


def _prefix(stream):
    return list(itertools.accumulate(stream))


def test_levels_and_intervals() -> None:
    assert [levels(T) for T in (1, 2, 3, 4, 7, 8, 9)] == [1, 2, 2, 3, 3, 4, 4]
    assert [node_interval(t) for t in range(1, 9)] == [(1, 1), (1, 2), (3, 3), (1, 4), (5, 5), (5, 6), (7, 7), (1, 8)]


def test_zero_noise_gives_exact_prefix_sums_on_random_streams() -> None:
    rng = random.Random(1)
    for _ in range(600):
        T = rng.randrange(1, 40)
        stream = [rng.randrange(2) for _ in range(T)]
        outputs, nodes = binary_tree_counter_with_noise(stream, lambda t: 0.0)
        assert outputs == [float(c) for c in _prefix(stream)]
        assert nodes == [float(v) for v in node_vector(stream)]


def test_each_release_sums_popcount_nodes() -> None:
    # Tag the noise of node t with 1000^... style weights: give node t the noise 2^t.
    stream = [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1]
    outputs, _ = binary_tree_counter_with_noise(stream, lambda t: float(2 ** t))
    for t, (o, c) in enumerate(zip(outputs, _prefix(stream)), start=1):
        used = round(o - c)
        nodes_used = [u for u in range(1, t + 1) if (used >> u) & 1]
        # The nodes used at time t are the nodes closed at the prefixes of t's binary form.
        want, rest = [], t
        while rest:
            want.append(rest)
            rest -= rest & -rest
        assert sorted(nodes_used) == sorted(want)
        assert len(nodes_used) == bin(t).count("1") <= levels(len(stream))


def test_node_sensitivity_is_at_most_L_and_reached() -> None:
    for T in range(1, 9):
        L = levels(T)
        worst = 0
        for stream in itertools.product((0, 1), repeat=T):
            base = node_vector(stream)
            for s in range(T):
                other = list(stream)
                other[s] = 1 - other[s]
                d = sum(abs(p - q) for p, q in zip(base, node_vector(other)))
                worst = max(worst, d)
        assert worst <= L
        if T in (1, 2, 4, 8):
            assert worst == L  # time 1 lies in L nodes when T is a power of two


def _logpdf_nodes(point, centers, b):
    return sum(-abs(z - c) / b - math.log(2 * b) for z, c in zip(point, centers))


def test_log_density_ratio_of_noisy_nodes_is_at_most_epsilon() -> None:
    rng = random.Random(2)
    T, epsilon = 8, 0.7
    b = levels(T) / epsilon
    for _ in range(40):
        stream = [rng.randrange(2) for _ in range(T)]
        s = rng.randrange(T)
        other = list(stream)
        other[s] = 1 - other[s]
        cx, cy = node_vector(stream), node_vector(other)
        base = [rng.uniform(-20, 20) for _ in range(T)]
        direction = [rng.uniform(-1, 1) for _ in range(T)]

        def fx(z):
            return _logpdf_nodes([p + z * d for p, d in zip(base, direction)], cx, b)

        def fy(z):
            return _logpdf_nodes([p + z * d for p, d in zip(base, direction)], cy, b)

        grid = [k / 4 for k in range(-400, 401)]
        assert dpkit.log_ratio_grid(fx, fy, grid) <= epsilon + 1e-9
    # Tightness: at time 1 with T = 8 the change hits all 4 nodes over (1, 1), (1, 2), (1, 4), (1, 8).
    x = [0] * T
    y = [1] + [0] * (T - 1)
    cx, cy = node_vector(x), node_vector(y)
    far = [-100.0] * T  # far left of both centers, every coordinate moves the ratio the same way
    assert math.isclose(_logpdf_nodes(far, cx, b) - _logpdf_nodes(far, cy, b), epsilon)


def test_mean_square_error_matches_formula() -> None:
    rng = random.Random(3)
    T, epsilon, runs = 8, 1.0, 2000
    stream = [1, 0, 1, 1, 0, 1, 1, 1]
    true = _prefix(stream)
    sq = [0.0] * T
    for _ in range(runs):
        out = binary_tree_counter(stream, epsilon, rng)
        for t in range(T):
            sq[t] += (out[t] - true[t]) ** 2
    for t in range(1, T + 1):
        want = error_variance(t, T, epsilon)
        assert abs(sq[t - 1] / runs - want) <= 0.25 * want  # about 5 standard errors


def test_error_tail_within_chebyshev_bound() -> None:
    rng = random.Random(4)
    T, epsilon, runs, beta = 32, 1.0, 1000, 0.1
    stream = [rng.randrange(2) for _ in range(T)]
    true = _prefix(stream)
    bad = 0
    for _ in range(runs):
        out = binary_tree_counter(stream, epsilon, rng)
        t = T - 1  # popcount(31) = 5 nodes, the worst time for T = 32
        bad += abs(out[t - 1] - true[t - 1]) > math.sqrt(error_variance(t, T, epsilon) / beta)
    assert bad / runs <= beta + dpkit.hoeffding_margin(runs, 1e-6)


def test_laplace_tail_check_value() -> None:
    rng = random.Random(5)
    zs = [laplace_noise(2.0, rng) for _ in range(2000)]
    frac = sum(1 for z in zs if abs(z) > 2 * math.log(10)) / len(zs)
    assert abs(frac - 0.1) <= dpkit.hoeffding_margin(len(zs), 1e-6)


def test_edges() -> None:
    rng = random.Random(6)
    assert binary_tree_counter([], 1.0, rng) == []
    assert len(binary_tree_counter([1], 1.0, rng)) == 1
    try:
        binary_tree_counter([1], 0.0, rng)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
