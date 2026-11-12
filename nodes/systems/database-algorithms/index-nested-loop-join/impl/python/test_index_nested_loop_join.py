# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/index-nested-loop-join/. The authors are listed in prov/N97W1G.jsonl.

import random
from collections import Counter

from index_nested_loop_join import (BPlusTreeIndex, Disk, HashIndex, index_nested_loop_join,
                                    paginate)


def reference(r_rows, s_rows):
    return Counter(r + s for r in r_rows for s in s_rows if r[0] == s[0])


def rand_rel(rng, tag):
    return [(rng.randrange(6), f"{tag}{i}") for i in range(rng.randrange(0, 15))]


def test_against_reference() -> None:
    rng = random.Random(33)
    for _ in range(600):
        r, s = rand_rel(rng, "r"), rand_rel(rng, "s")
        pr, ps = rng.randrange(1, 4), rng.randrange(1, 4)
        want = reference(r, s)
        sp_sorted = paginate(sorted(s), ps)
        for index, sp, clustered in (
                (HashIndex(paginate(s, ps), 0, rng.randrange(1, 5), rng.randrange(1, 4)),
                 paginate(s, ps), False),
                (BPlusTreeIndex(paginate(s, ps), 0, rng.randrange(1, 4), rng.randrange(2, 4)),
                 paginate(s, ps), False),
                (BPlusTreeIndex(sp_sorted, 0, rng.randrange(1, 4), rng.randrange(2, 4)),
                 sp_sorted, True)):
            out, disk = index_nested_loop_join(paginate(r, pr), sp, 0, index, clustered)
            assert Counter(out) == want
            # The cost is M plus the sum of the probe costs, probe by probe.
            probe_cost = 0
            for row in r:
                d = Disk()
                rids = index.probe(row[0], d)
                pages = len({p for p, _ in rids}) if clustered else len(rids)
                probe_cost += d.reads + pages
            assert disk.reads == len(paginate(r, pr)) + probe_cost


def test_btree_probe_reads_exactly_the_leaves_with_the_key() -> None:
    rng = random.Random(5)
    for _ in range(300):
        s = [(rng.randrange(8), i) for i in range(rng.randrange(0, 40))]
        t = BPlusTreeIndex(paginate(s, 3), 0, rng.randrange(1, 5), rng.randrange(2, 5))
        leaves, node = [], t.root
        while not hasattr(node, "entries"):
            node = node.children[0]
        while node is not None:
            leaves.append(node)
            node = node.next
        for key in range(-1, 9):
            d = Disk()
            rids = t.probe(key, d)
            assert sorted(rids) == sorted((p, i) for p, page in enumerate(paginate(s, 3))
                                          for i, row in enumerate(page) if row[0] == key)
            holding = sum(1 for lf in leaves if any(k == key for k, _ in lf.entries))
            if key <= max([k for k, _ in s], default=-2):
                assert d.reads == t.height + max(1, holding)
            else:
                assert d.reads == 1


def test_cost_formula_exact_hash() -> None:
    # S has unique keys 0..39 on N = 10 pages, 64 buckets, no overflow page.
    # R: M = 8 pages of p = 5 tuples, each with exactly one match.
    s = [(k, -k) for k in range(40)]
    r = [(k % 40, k) for k in range(40)]
    idx = HashIndex(paginate(s, 4), 0, 64, 4)
    out, disk = index_nested_loop_join(paginate(r, 5), paginate(s, 4), 0, idx)
    assert len(out) == 40
    assert disk.reads == 8 + 5 * 8 * (1 + 1)


def test_cost_formula_exact_btree() -> None:
    # 64 entries, 16 leaves of 4, fanout 4: 4 inner nodes and a root, so h = 2.
    s = [(k, -k) for k in range(64)]
    r = [(k, k) for k in range(64)]
    t = BPlusTreeIndex(paginate(s, 8), 0, 4, 4)
    assert t.height == 2
    _, disk = index_nested_loop_join(paginate(r, 8), paginate(s, 8), 0, t, clustered=True)
    assert disk.reads == 8 + 8 * 8 * (2 + 1 + 1)
    # Unclustered, c = 3 matches per key, all in one leaf (keys 0..15, leaf size 3).
    s3 = [(k // 3, k) for k in range(48)]
    rng = random.Random(2)
    rng.shuffle(s3)
    t3 = BPlusTreeIndex(paginate(s3, 6), 0, 3, 4)
    r3 = [(k, k) for k in range(16)]
    out, disk = index_nested_loop_join(paginate(r3, 4), paginate(s3, 6), 0, t3)
    assert len(out) == 48 and t3.height == 2
    assert disk.reads == 4 + 4 * 4 * (2 + 1 + 3)


def test_empty() -> None:
    idx = BPlusTreeIndex([], 0, 2, 2)
    out, disk = index_nested_loop_join(paginate([(1,), (2,)], 1), [], 0, idx)
    assert out == [] and disk.reads == 2 + 2
    out, disk = index_nested_loop_join([], [], 0, HashIndex([], 0, 3, 2))
    assert out == [] and disk.reads == 0
