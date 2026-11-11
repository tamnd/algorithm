# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/collision-finding/. The authors are listed in prov/45XBR0.jsonl.

import random

from collision_finding import dp_search, rho_search, table_search, truncated_sha256

N = 24


def check(f, x1: int, x2: int) -> None:
    assert x1 != x2
    assert f(x1) == f(x2)


def test_three_methods_find_real_collisions() -> None:
    f = truncated_sha256(N, b"cf")
    x1, x2, calls_t, stored_t = table_search(f, N, random.Random(1))
    check(f, x1, x2)
    r = None
    x0 = 0
    while r is None:
        r = rho_search(f, x0)
        x0 += 1
    check(f, r[0], r[1])
    calls_r, stored_r = r[2], r[3]
    y1, y2, calls_d, stored_d = dp_search(f, N, 6, random.Random(2))
    check(f, y1, y2)
    # memory: table holds every value, rho holds two, distinguished points hold about 2^(n/2 - d)
    assert stored_t > 500
    assert stored_r == 2
    assert stored_d < stored_t // 8


def test_average_costs_show_the_trade_off() -> None:
    rows = {"table": [0, 0], "rho": [0, 0], "dp": [0, 0]}
    trials = 6
    for s in range(trials):
        f = truncated_sha256(20, bytes([s]))
        _, _, c, m = table_search(f, 20, random.Random(s))
        rows["table"][0] += c
        rows["table"][1] += m
        r, x0 = None, s << 10
        while r is None:
            r = rho_search(f, x0)
            x0 += 1
        rows["rho"][0] += r[2]
        rows["rho"][1] += r[3]
        _, _, c, m = dp_search(f, 20, 5, random.Random(100 + s))
        rows["dp"][0] += c
        rows["dp"][1] += m
    avg = {k: (v[0] / trials, v[1] / trials) for k, v in rows.items()}
    # 2^10 = 1024; table about 1.25 * 1024 calls; rho about 3 times as many; dp in between
    assert 400 < avg["table"][0] < 3000
    assert avg["rho"][0] > avg["table"][0]
    assert avg["rho"][1] == 2
    assert avg["dp"][1] < avg["table"][1] / 4


def test_rho_start_on_cycle_returns_none() -> None:
    f = lambda x: (x + 1) % 7  # a single cycle, no collision exists
    assert rho_search(f, 3) is None
