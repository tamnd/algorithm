# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sethi-ullman-numbering/. The authors are listed in prov/HKPTPW.jsonl.

import random
from collections import deque
from functools import lru_cache

from sethi_ullman_numbering import evaluate, generate, label, run


def random_tree(rng: random.Random, inner: int) -> object:
    """A random expression tree with the given number of inner nodes."""
    if inner == 0:
        return rng.choice("abcd")
    left = rng.randint(0, inner - 1)
    return (rng.choice("+-*"), random_tree(rng, left), random_tree(rng, inner - 1 - left))


def flatten(e: object) -> tuple[list, list]:
    """Number the nodes. Return (kids, is_left) lists; node 0 is the root."""
    kids: list = []
    is_left: list = []

    def walk(n: object, left: bool) -> int:
        i = len(kids)
        kids.append(None)
        is_left.append(left)
        if not isinstance(n, str):
            kids[i] = (walk(n[1], True), walk(n[2], False))
        return i

    walk(e, True)
    return kids, is_left


def min_registers(e: object, memory_operands: bool = True) -> int:
    """Brute force: the smallest peak of live register values over all
    store-free evaluation orders, interleaved or not."""
    kids, _ = flatten(e)
    n = len(kids)
    parent = [-1] * n
    for i, ks in enumerate(kids):
        if ks:
            parent[ks[0]] = parent[ks[1]] = i

    def live(done: int) -> int:
        return sum(1 for u in range(n) if done >> u & 1 and (parent[u] < 0 or not done >> parent[u] & 1))

    @lru_cache(maxsize=None)
    def best(done: int) -> int:
        if done >> 0 & 1:
            return 0
        res = 10**9
        for v in range(n):
            if done >> v & 1:
                continue
            if kids[v] is None:
                nxt = done | 1 << v  # load a leaf
            else:
                a, b = kids[v]
                if not done >> a & 1:
                    continue
                if done >> b & 1:
                    nxt = done | 1 << v
                elif kids[b] is None and memory_operands:
                    nxt = done | 1 << v | 1 << b  # b is a memory operand
                else:
                    continue
            res = min(res, max(live(nxt), best(nxt)))
        return res

    return best(0)


def min_instructions(e: object, k: int) -> int:
    """Brute force: the fewest instructions of any program for e with k registers.

    Status of a node: 0 not computed, 1 in a register, 2 in memory,
    3 in both, 4 used by its parent. Leaves start in memory. Loads, stores
    and operations cost 1. Forgetting the register copy of a value that is
    also in memory costs 0.
    """
    kids, _ = flatten(e)
    n = len(kids)
    start = tuple(2 if ks is None else 0 for ks in kids)
    dist = {start: 0}
    dq = deque([start])
    while dq:
        s = dq.popleft()
        d = dist[s]
        if s[0] in (1, 3):
            return d
        regs = sum(1 for x in s if x in (1, 3))
        moves = []
        for v in range(n):
            x = s[v]
            if x == 2 and regs < k:
                moves.append((v, 3, 1))  # load
            if x == 1:
                moves.append((v, 3, 1))  # store
            if x == 3:
                moves.append((v, 2, 0))  # forget the register copy
            if x == 0 and kids[v] is not None:
                a, b = kids[v]
                if s[a] in (1, 3) and s[b] in (1, 2, 3):
                    t = list(s)
                    t[a] = t[b] = 4
                    t[v] = 1
                    moves.append((tuple(t), None, 1))
        for v, x, c in moves:
            if x is None:
                t = v
            else:
                t = s[:v] + (x,) + s[v + 1:]
            if t not in dist or dist[t] > d + c:
                dist[t] = d + c
                if c == 0:
                    dq.appendleft(t)
                else:
                    dq.append(t)
    raise AssertionError("no program")


def used_registers(code: list) -> int:
    regs = set()
    for ins in code:
        if ins[0] == "load":
            regs.add(ins[1])
        elif ins[0] in ("op", "opm"):
            regs.update(r for r in ins[2:5] if isinstance(r, int))
        else:
            regs.add(ins[2])
    return len(regs)


def test_example() -> None:
    # (a - b) * (c + (d - e)), the tree of the page.
    e = ("*", ("-", "a", "b"), ("+", "c", ("-", "d", "e")))
    assert label(e) == 2
    assert label(e, memory_operands=False) == 3
    code, stores = generate(e, 2)
    assert stores == 0
    assert code == [
        ("load", 0, "c"),
        ("load", 1, "d"),
        ("opm", "-", 1, 1, "e"),
        ("op", "+", 0, 0, 1),
        ("load", 1, "a"),
        ("opm", "-", 1, 1, "b"),
        ("op", "*", 0, 1, 0),
    ]
    env = {"a": 7, "b": 2, "c": 3, "d": 10, "e": 4}
    assert run(code, env, 2) == evaluate(e, env) == 45
    code1, stores1 = generate(e, 1)
    assert stores1 == 2 and len(code1) == 9 == min_instructions(e, 1)
    assert run(code1, env, 1) == 45
    assert len(code) == 7 == min_instructions(e, 2)


def test_leaf_and_chain() -> None:
    assert label("x") == 1
    chain = "a"
    for v in "bcdefg":
        chain = ("+", chain, v)
    assert label(chain) == 1
    code, stores = generate(chain, 1)
    assert stores == 0 and len(code) == 7


def test_label_is_minimum_register_count() -> None:
    rng = random.Random(1970)
    for _ in range(300):
        e = random_tree(rng, rng.randint(0, 5))
        assert label(e) == min_registers(e)
        assert label(e, False) == min_registers(e, False)
        code, stores = generate(e, label(e))
        assert stores == 0
        assert used_registers(code) == label(e)


def test_complete_trees_need_more_registers() -> None:
    e = "a"
    for depth in range(1, 6):
        e = ("+", e, e)
        assert label(e) == depth
        assert label(e, False) == depth + 1


def test_code_computes_the_value() -> None:
    rng = random.Random(7)
    for _ in range(400):
        e = random_tree(rng, rng.randint(0, 12))
        env = {v: rng.randint(-9, 9) for v in "abcd"}
        for k in range(1, 5):
            code, stores = generate(e, k)
            assert run(code, env, k) == evaluate(e, env)
            assert (stores == 0) == (label(e) <= k)


def test_fewest_instructions() -> None:
    rng = random.Random(1976)
    for _ in range(150):
        e = random_tree(rng, rng.randint(1, 6))
        for k in (1, 2, 3):
            code, _ = generate(e, k)
            assert len(code) == min_instructions(e, k)
