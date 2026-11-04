# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/relaxed-heap/. The authors are listed in prov/KN6FTW.jsonl.

from typing import Any, Dict, Generic, Iterator, List, Optional, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


K = TypeVar("K", bound=Ordered)


class Node(Generic[K]):
    """A node of a relaxed binomial tree.

    children[i] is the child of rank i, so the rank is len(children) and the
    last child is children[-1]. An active node may have a smaller key than
    its parent.
    """

    __slots__ = ("key", "parent", "children", "active")

    def __init__(self, key: K) -> None:
        self.key = key
        self.parent: Optional[Node[K]] = None
        self.children: List[Node[K]] = []
        self.active = False

    @property
    def rank(self) -> int:
        return len(self.children)


class RelaxedHeap(Generic[K]):
    """Rank-relaxed heap: binomial trees in which a few nodes may violate heap order.

    Invariants when no operation runs: (a) at most one active node of each
    rank; (b) every active node is the last child of its parent; (c) every
    other non-root node has a key at least the key of its parent.
    """

    def __init__(self) -> None:
        self.roots: Dict[int, Node[K]] = {}
        self.actives: Dict[int, List[Node[K]]] = {}
        self.n = 0
        self.transformations = 0
        self._work: List[Node[K]] = []

    def __len__(self) -> int:
        return self.n

    # -- marks -------------------------------------------------------------

    def _mark(self, v: Node[K]) -> None:
        if not v.active:
            v.active = True
            self.actives.setdefault(v.rank, []).append(v)

    def _unmark(self, v: Node[K]) -> None:
        if v.active:
            v.active = False
            lst = self.actives[v.rank]
            lst.remove(v)
            if not lst:
                del self.actives[v.rank]

    def _set_rank_change(self, v: Node[K], f: Any) -> None:
        """Run f, which changes the rank of v, and keep the active lists right."""
        was = v.active
        self._unmark(v)
        f()
        if was:
            self._mark(v)

    # -- tree primitives ---------------------------------------------------

    def _place(self, new: Node[K], parent: Optional[Node[K]], slot: int) -> None:
        """Put new in the slot of rank slot under parent, or in the root list."""
        new.parent = parent
        if parent is None:
            self._unmark(new)
            self.roots[slot] = new
        else:
            parent.children[slot] = new
        self._work.append(new)

    def _link(self, a: Node[K], b: Node[K]) -> Node[K]:
        """Link two loose trees of equal rank and return the new root."""
        if b.key < a.key:
            a, b = b, a
        self._unmark(b)
        if a.children:
            self._work.append(a.children[-1])
        self._set_rank_change(a, lambda: a.children.append(b))
        b.parent = a
        return a

    def _add_root(self, t: Node[K]) -> None:
        t.parent = None
        self._unmark(t)
        while t.rank in self.roots:
            u = self.roots.pop(t.rank)
            t = self._link(t, u)
        self.roots[t.rank] = t

    # -- transformations ---------------------------------------------------

    def _parent_transformation(self, s: Node[K]) -> None:
        """s is the last child of p. Link s and p in the place of p."""
        self.transformations += 1
        p = s.parent
        assert p is not None and p.children[-1] is s
        self._set_rank_change(p, lambda: p.children.pop())
        s.parent = None
        self._work.extend(p.children[-1:])
        if s.key < p.key:
            g, slot = p.parent, p.rank + 1
            self._unmark(p)
            self._unmark(s)
            if s.children:
                self._work.append(s.children[-1])
            s.children.append(p)
            p.parent = s
            self._place(s, g, slot)
        else:
            self._unmark(s)
            self._set_rank_change(p, lambda: p.children.append(s))
            s.parent = p

    def _pair(self, x: Node[K], y: Node[K]) -> None:
        """x and y are active last children of rank r of different parents."""
        self.transformations += 1
        p, q = x.parent, y.parent
        assert p is not None and q is not None and p is not q
        self._unmark(x)
        self._unmark(y)
        self._set_rank_change(p, lambda: p.children.pop())
        self._set_rank_change(q, lambda: q.children.pop())
        x.parent = y.parent = None
        self._work.extend(p.children[-1:] + q.children[-1:])
        if q.key < p.key:
            p, q, x, y = q, p, y, x
        g, slot = q.parent, q.rank + 1
        self._unmark(q)
        if p.children:
            self._work.append(p.children[-1])
        self._set_rank_change(p, lambda: p.children.append(q))
        q.parent = p
        w = self._link(x, y)
        self._place(w, g, slot)

    def _triple(self, v: Node[K], s: Node[K], c: Node[K]) -> None:
        """v (slot r of p) and c (last child of s, slot r + 1 of p) are active."""
        self.transformations += 1
        p = v.parent
        assert p is not None
        r = v.rank
        self._unmark(v)
        self._unmark(c)
        self._set_rank_change(s, lambda: s.children.pop())
        c.parent = v.parent = None
        p.children[r] = s
        self._work.append(s)
        if s.children:
            self._work.append(s.children[-1])
        w = self._link(v, c)
        self._place(w, p, r + 1)

    def _fix(self) -> None:
        """Restore the invariants for the nodes in the work list."""
        while self._work:
            v = self._work.pop()
            p = v.parent
            if p is None or not v.key < p.key:  # @line L5
                self._unmark(v)
                continue
            self._mark(v)  # @line L6
            r = v.rank
            if p.children[-1] is not v:  # @line L7
                s = p.children[r + 1]
                if s.key < p.key:  # @line L8
                    if p.children[-1] is not s:
                        self._work.extend([v, s])
                        continue
                    self._parent_transformation(s)
                if p.children[-1] is not v:
                    s = p.children[r + 1]
                    c = s.children[-1]
                    if c.active or c.key < s.key:  # @line L9
                        self._triple(v, s, c)
                        continue
                    self.transformations += 1  # @line L10
                    p.children[r], s.children[r] = c, v
                    c.parent, v.parent = p, s
                    self._work.extend([c, v])
                    continue
            others = [y for y in self.actives.get(r, []) if y is not v]
            if others:  # @line L11
                y = others[0]
                yp = y.parent
                if yp is None or yp.children[-1] is not y or not y.key < yp.key:
                    self._work.extend([v, y])
                    continue
                self._pair(v, y)

    # -- operations --------------------------------------------------------

    def insert(self, key: K) -> Node[K]:
        """Insert key and return its node, the handle for decrease_key."""
        x = Node(key)  # @line L1
        self._add_root(x)
        self.n += 1
        self._fix()
        return x

    def _min_node(self) -> Node[K]:
        best: Optional[Node[K]] = None
        for v in list(self.roots.values()) + [a for lst in self.actives.values() for a in lst]:
            if best is None or v.key < best.key:
                best = v
        if best is None:
            raise IndexError("the heap is empty")
        return best

    def find_min(self) -> K:
        """Scan the roots and the active nodes."""
        return self._min_node().key  # @line L2

    def decrease_key(self, x: Node[K], key: K) -> None:
        """Lower the key of node x to key, which must not be larger."""
        if x.key < key:
            raise ValueError("new key is larger than the current key")
        x.key = key  # @line L3
        self._work.append(x)  # @line L4
        self._fix()

    def delete_min(self) -> K:
        """Remove and return a smallest key."""
        key = self._min_node().key
        m = self._min_node()  # @line L12
        extra: Optional[Node[K]] = None
        if m.parent is not None:  # @line L13
            k = min(self.roots)
            t = self.roots.pop(k)
            kids, t.children = t.children, []
            for c in kids:
                self._add_root(c)
            if m.parent is not None:
                self._replace_by_tree(m, t)  # @line L14
                m = None  # type: ignore[assignment]
            else:
                extra = t
        if m is not None:
            del self.roots[m.rank]  # @line L15
            self._unmark(m)
            kids, m.children = m.children, []
            for c in kids:
                self._add_root(c)
            if extra is not None:
                self._add_root(extra)
        self.n -= 1
        self._fix()
        return key

    def _replace_by_tree(self, m: Node[K], e: Node[K]) -> None:
        """Rebuild the subtree of m without m, from e and the children of m."""
        p, r = m.parent, m.rank
        assert p is not None
        self._unmark(m)
        kids, m.children = m.children, []
        u = e
        for c in kids:
            self._unmark(c)
            c.parent = None
            u = self._link(u, c)
        self._place(u, p, r)
        m.parent = None

    # -- checking ----------------------------------------------------------

    def nodes(self) -> Iterator[Node[K]]:
        stack = list(self.roots.values())
        while stack:
            v = stack.pop()
            yield v
            stack.extend(v.children)

    def check_invariant(self) -> None:
        """Check the binomial shape, the parents and the invariants (a) to (c)."""
        count = 0
        seen: Dict[int, int] = {}
        for k, t in self.roots.items():
            assert t.rank == k and t.parent is None and not t.active
        for v in self.nodes():
            count += 1
            for i, c in enumerate(v.children):
                assert c.parent is v and c.rank == i
            if v.parent is not None:
                if v.active:
                    assert v.parent.children[-1] is v
                    seen[v.rank] = seen.get(v.rank, 0) + 1
                else:
                    assert not v.key < v.parent.key
        assert all(c == 1 for c in seen.values())
        assert sum(len(lst) for lst in self.actives.values()) == sum(seen.values())
        for r, lst in self.actives.items():
            assert all(a.active and a.rank == r for a in lst)
        assert count == self.n
        assert not self._work
