# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lock-freedom/. The authors are listed in prov/NXBV97.jsonl.
"""Lock-freedom on the Treiber stack push.

push is the CAS retry loop. It is lock-free: a CAS fails only if another
CAS succeeded since the read. It is not wait-free: the schedule in
starving_schedule() makes one process fail for ever while the other keeps
pushing. A lock-based push is shown for contrast: if the lock holder stops,
nobody completes.
"""

from explorer import World


def push(v, uid):
    yield ("inv", "push", v)
    while True:
        t = yield ("read", "top")
        if (yield ("cas", "top", t, (uid, v, t))):
            yield ("res", None)
            return


def pusher(pid, count):
    """Push count values (for ever if count is None)."""
    k = 0
    while count is None or k < count:
        yield from push(k, (pid, k))
        k += 1


def locked_push(v, uid):
    """A push under a test-and-set spin lock."""
    yield ("inv", "push", v)
    while (yield ("tas", "lock")) == 1:
        pass
    t = yield ("read", "top")
    yield ("write", "top", (uid, v, t))
    yield ("write", "lock", 0)
    yield ("res", None)


def locked_pusher(pid, count):
    k = 0
    while count is None or k < count:
        yield from locked_push(k, (pid, k))
        k += 1


def setup_for(n, count, locked=False):
    def setup():
        make = locked_pusher if locked else pusher
        return {"top": None, "lock": 0}, [make(p, count) for p in range(n)]

    return setup


def completions(w):
    """The number of completed operations of each process."""
    out = [0] * len(w.gens)
    for e in w.history:
        if e[0] == "res":
            out[e[1]] += 1
    return out


def starving_schedule(rounds):
    """p0 reads, p1 runs a whole push, p0's CAS fails. Repeat.

    Both processes take infinitely many steps, so the schedule is fair, yet
    p0 never completes. Returns the world after the given number of rounds.
    """
    w = World(setup_for(2, None))
    for _ in range(rounds):
        w.step(0)          # p0 reads top
        w.step(1)          # p1 reads top
        w.step(1)          # p1 CAS succeeds: one push done
        w.step(0)          # p0 CAS fails, because top changed
    return w


def max_steps_without_completion(n, count):
    """The longest stretch of steps with no completed operation, over all runs.

    A depth first search over (state, length of the current stretch).
    """
    best = 0
    seen = set()
    stack = [((), 0)]
    setup = setup_for(n, count)
    while stack:
        s, run = stack.pop()
        w = World(setup)
        for p in s:
            w.step(p)
        k = (w.key(), run)
        if k in seen:
            continue
        seen.add(k)
        best = max(best, run)
        for p in w.enabled():
            before = len([e for e in w.history if e[0] == "res"])
            w2 = World(setup)
            for q in s + (p,):
                w2.step(q)
            after = len([e for e in w2.history if e[0] == "res"])
            stack.append((s + (p,), 0 if after > before else run + 1))
    return best
