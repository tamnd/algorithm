# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interleaving/. The authors are listed in prov/E58STP.jsonl.

import itertools
import random

from interleaving import (
    ConvolutionalDeinterleaver, ConvolutionalInterleaver, block_deinterleave, block_interleave,
    block_position, convolutional_delay, convolutional_memory, convolutional_position,
    hamming74_decode, hamming74_encode, interleaved_link, max_hits_per_codeword,
)


def burst_length(bits) -> int:
    ones = [i for i, b in enumerate(bits) if b]
    return ones[-1] - ones[0] + 1 if ones else 0


def test_block_round_trip_and_order() -> None:
    words = [["a0", "a1", "a2"], ["b0", "b1", "b2"]]
    x = block_interleave(words)
    assert x == ["a0", "b0", "a1", "b1", "a2", "b2"]
    assert block_deinterleave(x, 2) == words
    rng = random.Random(1)
    for _ in range(50):
        depth, n = rng.randrange(1, 9), rng.randrange(1, 9)
        words = [[rng.randrange(100) for _ in range(n)] for _ in range(depth)]
        assert block_deinterleave(block_interleave(words), depth) == words


def test_block_spreads_bursts_exhaustively() -> None:
    # every error pattern whose burst length is at most I b leaves, in each row, an error
    # pattern of burst length at most b; one of length I b + 1 can leave b + 1
    for depth in range(1, 5):
        for n in range(1, 13 // depth + 1):
            total = depth * n
            for b in range(1, n + 1):
                worst = 0
                for e in range(1, 1 << total):
                    bits = [(e >> i) & 1 for i in range(total)]
                    rows = block_deinterleave(bits, depth)
                    row_burst = max(burst_length(r) for r in rows)
                    if burst_length(bits) <= depth * b:
                        assert row_burst <= b
                        assert max(sum(r) for r in rows) <= b
                    elif burst_length(bits) == depth * b + 1:
                        worst = max(worst, row_burst)
                if depth * b + 1 <= total:
                    assert worst == b + 1


def test_template_with_hamming_code() -> None:
    depth, rng = 5, random.Random(3)
    messages = [[rng.randrange(2) for _ in range(4)] for _ in range(depth)]
    total = 7 * depth
    # every burst of length at most I t = 5 is corrected (t = 1 for the Hamming code)
    for length in range(1, depth + 1):
        for start in range(total - length + 1):
            inner = list(range(start + 1, start + length - 1))
            for k in range(len(inner) + 1):
                for mid in itertools.combinations(inner, k):
                    pos = {start, start + length - 1, *mid}

                    def channel(x, pos=pos):
                        return [s ^ 1 if i in pos else s for i, s in enumerate(x)]

                    assert interleaved_link(messages, hamming74_encode, hamming74_decode, channel) == messages
    # a solid burst of length 6 puts two errors into codeword 0, which then decodes wrongly

    def burst6(x):
        return [s ^ 1 if i < 6 else s for i, s in enumerate(x)]

    out = interleaved_link(messages, hamming74_encode, hamming74_decode, burst6)
    assert out[0] != messages[0] and out[1:] == messages[1:]
    # without interleaving, a burst of length 2 already defeats the code
    word = hamming74_encode(messages[0])
    word[0] ^= 1
    word[1] ^= 1
    assert hamming74_decode(word) != messages[0]


def test_convolutional_interleaver_structure() -> None:
    for branches, unit in [(2, 1), (3, 2), (4, 3), (12, 17)]:
        count = branches * (branches * unit + 3) * 3
        inter = ConvolutionalInterleaver(branches, unit)
        out = inter.run(list(range(count)))
        for q, u in enumerate(out):
            if u is not None:
                assert convolutional_position(u, branches, unit) == q
        deint = ConvolutionalDeinterleaver(branches, unit)
        back = deint.run(out)
        delay = convolutional_delay(branches, unit)
        assert back[delay:] == list(range(count - delay))
        assert sum(len(line) for line in inter.lines) == convolutional_memory(branches, unit)
        assert sum(len(line) for line in deint.lines) == convolutional_memory(branches, unit)


def test_convolutional_spreading() -> None:
    def worst(branches, unit, n, length, offset):
        count = n * (branches * unit + 2) * 3
        pos = [convolutional_position(u, branches, unit) for u in range(count)]
        return max_hits_per_codeword(pos, n, length, offset)

    # I J >= n + 1: any burst of length <= t I hits each codeword at most t times, whatever the alignment
    for branches, unit, n in [(3, 2, 5), (4, 2, 7), (3, 3, 8), (4, 3, 11), (5, 2, 9)]:
        assert branches * unit >= n + 1
        for offset in range(branches):
            for t in (1, 2, 3):
                assert worst(branches, unit, n, t * branches, offset) == t
    # I J = n: true when each codeword starts on branch 0, false otherwise
    for branches, unit in [(3, 2), (4, 3)]:
        n = branches * unit
        assert worst(branches, unit, n, branches, 0) == 1
        assert worst(branches, unit, n, branches, 1) == 2
    # I J < n: two symbols of one codeword can be next to each other on the channel
    assert worst(4, 2, 9, 4, 0) == 2


def test_dvb_parameters() -> None:
    # I = 12 branches, J = 17, codewords of n = 204 bytes starting on branch 0
    branches, unit, n = 12, 17, 204
    count = n * 40
    pos = [convolutional_position(u, branches, unit) for u in range(count)]
    assert max_hits_per_codeword(pos, n, 8 * branches, 0) == 8
    assert convolutional_memory(branches, unit) == 1122
    assert branches * n == 2448  # a block interleaver of the same depth stores this much
