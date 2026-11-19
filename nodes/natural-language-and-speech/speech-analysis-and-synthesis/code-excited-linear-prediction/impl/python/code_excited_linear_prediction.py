# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/code-excited-linear-prediction/. The authors are listed in prov/X96A2P.jsonl.

"""Code-excited linear prediction (CELP): an analysis-by-synthesis speech coder.

Per frame, an LPC polynomial A(z) = 1 - sum a_k z^-k models the spectral envelope.
Per subframe, the excitation is g_a v_T + g_f c_k: v_T is the past excitation
delayed by the lag T (the adaptive codebook, for the pitch), c_k is entry k of a
fixed codebook of random vectors. The encoder picks T, k and the gains that
minimize the energy of the weighted error W(z) (s - s_hat), with
W(z) = A(z / gamma1) / A(z / gamma2), where s_hat is the excitation through 1 / A(z).

The weighted error of a subframe is affine in the excitation e:
    ew(e) = t - H e,
where t is the weighted error with e = 0 (the filters run on from their states)
and H is the zero-state response of W(z) / A(z). For a single vector y = H c the
best gain is g = <t, y> / <y, y>, and the error falls by <t, y>^2 / <y, y>, so the
search picks the c with the largest such score. The two codebooks are searched
one after the other, which is the usual suboptimal but fast order.

This code does not quantize the LPC coefficients or the gains; a real coder does,
and its bit rate depends on that.
"""

import math
import random
from typing import Dict, List, Optional, Sequence, Tuple

from nlsdsp import autocorr, hamming, levinson


def bandwidth_expand(a: Sequence[float], gamma: float) -> List[float]:
    """The coefficients of A(z / gamma): a_k gamma^k."""
    return [c * gamma ** (k + 1) for k, c in enumerate(a)]


def lpc(frame: Sequence[float], order: int) -> List[float]:
    """LPC by the autocorrelation method on a Hamming window; zeros for a silent frame."""
    w = hamming(len(frame))
    r = autocorr([x * v for x, v in zip(frame, w)], order)
    if r[0] <= 1e-12:
        return [0.0] * order
    r = [r[0] * (1 + 1e-9)] + r[1:]  # a tiny white noise floor keeps A(z) well conditioned
    return levinson(r, order)[0]


class Filters:
    """The states of the synthesis filter 1 / A(z) and of the weighting filter W(z) on the error s - s_hat."""

    def __init__(self, order: int) -> None:
        self.syn = [0.0] * order  # past s_hat, newest first
        self.err_in = [0.0] * order  # past s - s_hat, newest first
        self.err_out = [0.0] * order  # past weighted error, newest first

    def copy(self) -> "Filters":
        f = Filters(0)
        f.syn, f.err_in, f.err_out = self.syn[:], self.err_in[:], self.err_out[:]
        return f

    def run(
        self, s: Sequence[float], e: Sequence[float], a: Sequence[float], w1: Sequence[float], w2: Sequence[float]
    ) -> Tuple[List[float], List[float]]:
        """Advance over one subframe of speech s and excitation e. Returns (s_hat, weighted error)."""
        s_hat, ew = [], []
        for x, u in zip(s, e):
            y = u + sum(c * m for c, m in zip(a, self.syn))
            self.syn = [y] + self.syn[:-1]
            d = x - y
            v = d - sum(c * m for c, m in zip(w1, self.err_in)) + sum(c * m for c, m in zip(w2, self.err_out))
            self.err_in = [d] + self.err_in[:-1]
            self.err_out = [v] + self.err_out[:-1]
            s_hat.append(y)
            ew.append(v)
        return s_hat, ew


def impulse_response(a: Sequence[float], w1: Sequence[float], w2: Sequence[float], n: int) -> List[float]:
    """The first n samples of the zero-state impulse response of W(z) / A(z)."""
    f = Filters(len(a))
    # the weighted error of s = 0 and e = delta is minus the response of W / A
    _, ew = f.run([0.0] * n, [1.0] + [0.0] * (n - 1), a, w1, w2)
    return [-v for v in ew]


def convolve(h: Sequence[float], c: Sequence[float]) -> List[float]:
    """y[n] = sum_{j <= n} h[n - j] c[j] for n < len(c): zero-state filtering truncated to the subframe."""
    return [sum(h[n - j] * c[j] for j in range(n + 1)) for n in range(len(c))]


def dot(x: Sequence[float], y: Sequence[float]) -> float:
    return sum(u * v for u, v in zip(x, y))


def search(target: Sequence[float], filtered: Sequence[Sequence[float]]) -> Tuple[int, float, float]:
    """The index of the best vector, its gain and the remaining error energy.

    The best vector maximizes <t, y>^2 / <y, y>; ties go to the smallest index.
    """
    best, best_score, best_gain = -1, -1.0, 0.0
    for k, y in enumerate(filtered):
        energy = dot(y, y)
        if energy <= 0:
            continue
        corr = dot(target, y)
        score = corr * corr / energy
        if score > best_score:
            best, best_score, best_gain = k, score, corr / energy
    if best < 0:
        return 0, 0.0, dot(target, target)
    return best, best_gain, dot(target, target) - best_score


def adaptive_vector(past: Sequence[float], lag: int, n: int) -> List[float]:
    """v[i] = past[-lag + i] for i < lag, then repeated with period lag: the past excitation delayed by lag."""
    v = []
    for i in range(n):
        v.append(past[len(past) - lag + i] if i < lag else v[i - lag])
    return v


def random_codebook(size: int, n: int, seed: int = 1) -> List[List[float]]:
    """A Gaussian codebook as in Schroeder and Atal, each vector scaled to unit energy."""
    rng = random.Random(seed)
    book = []
    for _ in range(size):
        v = [rng.gauss(0.0, 1.0) for _ in range(n)]
        z = math.sqrt(dot(v, v))
        book.append([x / z for x in v])
    return book


def encode(
    s: Sequence[float],
    codebook: Sequence[Sequence[float]],
    order: int = 10,
    frame_len: int = 160,
    sub_len: int = 40,
    lags: Optional[range] = range(20, 148),
    gamma1: float = 0.9,
    gamma2: float = 0.6,
    lpc_given: Optional[Sequence[Sequence[float]]] = None,
) -> Tuple[List[Dict], List[float]]:
    """Encode s. Returns the parameters of every subframe and the decoded speech of the encoder's own decoder.

    lags = None turns the adaptive codebook off. lpc_given, one list of a_k per
    frame, replaces the LPC analysis (for tests with a known filter).
    """
    max_lag = lags[-1] if lags else 0
    past = [0.0] * max(max_lag, 1)
    state = Filters(order)
    params: List[Dict] = []
    out: List[float] = []
    for fi, start in enumerate(range(0, len(s) - frame_len + 1, frame_len)):
        frame = s[start : start + frame_len]
        a = list(lpc_given[fi]) if lpc_given is not None else lpc(frame, order)  # @line L1
        w1, w2 = bandwidth_expand(a, gamma1), bandwidth_expand(a, gamma2)
        h = impulse_response(a, w1, w2, sub_len)  # @line L2
        filtered_book = [convolve(h, c) for c in codebook]
        for sub in range(0, frame_len, sub_len):
            seg = frame[sub : sub + sub_len]
            _, t = state.copy().run(seg, [0.0] * sub_len, a, w1, w2)  # @line L3
            lag, g_a, v = 0, 0.0, [0.0] * sub_len
            if lags:
                vs = [adaptive_vector(past, T, sub_len) for T in lags]
                j, g_a, _ = search(t, [convolve(h, x) for x in vs])  # @line L4
                lag, v = lags[j], vs[j]
                y = convolve(h, v)
                t = [x - g_a * u for x, u in zip(t, y)]  # @line L5
            k, g_f, err = search(t, filtered_book)  # @line L6
            e = [g_a * x + g_f * c for x, c in zip(v, codebook[k])]  # @line L7
            s_hat, _ = state.run(seg, e, a, w1, w2)
            past = (past + e)[-len(past) :]
            out.extend(s_hat)
            params.append({"a": a, "lag": lag, "g_a": g_a, "k": k, "g_f": g_f, "err": err})  # @line L8
    return params, out


def decode(params: Sequence[Dict], codebook: Sequence[Sequence[float]], sub_len: int = 40, max_lag: int = 147) -> List[float]:
    """The decoder: rebuild each excitation and pass it through 1 / A(z)."""
    order = len(params[0]["a"]) if params else 0
    syn = [0.0] * order
    past = [0.0] * max(max_lag, 1)
    out = []
    for p in params:
        v = adaptive_vector(past, p["lag"], sub_len) if p["lag"] else [0.0] * sub_len
        e = [p["g_a"] * x + p["g_f"] * c for x, c in zip(v, codebook[p["k"]])]
        for u in e:
            y = u + sum(c * m for c, m in zip(p["a"], syn))
            syn = [y] + syn[:-1]
            out.append(y)
        past = (past + e)[-len(past) :]
    return out


def snr_db(s: Sequence[float], s_hat: Sequence[float]) -> float:
    """10 log10 of the signal energy over the error energy."""
    noise = sum((x - y) ** 2 for x, y in zip(s, s_hat))
    return 10.0 * math.log10(dot(s, s) / noise) if noise > 0 else math.inf
