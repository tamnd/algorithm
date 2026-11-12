# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bcjr-algorithm/. The authors are listed in prov/PCHCXC.jsonl.

import itertools
import math
import random

from bcjr_algorithm import bcjr, build_trellis, max_star


def all_paths(trellis, terminated=True):
    """Every path of the trellis as (inputs, code bits), by brute force."""
    paths = [((), (), 0)]
    for step in trellis:
        nxt = []
        for us, cs, s in paths:
            for (a, u, b, out) in step:
                if a == s:
                    nxt.append((us + (u,), cs + out, b))
        paths = nxt
    return [(us, cs) for us, cs, s in paths if s == 0 or not terminated]


def metric(us, cs, lc, la):
    return 0.5 * (sum((1 - 2 * u) * a for u, a in zip(us, la)) + sum((1 - 2 * c) * l for c, l in zip(cs, lc)))


def brute(trellis, lc, la, terminated=True):
    ps = [(us, metric(us, cs, lc, la)) for us, cs in all_paths(trellis, terminated)]
    top = max(m for _, m in ps)
    exact, maxlog = [], []
    for t in range(len(trellis)):
        p0 = math.fsum(math.exp(m - top) for us, m in ps if us[t] == 0)
        p1 = math.fsum(math.exp(m - top) for us, m in ps if us[t] == 1)
        m0 = max((m for us, m in ps if us[t] == 0), default=-math.inf)
        m1 = max((m for us, m in ps if us[t] == 1), default=-math.inf)
        exact.append(math.log(p0 / p1) if p0 and p1 else None)
        maxlog.append(m0 - m1 if p0 and p1 else None)
    return exact, maxlog


def test_max_star() -> None:
    for a, b in [(0.0, 0.0), (1.5, -2.0), (-30.0, 4.0), (7.0, 7.0)]:
        assert abs(max_star(a, b) - math.log(math.exp(a) + math.exp(b))) < 1e-12
    assert max_star(float("-inf"), 2.0) == 2.0


def test_worked_example() -> None:
    # (7, 5) code, message 1 0 1 1, received BPSK values with sigma^2 = 1.
    y = [-0.8, -1.1, 0.3, 0.9, 1.2, -0.2, 0.7, -0.6, 1.0, -1.3, -0.6, -0.9]
    t = build_trellis([7, 5], 3, 4)
    lc = [2 * v for v in y]
    got = bcjr(t, lc)[:4]
    want, _ = brute(t, lc, [0.0] * len(t))
    for g, w in zip(got, want):
        assert abs(g - w) < 1e-9
    assert [round(v, 3) for v in got] == [-5.102, 5.426, -6.039, -6.632]
    assert [round(v, 3) for v in bcjr(t, lc, mode="maxlog")[:4]] == [-5.2, 6.2, -6.6, -7.6]
    assert [int(v < 0) for v in got] == [1, 0, 1, 1]


def test_bcjr_equals_brute_force_posteriors() -> None:
    rng = random.Random(12)
    cases = 0
    for trial in range(500):
        kind = trial % 3
        length = rng.randrange(1, 6)
        if kind == 0:
            t = build_trellis([7, 5], 3, length)
            term = True
        elif kind == 1:
            t = build_trellis([5], 3, length, fb=7)  # RSC (1, 5/7), terminated
            term = True
        else:
            t = build_trellis([int("15", 8)], 4, length, fb=int("13", 8), terminate=False)
            term = False
        n = len(t[0][0][3])
        lc = [rng.gauss(0.0, 3.0) for _ in range(n * len(t))]
        la = [rng.gauss(0.0, 1.0) for _ in range(len(t))]
        exact, maxlog = brute(t, lc, la, term)
        for mode, want in (("prob", exact), ("log", exact), ("maxlog", maxlog)):
            got = bcjr(t, lc, la, mode=mode, terminated=term)
            for g, w in zip(got, want):
                if w is not None:
                    assert abs(g - w) < 1e-9
                    cases += 1
    assert cases > 2000


def test_noiseless_and_signs() -> None:
    t = build_trellis([int("171", 8), int("133", 8)], 7, 8)
    msg = [1, 1, 0, 1, 0, 0, 1, 0]
    path = [()]
    s = 0
    for step, u in zip(t, msg + [0] * 6):
        e = next(e for e in step if e[0] == s and e[1] == u)
        path.append(e[3])
        s = e[2]
    lc = [4.0 * (1 - 2 * c) for out in path for c in out]
    for mode in ("prob", "log", "maxlog"):
        llr = bcjr(t, lc, mode=mode)[:8]
        assert [int(v < 0) for v in llr] == msg
