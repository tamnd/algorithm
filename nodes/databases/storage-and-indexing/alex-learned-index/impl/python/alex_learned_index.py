# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/alex-learned-index/. The authors are listed in prov/DS250H.jsonl.

"""ALEX, the updatable learned index of Ding et al. (SIGMOD 2020), simplified.

Inner nodes hold a linear model and a child array whose size is a power of 2;
a child may fill several adjacent slots. Data nodes are gapped arrays with a
linear model, a bitmap of occupied slots and gap values (each gap holds the
next key to its right, so the slot array is sorted and exponential search
works). Inserts are model-based. A full data node expands while it is small
enough, and otherwise splits: sideways if it fills two or more slots of its
parent, after doubling the parent if the parent can grow, and else down.

Simplifications: the cost models of the paper are replaced by fixed limits,
bulk loading uses one root over many data nodes, and deletes do not contract.
"""

import math
from bisect import bisect_left
from typing import List, Optional, Tuple

INF = math.inf


def fit_linear(keys: List[int], scale: float) -> Tuple[float, float]:
    """Least squares line of (key, rank), scaled so the ranks fill [0, scale)."""
    n = len(keys)
    if n == 0:
        return 0.0, 0.0
    if n == 1:
        return 0.0, scale / 2
    mx = sum(keys) / n
    my = (n - 1) / 2
    sxx = sum((k - mx) ** 2 for k in keys)
    sxy = sum((k - mx) * (i - my) for i, k in enumerate(keys))
    a = sxy / sxx if sxx else 0.0
    b = my - a * mx
    f = scale / n
    return a * f, b * f


class DataNode:
    def __init__(self, keys: List[int], capacity: int):
        self.parent: Optional["InnerNode"] = None
        self.next: Optional["DataNode"] = None
        self.prev: Optional["DataNode"] = None
        self._build(keys, capacity)

    def _build(self, keys: List[int], capacity: int) -> None:
        n = len(keys)
        assert capacity >= max(n, 1)
        self.capacity = capacity
        self.a, self.b = fit_linear(keys, capacity)
        self.vals: List[float] = [INF] * capacity
        self.occ = [False] * capacity
        self.n = n
        prev = -1
        for idx, k in enumerate(keys):                   # model-based placement
            p = self.predict(k)
            p = max(p, prev + 1)
            p = min(p, capacity - (n - idx))
            self.vals[p] = k
            self.occ[p] = True
            prev = p
        self._refill_all()

    def predict(self, k) -> int:
        p = int(round(self.a * k + self.b))
        return min(max(p, 0), self.capacity - 1)

    def _refill_all(self) -> None:
        nxt = INF
        for i in range(self.capacity - 1, -1, -1):
            if self.occ[i]:
                nxt = self.vals[i]
            else:
                self.vals[i] = nxt

    def _refill_before(self, p: int) -> None:
        """Set the gaps just before slot p to the value of slot p."""
        v = self.vals[p] if p < self.capacity else INF
        i = p - 1
        while i >= 0 and not self.occ[i]:
            self.vals[i] = v
            i -= 1

    def keys(self) -> List[int]:
        return [self.vals[i] for i in range(self.capacity) if self.occ[i]]

    def lower_bound(self, k, p: int) -> Tuple[int, int]:
        """EXPONENTIAL-SEARCH from p: the first slot whose value is >= k, and the probes."""
        vals, c = self.vals, self.capacity
        probes = 1
        if vals[p] >= k:
            step, hi = 1, p
            while hi - step >= 0 and vals[hi - step] >= k:
                probes += 1
                hi -= step
                step *= 2
            lo = max(hi - step, 0)
        else:
            step, lo = 1, p
            while lo + step < c and vals[lo + step] < k:
                probes += 1
                lo += step
                step *= 2
            hi = min(lo + step, c)
        i = bisect_left(vals, k, lo, hi)
        probes += max(1, (hi - lo).bit_length())
        return i, probes

    def _next_occupied(self, i: int) -> int:
        while i < self.capacity and not self.occ[i]:
            i += 1
        return i

    def find(self, k) -> Tuple[bool, int]:
        p = self.predict(k)                                          # @line L3
        i, probes = self.lower_bound(k, p)                           # @line L4
        j = self._next_occupied(i)                                   # @line L5
        return j < self.capacity and self.vals[j] == k, probes       # @line L5

    def insert(self, k) -> bool:
        """Model-based insert into a node that has a free slot."""
        assert self.n < self.capacity
        p = self.predict(k)                                          # @line L10
        i, _ = self.lower_bound(k, p)                                # @line L10
        q = self._next_occupied(i)                                   # @line L10
        if q < self.capacity and self.vals[q] == k:
            return False
        if i < q:                                                    # @line L11
            slot = min(max(p, i), q - 1)                             # @line L11
        else:                                                        # @line L12
            right = q
            while right < self.capacity and self.occ[right]:
                right += 1
            left = i - 1
            while left >= 0 and self.occ[left]:
                left -= 1
            if right < self.capacity and (left < 0 or right - q <= i - 1 - left):
                for t in range(right, q, -1):                        # @line L12
                    self.vals[t] = self.vals[t - 1]
                    self.occ[t] = True
                slot = q
            else:
                for t in range(left, i - 1):                         # @line L12
                    self.vals[t] = self.vals[t + 1]
                    self.occ[t] = True
                slot = i - 1
        self.vals[slot] = k                                          # @line L13
        self.occ[slot] = True                                        # @line L13
        self._refill_before(slot)                                    # @line L13
        self.n += 1
        return True

    def delete(self, k) -> bool:
        found, _ = self.find(k)
        if not found:
            return False
        i, _ = self.lower_bound(k, self.predict(k))
        j = self._next_occupied(i)
        self.occ[j] = False
        self.vals[j] = self.vals[j + 1] if j + 1 < self.capacity else INF
        self._refill_before(j)
        self.n -= 1
        return True


class InnerNode:
    def __init__(self, a: float, b: float, fanout: int):
        assert fanout & (fanout - 1) == 0
        self.a, self.b = a, b
        self.children: List[object] = [None] * fanout
        self.parent: Optional["InnerNode"] = None

    def slot(self, k) -> int:
        s = math.floor(self.a * k + self.b)
        return min(max(s, 0), len(self.children) - 1)

    def span(self, child) -> Tuple[int, int]:
        s = self.children.index(child)
        e = s
        while e < len(self.children) and self.children[e] is child:
            e += 1
        return s, e


class ALEX:
    def __init__(self, keys=(), max_capacity: int = 64, max_fanout: int = 16,
                 d_lower: float = 0.6, d_upper: float = 0.8, leaf_keys: int = 16):
        if not 0 < d_lower < d_upper <= 1:
            raise ValueError("need 0 < d_lower < d_upper <= 1")
        if max_fanout < 2 or max_fanout & (max_fanout - 1):
            raise ValueError("max_fanout must be a power of 2, at least 2")
        keys = sorted(set(keys))
        self.max_capacity = max_capacity
        self.max_fanout = max_fanout
        self.dl, self.du = d_lower, d_upper
        self.size = len(keys)
        self.expansions = self.splits = 0
        fanout = 2
        while fanout < max_fanout and fanout * leaf_keys < len(keys):
            fanout *= 2
        a, b = fit_linear(keys, fanout) if keys else (0.0, 0.0)
        root = InnerNode(a, b, fanout)
        parts: List[List[int]] = [[] for _ in range(fanout)]
        for k in keys:
            parts[root.slot(k)].append(k)
        prev = None
        pending: List[int] = []
        for s in range(fanout):
            if len(parts[s]) > max_capacity * d_lower:
                pending.extend(parts[s])     # too many keys for one node: insert them later
                parts[s] = []
            d = DataNode(parts[s], self._capacity_for(len(parts[s])))
            d.parent = root
            root.children[s] = d
            d.prev = prev
            if prev is not None:
                prev.next = d
            prev = d
        self.root = root
        self.size -= len(pending)
        for k in pending:
            self.insert(k)

    def _capacity_for(self, n: int) -> int:
        """The slots of a new node with n keys: n / d_lower, at most max_capacity."""
        return max(2, n + 1, min(math.ceil(n / self.dl), self.max_capacity))

    # ----- lookups -----

    def _leaf(self, k) -> DataNode:
        v = self.root                                                # @line L1
        while isinstance(v, InnerNode):                              # @line L2
            v = v.children[v.slot(k)]                                # @line L2
        return v

    def contains(self, k) -> bool:
        return self._leaf(k).find(k)[0]

    def probes(self, k) -> int:
        """How many slots the exponential search reads for k (a measurement)."""
        return self._leaf(k).find(k)[1]

    def range(self, lo, hi) -> List[int]:
        """The keys k with lo <= k <= hi, by a scan along the data nodes."""
        out: List[int] = []
        d: Optional[DataNode] = self._leaf(lo)
        while d is not None:
            for i in range(d.capacity):
                if d.occ[i]:
                    if d.vals[i] > hi:
                        return out
                    if d.vals[i] >= lo:
                        out.append(d.vals[i])
            d = d.next
        return out

    def keys(self) -> List[int]:
        out: List[int] = []
        d = self._first_leaf()
        while d is not None:
            out.extend(d.keys())
            d = d.next
        return out

    def _first_leaf(self) -> DataNode:
        v = self.root
        while isinstance(v, InnerNode):
            v = v.children[0]
        return v

    # ----- updates -----

    def insert(self, k) -> bool:
        while True:
            d = self._leaf(k)                                        # @line L6
            if d.find(k)[0]:
                return False
            if d.n + 1 <= self.du * d.capacity:                      # @line L7
                d.insert(k)
                self.size += 1
                return True
            need = max(2, math.ceil((d.n + 1) / self.dl))
            if need <= self.max_capacity:                            # @line L8
                d._build(d.keys(), need)                             # @line L8
                self.expansions += 1
            else:
                self._split(d)                                       # @line L9

    def delete(self, k) -> bool:
        ok = self._leaf(k).delete(k)
        if ok:
            self.size -= 1
        return ok

    def _replace(self, old: DataNode, parts: List[Tuple[DataNode, int, int]], parent: InnerNode) -> None:
        for d, s, e in parts:
            d.parent = parent
            for t in range(s, e):
                parent.children[t] = d
        first, last = parts[0][0], parts[-1][0]
        for x, y in zip(parts, parts[1:]):
            x[0].next, y[0].prev = y[0], x[0]
        first.prev, last.next = old.prev, old.next
        if old.prev is not None:
            old.prev.next = first
        if old.next is not None:
            old.next.prev = last

    def _split(self, d: DataNode) -> None:
        self.splits += 1
        p = d.parent
        s, e = p.span(d)
        if e - s == 1 and len(p.children) < self.max_fanout:
            # Double the parent: slot j becomes 2j and 2j + 1.
            p.children = [c for c in p.children for _ in (0, 1)]
            p.a, p.b = 2 * p.a, 2 * p.b
            s, e = 2 * s, 2 * e
        keys = d.keys()
        if e - s >= 2:                                               # split sideways
            mid = (s + e) // 2
            left = [k for k in keys if p.slot(k) < mid]
            right = [k for k in keys if p.slot(k) >= mid]
            l = DataNode(left, self._capacity_for(len(left)))
            r = DataNode(right, self._capacity_for(len(right)))
            self._replace(d, [(l, s, mid), (r, mid, e)], p)
            return
        # Split down: a new inner node with two children replaces d.
        lo, hi = keys[0], keys[-1]
        a = 2.0 / (hi - lo + 1)
        q = InnerNode(a, -a * lo, 2)
        q.parent = p
        left = [k for k in keys if q.slot(k) == 0]
        right = [k for k in keys if q.slot(k) == 1]
        l = DataNode(left, self._capacity_for(len(left)))
        r = DataNode(right, self._capacity_for(len(right)))
        for t in range(s, e):
            p.children[t] = q
        self._replace(d, [(l, 0, 1), (r, 1, 2)], q)

    # ----- checks -----

    def depth(self) -> int:
        def h(v):
            if isinstance(v, DataNode):
                return 1
            return 1 + max(h(c) for c in v.children)
        return h(self.root)

    def nodes(self) -> Tuple[int, int]:
        """The number of inner nodes and of data nodes."""
        inner, data, stack, seen = 0, 0, [self.root], set()
        while stack:
            v = stack.pop()
            if id(v) in seen:
                continue
            seen.add(id(v))
            if isinstance(v, DataNode):
                data += 1
            else:
                inner += 1
                stack.extend(v.children)
        return inner, data

    def check(self) -> None:
        """Raise AssertionError if an invariant fails."""
        seen = []
        self._check(self.root, seen)
        assert len(seen) == self.size
        assert seen == sorted(seen) and len(set(seen)) == len(seen)
        assert self.keys() == seen

    def _check(self, v, seen: List[int]) -> None:
        if isinstance(v, DataNode):
            assert v.n == sum(v.occ) <= v.capacity <= max(self.max_capacity, 2)
            nxt = INF
            for i in range(v.capacity - 1, -1, -1):
                if v.occ[i]:
                    nxt = v.vals[i]
                assert v.vals[i] == nxt, "gap value is not the next key"
            for k in v.keys():
                assert self._leaf(k) is v, "key is not in the node it routes to"
            seen.extend(v.keys())
            return
        prev = None
        for c in v.children:
            assert c.parent is v
            if c is not prev:
                self._check(c, seen)
            prev = c
        ids = [id(c) for c in v.children]
        for x in set(ids):                    # each child fills one run of slots
            idx = [i for i, y in enumerate(ids) if y == x]
            assert idx == list(range(idx[0], idx[-1] + 1))
