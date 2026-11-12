# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bubble-popping/. The authors are listed in prov/ZPJBHM.jsonl.

import random

from bubble_popping import alternative, bubble_popping, find_bubble, unitigs


def count(reads: list[str], k: int) -> dict[str, int]:
    c: dict[str, int] = {}
    for r in reads:
        for i in range(len(r) - k + 1):
            c[r[i : i + k]] = c.get(r[i : i + k], 0) + 1
    return c


def spell(p: list[str]) -> str:
    return p[0] + "".join(x[-1] for x in p[1:])


def contigs(c: dict[str, int]) -> list[str]:
    return sorted(spell(p) for p in unitigs(c))


def brute_alternative(paths: list[list[str]], counts: dict[str, int], skip: int) -> tuple[int, int] | None:
    """Try every vertex-simple path of unitigs; return the best (edges, total count)."""
    src, dst = paths[skip][0][:-1], paths[skip][-1][1:]
    best: tuple[int, int] | None = None
    stack = [(src, 0, 0, {src})]
    while stack:
        v, length, total, seen = stack.pop()
        for j, p in enumerate(paths):
            if j == skip or p[0][:-1] != v:
                continue
            w = p[-1][1:]
            cand = (length + len(p), total + sum(counts[x] for x in p))
            if w == dst:
                if best is None or (cand[0], -cand[1]) < (best[0], -best[1]):
                    best = cand
            elif w not in seen:
                stack.append((w, cand[0], cand[1], seen | {w}))
    return best


def reachable(c: dict[str, int]) -> set[tuple[str, str]]:
    succ: dict[str, set[str]] = {}
    for x in c:
        succ.setdefault(x[:-1], set()).add(x[1:])
        succ.setdefault(x[1:], set())
    pairs = set()
    for s in succ:
        stack, seen = [s], {s}
        while stack:
            v = stack.pop()
            for w in succ[v]:
                if w not in seen:
                    seen.add(w)
                    stack.append(w)
        pairs |= {(s, t) for t in seen}
    return pairs


def random_genome(rng: random.Random, n: int, w: int) -> str:
    while True:
        s = "".join(rng.choice("ACGT") for _ in range(n))
        ws = [s[i : i + w] for i in range(n - w + 1)]
        if len(set(ws)) == len(ws):
            return s


def test_example_error_bubble() -> None:
    s = "ATGGCGTACCTTAGCAGTCCA"
    reads = [s[p : p + 10] for p in (0, 4, 8, 11, 2, 6, 9, 3)] + ["CGTACATTAG"]
    c = count(reads, 5)
    assert contigs(c) == ["ATGGCGTAC", "GTACATTAG", "GTACCTTAG", "TTAGCAGTCCA"]
    assert find_bubble(c, 10, 2) == ["GTACA", "TACAT", "ACATT", "CATTA", "ATTAG"]
    assert contigs(bubble_popping(c, 5)) == [s]


def test_example_true_allele_is_lost() -> None:
    h1 = "GATTACAGGCTCAAGTCCGA"
    h2 = "GATTACAGGCGCAAGTCCGA"
    reads = [h1[i : i + 10] for i in range(0, 11, 2)] + [h2[i : i + 10] for i in range(1, 11, 3)]
    c = count(reads, 5)
    assert contigs(c) == ["AGGCGCAAG", "AGGCTCAAG", "CAAGTCCGA", "GATTACAGGC"]
    assert contigs(bubble_popping(c, 5)) == [h1]
    assert contigs(bubble_popping(c, 5, max_len=4)) == contigs(c)


def test_edges() -> None:
    assert bubble_popping({}, 3) == {}
    equal = {"ACG": 2, "ACT": 2}
    assert bubble_popping(equal, 3) == equal  # two edges with different ends are no bubble
    two = {"AAC": 1, "AGC": 1, "AAG": 1}  # AA->AC directly, and AA->AG->GC: ends differ
    assert bubble_popping(two, 3) == two


def test_alternative_against_brute_force() -> None:
    rng = random.Random(4)
    for _ in range(300):
        k = rng.randint(3, 4)
        c = {"".join(rng.choice("AC") for _ in range(k)): rng.randint(1, 5) for _ in range(rng.randint(1, 14))}
        paths = unitigs(c)
        for j in range(len(paths)):
            if paths[j][0][:-1] == paths[j][-1][1:]:
                continue
            got = alternative(paths, c, j)
            want = brute_alternative(paths, c, j)
            assert (got[:2] if got else None) == want


def test_result_has_no_bubble_and_keeps_reachability() -> None:
    rng = random.Random(6)
    for _ in range(200):
        k = rng.randint(3, 4)
        c = {"".join(rng.choice("ACG") for _ in range(k)): rng.randint(1, 6) for _ in range(rng.randint(1, 16))}
        g = bubble_popping(c, k, max_len=6, max_diff=1)
        assert all(x in c and g[x] == c[x] for x in g)
        assert find_bubble(g, 6, 1) is None
        before, after = reachable(c), reachable(g)
        alive = {x[:-1] for x in g} | {x[1:] for x in g}
        assert {(a, b) for a, b in before if a in alive and b in alive} == after


def test_errors_inside_reads_are_popped() -> None:
    rng = random.Random(10)
    for _ in range(15):
        k = 15
        s = random_genome(rng, 250, k - 1)
        reads = [s[p : p + 50] for p in range(0, 201, 5)] * 2
        for _ in range(3):
            j = rng.randrange(len(reads))
            i = rng.randint(k - 1, 50 - k)  # at least k - 1 letters from both ends of the read
            r = list(reads[j])
            r[i] = rng.choice([b for b in "ACGT" if b != r[i]])
            reads[j] = "".join(r)
        assert contigs(bubble_popping(count(reads, k), k)) == [s]
