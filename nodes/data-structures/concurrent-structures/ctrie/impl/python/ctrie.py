# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ctrie/. The authors are listed in prov/3YJ33R.jsonl.

import threading
import time
from collections.abc import Callable, Generator, Hashable
from typing import Any, TypeVar

R = TypeVar("R")

SPIN = "spin"
NOTFOUND = "NOTFOUND"
RESTART = "RESTART"

Steps = Generator[str | None, None, R]


def run(steps: "Steps[R]") -> R:
    """Run a step generator to its end in the calling thread and return its result."""
    while True:
        try:
            if next(steps) == SPIN:
                time.sleep(0)
        except StopIteration as stop:
            return stop.value


class SNode:
    """A key and its value. Immutable."""

    __slots__ = ("key", "value", "hash")

    def __init__(self, key: Hashable, value: Any, h: int) -> None:
        self.key, self.value, self.hash = key, value, h


class TNode:
    """A tomb: the single S-node left in an I-node that is to be removed. Immutable."""

    __slots__ = ("sn",)

    def __init__(self, sn: SNode) -> None:
        self.sn = sn


class LNode:
    """The S-nodes whose hashes are equal in every bit. Immutable."""

    __slots__ = ("sns",)

    def __init__(self, sns: tuple[SNode, ...]) -> None:
        self.sns = sns

    def find(self, key: Hashable) -> Any:
        for sn in self.sns:
            if sn.key == key:
                return sn.value
        return NOTFOUND


class CNode:
    """A bitmap and the array of branches (I-nodes or S-nodes) for the set bits. Immutable."""

    __slots__ = ("bmp", "array")

    def __init__(self, bmp: int, array: tuple[Any, ...]) -> None:
        self.bmp, self.array = bmp, array

    def inserted(self, pos: int, flag: int, b: Any) -> "CNode":
        return CNode(self.bmp | flag, self.array[:pos] + (b,) + self.array[pos:])

    def updated(self, pos: int, b: Any) -> "CNode":
        return CNode(self.bmp, self.array[:pos] + (b,) + self.array[pos + 1:])

    def removed(self, pos: int, flag: int) -> "CNode":
        return CNode(self.bmp ^ flag, self.array[:pos] + self.array[pos + 1:])


class INode:
    """The only mutable node: one word main, read and changed by compare-and-swap.

    The compare-and-swap compares by identity and is simulated with a lock.
    """

    __slots__ = ("_main", "_lock")

    def __init__(self, main: Any) -> None:
        self._main = main
        self._lock = threading.Lock()

    def read(self) -> Any:
        with self._lock:
            return self._main

    def cas(self, expect: Any, new: Any) -> bool:
        with self._lock:
            if self._main is expect:
                self._main = new
                return True
            return False


class Ctrie:
    """The Ctrie of Prokopec, Bagwell and Odersky, without snapshots.

    Each C-node branches on W bits of the hash; when all hbits bits are used,
    keys with equal hashes share an L-node. Every read of an I-node and every
    compare-and-swap is one step of a generator.
    """

    def __init__(self, w: int = 5, hbits: int = 30, hash_fn: Callable[[Hashable], int] | None = None) -> None:
        self.w, self.hbits = w, hbits
        self.mask = (1 << w) - 1
        self.hash_fn = hash_fn or hash
        self.root = INode(CNode(0, ()))

    def _hash(self, key: Hashable) -> int:
        return self.hash_fn(key) & ((1 << self.hbits) - 1)

    def _flagpos(self, h: int, lev: int, bmp: int) -> tuple[int, int]:
        flag = 1 << ((h >> lev) & self.mask)
        return flag, bin(bmp & (flag - 1)).count("1")

    def _dual(self, x: SNode, y: SNode, lev: int) -> Any:
        """The main node that holds two S-nodes whose hashes agree below level lev."""
        if lev >= self.hbits:
            return LNode((x, y))
        fx, fy = 1 << ((x.hash >> lev) & self.mask), 1 << ((y.hash >> lev) & self.mask)
        if fx == fy:
            return CNode(fx, (INode(self._dual(x, y, lev + self.w)),))
        return CNode(fx | fy, (x, y) if fx < fy else (y, x))

    def _contract(self, cn: CNode, lev: int) -> Any:
        if lev > 0 and len(cn.array) == 1 and isinstance(cn.array[0], SNode):
            return TNode(cn.array[0])
        return cn

    def _compress(self, cn: CNode, lev: int) -> "Steps[Any]":
        branches = []
        for b in cn.array:
            if isinstance(b, INode):
                m = b.read()
                yield None
                if isinstance(m, TNode):
                    b = m.sn  # resurrect
            branches.append(b)
        return self._contract(CNode(cn.bmp, tuple(branches)), lev)

    def _clean_steps(self, p: INode | None, lev: int) -> "Steps[None]":
        if p is None:
            return None
        m = p.read()  # @line L26
        yield None
        if isinstance(m, CNode):
            new = yield from self._compress(m, lev)
            p.cas(m, new)
            yield None
        return None

    def _clean_parent_steps(self, p: INode | None, i: INode, h: int, lev: int) -> "Steps[None]":
        while p is not None:
            m = p.read()  # @line L27
            yield None
            if not isinstance(m, CNode):
                return None
            flag, pos = self._flagpos(h, lev, m.bmp)
            if not m.bmp & flag or m.array[pos] is not i:
                return None
            im = i.read()  # @line L28
            yield None
            if not isinstance(im, TNode):
                return None
            ok = p.cas(m, self._contract(m.updated(pos, im.sn), lev))
            yield None
            if ok:
                return None
        return None

    # ---- lookup ----

    def lookup_steps(self, key: Hashable) -> "Steps[Any]":
        h = self._hash(key)
        while True:
            r = yield from self._ilookup(self.root, key, h, 0, None)  # @line L1
            if r is not RESTART:
                return r

    def _ilookup(self, i: INode, key: Hashable, h: int, lev: int, parent: INode | None) -> "Steps[Any]":
        m = i.read()  # @line L2
        yield None
        if isinstance(m, CNode):  # @line L3
            flag, pos = self._flagpos(h, lev, m.bmp)
            if not m.bmp & flag:
                return NOTFOUND
            b = m.array[pos]  # @line L4
            if isinstance(b, INode):
                return (yield from self._ilookup(b, key, h, lev + self.w, i))
            return b.value if b.key == key else NOTFOUND  # @line L5
        if isinstance(m, TNode):  # @line L6
            yield from self._clean_steps(parent, lev - self.w)
            return RESTART
        return m.find(key)  # @line L7

    # ---- insert ----

    def insert_steps(self, key: Hashable, value: Any) -> "Steps[None]":
        h = self._hash(key)
        while True:
            r = yield from self._iinsert(self.root, SNode(key, value, h), 0, None)  # @line L8
            if r is not RESTART:
                return None

    def _iinsert(self, i: INode, sn: SNode, lev: int, parent: INode | None) -> "Steps[Any]":
        m = i.read()  # @line L9
        yield None
        if isinstance(m, CNode):  # @line L10
            flag, pos = self._flagpos(sn.hash, lev, m.bmp)
            if not m.bmp & flag:
                ok = i.cas(m, m.inserted(pos, flag, sn))
                yield None
                return "OK" if ok else RESTART
            b = m.array[pos]  # @line L11
            if isinstance(b, INode):
                return (yield from self._iinsert(b, sn, lev + self.w, i))
            n = sn if b.key == sn.key else INode(self._dual(b, sn, lev + self.w))  # @line L12
            ok = i.cas(m, m.updated(pos, n))  # @line L13
            yield None
            return "OK" if ok else RESTART
        if isinstance(m, TNode):  # @line L14
            yield from self._clean_steps(parent, lev - self.w)
            return RESTART
        rest = tuple(x for x in m.sns if x.key != sn.key)  # @line L15
        ok = i.cas(m, LNode((sn,) + rest))
        yield None
        return "OK" if ok else RESTART

    # ---- remove ----

    def remove_steps(self, key: Hashable) -> "Steps[Any]":
        h = self._hash(key)
        while True:
            r = yield from self._iremove(self.root, key, h, 0, None)  # @line L16
            if r is not RESTART:
                return r

    def _iremove(self, i: INode, key: Hashable, h: int, lev: int, parent: INode | None) -> "Steps[Any]":
        m = i.read()  # @line L17
        yield None
        if isinstance(m, CNode):  # @line L18
            flag, pos = self._flagpos(h, lev, m.bmp)
            if not m.bmp & flag:
                return NOTFOUND
            b = m.array[pos]
            if isinstance(b, INode):  # @line L19
                r = yield from self._iremove(b, key, h, lev + self.w, i)
            elif b.key != key:  # @line L20
                r = NOTFOUND
            else:
                ok = i.cas(m, self._contract(m.removed(pos, flag), lev))  # @line L21
                yield None
                r = b.value if ok else RESTART
            if r is not NOTFOUND and r is not RESTART:  # @line L22
                im = i.read()
                yield None
                if isinstance(im, TNode):
                    yield from self._clean_parent_steps(parent, i, h, lev - self.w)
            return r  # @line L23
        if isinstance(m, TNode):  # @line L24
            yield from self._clean_steps(parent, lev - self.w)
            return RESTART
        v = m.find(key)  # @line L25
        if v is NOTFOUND:
            return NOTFOUND
        rest = tuple(x for x in m.sns if x.key != key)
        new = TNode(rest[0]) if len(rest) == 1 else LNode(rest)
        ok = i.cas(m, new)
        yield None
        return v if ok else RESTART

    # ---- plain methods and checks ----

    def lookup(self, key: Hashable) -> Any:
        return run(self.lookup_steps(key))

    def insert(self, key: Hashable, value: Any) -> None:
        run(self.insert_steps(key, value))

    def remove(self, key: Hashable) -> Any:
        return run(self.remove_steps(key))

    def items(self) -> dict[Hashable, Any]:
        """The abstract map: every S-node reachable from the root. Checks the shape on the way."""
        out: dict[Hashable, Any] = {}

        def add(sn: SNode, lev: int, prefix: int) -> None:
            assert sn.hash & ((1 << lev) - 1) == prefix, "key on the wrong path"
            assert sn.key not in out, "duplicate key"
            out[sn.key] = sn.value

        def walk(i: INode, lev: int, prefix: int) -> None:
            m = i.read()
            if isinstance(m, CNode):
                assert len(m.array) == bin(m.bmp).count("1")
                idxs = [k for k in range(self.mask + 1) if m.bmp >> k & 1]
                for idx, b in zip(idxs, m.array):
                    p2 = prefix | (idx << lev)
                    if isinstance(b, INode):
                        walk(b, lev + self.w, p2)
                    else:
                        add(b, lev + self.w, p2)
            elif isinstance(m, TNode):
                assert lev > 0, "a tomb at the root"
                add(m.sn, lev, prefix)
            else:
                assert lev >= self.hbits and len(m.sns) >= 2
                for sn in m.sns:
                    add(sn, self.hbits, prefix & ((1 << self.hbits) - 1))

        walk(self.root, 0, 0)
        return out
