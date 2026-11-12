# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/priority-ceiling-protocol/. The authors are listed in prov/TNQ9RS.jsonl.

import random

from priority_ceiling_protocol import Job, ceilings, simulate


def opposite_order() -> list[Job]:
    low = Job("J1", 1, 0, [("lock", "A"), ("run", 1), ("lock", "B"), ("run", 1), ("unlock", "B"), ("unlock", "A")])
    high = Job("J2", 2, 1, [("lock", "B"), ("run", 1), ("lock", "A"), ("run", 1), ("unlock", "A"), ("unlock", "B")])
    return [low, high]


def chain() -> list[Job]:
    return [
        Job("J3", 1, 0, [("lock", "A"), ("run", 2), ("unlock", "A")]),
        Job("J2", 2, 1, [("lock", "B"), ("run", 2), ("unlock", "B")]),
        Job("J1", 3, 2, [("lock", "A"), ("run", 1), ("unlock", "A"), ("lock", "B"), ("run", 1), ("unlock", "B")]),
    ]


def test_opposite_lock_order_deadlocks_under_pip_not_pcp() -> None:
    assert simulate(opposite_order(), "pip").deadlock
    assert simulate(opposite_order(), "none").deadlock
    r = simulate(opposite_order(), "pcp")
    assert not r.deadlock
    assert r.timeline == ["J1", "J1", "J2", "J2"]
    assert r.finish == {"J1": 2, "J2": 4}
    assert r.blocking["J2"] == 1
    i = simulate(opposite_order(), "icpp")
    assert not i.deadlock and i.finish == {"J1": 2, "J2": 4}


def test_chained_blocking() -> None:
    p = simulate(chain(), "pip")
    assert p.timeline == ["J3", "J2", "J3", "J1", "J2", "J1"]
    assert p.blockers["J1"] == {("J3", 1), ("J2", 1)}
    assert p.blocking["J1"] == 2
    c = simulate(chain(), "pcp")
    assert c.timeline == ["J3", "J3", "J1", "J1", "J2", "J2"]
    assert c.blocking["J1"] == 0
    assert c.blockers["J2"] == {("J3", 1)}


def test_ceilings() -> None:
    assert ceilings(chain()) == {"A": 3, "B": 3}
    assert ceilings(opposite_order()) == {"A": 2, "B": 2}


def test_edges() -> None:
    assert simulate([], "pcp").finish == {}
    r = simulate([Job("a", 1, 3, [("run", 2)])], "pcp")
    assert r.timeline == [None, None, None, "a", "a"] and r.finish == {"a": 5}
    r = simulate([Job("a", 1, 0, [("lock", "S"), ("unlock", "S")])], "pcp")
    assert r.finish == {"a": 0} and not r.deadlock


def random_jobs(rng: random.Random, ordered: bool) -> list[Job]:
    k = rng.randint(2, 5)
    prios = rng.sample(range(1, 20), k)
    jobs = []
    for i in range(k):
        acts: list = []
        for _ in range(rng.randint(1, 2)):
            if rng.random() < 0.5:
                acts.append(("run", rng.randint(1, 2)))
            locks = rng.sample(["A", "B", "C"], rng.randint(1, 2))
            if ordered:
                locks.sort()
            acts.append(("lock", locks[0]))
            acts.append(("run", rng.randint(1, 3)))
            if len(locks) == 2:
                acts += [("lock", locks[1]), ("run", rng.randint(1, 2)), ("unlock", locks[1])]
                if rng.random() < 0.5:
                    acts.append(("run", 1))
            acts.append(("unlock", locks[0]))
        if rng.random() < 0.5:
            acts.append(("run", rng.randint(1, 2)))
        jobs.append(Job(f"J{i}", prios[i], rng.randint(0, 6), acts))
    return jobs


def outer_sections(job: Job) -> list[tuple[set, int]]:
    """For each outermost critical section: the locks in it and its length."""
    out, depth = [], 0
    for kind, arg in job.actions:
        if kind == "lock":
            if depth == 0:
                out.append([set(), 0])
            depth += 1
            out[-1][0].add(arg)
        elif kind == "unlock":
            depth -= 1
        elif depth > 0:
            out[-1][1] += arg
    return [(s, n) for s, n in out]


def outermost_locks(job: Job) -> list:
    out, depth = [], 0
    for kind, arg in job.actions:
        if kind == "lock":
            if depth == 0:
                out.append(arg)
            depth += 1
        elif kind == "unlock":
            depth -= 1
    return out


def check_mutual_exclusion_and_work(jobs: list[Job], r) -> None:
    for j in jobs:
        need = sum(a for k, a in j.actions if k == "run")
        assert r.timeline.count(j.name) == need
        assert all(r.timeline[t] != j.name for t in range(min(j.release, len(r.timeline))))


def test_pcp_random_never_deadlocks_and_blocks_once() -> None:
    rng = random.Random(7)
    for _ in range(600):
        jobs = random_jobs(rng, ordered=False)
        ceil = ceilings(jobs)
        for proto in ("pcp", "icpp"):
            r = simulate(jobs, proto)
            assert not r.deadlock
            assert len(r.finish) == len(jobs)
            check_mutual_exclusion_and_work(jobs, r)
            for j in jobs:
                assert len(r.blockers[j.name]) <= 1
                assert all(cs > 0 for _, cs in r.blockers[j.name])
                bound = max(
                    [n for o in jobs if o.priority < j.priority for s, n in outer_sections(o)
                     if max(ceil[x] for x in s) >= j.priority],
                    default=0,
                )
                assert r.blocking[j.name] <= bound


def test_pip_random_bounded_by_lower_jobs_and_locks() -> None:
    rng = random.Random(11)
    seen_two = False
    for _ in range(600):
        jobs = random_jobs(rng, ordered=True)
        r = simulate(jobs, "pip")
        assert not r.deadlock
        check_mutual_exclusion_and_work(jobs, r)
        for j in jobs:
            lower = [o for o in jobs if o.priority < j.priority]
            outer = {a for o in lower for a in outermost_locks(o)}
            assert all(cs > 0 for _, cs in r.blockers[j.name])
            assert len(r.blockers[j.name]) <= min(len(lower), len(outer))
            assert len({b for b, _ in r.blockers[j.name]}) == len(r.blockers[j.name])
            seen_two |= len(r.blockers[j.name]) >= 2
    assert seen_two
