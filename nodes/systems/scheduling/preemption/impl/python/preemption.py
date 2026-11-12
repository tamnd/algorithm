# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/preemption/. The authors are listed in prov/D0YFHB.jsonl.

"""Priority scheduling on one CPU under three preemption models.

mode "none":   a process keeps the CPU until its burst ends.
mode "resume": an arriving process of higher priority preempts the running one,
               which later continues where it stopped (preempt-resume).
mode "repeat": as "resume", but the preempted process loses its progress and
               must run its whole burst again (preempt-repeat).

A smaller priority number is a higher priority. Each dispatch of a process
other than the one that ran last costs `switch` time units. If a process of
higher priority arrives during a switch, the preemptive modes decide again when
the switch ends. Times may be int or Fraction.
"""


def schedule(arrival: list, burst: list, priority: list, mode: str = "resume", switch=0) -> dict:
    """Return a dict with completion, slices (process, start, end) and switches."""
    assert mode in ("none", "resume", "repeat")
    n = len(arrival)
    order = sorted(range(n), key=lambda i: (arrival[i], i))
    left = list(burst)
    completion = [None] * n
    slices, ready = [], []
    k, t, last, switches = 0, 0, None, 0

    def admit(now) -> None:
        nonlocal k
        while k < n and arrival[order[k]] <= now:
            ready.append(order[k])
            k += 1

    while k < n or ready:
        if not ready and t < arrival[order[k]]:
            t = arrival[order[k]]
        admit(t)
        i = min(ready, key=lambda j: (priority[j], arrival[j], j))
        ready.remove(i)
        key = (priority[i], arrival[i], i)
        if i != last:
            t = t + switch
            switches += 1
            last = i
            admit(t)
            if mode != "none" and any((priority[j], arrival[j], j) < key for j in ready):
                ready.append(i)  # outranked during the switch: decide again
                continue
        end = t + left[i]
        if mode != "none":
            # the first later arrival that outranks i ends the slice
            for j in order[k:]:
                if arrival[j] >= end:
                    break
                if (priority[j], arrival[j], j) < key:
                    end = arrival[j]
                    break
        slices.append((i, t, end))
        left[i] = left[i] - (end - t)
        t, last = end, i
        admit(t)
        if left[i] > 0:
            if mode == "repeat":
                left[i] = burst[i]
            ready.append(i)
        else:
            completion[i] = t
    return {"completion": completion, "slices": slices, "switches": switches}


def response_times(arrival: list, result: dict) -> list:
    """Time from arrival to the first slice, for each process."""
    first = {}
    for i, s, _ in result["slices"]:
        first.setdefault(i, s)
    return [first[i] - arrival[i] for i in range(len(arrival))]
