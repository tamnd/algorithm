# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/monitor/. The authors are listed in prov/7D5E07.jsonl.

"""Monitors, as procsim models, with Hoare and Mesa semantics.

A monitor is shared data with procedures that run under mutual exclusion,
and condition variables on which a procedure can wait. Three modes:

  mesa       procsim's Mesa conditions: signal only makes a waiter ready;
             the signaller goes on, and other processes may enter the monitor
             before the waiter runs again
  hoare      procsim's Hoare conditions: signal hands the monitor to the
             waiter at once; the signaller waits until the waiter leaves or
             waits again
  hoare-sem  Hoare's own implementation of his monitors from semaphores
             (Hoare 1974): mutex = 1, urgent = 0 and urgentcount = 0 for the
             monitor, and condsem = 0 and condcount = 0 for each condition.
               entry:      P(mutex)
               exit:       if urgentcount > 0 then V(urgent) else V(mutex)
               wait(c):    condcount := condcount + 1
                           if urgentcount > 0 then V(urgent) else V(mutex)
                           P(condsem); condcount := condcount - 1
               signal(c):  urgentcount := urgentcount + 1
                           if condcount > 0 then V(condsem); P(urgent)
                           urgentcount := urgentcount - 1
  hoare-sem-no-urgent  the same, but exit and wait always do V(mutex); a
             broken variant, to show what urgent is for

Each model checks Hoare's proof rules as it runs: the monitor invariant I
must hold at every wait, at every signal, and at every exit; under Hoare
semantics the condition B of a wait must hold when the wait returns, and
must hold at every signal. A failed check sets a flag that the invariant
`check` reports.

Scenarios:
  build_resource  Hoare's single resource monitor (acquire and release with
                  a boolean busy and a condition nonbusy), tested with if or
                  while
  build_buffer    a bounded buffer monitor with conditions nonfull and
                  nonempty (only the count of items is modelled)

Precondition: a process calls monitor operations only between entry and
exit. Cost: each monitor operation is O(1) steps; under Hoare semantics a
signal that wakes a waiter costs two process switches.
"""

from typing import Callable, Iterator, Optional

from procsim import Sim

MODES = ("mesa", "hoare", "hoare-sem")
Pred = Callable[[Sim], bool]


def _flag(name: str):
    def f(s: Sim) -> None:
        s.v[name] = True
    return f


def _add(name: str, d: int):
    def f(s: Sim) -> int:
        s.v[name] += d
        return s.v[name]
    return f


def _get(name: str):
    def f(s: Sim):
        return s.v[name]
    return f


def _check(where: str, ok: Pred):
    def f(s: Sim) -> None:
        if not ok(s):
            s.v["broken"] = where
    return f


def _event(kind: str):
    """Log (kind, process) for the tests; the log is not part of the state."""
    def f(s: Sim) -> None:
        s.emit(kind, s.current)
    return f


def _inv(s: Sim) -> bool:
    return s.v["I"](s)


def enter(mode: str) -> Iterator[tuple]:
    if mode.startswith("hoare-sem"):
        yield ("P", "mutex")
    else:
        yield ("lock", "mon")
    yield ("atomic", _add("inside", 1))


def _release_monitor(mode: str) -> Iterator[tuple]:
    """Hoare's exit code: let a waiting signaller in first."""
    if mode == "hoare-sem-no-urgent":  # a broken variant that ignores waiting signallers
        yield ("V", "mutex")
    elif (yield ("atomic", _get("urgentcount"))) > 0:
        yield ("V", "urgent")
    else:
        yield ("V", "mutex")


def leave(mode: str) -> Iterator[tuple]:
    yield ("atomic", _check("I at exit", _inv))
    yield ("atomic", _add("inside", -1))
    if mode.startswith("hoare-sem"):
        yield from _release_monitor(mode)
    else:
        yield ("unlock", "mon")


def mwait(mode: str, c: str, b: Pred) -> Iterator[tuple]:
    """c.wait, with the proof rule: {I} wait {I}, and also {B} after it under Hoare."""
    yield ("atomic", _check("I at wait", _inv))
    yield ("atomic", _event("wait"))
    yield ("atomic", _add("inside", -1))
    if mode.startswith("hoare-sem"):
        yield ("atomic", _add(c + ".count", 1))
        yield from _release_monitor(mode)
        yield ("P", c + ".sem")
        yield ("atomic", _add(c + ".count", -1))
    else:
        yield ("wait", c)
    yield ("atomic", _add("inside", 1))
    yield ("atomic", _event("resume"))
    yield ("atomic", _check("I after wait", _inv))
    if mode == "mesa":
        if not (yield ("atomic", b)):
            yield ("atomic", _flag("B false after wait"))
    else:
        yield ("atomic", _check("B after wait", b))


def msignal(mode: str, c: str, b: Pred) -> Iterator[tuple]:
    """c.signal; under Hoare semantics the rule is {I and B} signal {I}."""
    yield ("atomic", _check("I at signal", _inv))
    yield ("atomic", _event("signal"))
    if mode != "mesa":
        yield ("atomic", _check("B at signal", b))
    if mode.startswith("hoare-sem"):
        yield ("atomic", _add("urgentcount", 1))
        if (yield ("atomic", _get(c + ".count"))) > 0:
            yield ("atomic", _add("inside", -1))
            yield ("V", c + ".sem")
            yield ("P", "urgent")
            yield ("atomic", _add("inside", 1))
        yield ("atomic", _add("urgentcount", -1))
    elif mode == "hoare":
        yield ("atomic", _add("inside", -1))  # the waiter, if any, runs now
        yield ("signal", c)
        yield ("atomic", _add("inside", 1))
    else:
        yield ("signal", c)


def wait_for(mode: str, c: str, b: Pred, loop: bool) -> Iterator[tuple]:
    """`while not B: c.wait` (or `if not B: c.wait` when loop is False)."""
    if loop:
        while not (yield ("atomic", b)):
            yield from mwait(mode, c, b)
    elif not (yield ("atomic", b)):
        yield from mwait(mode, c, b)


def _new_monitor(mode: str, conds: tuple, invariant: Pred) -> Sim:
    s = Sim()
    s.v.update(inside=0, broken=None, I=invariant)
    s.v["B false after wait"] = False
    if mode.startswith("hoare-sem"):
        s.semaphore("mutex", 1)
        s.semaphore("urgent", 0)
        s.v["urgentcount"] = 0
        for c in conds:
            s.semaphore(c + ".sem", 0)
            s.v[c + ".count"] = 0
    else:
        s.mutex("mon")
        for c in conds:
            s.cond(c, "mon", "mesa" if mode == "mesa" else "hoare")
    return s


# Hoare's single resource monitor.

def _resource_inv(s: Sim) -> bool:
    return s.v["held"] == (1 if s.v["busy"] else 0)


def _nonbusy(s: Sim) -> bool:
    return not s.v["busy"]


def _take(me: str):
    def f(s: Sim) -> None:
        s.v["busy"] = True
        s.v["held"] += 1
        s.emit("acquire", me)
    return f


def _give(s: Sim) -> None:
    s.v["busy"] = False
    s.v["held"] -= 1


def acquire(mode: str, me: str, loop: bool) -> Iterator[tuple]:
    yield from enter(mode)
    yield from wait_for(mode, "nonbusy", _nonbusy, loop)
    yield ("atomic", _take(me))
    yield from leave(mode)


def release(mode: str, me: str) -> Iterator[tuple]:
    yield from enter(mode)
    yield ("atomic", _give)
    yield from msignal(mode, "nonbusy", _nonbusy)
    yield from leave(mode)


def user(sim: Sim, me: str, mode: str, rounds: int, loop: bool) -> Iterator[tuple]:
    for _ in range(rounds):
        yield from acquire(mode, me, loop)
        yield ("tick",)  # use the resource
        yield from release(mode, me)


def build_resource(mode: str, users: int = 3, rounds: int = 1, loop: bool = False) -> Sim:
    """`users` processes each acquire and release the resource `rounds` times."""
    s = _new_monitor(mode, ("nonbusy",), _resource_inv)
    s.v.update(busy=False, held=0)
    for i in range(users):
        s.spawn(f"u{i}", user, mode, rounds, loop)
    return s


# A bounded buffer monitor (Hoare's example, with if).

def _buffer_inv(s: Sim) -> bool:
    return 0 <= s.v["count"] <= s.v["capacity"]


def _nonfull(s: Sim) -> bool:
    return s.v["count"] < s.v["capacity"]


def _nonempty(s: Sim) -> bool:
    return s.v["count"] > 0


def _put(s: Sim) -> None:
    s.v["count"] += 1


def _get_item(s: Sim) -> None:
    s.v["count"] -= 1


def producer(sim: Sim, me: str, mode: str, items: int, loop: bool) -> Iterator[tuple]:
    for _ in range(items):
        yield from enter(mode)
        yield from wait_for(mode, "nonfull", _nonfull, loop)
        yield ("atomic", _put)
        yield from msignal(mode, "nonempty", _nonempty)
        yield from leave(mode)


def consumer(sim: Sim, me: str, mode: str, items: int, loop: bool) -> Iterator[tuple]:
    for _ in range(items):
        yield from enter(mode)
        yield from wait_for(mode, "nonempty", _nonempty, loop)
        yield ("atomic", _get_item)
        yield from msignal(mode, "nonfull", _nonfull)
        yield from leave(mode)


def build_buffer(mode: str, capacity: int = 1, producers: int = 1, consumers: int = 2,
                 items: int = 1, loop: bool = False) -> Sim:
    """Precondition: producers divides consumers * items."""
    total = consumers * items
    assert total % producers == 0
    s = _new_monitor(mode, ("nonfull", "nonempty"), _buffer_inv)
    s.v.update(count=0, capacity=capacity)
    for i in range(producers):
        s.spawn(f"p{i}", producer, mode, total // producers, loop)
    for i in range(consumers):
        s.spawn(f"c{i}", consumer, mode, items, loop)
    return s


def check(s: Sim) -> Optional[str]:
    """Mutual exclusion in the monitor, the proof rules, and the data invariants."""
    if s.v["inside"] > 1:
        return "two processes active in the monitor"
    if s.v["broken"]:
        return "proof rule broken: " + s.v["broken"]
    if "held" in s.v and s.v["held"] > 1:
        return "two processes hold the resource"
    if "count" in s.v and not _buffer_inv(s):
        return f"buffer count {s.v['count']} out of range"
    return None
