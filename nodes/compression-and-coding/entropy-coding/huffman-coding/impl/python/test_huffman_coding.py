# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/huffman-coding/. The authors are listed in prov/06ZXXT.jsonl.

import math
import random
from functools import lru_cache

from huffman_coding import (
    code_lengths,
    codewords,
    cost,
    decode,
    encode,
    huffman_code,
    huffman_tree,
    huffman_tree_sorted,
)


@lru_cache(maxsize=None)
def leaf_depth_profiles(n: int) -> frozenset:
    """All sorted leaf-depth tuples of full binary trees with n leaves."""
    if n == 1:
        return frozenset({(0,)})
    out = set()
    for k in range(1, n):
        for left in leaf_depth_profiles(k):
            for right in leaf_depth_profiles(n - k):
                out.add(tuple(sorted(d + 1 for d in left + right)))
    return frozenset(out)


def brute_force_cost(weights):
    """Minimum of sum w_i l_i over all full binary trees with n leaves.

    For a fixed tree, the best assignment puts the largest weight on the
    shallowest leaf (rearrangement inequality).
    """
    ws = sorted(weights, reverse=True)
    return min(sum(w * d for w, d in zip(ws, prof)) for prof in leaf_depth_profiles(len(ws)))


def entropy(p):
    return -sum(x * math.log2(x) for x in p if x > 0)


def test_worked_example() -> None:
    w = [12, 9, 8, 7, 6, 4, 3, 1]
    lengths = code_lengths(huffman_tree(w), len(w))
    assert lengths == [2, 2, 3, 3, 3, 4, 5, 5]
    assert cost(w, lengths) == 141


def test_optimal_against_all_full_binary_trees() -> None:
    rng = random.Random(1)
    for n in range(1, 8):
        for _ in range(60):
            w = [rng.randint(1, 30) for _ in range(n)]
            lengths = code_lengths(huffman_tree(w), n)
            assert cost(w, lengths) == brute_force_cost(w)


def test_two_queue_matches_heap() -> None:
    rng = random.Random(2)
    for _ in range(300):
        n = rng.randint(1, 40)
        w = sorted(rng.randint(1, 50) for _ in range(n))
        a = cost(w, code_lengths(huffman_tree(w), n))
        b = cost(w, code_lengths(huffman_tree_sorted(w), n))
        assert a == b


def test_two_queue_tie_break_gives_smallest_max_length() -> None:
    rng = random.Random(3)
    for _ in range(200):
        n = rng.randint(2, 7)
        w = sorted(rng.randint(1, 6) for _ in range(n))  # many ties
        best = brute_force_cost(w)
        ws = sorted(w, reverse=True)
        min_max = min(
            max(p) for p in leaf_depth_profiles(n) if sum(x * d for x, d in zip(ws, p)) == best
        )
        lengths = code_lengths(huffman_tree_sorted(w), n)
        assert cost(w, lengths) == best
        assert max(lengths) == min_max


def test_kraft_and_entropy_bounds() -> None:
    rng = random.Random(4)
    sigma = 1 - math.log2(math.e) + math.log2(math.log2(math.e))  # about 0.0861
    for _ in range(500):
        n = rng.randint(2, 30)
        w = [rng.random() ** 3 + 1e-9 for _ in range(n)]
        s = sum(w)
        p = [x / s for x in w]
        lengths = code_lengths(huffman_tree(p), n)
        assert abs(sum(2.0 ** -l for l in lengths) - 1) < 1e-12  # a full tree
        h = entropy(p)
        avg = cost(p, lengths)
        assert h - 1e-9 <= avg < h + 1
        assert avg - h <= max(p) + sigma + 1e-9  # Gallager 1978


def test_fibonacci_weights_give_the_deepest_tree() -> None:
    fib = [1, 1]
    while len(fib) < 20:
        fib.append(fib[-1] + fib[-2])
    for n in range(2, 21):
        lengths = code_lengths(huffman_tree(fib[:n]), n)
        assert max(lengths) == n - 1


def test_round_trip() -> None:
    rng = random.Random(5)
    cases = [
        "a",
        "aaaaaaa",
        "ab",
        "abababbbbbbbbbbb",
        "abracadabra",
        bytes(rng.randrange(256) for _ in range(2000)),
        bytes(rng.choice(b"aaaaaaabbbc") for _ in range(2000)),
    ]
    for msg in cases:
        freq: dict = {}
        for s in msg:
            freq[s] = freq.get(s, 0) + 1
        code = huffman_code(freq)
        words = list(code.values())
        for x in words:
            for y in words:
                assert x == y or not y.startswith(x)  # prefix free
        bits = encode(msg, code)
        assert decode(bits, code) == list(msg)
        if len(freq) > 1:
            n = len(freq)
            syms = sorted(freq, key=repr)
            assert len(bits) == brute_force_cost([freq[s] for s in syms]) if n <= 7 else True


def test_single_and_two_symbols() -> None:
    assert codewords(huffman_tree([5]), 1) == ["0"]
    assert sorted(codewords(huffman_tree([5, 9]), 2)) == ["0", "1"]
