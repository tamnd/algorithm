# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cube-pruning/. The authors are listed in prov/6RZK3C.jsonl.

import math
import random

from cube_pruning import BigramScores, Edge, combine, cube_prune, exhaustive_k_best, pop_order


def example() -> tuple[list[Edge], BigramScores]:
    subj = [(-1.0, ("he",)), (-1.2, ("they",)), (-1.5, ("she",))]
    verb = [(-0.8, ("go",)), (-1.0, ("goes",)), (-1.6, ("went",))]
    lm = BigramScores(
        {
            ("he", "go"): -3.0, ("he", "goes"): -0.4, ("he", "went"): -0.6,
            ("they", "go"): -0.3, ("they", "goes"): -3.0, ("they", "went"): -0.6,
            ("she", "go"): -3.0, ("she", "goes"): -0.4, ("she", "went"): -0.6,
        },
        default=-5.0,
    )
    return [Edge(0.0, (0, 1), [subj, verb])], lm


def rounded(items: list) -> list:
    return [(round(s, 9), w) for s, w in items]


def test_example() -> None:
    edges, lm = example()
    order = pop_order(edges, 4, lm)
    assert [(j, round(s, 9)) for _, j, s in order] == [((0, 0), -4.8), ((1, 0), -2.3), ((0, 1), -2.4), ((0, 2), -3.2)]
    got = rounded(cube_prune(edges, 3, lm))
    assert got == [(-2.3, ("they", "go")), (-2.4, ("he", "goes")), (-4.8, ("he", "go"))]
    want = rounded(exhaustive_k_best(edges, 3, lm))
    assert want == [(-2.3, ("they", "go")), (-2.4, ("he", "goes")), (-2.9, ("she", "goes"))]
    got4 = [s for s, _ in rounded(cube_prune(edges, 4, lm))]
    assert got4 == [-2.3, -2.4, -3.2, -4.8]
    # without the language model the grid is monotone and the result is exact
    assert rounded(cube_prune(edges, 3, lm, lm_weight=0.0)) == [(-1.8, ("he", "go")), (-2.0, ("he", "goes")), (-2.0, ("they", "go"))]


def random_edges(rng: random.Random, vocab: list[str]) -> list[Edge]:
    edges = []
    for _ in range(rng.randint(1, 3)):
        arity = rng.randint(0, 3)
        children = []
        for _ in range(arity):
            items = [(-rng.uniform(0, 4), tuple(rng.choice(vocab) for _ in range(rng.randint(1, 2)))) for _ in range(rng.randint(1, 4))]
            items.sort(key=lambda it: -it[0])
            children.append(items)
        pattern = list(range(arity))
        rng.shuffle(pattern)
        for _ in range(rng.randint(0, 2)):
            pattern.insert(rng.randint(0, len(pattern)), rng.choice(vocab))
        edges.append(Edge(-rng.uniform(0, 2), tuple(pattern), children))
    return edges


def random_lm(rng: random.Random, vocab: list[str]) -> BigramScores:
    return BigramScores({(a, b): -rng.uniform(0.1, 5.0) for a in vocab for b in vocab}, default=-5.0)


def test_exact_without_language_model() -> None:
    rng = random.Random(2005)
    vocab = ["p", "q", "r", "s"]
    for _ in range(400):
        edges, lm = random_edges(rng, vocab), random_lm(rng, vocab)
        k = rng.randint(1, 12)
        got = [round(s, 9) for s, _ in cube_prune(edges, k, lm, lm_weight=0.0)]
        want = [round(s, 9) for s, _ in exhaustive_k_best(edges, k, lm, lm_weight=0.0)]
        assert got == want
        order = [s for _, _, s in pop_order(edges, k, lm, lm_weight=0.0)]
        assert all(a >= b - 1e-12 for a, b in zip(order, order[1:]))


def test_with_language_model_is_a_heuristic() -> None:
    rng = random.Random(2007)
    vocab = ["p", "q", "r", "s"]
    misses = 0
    for _ in range(400):
        edges, lm = random_edges(rng, vocab), random_lm(rng, vocab)
        k = rng.randint(1, 6)
        got = cube_prune(edges, k, lm)
        want = exhaustive_k_best(edges, k, lm)
        assert len(got) == len(want)
        # every popped item is a real grid item with its true score
        assert all(a[0] >= b[0] - 1e-12 for a, b in zip(got, got[1:]))
        assert all(g[0] <= w[0] + 1e-12 for g, w in zip(got, want))
        if got[0][0] < want[0][0] - 1e-12:
            misses += 1
        # with k at least the grid size, every point is popped
        total = sum(math.prod(len(c) for c in e.children) for e in edges)
        assert [round(s, 9) for s, _ in cube_prune(edges, total, lm)] == [round(s, 9) for s, _ in exhaustive_k_best(edges, total, lm)]
    assert misses > 0


def test_combine_counts_only_new_bigrams() -> None:
    lm = BigramScores({("a", "b"): -1.0, ("b", "c"): -2.0, ("c", "d"): -3.0}, default=-7.0)
    edge = Edge(-0.5, (0, "c", 1), [[(-1.0, ("a", "b"))], [(-2.0, ("d",))]])
    score, words = combine(edge, (0, 0), lm, 1.0)
    assert words == ("a", "b", "c", "d")
    assert math.isclose(score, -0.5 - 1.0 - 2.0 - 2.0 - 3.0)
