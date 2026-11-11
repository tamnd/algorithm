# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/oblivious-transfer-extension/. The authors are listed in prov/6D0YW3.jsonl.
"""IKNP oblivious transfer extension, semi-honest version.

Kappa base OTs (here a local ideal OT) with the roles reversed give the
sender a secret s and the receiver a matrix T such that each row satisfies
q_j = t_j xor r_j * s. Hashing the rows then gives m 1-out-of-2 OTs.

  G: SHA-256 in counter mode, stretching a 16-byte seed to m bits (the PRG);
  H: SHA-256 of (j, row), cut to the message length (the random oracle,
     or correlation-robust hash, of IKNP).

Bit strings of length m or kappa are Python ints. Bit j of a column is
(col >> j) & 1, and bit i of a row is (row >> i) & 1.

The module also has the cheating receiver that uses a different choice
vector in each column. That attack is why KOS adds a consistency check.

For study only. The code is not constant time, uses Python's random
module, and runs both parties in one process. Use a maintained library such
as libOTe or EMP-toolkit for real data.
"""

import hashlib
import random
from dataclasses import dataclass, field
from typing import Callable, Optional, Sequence

KAPPA = 128
SEED_BYTES = 16


def prg(seed: bytes, nbits: int) -> int:
    """G: stretch a seed to nbits pseudorandom bits with SHA-256 in counter mode."""
    out = bytearray()
    ctr = 0
    while 8 * len(out) < nbits:
        out += hashlib.sha256(seed + ctr.to_bytes(8, "big")).digest()
        ctr += 1
    return int.from_bytes(out, "little") & ((1 << nbits) - 1)


def hash_row(j: int, row: int, nbytes: int, kappa: int = KAPPA) -> bytes:
    """H(j, row): SHA-256 of the index and the row, cut to nbytes (at most 32)."""
    data = j.to_bytes(8, "big") + row.to_bytes((kappa + 7) // 8, "big")
    return hashlib.sha256(data).digest()[:nbytes]


def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))


def transpose(cols: Sequence[int], m: int) -> list[int]:
    """Columns (kappa ints of m bits) to rows (m ints of kappa bits)."""
    strs = [format(c, f"0{m}b")[::-1] for c in cols]          # strs[i][j] = bit j of column i
    return [int("".join(bits)[::-1], 2) for bits in zip(*strs)]


@dataclass
class Counters:
    base_ots: int = 0
    receiver_bits: int = 0       # bits the receiver sends in the extension (the u columns)
    sender_bytes: int = 0        # bytes the sender sends (the y pairs)
    hash_calls: int = 0


@dataclass
class Run:
    outputs: list[bytes]
    s: int                       # the sender's secret
    t_rows: list[int]            # the receiver's rows t_j
    q_rows: list[int]            # the sender's rows q_j
    y: list[tuple[bytes, bytes]]
    counters: Counters = field(default_factory=Counters)


def ideal_base_ot(m0: bytes, m1: bytes, b: int, ctr: Counters) -> bytes:
    """A local ideal 1-out-of-2 OT: the receiver gets m_b and nothing else."""
    ctr.base_ots += 1
    return m1 if b else m0


def iknp(pairs: Sequence[tuple[bytes, bytes]], r: Sequence[int], rng: random.Random,
         kappa: int = KAPPA,
         columns: Optional[Callable[[int], int]] = None) -> Run:
    """Run IKNP for the sender's pairs and the receiver's choice bits r.

    columns(i), if given, is the vector the receiver puts into column i in
    place of r: an honest receiver uses r for every column. A cheating
    receiver uses different vectors."""
    m = len(pairs)
    nbytes = len(pairs[0][0])
    ctr = Counters()
    rint = sum(bit << j for j, bit in enumerate(r))
    s = rng.getrandbits(kappa)  # @line L1
    seeds = [(rng.randbytes(SEED_BYTES), rng.randbytes(SEED_BYTES)) for _ in range(kappa)]  # @line L2
    t_cols, q_cols = [], []
    for i in range(kappa):
        si = (s >> i) & 1
        k = ideal_base_ot(seeds[i][0], seeds[i][1], si, ctr)  # @line L3
        ri = rint if columns is None else columns(i)
        t = prg(seeds[i][0], m)  # @line L4
        u = t ^ prg(seeds[i][1], m) ^ ri
        ctr.receiver_bits += m
        q = prg(k, m) ^ (u if si else 0)  # @line L5
        t_cols.append(t)
        q_cols.append(q)
    t_rows = transpose(t_cols, m)  # @line L6
    q_rows = transpose(q_cols, m)
    y = []
    for j, (x0, x1) in enumerate(pairs):
        y.append((xor_bytes(x0, hash_row(j, q_rows[j], nbytes, kappa)),  # @line L7
                  xor_bytes(x1, hash_row(j, q_rows[j] ^ s, nbytes, kappa))))
        ctr.sender_bytes += 2 * nbytes
        ctr.hash_calls += 2
    outputs = []
    for j in range(m):
        outputs.append(xor_bytes(y[j][r[j]], hash_row(j, t_rows[j], nbytes, kappa)))  # @line L8
        ctr.hash_calls += 1
    return Run(outputs, s, t_rows, q_rows, y, ctr)


# ---------------------------------------------------------------- the attack


def cheating_receiver_attack(pairs: Sequence[tuple[bytes, bytes]], known_x0: dict[int, bytes],
                             rng: random.Random, kappa: int = KAPPA) -> tuple[int, list[tuple[bytes, bytes]]]:
    """A receiver that breaks semi-honest IKNP by using non-constant rows.

    For probe transfers j = 0..kappa-1 the receiver puts the unit vector e_j
    in row j: bit j of column j is 1 and all other bits are 0. Then the
    sender's row is q_j = t_j xor s_j e_j, so the pad H(j, q_j) on x_j^0
    depends on the single bit s_j. The receiver knows x_j^0 for the probes
    (known_x0), so it tries both values of s_j and keeps the one that fits.
    The other rows use the choice bit 0 in every column. Once s is known,
    the receiver computes both pads H(j, t_j) and H(j, t_j xor s) of every
    other transfer, and so learns both messages.

    Returns the recovered s and the pairs the receiver learned for the
    transfers j >= kappa."""
    m = len(pairs)
    nbytes = len(pairs[0][0])

    def column(i: int) -> int:
        return 1 << i                       # row j has a 1 only in column j, for j < kappa

    run = iknp(pairs, [0] * m, rng, kappa, columns=column)
    s = 0
    for j in range(kappa):
        pad = xor_bytes(run.y[j][0], known_x0[j])
        if pad == hash_row(j, run.t_rows[j] ^ (1 << j), nbytes, kappa):
            s |= 1 << j
        else:
            assert pad == hash_row(j, run.t_rows[j], nbytes, kappa)
    learned = []
    for j in range(kappa, m):
        x0 = xor_bytes(run.y[j][0], hash_row(j, run.t_rows[j], nbytes, kappa))
        x1 = xor_bytes(run.y[j][1], hash_row(j, run.t_rows[j] ^ s, nbytes, kappa))
        learned.append((x0, x1))
    return s, learned
