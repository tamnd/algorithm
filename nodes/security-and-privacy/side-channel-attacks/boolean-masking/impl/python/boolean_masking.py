# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boolean-masking/. The authors are listed in prov/H7YXSN.jsonl.
"""First-order Boolean masking of a 4-bit S-box lookup by table recomputation.

The S-box is the 4-bit PRESENT S-box (Bogdanov et al., CHES 2007). Each
function returns, next to its result, the list of every intermediate
value it computes, so that a test can check the probing model by
exhaustive enumeration of the masks. This is a model of a computation, not
of a device: the masks come from a seeded ``random.Random`` or from the
caller.
"""

import random

PRESENT_SBOX: tuple[int, ...] = (
    0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD,
    0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2,
)

Wire = tuple[str, int]


def masked_sbox_wires(
    p: int, k: int, m_in: int, m_out: int, sbox: tuple[int, ...] = PRESENT_SBOX
) -> tuple[tuple[int, int], list[Wire]]:
    """Compute the shares (S(p xor k) xor m_out, m_out) with masks m_in and m_out.

    Precondition: sbox is a table of 2^w entries and p, k, m_in, m_out are
    w-bit values. Returns the two output shares and every intermediate wire.
    Cost: Theta(2^w) for the table and Theta(1) for the lookup.
    """
    wires: list[Wire] = [("m_in", m_in), ("m_out", m_out)]  # @line L1
    a = p ^ m_in  # @line L2
    wires.append(("p+m_in", a))
    x_masked = a ^ k  # @line L3
    wires.append(("x'", x_masked))
    table = [0] * len(sbox)
    for u in range(len(sbox)):  # @line L4
        table[u] = sbox[u ^ m_in] ^ m_out
        wires.append((f"T[{u}]", table[u]))
    y_masked = table[x_masked]  # @line L5
    wires.append(("y'", y_masked))
    return (y_masked, m_out), wires  # @line L6


def wrong_order_wires(
    p: int, k: int, m_in: int, m_out: int, sbox: tuple[int, ...] = PRESENT_SBOX
) -> tuple[tuple[int, int], list[Wire]]:
    """The same computation with the key added before the mask (a pitfall).

    The wire p xor k is not masked, so one probe gives the key.
    """
    wires: list[Wire] = [("m_in", m_in), ("m_out", m_out)]
    a = p ^ k
    wires.append(("p+k", a))
    x_masked = a ^ m_in
    wires.append(("x'", x_masked))
    table = [sbox[u ^ m_in] ^ m_out for u in range(len(sbox))]
    wires += [(f"T[{u}]", table[u]) for u in range(len(sbox))]
    y_masked = table[x_masked]
    wires.append(("y'", y_masked))
    return (y_masked, m_out), wires


def masked_sbox(rng: random.Random, p: int, k: int, sbox: tuple[int, ...] = PRESENT_SBOX) -> tuple[int, int]:
    """Masked lookup with fresh uniform masks. Returns (y', m_out) with y' xor m_out = S(p xor k)."""
    m_in = rng.randrange(len(sbox))
    m_out = rng.randrange(len(sbox))
    return masked_sbox_wires(p, k, m_in, m_out, sbox)[0]


def gf2_linear(rows: tuple[int, ...], v: int) -> int:
    """Apply the GF(2)-linear map whose output bit i is the parity of v AND rows[i]."""
    out = 0
    for i, r in enumerate(rows):
        out |= (bin(v & r).count("1") & 1) << i
    return out


def three_share_linear_wires(
    p: int, k_shares: tuple[int, int, int], rows: tuple[int, ...]
) -> tuple[list[int], list[Wire]]:
    """Second-order masking of y = L(p xor k) with k in three shares.

    The public p is added to the first share only; the linear map L is
    applied to each share. Returns the output shares and every wire.
    Cost: Theta(1) for each share.
    """
    k1, k2, k3 = k_shares
    wires: list[Wire] = [("k1", k1), ("k2", k2), ("k3", k3)]
    x = [k1 ^ p, k2, k3]
    wires.append(("x1", x[0]))
    y = [gf2_linear(rows, v) for v in x]
    wires += [("y1", y[0]), ("y2", y[1]), ("y3", y[2])]
    return y, wires
