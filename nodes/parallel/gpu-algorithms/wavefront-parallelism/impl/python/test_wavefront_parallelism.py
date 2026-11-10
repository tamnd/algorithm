# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wavefront-parallelism/. The authors are listed in prov/PPA3V1.jsonl.
import random

from wavefront_parallelism import (
    cells_on_diagonal, edit_distance_rows, edit_distance_wavefront, simt_diagonal_buffers,
    smith_waterman_rows, smith_waterman_wavefront, tiled_wavefront_rounds,
)


def rand_str(rng, k, alphabet="ACGT"):
    return "".join(rng.choice(alphabet) for _ in range(k))


def test_edit_distance_matches_rows():
    assert edit_distance_rows("kitten", "sitting") == 3
    assert edit_distance_wavefront("kitten", "sitting")[0] == 3
    for seed in range(60):
        rng = random.Random(seed)
        a, b = rand_str(rng, rng.randrange(0, 25)), rand_str(rng, rng.randrange(0, 25))
        d, rounds, widths = edit_distance_wavefront(a, b)
        assert d == edit_distance_rows(a, b)
        n, m = len(a), len(b)
        assert rounds == (n + m - 1 if n and m else max(0, n + m - 1))
        if n and m:
            assert rounds == n + m - 1
            assert sum(widths) == n * m
            assert max(widths) == min(n, m)
            assert widths == [cells_on_diagonal(d, n, m) for d in range(2, n + m + 1)]


def test_diagonal_count_and_widths():
    for n in range(1, 12):
        for m in range(1, 12):
            ws = [cells_on_diagonal(d, n, m) for d in range(2, n + m + 1)]
            assert len(ws) == n + m - 1 and all(w >= 1 for w in ws)
            assert sum(ws) == n * m
            assert cells_on_diagonal(1, n, m) == 0 and cells_on_diagonal(n + m + 1, n, m) == 0
    assert [cells_on_diagonal(d, 3, 5) for d in range(2, 9)] == [1, 2, 3, 3, 3, 2, 1]


def test_smith_waterman_matches_rows():
    for seed in range(40):
        rng = random.Random(100 + seed)
        a, b = rand_str(rng, rng.randrange(0, 20)), rand_str(rng, rng.randrange(0, 20))
        s, _ = smith_waterman_wavefront(a, b)
        assert s == smith_waterman_rows(a, b)


def test_simt_buffers_and_utilization():
    for seed in range(30):
        rng = random.Random(200 + seed)
        a, b = rand_str(rng, rng.randrange(0, 40)), rand_str(rng, rng.randrange(0, 40))
        threads = rng.choice([1, 4, 32])
        d, barriers, slots, busy = simt_diagonal_buffers(a, b, threads)
        assert d == edit_distance_rows(a, b)
        n, m = len(a), len(b)
        if n and m:
            assert barriers == n + m - 1
            assert busy == n * m
            assert slots >= busy
    # n = m = 32 with 32 threads: 63 rounds of 32 lanes for 1024 cells
    _, barriers, slots, busy = simt_diagonal_buffers("A" * 32, "C" * 32, 32)
    assert (barriers, slots, busy) == (63, 63 * 32, 1024)


def test_tiled_rounds():
    for n in range(1, 40, 7):
        for m in range(1, 40, 5):
            for b in (1, 4, 8):
                diags = {(i // b) + (j // b) for i in range(n) for j in range(m)}
                assert tiled_wavefront_rounds(n, m, b) == len(diags)
