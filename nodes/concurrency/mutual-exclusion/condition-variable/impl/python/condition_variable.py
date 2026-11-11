# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/condition-variable/. The authors are listed in prov/TSEGXF.jsonl.

"""Condition variables, as procsim models.

A condition variable c is used with a mutex m. Its operations are

  wait(c)       release m and block, in one atomic step; when woken, take m
                again before returning (Mesa semantics: a woken thread only
                gets a hint, and must test its predicate again)
  signal(c)     wake at least one thread that waits on c, if any
  broadcast(c)  wake every thread that waits on c

Signal and broadcast do nothing when no thread waits: unlike a semaphore,
a condition variable has no memory.

Implementations (the argument `impl`):
  native           the condition variables of procsim (Mesa semantics)
  birrell1         Birrell's first try: a binary semaphore s.
                   Wait: m.Release(); s.P(); m.Acquire().  Signal: s.V().
                   Bug: a Signal with no waiter leaves s at 1, and a later
                   Wait returns at once.
  birrell2-binary  Birrell's second try: a lock x and a count waiters, so a
                   Signal with no waiter does nothing; s is still binary.
                   Bug: a Broadcast that does V(s) several times while the
                   waiters have not yet done P(s) leaves s at 1, and all but
                   one waiter stay blocked.
  birrell2         the same with a counting s.
                   Bug: a thread that calls Wait after a Broadcast or Signal
                   can take a V(s) that was meant for an older waiter, which
                   then stays blocked.
  birrell3         Birrell's third version: a handshake semaphore h; Signal
                   and Broadcast wait until each woken thread has done its
                   P(s). Correct, at the cost of extra context switches.
  queue            an explicit FIFO queue of waiting threads, each with its
                   own binary semaphore, under a lock x.

Scenarios:
  build_flag    threads wait for a flag that one setter raises; optionally a
                late thread that waits for a flag value that never comes, and
                waiters that do not test the predicate at all
  build_buffer  a bounded buffer of `capacity` slots (only the count is
                modelled) with producers and consumers, one or two condition
                variables, signal or broadcast, and while or if

Every wait is checked against the law "a wait returns only after some
signal or broadcast that was issued after the wait began" (spurious
wakeups are not modelled). A wait that breaks it sets v["early"].

Precondition: the caller of wait, signal and broadcast holds m.
Cost: each operation is O(1) steps, except that broadcast is O(w) steps for
w waiters; birrell3 adds 2 semaphore operations per woken thread.
"""

from typing import Callable, Iterator, Optional

from procsim import Semaphore, Sim

IMPLS = ("native", "birrell1", "birrell2-binary", "birrell2", "birrell3", "queue")
CORRECT = ("native", "birrell3", "queue")


def make_cv(s: Sim, impl: str, c: str, m: str) -> None:
    """Create the objects of condition variable c, used with mutex m."""
    s.v.setdefault("wakes", {})[c] = 0
    if impl == "native":
        s.cond(c, m, "mesa")
    elif impl == "birrell1":
        s.semaphore(c + ".s", 0)
    elif impl in ("birrell2-binary", "birrell2", "birrell3"):
        s.semaphore(c + ".x", 1)
        s.semaphore(c + ".s", 0)
        s.v[c + ".waiters"] = 0
        if impl == "birrell3":
            s.semaphore(c + ".h", 0)
    elif impl == "queue":
        s.mutex(c + ".x")
        s.v[c + ".q"] = []
    else:
        raise ValueError(impl)


def _binary_v(name: str):
    """V on a binary semaphore: the count stops at 1."""
    def f(s: Sim) -> None:
        sem = s.sems[name]
        sem.count = min(1, sem.count + 1)
    return ("atomic", f)


def _add(name: str, d: int):
    def f(s: Sim) -> int:
        s.v[name] += d
        return s.v[name]
    return f


def _get(name: str):
    def f(s: Sim):
        return s.v[name]
    return f


def _enqueue(c: str, me: str):
    def f(s: Sim) -> None:
        s.v[c + ".q"].append(me)
        s.sems.setdefault(f"{c}.{me}", Semaphore(0, False))
    return f


def _dequeue(c: str, all_: bool):
    def f(s: Sim) -> list:
        q = s.v[c + ".q"]
        out = q[:] if all_ else q[:1]
        del q[: len(out)]
        return out
    return f


def wait(impl: str, c: str, m: str, me: str) -> Iterator[tuple]:
    """Release m, block until woken, take m again."""
    if impl == "native":
        yield ("wait", c)
    elif impl == "birrell1":
        yield ("unlock", m)
        yield ("P", c + ".s")
        yield ("lock", m)
    elif impl in ("birrell2-binary", "birrell2", "birrell3"):
        yield ("P", c + ".x")
        yield ("atomic", _add(c + ".waiters", 1))
        yield ("V", c + ".x")
        yield ("unlock", m)
        yield ("P", c + ".s")  # point (1) in Birrell's text
        if impl == "birrell3":
            yield ("V", c + ".h")
        yield ("lock", m)
    elif impl == "queue":
        yield ("lock", c + ".x")
        yield ("atomic", _enqueue(c, me))
        yield ("unlock", c + ".x")
        yield ("unlock", m)
        yield ("P", f"{c}.{me}")
        yield ("lock", m)
    else:
        raise ValueError(impl)


def _v_s(impl: str, c: str):
    return _binary_v(c + ".s") if impl == "birrell2-binary" else ("V", c + ".s")


def signal(impl: str, c: str) -> Iterator[tuple]:
    """Wake one waiter of c, if there is one."""
    if impl == "native":
        yield ("signal", c)
    elif impl == "birrell1":
        yield _binary_v(c + ".s")
    elif impl in ("birrell2-binary", "birrell2", "birrell3"):
        yield ("P", c + ".x")
        if (yield ("atomic", _get(c + ".waiters"))) > 0:
            yield ("atomic", _add(c + ".waiters", -1))
            yield _v_s(impl, c)
            if impl == "birrell3":
                yield ("P", c + ".h")
        yield ("V", c + ".x")
    elif impl == "queue":
        yield ("lock", c + ".x")
        for w in (yield ("atomic", _dequeue(c, False))):
            yield ("V", f"{c}.{w}")
        yield ("unlock", c + ".x")
    else:
        raise ValueError(impl)


def broadcast(impl: str, c: str) -> Iterator[tuple]:
    """Wake every waiter of c."""
    if impl == "native":
        yield ("broadcast", c)
    elif impl == "birrell1":
        raise ValueError("Birrell's first version has no Broadcast")
    elif impl in ("birrell2-binary", "birrell2"):
        yield ("P", c + ".x")
        while (yield ("atomic", _get(c + ".waiters"))) > 0:
            yield ("atomic", _add(c + ".waiters", -1))
            yield _v_s(impl, c)
        yield ("V", c + ".x")
    elif impl == "birrell3":
        yield ("P", c + ".x")
        n = yield ("atomic", _get(c + ".waiters"))
        for _ in range(n):
            yield ("V", c + ".s")
        while (yield ("atomic", _get(c + ".waiters"))) > 0:
            yield ("atomic", _add(c + ".waiters", -1))
            yield ("P", c + ".h")
        yield ("V", c + ".x")
    elif impl == "queue":
        yield ("lock", c + ".x")
        for w in (yield ("atomic", _dequeue(c, True))):
            yield ("V", f"{c}.{w}")
        yield ("unlock", c + ".x")
    else:
        raise ValueError(impl)


# The law check: a wait returns only after a signal or broadcast issued after it began.

def _count_wake(c: str):
    def f(s: Sim) -> None:
        s.v["wakes"][c] += 1
    return f


def _wakes(c: str):
    def f(s: Sim) -> int:
        return s.v["wakes"][c]
    return f


def _check_after(c: str, start: int):
    def f(s: Sim) -> None:
        if s.v["wakes"][c] <= start:
            s.v["early"] = True
    return f


def checked_wait(impl: str, c: str, m: str, me: str) -> Iterator[tuple]:
    start = yield ("atomic", _wakes(c))
    yield from wait(impl, c, m, me)
    yield ("atomic", _check_after(c, start))


def notify(impl: str, c: str, how: str) -> Iterator[tuple]:
    """signal(c) or broadcast(c), counted for the law check."""
    yield ("atomic", _count_wake(c))
    yield from (signal(impl, c) if how == "signal" else broadcast(impl, c))


def wait_until(impl: str, c: str, m: str, me: str, pred: Callable[[Sim], bool],
               loop: bool = True) -> Iterator[tuple]:
    """while not pred: wait(c)  (or `if` in place of `while` when loop is False)."""
    if loop:
        while not (yield ("atomic", pred)):
            yield from checked_wait(impl, c, m, me)
    elif not (yield ("atomic", pred)):
        yield from checked_wait(impl, c, m, me)


# Scenario 1: a flag.

def _flag_at_least(k: int):
    def f(s: Sim) -> bool:
        return s.v["flag"] >= k
    return f


def _set_flag(s: Sim) -> None:
    s.v["flag"] = 1


def flag_waiter(sim: Sim, me: str, impl: str, check: bool, target: int) -> Iterator[tuple]:
    yield ("lock", "m")
    if check:
        yield from wait_until(impl, "c", "m", me, _flag_at_least(target))
    else:
        yield from checked_wait(impl, "c", "m", me)  # waits without testing the flag
    yield ("unlock", "m")


def setter(sim: Sim, me: str, impl: str, how: str) -> Iterator[tuple]:
    yield ("lock", "m")
    yield ("atomic", _set_flag)
    yield from notify(impl, "c", how)
    yield ("unlock", "m")


def build_flag(impl: str, waiters: int = 1, how: str = "broadcast", late: bool = False,
               check: bool = True) -> Sim:
    """`waiters` threads wait for flag >= 1, which one setter raises.

    With late=True, a daemon thread also waits on c for flag >= 2, which never
    happens; it may call wait after the setter's signal or broadcast.
    """
    s = Sim()
    s.v.update(flag=0, early=False)
    s.mutex("m")
    make_cv(s, impl, "c", "m")
    for i in range(waiters):
        s.spawn(f"w{i}", flag_waiter, impl, check, 1)
    s.spawn("setter", setter, impl, how)
    if late:
        s.spawn("late", flag_waiter, impl, True, 2, daemon=True)
    return s


# Scenario 2: a bounded buffer (only the count of items is modelled).

def _not_full(s: Sim) -> bool:
    return s.v["count"] < s.v["capacity"]


def _not_empty(s: Sim) -> bool:
    return s.v["count"] > 0


def _put(s: Sim) -> None:
    s.v["count"] += 1


def _take(s: Sim) -> None:
    s.v["count"] -= 1


def producer(sim: Sim, me: str, impl: str, items: int, conds: tuple, how: str,
             loop: bool) -> Iterator[tuple]:
    not_full, not_empty = conds
    for _ in range(items):
        yield ("lock", "m")
        yield from wait_until(impl, not_full, "m", me, _not_full, loop)
        yield ("atomic", _put)
        yield from notify(impl, not_empty, how)
        yield ("unlock", "m")


def consumer(sim: Sim, me: str, impl: str, items: int, conds: tuple, how: str,
             loop: bool) -> Iterator[tuple]:
    not_full, not_empty = conds
    for _ in range(items):
        yield ("lock", "m")
        yield from wait_until(impl, not_empty, "m", me, _not_empty, loop)
        yield ("atomic", _take)
        yield from notify(impl, not_full, how)
        yield ("unlock", "m")


def build_buffer(impl: str = "native", capacity: int = 1, producers: int = 1, consumers: int = 2,
                 items: int = 1, two_conds: bool = True, how: str = "signal",
                 loop: bool = True) -> Sim:
    """Producers and consumers on a buffer; each consumer takes `items` items.

    Precondition: producers divides consumers * items.
    """
    total = consumers * items
    assert total % producers == 0
    s = Sim()
    s.v.update(count=0, capacity=capacity, early=False)
    s.mutex("m")
    conds = ("notFull", "notEmpty") if two_conds else ("c", "c")
    for c in set(conds):
        make_cv(s, impl, c, "m")
    for i in range(producers):
        s.spawn(f"p{i}", producer, impl, total // producers, conds, how, loop)
    for i in range(consumers):
        s.spawn(f"c{i}", consumer, impl, items, conds, how, loop)
    return s


def safe(s: Sim) -> Optional[str]:
    """The invariant: no wait returned early, and the buffer count is in range."""
    if s.v.get("early"):
        return "a wait returned with no signal or broadcast after it began"
    if "count" in s.v and not 0 <= s.v["count"] <= s.v["capacity"]:
        return f"buffer count {s.v['count']} out of range"
    return None
