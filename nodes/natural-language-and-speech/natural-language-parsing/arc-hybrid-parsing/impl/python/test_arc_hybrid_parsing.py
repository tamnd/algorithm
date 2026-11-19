# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/arc-hybrid-parsing/. The authors are listed in prov/TTAZ45.jsonl.

import itertools
import random

import pytest

from arc_hybrid_parsing import (
    SHIFT,
    Config,
    apply,
    cost,
    count_dp,
    dynamic_oracle,
    is_legal,
    legal_transitions,
    oracle_sequence,
    parse,
    viterbi_dp,
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
            out.append((tuple(c.heads), steps))
            continue
        for t in legal_transitions(c, ["dep"]):
            c2 = c.copy()
            apply(c2, t)
            todo.append((c2, steps + 1))
    return out


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


def min_loss(c, gold, memo):
    k = c.key()
    if k in memo:
        return memo[k]
    if c.is_terminal():
        v = sum(1 for d in range(1, c.n + 1) if c.heads[d] != gold[d])
    else:
        v = None
        for t in legal_transitions(c, ["dep"]):
            c2 = c.copy()
            apply(c2, t)
            x = min_loss(c2, gold, memo)
            v = x if v is None else min(v, x)
    memo[k] = v
    return v


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


def test_example_sequence():
    seq = oracle_sequence(GOLD_HEADS, GOLD_LABELS)
    names = [t[0] if t[1] is None else f"{t[0]}-{t[1]}" for t in seq]
    assert names == ["SH", "LA-det", "SH", "LA-nsubj", "SH", "SH", "SH", "LA-det", "LA-case", "SH", "RA-obl", "RA-root"]


def test_sound_and_complete_for_projective_trees():
    for n in range(1, 6):
        runs = all_complete_runs(n)
        assert {h for h, _ in runs} == {tuple(t) for t in PROJ[n]}
        assert all(steps == 2 * n for _, steps in runs)
        # The deduction system counts computations, not trees.
        assert count_dp(n) == len(runs)
    assert [count_dp(n) for n in range(1, 6)] == [1, 3, 13, 67, 381]


def test_spurious_ambiguity():
    # 0 -> 1, 0 -> 3, 3 -> 2: RIGHT-ARC 0 -> 1 can come before or after LEFT-ARC 3 -> 2.
    runs = [h for h, _ in all_complete_runs(3) if h == (-1, 0, 3, 0)]
    assert len(runs) == 2


def test_static_oracle_succeeds_exactly_on_projective_trees():
    for n in range(1, 6):
        for heads in TREES[n]:
            if is_projective(heads):
                assert len(oracle_sequence(heads)) == 2 * n
            else:
                with pytest.raises(ValueError):
                    oracle_sequence(heads)


def test_dynamic_oracle_cost_equals_brute_force_small():
    for n in range(1, 5):
        for gold in PROJ[n]:
            check_costs(n, gold)


def test_dynamic_oracle_cost_equals_brute_force_n5():
    rng = random.Random(6)
    for gold in rng.sample(PROJ[5], 12):
        check_costs(5, gold)


def test_dynamic_oracle_after_an_error():
    gold = GOLD_HEADS
    c = Config(6)
    apply(c, SHIFT)
    apply(c, SHIFT)  # "the" can no longer get its head "cat": one gold arc is lost
    best = min_loss(c, gold, {})
    while not c.is_terminal():
        apply(c, dynamic_oracle(c, gold)[0])
    assert sum(1 for d in range(1, 7) if c.heads[d] != gold[d]) == best == 1


def test_viterbi_dp_against_brute_force():
    rng = random.Random(10)
    for n in range(1, 6):
        for _ in range(20 if n < 5 else 8):
            s = [[rng.randint(-9, 9) for _ in range(n + 1)] for _ in range(n + 1)]
            best = max(sum(s[t[d]][d] for d in range(1, n + 1)) for t in PROJ[n])
            score, heads = viterbi_dp(s)
            assert score == best
            assert is_tree(heads) and is_projective(heads)
            assert sum(s[heads[d]][d] for d in range(1, n + 1)) == score


def test_greedy_and_preconditions():
    rng = random.Random(12)
    for _ in range(200):
        n = rng.randint(1, 8)
        heads, _, seq = parse(n, lambda c, t: rng.random(), ["x"])
        assert len(seq) == 2 * n and is_tree(heads) and is_projective(heads)
    c = Config(1)
    assert not is_legal(c, ("LA", "x")) and not is_legal(c, ("RA", "x"))
    apply(c, SHIFT)
    assert not is_legal(c, SHIFT) and not is_legal(c, ("LA", "x")) and is_legal(c, ("RA", "x"))
