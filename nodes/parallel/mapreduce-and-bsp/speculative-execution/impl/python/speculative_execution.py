# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/speculative-execution/. The authors are listed in prov/SZRQN3.jsonl.
"""Speculative execution (backup tasks) in a simple model, and the task
choice rules of Hadoop and LATE.

The model: a job has n independent tasks. A task takes time 1, but with
probability pi it lands on a slow machine and takes time s >= 2. At time 1
every task that has not finished gets one backup copy on a fresh machine,
which is slow with probability pi, independently. A task ends when its first
copy ends, and the job ends when its last task ends.
"""


def expected_no_backup(n, pi, s):
    """E[T] = 1 + (s - 1) * (1 - (1 - pi)^n)."""
    return 1 + (s - 1) * (1 - (1 - pi) ** n)


def expected_with_backup(n, pi, s):
    """E[T] = (1-pi)^n * 1 + ((1-pi^2)^n - (1-pi)^n) * 2 + (1 - (1-pi^2)^n) * s.
    A task is late (time s) only when the original and the backup are both slow."""
    a = (1 - pi) ** n
    b = (1 - pi * pi) ** n
    return a + 2 * (b - a) + s * (1 - b)


def simulate(n, pi, s, rng, backups):
    """One run of the job. Returns (the job time, the number of backup copies)."""
    if s < 2:
        raise ValueError("the model needs s >= 2")
    finish, copies = 0, 0
    for _ in range(n):
        t = s if rng.random() < pi else 1
        if backups and t > 1:
            copies += 1
            b = s if rng.random() < pi else 1
            t = min(t, 1 + b)
        finish = max(finish, t)
    return finish, copies


# ------------------------------------------------------------- choice rules


def hadoop_candidates(tasks, now, min_age=60.0, gap=0.2):
    """Hadoop's rule (Zaharia et al. 2008, Section 2.1): a task is a
    candidate when its progress score is below the average of its category
    minus 0.2 and it has run for at least one minute. tasks is a list of
    (name, start time, progress score in [0, 1])."""
    if not tasks:
        return []
    avg = sum(ps for _, _, ps in tasks) / len(tasks)
    return [name for name, start, ps in tasks if ps < avg - gap and now - start >= min_age]


def late_estimates(tasks, now):
    """LATE: progress rate = score / elapsed time, and
    time left = (1 - score) / rate."""
    out = {}
    for name, start, ps in tasks:
        elapsed = now - start
        rate = ps / elapsed if elapsed > 0 else 0.0
        out[name] = (rate, (1 - ps) / rate if rate > 0 else float("inf"))
    return out


def late_choice(tasks, now, slow_task_percentile=25):
    """Among the tasks whose progress rate is at or below the given
    percentile of all rates, pick the one with the longest time left."""
    est = late_estimates(tasks, now)
    if not est:
        return None
    rates = sorted(r for r, _ in est.values())
    cut = rates[(len(rates) - 1) * slow_task_percentile // 100]
    slow = [name for name, (r, _) in est.items() if r <= cut]
    return max(slow, key=lambda name: est[name][1])
