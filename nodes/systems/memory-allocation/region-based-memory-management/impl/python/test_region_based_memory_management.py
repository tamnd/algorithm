# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/region-based-memory-management/. The authors are listed in prov/M2QAS8.jsonl.

import random

import pytest

from region_based_memory_management import DanglingAccess, RegionError, Runtime, check, run

# letregion r1 in
#   let p = (letregion r2 in let q = (1, 2) at r2 in (fst q, snd q) at r1) in
#   fst p
GOOD = (
    "letregion",
    "r1",
    (
        "let",
        "p",
        (
            "letregion",
            "r2",
            (
                "let",
                "q",
                ("pair", ("int", 1), ("int", 2), "r2"),
                ("pair", ("fst", ("var", "q")), ("snd", ("var", "q")), "r1"),
            ),
        ),
        ("fst", ("var", "p")),
    ),
)

# letregion r1 in let p = (letregion r2 in (1, 2) at r2) in fst p
BAD = (
    "letregion",
    "r1",
    (
        "let",
        "p",
        ("letregion", "r2", ("pair", ("int", 1), ("int", 2), "r2")),
        ("fst", ("var", "p")),
    ),
)


def test_worked_example() -> None:
    assert check(GOOD) == "int"
    rt = Runtime()
    assert run(GOOD, rt) == 1
    assert rt.peak_words == 4 and rt.live_words == 0
    assert rt.freed_regions == 2 and rt.stack == []
    with pytest.raises(RegionError):
        check(BAD)  # r2 occurs in the type of the inner letregion
    with pytest.raises(DanglingAccess):
        run(BAD)  # the pair is read after r2 is freed


def test_checker_errors() -> None:
    with pytest.raises(RegionError):
        check(("pair", ("int", 1), ("int", 2), "r"))  # r is not in scope
    with pytest.raises(RegionError):
        check(("letregion", "r", ("letregion", "r", ("int", 0))))
    with pytest.raises(RegionError):
        check(("fst", ("int", 3)))
    with pytest.raises(RegionError):
        check(("var", "x"))


def gen(rng: random.Random, depth: int, vars_: list[str], regs: list[str]) -> tuple:
    """A random program; it may be ill-typed or have regions out of scope."""
    if depth == 0:
        if vars_ and rng.random() < 0.6:
            return ("var", rng.choice(vars_))
        return ("int", rng.randrange(10))
    c = rng.randrange(6)
    if c == 0:
        x = f"x{len(vars_)}"
        return ("let", x, gen(rng, depth - 1, vars_, regs), gen(rng, depth - 1, vars_ + [x], regs))
    if c == 1 and regs:
        r = rng.choice(regs + ["zz"]) if rng.random() < 0.1 else rng.choice(regs)
        return ("pair", gen(rng, depth - 1, vars_, regs), gen(rng, depth - 1, vars_, regs), r)
    if c == 2:
        return (rng.choice(["fst", "snd"]), gen(rng, depth - 1, vars_, regs))
    if c in (3, 4):
        r = f"r{len(regs)}"
        return ("letregion", r, gen(rng, depth - 1, vars_, regs + [r]))
    return gen(rng, depth - 1, vars_, regs)


def test_checked_programs_never_dangle() -> None:
    rng = random.Random(1997)
    accepted = dangling = 0
    for _ in range(4000):
        e = gen(rng, rng.randrange(1, 7), [], [])
        try:
            check(e)
            ok = True
        except RegionError:
            ok = False
        rt = Runtime()
        try:
            run(e, rt)
            fault = None
        except DanglingAccess:
            fault = "dangling"
        except (TypeError, KeyError, IndexError):
            fault = "type"  # an ill-typed program went wrong in another way
        if ok:
            accepted += 1
            assert fault is None  # well-checked programs never read a freed region
            assert rt.stack == [] and rt.live_words == 0  # every region was freed
        if fault == "dangling":
            dangling += 1
            assert not ok
    assert accepted > 500 and dangling > 20
