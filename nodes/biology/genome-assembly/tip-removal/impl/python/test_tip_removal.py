# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tip-removal/. The authors are listed in prov/W7590Z.jsonl.

import random

from tip_removal import find_tips, tip_removal


def count(reads: list[str], k: int) -> dict[str, int]:
    c: dict[str, int] = {}
    for r in reads:
        for i in range(len(r) - k + 1):
            c[r[i : i + k]] = c.get(r[i : i + k], 0) + 1
    return c


def contigs(c: dict[str, int]) -> list[str]:
    """Unitig strings, found by extending each edge both ways (independent of the module)."""
    by_prefix: dict[str, list[str]] = {}
    by_suffix: dict[str, list[str]] = {}
    for y in sorted(c):
        by_prefix.setdefault(y[:-1], []).append(y)
        by_suffix.setdefault(y[1:], []).append(y)
    succ = {x: by_prefix.get(x[1:], []) for x in c}
    pred = {x: by_suffix.get(x[:-1], []) for x in c}

    def joined(a: str, b: str) -> bool:
        return succ[a] == [b] and pred[b] == [a]

    seen: set[str] = set()
    res = []
    for e in sorted(c):
        if e in seen:
            continue
        path = [e]
        while len(pred[path[0]]) == 1 and joined(pred[path[0]][0], path[0]) and pred[path[0]][0] not in path:
            path.insert(0, pred[path[0]][0])
        while len(succ[path[-1]]) == 1 and joined(path[-1], succ[path[-1]][0]) and succ[path[-1]][0] not in path:
            path.append(succ[path[-1]][0])
        seen.update(path)
        res.append(path[0] + "".join(x[-1] for x in path[1:]))
    return sorted(res)


def brute_tips(c: dict[str, int], max_len: int) -> list[list[str]]:
    """Tips by the definition: a dead-end chain into or out of a junction, short, with a minority count."""
    succ = {x: [y for y in c if y[:-1] == x[1:]] for x in c}
    pred = {x: [y for y in c if y[1:] == x[:-1]] for x in c}
    tips = []
    for e in c:
        if not pred[e]:  # e starts at a vertex with in-degree 0
            if len([y for y in c if y[:-1] == e[:-1]]) != 1:
                continue
            path = [e]
            while len(succ[path[-1]]) == 1 and len(pred[succ[path[-1]][0]]) == 1:
                path.append(succ[path[-1]][0])
            others = [y for y in c if y[1:] == path[-1][1:] and y != path[-1]]
            if others and len(path) < max_len and c[path[-1]] < max(c[y] for y in others):
                tips.append(path)
        if not succ[e]:  # e ends at a vertex with out-degree 0
            if len([y for y in c if y[1:] == e[1:]]) != 1:
                continue
            path = [e]
            while len(pred[path[0]]) == 1 and len(succ[pred[path[0]][0]]) == 1:
                path.insert(0, pred[path[0]][0])
            others = [y for y in c if y[:-1] == path[0][:-1] and y != path[0]]
            if others and len(path) < max_len and c[path[0]] < max(c[y] for y in others):
                tips.append(path)
    return tips


def random_genome(rng: random.Random, n: int, w: int) -> str:
    while True:
        s = "".join(rng.choice("ACGT") for _ in range(n))
        ws = [s[i : i + w] for i in range(n - w + 1)]
        if len(set(ws)) == len(ws):
            return s


def test_example_error_tip() -> None:
    s = "ATGGCGTACCTTAGCAGTCCA"
    reads = [s[0:10], s[4:14], s[8:18], s[11:21], s[2:12], s[6:16], s[9:19]]
    c = count(reads + ["CCTTAGCATT"], 5)
    assert contigs(c) == ["AGCAGTCCA", "AGCATT", "ATGGCGTACCTTAGCA"]
    assert find_tips(c, 10) == [(1, ["AGCAT", "GCATT"])]
    assert contigs(tip_removal(c, 5)) == [s]


def test_example_true_end_is_lost() -> None:
    t = "CGGGAGTCCCTGAGAGGCTTCCTGGTT"
    c = count([t[i : i + 10] for i in range(len(t) - 9)], 5)
    assert contigs(c) == ["CCTGAGAGGCTTCCTG", "CCTGGTT", "CGGGAGTCCCTG"]
    assert contigs(tip_removal(c, 5)) == ["CCTGAGAGGCTTCCTG", "CGGGAGTCCCTG"]
    assert contigs(tip_removal(c, 5, max_len=3)) == ["CCTGAGAGGCTTCCTG", "CCTGGTT", "CGGGAGTCCCTG"]


def test_edges() -> None:
    assert tip_removal({}, 3) == {}
    one = {"ACG": 1, "CGT": 1}
    assert tip_removal(one, 3) == one  # a lone path has no junction
    equal = {"AAC": 2, "ACG": 2, "ACT": 2}
    assert tip_removal(equal, 3) == equal  # a tie is not a minority


def test_against_brute_force_definition() -> None:
    rng = random.Random(2)
    for _ in range(300):
        k = rng.randint(3, 5)
        s = "".join(rng.choice("ACG") for _ in range(rng.randint(k, 30)))
        reads = [s[p : p + 8] for p in (rng.randrange(max(1, len(s) - 7)) for _ in range(rng.randint(1, 12)))]
        reads = [r for r in reads if len(r) >= k]
        c = count(reads, k)
        max_len = rng.randint(1, 2 * k)
        found = sorted(p for _, p in find_tips(c, max_len))
        assert found == sorted(brute_tips(c, max_len))
        g = tip_removal(c, k, max_len)
        assert all(x in c and g[x] == c[x] for x in g)
        assert brute_tips(g, max_len) == []


def test_errors_near_read_ends_are_removed() -> None:
    rng = random.Random(9)
    for _ in range(25):
        k = 15
        s = random_genome(rng, 300, k - 1)
        reads = [s[p : p + 50] for p in range(0, 251, 5)] * 2
        for _ in range(4):
            j = rng.randrange(len(reads))
            p = 5 * (j % 51)
            d = rng.randrange(k - 1)
            i = 49 - d if rng.random() < 0.5 else d  # an error d letters from one end
            if not 3 * k <= p + i <= len(s) - 3 * k:
                continue
            r = list(reads[j])
            r[i] = rng.choice([b for b in "ACGT" if b != r[i]])
            reads[j] = "".join(r)
        assert contigs(tip_removal(count(reads, k), k)) == [s]
