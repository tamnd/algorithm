# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/trellis/. The authors are listed in prov/ZSECMK.jsonl.

import itertools
import random

from trellis import (
    codewords_from_generator,
    convolutional_trellis,
    minimal_profile,
    paths,
    state_profile,
    syndrome_trellis,
    tail_biting_paths,
)

H74 = [[1, 0, 1, 1, 1, 0, 0], [1, 1, 1, 0, 0, 1, 0], [0, 1, 1, 1, 0, 0, 1]]
G74 = [[1, 0, 0, 0, 1, 1, 0], [0, 1, 0, 0, 0, 1, 1], [0, 0, 1, 0, 1, 1, 1], [0, 0, 0, 1, 1, 0, 1]]


def null_space_words(h):
    n = len(h[0])
    return {c for c in itertools.product((0, 1), repeat=n) if all(sum(a * b for a, b in zip(r, c)) % 2 == 0 for r in h)}


def test_hamming_trellis_paths_are_codewords() -> None:
    t = syndrome_trellis(H74)
    words = list(paths(t))
    assert len(words) == len(set(words)) == 16
    assert set(words) == codewords_from_generator(G74) == null_space_words(H74)
    assert state_profile(t) == [1, 2, 4, 8, 8, 4, 2, 1]


def test_hamming_other_order() -> None:
    # columns 1..7 in binary: a different coordinate order of the same code
    h = [[(j >> r) & 1 for j in range(1, 8)] for r in range(3)]
    t = syndrome_trellis(h)
    assert set(paths(t)) == null_space_words(h)
    assert state_profile(t) == [1, 2, 4, 4, 8, 4, 2, 1]


def test_syndrome_trellis_is_minimal_on_random_codes() -> None:
    rng = random.Random(11)
    for _ in range(150):
        n = rng.randrange(2, 9)
        r = rng.randrange(1, n + 1)
        h = [[rng.randrange(2) for _ in range(n)] for _ in range(r)]
        t = syndrome_trellis(h)
        words = set(paths(t))
        assert words == null_space_words(h)
        assert state_profile(t) == minimal_profile(words)


def test_each_edge_is_on_a_path() -> None:
    t = syndrome_trellis(H74)
    starts = [{0}]
    for sec in t:
        assert {e[0] for e in sec} == starts[-1]
        starts.append({e[2] for e in sec})
    assert starts[-1] == {0}


def test_convolutional_trellis_terminated() -> None:
    def enc(bits):
        s, out = 0, []
        for u in list(bits) + [0, 0]:
            w = (u << 2) | s
            out += [bin(7 & w).count("1") & 1, bin(5 & w).count("1") & 1]
            s = w >> 1
        return tuple(out)

    for length in range(1, 7):
        t = convolutional_trellis([7, 5], 3, length)
        want = {enc(m) for m in itertools.product((0, 1), repeat=length)}
        assert set(paths(t)) == want


def test_tail_biting() -> None:
    def tb(bits):
        s = (bits[-1] << 1) | bits[-2]  # register holds the last two inputs
        out = []
        for u in bits:
            w = (u << 2) | s
            out += [bin(7 & w).count("1") & 1, bin(5 & w).count("1") & 1]
            s = w >> 1
        return tuple(out)

    for length in range(2, 7):
        want = {tb(m) for m in itertools.product((0, 1), repeat=length)}
        assert tail_biting_paths([7, 5], 3, length) == want
