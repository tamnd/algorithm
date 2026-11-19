# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hierarchical-softmax/. The authors are listed in prov/5QHTPW.jsonl.

import itertools
import math
import random

from hierarchical_softmax import (
    balanced_paths,
    entropy_bits,
    expected_length,
    huffman_paths,
    log_prob,
    loss_gradient,
)


def is_prefix_free(paths):
    codes = [tuple(b for _, b in p) for p in paths]
    return all(a[: len(b)] != b for a in codes for b in codes if a is not b and len(a) >= len(b))


def test_hand_example():
    paths = [[(0, 0)], [(0, 1), (1, 0)], [(0, 1), (1, 1), (2, 0)], [(0, 1), (1, 1), (2, 1)]]
    nodes = [[0.5], [-1.0], [2.0]]
    p = [math.exp(log_prob([1.0], nodes, q)) for q in paths]
    assert [round(x, 4) for x in p] == [0.6225, 0.1015, 0.2431, 0.0329]
    assert abs(sum(p) - 1.0) < 1e-12


def test_huffman_lengths_and_entropy():
    counts = [5, 2, 1, 1]
    paths = huffman_paths(counts)
    assert sorted(len(p) for p in paths) == [1, 2, 3, 3]
    assert len(paths[0]) == 1
    assert abs(expected_length(counts, paths) - 15 / 9) < 1e-12
    assert round(entropy_bits(counts), 4) == 1.6577


def test_probabilities_sum_to_one_over_vocabulary():
    rng = random.Random(1)
    for v in (2, 3, 7, 16, 50):
        counts = [rng.randint(1, 100) for _ in range(v)]
        for paths in (huffman_paths(counts), balanced_paths(v)):
            assert is_prefix_free(paths)
            nodes_used = {n for p in paths for n, _ in p}
            assert nodes_used == set(range(v - 1))
            nodes = [[rng.gauss(0, 2) for _ in range(5)] for _ in range(v - 1)]
            for _ in range(3):
                h = [rng.gauss(0, 1) for _ in range(5)]
                total = sum(math.exp(log_prob(h, nodes, p)) for p in paths)
                assert abs(total - 1.0) < 1e-12


def test_balanced_depth():
    for v in range(2, 51):
        assert max(len(p) for p in balanced_paths(v)) == math.ceil(math.log2(v))


def test_huffman_is_optimal_against_all_length_vectors():
    rng = random.Random(2)
    for v in (2, 3, 4, 5, 6):
        for _ in range(5):
            counts = [rng.randint(1, 30) for _ in range(v)]
            best = min(
                sum(c * l for c, l in zip(counts, lengths))
                for lengths in itertools.product(range(1, v), repeat=v)
                if sum(2.0 ** -l for l in lengths) <= 1.0
            )
            got = sum(c * len(p) for c, p in zip(counts, huffman_paths(counts)))
            assert got == best
            h = entropy_bits(counts)
            assert h <= expected_length(counts, huffman_paths(counts)) < h + 1


def test_gradient_against_finite_differences():
    rng = random.Random(3)
    counts = [9, 4, 4, 2, 1, 1]
    paths = huffman_paths(counts)
    nodes = [[rng.uniform(-1, 1) for _ in range(4)] for _ in range(5)]
    h = [rng.uniform(-1, 1) for _ in range(4)]
    eps = 1e-6
    for path in paths:
        _, gh, gn = loss_gradient(h, nodes, path)
        for vec, grad in [(h, gh)] + [(nodes[n], gn.get(n, [0.0] * 4)) for n in range(5)]:
            for k in range(4):
                old = vec[k]
                vec[k] = old + eps
                up = -log_prob(h, nodes, path)
                vec[k] = old - eps
                down = -log_prob(h, nodes, path)
                vec[k] = old
                assert abs((up - down) / (2 * eps) - grad[k]) < 1e-5
