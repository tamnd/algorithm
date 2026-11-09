# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/matroid-intersection-algorithm/. The authors are listed in prov/1YKCWY.jsonl.

import random
from itertools import combinations

from matroid_intersection_algorithm import matroid_intersection


def graphic(edges: list[tuple[int, int]]):
    """Independent sets are the forests of a multigraph."""

    def indep(s: frozenset[int]) -> bool:
        parent: dict[int, int] = {}

        def find(x: int) -> int:
            while parent.get(x, x) != x:
                x = parent[x]
            return x

        for i in s:
            a, b = find(edges[i][0]), find(edges[i][1])
            if a == b:
                return False
            parent[a] = b
        return True

    return indep


def partition(block: list[int], cap: list[int]):
    """At most cap[b] elements from each block b."""

    def indep(s: frozenset[int]) -> bool:
        used = [0] * len(cap)
        for i in s:
            used[block[i]] += 1
            if used[block[i]] > cap[block[i]]:
                return False
        return True

    return indep


def uniform(k: int):
    return lambda s: len(s) <= k


def binary(vectors: list[int]):
    """Linear matroid over GF(2): vectors are bit masks."""

    def indep(s: frozenset[int]) -> bool:
        basis: list[int] = []
        for i in s:
            v = vectors[i]
            for b in basis:
                v = min(v, v ^ b)
            if v == 0:
                return False
            basis.append(v)
            basis.sort(reverse=True)
        return True

    return indep


def rank(indep, s) -> int:
    cur: frozenset[int] = frozenset()
    for x in sorted(s):
        if indep(cur | {x}):
            cur = cur | {x}
    return len(cur)


def brute_force(n: int, indep1, indep2) -> int:
    for k in range(n, -1, -1):
        for s in combinations(range(n), k):
            fs = frozenset(s)
            if indep1(fs) and indep2(fs):
                return k
    return 0


def random_matroid(rng: random.Random, n: int):
    kind = rng.randrange(4)
    if kind == 0:
        nv = rng.randint(2, 6)
        return graphic([tuple(rng.sample(range(nv), 2)) for _ in range(n)])
    if kind == 1:
        nb = rng.randint(1, 5)
        return partition([rng.randrange(nb) for _ in range(n)], [rng.choice([0, 1, 1, 1, 2]) for _ in range(nb)])
    if kind == 2:
        return uniform(rng.randint(1, n) if n else 0)
    bits = rng.randint(2, 5)
    return binary([rng.randrange(1 << bits) for _ in range(n)])


def check(n: int, indep1, indep2) -> list[int]:
    sizes: list[int] = []

    def on_augment(path: list[int], cur: frozenset[int]) -> None:
        # Each augmentation keeps a common independent set and adds one element.
        assert indep1(cur) and indep2(cur)
        assert len(cur) == len(sizes) + 1
        sizes.append(len(cur))
        assert len(path) % 2 == 1

    I, U = matroid_intersection(n, indep1, indep2, on_augment)
    fs = frozenset(I)
    assert indep1(fs) and indep2(fs)
    assert len(I) == len(sizes)
    # The certificate U proves optimality: |I| = r1(U) + r2(E - U).
    rest = set(range(n)) - set(U)
    assert len(I) == rank(indep1, U) + rank(indep2, rest)
    assert len(I) == brute_force(n, indep1, indep2)
    return I


def test_example() -> None:
    # Links 15, 25, 34, 12, 25, 14 offered by companies red, yellow,
    # yellow, green, blue, yellow; at most one link per company.
    edges = [(1, 5), (2, 5), (3, 4), (1, 2), (2, 5), (1, 4)]
    color = [0, 3, 3, 2, 1, 3]
    paths: list[list[int]] = []
    I, U = matroid_intersection(6, graphic(edges), partition(color, [1, 1, 1, 1]), lambda p, c: paths.append(p))
    assert paths == [[0], [1], [2, 1, 3]]
    assert I == [0, 2, 3]
    assert U == [0, 3, 4]
    check(6, graphic(edges), partition(color, [1, 1, 1, 1]))


def test_bipartite_matching() -> None:
    # Edges of a bipartite graph; one partition matroid per side.
    edges = [(0, 0), (0, 1), (1, 0), (2, 1), (2, 2), (3, 2)]
    left = partition([u for u, _ in edges], [1] * 4)
    right = partition([v for _, v in edges], [1] * 3)
    I = check(len(edges), left, right)
    assert len(I) == 3


def test_empty_and_trivial() -> None:
    assert matroid_intersection(0, uniform(0), uniform(0)) == ([], [])
    assert matroid_intersection(3, uniform(0), uniform(3))[0] == []
    assert matroid_intersection(3, uniform(3), uniform(2))[0] == [0, 1]


def test_random_against_brute_force() -> None:
    rng = random.Random(8803)
    for _ in range(600):
        n = rng.randint(0, 8)
        check(n, random_matroid(rng, n), random_matroid(rng, n))


def test_colorful_forests_and_matchings() -> None:
    # These families need long augmenting paths more often.
    rng = random.Random(5521)
    longest = 0
    for k in range(400):
        n = rng.randint(4, 9)
        if k % 2 == 0:
            nv = rng.randint(3, 6)
            edges = [tuple(rng.sample(range(nv), 2)) for _ in range(n)]
            nc = rng.randint(2, 4)
            m1, m2 = graphic(edges), partition([rng.randrange(nc) for _ in range(n)], [1] * nc)
        else:
            nl, nr = rng.randint(2, 4), rng.randint(2, 4)
            edges = [(rng.randrange(nl), rng.randrange(nr)) for _ in range(n)]
            m1 = partition([u for u, _ in edges], [1] * nl)
            m2 = partition([v for _, v in edges], [1] * nr)
        lengths: list[int] = []
        matroid_intersection(n, m1, m2, lambda p, c: lengths.append(len(p)))
        longest = max(longest, max(lengths, default=0))
        check(n, m1, m2)
    assert longest >= 5


if __name__ == "__main__":
    test_example()
    test_bipartite_matching()
    test_empty_and_trivial()
    test_random_against_brute_force()
    test_colorful_forests_and_matchings()
    print("ok")
