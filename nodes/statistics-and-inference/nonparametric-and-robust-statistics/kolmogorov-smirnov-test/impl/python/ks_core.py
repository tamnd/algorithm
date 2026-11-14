# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kolmogorov-smirnov-test/. The authors are listed in prov/DWDQWW.jsonl.

import math
from typing import Callable

ALTERNATIVES = ("two-sided", "greater", "less")

# Below this two-sided tail the code returns 2 P(D+ >= d), an upper bound whose
# relative excess P(D+ >= d and D- >= d) / P(D >= d) is negligible there, instead of
# 1 - P(D < d), which loses digits to cancellation.
SMALL_TAIL = 1e-3


def ks_statistic(x: list[float], cdf: Callable[[float], float]) -> tuple[float, float, float]:
    """Return (D, D+, D-) with D+ = sup (F_n - F_0) and D- = sup (F_0 - F_n)."""
    n = len(x)
    u = [cdf(v) for v in sorted(x)]  # @line L1
    d_plus = max(i / n - ui for i, ui in enumerate(u, start=1))  # @line L2
    d_minus = max(ui - (i - 1) / n for i, ui in enumerate(u, start=1))
    return max(d_plus, d_minus), d_plus, d_minus


def smirnov_sf(n: int, d: float) -> float:
    """P(D_n^+ >= d) for a continuous F_0, by the exact finite sum of Smirnov,
    Birnbaum and Tingey: d sum_{j=0}^{floor(n(1-d))} C(n, j) (1 - d - j/n)^(n-j) (d + j/n)^(j-1).
    Every term is positive, so the sum does not cancel; each term is formed in logs."""
    if d <= 0.0:
        return 1.0
    if d >= 1.0:
        return 0.0
    terms = []
    for j in range(int(math.floor(n * (1.0 - d) + 1e-12)) + 1):
        a = 1.0 - d - j / n
        if a <= 0.0:
            if n - j > 0:
                continue
            log_a = 0.0  # 0^0 = 1
        else:
            log_a = (n - j) * math.log(a)
        log_c = math.lgamma(n + 1) - math.lgamma(j + 1) - math.lgamma(n - j + 1)
        terms.append(math.exp(log_c + log_a + (j - 1) * math.log(d + j / n)))
    return min(1.0, d * math.fsum(terms))


def _matmul(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    bt = list(zip(*b))
    return [[math.fsum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def kolmogorov_cdf(n: int, d: float) -> float:
    """P(D_n < d) for a continuous F_0, by the matrix method of Durbin (1973) in the
    form of Marsaglia, Tsang and Wang (2003). Powers are rescaled by powers of 2."""
    if d <= 0.0:
        return 0.0
    if d >= 1.0:
        return 1.0
    nd = n * d
    k = int(math.floor(nd)) + 1  # @line L4
    h = k - nd
    m = 2 * k - 1
    fact = [math.factorial(i) for i in range(m + 1)]
    hm = [[1.0 / fact[i - j + 1] if i - j + 1 >= 0 else 0.0 for j in range(m)]
          for i in range(m)]  # @line L5
    for i in range(m):  # @line L6
        hm[i][0] -= h ** (i + 1) / fact[i + 1]
        hm[m - 1][i] -= h ** (m - i) / fact[m - i]
    hm[m - 1][0] += max(0.0, 2.0 * h - 1.0) ** m / fact[m]
    # Repeated squaring; each matrix carries a binary exponent so nothing overflows.
    result, result_exp = None, 0
    base, base_exp = hm, 0
    e = n
    while e:  # @line L7
        if e & 1:
            if result is None:
                result, result_exp = base, base_exp
            else:
                result, result_exp = _matmul(result, base), result_exp + base_exp
                big = max(abs(v) for row in result for v in row)
                if big > 0.0:
                    shift = math.frexp(big)[1]
                    result = [[math.ldexp(v, -shift) for v in row] for row in result]
                    result_exp += shift
        e >>= 1
        if e:
            base, base_exp = _matmul(base, base), 2 * base_exp
            big = max(abs(v) for row in base for v in row)
            if big > 0.0:
                shift = math.frexp(big)[1]
                base = [[math.ldexp(v, -shift) for v in row] for row in base]
                base_exp += shift
    t = result[k - 1][k - 1]
    if t <= 0.0:
        return 0.0
    log_p = math.log(t) + result_exp * math.log(2.0) + math.lgamma(n + 1) - n * math.log(n)
    return min(1.0, math.exp(log_p))


def kolmogorov_sf(x: float) -> float:
    """The limit P(K > x) = 2 sum_{k>=1} (-1)^(k-1) exp(-2 k^2 x^2) of sqrt(n) D_n.
    For x < 1 the alternating series converges slowly, so the code uses the
    equivalent form 1 - (sqrt(2 pi)/x) sum_{k>=1} exp(-(2k-1)^2 pi^2 / (8 x^2))."""
    if x <= 0.0:
        return 1.0
    if x < 1.0:
        s = math.fsum(math.exp(-((2 * k - 1) ** 2) * math.pi**2 / (8 * x * x)) for k in range(1, 30))
        return max(0.0, 1.0 - math.sqrt(2 * math.pi) / x * s)
    return min(1.0, 2.0 * math.fsum((-1) ** (k - 1) * math.exp(-2.0 * k * k * x * x)
                                    for k in range(1, 101)))


def ks_1samp(
    x: list[float],
    cdf: Callable[[float], float],
    alternative: str = "two-sided",
    method: str = "auto",
) -> tuple[float, float]:
    """One-sample Kolmogorov-Smirnov test of H0: the data have the continuous CDF F_0.

    Returns (statistic, p). "greater" uses D+ (H1: F > F_0 somewhere), "less"
    uses D- (H1: F < F_0 somewhere); their exact null laws are the same.
    method "exact" uses the exact finite-n law, "asymptotic" the Kolmogorov
    limit (or exp(-2 n d^2) for one side), and "auto" is exact for n <= 100.
    """
    if alternative not in ALTERNATIVES:
        raise ValueError("unknown alternative")
    if method not in ("auto", "exact", "asymptotic"):
        raise ValueError("unknown method")
    n = len(x)
    if n == 0:
        raise ValueError("need at least one observation")
    d, d_plus, d_minus = ks_statistic(x, cdf)
    use_exact = method == "exact" or (method == "auto" and n <= 100)
    if alternative != "two-sided":
        s = d_plus if alternative == "greater" else d_minus
        if use_exact:
            return s, smirnov_sf(n, s)
        return s, min(1.0, math.exp(-2.0 * n * s * s))
    if not use_exact:
        return d, kolmogorov_sf(math.sqrt(n) * d)
    tail2 = 2.0 * smirnov_sf(n, d)
    if d >= 0.5 or tail2 < SMALL_TAIL:  # @line L3
        return d, min(1.0, tail2)
    return d, max(0.0, 1.0 - kolmogorov_cdf(n, d))  # @line L8


def ks_2samp_stat(x: list[float], y: list[float]) -> tuple[int, int, int]:
    """Return (t, m, n) with D = t / (m n) = sup |F_m - G_n|, where t = max |i n - j m|
    over the points after each block of equal values in the merged order."""
    m, n = len(x), len(y)
    xs, ys = sorted(x), sorted(y)
    i = j = t = 0
    while i < m or j < n:
        v = min(xs[i] if i < m else math.inf, ys[j] if j < n else math.inf)
        while i < m and xs[i] == v:
            i += 1
        while j < n and ys[j] == v:
            j += 1
        t = max(t, abs(i * n - j * m))
    return t, m, n


def ks_2samp(x: list[float], y: list[float], method: str = "exact") -> tuple[float, float]:
    """Two-sample Kolmogorov-Smirnov test, two-sided. Returns (D, p).

    method "exact" counts the lattice paths from (0, 0) to (m, n) that stay
    strictly inside |i n - j m| < t; the p-value is 1 minus their share of all
    C(m + n, m) paths, in exact integers. It is exact when there are no ties.
    method "asymptotic" uses the Kolmogorov limit at sqrt(m n / (m + n)) D.
    """
    if not x or not y:
        raise ValueError("both samples must be nonempty")
    t, m, n = ks_2samp_stat(x, y)
    d = t / (m * n)
    if method == "asymptotic":
        return d, kolmogorov_sf(math.sqrt(m * n / (m + n)) * d)
    if method != "exact":
        raise ValueError("unknown method")
    row = [0] * (n + 1)
    for i in range(m + 1):
        for j in range(n + 1):
            if abs(i * n - j * m) >= t:
                row[j] = 0
            elif i == 0 and j == 0:
                row[j] = 1
            else:
                row[j] = (row[j] if i > 0 else 0) + (row[j - 1] if j > 0 else 0)
    total = math.comb(m + n, m)
    return d, (total - row[n]) / total
