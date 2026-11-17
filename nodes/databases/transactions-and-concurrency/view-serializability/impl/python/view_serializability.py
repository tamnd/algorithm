# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/view-serializability/. The authors are listed in prov/S03CR7.jsonl.

"""View serializability by brute force over all serial orders.

A schedule is a list of actions (op, txn, item), op "r" or "w", of committed
transactions. Each action is named by (txn, k): it is the k-th action of txn.
The test is exponential in the number of transactions, as it must be unless
P = NP: deciding view serializability is NP-complete (Papadimitriou 1979).
"""

import itertools
from collections import Counter

Action = tuple[str, int, str]
Name = tuple[int, int]


def parse(text: str) -> list[Action]:
    """Parse "r1(x) w2(x)" into actions."""
    return [(t[0], int(t[1 : t.index("(")]), t[t.index("(") + 1 : -1]) for t in text.split()]


def named(s: list[Action]) -> list[tuple[Action, Name]]:
    count: Counter = Counter()
    out = []
    for p in s:
        count[p[1]] += 1
        out.append((p, (p[1], count[p[1]])))
    return out


def reads_from(s: list[Action]) -> set[tuple[Name, Name | None]]:
    """Pairs (read, write): the read sees the value of that write.

    None stands for the initial value (the write of the virtual T0).
    """
    last: dict[str, Name] = {}
    out = set()
    for (op, _, x), name in named(s):
        if op == "r":
            out.add((name, last.get(x)))
        else:
            last[x] = name
    return out


def final_writes(s: list[Action]) -> dict[str, Name]:
    """For each written item, the write that leaves its final value."""
    last: dict[str, Name] = {}
    for (op, _, x), name in named(s):
        if op == "w":
            last[x] = name
    return last


def view_equivalent(s1: list[Action], s2: list[Action]) -> bool:
    """Same actions, same reads-from relation and same final writes."""
    return (
        Counter(s1) == Counter(s2)
        and reads_from(s1) == reads_from(s2)
        and final_writes(s1) == final_writes(s2)
    )


def serial(s: list[Action], order) -> list[Action]:
    return [p for t in order for p in s if p[1] == t]


def view_serial_order(s: list[Action]) -> tuple[int, ...] | None:
    """The first serial order (in lexicographic order) view equivalent to s, or None."""
    for order in itertools.permutations(sorted({p[1] for p in s})):
        if view_equivalent(s, serial(s, order)):
            return order
    return None


def is_view_serializable(s: list[Action]) -> bool:
    return view_serial_order(s) is not None


def has_blind_write(s: list[Action]) -> bool:
    """True if some w_i(x) is not preceded by r_i(x) in the same transaction."""
    read: set[tuple[int, str]] = set()
    for op, t, x in s:
        if op == "r":
            read.add((t, x))
        elif (t, x) not in read:
            return True
    return False


def herbrand(s: list[Action]) -> tuple[dict, dict]:
    """Run s with symbolic values.

    A write stores the term (txn, k, values read by txn so far), so the value
    depends on everything the transaction has read. Return the value seen by
    each read and the final value of each item.
    """
    db: dict[str, object] = {}
    seen: dict[int, list] = {}
    reads: dict[Name, object] = {}
    for (op, t, x), name in named(s):
        if op == "r":
            v = db.get(x, ("init", x))
            reads[name] = v
            seen.setdefault(t, []).append(v)
        else:
            db[x] = (name, tuple(seen.get(t, [])))
    return reads, db
