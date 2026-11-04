# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/finger-search-tree/. The authors are listed in prov/X7SV6M.jsonl.
"""A level-linked (2,4)-tree with keys in the bottom nodes, supporting finger search.

Each node stores its key range (lo, hi]: lo is exclusive, hi is inclusive, and
None stands for minus or plus infinity. All nodes of one level are linked in
key order by prev and next. A finger is a bottom node.
"""

from typing import Any, List, Optional, Tuple


class Node:
    __slots__ = ("bottom", "keys", "children", "parent", "prev", "next", "lo", "hi")

    def __init__(self, bottom: bool) -> None:
        self.bottom = bottom
        self.keys: List[Any] = []  # bottom: the stored keys; internal: separators
        self.children: List["Node"] = []
        self.parent: Optional["Node"] = None
        self.prev: Optional["Node"] = None
        self.next: Optional["Node"] = None
        self.lo: Any = None
        self.hi: Any = None


def _in_range(v: Node, k: Any) -> bool:
    return (v.lo is None or v.lo < k) and (v.hi is None or k <= v.hi)


def _size(v: Node) -> int:
    return len(v.keys) if v.bottom else len(v.children)


class FingerSearchTree:
    def __init__(self) -> None:
        self.root = Node(True)
        self.n = 0
        self.last_climb = 0  # levels climbed by the last finger search

    def __len__(self) -> int:
        return self.n

    # ---- searching -------------------------------------------------------

    def _descend(self, v: Node, k: Any) -> Node:
        while not v.bottom:  # @line L7
            j = 0  # @line L8
            while j < len(v.keys) and v.keys[j] < k:
                j += 1
            v = v.children[j]  # @line L9
        return v  # @line L10

    def finger_search(self, f: Node, k: Any) -> Tuple[Node, bool]:
        """Return the bottom node whose range holds k, and whether k is stored."""
        v = f  # @line L1
        climb = 0
        while not _in_range(v, k):  # @line L2
            w = v.next if (v.hi is not None and k > v.hi) else v.prev  # @line L3
            if w is not None and _in_range(w, k):  # @line L4
                v = w
                break
            v = v.parent  # @line L5
            climb += 1
        self.last_climb = climb
        b = self._descend(v, k)  # @line L6
        return b, k in b.keys

    def finger(self, k: Any) -> Node:
        """The bottom node whose range holds k, found from the root."""
        return self._descend(self.root, k)

    def search(self, k: Any, f: Optional[Node] = None) -> bool:
        if f is None:
            return k in self.finger(k).keys
        return self.finger_search(f, k)[1]

    # ---- updates ---------------------------------------------------------

    def _link_after(self, v: Node, u: Node) -> None:
        u.prev, u.next = v, v.next
        if v.next is not None:
            v.next.prev = u
        v.next = u

    def _unlink(self, v: Node) -> None:
        if v.prev is not None:
            v.prev.next = v.next
        if v.next is not None:
            v.next.prev = v.prev

    def insert(self, k: Any, f: Optional[Node] = None) -> Node:
        """Insert k; return the bottom node that holds k afterwards."""
        b, found = self.finger_search(f, k) if f is not None else (self.finger(k), False)  # @line L11
        if found or k in b.keys:
            return b
        j = 0  # @line L12
        while j < len(b.keys) and b.keys[j] < k:
            j += 1
        b.keys.insert(j, k)
        self.n += 1
        holder = b
        v = b  # @line L13
        while _size(v) > (3 if v.bottom else 4):  # @line L14
            u = Node(v.bottom)  # @line L15
            if v.bottom:
                s = v.keys[1]
                u.keys, v.keys = v.keys[2:], v.keys[:2]
                if k in u.keys:
                    holder = u
            else:
                s = v.keys[2]
                u.keys, v.keys = v.keys[3:], v.keys[:2]
                u.children, v.children = v.children[3:], v.children[:3]
                for c in u.children:
                    c.parent = u
            u.lo, u.hi, v.hi = s, v.hi, s
            self._link_after(v, u)
            p = v.parent
            if p is None:  # @line L16
                r = Node(False)
                r.keys, r.children = [s], [v, u]
                v.parent = u.parent = r
                self.root = r
                break
            i = p.children.index(v)  # @line L17
            p.children.insert(i + 1, u)
            p.keys.insert(i, s)
            u.parent = p
            v = p  # @line L18
        return holder  # @line L19

    def delete(self, k: Any, f: Optional[Node] = None) -> Optional[Node]:
        """Delete k if present; return a bottom node whose range holds k afterwards."""
        b = self.finger_search(f, k)[0] if f is not None else self.finger(k)
        if k not in b.keys:
            return b
        b.keys.remove(k)
        self.n -= 1
        holder = b
        v = b
        while v.parent is not None and _size(v) < (1 if v.bottom else 2):
            p = v.parent
            i = p.children.index(v)
            left = i > 0
            sib = p.children[i - 1] if left else p.children[i + 1]
            if _size(sib) > (1 if v.bottom else 2):
                self._borrow(p, i, v, sib, left)
                break
            survivor = self._merge(p, i, v, sib, left)
            if v is holder:
                holder = survivor
            v = p
        r = self.root
        if not r.bottom and len(r.children) == 1:
            c = r.children[0]
            c.parent = None
            self.root = c
        return holder

    def _borrow(self, p: Node, i: int, v: Node, sib: Node, left: bool) -> None:
        if v.bottom:
            if left:
                v.keys.insert(0, sib.keys.pop())
                t = sib.keys[-1]
                p.keys[i - 1] = t
                sib.hi = v.lo = t
            else:
                t = sib.keys.pop(0)
                v.keys.append(t)
                p.keys[i] = t
                v.hi = sib.lo = t
            return
        if left:
            c = sib.children.pop()
            t = sib.keys.pop()
            v.children.insert(0, c)
            v.keys.insert(0, p.keys[i - 1])
            p.keys[i - 1] = t
            sib.hi = v.lo = t
        else:
            c = sib.children.pop(0)
            t = sib.keys.pop(0)
            v.children.append(c)
            v.keys.append(p.keys[i])
            p.keys[i] = t
            v.hi = sib.lo = t
        c.parent = v

    def _merge(self, p: Node, i: int, v: Node, sib: Node, left: bool) -> Node:
        if left:  # sib is just before v
            sep = p.keys.pop(i - 1)
            if not v.bottom:
                sib.keys += [sep] + v.keys
            else:
                sib.keys += v.keys
            sib.hi = v.hi
        else:  # sib is just after v
            sep = p.keys.pop(i)
            if not v.bottom:
                sib.keys = v.keys + [sep] + sib.keys
            else:
                sib.keys = v.keys + sib.keys
            sib.lo = v.lo
        if not v.bottom:
            for c in v.children:
                c.parent = sib
            sib.children = sib.children + v.children if left else v.children + sib.children
        p.children.pop(i)
        self._unlink(v)
        return sib

    # ---- inspection ------------------------------------------------------

    def keys(self) -> List[Any]:
        v = self.root
        while not v.bottom:
            v = v.children[0]
        out: List[Any] = []
        while v is not None:
            out.extend(v.keys)
            v = v.next
        return out

    def height(self) -> int:
        h, v = 0, self.root
        while not v.bottom:
            v, h = v.children[0], h + 1
        return h

    def check_invariant(self) -> None:
        r = self.root
        assert r.parent is None and r.lo is None and r.hi is None
        level = [r]
        count = 0
        while True:
            for a, b in zip(level, level[1:]):
                assert a.next is b and b.prev is a and a.hi == b.lo
            assert level[0].prev is None and level[-1].next is None
            nxt: List[Node] = []
            for v in level:
                if v.bottom:
                    assert v is r or 1 <= len(v.keys) <= 3
                    assert all(a < b for a, b in zip(v.keys, v.keys[1:]))
                    assert all(_in_range(v, x) for x in v.keys)
                    assert not v.children
                    count += len(v.keys)
                    continue
                assert 2 <= len(v.children) <= 4
                assert len(v.keys) == len(v.children) - 1
                assert all(a < b for a, b in zip(v.keys, v.keys[1:]))
                bounds = [v.lo] + v.keys + [v.hi]
                for j, c in enumerate(v.children):
                    assert c.parent is v and c.lo == bounds[j] and c.hi == bounds[j + 1]
                nxt.extend(v.children)
            if level[0].bottom:
                assert all(v.bottom for v in level)
                break
            assert all(not v.bottom for v in level)
            level = nxt
        assert count == self.n
