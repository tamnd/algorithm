# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scuttlebutt-reconciliation/. The authors are listed in prov/75N9PB.jsonl.

import random

from scuttlebutt_reconciliation import (Aimd, Participant, exchange, invariant_holds, share_rates, simulate,
                                        stale_mappings)


def test_basic_exchange() -> None:
    p, q = Participant(0, 2), Participant(1, 2)
    p.update("a", "x", 1)
    q.update("b", "y", 2)
    assert exchange(p, q, 10, "scuttle-depth", random.Random(0)) == (1, 1)
    assert p.state == q.state and p.digest() == q.digest() == (1, 2)
    assert exchange(p, q, 10, "scuttle-depth", random.Random(0)) == (0, 0)


def test_mtu_bounds_messages_and_keeps_version_order() -> None:
    rng = random.Random(4)
    p, q = Participant(0, 3), Participant(1, 3)
    for v in range(1, 31):
        p.update(f"k{v % 7}", f"v{v}", v)
    for ordering in ("scuttle-depth", "scuttle-breadth"):
        sent = p.select(q.digest(), 4, ordering, rng)
        assert len(sent) == 4
        mine = sorted(n for _, _, _, n in sent)
        avail = sorted(d[3] for d in p.available(q.digest())[0])
        assert mine == avail[:4]  # a prefix in version order


def test_figure_1_style_example() -> None:
    # Equal maxima mean nothing is sent for r, even though p and q differ on r's keys.
    rng = random.Random(0)
    p, q, r = Participant(0, 3), Participant(1, 3), Participant(2, 3)
    r.update("a", "x", 1)
    r.update("b", "y", 2)
    exchange(p, r, 10, "scuttle-depth", rng)
    r.update("a", "x2", 3)
    r.update("b", "y2", 4)
    exchange(q, r, 1, "scuttle-depth", rng)
    exchange(p, r, 1, "scuttle-depth", rng)
    assert p.maxv[2] == q.maxv[2] == 3
    assert p.state[2]["b"] == ("y", 2) and "b" not in q.state[2]
    assert exchange(p, q, 10, "scuttle-depth", rng) == (0, 0)
    for x in (p, q):
        assert invariant_holds(r, x)


def test_invariant_holds_after_every_exchange() -> None:
    rng = random.Random(7)
    n = 6
    parts = [Participant(i, n) for i in range(n)]
    version = 0
    for step in range(300):
        version += 1
        parts[rng.randrange(n)].update(f"k{rng.randrange(4)}", f"v{version}", version)
        a, b = rng.sample(range(n), 2)
        exchange(parts[a], parts[b], rng.randrange(1, 4), rng.choice(("scuttle-depth", "scuttle-breadth")), rng)
        for p in parts:
            for q in parts:
                assert invariant_holds(p, q)
                if q.maxv[p.id] == p.maxv[p.id]:
                    assert q.state[p.id] == p.state[p.id]  # property (3)


def test_converges_after_updates_stop_with_bounded_messages() -> None:
    for ordering in ("scuttle-depth", "scuttle-breadth", "precise-oldest", "precise-newest"):
        stale, biggest = simulate(24, 6, random.Random(1), 8, ordering, 16, 20, 45)
        assert biggest <= 8
        assert stale[19] > 0 and stale[-1] == 0, ordering


def test_unbounded_messages_converge_in_logarithmic_time() -> None:
    stale, _ = simulate(32, 8, random.Random(1), 10**9, "scuttle-depth", 24, 30, 45)
    after = next(i for i in range(30, 45) if stale[i] == 0) - 29
    assert after <= 8


def test_stale_count() -> None:
    p, q = Participant(0, 2), Participant(1, 2)
    p.update("a", "x", 1)
    assert stale_mappings([p, q]) == 1


def test_share_rates_conserves_the_sum() -> None:
    rng = random.Random(3)
    for _ in range(200):
        rp, rq, tp, tq = (rng.uniform(0, 10) for _ in range(4))
        a, b = share_rates(rp, rq, tp, tq)
        assert abs(a + b - tp - tq) < 1e-9
        if rp + rq <= tp + tq:
            assert a >= rp - 1e-9 and b >= rq - 1e-9
    assert share_rates(1, 1, 2, 4) == (3, 3)
    assert share_rates(1, 3, 2, 4) == (2, 4)
    assert share_rates(5, 5, 2, 4) == (3, 3)
    assert share_rates(1, 9, 2, 4) == (1, 5)


def test_aimd() -> None:
    c = Aimd(tau=10, mtu=100)
    for _ in range(3):
        c.observe((150, 20))
    assert c.tau == 7.5
    for _ in range(6):
        c.observe((20, 20))
    assert abs(c.tau - 7.9) < 1e-9
    # A message that is exactly full ends both streaks.
    for sizes in ((150, 0), (150, 0), (100, 0), (150, 0), (150, 0)):
        c.observe(sizes)
    assert abs(c.tau - 7.9) < 1e-9
