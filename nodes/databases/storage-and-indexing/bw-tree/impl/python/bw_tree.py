# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bw-tree/. The authors are listed in prov/R4MGVH.jsonl.

"""Bw-tree of Levandoski, Lomet and Sengupta (ICDE 2013), as a simulation.

Pages are named by page ids (pids). A mapping table M maps a pid to the head
of a chain: zero or more delta records in front of a base page. Every change
is one compare-and-swap (CAS) on one slot of M, so no thread ever waits.

Threads are Python generators. Each operation reads a chain head, yields to
the scheduler, and then tries its CAS, so other threads can change the page
in between, as on a real machine. A seeded scheduler picks the thread that
runs next. The structure modifications are the two-step split of the paper
(a split delta on the page, then an index term delta on its parent) and
consolidation. Any thread that sees a half-done split helps to finish it.

Not modelled: page merges, the flash log of the LLAMA store and epoch-based
memory reclamation (Python's garbage collector frees unreachable chains).
"""

import math
import random
from bisect import bisect_right
from typing import Dict, Generator, List, Optional, Tuple

NEG, POS = -math.inf, math.inf


# ----- pages and deltas -----

class Base:
    """A base page. In a leaf, vals[i] is the value of keys[i]. In an inner
    page, keys[i] is the low key of the child kids[i], and keys[0] == low."""

    __slots__ = ("level", "keys", "vals", "kids", "low", "high", "right")

    def __init__(self, level, keys, vals_or_kids, low, high, right):
        self.level = level
        self.keys = keys
        self.vals = vals_or_kids if level == 0 else None
        self.kids = vals_or_kids if level > 0 else None
        self.low, self.high, self.right = low, high, right


class Delta:
    __slots__ = ("kind", "key", "val", "nxt", "base", "length")

    def __init__(self, kind: str, key, val, nxt):
        self.kind = kind          # "ins", "del", "split" or "term"
        self.key = key            # the key, or the separator of a split or an index term
        self.val = val            # the value, the new pid of a split, or (pid, high) of an index term
        self.nxt = nxt
        self.base = nxt if isinstance(nxt, Base) else nxt.base
        self.length = 1 if isinstance(nxt, Base) else nxt.length + 1


def chain_length(h) -> int:
    return 0 if isinstance(h, Base) else h.length


def base_of(h) -> Base:
    return h if isinstance(h, Base) else h.base


def bounds(h) -> Tuple[object, object, Optional[int]]:
    """(low, high, right) of the page whose chain starts at h."""
    b = base_of(h)
    d = h
    while isinstance(d, Delta):
        if d.kind == "split":          # the newest split is the tightest
            return b.low, d.key, d.val
        d = d.nxt
    return b.low, b.high, b.right


def leaf_find(h, k):
    """Search one leaf chain for k: (found, value). Assumes low <= k < high."""
    d = h
    while isinstance(d, Delta):
        if d.key == k and d.kind == "ins":
            return True, d.val
        if d.key == k and d.kind == "del":
            return False, None
        d = d.nxt
    i = bisect_right(d.keys, k) - 1
    if i >= 0 and d.keys[i] == k:
        return True, d.vals[i]
    return False, None


def inner_route(h, k) -> int:
    """The child pid for k in one inner chain. Assumes low <= k < high."""
    d = h
    while isinstance(d, Delta):
        if d.kind == "term":
            q, hi = d.val
            if d.key <= k < hi:
                return q
        d = d.nxt
    return d.kids[bisect_right(d.keys, k) - 1]


def logical(h) -> Tuple[Base, List, List]:
    """The contents of a chain as sorted keys and values (or kids)."""
    b = base_of(h)
    low, high, right = bounds(h)
    deltas = []
    d = h
    while isinstance(d, Delta):
        deltas.append(d)
        d = d.nxt
    if b.level == 0:
        content = dict(zip(b.keys, b.vals))
        for d in reversed(deltas):
            if d.kind == "ins":
                content[d.key] = d.val
            elif d.kind == "del":
                content.pop(d.key, None)
    else:
        content = dict(zip(b.keys, b.kids))
        for d in reversed(deltas):
            if d.kind == "term":
                content[d.key] = d.val[0]
    keys = sorted(x for x in content if low <= x < high)
    return Base(b.level, keys, [content[x] for x in keys], low, high, right), keys, [content[x] for x in keys]


# ----- the tree -----

ROOT = 0


class BwTree:
    def __init__(self, max_leaf: int = 4, max_inner: int = 4, max_chain: int = 3):
        self.M: Dict[int, object] = {ROOT: Base(0, [], [], NEG, POS, None)}
        self.next_pid = 1
        self.max_leaf, self.max_inner, self.max_chain = max_leaf, max_inner, max_chain
        self.stats = {"cas_ok": 0, "cas_fail": 0, "help": 0, "split": 0, "consolidate": 0, "root_split": 0}

    def cas(self, pid: int, expected, new) -> bool:
        if self.M[pid] is expected:
            self.M[pid] = new
            self.stats["cas_ok"] += 1
            return True
        self.stats["cas_fail"] += 1
        return False

    def new_pid(self, page) -> int:
        pid = self.next_pid
        self.next_pid += 1
        self.M[pid] = page         # not reachable yet, so no CAS is needed
        return pid

    # ----- traversal -----

    def _find(self, k, level: int = 0) -> Generator:
        """Walk from the root to the page at the given level whose range holds k.

        Returns (pid, parent pid, head). Helps to post missing index terms."""
        pid, parent, came_down = ROOT, None, True                    # @line L8
        while True:
            h = self.M[pid]                                          # @line L9
            yield "read"
            low, high, right = bounds(h)                             # @line L10
            if k >= high:                                            # @line L10
                if came_down and parent is not None:
                    yield from self._help_along(parent, high, right)  # @line L11
                pid, came_down = right, False                        # @line L11
                continue
            b = base_of(h)
            if b.level == level:                                     # @line L12
                return pid, parent, h                                # @line L12
            parent, pid, came_down = pid, inner_route(h, k), True    # @line L13

    def _help_along(self, parent: int, sep, q: int) -> Generator:
        """Post the index term (sep -> q) on the parent if it is missing."""
        while True:
            g = self.M[parent]                                       # @line L19
            low, high, _ = bounds(g)
            qh = self.M[q]
            if base_of(g).level != base_of(qh).level + 1 or not (low <= sep < high):
                return                                               # @line L19
            if inner_route(g, sep) == q:                             # @line L19
                return
            d = Delta("term", sep, (q, bounds(qh)[1]), g)
            yield "cas"
            self.stats["help"] += 1
            if self.cas(parent, g, d):                               # @line L20
                return

    # ----- operations (generators) -----

    def lookup(self, k) -> Generator:
        pid, _, h = yield from self._find(k)
        return leaf_find(h, k)[1]

    def upsert(self, k, v) -> Generator:
        """Insert or update k; return the old value or None."""
        return (yield from self._update(k, "ins", v))

    def delete(self, k) -> Generator:
        """Delete k; return the old value or None."""
        return (yield from self._update(k, "del", None))

    def _update(self, k, kind, v) -> Generator:
        while True:
            pid, parent, h = yield from self._find(k)                # @line L1
            found, old = leaf_find(h, k)                             # @line L2
            if kind == "del" and not found:                          # @line L3
                return None                                          # @line L3
            d = Delta(kind, k, v, h)                                 # @line L4
            yield "cas"
            if self.cas(pid, h, d):                                  # @line L5
                break
        yield from self._maintain(pid, parent)                       # @line L6
        return old

    def _maintain(self, pid: int, parent: Optional[int]) -> Generator:
        h = self.M[pid]
        if chain_length(h) > self.max_chain:                         # @line L6
            yield from self._consolidate(pid)
        page, keys, _ = logical(self.M[pid])
        limit = self.max_leaf if page.level == 0 else self.max_inner
        if len(keys) > limit:                                        # @line L7
            ok = yield from self._split(pid, parent)
            if ok and parent is not None:
                yield from self._maintain_parent(parent)

    def _maintain_parent(self, parent: int) -> Generator:
        # The parent's own parent is found by a new walk from the root.
        g = self.M[parent]
        b = base_of(g)
        if parent == ROOT:
            yield from self._maintain(ROOT, None)
            return
        lo = bounds(g)[0]
        found = yield from self._find(lo, b.level)
        if found[0] == parent:
            yield from self._maintain(parent, found[1])

    def _consolidate(self, pid: int) -> Generator:
        h = self.M[pid]                                              # @line L14
        page, _, _ = logical(h)                                      # @line L14
        yield "cas"
        if self.cas(pid, h, page):                                   # @line L15
            self.stats["consolidate"] += 1

    def _split(self, pid: int, parent: Optional[int]) -> Generator:
        h = self.M[pid]                                              # @line L16
        page, keys, items = logical(h)
        limit = self.max_leaf if page.level == 0 else self.max_inner
        if len(keys) <= limit:
            return False
        mid = len(keys) // 2
        sep = keys[mid]                                              # @line L16
        if pid == ROOT:
            # A root split makes two new pages and swaps the root in one CAS.
            r = Base(page.level, keys[mid:], items[mid:], sep, POS, None)
            rp = self.new_pid(r)
            l = Base(page.level, keys[:mid], items[:mid], NEG, sep, rp)
            lp = self.new_pid(l)
            root = Base(page.level + 1, [NEG, sep], [lp, rp], NEG, POS, None)
            yield "cas"
            if self.cas(ROOT, h, root):
                self.stats["root_split"] += 1
                return True
            return False
        q = Base(page.level, keys[mid:], items[mid:], sep, page.high, page.right)
        qp = self.new_pid(q)                                         # @line L16
        d = Delta("split", sep, qp, h)
        yield "cas"
        if not self.cas(pid, h, d):                                  # @line L17
            return False                                             # the new page is dropped
        self.stats["split"] += 1
        if parent is not None:
            yield from self._help_along(parent, sep, qp)             # @line L18
        return True

    # ----- checks (not concurrent) -----

    def items(self) -> List[Tuple[object, object]]:
        """All (key, value) pairs, by a walk along the leaf level."""
        pid = ROOT
        while base_of(self.M[pid]).level > 0:
            pid = inner_route(self.M[pid], NEG)
        out = []
        prev_high = NEG
        while pid is not None:
            page, keys, vals = logical(self.M[pid])
            assert page.low == prev_high, "the leaf level is not contiguous"
            out.extend(zip(keys, vals))
            prev_high = page.high
            pid = page.right
        assert prev_high == POS
        return out

    def height(self) -> int:
        return base_of(self.M[ROOT]).level + 1


def run(tree: BwTree, ops, seed: int, log: Optional[list] = None):
    """Run the operations as concurrent threads with a seeded scheduler.

    ops is a list of (thread, name, key, value). Each thread runs its ops in
    order. Returns the results and, if log is given, fills it with
    (thread, name, key, value, result, start step, end step)."""
    rng = random.Random(seed)
    per_thread: Dict[int, List] = {}
    for t, name, k, v in ops:
        per_thread.setdefault(t, []).append((name, k, v))
    gens: Dict[int, Tuple] = {}
    results = []
    step = 0

    def start(t):
        if per_thread[t]:
            name, k, v = per_thread[t].pop(0)
            g = tree.lookup(k) if name == "lookup" else tree.upsert(k, v) if name == "upsert" else tree.delete(k)
            gens[t] = (g, name, k, v, step)
        else:
            gens.pop(t, None)

    for t in list(per_thread):
        start(t)
    while gens:
        t = rng.choice(sorted(gens))
        g, name, k, v, s = gens[t]
        step += 1
        try:
            next(g)
        except StopIteration as e:
            results.append((t, name, k, v, e.value))
            if log is not None:
                log.append((t, name, k, v, e.value, s, step))
            start(t)
    return results


def run_one(tree: BwTree, gen):
    """Run one operation alone and return its result."""
    while True:
        try:
            next(gen)
        except StopIteration as e:
            return e.value
