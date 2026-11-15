# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximal-munch/. The authors are listed in prov/FV9S4Q.jsonl.

import random

from maximal_munch import RULES, choose, evaluate, run, select


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


def paths(t: tuple, p: tuple = ()) -> list[tuple]:
    """The path of every node: the list of child positions from the root."""
    out = [p]
    if t[0] not in ("CONST", "VAR"):
        for i, c in enumerate(t[1:]):
            out += paths(c, p + (i,))
    return out


def node_at(t: tuple, p: tuple) -> tuple:
    for i in p:
        t = t[1 + i]
    return t


def cover(pat: object, t: tuple, p: tuple) -> tuple[set, list] | None:
    """The paths that the pattern covers at path p, and the paths of its register holes."""
    n = node_at(t, p)
    if pat == "reg":
        return set(), [p]
    if pat == ("CONST",) or pat == ("VAR",):
        return ({p}, []) if n[0] == pat[0] else None
    if n[0] != pat[0]:
        return None
    covered, holes = {p}, []
    for i, q in enumerate(pat[1:]):
        m = cover(q, t, p + (i,))
        if m is None:
            return None
        covered |= m[0]
        holes += m[1]
    return covered, holes


def munch_tiles(t: tuple) -> dict[tuple, tuple]:
    """The tiles that munch chooses: root path -> (rule, covered paths, hole paths)."""
    tiles: dict[tuple, tuple] = {}

    def go(p: tuple) -> None:
        idx, _ = choose(node_at(t, p))
        covered, holes = cover(RULES[idx][1], t, p)
        tiles[p] = (idx, covered, holes)
        for h in holes:
            go(h)

    go(())
    return tiles


def tilings(t: tuple) -> list[int]:
    """The cost of every tiling of t."""
    res = []
    for _, pat, cost in RULES:
        m = cover(pat, t, ())
        if m is None:
            continue
        partial = [cost]
        for h in m[1]:
            partial = [x + y for x in partial for y in tilings(node_at(t, h))]
        res += partial
    return res


def test_munch_is_not_optimum() -> None:
    t = ("MEM", ("ADD", ("MUL", ("VAR", "a"), ("VAR", "b")), ("VAR", "c")))
    code, cost = select(t)
    assert [RULES[ins[0]][0] for ins in code] == ["ld", "ld", "mul", "ld", "ldx"]
    assert cost == 15
    assert min(tilings(t)) == 14
    env = {"a": 4, "b": 5, "c": 6}
    assert run(code, env) == evaluate(t, env) == 37


def test_cover_is_valid_and_locally_optimal() -> None:
    rng = random.Random(1978)
    worse = 0
    for _ in range(400):
        t = random_tree(rng, rng.randint(1, 8))
        tiles = munch_tiles(t)
        # each node is covered by exactly one tile
        seen: list = []
        for _, covered, _ in tiles.values():
            seen += covered
        assert sorted(seen) == sorted(paths(t))
        # a parent tile and a child tile never form one tile of the table
        for v, (_, cv, holes) in tiles.items():
            for h in holes:
                union = cv | tiles[h][1]
                for _, pat, _ in RULES:
                    m = cover(pat, t, v)
                    assert m is None or m[0] != union
        code, cost = select(t)
        assert cost == sum(RULES[idx][2] for idx, _, _ in tiles.values())
        assert cost >= min(tilings(t))
        worse += cost > min(tilings(t))
        for _ in range(3):
            env = {x: rng.randint(-20, 20) for x in "abc"}
            assert run(code, env) == evaluate(t, env)
    assert worse > 0


def test_each_tree_has_a_cover() -> None:
    rng = random.Random(9)
    for _ in range(200):
        t = random_tree(rng, rng.randint(1, 30))
        code, _ = select(t)
        env = {x: rng.randint(-9, 9) for x in "abc"}
        assert run(code, env) == evaluate(t, env)
