# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mixed-precision-training/. The authors are listed in prov/KD5CZY.jsonl.

import math
import random

from mixed_precision_training import (
    DynamicLossScaler,
    apply_update,
    bf16,
    forward_backward,
    fp16,
    fp16_only_sgd,
    fp32,
    mixed_precision_sgd,
    round_float,
    ulp,
)


def test_exact_rounding_agrees_with_struct_formats() -> None:
    rng = random.Random(1)
    for _ in range(5000):
        x = rng.uniform(-1, 1) * 2.0 ** rng.randint(-30, 18)
        assert round_float(x, 11, -14, 15) == fp16(x)
        assert round_float(x, 24, -126, 127) == fp32(x)


def test_fp16_range() -> None:
    assert fp16(65504.0) == 65504.0
    assert fp16(65519.0) == 65504.0
    assert fp16(65520.0) == math.inf and fp16(-1e6) == -math.inf
    assert fp16(2.0 ** -24) == 2.0 ** -24  # smallest subnormal
    assert fp16(2.0 ** -25) == 0.0  # tie, rounds to the even neighbour 0
    assert fp16(2.0 ** -26) == 0.0
    assert ulp(1.0) == 2.0 ** -10 and ulp(0.75) == 2.0 ** -11


def test_update_below_half_an_ulp_is_lost_in_fp16() -> None:
    w = 1.0
    for _ in range(10):
        w = apply_update(w, 2.0 ** -12, fp16)
    assert w == 1.0
    # Just above half an ulp, the update rounds up to a full ulp.
    assert apply_update(1.0, 2.0 ** -11 + 2.0 ** -20, fp16) == 1.0 + 2.0 ** -10


def test_fp32_master_copy_keeps_the_small_updates() -> None:
    master = 1.0
    for _ in range(10):
        master = apply_update(master, 2.0 ** -12, fp32)
    assert master == 1.0 + 10 * 2.0 ** -12
    # The FP16 copy used by the next forward pass has moved by two ulps.
    assert fp16(master) == 1.0 + 2.0 ** -9 == 1.001953125


def test_ratio_2048_rule() -> None:
    # For a weight w that is a power of two, an update u with w / u >= 2048 is
    # lost. (k >= -3 keeps the update itself a normal FP16 number.)
    for k in range(-3, 12):
        w = 2.0 ** k
        assert apply_update(w, w / 2048, fp16) == w
        assert apply_update(w, w / 4096, fp16) == w
        assert apply_update(w, w / 2048 * 1.01, fp16) > w


def test_loss_scaling_rescues_an_underflowing_gradient() -> None:
    g = 2.0 ** -26
    assert fp16(g) == 0.0
    scale = 2.0 ** 10
    assert fp16(g * scale) == 2.0 ** -16
    assert fp32(fp16(g * scale) / scale) == g
    # BF16 has the exponent range of FP32, so it needs no scaling here.
    assert bf16(g) == g


def test_loss_scaling_in_the_backward_pass() -> None:
    batch = [([2.0 ** -12], 2.0 ** -20)] * 8
    _, g_plain = forward_backward([0.0], batch, 1.0)
    _, g_scaled = forward_backward([0.0], batch, 2.0 ** 12)
    assert g_plain == [0.0]
    assert g_scaled == [-(2.0 ** -19)]
    assert g_scaled[0] / 2.0 ** 12 == -(2.0 ** -31)


def test_bf16_has_range_but_little_precision() -> None:
    assert bf16(1.0 + 2.0 ** -8) == 1.0  # a tie, to even
    assert bf16(1.0 + 3 * 2.0 ** -9) == 1.0 + 2.0 ** -7
    assert bf16(3.0e38) < math.inf and fp16(3.0e38) == math.inf
    assert apply_update(1.0, 2.0 ** -9, bf16) == 1.0


def test_dynamic_scaler_halves_on_overflow_and_grows_after_n_clean_steps() -> None:
    s = DynamicLossScaler(scale=8.0, interval=3)
    s.overflow()
    assert s.scale == 4.0
    s.clean_step()
    s.clean_step()
    assert s.scale == 4.0
    s.overflow()  # resets the count of clean steps
    assert s.scale == 2.0
    for _ in range(2):
        s.clean_step()
    assert s.scale == 2.0
    s.clean_step()
    assert s.scale == 4.0 and s.clean == 0
    for _ in range(3):
        s.clean_step()
    assert s.scale == 8.0


def test_overflowing_steps_are_skipped() -> None:
    # Large residuals overflow FP16 at the first scales; those steps leave the
    # master weights unchanged and halve the scale until the gradient fits.
    batch = [([1.0, 1.0], 40.0)] * 4
    s = DynamicLossScaler(scale=2.0 ** 16, interval=1000)
    path, skipped = mixed_precision_sgd([0.0, 0.0], [batch] * 12, 0.01, s)
    assert skipped == list(range(len(skipped))) and len(skipped) >= 5
    for t in skipped:
        assert path[t + 1] == path[t] == [0.0, 0.0]
    assert s.scale == 2.0 ** (16 - len(skipped))
    assert path[-1][0] > 0 and path[-1] != path[len(skipped)]


def _problem(seed, steps):
    rng = random.Random(seed)
    target = [1.01, 0.99, 1.005]
    batches = []
    for _ in range(steps):
        b = []
        for _ in range(8):
            x = [rng.uniform(-1, 1) for _ in range(3)]
            b.append((x, sum(a * c for a, c in zip(target, x))))
        batches.append(b)
    return target, batches


def test_master_weights_train_where_fp16_weights_stall() -> None:
    target, batches = _problem(3, 400)
    w0 = [1.0, 1.0, 1.0]
    lr = 0.01  # every update is below half an ulp of 1.0 in FP16
    stalled = fp16_only_sgd(w0, batches, lr)
    assert all(w == w0 for w in stalled)
    path, skipped = mixed_precision_sgd(w0, batches, lr, DynamicLossScaler(interval=50))
    assert max(abs(a - b) for a, b in zip(path[-1], target)) < 2e-3


def test_mixed_precision_matches_float64_sgd() -> None:
    rng = random.Random(4)
    target = [0.75, -0.5, 0.25]
    batches = []
    for _ in range(300):
        b = []
        for _ in range(8):
            x = [rng.uniform(-1, 1) for _ in range(3)]
            b.append((x, sum(a * c for a, c in zip(target, x))))
        batches.append(b)
    lr = 0.05
    w = [0.0, 0.0, 0.0]
    for b in batches:
        g = [sum(2 * (sum(a * c for a, c in zip(w, x)) - y) * x[k] for x, y in b) / len(b) for k in range(3)]
        w = [a - lr * c for a, c in zip(w, g)]
    path, _ = mixed_precision_sgd([0.0, 0.0, 0.0], batches, lr, DynamicLossScaler(interval=50))
    assert max(abs(a - b) for a, b in zip(path[-1], w)) < 2e-3
