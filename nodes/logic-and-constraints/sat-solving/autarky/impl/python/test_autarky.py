# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/autarky/. The authors are listed in prov/FSZY2A.jsonl.

import itertools
import random

from autarky import apply_autarky, find_autarky, is_autarky, lean_kernel


def satisfiable(clauses: list[list[int]], n: int) -> bool:
    return any(all(any(b[abs(a) - 1] == (a > 0) for a in c) for c in clauses)
               for b in itertools.product([False, True], repeat=n))


def partial_assignments(n: int):
    for vals in itertools.product([None, False, True], repeat=n):
        yield {i + 1: v for i, v in enumerate(vals) if v is not None}


def random_cnf(rng: random.Random, n: int, m: int) -> list[list[int]]:
    cnf = []
    for _ in range(m):
        k = rng.randint(1, min(3, n))
        vs = rng.sample(range(1, n + 1), k)
        cnf.append([v if rng.random() < 0.5 else -v for v in vs])
    return cnf


def test_page_example() -> None:
    f = [[1, 2], [-1, 2], [1, -2], [-1, -2], [2, 3, 4], [-3, 4], [-4, 5]]
    kernel, alpha = lean_kernel(f)
    assert kernel == [[1, 2], [-1, 2], [1, -2], [-1, -2]]
    assert is_autarky(f, alpha) and alpha == {4: True, 5: True}
    assert is_autarky(f, {5: True}) and not is_autarky(f, {4: True})


def test_pure_literal_and_model_are_autarkies() -> None:
    f = [[1, 2], [1, -3], [-2, 3]]
    assert is_autarky(f, {1: True})
    assert is_autarky(f, {1: True, 2: False, 3: False})
    assert apply_autarky(f, {1: True}) == [[-2, 3]]


def test_largest_autarky_by_brute_force() -> None:
    rng = random.Random(1985)
    for _ in range(150):
        n = rng.randint(1, 5)
        f = random_cnf(rng, n, rng.randint(1, 3 * n))
        kernel, alpha = lean_kernel(f)
        assert is_autarky(f, alpha)
        outside = [c for c in f if any(abs(a) in alpha for a in c)]
        assert len(outside) + len(kernel) == len(f)
        union = set()  # clauses satisfied by some autarky
        for beta in partial_assignments(n):
            if is_autarky(f, beta):
                union |= {i for i, c in enumerate(f) if any(abs(a) in beta for a in c)}
        assert len(union) == len(outside)
        assert satisfiable(kernel, n) == satisfiable(f, n)
        if satisfiable(f, n):
            assert kernel == []
        assert find_autarky(kernel) is None


def test_mus_inside_lean_kernel() -> None:
    rng = random.Random(3)
    for _ in range(60):
        n = rng.randint(2, 4)
        f = random_cnf(rng, n, rng.randint(4, 8))
        if satisfiable(f, n):
            continue
        kernel, _ = lean_kernel(f)
        kset = {tuple(c) for c in kernel}
        for r in range(1, len(f) + 1):
            for sub in itertools.combinations(f, r):
                s = list(sub)
                if not satisfiable(s, n) and all(satisfiable(s[:i] + s[i + 1:], n) for i in range(r)):
                    assert all(tuple(c) in kset for c in s)
