# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/warp-aggregated-atomics/. The authors are listed in prov/714B67.jsonl.
"""Warp-aggregated atomics on a small SIMT simulator.

A warp is a list of 32 lanes that run in lockstep.  The warp intrinsics
__ballot_sync, __popc, __ffs, __shfl_sync and __match_any_sync are modelled on
lists of lane values.  Global atomics act on a shared counter object that
counts its calls.  Warps run in an order that a seeded random generator picks,
because the hardware gives no order between warps.

The CUDA code on the page is not run by these tests.
"""

WARP = 32
FULL = (1 << WARP) - 1


class Counter:
    """A global int with atomicAdd. It counts the atomic operations it serves."""

    def __init__(self, value=0):
        self.value = value
        self.atomics = 0

    def atomic_add(self, v):
        old = self.value
        self.value += v
        self.atomics += 1
        return old


def ballot(preds):
    """__ballot_sync(FULL, pred): bit i is set when lane i has a true predicate."""
    m = 0
    for lane, p in enumerate(preds):
        if p:
            m |= 1 << lane
    return m


def popc(m):
    return bin(m).count("1")


def ffs(m):
    """__ffs: 1 + the index of the lowest set bit, or 0 when m is 0."""
    return (m & -m).bit_length()


def shfl(values, src):
    """__shfl_sync: every lane gets the value of lane src."""
    return [values[src]] * len(values)


def match_any(keys, active):
    """__match_any_sync: for each active lane, the mask of active lanes with the same key."""
    out = []
    for i, k in enumerate(keys):
        out.append(sum(1 << j for j, kj in enumerate(keys) if active[j] and kj == k) if active[i] else 0)
    return out


def _warps(n, rng):
    order = list(range(0, n, WARP))
    rng.shuffle(order)
    return order


def filter_per_thread(data, pred, rng):
    """Stream compaction where every passing thread does its own atomicAdd."""
    out = [None] * len(data)
    ctr = Counter()
    jobs = [i for w in _warps(len(data), rng) for i in range(w, min(len(data), w + WARP))]
    rng.shuffle(jobs)                      # atomics from all threads in any order
    for i in jobs:
        if pred(data[i]):
            out[ctr.atomic_add(1)] = data[i]
    return out[:ctr.value], ctr.atomics


def filter_warp_aggregated(data, pred, rng):
    """Stream compaction with one atomicAdd per warp that has a passing lane."""
    out = [None] * len(data)
    ctr = Counter()
    for w in _warps(len(data), rng):
        lanes = list(range(w, min(len(data), w + WARP)))
        p = [pred(data[i]) for i in lanes]
        mask = ballot(p)                                  # @line L1
        if mask == 0:
            continue
        leader = ffs(mask) - 1                            # @line L2
        base = [None] * len(lanes)
        base[leader] = ctr.atomic_add(popc(mask))         # @line L3: only the leader
        base = shfl(base, leader)                         # @line L4
        for lane, i in enumerate(lanes):
            if p[lane]:
                rank = popc(mask & ((1 << lane) - 1))     # @line L5
                out[base[lane] + rank] = data[i]          # @line L6
    return out[:ctr.value], ctr.atomics


def histogram_per_thread(keys, bins, rng):
    hist = [Counter() for _ in range(bins)]
    order = list(range(len(keys)))
    rng.shuffle(order)
    for i in order:
        hist[keys[i]].atomic_add(1)
    return [h.value for h in hist], sum(h.atomics for h in hist)


def histogram_match_any(keys, bins, rng):
    """Aggregation by key: lanes with the same bin elect one leader with __match_any_sync."""
    hist = [Counter() for _ in range(bins)]
    for w in _warps(len(keys), rng):
        ks = keys[w:w + WARP]
        active = [True] * len(ks)
        peers = match_any(ks, active)
        for lane, m in enumerate(peers):
            if ffs(m) - 1 == lane:                       # the lowest lane of its group
                hist[ks[lane]].atomic_add(popc(m))
    return [h.value for h in hist], sum(h.atomics for h in hist)


def expected_aggregated_atomics(n, q):
    """Expected warps with a passing lane when each item passes with probability q (n a multiple of 32)."""
    return (n // WARP) * (1 - (1 - q) ** WARP)
