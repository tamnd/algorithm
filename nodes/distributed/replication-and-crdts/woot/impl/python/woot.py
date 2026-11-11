# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/woot/. The authors are listed in prov/D9EX5G.jsonl.

"""WOOT (Oster, Urso, Molli and Imine 2006), a sequence CRDT made of W-characters.

A W-character is (id, value, prev, next): a unique id (site, clock), and the
ids of the characters just before and just after it at the moment it was
made. The sequence starts with a begin mark and ends with an end mark, and it
never loses a character: a delete only makes it invisible.
To place a remote character c between prev and next, integrate looks at the
characters that lie strictly between them. If none, c goes there. Otherwise
it keeps only those whose own prev and next lie outside the gap, finds the
place of c among them by id, and repeats on the smaller gap. An operation
waits in a pool until the characters it names are present, so delivery can
be in any order and duplicates are ignored.
"""

from typing import Any, NamedTuple

Id = tuple[int, int]  # (site, clock)
BEGIN: Id = (-1, 0)
END: Id = (-1, 1)


class WChar(NamedTuple):
    id: Id
    value: Any
    prev: Id
    next: Id


class Woot:
    """One WOOT replica with site id site."""

    def __init__(self, site: int) -> None:
        self.site = site
        self.clock = 0
        self.seq: list[Id] = [BEGIN, END]
        self.chars: dict[Id, WChar] = {}
        self.hidden: set[Id] = set()
        self.pool: list[tuple] = []

    def integrate(self, c: WChar, cp: Id, cn: Id) -> None:
        while True:
            pos = {x: k for k, x in enumerate(self.seq)}
            ip, iq = pos[cp], pos[cn]
            inner = self.seq[ip + 1: iq]  # @line L1
            if not inner:  # @line L2
                self.seq.insert(iq, c.id)  # @line L3
                self.chars[c.id] = c
                return
            ls = [cp]  # @line L4
            for d in inner:
                w = self.chars[d]
                if pos[w.prev] <= ip and iq <= pos[w.next]:  # @line L5
                    ls.append(d)
            ls.append(cn)
            i = 1  # @line L6
            while i < len(ls) - 1 and ls[i] < c.id:  # @line L7
                i += 1
            cp, cn = ls[i - 1], ls[i]  # @line L8

    def _visible(self) -> list[Id]:
        return [x for x in self.seq[1:-1] if x not in self.hidden]

    def local_insert(self, i: int, value: Any) -> tuple:
        vis = self._visible()
        cp = vis[i - 1] if i > 0 else BEGIN
        cn = vis[i] if i < len(vis) else END
        self.clock += 1
        c = WChar((self.site, self.clock), value, cp, cn)
        self.integrate(c, cp, cn)
        return ("ins", c)

    def local_delete(self, i: int) -> tuple:
        op = ("del", self._visible()[i])
        self.hidden.add(op[1])
        return op

    def _executable(self, op: tuple) -> bool:
        if op[0] == "del":
            return op[1] in self.chars
        c = op[1]
        return (c.prev == BEGIN or c.prev in self.chars) and (c.next == END or c.next in self.chars)

    def apply(self, op: tuple) -> None:
        """Receive a remote op in any order. It waits in the pool until it can run."""
        self.pool.append(op)
        progress = True
        while progress:
            progress = False
            for k, o in enumerate(self.pool):
                if self._executable(o):
                    self.pool.pop(k)
                    if o[0] == "del":
                        self.hidden.add(o[1])
                    elif o[1].id not in self.chars:
                        self.integrate(o[1], o[1].prev, o[1].next)
                    progress = True
                    break

    def value(self) -> list[Any]:
        return [self.chars[x].value for x in self._visible()]

    def order(self) -> list[Id]:
        return list(self.seq)

    def check_invariant(self) -> None:
        pos = {x: k for k, x in enumerate(self.seq)}
        assert len(pos) == len(self.seq) == len(self.chars) + 2
        for c in self.chars.values():
            assert pos[c.prev] < pos[c.id] < pos[c.next], "a character stays between its prev and next"
