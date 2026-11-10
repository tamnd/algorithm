# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/barrier-synchronization/. The authors are listed in prov/1ACZ46.jsonl.
"""Barriers, shown in two ways.

1. Message barriers in synchronous rounds: the dissemination barrier and the
   combining tree barrier. We track which arrivals each processor knows of.
2. Shared-memory barriers under a seeded random interleaving: a naive
   reusable counter barrier, which can deadlock, and the sense-reversing
   barrier, which cannot. Each thread is a generator. It yields None after
   one atomic step, or yields a condition (a function with no arguments)
   when it must wait until the condition is true.
"""


def ceil_log2(x):
    return (x - 1).bit_length() if x > 1 else 0


def ceil_log(x, k):
    """The least t >= 0 with k^t >= x."""
    t, cap = 0, 1
    while cap < x:
        cap *= k
        t += 1
    return t


# ------------------------------------------------------ dissemination barrier


def dissemination(p):
    """Run the dissemination barrier in synchronous rounds. In round r each
    processor i sends one message to (i + 2^r) mod p, and the receiver adds
    the sender's knowledge to its own. Returns (rounds, knowledge, messages),
    where knowledge[i] is the set of processors that i knows have arrived."""
    know = [{i} for i in range(p)]
    rounds = messages = 0
    while any(len(k) < p for k in know):
        d = 1 << rounds
        old = [set(k) for k in know]  # all sends of a round read the old state
        for i in range(p):
            know[(i + d) % p] |= old[i]
            messages += 1
        rounds += 1
    return rounds, know, messages


def dissemination_exit_times(arrive):
    """Asynchronous timing model: one message takes one time unit. Processor
    i arrives at time arrive[i]. It finishes round r at
    t_i(r) = max(t_i(r - 1), t_{i - 2^r}(r - 1)) + 1, with t_i(-1) = arrive[i].
    Returns the exit times."""
    p = len(arrive)
    t = list(arrive)
    for r in range(ceil_log2(p)):
        d = 1 << r
        t = [max(t[i], t[(i - d) % p]) + 1 for i in range(p)]
    return t


# ------------------------------------------------- combining tree barrier


def tree_barrier(p, k):
    """A combining tree of fan-in k in synchronous rounds. In the arrival
    phase each group of up to k nodes reports to its first member, level by
    level. In the release phase the root sends the go signal back down the
    same tree. Returns (arrival rounds, release rounds, the largest number of
    messages that one node receives in a round, the set the root knows)."""
    if k < 2:
        raise ValueError("fan-in must be at least 2")
    know = {i: {i} for i in range(p)}
    level = list(range(p))  # the nodes that still report upward
    up = 0
    fan = 0
    while len(level) > 1:
        nxt = []
        for g in range(0, len(level), k):
            group = level[g:g + k]
            head = group[0]
            for other in group[1:]:
                know[head] |= know[other]
            fan = max(fan, len(group) - 1)
            nxt.append(head)
        level = nxt
        up += 1
    root_knows = know[level[0]] if p else set()
    # The release follows the same tree downward: one round per level.
    down = up
    return up, down, fan, root_knows


# ------------------------------------------- shared-memory barriers, interleaved


class Shared:
    def __init__(self):
        self.count = 0
        self.flag = 0


def naive_barrier(sh, p, me, episodes, log):
    """The counter barrier with one flag and no sense reversal. The first
    thread to arrive resets the flag. This is wrong for reuse: a fast thread
    can reset the flag before a slow thread has seen it set."""
    for e in range(episodes):
        log.append(("arrive", e, me))
        yield None
        if sh.count == 0:          # one atomic step: the lock is held
            sh.flag = 0
        sh.count += 1
        mine = sh.count
        yield None
        if mine == p:
            sh.count = 0
            sh.flag = 1
            yield None
        else:
            yield (lambda: sh.flag == 1)
        log.append(("leave", e, me))
        yield None


def sense_barrier(sh, p, me, episodes, log):
    """The sense-reversing barrier. Each thread flips its local sense in each
    episode, and waits until the shared flag equals its local sense."""
    sense = 0
    for e in range(episodes):
        sense = 1 - sense
        log.append(("arrive", e, me))
        yield None
        sh.count += 1               # an atomic fetch-and-increment
        mine = sh.count
        yield None
        if mine == p:
            sh.count = 0
            sh.flag = sense
            yield None
        else:
            yield (lambda s=sense: sh.flag == s)
        log.append(("leave", e, me))
        yield None


def run_interleaved(barrier, p, episodes, rng, max_steps=100000):
    """Run p threads under a random interleaving chosen by rng.
    Returns ("ok" or "deadlock", log)."""
    sh = Shared()
    log = []
    threads = [barrier(sh, p, i, episodes, log) for i in range(p)]
    waits = [None] * p
    done = [False] * p
    for _ in range(max_steps):
        ready = [i for i in range(p) if not done[i] and (waits[i] is None or waits[i]())]
        if not ready:
            return ("ok" if all(done) else "deadlock"), log
        i = rng.choice(ready)
        waits[i] = None
        try:
            waits[i] = next(threads[i])
        except StopIteration:
            done[i] = True
    raise RuntimeError("step limit reached")


def barrier_property_holds(log, p):
    """No thread leaves episode e before all p threads have arrived at e."""
    arrived = {}
    for what, e, _ in log:
        if what == "arrive":
            arrived[e] = arrived.get(e, 0) + 1
        elif arrived.get(e, 0) < p:
            return False
    return True
