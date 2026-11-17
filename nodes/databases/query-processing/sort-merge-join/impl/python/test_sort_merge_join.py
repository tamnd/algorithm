# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sort-merge-join/. The authors are listed in prov/CHDTJ2.jsonl.

import random
from collections import Counter

import pytest

from sort_merge_join import paginate, sort_merge_join


def reference(r_rows, s_rows):
    return Counter(r + s for r in r_rows for s in s_rows if r[0] == s[0])


def rand_rel(rng, tag):
    return [(rng.randrange(6), f"{tag}{i}") for i in range(rng.randrange(0, 25))]


def test_example() -> None:
    r = [(k, f"r{i}") for i, k in enumerate([7, 2, 9, 2, 4, 7, 1, 5])]
    s = [(k, f"s{i}") for i, k in enumerate([2, 7, 3, 7, 8, 2])]
    out, disk = sort_merge_join(paginate(r, 2), paginate(s, 2), 0, 0, 4, 2, 2)
    assert Counter(out) == reference(r, s) and len(out) == 8
    # M = 4 and N = 3 pages, B = 4: pass 0 makes one run of each, so the cost is 3(M + N).
    assert disk.reads + disk.writes == 3 * (4 + 3)


def test_edges() -> None:
    with pytest.raises(ValueError):
        sort_merge_join([], [], 0, 0, 2, 1, 1)
    for combined in (True, False):
        out, disk = sort_merge_join([], paginate([(1,)], 1), 0, 0, 3, 1, 1, combined)
        assert out == [] and disk.ios == 3
        out, disk = sort_merge_join([], [], 0, 0, 3, 1, 1, combined)
        assert out == [] and disk.ios == 0


def test_against_reference() -> None:
    rng = random.Random(40)
    for _ in range(600):
        r, s = rand_rel(rng, "r"), rand_rel(rng, "s")
        pr, ps, b = rng.randrange(1, 4), rng.randrange(1, 4), rng.randrange(3, 7)
        want = reference(r, s)
        for combined in (True, False):
            out, _ = sort_merge_join(paginate(r, pr), paginate(s, ps), 0, 0, b, pr, ps, combined)
            assert Counter(out) == want


def test_cost_two_pass_and_combined_exact() -> None:
    r = [(i, "r") for i in range(40)]          # M = 10 pages of 4
    s = [(2 * i, "s") for i in range(24)]      # N = 6 pages of 4
    rng = random.Random(1)
    rng.shuffle(r)
    rng.shuffle(s)
    rp, sp = paginate(r, 4), paginate(s, 4)
    # Runs of pass 0 fit (2 + 1 <= B - 2): 3(M + N).
    out, disk = sort_merge_join(rp, sp, 0, 0, 6, 4, 4)
    assert disk.ios == 3 * (10 + 6) and len(out) == 20
    # Without the combined pass, B = 6: R needs 2 passes, S 1 pass: 4M + 2N + M + N.
    _, disk = sort_merge_join(rp, sp, 0, 0, 6, 4, 4, combined=False)
    assert disk.ios == 4 * 10 + 2 * 6 + 10 + 6
    # B = 4: both need 2 passes, so 5(M + N), with or without combining.
    for combined in (True, False):
        _, disk = sort_merge_join(rp, sp, 0, 0, 4, 4, 4, combined)
        assert disk.ios == 5 * (10 + 6)


def test_textbook_numbers() -> None:
    # Ramakrishnan and Gehrke: M = 1000, N = 500 (one tuple per page here).
    r = [(i % 400, i) for i in range(1000)]
    s = [(i, -i) for i in range(500)]
    random.Random(3).shuffle(r)
    rp, sp = paginate(r, 1), paginate(s, 1)
    _, disk = sort_merge_join(rp, sp, 0, 0, 35, 1, 1, combined=False)
    assert disk.ios == 7500
    _, disk = sort_merge_join(rp, sp, 0, 0, 300, 1, 1)
    assert disk.ios == 4500
    _, disk = sort_merge_join(rp, sp, 0, 0, 35, 1, 1)
    assert disk.ios == 2000 + 1000 + 2000 + 1500


def test_all_keys_equal_worst_case() -> None:
    r = [(0, i) for i in range(8)]     # M = 4
    s = [(0, -i) for i in range(6)]    # N = 3
    for combined in (True, False):
        out, disk = sort_merge_join(paginate(r, 2), paginate(s, 2), 0, 0, 3, 2, 2, combined)
        assert len(out) == 48
        # Sort R in 2 passes, S in 1; merge M + N; rescan S for 3 later pages of R.
        assert disk.ios == 2 * 4 * 2 + 2 * 3 + 4 + 3 + 3 * 3
    r = [(0, i) for i in range(20)]    # M = 10
    s = [(0, -i) for i in range(12)]   # N = 6
    out, disk = sort_merge_join(paginate(r, 2), paginate(s, 2), 0, 0, 6, 2, 2)
    assert len(out) == 240
    # Combined pass with 2 + 1 runs, one free frame: the S group is spilled once
    # (6 writes) and read for the 9 later pages of R.
    assert disk.ios == 3 * (10 + 6) + 6 + 9 * 6
