# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rapt-pitch-tracker/. The authors are listed in prov/D01A4J.jsonl.

"""RAPT, the robust algorithm for pitch tracking of Talkin (1995), in one pass.

Per frame: the normalized cross-correlation function (NCCF) over the lags of the
pitch range, its local maxima above CAND_TR times the largest value as voiced
candidates, and one unvoiced candidate. Over frames: a dynamic program with the
local costs and transition costs of Talkin, section 3.5, picks the path of least
total cost. The paper first finds peaks on a downsampled signal and then refines
them at the full rate; this code computes the NCCF at the full rate directly,
which gives the same kind of candidates at a higher cost.

Costs (Talkin's names):
  voiced local cost     1 - C (1 - LAG_WT L / L_max)
  unvoiced local cost   VO_BIAS + the largest candidate C of the frame
  voiced to voiced      FREQ_WT min(xi, DOUBL_C + |xi - ln 2|), xi = |ln(L_j / L_k)|
  unvoiced to voiced    VTRAN_C + VTR_S_C S + VTR_A_C / rr
  voiced to unvoiced    VTRAN_C + VTR_S_C S + VTR_A_C rr
  unvoiced to unvoiced  0
where rr is the RMS ratio of the frame to the previous frame and S = 0.2 / (I - 0.8)
with I the Itakura ratio of the LPC spectra of the two frames.
"""

import math
from typing import Callable, List, Optional, Sequence, Tuple

from nlsdsp import autocorr, hamming, levinson

PARAMS = {
    "f0_min": 50.0,
    "f0_max": 500.0,
    "frame_step": 0.01,
    "wind_dur": 0.0075,
    "cand_tr": 0.3,
    "lag_wt": 0.3,
    "freq_wt": 0.02,
    "vtran_c": 0.005,
    "vtr_a_c": 0.5,
    "vtr_s_c": 0.5,
    "vo_bias": 0.0,
    "doubl_c": 0.35,
    "n_cands": 20,
}

Candidate = Tuple[float, float]  # (lag in samples, correlation); lag 0 means unvoiced


def nccf(x: Sequence[float], m: int, n: int, k_lo: int, k_hi: int, eps: float = 0.0) -> List[float]:
    """phi(k) = sum_{j=m}^{m+n-1} x_j x_{j+k} / sqrt(e_m e_{m+k} + eps) for k = k_lo .. k_hi.

    Here e_j = sum_{l=j}^{j+n-1} x_l^2. The value is 0 when the denominator is 0.
    Needs m + k_hi + n <= len(x).
    """
    if m < 0 or k_lo < 0 or m + k_hi + n > len(x):
        raise ValueError("the signal is too short for this frame and lag range")
    e_m = sum(x[m + l] ** 2 for l in range(n))
    e_k = sum(x[m + k_lo + l] ** 2 for l in range(n))
    out = []
    for k in range(k_lo, k_hi + 1):
        if k > k_lo:  # slide the energy window by one sample
            e_k += x[m + k + n - 1] ** 2 - x[m + k - 1] ** 2
            e_k = max(e_k, 0.0)
        num = sum(x[m + j] * x[m + j + k] for j in range(n))
        den = math.sqrt(e_m * e_k + eps)
        out.append(num / den if den > 0 else 0.0)
    return out


def peaks(phi: Sequence[float], k_lo: int, k_min: int, k_max: int, cand_tr: float, n_max: int) -> List[Candidate]:
    """Voiced candidates: interpolated local maxima of phi in [k_min, k_max] with value >= cand_tr * the largest.

    phi[i] is the value at lag k_lo + i, and must cover k_min - 1 .. k_max + 1.
    At most n_max candidates are kept, the largest first; ties go to the shorter lag.
    """
    at = lambda k: phi[k - k_lo]
    top = max(at(k) for k in range(k_min, k_max + 1))
    if top <= 0:
        return []
    found = []
    for k in range(k_min, k_max + 1):
        if at(k) >= at(k - 1) and at(k) > at(k + 1) and at(k) >= cand_tr * top:
            a = at(k - 1) - 2 * at(k) + at(k + 1)
            off = (at(k - 1) - at(k + 1)) / (2 * a) if a < 0 else 0.0
            value = at(k) - 0.25 * (at(k - 1) - at(k + 1)) * off
            found.append((k + off, min(value, 1.0)))
    found.sort(key=lambda c: (-c[1], c[0]))
    return found[:n_max]


def itakura_ratio(seg_ref: Sequence[float], seg_other: Sequence[float], order: int) -> float:
    """I = a_o' R a_o / a_r' R a_r, with R the autocorrelation matrix of seg_ref and a_r, a_o the LPC inverse filters.

    The LPC of seg_ref minimizes the quadratic form, so I >= 1. A silent segment gives 1.
    """
    w = hamming(len(seg_ref))
    r = autocorr([v * u for v, u in zip(seg_ref, w)], order)
    r2 = autocorr([v * u for v, u in zip(seg_other, w)], order)
    if r[0] <= 1e-12 or r2[0] <= 1e-12:
        return 1.0
    a_ref = [1.0] + [-c for c in levinson(r, order)[0]]
    a_oth = [1.0] + [-c for c in levinson(r2, order)[0]]

    def form(a):
        return sum(a[j] * a[k] * r[abs(j - k)] for j in range(order + 1) for k in range(order + 1))

    base = form(a_ref)
    return form(a_oth) / base if base > 0 else 1.0


def rms(seg: Sequence[float]) -> float:
    return math.sqrt(sum(v * v for v in seg) / len(seg))


def transition_cost(
    prev: Candidate, cur: Candidate, rr: float, s: float, p: dict = PARAMS
) -> float:
    """The cost of moving from candidate prev of frame i - 1 to candidate cur of frame i."""
    pv, cv = prev[0] > 0, cur[0] > 0
    if pv and cv:
        xi = abs(math.log(cur[0] / prev[0]))
        return p["freq_wt"] * min(xi, p["doubl_c"] + abs(xi - math.log(2.0)))
    if not pv and not cv:
        return 0.0
    if cv:  # onset
        return p["vtran_c"] + p["vtr_s_c"] * s + p["vtr_a_c"] / rr
    return p["vtran_c"] + p["vtr_s_c"] * s + p["vtr_a_c"] * rr  # offset


def dp(local: Sequence[Sequence[float]], trans: Callable[[int, int, int], float]) -> Tuple[List[int], float]:
    """The path of least total cost: D_1 = d_1, D_i(j) = d_i(j) + min_k D_{i-1}(k) + trans(i, k, j).

    local[i][j] is the local cost of state j in frame i, trans(i, k, j) the cost of
    moving from state k of frame i - 1 to state j of frame i. Ties go to the
    smallest state. Returns the states, one per frame, and the total cost.
    """
    if not local:
        return [], 0.0
    cost = list(local[0])  # @line L5
    back: List[List[int]] = []
    for i in range(1, len(local)):  # @line L6
        new, ptr = [], []
        for j, d in enumerate(local[i]):
            best_k = min(range(len(cost)), key=lambda k: (cost[k] + trans(i, k, j), k))
            new.append(d + cost[best_k] + trans(i, best_k, j))  # @line L7
            ptr.append(best_k)
        cost = new
        back.append(ptr)
    last = min(range(len(cost)), key=lambda j: (cost[j], j))  # @line L8
    path = [last]
    for ptr in reversed(back):  # @line L9
        path.append(ptr[path[-1]])
    path.reverse()
    return path, cost[last]


def frame_states(
    x: Sequence[float], fs: float, p: dict = PARAMS, lpc_order: int = 8
) -> Tuple[List[List[Candidate]], List[List[float]], List[float], List[float]]:
    """Candidates (voiced ones, then (0, 0) for unvoiced), local costs, rr and S of every frame."""
    hop = round(p["frame_step"] * fs)
    n = round(p["wind_dur"] * fs)
    k_min = max(2, math.floor(fs / p["f0_max"]))
    k_max = math.ceil(fs / p["f0_min"])
    span = k_max + 1 + n
    beta = p["lag_wt"] / k_max
    cands, local, rrs, ss = [], [], [], []
    prev_seg = None
    m = 0
    while m + span <= len(x):
        phi = nccf(x, m, n, k_min - 1, k_max + 1)  # @line L1
        voiced = peaks(phi, k_min - 1, k_min, k_max, p["cand_tr"], p["n_cands"] - 1)  # @line L2
        c_max = max((c for _, c in voiced), default=0.0)
        costs = [1.0 - c * (1.0 - beta * lag) for lag, c in voiced]  # @line L3
        costs.append(p["vo_bias"] + c_max)
        seg = x[m : m + span]
        if prev_seg is None:
            rr, s = 1.0, 1.0
        else:
            rr = (rms(seg) + 1e-9) / (rms(prev_seg) + 1e-9)  # @line L4
            s = 0.2 / (itakura_ratio(seg, prev_seg, lpc_order) - 0.8)
        cands.append(voiced + [(0.0, 0.0)])
        local.append(costs)
        rrs.append(rr)
        ss.append(s)
        prev_seg = seg
        m += hop
    return cands, local, rrs, ss


def rapt(x: Sequence[float], fs: float, p: dict = PARAMS) -> List[Optional[float]]:
    """The RAPT track: fs / L for each voiced frame, None for each unvoiced frame. Frames start every frame_step seconds."""
    cands, local, rrs, ss = frame_states(x, fs, p)

    def trans(i, k, j):
        return transition_cost(cands[i - 1][k], cands[i][j], rrs[i], ss[i], p)

    path, _ = dp(local, trans)
    out = []
    for i, j in enumerate(path):
        lag = cands[i][j][0]
        out.append(fs / lag if lag > 0 else None)  # @line L10
    return out
