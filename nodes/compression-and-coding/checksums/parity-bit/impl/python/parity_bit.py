# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parity-bit/. The authors are listed in prov/XJCSTS.jsonl.

"""Parity bits: the single parity check, two-dimensional parity with
single-error correction, and XOR parity over blocks as in RAID 4 and 5."""


def even_parity(word: int) -> int:
    """The bit that makes the number of 1 bits even: the XOR of all bits."""
    return word.bit_count() & 1


def odd_parity(word: int) -> int:
    """The bit that makes the number of 1 bits odd."""
    return even_parity(word) ^ 1


def add_parity_7bit(ch: int, odd: bool = False) -> int:
    """A 7-bit character with its parity bit in bit 7."""
    p = odd_parity(ch) if odd else even_parity(ch)
    return ch | (p << 7)


def check_8bit(byte: int, odd: bool = False) -> bool:
    """True when the 8-bit frame has the right parity."""
    return byte.bit_count() % 2 == (1 if odd else 0)


# Two-dimensional parity. A block is a list of rows, each a list of bits.

def encode_2d(block: list[list[int]]) -> list[list[int]]:
    """Append a parity bit to each row, then a row of column parities. The
    corner bit is the parity of the parity row, which equals the parity of
    the parity column."""
    rows = [row + [sum(row) % 2] for row in block]
    rows.append([sum(col) % 2 for col in zip(*rows)])
    return rows


def syndromes_2d(word: list[list[int]]) -> tuple[list[int], list[int]]:
    bad_rows = [i for i, row in enumerate(word) if sum(row) % 2]
    bad_cols = [j for j, col in enumerate(zip(*word)) if sum(col) % 2]
    return bad_rows, bad_cols


def decode_2d(word: list[list[int]]) -> tuple[str, list[list[int]]]:
    """Return ("ok", word), ("corrected", fixed word) or ("error", word).
    One bad row and one bad column locate a single error, which is flipped.
    Any other nonzero syndrome is reported as an uncorrectable error."""
    bad_rows, bad_cols = syndromes_2d(word)
    if not bad_rows and not bad_cols:
        return "ok", word
    if len(bad_rows) == 1 and len(bad_cols) == 1:
        fixed = [row[:] for row in word]
        fixed[bad_rows[0]][bad_cols[0]] ^= 1
        return "corrected", fixed
    return "error", word


# XOR parity over blocks, as in RAID 4 and RAID 5.

def parity_block(blocks: list[bytes]) -> bytes:
    out = bytearray(len(blocks[0]))
    for b in blocks:
        for i, x in enumerate(b):
            out[i] ^= x
    return bytes(out)


def rebuild(blocks: list[bytes | None], parity: bytes) -> list[bytes]:
    """Rebuild the one missing data block (marked None): it is the XOR of
    the parity block and all the other data blocks."""
    missing = [i for i, b in enumerate(blocks) if b is None]
    assert len(missing) == 1, "XOR parity can rebuild only one lost block"
    present = [b for b in blocks if b is not None]
    out = list(blocks)
    out[missing[0]] = parity_block([parity, *present])
    return out  # type: ignore[return-value]
