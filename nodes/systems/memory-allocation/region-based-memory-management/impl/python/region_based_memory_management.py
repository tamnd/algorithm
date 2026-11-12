# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/region-based-memory-management/. The authors are listed in prov/M2QAS8.jsonl.

"""Region-based memory management for a tiny first-order language.

The language is a fragment of the region calculus of Tofte and Talpin, with no
functions, so the types need no effects:

    e ::= ("int", k) | ("var", x) | ("let", x, e1, e2)
        | ("pair", e1, e2, r)        allocate a pair in region r
        | ("fst", e) | ("snd", e)    read a pair
        | ("letregion", r, e)        make region r, run e, free r

check(e) is the type checker. Its letregion rule says that region r must not
occur in the type of the body, so no pointer into r can leave the scope of r.
run(e) is the runtime: a stack of regions, each a bump-allocated block list.
letregion pushes a region and pops it, with all its pairs, at the end of e.
Both work with explicit stacks, not recursion.
"""

Type = object  # "int" or ("pair", t1, t2, r)


class RegionError(Exception):
    """The checker rejects the program."""


class DanglingAccess(Exception):
    """The program reads a pair in a region that is already freed."""


def regions_of(t: Type) -> set[str]:
    out: set[str] = set()
    stack = [t]
    while stack:
        t = stack.pop()
        if t != "int":
            _, t1, t2, r = t
            out.add(r)
            stack += [t1, t2]
    return out


def check(e: tuple) -> Type:
    """Return the type of the closed program e, or raise RegionError."""
    types: list[Type] = []
    work: list[tuple] = [("check", e, {}, frozenset())]
    while work:
        item = work.pop()
        tag = item[0]
        if tag == "check":
            _, e, env, live = item
            op = e[0]
            if op == "int":
                types.append("int")
            elif op == "var":
                if e[1] not in env:
                    raise RegionError(f"unbound variable {e[1]}")
                types.append(env[e[1]])
            elif op == "let":
                work.append(("bind", e[1], e[3], env, live))
                work.append(("check", e[2], env, live))
            elif op == "pair":
                if e[3] not in live:
                    raise RegionError(f"region {e[3]} is not in scope")
                work.append(("mkpair", e[3]))
                work.append(("check", e[2], env, live))
                work.append(("check", e[1], env, live))
            elif op in ("fst", "snd"):
                work.append(("proj", 1 if op == "fst" else 2))
                work.append(("check", e[1], env, live))
            elif op == "letregion":
                if e[1] in live:
                    raise RegionError(f"region {e[1]} is already in scope")
                work.append(("endregion", e[1]))
                work.append(("check", e[2], env, live | {e[1]}))  # @line L1
            else:
                raise RegionError(f"unknown form {op}")
        elif tag == "bind":
            _, x, body, env, live = item
            work.append(("check", body, {**env, x: types.pop()}, live))
        elif tag == "mkpair":
            t2, t1 = types.pop(), types.pop()
            types.append(("pair", t1, t2, item[1]))
        elif tag == "proj":
            t = types.pop()
            if t == "int":
                raise RegionError("fst or snd of an integer")
            types.append(t[item[1]])
        else:  # endregion: the letregion rule
            if item[1] in regions_of(types[-1]):  # @line L2
                raise RegionError(f"region {item[1]} escapes in the type {types[-1]}")
    return types.pop()


class Runtime:
    """A stack of regions. A pointer is (region number, offset in words)."""

    def __init__(self) -> None:
        self.stack: list[int] = []  # numbers of the live regions, oldest first
        self.cells: dict[int, list] = {}  # region number -> its words
        self.next_region = 0
        self.live_words = self.peak_words = self.freed_regions = 0

    def push_region(self) -> int:
        k = self.next_region
        self.next_region += 1
        self.stack.append(k)
        self.cells[k] = []
        return k

    def pop_region(self, k: int) -> None:
        if self.stack[-1] != k:
            raise AssertionError("regions are freed in LIFO order")
        self.stack.pop()
        self.live_words -= len(self.cells.pop(k))  # free the whole region at once
        self.freed_regions += 1

    def alloc_pair(self, k: int, v1: object, v2: object) -> tuple:
        words = self.cells[k]
        p = ("ptr", k, len(words))  # @line L6
        words += [v1, v2]
        self.live_words += 2
        self.peak_words = max(self.peak_words, self.live_words)
        return p

    def read(self, p: tuple, i: int) -> object:
        _, k, off = p
        if k not in self.cells:
            raise DanglingAccess(f"read of region {k} after it was freed")
        return self.cells[k][off + i - 1]


def run(e: tuple, rt: Runtime | None = None) -> object:
    """Evaluate the closed program e with a stack of regions."""
    rt = rt or Runtime()
    vals: list[object] = []
    work: list[tuple] = [("eval", e, {}, {})]
    while work:
        item = work.pop()
        tag = item[0]
        if tag == "eval":
            _, e, env, regs = item
            op = e[0]
            if op == "int":
                vals.append(e[1])
            elif op == "var":
                vals.append(env[e[1]])
            elif op == "let":
                work.append(("bind", e[1], e[3], env, regs))
                work.append(("eval", e[2], env, regs))
            elif op == "pair":
                work.append(("mkpair", regs[e[3]]))
                work.append(("eval", e[2], env, regs))
                work.append(("eval", e[1], env, regs))
            elif op in ("fst", "snd"):
                work.append(("proj", 1 if op == "fst" else 2))
                work.append(("eval", e[1], env, regs))
            else:  # letregion
                k = rt.push_region()  # @line L3
                work.append(("pop", k))
                work.append(("eval", e[2], env, {**regs, e[1]: k}))  # @line L4
        elif tag == "bind":
            _, x, body, env, regs = item
            work.append(("eval", body, {**env, x: vals.pop()}, regs))
        elif tag == "mkpair":
            v2, v1 = vals.pop(), vals.pop()
            vals.append(rt.alloc_pair(item[1], v1, v2))
        elif tag == "proj":
            vals.append(rt.read(vals.pop(), item[1]))
        else:  # pop: the end of a letregion frees its region
            rt.pop_region(item[1])  # @line L5
    return vals.pop()
