# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mapreduce-communication-lower-bounds/. The authors are listed in prov/7HM42M.jsonl.

import math
import random
from itertools import combinations

from mapreduce_communication_lower_bounds import (hamming1_brute, hamming1_lower_bound,
                                                  hamming1_splitting, matmul_schema,
                                                  max_edges_in_subset, schema_stats,
                                                  triangle_lower_bound, triangle_schema,
                                                  triangles_brute,
                                                  triangles_from_schema)


def test_splitting_matches_brute_force_and_the_bound():
    for b in range(1, 11):
        all_pairs = hamming1_brute(range(1 << b))
        assert len(all_pairs) == b * (1 << (b - 1))
        for k in range(1, b + 1):
            if b % k:
                continue
            schema, found = hamming1_splitting(b, k)
            assert found == all_pairs
            q, r = schema_stats(schema, 1 << b)
            assert q == 1 << (b // k) and r == k
            assert len(schema) == k * (1 << (b - b // k))
            if q > 1:
                assert r == hamming1_lower_bound(b, q)  # the schema meets the bound


def test_splitting_on_input_subsets():
    rng = random.Random(9)
    for _ in range(40):
        b = rng.choice([4, 6, 8])
        k = rng.choice([d for d in range(1, b + 1) if b % d == 0])
        inputs = rng.sample(range(1 << b), rng.randint(0, 1 << b))
        _, found = hamming1_splitting(b, k, inputs)
        assert found == hamming1_brute(inputs)


def test_subset_edge_lemma():
    # At most (q/2) log2 q pairs at distance 1 among any q strings, with equality for subcubes.
    for b in (2, 3, 4):
        for q in range(1, (1 << b) + 1):
            if b == 4 and 5 <= q <= 11:
                continue  # skip the largest searches to keep the test fast
            best = max_edges_in_subset(b, q)
            assert best <= q / 2 * math.log2(q) + 1e-9
            if q & (q - 1) == 0:
                assert best == q // 2 * (q.bit_length() - 1)


def test_triangle_schema():
    rng = random.Random(10)
    for n, k in [(6, 1), (6, 2), (9, 3), (12, 4), (10, 3)]:
        schema = triangle_schema(n, k)
        q, r = schema_stats(schema, n * (n - 1) // 2)
        assert r == k
        assert r >= triangle_lower_bound(n, q)    # the lower bound, with exact |I| and |O|
        assert r <= 3 * n / math.sqrt(2 * q)      # this schema is within a factor 3
        for _ in range(5):
            edges = [e for e in combinations(range(n), 2) if rng.random() < 0.5]
            assert sorted(triangles_from_schema(schema, k, edges)) == triangles_brute(n, edges)


def test_matmul_schema():
    rng = random.Random(11)
    for n, g in [(4, 1), (4, 2), (6, 3), (8, 4), (6, 6)]:
        A = [[rng.randint(-3, 3) for _ in range(n)] for _ in range(n)]
        B = [[rng.randint(-3, 3) for _ in range(n)] for _ in range(n)]
        C, schema = matmul_schema(A, B, g)
        assert C == [[sum(A[i][t] * B[t][j] for t in range(n)) for j in range(n)] for i in range(n)]
        q, r = schema_stats(schema, 2 * n * n)
        assert q == 2 * n * n // g and r == g
        assert r == 2 * n * n / q  # the lower bound r >= 2n^2/q holds with equality
