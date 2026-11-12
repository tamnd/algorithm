# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/store-and-forward/. The authors are listed in prov/TC3XFV.jsonl.

import math
import random

from store_and_forward import (Link, best_payload, message_time, path,
                               simulate)


def close(a, b):
    return abs(a - b) <= 1e-9 * max(1.0, abs(a), abs(b))


def test_one_packet_pays_the_full_transmission_time_at_every_hop():
    for h in range(1, 8):
        links, route = path(h, rate=1000.0, prop=0.003)
        [t] = simulate(links, [(0.0, 1500 * 8, route)])
        assert close(t, h * (1500 * 8 / 1000.0 + 0.003))


def test_n_packets_take_h_plus_n_minus_one_slots():
    for h in range(1, 7):
        for n in range(1, 9):
            L, R, d = 1000.0, 250.0, 0.5
            links, route = path(h, R, d)
            done = simulate(links, [(0.0, L, route)] * n)
            for i, t in enumerate(done):
                assert close(t, (h + i) * L / R + h * d)
            assert close(done[-1], (h + n - 1) * L / R + h * d)


def test_bottleneck_link_sets_the_pace():
    rng = random.Random(1)
    for _ in range(30):
        h, n = rng.randint(1, 6), rng.randint(1, 8)
        rates = [rng.choice([1.0, 2.0, 5.0, 10.0]) for _ in range(h)]
        links = {i: Link(r) for i, r in enumerate(rates)}
        L = 10.0
        done = simulate(links, [(0.0, L, list(range(h)))] * n)
        s = [L / r for r in rates]
        assert close(done[-1], sum(s) + (n - 1) * max(s))


def test_splitting_a_message_and_the_best_packet_size():
    M, H, R = 12000, 40, 1.0
    for h in (2, 3, 5, 9):
        sizes = [p for p in range(1, M + 1) if M % p == 0]
        for p in sizes[:: max(1, len(sizes) // 8)]:
            links, route = path(h, R)
            done = simulate(links, [(0.0, p + H, route)] * (M // p))
            assert close(done[-1], message_time(M, p, H, h, R))
        best = min(sizes, key=lambda p: message_time(M, p, H, h, R))
        pstar = best_payload(M, H, h)
        # the best divisor is next to the real optimum
        below = max([p for p in sizes if p <= pstar], default=sizes[0])
        above = min([p for p in sizes if p >= pstar], default=sizes[-1])
        assert best in (below, above)
        # one big packet is worse than the best split when h > 1
        assert message_time(M, M, H, h, R) > message_time(M, best, H, h, R)


def test_queueing_matches_the_lindley_recursion():
    # one link, random arrivals and sizes: waiting time W(k+1) = max(0, W(k) + S(k) - gap)
    rng = random.Random(7)
    links = {"a": Link(2.0, 0.25), "b": Link(4.0, 0.0)}
    pk, t = [], 0.0
    for _ in range(300):
        t += rng.expovariate(1.0)
        pk.append((t, rng.uniform(0.5, 3.0), ["a", "b"]))
    done = simulate(links, pk)
    # replay both FIFO links by hand
    free_a = free_b = 0.0
    for (t0, size, _), got in zip(pk, done):
        start_a = max(t0, free_a)
        free_a = start_a + size / 2.0
        at_b = free_a + 0.25
        start_b = max(at_b, free_b)
        free_b = start_b + size / 4.0
        assert close(got, free_b)


def test_cross_traffic_shares_a_link_in_fifo_order():
    links = {"x": Link(1.0), "y": Link(1.0), "z": Link(1.0)}
    pk = [(0.0, 2.0, ["x", "z"]), (0.0, 3.0, ["y", "z"]), (1.0, 1.0, ["z"])]
    done = simulate(links, pk)
    # packet 2 reaches z first (t=1), then packet 0 (t=2), then packet 1 (t=3)
    assert done == [4.0, 7.0, 2.0]
    assert math.isclose(best_payload(100, 4, 2), 20.0)
