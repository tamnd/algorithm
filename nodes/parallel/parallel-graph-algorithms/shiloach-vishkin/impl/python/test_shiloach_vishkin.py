# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shiloach-vishkin/. The authors are listed in prov/NADX4Y.jsonl.

import math
import random

from shiloach_vishkin import Cost, shiloach_vishkin, star_flags


def uf_labels(n: int, edges: list[tuple[int, int]]) -> list[int]:
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in edges:
        a, b = find(u), find(v)
        if a != b:
            parent[a] = b
    return [find(v) for v in range(n)]


def same_partition(a: list[int], b: list[int]) -> bool:
    fwd: dict[int, int] = {}
    bwd: dict[int, int] = {}
    for x, y in zip(a, b):
        if fwd.setdefault(x, y) != y or bwd.setdefault(y, x) != x:
            return False
    return True


def family(rng: random.Random) -> list[tuple[int, list[tuple[int, int]]]]:
    out = []
    for n in (1, 2, 5, 17, 40):
        out.append((n, []))
        out.append((n, [(i, i + 1) for i in range(n - 1)]))
        out.append((n, [(0, i) for i in range(1, n)]))
        if n >= 3:
            out.append((n, [(i, (i + 1) % n) for i in range(n)]))
        out.append((n, [(i, j) for i in range(n) for j in range(i + 1, n)]))
    for _ in range(150):
        n = rng.randint(1, 60)
        p = rng.choice([0.01, 0.03, 0.06, 0.15, 0.5])
        es = [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < p]
        perm = list(range(n))
        rng.shuffle(perm)  # random names, so that the hooks do not follow the input order
        out.append((n, [(perm[u], perm[v]) for u, v in es]))
    return out


def test_star_flags() -> None:
    assert star_flags([0, 0, 0, 3]) == [True, True, True, True]
    assert star_flags([0, 0, 1, 3]) == [False, False, False, True]


def test_example() -> None:
    n, edges = 6, [(5, 4), (4, 3), (3, 2), (2, 1), (1, 0)]
    c = Cost()
    P = shiloach_vishkin(n, edges, random.Random(0), c)
    assert P == [0] * 6
    assert c.iterations == 4
    # the star with center 4: the leaves that lose in L5 are stagnant and hook in L8
    for seed in range(20):
        c = Cost()
        P = shiloach_vishkin(5, [(4, 0), (4, 1), (4, 2), (4, 3)], random.Random(seed), c)
        assert len(set(P)) == 1 and P[4] in (0, 1, 2, 3)
        assert c.iterations == 2


def test_against_union_find() -> None:
    rng = random.Random(2024)
    runs = 0
    for n, edges in family(rng):
        want = uf_labels(n, edges)
        bound = math.ceil(math.log(max(n, 2), 1.5)) + 3
        for full in (False, True):
            for _ in range(2):
                c = Cost()
                P = shiloach_vishkin(n, edges, random.Random(rng.random()), c, full)
                assert same_partition(P, want)
                assert all(P[P[v]] == P[v] for v in range(n))  # every tree is a star at the end
                if full:
                    assert c.iterations <= math.ceil(math.log2(max(n, 1))) + 1
                else:
                    assert c.iterations <= bound
                runs += 1
    assert runs >= 500


def test_mean_iterations() -> None:
    # c = 1.5: the mean number of iterations of the one-shortcut form stays below 1.5 log2 n + 2
    rng = random.Random(7)
    for n in (16, 64, 256):
        total = 0
        trials = 20
        for _ in range(trials):
            edges = [(i, i + 1) for i in range(n - 1)]
            perm = list(range(n))
            rng.shuffle(perm)
            edges = [(perm[u], perm[v]) for u, v in edges]
            c = Cost()
            shiloach_vishkin(n, edges, random.Random(rng.random()), c)
            total += c.iterations
        assert total / trials <= 1.5 * math.log2(n) + 2
