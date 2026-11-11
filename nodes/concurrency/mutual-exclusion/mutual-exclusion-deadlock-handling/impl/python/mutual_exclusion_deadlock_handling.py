# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mutual-exclusion-deadlock-handling/. The authors are listed in prov/Z43BNF.jsonl.

"""Wait-die and wound-wait (Rosenkrantz, Stearns and Lewis 1978) in procsim.

Transactions take exclusive locks one at a time and release them all at
commit or abort. Each transaction has a fixed timestamp; a smaller one is
older. An aborted transaction restarts with the same timestamp.

  rule "wait"        always wait (no deadlock handling; can deadlock)
  rule "wait-die"    an older requester waits; a younger one dies (aborts)
  rule "wound-wait"  an older requester wounds (aborts) the holder; a younger one waits

Precondition of build: distinct timestamps, and each transaction lists
distinct locks. Cost: each exhaustive search in the tests visits at most a
few thousand states.
"""

from typing import Callable, Iterator

from procsim import Sim


def _request(me: str, lock: str, rule: str) -> Callable[[Sim], str]:
    def f(s: Sim) -> str:
        v = s.v
        v["waiting"][me] = None
        if v["wounded"][me]:  # @line L1
            return "dead"
        if v["owner"][lock] is None:  # @line L2
            v["owner"][lock] = me
            return "got"
        holder = v["owner"][lock]  # @line L3
        older = v["ts"][me] < v["ts"][holder]
        if rule == "wait-die" and not older:  # @line L4
            return "die"
        if rule == "wound-wait" and older:  # @line L5
            v["wounded"][holder] = True
        v["waiting"][me] = lock  # @line L6
        return "wait"
    return f


def _release_all(s: Sim, me: str) -> None:
    """Free every lock of me. A freed lock goes to its oldest live waiter, as in a
    lock manager; under wait-die, the other waiters that are younger than the new
    holder must then die."""
    v = s.v
    v["waiting"][me] = None
    for lock, holder in v["owner"].items():  # @line L7
        if holder != me:
            continue
        waiters = [t for t, w in v["waiting"].items() if w == lock and not v["wounded"][t]]
        if not waiters:  # @line L8
            v["owner"][lock] = None
            continue
        new = min(waiters, key=v["ts"].__getitem__)
        v["owner"][lock] = new
        v["waiting"][new] = None
        if v["rule"] == "wait-die":  # @line L9
            for t in waiters:
                if v["ts"][t] > v["ts"][new]:
                    v["wounded"][t] = True  # it would wait for an older holder: it dies


def _commit(me: str) -> Callable[[Sim], bool]:
    def f(s: Sim) -> bool:
        if s.v["wounded"][me]:  # @line L10
            return False
        _release_all(s, me)
        s.emit("commit", me)
        return True
    return f


def _abort(me: str) -> Callable[[Sim], None]:
    def f(s: Sim) -> None:
        _release_all(s, me)  # @line L11
        s.v["wounded"][me] = False
        s.emit("abort", me)
    return f


def transaction(sim: Sim, me: str, locks: list[str], rule: str) -> Iterator[tuple]:
    """Take the locks in the given order, then commit; on abort, restart."""
    while True:
        aborted = False
        for lock in locks:
            r = yield ("atomic", _request(me, lock, rule))
            if r == "wait":  # the lock manager hands the lock over, or we are aborted
                yield ("await", lambda s, lock=lock: s.v["owner"][lock] == me or s.v["wounded"][me])
                r = "got" if sim.v["owner"][lock] == me and not sim.v["wounded"][me] else "dead"
            if r != "got":
                aborted = True
                break
        if not aborted:
            ok = yield ("atomic", _commit(me))
            if ok:
                return
        yield ("atomic", _abort(me))


def build(programs: dict[str, list[str]], ts: dict[str, int], rule: str) -> Sim:
    s = Sim()
    locks = sorted({x for ls in programs.values() for x in ls})
    s.v["owner"] = {x: None for x in locks}
    s.v["waiting"] = {t: None for t in programs}
    s.v["wounded"] = {t: False for t in programs}
    s.v["ts"] = dict(ts)
    s.v["rule"] = rule
    for t in sorted(programs):
        s.spawn(t, transaction, programs[t], rule)
    return s


def wait_edges(s: Sim) -> list[tuple[str, str]]:
    """Edges t -> holder for each transaction t that is blocked on a lock."""
    out = []
    for t in s.blocked():
        lock = s.v["waiting"][t]
        if lock is not None and s.v["owner"][lock] not in (None, t):
            out.append((t, s.v["owner"][lock]))
    return out
