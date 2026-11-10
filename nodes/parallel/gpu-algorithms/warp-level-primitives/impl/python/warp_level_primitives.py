# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/warp-level-primitives/.
"""Warp-level primitives on a simulated warp of 32 lanes.

A warp value is a list of 32 per-lane values. Each primitive takes the member mask and returns a
new list with the result of each lane in the mask (None for lanes outside the mask). The rules
follow the CUDA Programming Guide v13.5, Section 5.4.6: a lane may read only from lanes in the mask,
width is a power of 2 up to 32, and the lanes form segments of `width` consecutive lanes.
"""

WARP = 32
FULL = (1 << WARP) - 1


def _lanes(mask):
    return [l for l in range(WARP) if mask >> l & 1]


def _check_width(width):
    assert 1 <= width <= WARP and width & (width - 1) == 0


def _read(var, mask, src):
    assert mask >> src & 1, "a lane reads from a lane that is not in the mask"
    return var[src]


def shfl(mask, var, src_lane, width=WARP):
    """__shfl_sync: every lane reads lane src_lane % width of its own segment."""
    _check_width(width)
    out = [None] * WARP
    for l in _lanes(mask):
        base = l - l % width
        s = src_lane[l] if isinstance(src_lane, list) else src_lane
        out[l] = _read(var, mask, base + s % width)
    return out


def shfl_up(mask, var, delta, width=WARP):
    """__shfl_up_sync: read lane l - delta; lanes below delta in their segment keep their value."""
    _check_width(width)
    out = [None] * WARP
    for l in _lanes(mask):
        out[l] = var[l] if l % width < delta else _read(var, mask, l - delta)
    return out


def shfl_down(mask, var, delta, width=WARP):
    """__shfl_down_sync: read lane l + delta; lanes whose source leaves the segment keep their value."""
    _check_width(width)
    out = [None] * WARP
    for l in _lanes(mask):
        out[l] = var[l] if l % width + delta >= width else _read(var, mask, l + delta)
    return out


def shfl_xor(mask, var, lane_mask, width=WARP):
    """__shfl_xor_sync: read lane l ^ lane_mask; a source in a later segment gives the own value."""
    _check_width(width)
    out = [None] * WARP
    for l in _lanes(mask):
        src = l ^ lane_mask
        out[l] = var[l] if src // width > l // width else _read(var, mask, src)
    return out


def ballot(mask, pred):
    """__ballot_sync: bit l is set when lane l is in the mask and its predicate is true."""
    return sum(1 << l for l in _lanes(mask) if pred[l])


def any_sync(mask, pred):
    return ballot(mask, pred) != 0


def all_sync(mask, pred):
    return ballot(mask, pred) == mask


def match_any(mask, var):
    """__match_any_sync: for each lane, the mask of lanes in the mask with an equal value."""
    out = [None] * WARP
    for l in _lanes(mask):
        out[l] = sum(1 << k for k in _lanes(mask) if var[k] == var[l])
    return out


def match_all(mask, var):
    """__match_all_sync: (mask, True) when all lanes in the mask hold the same value, else (0, False)."""
    vals = {var[l] for l in _lanes(mask)}
    return (mask, True) if len(vals) == 1 else (0, False)


def reduce_add(mask, var):
    """__reduce_add_sync for integers: every lane in the mask gets the sum over the mask."""
    s = sum(var[l] for l in _lanes(mask))
    return [s if mask >> l & 1 else None for l in range(WARP)]


def popc(x):
    return bin(x).count("1")


# ---------------------------------------------------------------- algorithms in log2(32) = 5 steps


def warp_reduce_down(var, op=lambda a, b: a + b):
    """Tree reduction with shfl_down and offsets 16, 8, 4, 2, 1. Lane 0 holds the result."""
    v, steps = list(var), 0
    offset = WARP // 2
    while offset > 0:
        other = shfl_down(FULL, v, offset)
        v = [op(a, b) for a, b in zip(v, other)]  # lanes past the end combine junk; lane 0 is right
        offset //= 2
        steps += 1
    return v[0], steps


def warp_allreduce_xor(var, op=lambda a, b: a + b):
    """Butterfly reduction with shfl_xor and masks 16, 8, 4, 2, 1. Every lane holds the result."""
    v, steps = list(var), 0
    m = WARP // 2
    while m > 0:
        other = shfl_xor(FULL, v, m)
        v = [op(a, b) for a, b in zip(v, other)]
        m //= 2
        steps += 1
    return v, steps


def warp_inclusive_scan(var, op=lambda a, b: a + b):
    """Hillis-Steele scan with shfl_up and offsets 1, 2, 4, 8, 16."""
    v, steps = list(var), 0
    offset = 1
    while offset < WARP:
        other = shfl_up(FULL, v, offset)
        v = [op(other[l], v[l]) if l >= offset else v[l] for l in range(WARP)]
        offset *= 2
        steps += 1
    return v, steps


def warp_compact_offsets(pred):
    """Each lane with a true predicate gets its output slot: the number of true lanes below it."""
    b = ballot(FULL, pred)
    slots = [popc(b & ((1 << l) - 1)) if pred[l] else None for l in range(WARP)]
    return slots, popc(b)
