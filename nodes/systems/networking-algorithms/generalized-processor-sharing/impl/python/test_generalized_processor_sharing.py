# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-processor-sharing/. The authors are listed in prov/REWV62.jsonl.

import random
from fractions import Fraction

from generalized_processor_sharing import gps, virtual_finish_tags


def test_hand_example() -> None:
    # Weights 1 and 3 on a link of rate 1. A sends 4 bits, B sends 6, both
    # at time 0. B gets 3/4 of the link and finishes at 8; A then has 2 bits
    # left and finishes at 10.
    arrivals = [(0, "A", 4), (0, "B", 6)]
    out = gps(arrivals, {"A": 1, "B": 3}, 1)
    assert out[1][0] == 8 and out[0][0] == 10
    assert out[1][2] == 2 and out[0][2] == 4  # V(8) = 2, V(10) = 4


def random_trace(rng: random.Random, flows: list, n: int):
    t, out = 0, []
    for _ in range(n):
        t += rng.choice([0, 0, 1, 2, 5, 20])
        out.append((t, rng.choice(flows), rng.randint(1, 12)))
    return out


def test_finish_times_match_the_virtual_tags() -> None:
    # Parekh and Gallager: a packet finishes under GPS exactly when V(t)
    # reaches its tag F = max(F_prev, V(a)) + L / phi.
    for seed in range(40):
        rng = random.Random(seed)
        flows = list(range(rng.randint(1, 5)))
        phi = {f: rng.randint(1, 4) for f in flows}
        arrivals = random_trace(rng, flows, 50)
        out = gps(arrivals, phi, rng.choice([1, 2, 3]))
        tags = virtual_finish_tags(arrivals, phi, {p: out[p][1] for p in out})
        assert len(out) == len(arrivals)
        for p in out:
            assert out[p][2] == tags[p]


def test_work_conserving() -> None:
    # The last finish time equals that of FIFO on the same arrivals.
    for seed in range(20):
        rng = random.Random(100 + seed)
        flows = list(range(4))
        phi = {f: rng.randint(1, 5) for f in flows}
        arrivals = random_trace(rng, flows, 60)
        rate = Fraction(rng.randint(1, 3))
        t = Fraction(0)
        for a, _, size in arrivals:
            t = max(t, Fraction(a)) + size / rate
        out = gps(arrivals, phi, rate)
        assert max(f for f, _, _ in out.values()) == t


def token_bucket_trace(rng: random.Random, sigma: int, rho: Fraction, n: int, flow):
    """Packets that conform to a token bucket of depth sigma and rate rho."""
    t = Fraction(0)
    tokens = Fraction(sigma)
    out = []
    for _ in range(n):
        gap = Fraction(rng.choice([0, 0, 0, 1, 3, 10, 40]))
        tokens = min(Fraction(sigma), tokens + rho * gap)
        t += gap
        size = rng.randint(1, sigma)
        if tokens < size:  # wait for enough tokens
            wait = (size - tokens) / rho
            t += wait
            tokens = Fraction(size)
        tokens -= size
        out.append((t, flow, size))
    return out


def test_leaky_bucket_delay_bound() -> None:
    # If flow i conforms to (sigma_i, rho_i) and rho_i <= g_i, the guaranteed
    # rate phi_i r / sum phi, then every packet of flow i leaves within
    # sigma_i / g_i of its arrival, whatever the other flows send.
    for seed in range(10):
        rng = random.Random(500 + seed)
        phi = {"a": 1, "b": 2, "x": 1}
        rate = Fraction(4)
        g = {f: phi[f] * rate / 4 for f in phi}
        sigma = {"a": 8, "b": 15}
        arrivals = token_bucket_trace(rng, 8, g["a"], 80, "a")
        arrivals += token_bucket_trace(rng, 15, g["b"], 80, "b")
        # flow x is greedy: a large burst at time 0 and more later
        arrivals += [(Fraction(k * 5), "x", 30) for k in range(40)]
        arrivals.sort(key=lambda e: e[0])
        out = gps(arrivals, phi, rate)
        for p, (a, f, _) in enumerate(arrivals):
            if f in sigma:
                assert out[p][0] - a <= sigma[f] / g[f]
