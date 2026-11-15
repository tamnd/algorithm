# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/burs/. The authors are listed in prov/VPX7R8.jsonl.

import random

from burs import RULES, Burs, evaluate, run


def random_tree(rng: random.Random, size: int) -> tuple:
    """A random tree with exactly size nodes."""
    if size == 1:
        if rng.random() < 0.5:
            return ("CONST", rng.randint(0, 9))
        return ("VAR", rng.choice("abc"))
    if size == 2 or rng.random() < 0.25:
        return ("MEM", random_tree(rng, size - 1))
    left = rng.randint(1, size - 2)
    return (rng.choice(["ADD", "ADD", "MUL"]), random_tree(rng, left), random_tree(rng, size - 1 - left))


def holes(p: object, n: tuple) -> list | None:
    """The subtrees under the register holes of p at n, or None."""
    if p == "reg":
        return [n]
    if p == ("CONST",) or p == ("VAR",):
        return [] if n[0] == p[0] else None
    if n[0] != p[0]:
        return None
    out: list = []
    for q, c in zip(p[1:], n[1:]):
        m = holes(q, c)
        if m is None:
            return None
        out += m
    return out


def tilings(t: tuple, rules: list) -> list[int]:
    """The cost of every tiling of t."""
    res = []
    for _, p, cost in rules:
        hs = holes(p, t)
        if hs is None:
            continue
        partial = [cost]
        for h in hs:
            partial = [x + y for x in partial for y in tilings(h, rules)]
        res += partial
    return res


def dp(t: tuple, rules: list) -> int:
    """The least tiling cost, by dynamic programming at compile time."""
    best = None
    for _, p, cost in rules:
        hs = holes(p, t)
        if hs is not None:
            c = cost + sum(dp(h, rules) for h in hs)
            best = c if best is None else min(best, c)
    return best


def test_example() -> None:
    b = Burs()
    t = ("MEM", ("ADD", ("MUL", ("VAR", "a"), ("VAR", "b")), ("VAR", "c")))
    code, cost = b.generate(t)
    assert cost == 14 == min(tilings(t, RULES))
    assert [RULES[ins[0]][0] for ins in code] == ["ld", "ld", "ld", "madd", "ldr"]
    env = {"a": 4, "b": 5, "c": 6}
    assert run(code, env) == evaluate(t, env) == 37


def test_tables() -> None:
    b = Burs()
    assert len(b.states) == 11
    for s in b.states:
        assert min(c for _, c, _ in s) == 0
    # every operator has an entry for every state or pair of states
    k = len(b.states)
    assert len(b.table) == 2 + k + 2 * k * k


def test_least_cost_on_small_trees() -> None:
    rng = random.Random(1988)
    b = Burs()
    for _ in range(400):
        t = random_tree(rng, rng.randint(1, 8))
        code, cost = b.generate(t)
        assert cost == min(tilings(t, RULES)) == dp(t, RULES)
        for _ in range(3):
            env = {x: rng.randint(-20, 20) for x in "abc"}
            assert run(code, env) == evaluate(t, env)


def test_large_trees_and_other_tables() -> None:
    rng = random.Random(1992)
    for rules in (RULES, RULES[:9], [r for r in RULES if r[0] != "ldx"]):
        b = Burs(rules)
        for _ in range(100):
            t = random_tree(rng, rng.randint(1, 40))
            code, cost = b.generate(t)
            assert cost == dp(t, rules)
            env = {x: rng.randint(-9, 9) for x in "abc"}
            assert run(code, env, rules) == evaluate(t, env)
