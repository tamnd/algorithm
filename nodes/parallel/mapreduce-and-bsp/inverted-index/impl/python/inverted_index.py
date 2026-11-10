# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/inverted-index/. The authors are listed in prov/GZMPCF.jsonl.

"""Building a positional inverted index with MapReduce, on a small simulator.

Baseline: map emits (term, (doc, position)) for each token; the reducer buffers
and sorts the postings of a term in memory.
Value-to-key: map emits ((term, doc), (doc, positions)) once per term and
document; the partitioner and the grouping use the term only, so the postings
arrive in document order and the reducer gap-encodes them as they stream past.
"""

import itertools
import random
import zlib
from typing import Any, Callable, Iterable

Pair = tuple[Any, Any]
Postings = list[tuple[int, list[int]]]  # [(doc id, [positions])] in increasing doc id


def stable_hash(key: Any) -> int:
    return zlib.crc32(repr(key).encode("utf-8"))


def run_round(splits: list[list[Pair]], mapper: Callable, reducer: Callable, r: int,
              partitioner: Callable[[Any, int], int] | None = None,
              group_key: Callable[[Any], Any] | None = None,
              rng: random.Random | None = None) -> tuple[list[list[Pair]], int, int]:
    """One round. Returns (output per reducer, pairs shuffled, largest reducer input in pairs)."""
    partitioner = partitioner or (lambda k, n: stable_hash(k) % n)
    group_key = group_key or (lambda k: k)
    inbox: list[list[Pair]] = [[] for _ in range(r)]
    sent = 0
    for split in splits:  # independent map tasks
        for k, v in (kv for rec in split for kv in mapper(*rec)):
            inbox[partitioner(k, r)].append((k, v))
            sent += 1
    outputs = []
    for box in inbox:  # independent reducers
        if rng is not None:
            rng.shuffle(box)
        box.sort(key=lambda kv: kv[0])
        out = []
        for _, run in itertools.groupby(box, key=lambda kv: group_key(kv[0])):
            run = list(run)
            out.extend(reducer(run[0][0], [v for _, v in run]))
        outputs.append(out)
    return outputs, sent, max((len(b) for b in inbox), default=0)


def make_splits(records: list[Any], m: int) -> list[list[Any]]:
    n = len(records)
    bounds = [i * n // m for i in range(m + 1)]
    return [records[bounds[i]:bounds[i + 1]] for i in range(m)]


# The single-machine index, the reference.

def build_index_one_machine(docs: list[tuple[int, str]]) -> dict[str, Postings]:
    index: dict[str, dict[int, list[int]]] = {}
    for d, text in docs:
        for p, t in enumerate(text.split()):
            index.setdefault(t, {}).setdefault(d, []).append(p)
    return {t: sorted(by_doc.items()) for t, by_doc in index.items()}


# Baseline: one pair per token, sort in the reducer.

def baseline_map(doc: int, text: str) -> Iterable[Pair]:
    for p, t in enumerate(text.split()):
        yield (t, (doc, p))


def baseline_reduce(term: str, values: list[tuple[int, int]]) -> Iterable[Pair]:
    values = sorted(values)  # the buffer and in-memory sort that does not scale
    yield (term, [(d, [p for _, p in run]) for d, run in itertools.groupby(values, key=lambda dp: dp[0])])


def build_index_baseline(docs: list[tuple[int, str]], m: int, r: int,
                         rng: random.Random | None = None) -> tuple[dict[str, Postings], int, int]:
    outputs, sent, largest = run_round(make_splits(docs, m), baseline_map, baseline_reduce, r, rng=rng)
    return {t: ps for out in outputs for t, ps in out}, sent, largest


# Gap encoding with variable-byte codes.

def vbyte(n: int) -> bytes:
    """Variable-byte code of n >= 1: 7 bits per byte, most significant group first, high bit on the last byte."""
    groups = [n & 0x7F]
    n >>= 7
    while n:
        groups.append(n & 0x7F)
        n >>= 7
    groups.reverse()
    groups[-1] |= 0x80
    return bytes(groups)


def vbyte_decode(data: bytes) -> list[int]:
    nums, n = [], 0
    for b in data:
        n = (n << 7) | (b & 0x7F)
        if b & 0x80:
            nums.append(n)
            n = 0
    return nums


def gaps(sorted_ids: list[int]) -> list[int]:
    """Gaps of increasing ids >= 0, with -1 before the first, so every gap is >= 1."""
    return [b - a for a, b in zip([-1] + sorted_ids, sorted_ids)]


def encode_postings(postings: Postings) -> bytes:
    """Doc gaps; for each doc its term frequency and its position gaps, all in variable-byte."""
    out = bytearray()
    for g, (_, ps) in zip(gaps([d for d, _ in postings]), postings):
        out += vbyte(g) + vbyte(len(ps)) + b"".join(vbyte(x) for x in gaps(ps))
    return bytes(out)


def decode_postings(data: bytes) -> Postings:
    nums = vbyte_decode(data)
    postings, i, d = [], 0, -1
    while i < len(nums):
        d += nums[i]
        tf = nums[i + 1]
        ps = list(itertools.accumulate(nums[i + 2:i + 2 + tf], initial=-1))[1:]
        postings.append((d, ps))
        i += 2 + tf
    return postings


def gamma_bits(n: int) -> int:
    """Length in bits of the Elias gamma code of n >= 1."""
    return 2 * (n.bit_length() - 1) + 1


# Value-to-key: one pair per (term, doc), sorted by the framework.

def vtk_map(doc: int, text: str) -> Iterable[Pair]:
    positions: dict[str, list[int]] = {}
    for p, t in enumerate(text.split()):
        positions.setdefault(t, []).append(p)
    for t, ps in positions.items():
        yield ((t, doc), (doc, ps))


def vtk_reduce(key: tuple, values: list[tuple[int, list[int]]]) -> Iterable[Pair]:
    # The values arrive in increasing doc id, so there is no sort here.
    # A real reducer would write each encoded posting at once and keep only the last doc id.
    postings = list(values)
    yield (key[0], (postings, encode_postings(postings)))


def build_index_vtk(docs: list[tuple[int, str]], m: int, r: int, rng: random.Random | None = None
                    ) -> tuple[dict[str, Postings], dict[str, bytes], int, int]:
    outputs, sent, largest = run_round(make_splits(docs, m), vtk_map, vtk_reduce, r,
                                       partitioner=lambda k, n: stable_hash(k[0]) % n,
                                       group_key=lambda k: k[0], rng=rng)
    index = {t: ps for out in outputs for t, (ps, _) in out}
    encoded = {t: code for out in outputs for t, (_, code) in out}
    return index, encoded, sent, largest
