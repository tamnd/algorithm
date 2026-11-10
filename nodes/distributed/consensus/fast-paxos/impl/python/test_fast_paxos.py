# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-paxos/. The authors are listed in prov/YZ2GMJ.jsonl.

from fast_paxos import (ANY, FastPaxos, counting_condition, drain_rounds, pick,
                        requirement_holds, safe, smallest_fast_quorum)


def flush(sim: FastPaxos, pred) -> None:
    keep, todo = [], []
    for item in sim.net.queue:
        (todo if pred(*item) else keep).append(item)
    sim.net.queue = keep
    for dst, msg in todo:
        sim.deliver(dst, msg)


def test_brute_force_matches_counting_rule() -> None:
    for n in range(1, 7):
        for qc in range(1, n + 1):
            for qf in range(qc, n + 1):
                assert requirement_holds(n, qc, qf) == counting_condition(n, qc, qf), (n, qc, qf)


def test_fast_quorum_sizes() -> None:
    for n in range(1, 40):
        assert smallest_fast_quorum(n) == -(-3 * n // 4), n
    # Equal quorums: the largest e with n > 3e, so e = ceil(n / 3) - 1.
    for n in range(1, 40):
        e = max(e for e in range(n) if counting_condition(n, n - e, n - e))
        assert e == -(-n // 3) - 1, n
    assert [smallest_fast_quorum(n) for n in (3, 4, 5, 7)] == [3, 3, 4, 6]


def test_safe_random_runs() -> None:
    for seed in range(150):
        sim = FastPaxos(5, 3, 4, ["x", "y", "z"], seed, drop=0.1, dup=0.1, crash_prob=0.01,
                        max_acceptor_crashes=1, timeout_prob=0.05, stable_after=500)
        r = sim.run()
        assert safe(r, sim.values), seed
        assert len(r.learned) == 2, seed
    for seed in range(100):  # any number of crashes, no liveness check
        sim = FastPaxos(4, 3, 3, ["x", "y"], seed, drop=0.1, dup=0.1, crash_prob=0.01,
                        max_acceptor_crashes=4, timeout_prob=0.05, max_steps=1500)
        assert safe(sim.run(), sim.values), seed


def test_small_fast_quorum_breaks_safety() -> None:
    # n = 5 with qc = qf = 3 has qc + 2 qf = 9, not more than 10.
    assert not requirement_holds(5, 3, 3)
    bad = sum(not safe(FastPaxos(5, 3, 3, ["x", "y", "z"], s, timeout_prob=0.05,
                                 drop=0.1, dup=0.1, max_steps=1500).run(), ["x", "y", "z"])
              for s in range(150))
    assert bad > 0


def test_small_fast_quorum_explicit_run() -> None:
    # Fast round 0: A0, A1, A2 vote y (a fast quorum of 3), A3, A4 vote x.
    sim = FastPaxos(5, 3, 3, ["y", "x"], seed=0, k=1)
    for a in range(5):
        sim.acceptors[a].on_2a(sim.net, 0, ANY)
    for a, v in [(0, "y"), (1, "y"), (2, "y"), (3, "x"), (4, "x")]:
        sim.acceptors[a].on_proposal(sim.net, v)
    sim.net.queue = []
    # The coordinator of round 2 hears from A2, A3, A4. Both x and y pass O4,
    # and it picks x, which a quorum then chooses in round 2.
    reports = {2: (0, "y"), 3: (0, "x"), 4: (0, "x")}
    assert pick(reports, 3, 3, 5, 3, []) == "x"
    for a in (2, 3, 4):
        sim.acceptors[a].on_2a(sim.net, 3, "x")
    assert sim.result().chosen == {"x", "y"}
    # With qf = 4 the same reports allow only x, and y was never chosen.
    assert pick(reports, 3, 4, 5, 3, []) == "x"


def test_recovery_keeps_fast_choice() -> None:
    # n = 5, qf = 4: y is chosen in the fast round by A0..A3. Any classic
    # quorum then sees y on a majority of its members, and O4 picks y.
    for q in [(0, 1, 4), (2, 3, 4), (0, 3, 4), (1, 2, 3)]:
        reports = {a: (0, "x" if a == 4 else "y") for a in q}
        assert pick(reports, 3, 4, 5, 1, ["x"]) == "y", q


def prepare_fast_round(sim: FastPaxos) -> None:
    c = sim.coords[0]
    c.start(sim.net, -1)
    flush(sim, lambda d, m: m[0] == "1a")
    flush(sim, lambda d, m: m[0] == "1b")
    flush(sim, lambda d, m: m[0] == "2a")
    assert all(a.any_round == c.crnd for a in sim.acceptors)


def test_fast_round_takes_two_delays() -> None:
    sim = FastPaxos(5, 3, 4, ["x"], seed=0, k=1)
    prepare_fast_round(sim)
    for a in range(5):
        sim.net.send(("P", 0), ("A", a), ("prop", "x"))
    assert drain_rounds(sim, lambda: all(l.learned == "x" for l in sim.learners)) == 2


def test_classic_round_takes_three_delays() -> None:
    sim = FastPaxos(5, 3, 4, ["x"], seed=0, k=1)
    c = sim.coords[0]
    c.crnd = 1  # a classic round
    sim.net.send(("P", 0), ("C", 0), ("prop", "x"))
    assert drain_rounds(sim, lambda: "x" in c.proposals) == 1
    for a in range(3):
        c.on_1b(sim.net, 1, a, -1, None)  # phase 1 was done before: 2a goes out now
    assert drain_rounds(sim, lambda: all(l.learned == "x" for l in sim.learners)) == 2


def test_collision_and_coordinated_recovery() -> None:
    sim = FastPaxos(5, 3, 4, ["x", "y"], seed=0, k=1)
    prepare_fast_round(sim)
    # Two proposals arrive in different orders: A0, A1, A2 see x first, A3, A4 see y.
    for a in range(5):
        first, second = ("x", "y") if a < 3 else ("y", "x")
        sim.net.queue.append((("A", a), ("prop", first)))
        sim.net.queue.append((("A", a), ("prop", second)))
    for c in ("x", "y"):
        sim.net.queue.append((("C", 0), ("prop", c)))
    rounds = drain_rounds(sim, lambda: all(l.learned is not None for l in sim.learners))
    assert rounds == 4  # 2 for the fast round, 2 more for the recovery round
    r = sim.result()
    assert r.chosen == {"x"} and all(l.learned == "x" for l in sim.learners)
