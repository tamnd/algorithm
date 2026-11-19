# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/arc-standard-parsing/. The authors are listed in prov/D0MMXM.jsonl.

import itertools
import random

import pytest

from arc_standard_parsing import (
    SHIFT,
    Config,
    apply,
    is_legal,
    legal_transitions,
    oracle_sequence,
    parse,
    run,
    static_oracle,
)

# the cat sat on the mat
SENT = ["the", "cat", "sat", "on", "the", "mat"]
GOLD_HEADS = [-1, 2, 3, 0, 6, 6, 3]
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


def all_complete_runs(n, single_root=False):
    """Brute force: every complete transition sequence (unlabeled), by depth-first search."""
    out = []
    todo = [(Config(n), [])]
    while todo:
        c, seq = todo.pop()
        if c.is_terminal():
            out.append((tuple(c.heads), seq))
            continue
        for t in legal_transitions(c, ["dep"], single_root):
            c2 = c.copy()
            apply(c2, t)
            todo.append((c2, seq + [t]))
    return out


def test_example_sequence():
    seq = oracle_sequence(GOLD_HEADS, GOLD_LABELS)
    names = [t[0] if t[1] is None else f"{t[0]}-{t[1]}" for t in seq]
    assert names == [
        "SH", "SH", "LA-det", "SH", "LA-nsubj", "SH", "SH", "SH", "LA-det", "LA-case", "RA-obl", "RA-root",
    ]
    c = run(6, seq)
    assert c.heads == GOLD_HEADS and c.labels == GOLD_LABELS


def test_oracle_succeeds_exactly_on_projective_trees():
    for n in range(1, 6):
        for heads in TREES[n]:
            if is_projective(heads):
                seq = oracle_sequence(heads)
                assert len(seq) == 2 * n
            else:
                with pytest.raises(ValueError):
                    oracle_sequence(heads)


@pytest.mark.parametrize("single_root", [False, True])
def test_sound_and_complete_for_projective_trees(single_root):
    for n in range(1, 6):
        runs = all_complete_runs(n, single_root)
        built = {heads for heads, _ in runs}
        expected = {
            tuple(t) for t in TREES[n]
            if is_projective(t) and (not single_root or t[1:].count(0) == 1)
        }
        assert built == expected
        assert all(len(seq) == 2 * n for _, seq in runs)
    counts = [len({h for h, _ in all_complete_runs(n, single_root)}) for n in range(1, 6)]
    assert counts == ([1, 2, 7, 30, 143] if single_root else [1, 3, 12, 55, 273])


def test_spurious_ambiguity():
    # a h b with h the root child: the two arcs of h can be built in either order.
    runs = [seq for heads, seq in all_complete_runs(3) if heads == (-1, 2, 0, 2)]
    assert len(runs) == 2


def test_greedy_with_oracle_scores_rebuilds_gold():
    rng = random.Random(1)
    labels = ["a", "b", "c"]
    for n in range(1, 7):
        for _ in range(20):
            heads = [-1] + [rng.randint(0, n) for _ in range(n)]
            if not is_tree(heads) or not is_projective(heads):
                continue
            gl = [None] + [rng.choice(labels) for _ in range(n)]

            def score(c, t, heads=heads, gl=gl):
                return 1.0 if t == static_oracle(c, heads, gl) else 0.0

            got_heads, got_labels, seq = parse(n, score, labels)
            assert got_heads == heads and got_labels == gl
            assert seq == oracle_sequence(heads, gl)


def test_greedy_random_scores_give_projective_trees():
    rng = random.Random(2)
    for _ in range(200):
        n = rng.randint(1, 8)
        heads, labels, seq = parse(n, lambda c, t: rng.random(), ["x", "y"])
        assert len(seq) == 2 * n
        assert is_tree(heads) and is_projective(heads)


def test_greedy_is_not_exact():
    # Arc-factored scores; SHIFT scores 0. Greedy attaches word 1 to the root at
    # once (score 1 > 0), so word 1 can no longer take its dependents 2 and 3.
    s = [[0, 1, 0, 0], [0, 0, 5, 5], [0, 3, 0, 0], [0, 0, 0, 0]]

    def score(c, t):
        if t[0] == "SH":
            return 0.0
        s1, s0 = c.stack[-2], c.stack[-1]
        return s[s0][s1] if t[0] == "LA" else s[s1][s0]

    heads, _, _ = parse(3, score)
    greedy = sum(s[heads[d]][d] for d in range(1, 4))
    best = max(sum(s[t[d]][d] for d in range(1, 4)) for t in TREES[3] if is_projective(t))
    assert best == 11
    assert greedy < best


def test_preconditions():
    c = Config(2)
    assert not is_legal(c, ("LA", "x")) and not is_legal(c, ("RA", "x"))
    apply(c, SHIFT)
    assert not is_legal(c, ("LA", "x"))  # s1 is the root
    assert is_legal(c, ("RA", "x"))
    assert not is_legal(c, ("RA", "x"), single_root=True)  # buffer not empty
    with pytest.raises(ValueError):
        run(2, [("LA", "x")])
