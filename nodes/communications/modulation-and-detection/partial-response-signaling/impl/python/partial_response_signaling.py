# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/partial-response-signaling/. The authors are listed in prov/HBVC3V.jsonl.

"""Partial-response signaling at one sample per symbol: the precoder, the controlled ISI and
the symbol-by-symbol decoder.

The partial-response polynomial is a list f of integers with f[0] = 1, so that
c_k = sum_i f[i] a_(k-i). Digits b_k are in {0, ..., M - 1}; the levels are a = 2p - (M - 1).
The precoder and the channel both start from p_k = 0 for k <= 0.
"""


def precode(bits: list[int], f: list[int], m: int) -> list[int]:
    """p_k = (b_k - sum_(i >= 1) f[i] p_(k-i)) mod M, with p_k = 0 before the start."""
    if f[0] != 1:
        raise ValueError("f[0] must be 1")
    nu = len(f) - 1
    p = [0] * nu  # @line L1
    for b in bits:  # @line L2
        p.append((b - sum(f[i] * p[-i] for i in range(1, nu + 1))) % m)  # @line L3
    return p[nu:]


def levels(p: list[int], m: int) -> list[int]:
    """The M-PAM levels 2p - (M - 1)."""
    return [2 * v - (m - 1) for v in p]  # @line L4


def controlled_isi(a: list[int], f: list[int], a_start: int) -> list[int]:
    """c_k = sum_i f[i] a_(k-i), with a_k = a_start for k <= 0."""
    nu = len(f) - 1
    ext = [a_start] * nu + list(a)
    return [sum(f[i] * ext[k + nu - i] for i in range(nu + 1)) for k in range(len(a))]  # @line L5


def allowed_values(f: list[int], m: int) -> list[int]:
    """All values c_k can take."""
    vals = {0}
    for fi in f:
        vals = {v + fi * (2 * q - (m - 1)) for v in vals for q in range(m)}
    return sorted(vals)


def detect(y: float, allowed: list[int]) -> int:
    """The allowed value of c nearest to the sample y."""
    return min(allowed, key=lambda c: abs(y - c))  # @line L7


def decode(c_hat: int, f: list[int], m: int) -> int:
    """b_k = ((c_k + (M - 1) sum f) / 2) mod M, from one sample."""
    return ((c_hat + (m - 1) * sum(f)) // 2) % m  # @line L8


def link(bits: list[int], f: list[int], m: int, noise: list[float] | None = None) -> list[int]:
    """Precode, form c_k, add the noise samples w_k, and decode each sample alone."""
    a = levels(precode(bits, f, m), m)
    c = controlled_isi(a, f, -(m - 1))
    y = [ck + (noise[k] if noise else 0.0) for k, ck in enumerate(c)]  # @line L6
    allowed = allowed_values(f, m)
    return [decode(detect(v, allowed), f, m) for v in y]  # @line L9


def decode_without_precoder(c_hat: list[int], f: list[int], m: int) -> list[int]:
    """Without a precoder (a = 2b - (M - 1)), recover a_k = c_k - sum_(i >= 1) f[i] a_(k-i)
    from the earlier decisions. One wrong c_k can spread to later decisions."""
    nu = len(f) - 1
    a = [-(m - 1)] * nu
    out = []
    for c in c_hat:
        ak = c - sum(f[i] * a[-i] for i in range(1, nu + 1))
        a.append(ak)
        out.append(min(range(m), key=lambda q: abs(2 * q - (m - 1) - ak)))
    return out
