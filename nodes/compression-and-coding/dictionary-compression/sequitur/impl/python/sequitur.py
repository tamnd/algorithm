# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sequitur/. The authors are listed in prov/ZP2YY9.jsonl.

"""Sequitur (Nevill-Manning and Witten): online grammar inference.

The grammar keeps two invariants after each input symbol:
- digram uniqueness: no two non-overlapping occurrences of the same pair of adjacent
  symbols appear anywhere in the right-hand sides;
- rule utility: each rule other than the start rule is used at least twice.

Each rule is a circular doubly linked list with a guard node. A hash table maps each
digram to the nodes where it starts. Repairs are kept on two work lists, not on the
call stack, so the code never recurses. The time is O(n) expected for n symbols,
amortized O(1) expected per symbol.

Terminals are non-negative integers. In the output, rule k >= 1 is written as the
symbol -k, and rule 0 is the start rule.
"""

from typing import Iterable, Optional, Union


class _Rule:
    __slots__ = ("id", "guard", "uses", "alive")

    def __init__(self, rid: int) -> None:
        self.id = rid
        self.uses: set["_Node"] = set()
        self.alive = True
        g = _Node(None)
        g.owner = self
        g.prev = g.next = g
        self.guard = g


class _Node:
    __slots__ = ("sym", "prev", "next", "owner", "alive")

    def __init__(self, sym: Union[int, _Rule, None]) -> None:
        self.sym = sym  # int: terminal, _Rule: nonterminal, None: guard
        self.prev: Optional["_Node"] = None
        self.next: Optional["_Node"] = None
        self.owner: Optional[_Rule] = None  # set only on guard nodes
        self.alive = True

    def value(self) -> int:
        s = self.sym
        return s if isinstance(s, int) else -s.id


def _real(x: Optional[_Node]) -> bool:
    return x is not None and x.sym is not None


class Sequitur:
    """Online Sequitur. Call append for each symbol; grammar() returns the rules."""

    def __init__(self) -> None:
        self.start = _Rule(0)
        self.next_id = 1
        self.rules: dict[int, _Rule] = {}
        self.index: dict[tuple[int, int], list[_Node]] = {}
        self.todo: list[_Node] = []
        self.underused: list[_Rule] = []

    # links: every change of a next pointer goes through these two methods
    def _link(self, a: _Node, b: _Node) -> None:
        a.next, b.prev = b, a
        if _real(a) and _real(b):
            self.index.setdefault((a.value(), b.value()), []).append(a)
            self.todo.append(a)

    def _unlink(self, a: _Node) -> None:
        b = a.next
        if _real(a) and _real(b):
            key = (a.value(), b.value())
            lst = self.index[key]
            lst.remove(a)
            if not lst:
                del self.index[key]

    def _new_node(self, sym: Union[int, _Rule]) -> _Node:
        x = _Node(sym)
        if isinstance(sym, _Rule):
            sym.uses.add(x)
        return x

    def _kill(self, x: _Node) -> None:
        x.alive = False
        if isinstance(x.sym, _Rule):
            r = x.sym
            r.uses.discard(x)
            if len(r.uses) == 1:
                self.underused.append(r)
            elif not r.uses:
                raise AssertionError("a rule lost all its uses")

    def append(self, c: int) -> None:
        """Add one terminal at the end of the start rule and restore both invariants."""
        g = self.start.guard
        last = g.prev
        self._unlink(last)  # @line L1
        x = self._new_node(c)
        self._link(last, x)
        self._link(x, g)
        self._repair()  # @line L2

    def _repair(self) -> None:
        while self.todo or self.underused:  # @line L3
            if self.underused:
                r = self.underused.pop()
                if r.alive and len(r.uses) == 1:  # @line L4
                    self._expand(r)  # @line L5
                continue
            x = self.todo.pop()
            if not x.alive or not _real(x) or not _real(x.next):
                continue
            m = self._other(x)  # @line L6
            if m is not None:
                self._match(x, m)  # @line L7

    def _other(self, x: _Node) -> Optional[_Node]:
        """Another occurrence of the digram at x that does not overlap it, if any."""
        best = None
        for m in self.index.get((x.value(), x.next.value()), ()):
            if m is x or m.next is x or x.next is m:
                continue
            if self._full(m):
                return m
            best = m
        return best

    @staticmethod
    def _full(m: _Node) -> bool:
        return m.prev.sym is None and m.next.next.sym is None

    def _match(self, x: _Node, m: _Node) -> None:
        if self._full(m):  # @line L8
            if self._full(x):
                raise AssertionError("two rules with the same right-hand side")
            self._substitute(x, m.prev.owner)
        elif self._full(x):
            self._substitute(m, x.prev.owner)
            self.todo.append(x)  # check x again: a third occurrence may remain
        else:
            r = _Rule(self.next_id)  # @line L9
            self.next_id += 1
            self.rules[r.id] = r
            a = self._new_node(x.sym)
            b = self._new_node(x.next.sym)
            self._link(r.guard, a)
            self._link(a, b)
            self._link(b, r.guard)
            self._substitute(m, r)  # @line L10
            self._substitute(x, r)

    def _substitute(self, x: _Node, r: _Rule) -> None:
        """Replace the digram that starts at x by one use of rule r."""
        q, y = x.prev, x.next
        z = y.next
        self._unlink(q)
        self._unlink(x)
        self._unlink(y)
        nt = self._new_node(r)
        self._link(q, nt)
        self._link(nt, z)
        self._kill(x)
        self._kill(y)

    def _expand(self, r: _Rule) -> None:
        """Rule r has one use left: put its right-hand side in place of that use."""
        (s,) = r.uses
        left, right = s.prev, s.next
        f, l = r.guard.next, r.guard.prev
        self._unlink(left)
        self._unlink(s)
        self._unlink(r.guard)
        self._unlink(l)
        self._link(left, f)
        self._link(l, right)
        r.uses.clear()
        s.alive = False
        r.alive = False
        del self.rules[r.id]

    def grammar(self) -> dict[int, list[int]]:
        """The rules as lists of symbols: terminals as they are, rule k as -k."""
        out = {}
        for r in [self.start, *sorted(self.rules.values(), key=lambda t: t.id)]:
            body = []
            x = r.guard.next
            while x is not r.guard:
                body.append(x.value())
                x = x.next
            out[r.id] = body
        return out


def sequitur(text: Iterable[int]) -> dict[int, list[int]]:
    """Run Sequitur on a sequence of non-negative integers and return the grammar."""
    s = Sequitur()
    for c in text:
        if c < 0:
            raise ValueError("terminals must be non-negative")
        s.append(c)
    return s.grammar()


def expand(grammar: dict[int, list[int]]) -> list[int]:
    """Expand rule 0 with an explicit stack. Time O(output length + grammar size)."""
    out: list[int] = []
    stack = list(reversed(grammar.get(0, [])))
    while stack:
        s = stack.pop()
        if s < 0:
            stack.extend(reversed(grammar[-s]))
        else:
            out.append(s)
    return out


def size(grammar: dict[int, list[int]]) -> int:
    """Total length of the right-hand sides."""
    return sum(len(body) for body in grammar.values())
