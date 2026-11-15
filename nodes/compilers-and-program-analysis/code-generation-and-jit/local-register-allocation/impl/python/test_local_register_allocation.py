# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/local-register-allocation/. The authors are listed in prov/A84DF7.jsonl.

import random
from functools import lru_cache

from local_register_allocation import LOAD_COST, allocate, steps
from toyir import Block, Program, parse, run


def random_block(rng: random.Random, n: int) -> Program:
    """A block of n instructions over the parameters a, b, c and the names x0 .. x3."""
    names = ["a", "b", "c"]
    instrs = []
    for _ in range(n):
        x = "x%d" % rng.randrange(4)
        r = rng.random()
        if r < 0.1:
            instrs.append(("const", x, rng.randint(0, 9)))
        elif r < 0.2:
            instrs.append(("copy", x, rng.choice(names)))
        else:
            b = rng.choice(names) if rng.random() < 0.85 else rng.randint(1, 5)
            instrs.append(("op", x, rng.choice("+-*"), rng.choice(names), b))
        if x not in names:
            names.append(x)
    return Program(["a", "b", "c"], {"entry": Block(instrs, ("ret", rng.choice(names)))})


def best_cost(prog: Program, k: int, store_cost: int) -> int:
    """Brute force over every choice of the register to free, at every step
    where no register is free."""
    (block,) = prog.blocks.values()
    st = steps(block)

    @lru_cache(maxsize=None)
    def go(s: int, regs: frozenset, dirty: frozenset) -> int:
        if s == len(st):
            return 0
        kind, v = st[s][0], st[s][1]
        if kind == "drop":
            return go(s + 1, regs - {v}, dirty - {v})
        if kind == "use" and v in regs:
            return go(s + 1, regs, dirty)
        here = LOAD_COST if kind == "use" else 0
        new_dirty = dirty | {v} if kind == "def" else dirty
        if len(regs) < k:
            return here + go(s + 1, regs | {v}, new_dirty)
        pinned = st[s][2] if kind == "use" else ()
        best = None
        for w in regs:
            if w in pinned:
                continue
            c = here + (store_cost if w in dirty else 0)
            c += go(s + 1, (regs - {w}) | {v}, (new_dirty - {w}))
            best = c if best is None else min(best, c)
        return best

    return go(0, frozenset(), frozenset())


def check_runs(prog: Program, out: Program, k: int, rng: random.Random) -> None:
    (code,) = out.blocks.values()
    for ins in code.instrs:
        for a in ins[1:]:
            if isinstance(a, str) and a not in ("+", "-", "*"):
                assert a.startswith("mem.") or int(a[1:]) < k
    for _ in range(3):
        args = [rng.randint(-9, 9) for _ in prog.params]
        assert run(out, args) == run(prog, args)


def test_example() -> None:
    prog = parse(
        """
        # params: a, b, c, d
        entry:
          t = a + b
          u = c + d
          v = t * u
          w = v - a
          ret w
        """
    )
    out, cost = allocate(prog, 2)
    assert cost == best_cost(prog, 2, 1) == 7
    (code,) = out.blocks.values()
    assert sum(1 for ins in code.instrs if ins[0] == "copy" and ins[1] == "mem.t") == 1
    assert run(out, [1, 2, 3, 4]) == run(prog, [1, 2, 3, 4]) == ("ret", 20)
    out, cost = allocate(prog, 3)
    assert cost == best_cost(prog, 3, 1) == 5


def test_belady_is_optimal_when_stores_are_free() -> None:
    rng = random.Random(1966)
    for _ in range(300):
        prog = random_block(rng, rng.randint(1, 8))
        for k in (2, 3):
            out, cost = allocate(prog, k, store_cost=0)
            assert cost == best_cost(prog, k, 0)
            check_runs(prog, out, k, rng)


def test_dirty_values() -> None:
    rng = random.Random(2000)
    worse = 0
    for _ in range(300):
        prog = random_block(rng, rng.randint(1, 8))
        for k in (2, 3):
            out, cost = allocate(prog, k)
            best = best_cost(prog, k, 1)
            assert cost >= best
            worse += cost > best
            check_runs(prog, out, k, rng)
    assert worse > 0


def test_belady_is_not_optimal_with_dirty_values() -> None:
    prog = parse(
        """
        # params: a, b
        entry:
          t = b + 1
          u = b + t
          u = u * a
          t = b * t
          v = t * u
          ret v
        """
    )
    out, cost = allocate(prog, 3)
    assert run(out, [3, 5]) == run(prog, [3, 5])
    # Belady frees the register of t, which is dirty: one store and one load.
    # Freeing b, which is clean, costs one load.
    assert cost == 4
    assert best_cost(prog, 3, 1) == 3
    assert allocate(prog, 3, store_cost=0)[1] == best_cost(prog, 3, 0) == 3
