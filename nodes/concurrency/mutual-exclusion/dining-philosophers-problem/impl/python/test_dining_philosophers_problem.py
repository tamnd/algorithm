# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dining-philosophers-problem/. The authors are listed in prov/611KPX.jsonl.
from dining_philosophers_problem import build, neighbours_never_eat_together
from procsim import explore, random_run, run

SOLUTIONS = ("ordered", "asymmetric", "waiter", "dijkstra")


def test_naive_deadlocks_when_everyone_takes_the_left_fork():
    res = explore(lambda: build(3, "naive"))
    assert res.deadlocks and not res.truncated
    # the deadlock found: every philosopher holds its left fork
    sim = build(3, "naive")
    for p in ("p0", "p1", "p2", "p0", "p1", "p2"):  # think, then take the left fork
        sim.step(p)
    assert sim.enabled() == []
    assert all(sim.mutexes[f"fork{i}"].owner == f"p{i}" for i in range(3))


def test_solutions_exhaustive_at_n3():
    for policy in SOLUTIONS:
        res = explore(lambda: build(3, policy, rounds=2), invariant=neighbours_never_eat_together)
        assert res.deadlocks == [] and res.violations == [] and not res.truncated, policy
        assert res.finals == 1, policy


def test_solutions_seeded_at_n5():
    for policy in SOLUTIONS:
        for seed in range(30):
            r = random_run(lambda: build(5, policy, rounds=3), seed,
                           invariant=neighbours_never_eat_together)
            assert r.outcome == "done", (policy, seed, r.outcome, r.message)
            assert r.sim.v["meals"] == [3] * 5


def test_waiter_with_n_seats_deadlocks():
    # with n seats instead of n - 1 the waiter is no help
    def build_bad():
        s = build(3, "waiter")
        s.sems["seats"].count = 3
        return s
    assert explore(build_bad).deadlocks


def test_dijkstra_solution_can_starve_a_philosopher():
    # p0 and p2 are not neighbours, so they can take turns at eating with overlapping
    # meals; p1, between them, is hungry the whole time and never eats
    sim = build(5, "dijkstra", rounds=10)

    def advance(p, cond):
        for _ in range(50):
            if cond():
                return
            sim.step(p)
        raise AssertionError(p)

    advance("p0", lambda: sim.v["meals"][0] == 1)
    advance("p2", lambda: sim.v["meals"][2] == 1)
    advance("p1", lambda: "p1" not in sim.enabled())  # hungry, blocked in P(s1)
    assert sim.v["state"][1] == "hungry"
    for k in range(2, 10):
        for i in (0, 2):
            advance(f"p{i}", lambda i=i, k=k: sim.v["meals"][i] == k)
    assert sim.v["meals"][:3] == [9, 0, 9] and sim.v["state"][1] == "hungry"
    assert "p1" not in sim.enabled()


def lock_step(n):
    """The adversary of the symmetry argument: p0, p1, ..., p(n-1), again and again."""
    order = [f"p{i}" for i in range(n)]
    count = [0]

    def choose(sim, en):
        while True:
            p = order[count[0] % n]
            count[0] += 1
            if p in en:
                return p
    return choose


def test_symmetric_deterministic_rule_starves_everybody_in_lock_step():
    n = 5
    r = run(lambda: build(n, "polite"), lock_step(n), max_steps=40 * n)
    assert r.outcome == "limit" and r.sim.v["meals"] == [0] * n
    # after each full round, all philosophers are in the same local state
    sim = build(n, "polite")
    for rnd in range(30):
        for i in range(n):
            sim.step(f"p{i}")
        owners = [sim.mutexes[f"fork{i}"].owner for i in range(n)]
        assert owners == [None] * n or owners == [f"p{i}" for i in range(n)]
        ops = {sim.procs[f"p{i}"].op[0] for i in range(n)}
        assert len(ops) == 1


def test_lehmann_rabin_breaks_symmetry_with_coins():
    n = 5
    for seed in range(20):
        r = run(lambda: build(n, "free", rounds=2, seed=seed), lock_step(n), max_steps=5000,
                invariant=neighbours_never_eat_together)
        assert r.outcome == "done", (seed, r.outcome)
    for seed in range(20):
        r = random_run(lambda: build(n, "free", rounds=3, seed=seed), seed, max_steps=20000,
                       invariant=neighbours_never_eat_together)
        assert r.outcome == "done" and r.sim.v["meals"] == [3] * n
