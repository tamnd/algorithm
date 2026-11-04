# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hybrid-tst/. The authors are listed in prov/EHWQ99.jsonl.

from typing import Generic, TypeVar

V = TypeVar("V")


class _Node(Generic[V]):
    __slots__ = ("c", "left", "mid", "right", "val")

    def __init__(self, c: str) -> None:
        self.c = c
        self.left: _Node[V] | None = None
        self.mid: _Node[V] | None = None
        self.right: _Node[V] | None = None
        self.val: V | None = None


class _Cell(Generic[V]):
    """One entry of the R by R table: the value of the 2-symbol key and the TST of the rest."""

    __slots__ = ("val", "tst")

    def __init__(self) -> None:
        self.val: V | None = None
        self.tst: _Node[V] | None = None


class HybridTST(Generic[V]):
    """A ternary search tree whose root is an R by R table indexed by the first two symbols.

    The alphabet is a string of R distinct symbols in increasing order. Keys of length 0 and 1 are kept
    in a field and an array of R values; a key of length 2 is kept in its
    table cell. get and put take O(1) for the table plus a TST search on the
    remaining m - 2 symbols. Values must not be None.
    """

    def __init__(self, alphabet: str = "".join(map(chr, range(256)))) -> None:
        if list(alphabet) != sorted(set(alphabet)):
            raise ValueError("the alphabet must be sorted and without repeats")
        self.alphabet = alphabet
        self.code = {c: i for i, c in enumerate(alphabet)}
        r = self.r = len(alphabet)
        self.empty_val: V | None = None
        self.one: list[V | None] = [None] * r
        self.table: list[_Cell[V] | None] = [None] * (r * r)
        self.n = 0

    def size(self) -> int:
        return self.n

    def _code(self, c: str) -> int:
        k = self.code.get(c)
        if k is None:
            raise ValueError(f"symbol {c!r} is not in the alphabet")
        return k

    def _cell_index(self, s: str) -> int:
        return self._code(s[0]) * self.r + self._code(s[1])

    def get(self, s: str) -> V | None:
        """Return the value of key s, or None."""
        if len(s) < 2:  # @line L1
            if not s:
                return self.empty_val
            return self.one[self._code(s[0])]
        cell = self.table[self._cell_index(s)]  # @line L2
        if cell is None:  # @line L3
            return None
        if len(s) == 2:  # @line L4
            return cell.val
        x, d, rest = cell.tst, 0, s[2:]  # @line L5
        while x is not None:
            if rest[d] < x.c:
                x = x.left
            elif rest[d] > x.c:
                x = x.right
            elif d < len(rest) - 1:
                x, d = x.mid, d + 1
            else:
                return x.val
        return None

    def put(self, s: str, v: V) -> None:
        """Set the value of key s to v (v must not be None)."""
        if v is None:
            raise ValueError("a value must not be None")
        if len(s) < 2:  # @line L6
            if not s:
                old = self.empty_val
                self.empty_val = v
            else:
                k = self._code(s[0])
                old = self.one[k]
                self.one[k] = v
            if old is None:
                self.n += 1
            return
        i = self._cell_index(s)  # @line L7
        cell = self.table[i]
        if cell is None:
            cell = self.table[i] = _Cell()
        if len(s) == 2:  # @line L8
            if cell.val is None:
                self.n += 1
            cell.val = v
            return
        rest = s[2:]  # @line L9
        if cell.tst is None:
            cell.tst = _Node(rest[0])
        x, d = cell.tst, 0
        while True:
            c = rest[d]
            if c < x.c:
                if x.left is None:
                    x.left = _Node(c)
                x = x.left
            elif c > x.c:
                if x.right is None:
                    x.right = _Node(c)
                x = x.right
            elif d < len(rest) - 1:
                d += 1
                if x.mid is None:
                    x.mid = _Node(rest[d])
                x = x.mid
            else:
                if x.val is None:
                    self.n += 1
                x.val = v
                return

    def delete(self, s: str) -> None:
        """Remove key s if present; prune dead TST nodes and empty cells."""
        if len(s) < 2:  # @line L10
            if not s:
                if self.empty_val is not None:
                    self.empty_val = None
                    self.n -= 1
            else:
                k = self._code(s[0])
                if self.one[k] is not None:
                    self.one[k] = None
                    self.n -= 1
            return
        i = self._cell_index(s)  # @line L11
        cell = self.table[i]
        if cell is None:
            return
        if len(s) == 2:  # @line L12
            if cell.val is not None:
                cell.val = None
                self.n -= 1
        else:
            self._tst_delete(cell, s[2:])  # @line L13
        if cell.val is None and cell.tst is None:  # @line L14
            self.table[i] = None

    def _tst_delete(self, cell: _Cell[V], rest: str) -> None:
        path: list[tuple[_Node[V], _Node[V] | None, str]] = []
        x, parent, link, d = cell.tst, None, "root", 0
        while x is not None:
            path.append((x, parent, link))
            if rest[d] < x.c:
                x, parent, link = x.left, x, "left"
            elif rest[d] > x.c:
                x, parent, link = x.right, x, "right"
            elif d < len(rest) - 1:
                x, parent, link, d = x.mid, x, "mid", d + 1
            else:
                break
        if x is None or x.val is None:
            return
        x.val = None
        self.n -= 1
        for node, par, lk in reversed(path):
            if node.val is not None or node.mid is not None:
                return
            repl = _bst_remove_root(node)
            if par is None:
                cell.tst = repl
            else:
                setattr(par, lk, repl)

    def keys_with_prefix(self, p: str) -> list[str]:
        """Return the keys that start with p, in lexicographic order."""
        out: list[str] = []
        if p == "":  # @line L15
            if self.empty_val is not None:
                out.append("")
            for a in range(self.r):
                out.extend(self.keys_with_prefix(self.alphabet[a]))
            return out
        if len(p) == 1:  # @line L16
            a = self._code(p)
            if self.one[a] is not None:
                out.append(p)
            for b in range(self.r):
                cell = self.table[a * self.r + b]
                if cell is not None:
                    two = p + self.alphabet[b]
                    if cell.val is not None:
                        out.append(two)
                    _collect(cell.tst, two, out)
            return out
        cell = self.table[self._cell_index(p)]  # @line L17
        if cell is None:
            return out
        if len(p) == 2:
            if cell.val is not None:
                out.append(p)
            _collect(cell.tst, p, out)
            return out
        rest = p[2:]  # @line L18
        x, d = cell.tst, 0
        while x is not None:
            if rest[d] < x.c:
                x = x.left
            elif rest[d] > x.c:
                x = x.right
            elif d < len(rest) - 1:
                x, d = x.mid, d + 1
            else:
                break
        if x is None:
            return out
        if x.val is not None:
            out.append(p)
        _collect(x.mid, p, out)
        return out

    def keys(self) -> list[str]:
        return self.keys_with_prefix("")

    def longest_prefix_of(self, s: str) -> str | None:
        """Return the longest key that is a prefix of s, or None."""
        best = 0 if self.empty_val is not None else -1
        if len(s) >= 1 and self.one[self._code(s[0])] is not None:
            best = 1
        if len(s) >= 2:
            cell = self.table[self._cell_index(s)]
            if cell is not None:
                if cell.val is not None:
                    best = 2
                x, d = cell.tst, 2
                while x is not None and d < len(s):
                    if s[d] < x.c:
                        x = x.left
                    elif s[d] > x.c:
                        x = x.right
                    else:
                        d += 1
                        if x.val is not None:
                            best = d
                        x = x.mid
        return None if best < 0 else s[:best]

    def tst_node_count(self) -> int:
        count = 0
        for cell in self.table:
            if cell is not None:
                stack = [cell.tst]
                while stack:
                    y = stack.pop()
                    if y is not None:
                        count += 1
                        stack.extend((y.left, y.mid, y.right))
        return count

    def check_invariant(self) -> None:
        valued = (self.empty_val is not None) + sum(v is not None for v in self.one)
        for cell in self.table:
            if cell is None:
                continue
            assert cell.val is not None or cell.tst is not None, "empty cell"
            valued += cell.val is not None
            stack: list[tuple[_Node[V] | None, str | None, str | None]] = [(cell.tst, None, None)]
            while stack:
                y, lo, hi = stack.pop()
                if y is None:
                    continue
                assert (lo is None or lo < y.c) and (hi is None or y.c < hi)
                assert y.val is not None or y.mid is not None, "dead node"
                valued += y.val is not None
                stack.append((y.left, lo, y.c))
                stack.append((y.right, y.c, hi))
                stack.append((y.mid, None, None))
        assert valued == self.n


def _bst_remove_root(node: _Node[V]) -> _Node[V] | None:
    if node.left is None:
        return node.right
    if node.right is None:
        return node.left
    p, m = node, node.right
    while m.left is not None:
        p, m = m, m.left
    if p is not node:
        p.left = m.right
        m.right = node.right
    m.left = node.left
    return m


def _collect(x: _Node[V] | None, prefix: str, out: list[str]) -> None:
    """Append the keys of the TST below x, each with the given prefix, in order."""
    stack: list[tuple[_Node[V] | None, str, int]] = [(x, prefix, 0)]
    while stack:
        y, t, state = stack.pop()
        if y is None:
            continue
        if state == 0:
            stack.append((y.right, t, 0))
            stack.append((y, t, 1))
            stack.append((y.left, t, 0))
        else:
            if y.val is not None:
                out.append(t + y.c)
            stack.append((y.mid, t + y.c, 0))
