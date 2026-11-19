# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hmm-based-speech-synthesis/. The authors are listed in prov/VMKZVY.jsonl.

"""A toy version of the synthesis stage of HMM-based speech synthesis.

This is a toy. It is not HTS and it does not train anything. It keeps the
core of the synthesis stage on one-dimensional streams:

  - a front end that turns a phone list into context labels (left, phone, right),
  - decision trees that map a (context, state) pair to a leaf with Gaussians,
  - state durations d_k = max(1, round(m_k + rho v_k)),
  - expansion of the state Gaussians to frames,
  - maximum likelihood parameter generation (MLPG) with static and delta
    windows, for a one-dimensional spectral parameter and for log F0 over each
    voiced region, solved here by dense Gaussian elimination because T is small,
  - a toy source-filter vocoder: a pulse train or white noise through a
    first-order all-pole filter whose coefficient is the spectral parameter.

The delta window is 0.5 (c[t+1] - c[t-1]) with the frame index clamped to
[0, T - 1] at the edges, as on the MLPG page.
"""

import math
import random
from typing import Dict, List, Sequence, Tuple

N_STATES = 5


def front_end(phones: Sequence[str]) -> List[Dict[str, str]]:
    """One context label per phone: the phone and its two neighbors ('#' at the edges)."""
    out = []
    for i, p in enumerate(phones):
        out.append({"left": phones[i - 1] if i > 0 else "#", "phone": p,
                    "right": phones[i + 1] if i + 1 < len(phones) else "#"})
    return out


def tree_lookup(tree, context: Dict[str, str], state: int):
    """Walk a decision tree. A node is ("leaf", payload) or ("q", key, values, yes, no);
    the key "state" asks about the state index, any other key about the context."""
    node = tree
    while node[0] == "q":
        _, key, values, yes, no = node
        x = state if key == "state" else context[key]
        node = yes if x in values else no
    return node[1]


def rho_for_total(means: Sequence[float], variances: Sequence[float], total: float) -> float:
    """The rho that makes the real-valued durations m_k + rho v_k sum to total."""
    return (total - sum(means)) / sum(variances)


def state_durations(means, variances, rho: float = 0.0) -> List[int]:
    return [max(1, int(round(m + rho * v))) for m, v in zip(means, variances)]


def mlpg_1d(mu_s, var_s, mu_d, var_d) -> List[float]:
    """The trajectory c maximizing sum_t N(c_t; mu_s, var_s) N(delta c_t; mu_d, var_d)."""
    T = len(mu_s)
    rows = []  # each row: (coefficients dict over frames, mean, variance)
    for t in range(T):
        rows.append(({t: 1.0}, mu_s[t], var_s[t]))
        lo, hi = max(t - 1, 0), min(t + 1, T - 1)
        w: Dict[int, float] = {}
        w[hi] = w.get(hi, 0.0) + 0.5
        w[lo] = w.get(lo, 0.0) - 0.5
        rows.append((w, mu_d[t], var_d[t]))
    P = [[0.0] * T for _ in range(T)]
    r = [0.0] * T
    for w, m, v in rows:
        for a, wa in w.items():
            r[a] += wa * m / v
            for b, wb in w.items():
                P[a][b] += wa * wb / v
    return _solve(P, r)


def _solve(A, b) -> List[float]:
    """Gaussian elimination with partial pivoting on copies of A and b."""
    n = len(b)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for k in range(n):
        p = max(range(k, n), key=lambda i: abs(M[i][k]))
        if abs(M[p][k]) < 1e-300:
            raise ValueError("singular system")
        M[k], M[p] = M[p], M[k]
        for i in range(k + 1, n):
            f = M[i][k] / M[k][k]
            if f:
                for j in range(k, n + 1):
                    M[i][j] -= f * M[k][j]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (M[i][n] - sum(M[i][j] * x[j] for j in range(i + 1, n))) / M[i][i]
    return x


def synthesize(phones: Sequence[str], trees: Dict[str, tuple], rho: float = 0.0,
               hop: int = 80, fs: int = 8000, seed: int = 0):
    """Return (samples, frames) for a phone list.

    trees["dur"] leaves are (mean, variance) of a state duration in frames.
    trees["spec"] leaves are (mu_s, var_s, mu_d, var_d) of the spectral parameter.
    trees["f0"] leaves are (voiced_weight, mu_s, var_s, mu_d, var_d) of log F0.
    frames is a dict with the per-frame state means, the voicing and the trajectories.
    """
    labels = front_end(phones)  # @line L1
    spec_g, f0_g, dur_m, dur_v = [], [], [], []
    for lab in labels:  # @line L2
        for k in range(N_STATES):
            m, v = tree_lookup(trees["dur"], lab, k)  # @line L3
            dur_m.append(m)
            dur_v.append(v)
            spec_g.append(tree_lookup(trees["spec"], lab, k))  # @line L4
            f0_g.append(tree_lookup(trees["f0"], lab, k))
    d = state_durations(dur_m, dur_v, rho)  # @line L5
    spec_f, f0_f = [], []
    for k, n in enumerate(d):  # @line L6
        spec_f.extend([spec_g[k]] * n)
        f0_f.extend([f0_g[k]] * n)
    T = len(spec_f)
    voiced = [g[0] > 0.5 for g in f0_f]  # @line L7
    c = mlpg_1d(*[[g[i] for g in spec_f] for i in range(4)])  # @line L8
    logf0 = [None] * T
    t = 0
    while t < T:  # @line L9
        if not voiced[t]:
            t += 1
            continue
        u = t
        while u < T and voiced[u]:
            u += 1
        seg = f0_f[t:u]
        traj = mlpg_1d(*[[g[i] for g in seg] for i in range(1, 5)])
        logf0[t:u] = traj
        t = u
    rng = random.Random(seed)
    excitation, phase = [], 0.0
    for t in range(T):  # @line L10
        for _ in range(hop):
            if voiced[t]:
                phase += math.exp(logf0[t]) / fs
                if phase >= 1.0:
                    phase -= 1.0
                    excitation.append(1.0)
                else:
                    excitation.append(0.0)
            else:
                excitation.append(rng.gauss(0.0, 0.1))
    y, prev = [], 0.0
    for n, e in enumerate(excitation):  # @line L11
        a = max(-0.99, min(0.99, c[n // hop]))
        prev = e + a * prev
        y.append(prev)
    frames = {"durations": d, "voiced": voiced, "spec": c, "logf0": logf0,
              "spec_means": [g[0] for g in spec_f]}
    return y, frames
