# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/swap-transition-system/. The authors are listed in prov/CCPJNB.jsonl.

import heapq
import itertools
import random

from swap_transition_system import (
    SHIFT,
    SWAP,
    Config,
    apply,
    is_legal,
    legal_transitions,
    oracle_sequence,
    parse,
    projective_order,
)

# A hearing is scheduled on the issue today
HEARING = [-1, 2, 3, 0, 3, 2, 7, 5, 4]


def is_tree(heads):
    n = len(heads) - 1
    for d in range(1, n + 1):
        x, steps = d, 0
        while x != 0:
            x, steps = heads[x], steps + 1
            if x == -1 or steps > n:
                return False
    return True


def is_projective_under(heads, pos):
    """Projectivity of the tree when word w is placed at position pos[w]."""
    n = len(heads) - 1
    at = sorted(range(n + 1), key=lambda w: pos[w])
    for d in range(1, n + 1):
        h = heads[d]
        lo, hi = sorted((pos[h], pos[d]))
        for k in at[lo + 1:hi]:
            x = k
            while x != h and x != 0:
                x = heads[x]
            if x != h:
                return False
    return True


def all_trees(n):
    return [[-1] + list(hs) for hs in itertools.product(range(n + 1), repeat=n) if is_tree([-1] + list(hs))]


TREES = {n: all_trees(n) for n in range(1, 6)}


def key(c):
    return (tuple(c.stack), tuple(c.buffer), tuple(c.heads))


def terminal_trees(n):
    """All trees in terminal configurations reachable from the start, by search."""
    seen, out, todo = set(), set(), [Config(n)]
    while todo:
        c = todo.pop()
        if key(c) in seen:
            continue
        seen.add(key(c))
        if c.is_terminal():
            out.add(tuple(c.heads))
            continue
        for t in legal_transitions(c, ["dep"]):
            c2 = c.copy()
            apply(c2, t)
            todo.append(c2)
    return out


def min_swaps(gold):
    """The fewest swaps of any sequence that builds the gold tree (search by swaps)."""
    n = len(gold) - 1
    tie = itertools.count()
    pq = [(0, next(tie), Config(n))]
    seen = set()
    while pq:
        k, _, c = heapq.heappop(pq)
        if key(c) in seen:
            continue
        seen.add(key(c))
        if c.is_terminal():
            return k
        for t in legal_transitions(c, ["dep"]):
            if t[0] in ("LA", "RA"):
                s1, s0 = c.stack[-2], c.stack[-1]
                if (t[0] == "LA" and gold[s1] != s0) or (t[0] == "RA" and gold[s0] != s1):
                    continue
            c2 = c.copy()
            apply(c2, t)
            heapq.heappush(pq, (k + (t[0] == "SW"), next(tie), c2))
    raise AssertionError("no sequence")


def test_projective_order():
    pos = projective_order(HEARING)
    assert sorted(range(9), key=lambda w: pos[w]) == [0, 1, 2, 5, 6, 7, 3, 4, 8]
    for n in range(1, 6):
        for heads in TREES[n]:
            assert is_projective_under(heads, projective_order(heads))


def test_example_sequence():
    seq = oracle_sequence(HEARING)
    assert seq.count(SWAP) == 6 and len(seq) == 28
    assert min_swaps(HEARING) == 2


def test_oracle_builds_every_tree():
    # The search for the least number of swaps is slow, so for n = 5 it runs
    # on a fixed sample of 150 of the 1296 trees; the other checks run on all.
    sample = set(map(tuple, random.Random(7).sample(TREES[5], 150)))
    for n in range(1, 6):
        for heads in TREES[n]:
            seq = oracle_sequence(heads)  # raises if the tree is not built
            k = seq.count(SWAP)
            assert len(seq) == 2 * n + 2 * k
            assert k <= n * (n - 1) // 2 and len(seq) <= n + n * n
            pos = projective_order(heads)
            inversions = sum(1 for a in range(1, n + 1) for b in range(a + 1, n + 1) if pos[a] > pos[b])
            assert k <= inversions
            if n <= 4 or tuple(heads) in sample:
                assert min_swaps(heads) <= k
            if inversions == 0:
                assert k == 0


def test_sound_and_complete():
    for n in range(1, 5):
        assert terminal_trees(n) == {tuple(t) for t in TREES[n]}


def test_greedy_terminates_with_a_tree():
    rng = random.Random(3)
    for _ in range(300):
        n = rng.randint(1, 9)
        heads, labels, seq = parse(n, lambda c, t: rng.random(), ["x"])
        assert is_tree(heads)
        k = seq.count(SWAP)
        assert len(seq) == 2 * n + 2 * k <= n + n * n


def test_preconditions():
    c = Config(2)
    assert is_legal(c, SHIFT) and not is_legal(c, SWAP) and not is_legal(c, ("RA", "x"))
    apply(c, SHIFT)
    assert not is_legal(c, ("LA", "x")) and not is_legal(c, SWAP) and is_legal(c, ("RA", "x"))
    apply(c, SHIFT)
    assert is_legal(c, SWAP)
    apply(c, SWAP)
    assert c.stack == [0, 2] and c.buffer == [1]
    apply(c, SHIFT)
    assert not is_legal(c, SWAP)  # 2 > 1: the same pair cannot be swapped back
