# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lock-ordering/. The authors are listed in prov/QFVDF2.jsonl.

"""Lock ordering in procsim: address order, a parent and child pair that
cannot be ordered (two phase with trylock), and a lock order validator in
the spirit of the Linux lock validator.

Each build function returns a fresh Sim. Precondition: none. Cost: each
exhaustive search here visits at most a few thousand states.
"""

from typing import Iterator, Optional

from procsim import Sim


# 1. Transfers between accounts, locked by address order.

def transfer(sim: Sim, me: str, src: int, dst: int, ordered: bool) -> Iterator[tuple]:
    """Move one unit from account src to account dst under both account locks.

    Precondition: src != dst. With ordered=True the locks are taken in
    increasing account number, whatever the direction of the transfer.
    """
    first, second = (min(src, dst), max(src, dst)) if ordered else (src, dst)
    yield ("lock", f"acct{first}")
    yield ("lock", f"acct{second}")

    def move(s: Sim) -> None:
        s.v["bal"][src] -= 1
        s.v["bal"][dst] += 1

    yield ("atomic", move)
    yield ("unlock", f"acct{second}")
    yield ("unlock", f"acct{first}")


def build_transfers(ordered: bool) -> Sim:
    s = Sim()
    s.v["bal"] = [5, 5, 5]
    for a in range(3):
        s.mutex(f"acct{a}")
    s.spawn("p", transfer, 0, 1, ordered)
    s.spawn("q", transfer, 1, 0, ordered)
    s.spawn("r", transfer, 2, 1, ordered)
    return s


# 2. A parent and a child. The order is parent before child, but one process
# starts from the child and only then learns that it needs the parent.

def top_down(sim: Sim, me: str) -> Iterator[tuple]:
    yield ("lock", "parent")
    yield ("lock", "child")
    yield ("atomic", lambda s: s.v.__setitem__("ops", s.v["ops"] + 1))
    yield ("unlock", "child")
    yield ("unlock", "parent")


def bottom_up_naive(sim: Sim, me: str) -> Iterator[tuple]:
    """Holds the child and waits for the parent: against the order."""
    yield ("lock", "child")
    yield ("lock", "parent")
    yield ("atomic", lambda s: s.v.__setitem__("ops", s.v["ops"] + 1))
    yield ("unlock", "parent")
    yield ("unlock", "child")


def bottom_up_trylock(sim: Sim, me: str) -> Iterator[tuple]:
    """Holds the child, tries the parent; on failure releases and takes both in order."""
    yield ("lock", "child")
    ok = yield ("trylock", "parent")
    if not ok:
        yield ("unlock", "child")
        yield ("lock", "parent")  # now in order: parent, then child
        yield ("lock", "child")
        # a real program re-checks here that the child still belongs to this parent
    yield ("atomic", lambda s: s.v.__setitem__("ops", s.v["ops"] + 1))
    yield ("unlock", "parent")
    yield ("unlock", "child")


def build_parent_child(fixed: bool) -> Sim:
    s = Sim()
    s.v["ops"] = 0
    s.mutex("parent")
    s.mutex("child")
    s.spawn("down", top_down)
    s.spawn("up", bottom_up_trylock if fixed else bottom_up_naive)
    return s


# 3. A lock order validator.

class LockOrderValidator:
    """Learn the order "a before b" each time b is taken while a is held, and
    report the first acquisition that closes a cycle in the learned order.

    It works on one trace of acquire and release events, so it can flag an
    order that could deadlock even in a run that did not deadlock.
    Cost: O(V + E) per acquisition for the cycle search.
    """

    def __init__(self) -> None:
        self.held: dict[str, list[str]] = {}
        self.after: dict[str, set[str]] = {}
        self.reports: list[tuple] = []

    def _reaches(self, s: str, t: str) -> bool:
        seen, stack = {s}, [s]
        while stack:
            v = stack.pop()
            if v == t:
                return True
            for w in self.after.get(v, ()):
                if w not in seen:
                    seen.add(w)
                    stack.append(w)
        return False

    def acquire(self, proc: str, lock: str) -> Optional[tuple]:
        """Record that proc took lock. Return (held, lock) if this closes a cycle."""
        found = None
        for h in self.held.get(proc, []):
            if lock not in self.after.get(h, set()):
                if self._reaches(lock, h):
                    found = (h, lock)
                    self.reports.append((proc, h, lock))
                    continue  # do not add the edge that closes the cycle
                self.after.setdefault(h, set()).add(lock)
        self.held.setdefault(proc, []).append(lock)
        return found

    def release(self, proc: str, lock: str) -> None:
        self.held[proc].remove(lock)


class Levels:
    """A lock hierarchy: a process may take a lock only if its level is
    above the levels of all locks it holds. Cost: O(1) per operation."""

    def __init__(self, level: dict[str, int]) -> None:
        self.level = level
        self.stack: dict[str, list[str]] = {}

    def acquire(self, proc: str, lock: str) -> None:
        st = self.stack.setdefault(proc, [])
        if st and self.level[lock] <= self.level[st[-1]]:
            raise RuntimeError(f"{proc} takes {lock} at level {self.level[lock]} while holding {st[-1]}")
        st.append(lock)

    def release(self, proc: str, lock: str) -> None:
        self.stack[proc].remove(lock)
