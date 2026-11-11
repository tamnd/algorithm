# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/byte-pair-encoding/. The authors are listed in prov/8H71X7.jsonl.

"""Byte pair encoding, in its two uses.

1. Gage's compressor (1994). Work on blocks of bytes. In each block, replace the most
   frequent pair of adjacent bytes by a byte value that does not occur in the block, and
   record the pair in a table. Stop when no unused byte value is left or when the best
   pair is too rare to pay for its table entry.
   The container format here is this module's own: for each block, one byte k, then k
   entries (code, left, right), then the length of the packed block in 4 bytes (big
   endian), then the packed bytes. It is not the file format of Gage's program.
   Time: O(256 n) for n input bytes, because each block has at most 255 merges and each
   merge scans the block once.

2. The subword tokenizer of Sennrich, Haddow and Birch (2016). Learn merges on a table
   of word counts, then segment a word by applying the merges in the order learned.
"""

from typing import Sequence

Pair = tuple[int, int]


def _count_pairs(buf: Sequence[int]) -> dict[Pair, int]:
    """Non-overlapping occurrences of each adjacent pair (a run of k equal bytes counts k // 2)."""
    counts: dict[Pair, int] = {}
    last: dict[Pair, int] = {}
    for i in range(len(buf) - 1):
        pair = (buf[i], buf[i + 1])
        if pair[0] == pair[1] and last.get(pair) == i - 1:
            continue
        last[pair] = i
        counts[pair] = counts.get(pair, 0) + 1
    return counts


def compress_block(block: bytes, threshold: int = 4) -> tuple[list[tuple[int, int, int]], list[int]]:
    """Gage's loop on one block. Returns the pair table [(code, a, b)] and the packed block."""
    if threshold < 2:
        raise ValueError("threshold must be at least 2")
    buf = list(block)
    unused = sorted(set(range(256)) - set(buf))  # @line L1
    unused.reverse()  # pop() gives the smallest code
    table: list[tuple[int, int, int]] = []  # @line L2
    while unused:  # @line L3
        counts = _count_pairs(buf)  # @line L4
        if not counts:
            break
        (a, b), c = min(counts.items(), key=lambda kv: (-kv[1], kv[0]))  # @line L5
        if c < threshold:  # @line L6
            break
        code = unused.pop()  # @line L7
        out, i = [], 0
        while i < len(buf):  # @line L8
            if i + 1 < len(buf) and buf[i] == a and buf[i + 1] == b:
                out.append(code)
                i += 2
            else:
                out.append(buf[i])
                i += 1
        buf = out
        table.append((code, a, b))  # @line L9
    return table, buf  # @line L10


def expand_block(table: Sequence[tuple[int, int, int]], packed: Sequence[int]) -> bytes:
    """Undo compress_block with an explicit stack. Time O(output length)."""
    pairs = {code: (a, b) for code, a, b in table}
    out = bytearray()
    stack = list(reversed(packed))
    while stack:
        c = stack.pop()
        if c in pairs:
            a, b = pairs[c]
            stack.append(b)
            stack.append(a)
        else:
            out.append(c)
    return bytes(out)


def compress(data: bytes, block_size: int = 4096, threshold: int = 4) -> bytes:
    """Compress data block by block into this module's container format."""
    if block_size < 1:
        raise ValueError("block_size must be positive")
    out = bytearray()
    for start in range(0, len(data), block_size):
        table, packed = compress_block(data[start:start + block_size], threshold)
        out.append(len(table))
        for code, a, b in table:
            out += bytes((code, a, b))
        out += len(packed).to_bytes(4, "big")
        out += bytes(packed)
    return bytes(out)


def decompress(blob: bytes) -> bytes:
    """Read the container format written by compress."""
    out = bytearray()
    i = 0
    while i < len(blob):
        k = blob[i]
        i += 1
        table = [(blob[i + 3 * t], blob[i + 3 * t + 1], blob[i + 3 * t + 2]) for t in range(k)]
        i += 3 * k
        length = int.from_bytes(blob[i:i + 4], "big")
        i += 4
        if i + length > len(blob):
            raise ValueError("truncated block")
        out += expand_block(table, blob[i:i + length])
        i += length
    return bytes(out)


END = "</w>"


def learn_merges(word_counts: dict[str, int], num_merges: int) -> list[tuple[str, str]]:
    """Learn up to num_merges merges, as in Sennrich et al. (2016), Algorithm 1.

    Each word starts as its characters plus the end-of-word symbol END. A pair's count
    is the sum, over the words, of the word count times the number of adjacent
    positions that hold the pair. Ties go to the smallest pair. Learning stops early
    when no pair is left.
    """
    vocab = [(list(w) + [END], f) for w, f in word_counts.items() if f > 0]
    merges: list[tuple[str, str]] = []
    for _ in range(num_merges):
        stats: dict[tuple[str, str], int] = {}
        for symbols, f in vocab:
            for i in range(len(symbols) - 1):
                pair = (symbols[i], symbols[i + 1])
                stats[pair] = stats.get(pair, 0) + f
        if not stats:
            break
        best = min(stats, key=lambda p: (-stats[p], p))
        merges.append(best)
        vocab = [(_merge(symbols, best), f) for symbols, f in vocab]
    return merges


def _merge(symbols: list[str], pair: tuple[str, str]) -> list[str]:
    out, i = [], 0
    while i < len(symbols):
        if i + 1 < len(symbols) and symbols[i] == pair[0] and symbols[i + 1] == pair[1]:
            out.append(pair[0] + pair[1])
            i += 2
        else:
            out.append(symbols[i])
            i += 1
    return out


def segment(word: str, merges: Sequence[tuple[str, str]]) -> list[str]:
    """Split a word into subword units: apply each merge, in the order learned."""
    symbols = list(word) + [END]
    for pair in merges:
        if len(symbols) == 1:
            break
        symbols = _merge(symbols, pair)
    return symbols
