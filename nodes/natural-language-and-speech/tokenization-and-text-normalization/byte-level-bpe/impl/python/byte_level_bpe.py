# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/byte-level-bpe/. The authors are listed in prov/HZ50C6.jsonl.

"""Byte-level byte-pair encoding, in the style of GPT-2.

The text is first split into pre-tokens by a scanner that follows the GPT-2
pattern (contractions, an optional space and a run of letters, of digits or
of other symbols, and runs of whitespace). Each pre-token becomes the list of
its UTF-8 bytes, and BPE merges are learned and applied on those bytes. Any
string has an encoding, so there is no unknown token.

recover is the dynamic program of Wang, Cho and Gu (2020) that keeps as many
characters as possible from a byte sequence that is not valid UTF-8.
"""

import unicodedata
from typing import Dict, List, Sequence, Tuple

Pair = Tuple[bytes, bytes]
CONTRACTIONS = ("'s", "'t", "'re", "'ve", "'m", "'ll", "'d")


def bytes_to_unicode() -> Dict[int, str]:
    """The GPT-2 map from the 256 byte values to printable characters."""
    keep = list(range(ord("!"), ord("~") + 1)) + list(range(ord("¡"), ord("¬") + 1)) + list(range(ord("®"), ord("ÿ") + 1))
    codes = keep[:]
    extra = 0
    for b in range(256):
        if b not in keep:
            keep.append(b)
            codes.append(256 + extra)
            extra += 1
    return {b: chr(c) for b, c in zip(keep, codes)}


BYTE_CHAR = bytes_to_unicode()


def show(token: bytes) -> str:
    """Print a token as GPT-2 does, for example b" world" as "Ġworld"."""
    return "".join(BYTE_CHAR[b] for b in token)


def _kind(ch: str) -> str:
    if ch.isspace():
        return "S"
    cat = unicodedata.category(ch)
    if cat[0] == "L":
        return "L"
    if cat[0] == "N":
        return "N"
    return "O"


def pretokenize(text: str) -> List[str]:
    """Split text like the GPT-2 pattern
    's|'t|'re|'ve|'m|'ll|'d| ?\\p{L}+| ?\\p{N}+| ?[^\\s\\p{L}\\p{N}]+|\\s+(?!\\S)|\\s+
    """
    out, i, n = [], 0, len(text)
    while i < n:
        hit = next((c for c in CONTRACTIONS if text.startswith(c, i)), None)
        if hit is not None:
            out.append(hit)
            i += len(hit)
            continue
        k = i + 1 if text[i] == " " and i + 1 < n else i
        kind = _kind(text[k])
        if kind != "S":
            j = k
            while j < n and _kind(text[j]) == kind:
                j += 1
            out.append(text[i:j])
            i = j
            continue
        j = i
        while j < n and text[j].isspace():
            j += 1
        if j < n and j - i >= 2:
            j -= 1  # leave the last space for the next word
        out.append(text[i:j])
        i = j
    return out


def _merge(units: Sequence[bytes], a: bytes, b: bytes) -> List[bytes]:
    out, i = [], 0
    while i < len(units):
        if i + 1 < len(units) and units[i] == a and units[i + 1] == b:
            out.append(a + b)
            i += 2
        else:
            out.append(units[i])
            i += 1
    return out


def _count_pair(units: Sequence[bytes], a: bytes, b: bytes) -> int:
    k, i = 0, 0
    while i + 1 < len(units):
        if units[i] == a and units[i + 1] == b:
            k += 1
            i += 2
        else:
            i += 1
    return k


def pair_counts(seg: Dict[str, List[bytes]], freq: Dict[str, int]) -> Dict[Pair, int]:
    """Non-overlapping occurrences of each adjacent pair, weighted by the counts."""
    pairs = set()
    for units in seg.values():
        pairs.update(zip(units, units[1:]))
    out = {}
    for a, b in pairs:
        k = sum(freq[x] * _count_pair(u, a, b) for x, u in seg.items())
        if k:
            out[(a, b)] = k
    return out


def train(texts: Sequence[str], merges: int) -> List[Pair]:
    """Learn up to `merges` byte-pair merges from a list of texts."""
    freq: Dict[str, int] = {}
    for text in texts:  # @line L1
        for x in pretokenize(text):
            freq[x] = freq.get(x, 0) + 1
    seg = {x: [bytes([b]) for b in x.encode("utf-8")] for x in freq}  # @line L2
    done: List[Pair] = []  # @line L3
    for _ in range(merges):  # @line L4
        p = pair_counts(seg, freq)  # @line L5
        if not p:  # @line L6
            break
        a, b = min(p, key=lambda pr: (-p[pr], pr))  # @line L7
        seg = {x: _merge(u, a, b) for x, u in seg.items()}  # @line L8
        done.append((a, b))  # @line L9
    return done  # @line L10


def encode(text: str, merges: Sequence[Pair]) -> List[bytes]:
    """Encode text into byte tokens by applying the merge of lowest rank first."""
    rank = {pr: r for r, pr in enumerate(merges)}  # @line E1
    out: List[bytes] = []  # @line E2
    for x in pretokenize(text):  # @line E3
        u = [bytes([b]) for b in x.encode("utf-8")]  # @line E4
        while any(pr in rank for pr in zip(u, u[1:])):  # @line E5
            a, b = min((pr for pr in zip(u, u[1:]) if pr in rank), key=rank.__getitem__)  # @line E6
            u = _merge(u, a, b)  # @line E7
        out.extend(u)  # @line E8
    return out  # @line E9


def replay(text: str, merges: Sequence[Pair]) -> List[bytes]:
    """Apply every merge in the order learned, to each pre-token."""
    out: List[bytes] = []
    for x in pretokenize(text):
        u = [bytes([b]) for b in x.encode("utf-8")]
        for a, b in merges:
            u = _merge(u, a, b)
        out.extend(u)
    return out


def token_ids(tokens: Sequence[bytes], merges: Sequence[Pair]) -> List[int]:
    """Byte b has id b, and the k-th merge (from 0) has id 256 + k."""
    ids = {bytes([b]): b for b in range(256)}
    for k, (a, b) in enumerate(merges):
        ids.setdefault(a + b, 256 + k)
    return [ids[t] for t in tokens]


def decode(tokens: Sequence[bytes]) -> str:
    """Join the bytes and decode them; bad UTF-8 becomes U+FFFD."""
    return b"".join(tokens).decode("utf-8", errors="replace")


def is_char(chunk: bytes) -> bool:
    """g(i, j) of Wang et al.: 1 if the bytes are one valid UTF-8 character."""
    try:
        return len(chunk.decode("utf-8")) == 1
    except UnicodeDecodeError:
        return False


def recover(data: bytes) -> Tuple[int, str]:
    """Keep the most characters from data; return (count, characters kept).

    The program works in the (max, +) semiring over chunks of 1 to 4 bytes.
    """
    n = len(data)
    f = [0] * (n + 1)  # @line R1
    back = [0] * (n + 1)
    for k in range(1, n + 1):  # @line R2
        best, arg = -1, 0
        for t in range(1, min(4, k) + 1):  # @line R3
            v = f[k - t] + is_char(data[k - t:k])
            if v > best:
                best, arg = v, t
        f[k], back[k] = best, arg  # @line R4
    kept, k = [], n  # @line R5
    while k > 0:
        t = back[k]
        if is_char(data[k - t:k]):
            kept.append(data[k - t:k].decode("utf-8"))
        k -= t
    return f[n], "".join(reversed(kept))
