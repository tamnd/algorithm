# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bkp-speed-scaling/. The authors are listed in prov/Z0T4F5.jsonl.

import math

E = math.e
EPS = 1e-9

Job = tuple[float, float, float]  # (release r, work w, deadline d)


def bkp_speed(jobs: list[Job], t: float) -> float:
    """Return the BKP speed at time t, from the jobs released by t.

    The speed is the maximum over t2 > t of w(t, t1, t2) / (t2 - t), with
    t1 = e t - (e - 1) t2, where w(t, t1, t2) is the original work of the
    jobs with t1 <= r_j <= t and d_j <= t2. The maximum is reached at a
    deadline or at a time where t1 equals a release time.
    """
    known = [job for job in jobs if job[0] <= t]  # @line L2
    cands = [d for _, _, d in known if d > t]  # @line L3
    cands += [(E * t - r) / (E - 1) for r, _, _ in known if r < t]
    speed = 0.0
    for t2 in cands:  # @line L4
        t1 = E * t - (E - 1) * t2  # @line L5
        work = sum(w for r, w, d in known if r >= t1 - EPS and d <= t2 + EPS)
        speed = max(speed, work / (t2 - t))  # @line L6
    return speed


def bkp_schedule(jobs: list[Job], h: float, alpha: float) -> tuple[float, list[float], float]:
    """Simulate BKP with time steps of length h.

    The release times should be multiples of h after the first release.
    The speed of each step is the BKP speed at its midpoint, and the
    processor runs the released, unfinished job with the earliest deadline,
    or idles if there is none. Return the energy, the completion time of
    each job (rounded up to the end of its step) and the largest speed.
    """
    n = len(jobs)
    start = min(r for r, _, _ in jobs)
    rem = [float(w) for _, w, _ in jobs]
    done = [math.inf] * n
    total, top = 0.0, 0.0
    i = 0
    while any(x > EPS for x in rem):  # @line L1
        a = start + i * h
        i += 1
        ready = [j for j in range(n) if rem[j] > EPS and jobs[j][0] <= a + EPS]
        if not ready:
            continue
        s = bkp_speed(jobs, a + h / 2)  # @line L2
        total += s ** alpha * h  # @line L7
        top = max(top, s)
        work = s * h
        for j in sorted(ready, key=lambda j: (jobs[j][2], j)):
            x = min(work, rem[j])
            rem[j] -= x
            work -= x
            if rem[j] <= EPS:
                rem[j] = 0.0
                done[j] = a + h
            if work <= 0:
                break
    return total, done, top  # @line L8
