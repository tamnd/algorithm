# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hoyer-neerbek-shi-ordered-search/. The authors are listed in prov/M3Z7WG.jsonl.
import math

from hoyer_neerbek_shi_ordered_search import layout, ordered_search, plan, queries, u2_block
from qsim import TOL, is_unitary, probabilities


def monotone(m, a):
    return [0] * a + [1] * (m - a)


def test_exact_for_every_input():
    # every monotone string of length m <= 64 with last bit 1
    for m in range(1, 65):
        for a in range(m):
            f, q, amp = ordered_search(monotone(m, a))
            p = probabilities([complex(t) for t in amp])
            assert f == a
            assert abs(p[a] - 1) < TOL
            assert abs(sum(p) - 1) < TOL
            assert q == queries(m)


def test_trace_n10():
    # the trace on the page: N = 10, answer 6, two colors, three queries
    f, q, amp = ordered_search(monotone(10, 6))
    assert (f, q) == (6, 3)
    assert plan(10) == (3, 1)
    blocks, colors, load = layout(10, 1)
    assert blocks == [(0, 2), (4, 2), (8, 1)]
    assert colors == [[[1], [0]], [[0], [1]], [[0, 1]]]
    assert load == [4, 4]


def test_pebbling_conditions():
    for m in range(2, 200):
        for s in range(0, 4):
            if (1 << (s + 1)) > m + (m & 1):
                continue
            blocks, colors, load = layout(m, s)
            assert sum(1 << h for _, h in blocks) == m + (m & 1)
            for (_, h), sets in zip(blocks, colors):
                # (A): every color sits on exactly one depth of the block
                flat = sorted(c for level in sets for c in level)
                assert flat == list(range(1 << s))
                # (B), tight: pebbles at depth j equal the pebbles on all ancestors (j >= 1)
                sizes = [len(level) for level in sets]
                for j in range(1, h):
                    assert sizes[j] == sum(sizes[:j])
            # load[c] = |V_c|, the size of the subproblem of color c
            assert sum(load) == sum(sum(len(lv) << j for j, lv in enumerate(sets)) for sets in colors)


def test_u2_is_unitary():
    for h in range(1, 5):
        u = u2_block(h)
        assert is_unitary([[complex(v) for v in row] for row in u])


def test_query_counts():
    assert [queries(m) for m in (2, 4, 9, 10, 11, 28, 29, 64, 512, 4096)] == [1, 2, 3, 3, 4, 4, 5, 5, 7, 9]
    for m in range(2, 600):
        q = queries(m)
        assert q <= math.ceil(math.log2(m))  # never worse than binary search
        assert q > (math.log(m) - 1) / math.pi  # the HNS lower bound for exact algorithms
