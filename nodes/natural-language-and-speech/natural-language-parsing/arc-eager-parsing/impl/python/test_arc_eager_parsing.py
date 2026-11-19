# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/arc-eager-parsing/. The authors are listed in prov/BSRJBW.jsonl.

import itertools
import random

import pytest

from arc_eager_parsing import (
    REDUCE,
    SHIFT,
    Config,
    apply,
    cost,
    dynamic_oracle,
    finish,
    is_legal,
    legal_transitions,
    oracle_sequence,
    parse,
    static_oracle,
)

GOLD_HEADS = [-1, 2, 3, 0, 6, 6, 3]  # the cat sat on the mat
GOLD_LABELS = [None, "det", "nsubj", "root", "case", "det", "obl"]


def is_tree(heads):
    n = len(heads) - 1
    for d in range(1, n + 1):
        x, steps = d, 0
        while x != 0:
            x, steps = heads[x], steps + 1
            if x == -1 or steps > n:
                return False
    return True


def is_projective(heads):
    n = len(heads) - 1
    for d in range(1, n + 1):
        h = heads[d]
        for k in range(min(h, d) + 1, max(h, d)):
            x = k
            while x != h and x != 0:
                x = heads[x]
            if x != h:
                return False
    return True


def all_trees(n):
    return [[-1] + list(hs) for hs in itertools.product(range(n + 1), repeat=n) if is_tree([-1] + list(hs))]


TREES = {n: all_trees(n) for n in range(1, 6)}
PROJ = {n: [t for t in TREES[n] if is_projective(t)] for n in TREES}


def all_complete_runs(n):
    out = []
    todo = [(Config(n), 0)]
    while todo:
        c, steps = todo.pop()
        if c.is_terminal():
            out.append((tuple(finish(c)[0]), steps))
            continue
        for t in legal_transitions(c, ["dep"]):
            c2 = c.copy()
            apply(c2, t)
            todo.append((c2, steps + 1))
    return out


def min_loss(c, gold, memo):
    """Brute force: the smallest Hamming loss of a tree reachable from c."""
    k = c.key()
    if k in memo:
        return memo[k]
    if c.is_terminal():
        heads, _ = finish(c)
        v = sum(1 for d in range(1, c.n + 1) if heads[d] != gold[d])
    else:
        v = None
        for t in legal_transitions(c, ["dep"]):
            c2 = c.copy()
            apply(c2, t)
            x = min_loss(c2, gold, memo)
            v = x if v is None else min(v, x)
    memo[k] = v
    return v


def reachable_configs(n):
    seen, out, todo = set(), [], [Config(n)]
    while todo:
        c = todo.pop()
        if c.key() in seen:
            continue
        seen.add(c.key())
        out.append(c)
        if not c.is_terminal():
            for t in legal_transitions(c, ["dep"]):
                c2 = c.copy()
                apply(c2, t)
                todo.append(c2)
    return out


CONFIGS = {n: reachable_configs(n) for n in range(1, 6)}


def test_example_sequence():
    seq = oracle_sequence(GOLD_HEADS, GOLD_LABELS)
    names = [t[0] if t[1] is None else f"{t[0]}-{t[1]}" for t in seq]
    assert names == ["SH", "LA-det", "SH", "LA-nsubj", "RA-root", "SH", "SH", "LA-det", "LA-case", "RA-obl"]


def test_sound_and_complete_for_projective_trees():
    for n in range(1, 6):
        runs = all_complete_runs(n)
        assert {h for h, _ in runs} == {tuple(t) for t in PROJ[n]}
        assert all(n <= steps <= 2 * n for _, steps in runs)
        assert max(steps for _, steps in runs) == 2 * n - 1 if n > 1 else True


def test_static_oracle_succeeds_exactly_on_projective_trees():
    for n in range(1, 6):
        for heads in TREES[n]:
            if is_projective(heads):
                assert len(oracle_sequence(heads)) <= 2 * n
            else:
                with pytest.raises(ValueError):
                    oracle_sequence(heads)


def check_costs(n, gold):
    memo = {}
    for c in CONFIGS[n]:
        if c.is_terminal():
            continue
        base = min_loss(c, gold, memo)
        zero = 0
        for t in legal_transitions(c, ["dep"]):
            c2 = c.copy()
            apply(c2, t)
            brute = min_loss(c2, gold, memo) - base
            assert cost(c, t, gold) == brute, (c.key(), t, gold)
            zero += brute == 0
        assert zero >= 1


def test_dynamic_oracle_cost_equals_brute_force_small():
    for n in range(1, 5):
        for gold in PROJ[n]:
            check_costs(n, gold)


def test_dynamic_oracle_cost_equals_brute_force_n5():
    rng = random.Random(4)
    for gold in rng.sample(PROJ[5], 12):
        check_costs(5, gold)


def test_dynamic_oracle_recovers_after_an_error():
    # Take a wrong first step, then follow the dynamic oracle: the loss is the
    # smallest one still reachable.
    gold = GOLD_HEADS
    c = Config(6)
    apply(c, ("RA", "dep"))  # attaches "the" to the root: one gold arc is lost
    memo = {}
    best = min_loss(c, gold, memo)
    while not c.is_terminal():
        apply(c, dynamic_oracle(c, gold)[0])
    heads, _ = finish(c)
    assert sum(1 for d in range(1, 7) if heads[d] != gold[d]) == best == 1


def test_greedy_parse_and_preconditions():
    rng = random.Random(8)
    for _ in range(200):
        n = rng.randint(1, 8)
        heads, labels, seq = parse(n, lambda c, t: rng.random(), ["x"])
        assert n <= len(seq) <= 2 * n
        assert is_tree(heads) and is_projective(heads)
    c = Config(2)
    assert not is_legal(c, ("LA", "x"))  # s is the root
    assert not is_legal(c, REDUCE)  # the root never has a head
    apply(c, SHIFT)
    assert is_legal(c, ("LA", "x")) and not is_legal(c, REDUCE)
    apply(c, ("LA", "x"))
    apply(c, ("RA", "x"))
    assert c.is_terminal() and not is_legal(c, SHIFT)
    assert static_oracle(Config(1), [-1, 0], [None, "root"]) == ("RA", "root")
