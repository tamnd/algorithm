# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-replica-dynamics/. The authors are listed in prov/6Z28SF.jsonl.
"""Parallel replica dynamics (Voter 1998) for a dynamics given as a time step.

step(x, rng) returns the state after one time step of length h, and
state_of(x) returns the label of the basin that contains x. One cycle has
three stages:

1. Decorrelation. One trajectory runs serially, and the clock advances
   with it, until it has stayed n_corr steps in one basin. Every change of
   basin in this stage is a transition of the output.
2. Dephasing. m replicas start from the current point and each runs until
   it has stayed n_corr steps in the basin. A replica that leaves the
   basin restarts. These steps do not advance the clock.
3. Parallel stage. All replicas advance one step at a time. At the first
   step w at which some replica leaves, take the smallest such index j
   (1-based). The clock advances by (m (w - 1) + j) h, and the trajectory
   continues from that replica.

If the escape from the basin is exponential (geometric, for discrete
steps) once the replicas are dephased, the time and the exit of each
transition have the same law as for one serial trajectory. This holds
exactly for a chain whose escape probability per step is constant in the
basin, and approximately for a real dynamics after dephasing. The speedup
is a measurement.

The time accounting m (w - 1) + j counts the trials of the replicas as if
they were done one after the other in the order (step, replica). This is
the accounting of Aristoff, Lelievre and Simpson (2014) for Markov chains.
"""

from typing import Callable, Hashable


def parallel_replica_dynamics(x0, step: Callable, state_of: Callable[[object], Hashable], m: int,
                              n_corr: int, rng, n_transitions: int, h: float = 1.0,
                              max_work: int = 10**7):
    """Run parallel replica dynamics until n_transitions changes of basin.

    Returns (x, t, transitions, work, wall): the final point, the clock, the
    list of (time, from_state, to_state), the total number of steps of all
    replicas (the cost), and the number of steps on the longest replica
    (the elapsed time on m processors, in steps). The measured speedup of a
    run is t / (h wall). Raises RuntimeError if work exceeds max_work.
    """
    x = x0
    s = state_of(x)
    t = 0.0                                                             # @line L1
    transitions = []
    work = 0
    wall = 0

    def charge(n=1):
        nonlocal work
        work += n
        if work > max_work:
            raise RuntimeError("parallel_replica_dynamics: max_work exceeded")

    while len(transitions) < n_transitions:                             # @line L2
        k = 0
        while k < n_corr and len(transitions) < n_transitions:
            x = step(x, rng)                                            # @line L3
            t += h
            charge()
            wall += 1
            k += 1
            s_new = state_of(x)
            if s_new != s:
                transitions.append((t, s, s_new))                       # @line L4
                s = s_new
                k = 0
        if len(transitions) >= n_transitions:
            break
        replicas = []
        longest = 0
        for _ in range(m):                                              # @line L5
            y, k, n = x, 0, 0
            while k < n_corr:
                y = step(y, rng)
                charge()
                n += 1
                k += 1
                if state_of(y) != s:
                    y, k = x, 0
            replicas.append(y)
            longest = max(longest, n)
        wall += longest
        w = 0
        while True:
            w += 1
            for j in range(m):                                          # @line L6
                replicas[j] = step(replicas[j], rng)
            charge(m)
            wall += 1
            first = next((j for j in range(m) if state_of(replicas[j]) != s), None)  # @line L7
            if first is not None:
                t += (m * (w - 1) + first + 1) * h                      # @line L8
                x = replicas[first]
                s_new = state_of(x)
                transitions.append((t, s, s_new))                       # @line L9
                s = s_new
                break
    return x, t, transitions, work, wall                                # @line L10
