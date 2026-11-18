# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/motion-warping/. The authors are listed in prov/7QR9V6.jsonl.
"""Motion warping (Witkin and Popovic 1995) of sampled joint curves.

A motion channel is a list of samples theta[0..f-1] at the frame times
0, 1, ..., f-1 (any unit of time; the code uses frames). The warped channel
is

    theta'(t) = c(t) theta(g(t)) + b(t),

where g is a time warp (a monotone piecewise linear map from new time to
original time), c is a smooth scale curve and b is a smooth offset curve.
The animator gives key constraints (t_k, value_k): the warped channel must
take value_k at time t_k. With c fixed (by default c = 1), the offsets
b_k = value_k - c(t_k) theta(g(t_k)) are interpolated by a natural cubic
spline, so theta' passes through every key and stays C2 between keys
wherever theta is C2. Outside the key range, b keeps its end value.
"""

import bisect


def sample(theta, t):
    """Linear interpolation of the samples, clamped at the ends."""
    f = len(theta)
    if t <= 0:
        return theta[0]
    if t >= f - 1:
        return theta[-1]
    i = int(t)
    u = t - i
    return (1 - u) * theta[i] + u * theta[i + 1]


class NaturalSpline:
    """The natural cubic spline through (x_k, y_k), x strictly increasing."""

    def __init__(self, xs, ys):
        n = len(xs)
        if n < 1 or any(b <= a for a, b in zip(xs, xs[1:])):
            raise ValueError("key times must increase")
        self.x, self.y = list(xs), list(ys)
        self.m = [0.0] * n  # second derivatives
        if n > 2:
            h = [xs[i + 1] - xs[i] for i in range(n - 1)]
            # tridiagonal system for m[1..n-2], with m[0] = m[n-1] = 0
            a = [h[i - 1] for i in range(1, n - 1)]
            b = [2.0 * (h[i - 1] + h[i]) for i in range(1, n - 1)]
            c = [h[i] for i in range(1, n - 1)]
            d = [6.0 * ((ys[i + 1] - ys[i]) / h[i] - (ys[i] - ys[i - 1]) / h[i - 1])
                 for i in range(1, n - 1)]
            for i in range(1, len(b)):
                w = a[i] / b[i - 1]
                b[i] -= w * c[i - 1]
                d[i] -= w * d[i - 1]
            sol = [0.0] * len(b)
            sol[-1] = d[-1] / b[-1]
            for i in range(len(b) - 2, -1, -1):
                sol[i] = (d[i] - c[i] * sol[i + 1]) / b[i]
            self.m[1:n - 1] = sol

    def __call__(self, t):
        x, y, m = self.x, self.y, self.m
        if len(x) == 1 or t <= x[0]:
            return y[0]
        if t >= x[-1]:
            return y[-1]
        i = bisect.bisect_right(x, t) - 1
        h = x[i + 1] - x[i]
        A = (x[i + 1] - t) / h
        B = (t - x[i]) / h
        return (A * y[i] + B * y[i + 1]
                + ((A ** 3 - A) * m[i] + (B ** 3 - B) * m[i + 1]) * h * h / 6.0)


class TimeWarp:
    """g(t') through the pairs (new time, original time), both increasing.
    Outside the pairs, g has slope 1."""

    def __init__(self, pairs):
        self.new = [p for p, _ in pairs]
        self.old = [q for _, q in pairs]
        if any(b <= a for a, b in zip(self.new, self.new[1:])) or \
                any(b <= a for a, b in zip(self.old, self.old[1:])):
            raise ValueError("a time warp must be strictly increasing")

    def __call__(self, t):
        n, o = self.new, self.old
        if t <= n[0]:
            return o[0] + (t - n[0])
        if t >= n[-1]:
            return o[-1] + (t - n[-1])
        i = bisect.bisect_right(n, t) - 1
        u = (t - n[i]) / (n[i + 1] - n[i])
        return o[i] + u * (o[i + 1] - o[i])


def warp_channel(theta, keys, scale_keys=None, timewarp=None):
    """Return the function t -> theta'(t) for one channel.

    keys: list of (t_k, value_k) in new time; scale_keys: optional list of
    (t_k, c_k) for the scale curve; timewarp: optional TimeWarp.
    """
    g = timewarp if timewarp is not None else (lambda t: t)
    if scale_keys:
        c = NaturalSpline([t for t, _ in scale_keys], [v for _, v in scale_keys])
    else:
        c = lambda t: 1.0
    src = lambda t: sample(theta, g(t))  # @line L1
    keys = sorted(keys)
    offsets = [v - c(t) * src(t) for t, v in keys]  # @line L2
    b = NaturalSpline([t for t, _ in keys], offsets)  # @line L3
    return lambda t: c(t) * src(t) + b(t)  # @line L4


def warp_motion(motion, keys_per_channel, timewarp=None, frames=None):
    """Warp every channel and resample at the integer new times.

    motion: list of frames, each a list of channel values.
    keys_per_channel: dict channel -> list of (t, value); channels without
    keys get only the time warp.
    """
    f = len(motion)
    if frames is None:
        frames = f if timewarp is None else int(timewarp.new[-1]) + 1
    chans = list(zip(*motion))
    out_ch = []
    for ci, ch in enumerate(chans):
        keys = keys_per_channel.get(ci)
        if keys:
            fn = warp_channel(list(ch), keys, timewarp=timewarp)
        else:
            g = timewarp if timewarp is not None else (lambda t: t)
            fn = lambda t, ch=ch, g=g: sample(list(ch), g(t))
        out_ch.append([fn(t) for t in range(frames)])  # @line L5
    return [list(v) for v in zip(*out_ch)]  # @line L6
