# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/d-blast/. The authors are listed in prov/YCBK18.jsonl.

"""D-BLAST: diagonal layering with a nulling and cancelling receiver.

The transmitter has n antennas and sends L layers. Each layer is cut into n
blocks of the same length. Block k of layer l goes out on antenna k at block
time l + k, so a frame has L + n - 1 block times, and at block time t the
antenna k carries layer t - k when 0 <= t - k < L and is silent otherwise.
The channel H (m by n) stays the same for the whole frame (slow fading).

The receiver decodes the layers in the order 0, 1, ..., L - 1. For block k
of layer l at time t = l + k, the antennas k' > k carry earlier layers,
which are already decided, so the receiver subtracts them. The active
antennas k' < k carry later layers, so the receiver nulls them with the ZF
(a = 0) or MMSE (a = N0 / Es) filter. It then decodes the layer from the n
filter outputs. Two layer decoders are given: slicing each symbol alone
(no code) and a repetition code, where the same symbols fill all n blocks
and the receiver adds the n outputs with weights that maximize the SNR.
"""

import cbb


def nearest(z: complex, points: list[complex]) -> int:
    """The index of the point nearest to z (the lowest index on a tie)."""
    best, arg = float("inf"), -1
    for i, p in enumerate(points):
        d = abs(z - p) ** 2
        if d < best:
            best, arg = d, i
    return arg


def layer_map(n: int, layers: int) -> list[list[int]]:
    """grid[t][k] is the layer on antenna k at block time t, or -1 if the antenna is silent."""
    return [[t - k if 0 <= t - k < layers else -1 for k in range(n)] for t in range(layers + n - 1)]


def rate_fraction(n: int, layers: int) -> float:
    """The fraction L / (L + n - 1) of the V-BLAST rate that the frame carries."""
    return layers / (layers + n - 1)


def dblast_transmit(blocks: list[list[list[complex]]], n: int) -> list[list[complex]]:
    """The transmitted vectors of a frame. blocks[l][k] is the list of symbols of block k of layer l."""
    layers = len(blocks)
    blen = len(blocks[0][0])
    out = []
    for t, row in enumerate(layer_map(n, layers)):
        for s in range(blen):
            out.append([blocks[row[k]][k][s] if row[k] >= 0 else 0j for k in range(n)])
    return out


def _filter(h: list[list[complex]], k: int, t: int, layers: int, a: float) -> tuple[list[complex], float]:
    """The nulling row for antenna k at block time t and the entry P_kk."""
    cols = [c for c in range(k) if t - c < layers] + [k]  # @line L5
    hk = [[row[c] for c in cols] for row in h]
    hh = cbb.herm(hk)
    g = cbb.matmul(hh, hk)
    for i in range(len(cols)):
        g[i][i] += a
    try:
        p = cbb.inv(g)  # @line L6
    except ValueError:
        raise ValueError("ZF nulling needs independent columns; use MMSE nulling") from None
    i = len(cols) - 1
    pkk = p[i][i].real
    w = [sum(p[i][c] * hh[c][j] for c in range(len(cols))) for j in range(len(h))]
    if a > 0:
        w = [v / (1.0 - a * pkk) for v in w]  # remove the MMSE bias
    return w, pkk


def block_sinrs(h: list[list[complex]], layers: int, es: float, n0: float, mmse: bool = True) -> list[list[float]]:
    """sinr[l][k], the SNR (ZF) or unbiased SINR (MMSE) of block k of layer l, assuming correct cancellation."""
    n = len(h[0])
    a = n0 / es
    out = []
    for l in range(layers):
        row = []
        for k in range(n):
            _, pkk = _filter(h, k, l + k, layers, a if mmse else 0.0)
            row.append(1.0 / (a * pkk) - 1.0 if mmse else (es / n0) / pkk)
        out.append(row)
    return out


def dblast_detect(
    ys: list[list[complex]],
    h: list[list[complex]],
    points: list[complex],
    layers: int,
    n0: float = 0.0,
    es: float = 1.0,
    mmse: bool = False,
    repeat: bool = False,
) -> list:
    """The decisions of every layer.

    ys holds the received vectors of the frame, (L + n - 1) * blen of them.
    Without repeat, the result is out[l][k][s], the point index of symbol s
    of block k of layer l. With repeat, every layer carries one list of blen
    symbols, repeated in all n blocks, and the result is out[l][s].
    """
    n = len(h[0])
    if mmse and n0 <= 0:
        raise ValueError("MMSE nulling needs N0 > 0")
    if len(ys) % (layers + n - 1):
        raise ValueError("the frame length must be a multiple of L + n - 1")
    blen = len(ys) // (layers + n - 1)
    a = n0 / es if mmse else 0.0
    dec = [[[0j] * blen for _ in range(n)] for _ in range(layers)]  # decided symbols
    out = []
    for l in range(layers):  # @line L1
        zs, wts = [], []
        for k in range(n):  # @line L2
            t = l + k  # @line L3
            w, pkk = _filter(h, k, t, layers, a)
            wts.append(1.0 / (a * pkk) - 1.0 if mmse else 1.0 / pkk)  # @line L7
            zk = []
            for s in range(blen):
                r = list(ys[t * blen + s])
                for c in range(k + 1, n):  # @line L4
                    if t - c >= 0:
                        x = dec[t - c][c][s]
                        r = [rv - row[c] * x for rv, row in zip(r, h)]
                zk.append(sum(c * v for c, v in zip(w, r)))
            zs.append(zk)
        if repeat:  # @line L8
            tot = sum(wts)
            idx = [nearest(sum(wt * z[s] for wt, z in zip(wts, zs)) / tot, points) for s in range(blen)]
            for k in range(n):
                dec[l][k] = [points[i] for i in idx]
            out.append(idx)
        else:
            idx = [[nearest(z, points) for z in zk] for zk in zs]
            for k in range(n):
                dec[l][k] = [points[i] for i in idx[k]]
            out.append(idx)
    return out  # @line L9
