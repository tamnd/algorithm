# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/latin-square-design/. The authors are listed in prov/AR1SZ9.jsonl.

import random
from fractions import Fraction
from itertools import combinations, permutations

import pytest

from latin_square_design import are_orthogonal, cyclic, field, is_latin, latin_square_anova, mols, randomize


def all_latin_with_first_row(n: int) -> list[list[list[int]]]:
    """Every Latin square of order n whose first row is 0, 1, ..., n - 1 (backtracking)."""
    out = []
    perms = list(permutations(range(n)))

    def extend(rows):
        if len(rows) == n:
            out.append([list(r) for r in rows])
            return
        for p in perms:
            if all(p[j] != r[j] for r in rows for j in range(n)):
                extend(rows + [p])

    extend([tuple(range(n))])
    return out


def has_transversal(sq) -> bool:
    n = len(sq)
    return any(len({sq[i][p[i]] for i in range(n)}) == n for p in permutations(range(n)))


def test_cyclic_squares() -> None:
    for n in range(1, 16):
        assert is_latin(cyclic(n))


def test_field_axioms_small_orders() -> None:
    for q in (2, 3, 4, 5, 7, 8, 9, 16, 25, 27):
        add, mul = field(q)
        for a in range(q):
            assert add[a][0] == a and mul[a][1] == a and mul[a][0] == 0
            assert sorted(add[a]) == list(range(q))
            if a:
                assert sorted(mul[a]) == list(range(q))  # no zero divisors: an inverse exists
        rng = random.Random(q)
        for _ in range(200):
            a, b, c = (rng.randrange(q) for _ in range(3))
            assert mul[a][add[b][c]] == add[mul[a][b]][mul[a][c]]
            assert mul[mul[a][b]][c] == mul[a][mul[b][c]] and mul[a][b] == mul[b][a]


def test_complete_sets_of_mols() -> None:
    for q in (2, 3, 4, 5, 7, 8, 9):
        squares = mols(q)
        assert len(squares) == q - 1
        assert all(is_latin(s) for s in squares)
        assert all(are_orthogonal(a, b) for a, b in combinations(squares, 2))


def test_example_squares() -> None:
    assert mols(3) == [[[0, 1, 2], [1, 2, 0], [2, 0, 1]], [[0, 1, 2], [2, 0, 1], [1, 2, 0]]]
    assert mols(4)[0] == [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]


def max_mols(n: int) -> int:
    """The size of the largest set of MOLS of order n, by exhaustive search over squares
    with first row 0, ..., n - 1 (renaming symbols keeps orthogonality)."""
    sq = all_latin_with_first_row(n)
    best = 1
    adj = {i: {j for j in range(len(sq)) if j != i and are_orthogonal(sq[i], sq[j])} for i in range(len(sq))}

    def grow(clique, cand):
        nonlocal best
        best = max(best, len(clique))
        for v in sorted(cand):
            if v > (clique[-1] if clique else -1):
                grow(clique + [v], cand & adj[v])

    grow([], set(range(len(sq))))
    return best


def test_bound_n_minus_one_is_reached_and_not_beaten() -> None:
    assert len(all_latin_with_first_row(3)) == 2
    assert len(all_latin_with_first_row(4)) == 24
    assert max_mols(3) == 2 and max_mols(4) == 3
    assert max_mols(2) == 1


def test_cyclic_even_squares_have_no_transversal() -> None:
    for n in (2, 4, 6):
        assert not has_transversal(cyclic(n))
    for n in (3, 5, 7):
        assert has_transversal(cyclic(n))


def test_randomize_keeps_latin() -> None:
    rng = random.Random(1)
    for n in range(1, 9):
        assert is_latin(randomize(cyclic(n), rng))


def exact_rss(cols, y) -> Fraction:
    k = len(cols)
    m = [[sum(Fraction(a) * b for a, b in zip(cols[i], cols[j])) for j in range(k)]
         + [sum(Fraction(a) * v for a, v in zip(cols[i], y))] for i in range(k)]
    for c in range(k):
        piv = next(r for r in range(c, k) if m[r][c] != 0)
        m[c], m[piv] = m[piv], m[c]
        for r in range(k):
            if r != c and m[r][c] != 0:
                f = m[r][c] / m[c][c]
                m[r] = [x - f * z for x, z in zip(m[r], m[c])]
    beta = [m[i][k] / m[i][i] for i in range(k)]
    return sum((v - sum(beta[i] * cols[i][t] for i in range(k))) ** 2 for t, v in enumerate(y))


def test_anova_against_least_squares() -> None:
    rng = random.Random(2)
    for n in (3, 4, 5):
        sq = randomize(cyclic(n), rng)
        y = [[rng.randint(0, 40) for _ in range(n)] for _ in range(n)]
        flat = [y[i][j] for i in range(n) for j in range(n)]
        ind = lambda f: [[1 if f(i, j) == lev else 0 for i in range(n) for j in range(n)] for lev in range(1, n)]
        one = [[1] * (n * n)]
        rows, cols, trts = ind(lambda i, j: i), ind(lambda i, j: j), ind(lambda i, j: sq[i][j])
        full = exact_rss(one + rows + cols + trts, flat)
        table = latin_square_anova(y, sq)
        assert abs(table["error"][0] - float(full)) < 1e-9
        # orthogonality: each factor's SS is its drop in RSS whatever else is in the model
        assert abs(table["treatments"][0] - float(exact_rss(one + rows + cols, flat) - full)) < 1e-9
        assert abs(table["treatments"][0] - float(exact_rss(one, flat) - exact_rss(one + trts, flat))) < 1e-9
        assert table["error"][1] == (n - 1) * (n - 2)


EXAMPLE_Y = [[30, 32, 31, 31], [37, 34, 36, 28], [29, 31, 31, 30], [37, 31, 37, 25]]


def test_example() -> None:
    sq = mols(4)[0]
    assert sq == [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]
    table = latin_square_anova(EXAMPLE_Y, sq)
    expected = {"rows": Fraction(117, 4), "columns": Fraction(269, 4), "treatments": Fraction(257, 4), "error": Fraction(21)}
    for key, value in expected.items():
        assert abs(table[key][0] - float(value)) < 1e-9 and table[key][1] == (3 if key != "error" else 6)
    means = [Fraction(sum(EXAMPLE_Y[i][j] for i in range(4) for j in range(4) if sq[i][j] == s), 4) for s in range(4)]
    assert means == [30, 34, Fraction(119, 4), Fraction(135, 4)]
    assert (expected["treatments"] / 3) / (expected["error"] / 6) == Fraction(257, 42)
    # the one-way analysis of the same data, ignoring rows and columns
    groups = [[Fraction(EXAMPLE_Y[i][j]) for i in range(4) for j in range(4) if sq[i][j] == s] for s in range(4)]
    ssw = sum((v - m) ** 2 for g, m in zip(groups, means) for v in g)
    assert ssw == Fraction(117, 4) + Fraction(269, 4) + 21
    assert abs(float((expected["treatments"] / 3) / (ssw / 12)) - 2.1872) < 1e-4


def test_errors() -> None:
    with pytest.raises(ValueError):
        latin_square_anova([[1.0, 2.0], [3.0, 4.0]], cyclic(2))
    with pytest.raises(ValueError):
        field(6)
