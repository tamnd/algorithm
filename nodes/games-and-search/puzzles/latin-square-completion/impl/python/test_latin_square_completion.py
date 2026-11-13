# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/latin-square-completion/. The authors are listed in prov/5D4CRB.jsonl.

import itertools
import random

from latin_square_completion import (
    complete_latin,
    evans_counterexample,
    extend_rectangle,
    is_latin,
    is_partial_latin,
)


def all_rectangles(k, n):
    """All k by n Latin rectangles: rows are permutations, columns never repeat."""
    perms = list(itertools.permutations(range(n)))
    out = []
    stack = [()]
    while stack:
        rows = stack.pop()
        if len(rows) == k:
            out.append(rows)
            continue
        for p in perms:
            if all(p[j] != r[j] for r in rows for j in range(n)):
                stack.append(rows + (p,))
    return out


SQUARES = {n: [tuple(v for row in s for v in row) for s in all_rectangles(n, n)] for n in range(1, 5)}


def brute_completions(partial):
    n = len(partial)
    flat = [v for row in partial for v in row]
    return {s for s in SQUARES[n] if all(f is None or f == x for f, x in zip(flat, s))}


def key(square):
    return tuple(v for row in square for v in row)


def test_number_of_latin_squares() -> None:
    assert [len(SQUARES[n]) for n in range(1, 5)] == [1, 2, 12, 576]
    for n in range(1, 5):
        empty = [[None] * n for _ in range(n)]
        assert {key(s) for s in complete_latin(empty)} == set(SQUARES[n])


def test_random_partial_squares_against_brute_force() -> None:
    rng = random.Random(3)
    for _ in range(400):
        n = rng.randint(2, 4)
        if rng.random() < 0.5:
            source = rng.choice(SQUARES[n])
            flat = [v if rng.random() < 0.35 else None for v in source]
        else:
            flat = [rng.choice([None, None, None] + list(range(n))) for _ in range(n * n)]
        partial = [flat[n * i:n * i + n] for i in range(n)]
        if not is_partial_latin(partial):
            assert complete_latin(partial) == []
            continue
        got = {key(s) for s in complete_latin(partial)}
        assert got == brute_completions(partial)


def test_hall_extension_of_every_rectangle() -> None:
    for n in range(1, 5):
        for k in range(0, n + 1):
            for rect in all_rectangles(k, n):
                sq = extend_rectangle(rect, n)
                assert is_latin(sq)
                assert [tuple(r) for r in sq[:k]] == list(rect)
    for k in (1, 2):
        for rect in all_rectangles(k, 5):
            sq = extend_rectangle(rect, 5)
            assert is_latin(sq) and [tuple(r) for r in sq[:k]] == list(rect)


def test_hall_extension_of_random_rectangles() -> None:
    rng = random.Random(8)
    for _ in range(60):
        n = rng.randint(5, 9)
        k = rng.randint(1, n - 1)
        # A random rectangle: the first k rows of a shuffled cyclic square.
        perm_r = list(range(n))
        perm_c = list(range(n))
        perm_s = list(range(n))
        rng.shuffle(perm_r)
        rng.shuffle(perm_c)
        rng.shuffle(perm_s)
        rect = [[perm_s[(perm_r[i] + perm_c[j]) % n] for j in range(n)] for i in range(k)]
        sq = extend_rectangle(rect, n)
        assert is_latin(sq) and sq[:k] == rect


def test_evans_bound_for_small_orders() -> None:
    # Every partial Latin square with at most n - 1 filled cells completes (n <= 4).
    for n in range(2, 5):
        cells = [(i, j) for i in range(n) for j in range(n)]
        completable = set()
        for s in SQUARES[n]:
            for size in range(n):
                for chosen in itertools.combinations(range(n * n), size):
                    completable.add(tuple((c, s[c]) for c in chosen))
        for size in range(n):
            for chosen in itertools.combinations(range(n * n), size):
                for symbols in itertools.product(range(n), repeat=size):
                    partial = [[None] * n for _ in range(n)]
                    for c, v in zip(chosen, symbols):
                        partial[cells[c][0]][cells[c][1]] = v
                    if is_partial_latin(partial):
                        assert tuple(zip(chosen, symbols)) in completable


def test_n_cells_can_block_completion() -> None:
    for n in range(2, 7):
        sq = evans_counterexample(n)
        assert sum(v is not None for row in sq for v in row) == n
        assert is_partial_latin(sq)
        assert complete_latin(sq, limit=1) == []


def test_completion_of_larger_orders() -> None:
    rng = random.Random(21)
    for n in (6, 7, 8):
        for _ in range(3):
            base = [[(i + j) % n for j in range(n)] for i in range(n)]
            flat = [v if rng.random() < 0.4 else None for row in base for v in row]
            partial = [flat[n * i:n * i + n] for i in range(n)]
            sols = complete_latin(partial, limit=1)
            assert len(sols) == 1 and is_latin(sols[0])
            assert all(partial[i][j] in (None, sols[0][i][j]) for i in range(n) for j in range(n))
