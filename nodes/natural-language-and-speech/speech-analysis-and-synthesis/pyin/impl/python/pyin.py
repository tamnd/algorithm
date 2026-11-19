# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pyin/. The authors are listed in prov/FCGMHH.jsonl.

"""pYIN, the probabilistic YIN pitch tracker of Mauch and Dixon (2014).

Stage 1, per frame: the YIN difference function d and its cumulative mean
normalized form d', then a prior P(s_i) over N = 100 thresholds s_i = i / 100.
Each threshold picks the YIN period Y(s_i): the bottom of the first dip of d'
below s_i, or, if no value is below s_i, the global minimum of d'. The period
tau gets the probability sum_i a(s_i, tau) P(s_i) [Y(s_i) = tau], with a = 1 when
d'(tau) < s_i and a = p_a = 0.01 otherwise. The mass left over means unvoiced.

Stage 2, over frames: an HMM with M pitch bins of 10 cents from 55 Hz, each with
a voiced and an unvoiced state. The observation of voiced bin m is 0.5 p*_m (the
candidate mass in the bin) and of every unvoiced state 0.5 (1 - sum_k p*_k). The
pitch moves by at most J bins per frame with triangular weights, the voicing
stays with probability 0.99. Viterbi decoding in log space gives the track.

The paper prints the Beta parameters as alpha = 1 and beta = 18, 11 1/3, 8, but
its stated means 0.10, 0.15 and 0.20 need alpha = 2, which this code uses.
"""

import math
from fractions import Fraction
from math import comb
from typing import Dict, List, Optional, Sequence, Tuple

from nlslog import NEG_INF, safe_log

# ---------------------------------------------------------------- stage 1


def difference(x: Sequence[float], w: int, tau_max: int) -> List[float]:
    """d(tau) = sum_{j=0}^{w-1} (x[j] - x[j + tau])^2 for tau = 0 .. tau_max. Needs w + tau_max samples."""
    if len(x) < w + tau_max:
        raise ValueError("the frame needs w + tau_max samples")
    return [sum((x[j] - x[j + tau]) ** 2 for j in range(w)) for tau in range(tau_max + 1)]


def cmndf(d: Sequence[float]) -> List[float]:
    """d'(0) = 1 and d'(tau) = tau d(tau) / sum_{j=1}^{tau} d(j), or 1 when the sum is 0."""
    out = [1.0]
    s = 0.0
    for tau in range(1, len(d)):
        s += d[tau]
        out.append(tau * d[tau] / s if s > 0 else 1.0)
    return out


def beta_cdf(x, a: int, b: int):
    """The regularized incomplete beta function I_x(a, b) for integer a, b >= 1, by the binomial sum.

    It is exact on Fractions: I_x(a, b) = sum_{j=a}^{a+b-1} C(a+b-1, j) x^j (1 - x)^(a+b-1-j).
    """
    n = a + b - 1
    return sum(comb(n, j) * x ** j * (1 - x) ** (n - j) for j in range(a, n + 1))


def threshold_prior(n: int = 100, a: int = 2, b: int = 18) -> List[Fraction]:
    """P(s_i) = I_{s_i}(a, b) - I_{s_{i-1}}(a, b) for s_i = i / n, i = 1 .. n. Sums to exactly 1."""
    cdf = [beta_cdf(Fraction(i, n), a, b) for i in range(n + 1)]
    return [cdf[i] - cdf[i - 1] for i in range(1, n + 1)]


def yin_period(dp: Sequence[float], s: float, tau_min: int, tau_max: int) -> Tuple[int, bool]:
    """Y(s): the bottom of the first dip of d' below s in [tau_min, tau_max], and True; else the argmin and False."""
    for tau in range(tau_min, tau_max + 1):
        if dp[tau] < s:
            while tau < tau_max and dp[tau + 1] < dp[tau]:
                tau += 1
            return tau, True
    best = tau_min
    for tau in range(tau_min + 1, tau_max + 1):
        if dp[tau] < dp[best]:
            best = tau
    return best, False


def parabolic(v: Sequence[float], tau: int) -> float:
    """The vertex of the parabola through v[tau - 1], v[tau], v[tau + 1], or tau at an edge."""
    if tau < 1 or tau + 1 >= len(v):
        return float(tau)
    a = v[tau - 1] - 2 * v[tau] + v[tau + 1]
    if a == 0:
        return float(tau)
    return tau + (v[tau - 1] - v[tau + 1]) / (2 * a)


def candidates(
    frame: Sequence[float],
    fs: float,
    w: int,
    fmin: float,
    fmax: float,
    prior: Sequence[float],
    p_a: float = 0.01,
) -> List[Tuple[float, float]]:
    """Stage 1 on one frame: a list of (frequency in Hz, probability), at most one pair per period."""
    tau_min = max(2, math.floor(fs / fmax))
    tau_max = math.ceil(fs / fmin)
    d = difference(frame, w, tau_max + 1)  # @line L1
    dp = cmndf(d)  # @line L2
    n = len(prior)
    mass: Dict[int, float] = {}
    for i in range(1, n + 1):  # @line L3
        tau, below = yin_period(dp, i / n, tau_min, tau_max)  # @line L4
        mass[tau] = mass.get(tau, 0.0) + (1.0 if below else p_a) * float(prior[i - 1])  # @line L5
    out = []
    for tau in sorted(mass):
        period = parabolic(dp, tau)  # @line L6
        out.append((fs / period, mass[tau]))
    return out


# ---------------------------------------------------------------- stage 2


def bin_frequency(m: int, fref: float = 55.0) -> float:
    """The center frequency of bin m: 10 cents per bin from fref."""
    return fref * 2.0 ** (m / 120.0)


def observations(cands: Sequence[Tuple[float, float]], m_bins: int, fref: float = 55.0) -> List[float]:
    """The 2M observation probabilities: voiced bins 0 .. M-1, then unvoiced bins M .. 2M-1."""
    pstar = [0.0] * m_bins
    for f, p in cands:
        m = round(1200.0 * math.log2(f / fref) / 10.0)
        if 0 <= m < m_bins:
            pstar[m] += p  # @line L7
    unvoiced = 0.5 * max(0.0, 1.0 - sum(pstar))
    return [0.5 * v for v in pstar] + [unvoiced] * m_bins


def pitch_transition(m_bins: int, jump: int) -> List[List[Tuple[int, float]]]:
    """For each bin i, the list of (j, P(j | i)) with P(j | i) = (jump + 1 - |j - i|) / (jump + 1)^2 for |j - i| <= jump.

    The triangular window sums to 1, as in the paper. Near the ends of the bin
    range the part of the window outside the range is dropped, so those rows sum
    to less than 1; normalizing each row instead would favor the end bins.
    """
    z = float((jump + 1) ** 2)
    rows = []
    for i in range(m_bins):
        lo, hi = max(0, i - jump), min(m_bins - 1, i + jump)
        rows.append([(j, (jump + 1 - abs(j - i)) / z) for j in range(lo, hi + 1)])
    return rows


def transition_prob(i: int, j: int, m_bins: int, rows, p_stay: float) -> float:
    """P(state j | state i) for the 2M states: the pitch move times the voicing move."""
    bi, vi = i % m_bins, i < m_bins
    bj, vj = j % m_bins, j < m_bins
    pitch = dict(rows[bi]).get(bj, 0.0)
    return pitch * (p_stay if vi == vj else 1.0 - p_stay)


def initial(m_bins: int, start: str) -> List[float]:
    """Log start probabilities: "all" is uniform over the 2M states, "unvoiced" (the paper) over the M unvoiced ones."""
    if start == "all":
        return [-math.log(2 * m_bins)] * (2 * m_bins)
    if start == "unvoiced":
        return [NEG_INF] * m_bins + [-math.log(m_bins)] * m_bins
    raise ValueError("start must be 'all' or 'unvoiced'")


def viterbi(
    obs: Sequence[Sequence[float]], m_bins: int, jump: int = 25, p_stay: float = 0.99, start: str = "all"
) -> Tuple[List[int], float]:
    """The most probable state sequence of the pYIN HMM and its log probability.

    The states are 0 .. M-1 (voiced) and M .. 2M-1 (unvoiced). Ties go to the
    smallest state. With start = "unvoiced", as in the paper, a first frame whose
    voiced mass is 1 gives every path probability 0, and ValueError is raised.
    """
    s_count = 2 * m_bins
    rows = pitch_transition(m_bins, jump)
    into: List[List[Tuple[int, float]]] = [[] for _ in range(m_bins)]  # into[j] = (i, log P(j | i))
    for i, row in enumerate(rows):
        for j, p in row:
            into[j].append((i, math.log(p)))
    log_stay, log_switch = safe_log(p_stay), safe_log(1.0 - p_stay)
    init = initial(m_bins, start)
    delta = [init[s] + safe_log(obs[0][s]) for s in range(s_count)]  # @line L8
    back: List[List[int]] = []
    for t in range(1, len(obs)):  # @line L9
        new = [NEG_INF] * s_count
        ptr = [0] * s_count
        for j in range(s_count):
            bj, vj = j % m_bins, j < m_bins
            best, arg = NEG_INF, -1
            for bi, lp in into[bj]:
                for vi in (True, False):
                    i = bi if vi else bi + m_bins
                    if delta[i] == NEG_INF:
                        continue
                    cand = delta[i] + lp + (log_stay if vi == vj else log_switch)  # @line L10
                    if cand > best or (cand == best and i < arg):
                        best, arg = cand, i
            new[j] = best + safe_log(obs[t][j]) if arg >= 0 else NEG_INF  # @line L11
            ptr[j] = max(arg, 0)
        delta = new
        back.append(ptr)
    last = max(range(s_count), key=lambda s: (delta[s], -s))  # @line L12
    if delta[last] == NEG_INF:
        raise ValueError("every state sequence has probability 0")
    path = [last]
    for ptr in reversed(back):  # @line L13
        path.append(ptr[path[-1]])
    path.reverse()
    return path, delta[last]


def pyin(
    x: Sequence[float],
    fs: float,
    frame_len: int,
    hop: int,
    fmin: float = 55.0,
    fmax: float = 880.0,
    m_bins: int = 480,
    jump: int = 25,
    prior: Optional[Sequence[float]] = None,
    start: str = "all",
) -> List[Optional[float]]:
    """The pYIN track: one frequency in Hz (the bin center) or None (unvoiced) per frame.

    Each frame uses frame_len samples for the sum and needs frame_len + fs / fmin + 2 samples.
    """
    if prior is None:
        prior = threshold_prior()
    need = frame_len + math.ceil(fs / fmin) + 2
    obs = []
    pos = 0
    while pos + need <= len(x):
        obs.append(observations(candidates(x[pos : pos + need], fs, frame_len, fmin, fmax, prior), m_bins))
        pos += hop
    if not obs:
        return []
    path, _ = viterbi(obs, m_bins, jump, 0.99, start)
    return [bin_frequency(s) if s < m_bins else None for s in path]  # @line L14
