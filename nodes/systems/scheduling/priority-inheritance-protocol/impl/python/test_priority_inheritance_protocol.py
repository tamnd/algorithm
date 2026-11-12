# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/priority-inheritance-protocol/. The authors are listed in prov/1XKZ0H.jsonl.

import random

from priority_inheritance_protocol import Job, simulate


def inversion(m: int) -> list[Job]:
    return [
        Job("L", 1, 0, [("lock", "S"), ("run", 3), ("unlock", "S"), ("run", 1)]),
        Job("H", 3, 1, [("lock", "S"), ("run", 1), ("unlock", "S")]),
        Job("M", 2, 2, [("run", m)]),
    ]


def test_example_trace() -> None:
    p = simulate(inversion(4), "pip")
    assert p.timeline == ["L", "L", "L", "H", "M", "M", "M", "M", "L"]
    assert p.finish == {"L": 9, "H": 4, "M": 8}
    n = simulate(inversion(4), "none")
    assert n.timeline == ["L", "L", "M", "M", "M", "M", "L", "H", "L"]
    assert n.finish["H"] == 8


def test_inheritance_bounds_the_inversion() -> None:
    for m in range(1, 30):
        n = simulate(inversion(m), "none")
        p = simulate(inversion(m), "pip")
        assert n.blocking["H"] == m + 2
        assert n.finish["H"] == m + 4
        assert p.blocking["H"] == 2
        assert p.finish["H"] == 4
        assert p.blockers["H"] == {("L", 1)}


def test_transitive_inheritance() -> None:
    jobs = [
        Job("J3", 1, 0, [("lock", "A"), ("run", 3), ("unlock", "A")]),
        Job("J2", 2, 1, [("lock", "B"), ("run", 1), ("lock", "A"), ("run", 1), ("unlock", "A"), ("unlock", "B")]),
        Job("Jm", 3, 3, [("run", 5)]),
        Job("J1", 4, 3, [("lock", "B"), ("run", 1), ("unlock", "B")]),
    ]
    r = simulate(jobs, "pip")
    assert r.timeline == ["J3", "J2", "J3", "J3", "J2", "J1", "Jm", "Jm", "Jm", "Jm", "Jm"]
    assert r.blockers["J1"] == {("J3", 1), ("J2", 1)}


def test_deadlock_is_not_prevented() -> None:
    jobs = [
        Job("J1", 1, 0, [("lock", "A"), ("run", 1), ("lock", "B"), ("run", 1), ("unlock", "B"), ("unlock", "A")]),
        Job("J2", 2, 1, [("lock", "B"), ("run", 1), ("lock", "A"), ("run", 1), ("unlock", "A"), ("unlock", "B")]),
    ]
    r = simulate(jobs, "pip")
    assert r.deadlock and r.timeline == ["J1", "J2"] and r.finish == {}


def test_chained_blocking() -> None:
    jobs = [
        Job("J3", 1, 0, [("lock", "A"), ("run", 2), ("unlock", "A")]),
        Job("J2", 2, 1, [("lock", "B"), ("run", 2), ("unlock", "B")]),
        Job("J1", 3, 2, [("lock", "A"), ("run", 1), ("unlock", "A"), ("lock", "B"), ("run", 1), ("unlock", "B")]),
    ]
    r = simulate(jobs, "pip")
    assert r.timeline == ["J3", "J2", "J3", "J1", "J2", "J1"]
    assert r.blocking["J1"] == 2 and len(r.blockers["J1"]) == 2


def test_edges() -> None:
    assert simulate([], "pip").finish == {}
    r = simulate([Job("a", 5, 2, [("run", 1)])], "pip")
    assert r.timeline == [None, None, "a"] and r.finish == {"a": 3}


def outermost(job: Job) -> list[tuple[object, int]]:
    out, depth = [], 0
    for kind, arg in job.actions:
        if kind == "lock":
            if depth == 0:
                out.append([arg, 0])
            depth += 1
        elif kind == "unlock":
            depth -= 1
        elif depth > 0:
            out[-1][1] += arg
    return [(s, n) for s, n in out]


def random_jobs(rng: random.Random) -> list[Job]:
    k = rng.randint(2, 5)
    prios = rng.sample(range(1, 20), k)
    jobs = []
    for i in range(k):
        acts: list = []
        for _ in range(rng.randint(1, 2)):
            if rng.random() < 0.5:
                acts.append(("run", rng.randint(1, 2)))
            locks = sorted(rng.sample(["A", "B", "C"], rng.randint(1, 2)))
            acts += [("lock", locks[0]), ("run", rng.randint(1, 3))]
            if len(locks) == 2:
                acts += [("lock", locks[1]), ("run", rng.randint(1, 2)), ("unlock", locks[1])]
            acts.append(("unlock", locks[0]))
        if rng.random() < 0.5:
            acts.append(("run", rng.randint(1, 2)))
        jobs.append(Job(f"J{i}", prios[i], rng.randint(0, 6), acts))
    return jobs


def test_random_blocking_bound_min_n_m() -> None:
    rng = random.Random(3)
    worse = 0
    for _ in range(700):
        jobs = random_jobs(rng)
        r = simulate(jobs, "pip")
        n = simulate(jobs, "none")
        assert not r.deadlock
        for j in jobs:
            assert r.timeline.count(j.name) == sum(a for k, a in j.actions if k == "run")
            lower = [o for o in jobs if o.priority < j.priority]
            sems = {s for o in lower for s, _ in outermost(o)}
            got = r.blockers[j.name]
            assert all(c > 0 for _, c in got)
            assert len(got) <= min(len(lower), len(sems))
            assert len({b for b, _ in got}) == len(got)
            longest = {o.name: max([x for _, x in outermost(o)], default=0) for o in lower}
            assert r.blocking[j.name] <= sum(longest.values())
        if not n.deadlock and max(n.blocking.values()) > max(r.blocking.values()):
            worse += 1
    assert worse > 0
