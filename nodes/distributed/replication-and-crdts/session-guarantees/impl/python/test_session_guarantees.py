# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/session-guarantees/. The authors are listed in prov/HVCFWA.jsonl.

import random

import pytest

from session_guarantees import ALL, MR, MW, RYW, WFR, Monitor, Server, Session, Unavailable

NONE: frozenset = frozenset()


def setup(m: int, g: frozenset) -> tuple[list[Server], Monitor, Session]:
    servers = [Server(i, m) for i in range(m)]
    mon = Monitor(servers)
    return servers, mon, Session(0, m, mon, g)


def scenario_ryw(g: frozenset) -> Monitor:
    s, mon, c = setup(2, g)
    c.write(s[0], "x", 1)
    c.read(s[1], "x")  # server 1 has not received the write
    return mon


def scenario_mr(g: frozenset) -> Monitor:
    s, mon, c = setup(2, g)
    other = Session(1, 2, mon, NONE)
    other.write(s[0], "x", 1)
    c.read(s[0], "x")  # sees 1
    c.read(s[1], "x")  # server 1 has nothing
    return mon


def scenario_wfr(g: frozenset) -> Monitor:
    s, mon, c = setup(3, g)
    other = Session(1, 3, mon, NONE)
    other.write(s[0], "x", 1)
    c.read(s[0], "x")  # a reply that depends on x = 1
    c.write(s[1], "y", 2)  # server 1 has not seen x = 1
    s[2].receive(s[1].snapshot())  # server 2 gets the reply without its cause
    mon.check_servers()
    return mon


def scenario_mw(g: frozenset) -> Monitor:
    s, mon, c = setup(3, g)
    c.write(s[0], "x", 1)
    c.write(s[1], "x", 2)
    s[2].receive(s[1].snapshot())  # server 2 has the second write only
    mon.check_servers()
    return mon


SCENARIOS = {RYW: scenario_ryw, MR: scenario_mr, WFR: scenario_wfr, MW: scenario_mw}


@pytest.mark.parametrize("g", [RYW, MR, WFR, MW])
def test_each_guarantee_fails_without_vectors(g: str) -> None:
    assert g in SCENARIOS[g](NONE).kinds()


@pytest.mark.parametrize("g", [RYW, MR, WFR, MW])
def test_each_guarantee_refuses_the_stale_server(g: str) -> None:
    with pytest.raises(Unavailable):
        SCENARIOS[g](frozenset({g}))


def test_ryw_and_mr_are_independent() -> None:
    # read your writes alone does not prevent the monotonic reads violation
    assert MR in scenario_mr(frozenset({RYW})).kinds()
    # monotonic reads alone does not prevent the read your writes violation
    assert RYW in scenario_ryw(frozenset({MR})).kinds()


def test_wfr_order_part() -> None:
    # The new write must be ordered after the write that was read. Here
    # server 1 has a lower Lamport counter, so without the check the reply
    # gets a smaller stamp than its cause, even once both are everywhere.
    s, mon, c = setup(2, NONE)
    other = Session(1, 2, mon, NONE)
    for v in range(3):
        other.write(s[0], "x", v)
    c.read(s[0], "x")
    w = c.write(s[1], "y", 9)
    s[1].receive(s[0].snapshot())
    mon.check_servers()
    assert w.stamp < s[0].lookup("x").stamp
    assert WFR in mon.kinds()


def run(rng: random.Random, g: frozenset) -> Monitor:
    m = rng.randint(2, 4)
    servers = [Server(i, m) for i in range(m)]
    mon = Monitor(servers)
    sessions = [Session(c, m, mon, g) for c in range(rng.randint(1, 3))]
    net: list[tuple[int, dict]] = []
    val = 0
    for _ in range(rng.randint(5, 30)):
        a = rng.random()
        if a < 0.45:
            c = rng.choice(sessions)
            order = rng.sample(servers, m)
            for s in order:  # try servers until one can serve the operation
                try:
                    if rng.random() < 0.5:
                        val += 1
                        c.write(s, rng.choice("xy"), val)
                    else:
                        c.read(s, rng.choice("xy"))
                    break
                except Unavailable:
                    continue
        elif a < 0.75:
            src, dst = rng.randrange(m), rng.randrange(m)
            net.append((dst, servers[src].snapshot()))
        elif net:
            k = rng.randrange(len(net))  # reordering
            dst, snap = net[k]
            if rng.random() < 0.7:
                net.pop(k)  # otherwise it stays and can be delivered again
            if rng.random() < 0.85:  # some deliveries are lost
                servers[dst].receive(snap)
        mon.check_servers()
    return mon


def test_no_violations_with_vectors() -> None:
    rng = random.Random(1994)
    for _ in range(600):
        assert run(rng, ALL).violations == []


def test_violations_appear_without_vectors() -> None:
    rng = random.Random(1994)
    seen: set[str] = set()
    for _ in range(600):
        seen |= run(rng, NONE).kinds()
    assert seen == {RYW, MR, WFR, MW}


def test_each_check_alone_prevents_its_own_violation() -> None:
    rng = random.Random(7)
    for g in (RYW, MR, WFR, MW):
        for _ in range(150):
            assert g not in run(rng, frozenset({g})).kinds()
