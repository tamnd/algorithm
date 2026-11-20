# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sofi/. The authors are listed in prov/70NF24.jsonl.
"""Super-resolution optical fluctuation imaging (SOFI): pixelwise cumulants.

A movie is a list of T frames, each an image movie[t][i][j]. The SOFI image
of order n with the time lags (tau_1, ..., tau_n) is, at each pixel, the
sample joint cumulant of the n series X_q(t) = F(t + tau_q), for
t = 0, ..., T - 1 - max(tau). Sample moments are means over these windows.

With distinct lags, noise that is independent from frame to frame adds
nothing to the cumulant in expectation; a constant background adds nothing
exactly. Works with float and fractions.Fraction values.
"""

import math


def _mean(xs):
    return sum(xs) / len(xs)


def _centered(xs):
    m = _mean(xs)
    return [x - m for x in xs]


def cumulant(series):
    """The sample joint cumulant of 2, 3 or 4 equal-length series.

    On the centered series a, b, c, d:
      order 2: E[ab]
      order 3: E[abc]
      order 4: E[abcd] - E[ab] E[cd] - E[ac] E[bd] - E[ad] E[bc]
    """
    n = len(series)
    if n not in (2, 3, 4):
        raise ValueError("order must be 2, 3 or 4")
    z = [_centered(s) for s in series]
    length = len(z[0])
    if n == 2:
        return _mean([z[0][t] * z[1][t] for t in range(length)])
    if n == 3:
        return _mean([z[0][t] * z[1][t] * z[2][t] for t in range(length)])

    def m2(p, q):
        return _mean([z[p][t] * z[q][t] for t in range(length)])

    m4 = _mean([z[0][t] * z[1][t] * z[2][t] * z[3][t] for t in range(length)])
    return m4 - m2(0, 1) * m2(2, 3) - m2(0, 2) * m2(1, 3) - m2(0, 3) * m2(1, 2)


def set_partitions(items):
    """All partitions of the list items into nonempty blocks."""
    if not items:
        yield []
        return
    first, rest = items[0], items[1:]
    for part in set_partitions(rest):
        yield [[first]] + part
        for i in range(len(part)):
            yield part[:i] + [[first] + part[i]] + part[i + 1:]


def cumulant_by_partitions(series):
    """The sample joint cumulant of any order by the partition formula.

    kappa = sum over partitions pi of (-1)^(|pi| - 1) (|pi| - 1)! prod_B E[prod_{q in B} X_q],
    with raw (not centered) sample moments.
    """
    length = len(series[0])
    total = 0
    for part in set_partitions(list(range(len(series)))):
        k = len(part)
        term = (-1) ** (k - 1) * math.factorial(k - 1)
        for block in part:
            prod = [1] * length
            for q in block:
                prod = [p * v for p, v in zip(prod, series[q])]
            term = term * _mean(prod)
        total += term
    return total


def lagged(s, lags):
    """The series X_q(t) = s(t + lags[q]) for t = 0, ..., len(s) - 1 - max(lags)."""
    length = len(s) - max(lags)
    if length < 2:
        raise ValueError("the movie is too short for these lags")
    return [s[tau:tau + length] for tau in lags]


def sofi_image(movie, order=2, lags=None):
    """The SOFI image of the given order: the joint cumulant of lagged series at each pixel.

    lags defaults to (0, 1, ..., order - 1), so all lags are distinct.
    """
    if lags is None:
        lags = tuple(range(order))
    if len(lags) != order:
        raise ValueError("one lag per factor")
    n1, n2 = len(movie[0]), len(movie[0][0])
    out = [[0] * n2 for _ in range(n1)]
    for i in range(n1):  # @line L1
        for j in range(n2):  # @line L1
            s = [frame[i][j] for frame in movie]  # @line L2
            xs = lagged(s, lags)  # @line L3
            out[i][j] = cumulant(xs)  # @line L4 L5
    return out  # @line L6


def mean_image(movie):
    """The widefield image: the time mean of each pixel."""
    n1, n2 = len(movie[0]), len(movie[0][0])
    return [[_mean([f[i][j] for f in movie]) for j in range(n2)] for i in range(n1)]


def markov_blinking(rng, length, a, b, on=None):
    """A two-state blinking series: P(off -> on) = a, P(on -> off) = b.

    The stationary on fraction is rho = a / (a + b), and the lag-1
    covariance is rho (1 - rho) (1 - a - b). The first state is drawn from
    the stationary law unless on is given.
    """
    if on is None:
        on = rng.random() < a / (a + b)
    out = []
    for _ in range(length):
        out.append(1 if on else 0)
        u = rng.random()
        on = (u >= b) if on else (u < a)
    return out


def gaussian_psf(dist2, sigma):
    """exp(-d^2 / (2 sigma^2)) for the squared distance d^2."""
    return math.exp(-dist2 / (2 * sigma * sigma))


def simulate_movie(rng, shape, emitters, sigma, length, a, b, background=0.0, noise=0.0):
    """A movie of blinking emitters with a Gaussian PSF.

    emitters is a list of (row, column, brightness) with real coordinates.
    Each frame is background + sum_k brightness_k s_k(t) U(r - r_k) plus
    independent N(0, noise^2) values.
    """
    n1, n2 = shape
    weights = [[[gaussian_psf((i - r) ** 2 + (j - c) ** 2, sigma) * e for j in range(n2)]
                for i in range(n1)] for r, c, e in emitters]
    states = [markov_blinking(rng, length, a, b) for _ in emitters]
    movie = []
    for t in range(length):
        frame = [[background] * n2 for _ in range(n1)]
        for k, w in enumerate(weights):
            if states[k][t]:
                for i in range(n1):
                    for j in range(n2):
                        frame[i][j] += w[i][j]
        if noise > 0:
            for i in range(n1):
                for j in range(n2):
                    frame[i][j] += rng.gauss(0.0, noise)
        movie.append(frame)
    return movie
