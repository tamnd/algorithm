# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kernel-launch-overhead/. The authors are listed in prov/EGK2KC.jsonl.
import random
from fractions import Fraction as F

from kernel_launch_overhead import (
    async_schedule, efficiency, graph_break_even, min_useful_elements, overhead_per_kernel,
    sequence_time, steady_per_kernel,
)

TAU = F(29, 10)   # Gray 2019: a 2.9 us kernel on a V100


def test_gray_measurements():
    per_kernel = {"sync each": F(96, 10), "sync per step": F(38, 10), "graph": F(34, 10)}
    o = {k: overhead_per_kernel(v, TAU) for k, v in per_kernel.items()}
    assert o == {"sync each": F(67, 10), "sync per step": F(9, 10), "graph": F(5, 10)}
    assert efficiency(TAU, o["sync each"]) == F(29, 96)
    assert efficiency(TAU, o["sync per step"]) == F(29, 38)
    assert efficiency(TAU, o["graph"]) == F(29, 34)
    # one step of 20 kernels
    assert sequence_time(20, TAU, o["sync each"]) == 192
    assert sequence_time(20, TAU, o["sync per step"]) == 76
    assert sequence_time(20, TAU, o["graph"]) == 68


def test_graph_break_even():
    # assumed: instantiation costs 100 us; the graph saves 0.4 us on each of 20 kernels
    n, q = graph_break_even(100, 20, F(4, 10))
    assert q == F(25, 2) and n == 13
    assert 13 * 20 * F(4, 10) >= 100 > 12 * 20 * F(4, 10)


def test_async_schedule_steady_state():
    rng = random.Random(7)
    for _ in range(200):
        tau = F(rng.randrange(1, 50), 10)
        c = F(rng.randrange(1, 80), 10)
        g = F(rng.randrange(0, 20), 10)
        k = rng.randrange(2, 40)
        starts, ends = async_schedule(k, tau, c, g)
        assert all(e - s == tau for s, e in zip(starts, ends))
        assert all(starts[i + 1] >= ends[i] + g for i in range(k - 1))
        assert ends[-1] - ends[-2] <= steady_per_kernel(tau, c, g)
        assert ends[-1] == tau + (k - 1) * steady_per_kernel(tau, c, g)


def test_tiny_kernels_are_host_bound():
    # assumed: the host needs 5 us per launch, the device gap is 1 us
    _, ends = async_schedule(100, F(1, 2), 5, 1)
    assert ends[-1] == F(1, 2) + 99 * 5
    assert efficiency(F(1, 2), F(9, 2)) == F(1, 10)
    _, ends = async_schedule(100, 20, 5, 1)
    assert ends[-1] == 20 + 99 * 21


def test_min_useful_size():
    # assumed: o = 3 us, a vector add moves 12 bytes per element, 1000 GB/s = 10**6 bytes per us
    assert min_useful_elements(3, 12, 10 ** 6) == 250000
