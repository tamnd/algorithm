# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/delta-encoding/. The authors are listed in prov/MHQMGE.jsonl.

"""Delta encoding of number sequences, the codes that usually follow it, and
a small delta encoder for byte strings.

delta_encode stores X[0] and then each X[i] - X[i-1]; delta_decode takes
prefix sums. Both take O(n) time. delta_encode(x, order=k) applies the step
k times.

zigzag maps signed integers to unsigned ones (0, -1, 1, -2, ... to 0, 1, 2, 3,
...), and varint writes an unsigned integer in groups of 7 bits, low group
first, with the high bit set on every byte but the last (LEB128, as in
Protocol Buffers).

copy_add_encode and copy_add_decode are a delta between two byte strings in
the style of VCDIFF (RFC 3284, Section 3): the target T is a list of ADD
(literal bytes), COPY (size, address in S followed by T) and RUN (size, byte)
instructions. The address space U = S + T lets a COPY take bytes from the
part of T made so far, and a COPY may overlap the bytes it produces. This is
not the byte format of RFC 3284.
"""

from collections.abc import Sequence


def delta_encode(x: Sequence[int], order: int = 1) -> list[int]:
    """X[0], X[1] - X[0], X[2] - X[1], ...; repeated order times."""
    d = list(x)
    for _ in range(order):
        prev = 0  # @line L1
        for i in range(len(d)):  # @line L2
            cur = d[i]
            d[i] = cur - prev  # @line L3
            prev = cur  # @line L4
    return d  # @line L5


def delta_decode(d: Sequence[int], order: int = 1) -> list[int]:
    """Inverse of delta_encode: prefix sums, repeated order times."""
    x = list(d)
    for _ in range(order):
        total = 0
        for i in range(len(x)):
            total += x[i]
            x[i] = total
    return x


def zigzag_encode(v: int) -> int:
    """0, -1, 1, -2, 2, ... to 0, 1, 2, 3, 4, ...; for any Python int."""
    return 2 * v if v >= 0 else -2 * v - 1


def zigzag_decode(u: int) -> int:
    if u < 0:
        raise ValueError("u must be at least 0")
    return u >> 1 if u % 2 == 0 else -((u + 1) >> 1)


def varint_encode(u: int) -> bytes:
    """Unsigned LEB128: 7 bits per byte, low group first, high bit = more bytes."""
    if u < 0:
        raise ValueError("u must be at least 0")
    out = bytearray()
    while True:
        b = u & 0x7F
        u >>= 7
        if u:
            out.append(b | 0x80)
        else:
            out.append(b)
            return bytes(out)


def varint_decode_all(data: bytes) -> list[int]:
    out, cur, shift = [], 0, 0
    for b in data:
        cur |= (b & 0x7F) << shift
        shift += 7
        if not b & 0x80:
            out.append(cur)
            cur, shift = 0, 0
    if shift:
        raise ValueError("the last varint is not complete")
    return out


def encode_int_sequence(x: Sequence[int]) -> bytes:
    """Delta, then zigzag, then varint: a common way to store a slowly
    changing sequence of integers."""
    return b"".join(varint_encode(zigzag_encode(v)) for v in delta_encode(x))


def decode_int_sequence(data: bytes) -> list[int]:
    return delta_decode([zigzag_decode(u) for u in varint_decode_all(data)])


def d_gaps(postings: Sequence[int]) -> list[int]:
    """The gaps of a strictly increasing list of document numbers."""
    if any(b <= a for a, b in zip(postings, postings[1:])):
        raise ValueError("the list must be strictly increasing")
    return delta_encode(postings)


# A delta between two byte strings: ADD, COPY and RUN instructions.

Instruction = tuple  # ("ADD", bytes) | ("COPY", size, addr) | ("RUN", size, byte)


def copy_add_encode(source: bytes, target: bytes, block: int = 4) -> list[Instruction]:
    """Greedy: at each position of T, take the longest match that starts at an
    indexed block of U = S + T before this position, if it has at least
    `block` bytes; else a RUN of at least `block` equal bytes; else one literal
    byte. Blocks of T are indexed as the position passes them."""
    u = source + target
    s = len(source)
    index: dict[bytes, list[int]] = {}
    for a in range(0, s - block + 1):
        index.setdefault(u[a : a + block], []).append(a)
    out: list[Instruction] = []
    lit = bytearray()
    next_t = s  # the next start in T to put in the index

    def flush() -> None:
        if lit:
            out.append(("ADD", bytes(lit)))
            lit.clear()

    p = s
    while p < len(u):
        while next_t + block <= p:
            index.setdefault(u[next_t : next_t + block], []).append(next_t)
            next_t += 1
        best_len, best_addr = 0, -1
        for a in index.get(u[p : p + block], [])[-32:]:
            k = 0
            # A copy from S stays inside S; a copy from T may overlap its output.
            limit = s - a if a < s else len(u) - p
            while k < limit and p + k < len(u) and u[a + k] == u[p + k]:
                k += 1
            if k > best_len:
                best_len, best_addr = k, a
        run = 1
        while p + run < len(u) and u[p + run] == u[p]:
            run += 1
        if best_len >= block and best_len >= run:
            flush()
            out.append(("COPY", best_len, best_addr))
            p += best_len
        elif run >= block:
            flush()
            out.append(("RUN", run, u[p]))
            p += run
        else:
            lit.append(u[p])
            p += 1
    flush()
    return out


def copy_add_decode(source: bytes, instructions: Sequence[Instruction]) -> bytes:
    """Rebuild T. A COPY reads U one byte at a time, so it may overlap the
    bytes it writes."""
    u = bytearray(source)
    for ins in instructions:
        if ins[0] == "ADD":
            u += ins[1]
        elif ins[0] == "RUN":
            u += bytes((ins[2],)) * ins[1]
        elif ins[0] == "COPY":
            size, addr = ins[1], ins[2]
            if not 0 <= addr < len(u):
                raise ValueError("COPY address is not in the data made so far")
            for k in range(size):
                u.append(u[addr + k])
        else:
            raise ValueError("unknown instruction")
    return bytes(u[len(source) :])
