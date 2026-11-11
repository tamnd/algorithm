# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/opacity/. The authors are listed in prov/7CW7RJ.jsonl.
"""Brute-force checkers for opacity and serializability of small TM histories.

A history is a list of events (kind, tid, addr, value) with kind in
B (begin), R (read that returned value), W (write of value), T (commit
requested), C (committed) and A (aborted), as recorded by stm.History.
A transaction is committed (C), aborted (A), commit-pending (T but no C or
A yet) or live (none of these). To complete a history, a live transaction
becomes aborted, and a commit-pending one becomes committed or aborted.

final_state_opaque(h) asks for a completion of h and one sequential order of
all its transactions that respects real-time order (T before U when T ended
before U began) in which every read of every transaction, committed or not,
returns the last value written before it by the same transaction, or else
by the last committed transaction before it in the order. opaque(h) asks
this for every prefix of h (Guerraoui and Kapalka). strictly_serializable
and serializable look only at the committed transactions.

Precondition: at most about 12 transactions. Cost: exponential in the
number of transactions t; the search visits each pair (set of placed
transactions, memory state) at most once, and each visit costs O(t * e)
for e events.
"""

from __future__ import annotations

from itertools import permutations, product
from typing import Any

Event = tuple[str, Any, int, Any]


def transactions(h: list[Event]) -> dict[Any, dict]:
    """Group the events of h by transaction."""
    txs: dict[Any, dict] = {}
    for i, (kind, tid, a, v) in enumerate(h):
        t = txs.setdefault(tid, {"ops": [], "status": "L", "first": i, "last": None})
        if kind in ("R", "W"):
            t["ops"].append((kind, a, v))
        elif kind == "T":
            t["status"] = "P"
        elif kind in ("C", "A"):
            t["status"] = kind
            t["last"] = i
    return txs


def _runs(t: dict, state: dict[int, Any]) -> bool:
    local: dict[int, Any] = {}
    for kind, a, v in t["ops"]:
        if kind == "R":
            if local.get(a, state.get(a, 0)) != v:
                return False
        else:
            local[a] = v
    return True


def _apply(t: dict, state: dict[int, Any], commit: bool) -> dict[int, Any]:
    if not commit:
        return state
    new = dict(state)
    for kind, a, v in t["ops"]:
        if kind == "W":
            new[a] = v
    return new


def _choices(t: dict) -> tuple[bool, ...]:
    return {"C": (True,), "P": (True, False)}.get(t["status"], (False,))


def _precedes(t: dict, u: dict) -> bool:
    return t["last"] is not None and t["last"] < u["first"]


def _search(txs: dict[Any, dict], init: dict[int, Any], real_time: bool) -> bool:
    ids = list(txs)
    pred = {u: {t for t in ids if real_time and t != u and _precedes(txs[t], txs[u])} for u in ids}
    seen: set[tuple] = set()
    stack = [(frozenset(), dict(init))]
    while stack:
        placed, state = stack.pop()
        if len(placed) == len(ids):
            return True
        key = (placed, frozenset(state.items()))
        if key in seen:
            continue
        seen.add(key)
        for u in ids:
            if u in placed or not pred[u] <= placed:
                continue
            if _runs(txs[u], state):
                for c in _choices(txs[u]):
                    stack.append((placed | {u}, _apply(txs[u], state, c)))
    return False


def final_state_opaque(h: list[Event], init: dict[int, Any] | None = None) -> bool:
    """True if all transactions of h, aborted and live ones included, fit one legal serial order."""
    return _search(transactions(h), init or {}, True)


def opaque(h: list[Event], init: dict[int, Any] | None = None) -> bool:
    """True if every prefix of h is final-state opaque."""
    return all(final_state_opaque(h[:i], init) for i in range(1, len(h) + 1))


def _committed(h: list[Event]) -> dict[Any, dict]:
    return {t: d for t, d in transactions(h).items() if d["status"] == "C"}


def strictly_serializable(h: list[Event], init: dict[int, Any] | None = None) -> bool:
    """True if the committed transactions fit a legal serial order that respects real time."""
    return _search(_committed(h), init or {}, True)


def serializable(h: list[Event], init: dict[int, Any] | None = None) -> bool:
    """True if the committed transactions fit some legal serial order."""
    return _search(_committed(h), init or {}, False)


def final_state_opaque_naive(h: list[Event], init: dict[int, Any] | None = None) -> bool:
    """The same test as final_state_opaque, by trying every completion and permutation."""
    txs = transactions(h)
    ids = list(txs)
    for order in permutations(ids):
        pos = {t: i for i, t in enumerate(order)}
        if any(_precedes(txs[t], txs[u]) and pos[t] > pos[u] for t in ids for u in ids if t != u):
            continue
        for commits in product(*(_choices(txs[t]) for t in order)):
            state = dict(init or {})
            ok = True
            for t, c in zip(order, commits):
                if not _runs(txs[t], state):
                    ok = False
                    break
                state = _apply(txs[t], state, c)
            if ok:
                return True
    return False
