# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/consistency-models/. The authors are listed in prov/RP1X08.jsonl.

"""Brute force checkers for four consistency models of read/write registers.

A history is a list of complete operations. Each operation names its process,
its kind ("w" or "r"), its register, its value, and the real times of its
invocation and its response. The operations of one process appear in the list
in program order. Every register starts with the value 0, and each written
value is unique for its register (the usual assumption that makes the
writes-into relation a function).

The checkers search for a legal serialization: a total order of a set of
operations in which every read returns the value of the last write to its
register before it (or 0). They differ only in which operations must be
ordered and which order constraints apply:

  linearizable   all operations; program order and real-time order
  sequential     all operations; program order
  causal         for each process p, its operations and all writes;
                 the causality order (program order plus writes-into, closed)
  pram           for each process p, its operations and all writes;
                 program order only

The search is a depth first search with memoization on the set of placed
operations and the register values. It is exponential in the worst case and
is meant for histories of up to about 10 operations.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Op:
    """One complete operation of a history."""

    proc: int
    kind: str  # "w" or "r"
    var: str
    val: int
    inv: float = 0.0
    res: float = 0.0


History = list[Op]


def w(proc: int, var: str, val: int, inv: float = 0.0, res: float = 0.0) -> Op:
    """A write of val to var by proc."""
    return Op(proc, "w", var, val, inv, res)


def r(proc: int, var: str, val: int, inv: float = 0.0, res: float = 0.0) -> Op:
    """A read of var by proc that returned val."""
    return Op(proc, "r", var, val, inv, res)


def program_order(h: History) -> set[tuple[int, int]]:
    """Pairs (i, j) such that op i comes before op j in the same process."""
    pairs = set()
    for i in range(len(h)):
        for j in range(i + 1, len(h)):
            if h[i].proc == h[j].proc:
                pairs.add((i, j))
    return pairs


def real_time_order(h: History) -> set[tuple[int, int]]:
    """Pairs (i, j) such that op i responds before op j is invoked."""
    return {(i, j) for i in range(len(h)) for j in range(len(h)) if h[i].res < h[j].inv}


def writes_into(h: History) -> Optional[set[tuple[int, int]]]:
    """Pairs (write, read) where the read returns the value of that write.

    Returns None when some read returns a nonzero value that no write wrote.
    """
    pairs = set()
    for j, op in enumerate(h):
        if op.kind == "r" and op.val != 0:
            src = [i for i, o in enumerate(h) if o.kind == "w" and o.var == op.var and o.val == op.val]
            if not src:
                return None
            pairs.add((src[0], j))
    return pairs


def transitive_closure(n: int, pairs: set[tuple[int, int]]) -> Optional[set[tuple[int, int]]]:
    """The transitive closure, or None when the relation has a cycle."""
    reach = [[False] * n for _ in range(n)]
    for i, j in pairs:
        reach[i][j] = True
    for k in range(n):
        for i in range(n):
            if reach[i][k]:
                for j in range(n):
                    if reach[k][j]:
                        reach[i][j] = True
    if any(reach[i][i] for i in range(n)):
        return None
    return {(i, j) for i in range(n) for j in range(n) if reach[i][j]}


def legal_serialization(h: History, ids: list[int], before: set[tuple[int, int]]) -> Optional[list[int]]:
    """A legal total order of the ops in ids that respects before, or None."""
    idset = set(ids)
    preds = {i: {a for (a, b) in before if b == i and a in idset} for i in ids}
    regs = sorted({h[i].var for i in ids})
    seen: set[tuple[frozenset[int], tuple[int, ...]]] = set()
    order: list[int] = []

    def dfs(placed: frozenset[int], vals: dict[str, int]) -> bool:
        if len(placed) == len(ids):
            return True
        key = (placed, tuple(vals[x] for x in regs))
        if key in seen:
            return False
        seen.add(key)
        for i in ids:
            if i in placed or not preds[i] <= placed:
                continue
            op = h[i]
            if op.kind == "r" and vals[op.var] != op.val:
                continue
            nvals = dict(vals)
            if op.kind == "w":
                nvals[op.var] = op.val
            order.append(i)
            if dfs(placed | {i}, nvals):
                return True
            order.pop()
        return False

    if dfs(frozenset(), {x: 0 for x in regs}):
        return list(order)
    return None


def is_linearizable(h: History) -> bool:
    """Herlihy and Wing: a legal order that respects real time (and so program order)."""
    before = program_order(h) | real_time_order(h)
    return legal_serialization(h, list(range(len(h))), before) is not None


def is_sequential(h: History) -> bool:
    """Lamport: a legal order of all operations that respects program order."""
    return legal_serialization(h, list(range(len(h))), program_order(h)) is not None


def _per_process(h: History, before: set[tuple[int, int]]) -> bool:
    for p in sorted({op.proc for op in h}):
        ids = [i for i, op in enumerate(h) if op.proc == p or op.kind == "w"]
        if legal_serialization(h, ids, before) is None:
            return False
    return True


def is_causal(h: History) -> bool:
    """Ahamad et al.: each process has a legal view of its ops and all writes
    that respects the causality order."""
    wi = writes_into(h)
    if wi is None:
        return False
    causality = transitive_closure(len(h), program_order(h) | wi)
    if causality is None:
        return False
    return _per_process(h, causality)


def is_pram(h: History) -> bool:
    """Lipton and Sandberg: each process has a legal view of its ops and all
    writes that respects the program order of every process."""
    return _per_process(h, program_order(h))


def classify(h: History) -> dict[str, bool]:
    """Membership of h in each of the four models."""
    return {
        "linearizable": is_linearizable(h),
        "sequential": is_sequential(h),
        "causal": is_causal(h),
        "pram": is_pram(h),
    }


# The separating histories of the page. Each one is in the weaker model and
# not in the stronger one.

# Sequential but not linearizable: the read starts after the write ends.
SEQ_NOT_LIN: History = [w(1, "x", 1, 0, 1), r(2, "x", 0, 2, 3)]

# Causal but not sequential: two concurrent writes seen in two orders.
CAUSAL_NOT_SEQ: History = [
    w(1, "x", 1),
    w(2, "x", 2),
    r(3, "x", 1), r(3, "x", 2),
    r(4, "x", 2), r(4, "x", 1),
]

# Causal but not sequential, the store buffer pattern.
STORE_BUFFER: History = [w(1, "x", 1), r(1, "y", 0), w(2, "y", 1), r(2, "x", 0)]

# PRAM but not causal: w(y)1 depends on w(x)1 through a read, and process 3
# sees the effect without the cause.
PRAM_NOT_CAUSAL: History = [
    w(1, "x", 1),
    r(2, "x", 1), w(2, "y", 1),
    r(3, "y", 1), r(3, "x", 0),
]

# Not PRAM: two writes of one process seen in the wrong order.
NOT_PRAM: History = [w(1, "x", 1), w(1, "x", 2), r(2, "x", 2), r(2, "x", 1)]
