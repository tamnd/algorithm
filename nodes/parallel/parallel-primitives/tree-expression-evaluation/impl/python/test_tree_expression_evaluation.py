# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tree-expression-evaluation/. The authors are listed in prov/D1DXVT.jsonl.

import random

from tree_expression_evaluation import Trace, Tree, evaluate


def ceil_log2(m: int) -> int:
    return 0 if m <= 1 else (m - 1).bit_length()


def build(leaves: int, rng: random.Random, shape: str) -> Tree:
    """A full binary tree with the given number of leaves, random operators and values, random labels."""
    op: list[str | None] = []
    left: list[int | None] = []
    right: list[int | None] = []

    def new() -> int:
        op.append(None)
        left.append(None)
        right.append(None)
        return len(op) - 1

    root = new()
    stack = [(root, leaves)]
    while stack:
        v, k = stack.pop()
        if k == 1:
            continue
        if shape == "left":
            j = k - 1
        elif shape == "right":
            j = 1
        elif shape == "balanced":
            j = k // 2
        else:
            j = rng.randint(1, k - 1)
        op[v] = rng.choice("+-*")
        left[v], right[v] = new(), new()
        stack.append((left[v], j))  # type: ignore[arg-type]
        stack.append((right[v], k - j))  # type: ignore[arg-type]
    n = len(op)
    value = [rng.randint(-3, 3) for _ in range(n)]
    perm = list(range(n))
    rng.shuffle(perm)

    def m(x: int | None) -> int | None:
        return None if x is None else perm[x]

    op2: list[str | None] = [None] * n
    l2: list[int | None] = [None] * n
    r2: list[int | None] = [None] * n
    v2 = [0] * n
    for v in range(n):
        op2[perm[v]], l2[perm[v]], r2[perm[v]], v2[perm[v]] = op[v], m(left[v]), m(right[v]), value[v]
    return Tree(op2, l2, r2, v2, perm[root])


def stack_eval(t: Tree) -> int:
    """Reference: postorder evaluation with an explicit stack."""
    out: dict[int, int] = {}
    stack = [(t.root, False)]
    while stack:
        v, done = stack.pop()
        o = t.op[v]
        if o is None:
            out[v] = t.value[v]
        elif done:
            x, y = out[t.left[v]], out[t.right[v]]  # type: ignore[index]
            out[v] = x + y if o == "+" else x - y if o == "-" else x * y
        else:
            stack.append((v, True))
            stack.append((t.right[v], False))  # type: ignore[arg-type]
            stack.append((t.left[v], False))  # type: ignore[arg-type]
    return out[t.root]


def test_example() -> None:
    # ((1 + 2) * 3) + (4 * (5 - 6)) = 5, with the nodes numbered in preorder
    op = ["+", "*", "+", None, None, None, "*", None, "-", None, None]
    left = [1, 2, 3, None, None, None, 7, None, 9, None, None]
    right = [6, 5, 4, None, None, None, 8, None, 10, None, None]
    value = [0, 0, 0, 1, 2, 3, 0, 4, 0, 5, 6]
    tr = Trace()
    assert evaluate(Tree(op, left, right, value, 0), tr) == 5
    assert tr.rounds == 3 and tr.rakes == 5


def test_single_leaf() -> None:
    assert evaluate(Tree([None], [None], [None], [7], 0)) == 7


def test_random_against_stack() -> None:
    rng = random.Random(1974)
    shapes = ["random", "left", "right", "balanced"]
    for k in range(800):
        leaves = rng.choice([1, 2, 3, 4, 5, 7, 8, 9, 16, 17, 31, 32, 60])
        t = build(leaves, rng, shapes[k % 4])
        tr = Trace()
        assert evaluate(t, tr) == stack_eval(t)
        assert tr.rounds == ceil_log2(leaves)
        assert tr.rakes == leaves - 1


def test_exclusive_access() -> None:
    # the rakes of one substep read and write pairwise disjoint cells (EREW)
    rng = random.Random(3)
    for k in range(300):
        t = build(rng.randint(1, 64), rng, ["random", "left", "right", "balanced"][k % 4])
        tr = Trace()
        evaluate(t, tr)
        for touched in tr.substeps:
            seen: set[tuple[str, int]] = set()
            for cells in touched:
                assert not (cells & seen)
                seen |= cells
