# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mixed-precision-training/. The authors are listed in prov/KD5CZY.jsonl.

"""Mixed precision training (Micikevicius et al. 2018) on a simulated FP16.

FP16 and FP32 rounding use the stdlib struct formats 'e' and 'f', which round
to nearest, ties to even. BF16 uses an exact rounding routine. The training
loop keeps FP32 master weights, computes the forward and backward pass in
FP16 with FP32 accumulation, scales the loss, and adjusts the scale
dynamically: halve and skip the step on overflow, double after N clean steps.
"""

import math
import struct
from fractions import Fraction

INF = math.inf


def fp16(x):
    """Round a Python float to IEEE binary16 (round to nearest even)."""
    try:
        return struct.unpack("<e", struct.pack("<e", x))[0]
    except OverflowError:
        return math.copysign(INF, x)


def fp32(x):
    """Round a Python float to IEEE binary32 (round to nearest even)."""
    try:
        return struct.unpack("<f", struct.pack("<f", x))[0]
    except OverflowError:
        return math.copysign(INF, x)


def round_float(x, p, emin, emax):
    """Round x to a binary format with p significand bits (hidden bit included),
    normal exponents emin..emax, subnormals, round to nearest, ties to even."""
    if x == 0 or math.isnan(x) or math.isinf(x):
        return x
    e = math.frexp(abs(x))[1] - 1  # exponent of the leading bit
    q = max(e, emin) - p + 1  # exponent of the last kept bit
    n = round(Fraction(abs(x)) / Fraction(2) ** q)  # Fraction rounds half to even
    r = math.ldexp(n, q)
    if r > math.ldexp(2 ** p - 1, emax - p + 1):
        r = INF
    return math.copysign(r, x)


def bf16(x):
    """Round to bfloat16: 8 significand bits and the exponent range of FP32."""
    return round_float(x, 8, -126, 127)


def ulp(x, p=11, emin=-14):
    """Unit in the last place of x in a format with p significand bits (FP16 default)."""
    if x == 0:
        return math.ldexp(1.0, emin - p + 1)
    return math.ldexp(1.0, max(math.frexp(abs(x))[1] - 1, emin) - p + 1)


def finite(v):
    return all(math.isfinite(a) for a in v)


def dot16(a, b):
    """FP16 inputs, products summed in FP32, result written as FP16."""
    s = 0.0
    for x, y in zip(a, b):
        s = fp32(s + fp32(x * y))
    return fp16(s)


def forward_backward(w16, batch, scale):
    """Linear model z = w . x with loss (1/n) sum (z - y)^2, computed in FP16.
    The loss is multiplied by scale in FP32; the backward pass then runs in
    FP16 with FP32 accumulation. Returns the FP16 loss and the FP16 gradient
    of scale times the loss."""
    n = len(batch)
    xs16 = [[fp16(a) for a in x] for x, _ in batch]
    z = [dot16(w16, x) for x in xs16]
    r = [fp16(zi - fp16(y)) for zi, (_, y) in zip(z, batch)]
    loss = fp16(dot16(r, r) / n)
    dz = [fp16(fp32(scale * fp32(2 * ri / n))) for ri in r]
    g = [dot16(dz, [x[k] for x in xs16]) for k in range(len(w16))]
    return loss, g


class DynamicLossScaler:
    """Halve the scale and skip the step when a gradient is inf or NaN;
    double it after `interval` consecutive clean steps."""

    def __init__(self, scale=2.0 ** 16, growth=2.0, backoff=0.5, interval=2000):
        self.scale, self.growth, self.backoff, self.interval = scale, growth, backoff, interval
        self.clean = 0

    def overflow(self):
        self.scale *= self.backoff  # @line L5
        self.clean = 0

    def clean_step(self):
        self.clean += 1  # @line L9
        if self.clean == self.interval:  # @line L10
            self.scale *= self.growth
            self.clean = 0


def mixed_precision_sgd(w, batches, lr, scaler=None):
    """SGD in mixed precision. w are FP32 master weights; returns the master
    weights after each batch and the list of steps that were skipped."""
    scaler = scaler or DynamicLossScaler()
    master = [fp32(a) for a in w]
    path, skipped = [list(master)], []
    for t, batch in enumerate(batches):  # @line L1
        w16 = [fp16(a) for a in master]  # @line L2
        _, g16 = forward_backward(w16, batch, scaler.scale)  # @line L3
        if not finite(g16):  # @line L4
            scaler.overflow()
            skipped.append(t)  # @line L6
            path.append(list(master))
            continue
        g = [fp32(a / scaler.scale) for a in g16]  # @line L7
        master = [fp32(a - fp32(lr * b)) for a, b in zip(master, g)]  # @line L8
        scaler.clean_step()
        path.append(list(master))
    return path, skipped  # @line L11


def fp16_only_sgd(w, batches, lr):
    """The baseline without a master copy: weights stored and updated in FP16,
    no loss scaling."""
    w16 = [fp16(a) for a in w]
    path = [list(w16)]
    for batch in batches:
        _, g = forward_backward(w16, batch, 1.0)
        w16 = [fp16(a - fp16(lr * b)) for a, b in zip(w16, g)]
        path.append(list(w16))
    return path


def apply_update(weight, update, rnd):
    """weight + update in the format given by the rounding function rnd."""
    return rnd(weight + rnd(update))
