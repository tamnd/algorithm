# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simplex-code/. The authors are listed in prov/KNDK1C.jsonl.

from itertools import combinations, product

from simplex_code import (
    codewords,
    encode,
    first_order_reed_muller,
    generator_matrix,
    griesmer_length,
    weight_distribution,
)


def dist(a, b):
    return sum(x != y for x, y in zip(a, b))


def test_page_example():
    g = generator_matrix(3)
    assert g == [[0, 0, 0, 1, 1, 1, 1], [0, 1, 1, 0, 0, 1, 1], [1, 0, 1, 0, 1, 0, 1]]
    assert encode((1, 0, 1), g) == (1, 0, 1, 1, 0, 1, 0)
    assert weight_distribution(codewords(3)) == {0: 1, 4: 7}


def test_constant_weight_binary_r_up_to_5():
    for r in range(1, 6):
        words = codewords(r)
        assert len(set(words)) == 2**r
        assert weight_distribution(words) == {0: 1, 2 ** (r - 1): 2**r - 1}


def test_equidistant():
    for r in range(2, 5):
        words = codewords(r)
        assert {dist(a, b) for a, b in combinations(words, 2)} == {2 ** (r - 1)}


def test_qary_constant_weight():
    for q, r in [(3, 2), (3, 3), (5, 2)]:
        words = codewords(r, q)
        n = (q**r - 1) // (q - 1)
        assert len(words[0]) == n
        assert weight_distribution(words) == {0: 1, q ** (r - 1): q**r - 1}


def test_dual_of_hamming():
    # Every simplex codeword is orthogonal to every Hamming codeword, and the dimensions add to n.
    for r in (3, 4):
        g = generator_matrix(r)
        n = len(g[0])
        hamming = [v for v in product(range(2), repeat=n) if all(sum(a * b for a, b in zip(row, v)) % 2 == 0 for row in g)]
        assert len(hamming) == 2 ** (n - r)
        for c in codewords(r):
            for v in hamming:
                assert sum(a * b for a, b in zip(c, v)) % 2 == 0


def test_meets_griesmer_and_plotkin():
    for r in range(1, 8):
        n, k, d = 2**r - 1, r, 2 ** (r - 1)
        assert griesmer_length(k, d) == n
        if 2 * d > n:
            assert 2 * (d // (2 * d - n)) == 2**k
    for q, r in [(3, 2), (3, 3), (5, 2)]:
        n, d = (q**r - 1) // (q - 1), q ** (r - 1)
        assert griesmer_length(r, d, q) == n


def test_reed_muller_extension():
    for r in range(1, 6):
        words = first_order_reed_muller(r)
        assert len(set(words)) == 2 ** (r + 1)
        want = {0: 1, 2 ** (r - 1): 2 ** (r + 1) - 2, 2**r: 1}
        assert weight_distribution(words) == want
