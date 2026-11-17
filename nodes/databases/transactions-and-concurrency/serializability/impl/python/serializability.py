# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/serializability/. The authors are listed in prov/YQV7PJ.jsonl.

"""Serializability and recoverability classes of a schedule, by definition.

A schedule is a list of actions (op, txn, item): op "r" or "w" with an item,
or "c" (commit) or "a" (abort) with item None. The serializability tests use
brute force over all serial orders of the committed transactions.
"""

import itertools
from collections import Counter

Action = tuple[str, int, str | None]


def parse(text: str) -> list[Action]:
    """Parse "r1(x) w2(x) c1 a2" into actions."""
    out: list[Action] = []
    for t in text.split():
        if "(" in t:
            out.append((t[0], int(t[1 : t.index("(")]), t[t.index("(") + 1 : -1]))
        else:
            out.append((t[0], int(t[1:]), None))
    return out


def committed_projection(s: list[Action]) -> list[Action]:
    done = {t for op, t, _ in s if op == "c"}
    return [p for p in s if p[0] in "rw" and p[1] in done]


def serial(s: list[Action], order) -> list[Action]:
    return [p for t in order for p in s if p[1] == t]


def _orders(s: list[Action]):
    return itertools.permutations(sorted({p[1] for p in s}))


def _herbrand(s: list[Action]) -> tuple[dict, dict]:
    """Symbolic run: a write stores (txn, k, values txn has read so far)."""
    db: dict = {}
    seen: dict = {}
    count: Counter = Counter()
    reads = {}
    for op, t, x in s:
        count[t] += 1
        if op == "r":
            v = db.get(x, ("init", x))
            reads[(t, count[t])] = v
            seen.setdefault(t, []).append(v)
        else:
            db[x] = (t, count[t], tuple(seen.get(t, [])))
    return reads, db


def _conflict_pairs(s: list[Action]) -> set:
    count: Counter = Counter()
    tagged = []
    for p in s:
        count[p[1]] += 1
        tagged.append((p, count[p[1]]))
    return {
        (a, b)
        for i, a in enumerate(tagged)
        for b in tagged[i + 1 :]
        if a[0][1] != b[0][1] and a[0][2] == b[0][2] and "w" in (a[0][0], b[0][0])
    }


def final_state_serializable(s: list[Action]) -> bool:
    """Same final state as some serial schedule, for every interpretation."""
    c = committed_projection(s)
    return any(_herbrand(c)[1] == _herbrand(serial(c, o))[1] for o in _orders(c))


def view_serializable(s: list[Action]) -> bool:
    """Every read sees the same value and the final state is the same."""
    c = committed_projection(s)
    return any(_herbrand(c) == _herbrand(serial(c, o)) for o in _orders(c))


def conflict_serializable(s: list[Action]) -> bool:
    c = committed_projection(s)
    return any(_conflict_pairs(c) == _conflict_pairs(serial(c, o)) for o in _orders(c))


def reads_from(s: list[Action]) -> list[tuple[int, int, int]]:
    """Triples (reader, writer, position of the read) with reader != writer.

    A read r_i(x) reads from the last earlier write of x whose transaction had
    not aborted before the read (an abort undoes the writes of its transaction).
    """
    aborted: set[int] = set()
    writes: dict[str, list[int]] = {}
    out = []
    for pos, (op, t, x) in enumerate(s):
        if op == "a":
            aborted.add(t)
        elif op == "w":
            writes.setdefault(x, []).append(t)
        elif op == "r":
            live = [w for w in writes.get(x, []) if w not in aborted]
            if live and live[-1] != t:
                out.append((t, live[-1], pos))
    return out


def _end(s: list[Action]) -> dict[int, int]:
    return {t: pos for pos, (op, t, _) in enumerate(s) if op in "ca"}


def recoverable(s: list[Action]) -> bool:
    """RC: if Ti reads from Tj and Ti commits, then Tj commits before Ti commits."""
    commit = {t: pos for pos, (op, t, _) in enumerate(s) if op == "c"}
    return all(i not in commit or (j in commit and commit[j] < commit[i]) for i, j, _ in reads_from(s))


def avoids_cascading_aborts(s: list[Action]) -> bool:
    """ACA: a transaction reads only values written by committed transactions."""
    commit = {t: pos for pos, (op, t, _) in enumerate(s) if op == "c"}
    return all(j in commit and commit[j] < pos for _, j, pos in reads_from(s))


def strict(s: list[Action]) -> bool:
    """ST: no item written by an active transaction is read or written by another."""
    end = _end(s)
    for i, (op, t, x) in enumerate(s):
        if op != "w":
            continue
        stop = end.get(t, len(s))
        for op2, t2, x2 in s[i + 1 : stop]:
            if op2 in "rw" and x2 == x and t2 != t:
                return False
    return True
