# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/template-attack/. The authors are listed in prov/9Z5T63.jsonl.
"""Template attack (Gaussian templates) on a synthetic two-sample leakage model.

The traces come from a stated statistical model, never from a device. For
the value v = S(p xor k), with S the 4-bit S-box of PRESENT (Bogdanov et
al., CHES 2007), sample 0 is HW(v) and sample 1 is a weighted sum of the
bits of v, and the noise of the two samples is Gaussian with correlation
``rho``, drawn with a seeded ``random.Random``. This is a study model for
defenders and students.
"""

import math
import random

PRESENT_SBOX: tuple[int, ...] = (
    0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD,
    0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2,
)
BIT_WEIGHTS: tuple[float, ...] = (1.0, 0.5, 0.25, 2.0)

Vector = list[float]
Matrix = list[list[float]]


def hamming_weight(v: int) -> int:
    """Return the number of 1 bits of a non-negative integer."""
    return bin(v).count("1")


def leakage_mean(v: int) -> Vector:
    """The noiseless two-sample leakage of the value v in the model."""
    return [
        float(hamming_weight(v)),
        sum(w for b, w in enumerate(BIT_WEIGHTS) if (v >> b) & 1),
    ]


def noisy_leakage(rng: random.Random, v: int, sigma: float, rho: float) -> Vector:
    """Leakage of v plus Gaussian noise with variance sigma^2 and correlation rho."""
    z0 = rng.gauss(0.0, 1.0)
    z1 = rng.gauss(0.0, 1.0)
    mu = leakage_mean(v)
    return [mu[0] + sigma * z0, mu[1] + sigma * (rho * z0 + math.sqrt(1.0 - rho * rho) * z1)]


def profiling_set(rng: random.Random, n: int, sigma: float, rho: float) -> list[tuple[int, Vector]]:
    """n profiling pairs (value, trace) with a known, uniform value. Cost: O(n)."""
    out = []
    for _ in range(n):
        v = rng.randrange(16)
        out.append((v, noisy_leakage(rng, v, sigma, rho)))
    return out


def attack_set(
    rng: random.Random, key: int, m: int, sigma: float, rho: float
) -> list[tuple[int, Vector]]:
    """m attack pairs (input, trace) for the key. Cost: O(m)."""
    out = []
    for _ in range(m):
        p = rng.randrange(16)
        out.append((p, noisy_leakage(rng, PRESENT_SBOX[p ^ key], sigma, rho)))
    return out


def cholesky(a: Matrix) -> Matrix:
    """Lower triangular L with L L^T = a, for a symmetric positive definite a.

    Raises ValueError if a is not positive definite. Cost: O(T^3).
    """
    t = len(a)
    low = [[0.0] * t for _ in range(t)]
    for i in range(t):
        for j in range(i + 1):
            s = a[i][j] - sum(low[i][q] * low[j][q] for q in range(j))
            if i == j:
                if s <= 0.0:
                    raise ValueError("matrix is not positive definite")
                low[i][i] = math.sqrt(s)
            else:
                low[i][j] = s / low[j][j]
    return low


def quadratic_form(low: Matrix, x: Vector) -> float:
    """Return x^T (L L^T)^{-1} x by one forward substitution. Cost: O(T^2)."""
    y: Vector = []
    for i in range(len(x)):
        y.append((x[i] - sum(low[i][q] * y[q] for q in range(i))) / low[i][i])
    return sum(v * v for v in y)


def build_templates(
    profile: list[tuple[int, Vector]], classes: int = 16, pooled: bool = True
) -> tuple[list[Vector], list[Matrix], list[float]]:
    """Return (means, Cholesky factors, log determinants) for each class.

    With ``pooled`` the covariance is the pooled covariance of the residuals
    of all classes (one matrix for every class); otherwise each class has its
    own sample covariance. Precondition: each class has at least two traces
    (T + 1 without pooling) and the covariances are positive definite.
    Cost: Theta(n * T^2 + V * T^3) for n traces and V classes.
    """
    t = len(profile[0][1])
    groups: list[list[Vector]] = [[] for _ in range(classes)]
    for v, tr in profile:
        groups[v].append(tr)
    if any(not g for g in groups):
        raise ValueError("every class needs profiling traces")
    means = [[sum(tr[j] for tr in g) / len(g) for j in range(t)] for g in groups]  # @line L1

    def scatter(vs: list[int]) -> tuple[Matrix, int]:
        s = [[0.0] * t for _ in range(t)]
        count = 0
        for v in vs:
            for tr in groups[v]:
                d = [tr[j] - means[v][j] for j in range(t)]
                for a in range(t):
                    for b in range(t):
                        s[a][b] += d[a] * d[b]
            count += len(groups[v]) - 1
        return [[x / count for x in row] for row in s], count

    if pooled:
        cov, _ = scatter(list(range(classes)))  # @line L2
        low = cholesky(cov)  # @line L3
        lows = [low] * classes
    else:
        lows = [cholesky(scatter([v])[0]) for v in range(classes)]
    logdets = [2.0 * sum(math.log(low[i][i]) for i in range(t)) for low in lows]
    return means, lows, logdets


def template_attack(
    attack: list[tuple[int, Vector]],
    templates: tuple[list[Vector], list[Matrix], list[float]],
    sbox: tuple[int, ...] = PRESENT_SBOX,
) -> tuple[int, list[float]]:
    """Return (best guess, log-likelihood of each guess) by Chari et al.

    The score of g is the sum over the attack traces (p, l) of the Gaussian
    log density of l under the template of the class sbox[p ^ g], without
    the constant -T/2 log(2 pi). The first guess with the top score wins.

    Precondition: at least one attack trace; templates from
    build_templates. Cost: Theta(g * m * T^2) for g guesses and m traces,
    and Theta(g + T) extra space.
    """
    if not attack:
        raise ValueError("need at least one attack trace")
    means, lows, logdets = templates
    best, top = -1, -math.inf  # @line L4
    scores: list[float] = []
    for g in range(len(sbox)):  # @line L5
        score = 0.0  # @line L6
        for p, tr in attack:  # @line L7
            v = sbox[p ^ g]
            d = [tr[j] - means[v][j] for j in range(len(tr))]
            score -= 0.5 * (quadratic_form(lows[v], d) + logdets[v])  # @line L8
        scores.append(score)
        if score > top:  # @line L9
            best, top = g, score  # @line L10
    return best, scores  # @line L11
