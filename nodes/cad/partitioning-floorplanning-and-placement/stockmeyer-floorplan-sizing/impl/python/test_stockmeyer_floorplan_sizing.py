# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stockmeyer-floorplan-sizing/. The authors are listed in prov/RH6JHQ.jsonl.

import itertools
import random

from stockmeyer_floorplan_sizing import merge_h, merge_v, pareto, shape_lists, stockmeyer_sizing


def evaluate(tokens: list, size: dict) -> tuple[int, int]:
    """Width and height of a Polish expression with one fixed shape per block."""
    st: list = []
    for t in tokens:
        if t == "V":
            b, a = st.pop(), st.pop()
            st.append((a[0] + b[0], max(a[1], b[1])))
        elif t == "H":
            b, a = st.pop(), st.pop()
            st.append((max(a[0], b[0]), a[1] + b[1]))
        else:
            st.append(size[t])
    return st[0]


def brute(tokens: list, shapes: dict) -> tuple[int, list]:
    """Least area and the non-dominated (W, H) pairs over all shape choices."""
    blocks = sorted(shapes)
    seen = set()
    for pick in itertools.product(*(range(len(shapes[b])) for b in blocks)):
        size = {b: shapes[b][k] for b, k in zip(blocks, pick)}
        seen.add(evaluate(tokens, size))
    front = sorted(p for p in seen if not any(q != p and q[0] <= p[0] and q[1] <= p[1] for q in seen))
    return min(w * h for w, h in seen), front


def random_tokens(rng: random.Random, leaves: list[int]) -> list:
    if len(leaves) == 1:
        return [leaves[0]]
    k = rng.randint(1, len(leaves) - 1)
    return random_tokens(rng, leaves[:k]) + random_tokens(rng, leaves[k:]) + [rng.choice("HV")]


def test_example() -> None:
    tokens = [1, 2, "V", 3, 4, "V", "H"]
    shapes = {1: [(2, 4), (4, 2)], 2: [(1, 3), (3, 1)], 3: [(3, 2), (2, 3)], 4: [(2, 2)]}
    root = shape_lists(tokens, shapes)
    assert [(e[0], e[1]) for e in root[2][1]] == [(3, 4), (5, 3), (7, 2)]
    assert [(e[0], e[1]) for e in root[3][1]] == [(4, 3), (5, 2)]
    area, w, h, choice, front = stockmeyer_sizing(tokens, shapes)
    assert front == [(4, 7), (5, 5), (7, 4)]
    assert (area, w, h) == (25, 5, 5)
    assert choice == {1: 1, 2: 0, 3: 0, 4: 0}
    assert evaluate(tokens, {1: (2, 4), 2: (1, 3), 3: (3, 2), 4: (2, 2)}) == (5, 6)


def test_merge_small() -> None:
    a = pareto([(1, 5), (2, 3), (4, 1)])
    b = pareto([(2, 4), (3, 2)])
    assert [(e[0], e[1]) for e in merge_v(a, b)] == [(3, 5), (4, 4), (5, 3), (7, 2)]
    pts = {(max(p[0], q[0]), p[1] + q[1]) for p in [(1, 5), (2, 3), (4, 1)] for q in [(2, 4), (3, 2)]}
    front = sorted(p for p in pts if not any(q != p and q[0] <= p[0] and q[1] <= p[1] for q in pts))
    assert [(e[0], e[1]) for e in merge_h(a, b)] == front


def test_single_block_and_squares() -> None:
    assert stockmeyer_sizing([5], {5: [(3, 2), (2, 3)]})[:3] == (6, 2, 3)
    area, w, h, choice, front = stockmeyer_sizing([1, 2, "V"], {1: [(2, 2)], 2: [(2, 2), (2, 2)]})
    assert (area, w, h) == (8, 4, 2) and front == [(4, 2)]


def test_orientations_against_all_choices() -> None:
    rng = random.Random(7)
    for trial in range(600):
        n = rng.randint(1, 8)
        leaves = list(range(n))
        rng.shuffle(leaves)
        tokens = random_tokens(rng, leaves)
        shapes = {}
        for b in leaves:
            w, h = rng.randint(1, 9), rng.randint(1, 9)
            shapes[b] = [(w, h), (h, w)]
        area, w, h, choice, front = stockmeyer_sizing(tokens, shapes)
        best, bfront = brute(tokens, shapes)
        assert area == best
        assert front == bfront
        assert len(front) <= n + 1
        assert evaluate(tokens, {b: shapes[b][choice[b]] for b in leaves}) == (w, h)


def test_general_shape_lists() -> None:
    rng = random.Random(8)
    for trial in range(300):
        n = rng.randint(1, 6)
        leaves = list(range(n))
        tokens = random_tokens(rng, leaves)
        shapes = {b: [(rng.randint(1, 9), rng.randint(1, 9)) for _ in range(rng.randint(1, 3))] for b in leaves}
        area, w, h, choice, front = stockmeyer_sizing(tokens, shapes)
        best, bfront = brute(tokens, shapes)
        assert (area, front) == (best, bfront)
        k = sum(len(pareto(shapes[b])) for b in leaves)
        assert len(front) <= k - (n - 1)
        assert evaluate(tokens, {b: shapes[b][choice[b]] for b in leaves}) == (w, h)
