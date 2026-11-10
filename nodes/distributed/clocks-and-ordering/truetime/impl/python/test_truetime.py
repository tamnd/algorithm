# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/truetime/. The authors are listed in prov/SPFG5M.jsonl.

import random

from truetime import Txn, execute, fixed_server, sine_server, violations

EPS = 0.007  # 7 ms, the top of the sawtooth reported for Spanner


def test_interval_holds_real_time() -> None:
    rng = random.Random(0)
    for _ in range(50):
        srv = sine_server(rng, EPS)
        for _ in range(50):
            t = rng.uniform(0, 1000)
            lo, hi = srv.now(t)
            assert lo <= t <= hi and abs((hi - lo) - 2 * EPS) < 1e-12


def test_page_example_without_commit_wait() -> None:
    # Leader A runs eps fast, leader B runs eps slow.
    servers = [fixed_server(EPS, +EPS), fixed_server(EPS, -EPS)]
    t1 = Txn("T1", start=0.000, leader=0)
    t2 = Txn("T2", start=0.003, leader=1)
    execute([t1, t2], servers, delay=0.0, work=0.001, commit_wait=False)
    assert abs(t1.s - 0.014) < 1e-12 and abs(t1.commit - 0.001) < 1e-12
    assert abs(t2.s - 0.003) < 1e-12
    assert violations([t1, t2]) == [("T1", "T2")]


def test_page_example_with_commit_wait() -> None:
    servers = [fixed_server(EPS, +EPS), fixed_server(EPS, -EPS)]
    t1 = Txn("T1", start=0.000, leader=0)
    execute([t1], servers, delay=0.0, work=0.001, commit_wait=True)
    # A's earliest is t, so T1 becomes visible just after t = 0.014.
    assert abs(t1.commit - 0.014) < 1e-9
    t2 = Txn("T2", start=t1.commit + 0.001, leader=1)
    execute([t2], servers, delay=0.0, work=0.001, commit_wait=True)
    assert t2.s > t1.s
    assert violations([t1, t2]) == []


def test_commit_wait_gives_external_consistency() -> None:
    for seed in range(40):
        rng = random.Random(seed)
        servers = [sine_server(rng, EPS) for _ in range(4)]
        txns = [Txn(f"T{i}", start=rng.uniform(0, 0.2), leader=rng.randrange(4)) for i in range(40)]
        execute(txns, servers, delay=rng.uniform(0, 0.002), work=0.0005, commit_wait=True)
        assert violations(txns) == []
        for tx in txns:
            assert tx.commit - tx.start <= 0.002 + 0.0005 + 4 * EPS + 1e-9


def test_skipping_commit_wait_breaks_it_on_seeded_runs() -> None:
    broken = 0
    for seed in range(40):
        rng = random.Random(seed)
        servers = [sine_server(rng, EPS) for _ in range(4)]
        txns = [Txn(f"T{i}", start=rng.uniform(0, 0.2), leader=rng.randrange(4)) for i in range(40)]
        execute(txns, servers, delay=0.0005, work=0.0005, commit_wait=False)
        broken += bool(violations(txns))
    assert broken > 0
