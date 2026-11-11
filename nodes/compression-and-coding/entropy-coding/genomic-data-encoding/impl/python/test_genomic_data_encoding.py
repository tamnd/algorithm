# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/genomic-data-encoding/. The authors are listed in prov/9E652P.jsonl.

import random

import pytest

from genomic_data_encoding import (
    bs_base,
    bs_code,
    pack,
    packed_size,
    ref_decode,
    ref_encode,
    unpack,
)

# UCSC Genome Browser, file format FAQ, ".2bit format" (genome.ucsc.edu/FAQ/FAQformat.html#format7),
# copied by hand: T = 00, C = 01, A = 10, G = 11; the first base in the most significant
# two bits of a byte. TCAG therefore packs to 0b00011011 = 0x1B.
UCSC_TCAG = 0x1B


def test_ucsc_base_codes() -> None:
    n, b, nb, exc = pack("TCAG")
    assert (n, b, nb, exc) == (4, bytes([UCSC_TCAG]), [], [])
    assert pack("GACT")[1] == bytes([0b11100100])


def test_worked_example_pack() -> None:
    x = "ACGTNNNNCAYG"
    n, b, nb, exc = pack(x)
    assert n == 12
    assert b == bytes([0x9C, 0x00, 0x63])
    assert nb == [(4, 4)]
    assert exc == [(10, "Y")]
    assert unpack(n, b, nb, exc) == x
    assert packed_size(n, nb, exc) == 4 + 3 + 4 + 8 + 4 + 5


def test_worked_example_reference() -> None:
    ref = "ACGTACGTTAGCCATG"
    reads = [(2, "GTACTT"), (5, "CGTTAGC"), (9, "AGCAATG")]
    data = ref_encode(ref, reads)
    assert data == bytes([0x02, 0x06, 0x01, 0x12, 0x03, 0x07, 0x00, 0x04, 0x07, 0x01, 0x0C])
    assert ref_decode(ref, data, 3) == reads


def test_substitution_codes() -> None:
    for r in "ACGTN":
        others = [c for c in "ACGTN" if c != r]
        assert [bs_code(r, c) for c in others] == [0, 1, 2, 3]
        assert [bs_base(r, k) for k in range(4)] == others


def random_dna(rng: random.Random, n: int) -> str:
    out = []
    while len(out) < n:
        t = rng.random()
        if t < 0.01:
            out.extend("N" * rng.randrange(1, 30))
        elif t < 0.015:
            out.append(rng.choice("RYSWKMBDHV"))
        else:
            out.append(rng.choice("ACGT"))
    return "".join(out[:n])


def oracle_blocks(x: str) -> tuple[list[tuple[int, int]], list[tuple[int, str]]]:
    blocks = []
    i = 0
    while i < len(x):
        if x[i] == "N":
            j = i
            while j < len(x) and x[j] == "N":
                j += 1
            blocks.append((i, j - i))
            i = j
        else:
            i += 1
    exc = [(i, c) for i, c in enumerate(x) if c not in "ACGTN"]
    return blocks, exc


def test_pack_random_round_trip() -> None:
    rng = random.Random(2024)
    for _ in range(500):
        x = random_dna(rng, rng.randrange(0, 400))
        n, b, nb, exc = pack(x)
        assert len(b) == (n + 3) // 4
        assert (nb, exc) == oracle_blocks(x)
        assert unpack(n, b, nb, exc) == x


def mutate(rng: random.Random, y: str, rate: float) -> str:
    out = list(y)
    for j in range(len(out)):
        if rng.random() < rate:
            out[j] = rng.choice([c for c in "ACGTN" if c != out[j]])
    return "".join(out)


def make_reads(rng: random.Random, ref: str, m: int, length: int, rate: float) -> list[tuple[int, str]]:
    starts = sorted(rng.randrange(0, len(ref) - length + 1) for _ in range(m))
    return [(p, mutate(rng, ref[p : p + length], rate)) for p in starts]


def test_reference_random_round_trip() -> None:
    rng = random.Random(7)
    for _ in range(500):
        ref = "".join(rng.choice("ACGT") for _ in range(rng.randrange(50, 600)))
        m = rng.randrange(0, 20)
        length = rng.randrange(1, 50)
        reads = make_reads(rng, ref, m, length, rng.choice([0.0, 0.01, 0.1, 0.5]))
        data = ref_encode(ref, reads)
        assert ref_decode(ref, data, m) == reads


def test_sizes_on_generated_reads() -> None:
    rng = random.Random(1)
    ref = "".join(rng.choice("ACGT") for _ in range(100_000))
    reads = make_reads(rng, ref, 2000, 100, 0.01)
    ascii_bytes = sum(len(y) for _, y in reads)
    two_bit_bytes = sum((len(y) + 3) // 4 for _, y in reads)
    data = ref_encode(ref, reads)
    assert ref_decode(ref, data, len(reads)) == reads
    assert ascii_bytes == 200_000
    assert two_bit_bytes == 50_000
    subs = sum(sum(a != b for a, b in zip(y, ref[p : p + 100])) for p, y in reads)
    # An independent count: a varint takes ceil(bits / 7) bytes. Each read has a
    # position delta (the mean gap is 50), a length and a count, and each
    # substitution takes 1 byte if its offset delta is below 32 and 2 bytes if not.
    expected = 0
    prev = 0
    for p, y in reads:
        diffs = [j for j in range(len(y)) if y[j] != ref[p + j]]
        expected += ulen(p - prev) + ulen(len(y)) + ulen(len(diffs))
        expected += sum(1 if j - i < 32 else 2 for i, j in zip([0] + diffs, diffs))
        prev = p
    assert len(data) == expected == SIZE_SEED_1
    assert subs == SUBS_SEED_1
    assert len(data) < 3 * len(reads) + 2 * subs + 200
    # The reference genome itself packs to a quarter of its ASCII size.
    n, b, nb, exc = pack(ref)
    assert len(b) == 25_000 and nb == [] and exc == []


SIZE_SEED_1 = 9093
SUBS_SEED_1 = 1979


def ulen(v: int) -> int:
    return max(1, -(-v.bit_length() // 7))


def test_edge_cases() -> None:
    assert pack("") == (0, b"", [], [])
    assert unpack(0, b"", [], []) == ""
    assert unpack(*pack("N")) == "N"
    assert pack("NNNNN")[2] == [(0, 5)]
    assert pack("NANN")[2] == [(0, 1), (2, 2)]
    with pytest.raises(ValueError):
        pack("ACGU")
    with pytest.raises(ValueError):
        pack("acgt")
    assert ref_decode("ACGT", ref_encode("ACGT", []), 0) == []
    assert ref_decode("ACGT", ref_encode("ACGT", [(0, "NNNN")]), 1) == [(0, "NNNN")]
    with pytest.raises(ValueError):
        ref_encode("ACGT", [(2, "GTA")])
    with pytest.raises(ValueError):
        ref_encode("ACGTACGT", [(3, "TA"), (1, "CG")])
