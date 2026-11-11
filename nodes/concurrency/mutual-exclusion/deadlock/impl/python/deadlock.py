# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deadlock/. The authors are listed in prov/Y272XW.jsonl.

"""Small models of resource and communication deadlock, run in procsim.

Each build function returns a fresh Sim. Precondition: none. Cost: each
exhaustive search below visits fewer than 100 states.
"""

from typing import Iterator

from procsim import Sim, explore, replay


def two_locks(sim: Sim, me: str, first: str, second: str) -> Iterator[tuple]:
    """Take two mutexes in the given order, then release them."""
    yield ("lock", first)
    yield ("lock", second)
    yield ("unlock", second)
    yield ("unlock", first)


def build_opposite_order() -> Sim:
    """p takes A then B, q takes B then A: the classic deadlock."""
    s = Sim()
    s.mutex("A")
    s.mutex("B")
    s.spawn("p", two_locks, "A", "B")
    s.spawn("q", two_locks, "B", "A")
    return s


def build_same_order() -> Sim:
    """Both take A then B: no deadlock is reachable."""
    s = Sim()
    s.mutex("A")
    s.mutex("B")
    s.spawn("p", two_locks, "A", "B")
    s.spawn("q", two_locks, "A", "B")
    return s


def receive_first(sim: Sim, me: str, inbox: str, outbox: str) -> Iterator[tuple]:
    """Wait for a message, then send one."""
    x = yield ("recv", inbox)
    yield ("send", outbox, x)


def send_first(sim: Sim, me: str, inbox: str, outbox: str) -> Iterator[tuple]:
    """Send a message, then wait for one."""
    yield ("send", outbox, me)
    yield ("recv", inbox)


def build_communication(fixed: bool) -> Sim:
    """Two processes that each wait for a message from the other.

    With fixed=False both receive first: a communication deadlock with no
    resource at all. With fixed=True the process p sends first.
    """
    s = Sim()
    s.channel("to_p")
    s.channel("to_q")
    s.spawn("p", send_first if fixed else receive_first, "to_p", "to_q")
    s.spawn("q", receive_first, "to_q", "to_p")
    return s


def relock(sim: Sim, me: str) -> Iterator[tuple]:
    """Lock a non-reentrant mutex twice: a deadlock of one process."""
    yield ("lock", "A")
    yield ("lock", "A")


def build_self_deadlock() -> Sim:
    s = Sim()
    s.mutex("A")
    s.spawn("p", relock)
    return s


def deadlocked_states(build) -> list[Sim]:
    """Every reachable state in which no process can step and some has not finished."""
    return [replay(build, list(d)) for d in explore(build).deadlocks]
