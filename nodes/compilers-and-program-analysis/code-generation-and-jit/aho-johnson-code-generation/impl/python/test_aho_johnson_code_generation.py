# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aho-johnson-code-generation/. The authors are listed in prov/10CJ5M.jsonl.

import heapq
import random

from aho_johnson_code_generation import RULES, STORE_COST, code_cost, evaluate, generate, run


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


def bushy_tree(rng: random.Random, size: int) -> tuple:
    """A random tree with size nodes and two children of near equal size.
    Such trees need many registers."""
    if size == 1:
        return ("VAR", rng.choice("abc")) if rng.random() < 0.7 else ("CONST", rng.randint(0, 9))
    if size == 2 or rng.random() < 0.15:
        return ("MEM", bushy_tree(rng, size - 1))
    left = (size - 1) // 2
    if rng.random() < 0.5:
        left = size - 1 - left
    return (rng.choice(["ADD", "MUL"]), bushy_tree(rng, left), bushy_tree(rng, size - 1 - left))


def tilings(t: tuple) -> list[int]:
    """The cost of every tiling of t, with no limit on registers.
    A memory operand of a pattern matches only a variable here."""

    def leaves(p: object, n: tuple) -> list | None:
        if p == "reg":
            return [n]
        if p == ("CONST",):
            return [] if n[0] == "CONST" else None
        if p == ("VAR",):
            return [] if n[0] == "VAR" else None
        if n[0] != p[0]:
            return None
        out: list = []
        for q, c in zip(p[1:], n[1:]):
            m = leaves(q, c)
            if m is None:
                return None
            out += m
        return out

    def all_costs(n: tuple) -> list[int]:
        res = []
        for _, p, cost in RULES:
            holes = leaves(p, n)
            if holes is None:
                continue
            partial = [cost]
            for h in holes:
                partial = [x + y for x in partial for y in all_costs(h)]
            res += partial
        return res

    return all_costs(t)


def min_program_cost(t: tuple, r: int) -> int:
    """Brute force: the cheapest program for t over all orders of instructions,
    stores and reloads, with at most r values in registers at each step."""
    nodes: list = []
    kids: list = []

    def walk(n: tuple) -> int:
        i = len(nodes)
        nodes.append(n)
        kids.append([])
        if n[0] not in ("CONST", "VAR"):
            kids[i] = [walk(c) for c in n[1:]]
        return i

    walk(t)
    m = len(nodes)

    def leaves(p: object, i: int) -> list | None:
        # (kind, node index) for the leaves of p, and ("inner", i) for covered nodes.
        if p == "reg":
            return [("reg", i)]
        if p == ("CONST",):
            return [("inner", i)] if nodes[i][0] == "CONST" else None
        if p == ("VAR",):
            return [("mem", i)]
        if nodes[i][0] != p[0]:
            return None
        out: list = []
        for q, c in zip(p[1:], kids[i]):
            x = leaves(q, c)
            if x is None:
                return None
            out += x
        return out

    # Status: 0 not computed, 1 in a register, 2 in memory, 3 used or covered.
    start = tuple(2 if n[0] == "VAR" else 0 for n in nodes)
    dist = {start: 0}
    pq = [(0, start)]
    while pq:
        d, s = heapq.heappop(pq)
        if d > dist[s]:
            continue
        if s[0] == 1:
            return d
        inreg = sum(1 for x in s if x == 1)
        nxt = []
        for i in range(m):
            if s[i] == 1:
                nxt.append((s[:i] + (2,) + s[i + 1:], STORE_COST))
            if s[i] == 2 and inreg < r:
                nxt.append((s[:i] + (1,) + s[i + 1:], RULES[1][2]))  # load
            if s[i] != 0:
                continue
            for _, p, cost in RULES:
                if p == ("VAR",):
                    continue
                lv = leaves(p, i)
                if lv is None:
                    continue
                ok = True
                new = list(s)
                for k, h in lv:
                    want = {"reg": (1,), "mem": (2,), "inner": (0,)}[k]
                    if s[h] not in want:
                        ok = False
                        break
                    new[h] = 3
                if not ok:
                    continue
                # the covered inner nodes of the pattern are also not computed
                cov = [i]
                stack = [(p, i)]
                while stack:
                    q, j = stack.pop()
                    if isinstance(q, tuple) and len(q) > 1:
                        for qq, c in zip(q[1:], kids[j]):
                            if isinstance(qq, tuple) and len(qq) > 1:
                                cov.append(c)
                            stack.append((qq, c))
                if any(s[c] != 0 for c in cov):
                    continue
                for c in cov:
                    new[c] = 3
                new[i] = 1
                if sum(1 for x in new if x == 1) <= r:
                    nxt.append((tuple(new), cost))
        for ns, c in nxt:
            if ns not in dist or dist[ns] > d + c:
                dist[ns] = d + c
                heapq.heappush(pq, (d + c, ns))
    raise AssertionError("no program")


def check_code(t: tuple, r: int, rng: random.Random) -> float:
    code, cost = generate(t, r)
    assert code_cost(code) == cost
    for _ in range(3):
        env = {v: rng.randint(-20, 20) for v in "abc"}
        assert run(code, env, r) == evaluate(t, env)
    return cost


def test_example() -> None:
    t = ("MEM", ("ADD", ("MUL", ("VAR", "a"), ("VAR", "b")), ("VAR", "c")))
    code, cost = generate(t, 3)
    assert cost == 14 == min(tilings(t))
    assert [RULES[ins[0]][0] for ins in code] == ["ld", "ld", "ld", "madd", "ldr"]
    code, cost = generate(t, 2)
    assert cost == 15 == min_program_cost(t, 2)
    env = {"a": 4, "b": 5, "c": 6}
    assert run(code, env, 2) == evaluate(t, env) == 37


def test_enough_registers_gives_the_cheapest_tiling() -> None:
    rng = random.Random(1976)
    for _ in range(300):
        size = rng.randint(1, 8)
        t = random_tree(rng, size)
        assert check_code(t, 8, rng) == min(tilings(t))


def test_few_registers_against_all_programs() -> None:
    rng = random.Random(488)
    spills = 0
    for _ in range(200):
        t = random_tree(rng, rng.randint(1, 8)) if rng.random() < 0.3 else bushy_tree(rng, rng.randint(5, 10))
        for r in (2, 3):
            assert check_code(t, r, rng) == min_program_cost(t, r)
            spills += any(ins[0] == "store" for ins in generate(t, r)[0])
    assert spills >= 30


def test_cost_falls_with_registers() -> None:
    rng = random.Random(5)
    for _ in range(100):
        t = random_tree(rng, rng.randint(1, 12))
        costs = [generate(t, r)[1] for r in range(2, 6)]
        assert all(x >= y for x, y in zip(costs, costs[1:]))
