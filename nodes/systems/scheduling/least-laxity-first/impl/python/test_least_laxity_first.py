# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/least-laxity-first/. The authors are listed in prov/GCJJ20.jsonl.

import random

from least_laxity_first import edf_slots, least_laxity_first, meets_deadlines, periodic_jobs, preemptions


def slot_feasible(jobs):
    """Brute force: try every choice of job in every unit slot."""
    end = max(d for _, _, d in jobs)
    states = {tuple(w for _, w, _ in jobs)}
    for t in range(end):
        new = set()
        for s in states:
            choices = [k for k in range(len(jobs)) if jobs[k][0] <= t and s[k] > 0]
            for k in choices or [None]:
                n = list(s)
                if k is not None:
                    n[k] -= 1
                if all(n[j] == 0 or jobs[j][2] > t + 1 for j in range(len(jobs))):
                    new.add(tuple(n))
        states = new
    return any(all(x == 0 for x in s) for s in states)


def test_thrashing_pair() -> None:
    jobs = [(0, 4, 8), (0, 4, 8)]
    slots, finish = least_laxity_first(jobs)
    assert slots == [0, 1, 1, 0, 0, 1, 1, 0] and finish == [8, 7]
    assert preemptions(slots, jobs) == 3
    loose, _ = least_laxity_first(jobs, sticky=False)
    assert loose == [0, 1, 0, 1, 0, 1, 0, 1] and preemptions(loose, jobs) == 6
    edf, _ = edf_slots(jobs)
    assert edf == [0, 0, 0, 0, 1, 1, 1, 1] and preemptions(edf, jobs) == 0


def test_periodic_preemptions_against_edf() -> None:
    jobs = periodic_jobs([(2, 5), (4, 7)])
    assert len(jobs) == 12
    llf, f1 = least_laxity_first(jobs)
    edf, f2 = edf_slots(jobs)
    assert meets_deadlines(f1, jobs) and meets_deadlines(f2, jobs)
    assert preemptions(llf, jobs) == 4 and preemptions(edf, jobs) == 1


def test_optimal_on_one_processor() -> None:
    rng = random.Random(6)
    feasible = 0
    for _ in range(400):
        jobs = []
        for _ in range(rng.randint(1, 4)):
            r = rng.randint(0, 5)
            w = rng.randint(1, 3)
            jobs.append((r, w, r + w + rng.randint(0, 4)))
        ok = slot_feasible(jobs)
        for sticky in (True, False):
            slots, finish = least_laxity_first(jobs, sticky)
            assert meets_deadlines(finish, jobs) == ok
            assert sum(1 for k in slots if k is not None) == sum(w for _, w, _ in jobs)
        feasible += ok
    assert 50 < feasible < 400


def test_never_fewer_preemptions_needed_than_zero() -> None:
    rng = random.Random(1)
    more = 0
    for _ in range(200):
        tasks = []
        for _ in range(rng.randint(2, 3)):
            t = rng.choice([3, 4, 5, 6, 8])
            tasks.append((rng.randint(1, t // 2 + 1), t))
        if sum(c / t for c, t in tasks) > 1:
            continue
        jobs = periodic_jobs(tasks)
        llf, _ = least_laxity_first(jobs)
        edf, _ = edf_slots(jobs)
        more += preemptions(llf, jobs) > preemptions(edf, jobs)
    assert more > 0
