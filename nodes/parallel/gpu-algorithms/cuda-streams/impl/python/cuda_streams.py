# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cuda-streams/. The authors are listed in prov/GVJ1ZR.jsonl.
"""A model of CUDA streams on a GPU with copy engines and one compute engine.

Each operation has a stream, a kind ("h2d", "kernel" or "d2h") and a duration.
Operations in one stream run in issue order.  Each engine takes the operations
sent to it in issue order (a FIFO queue), which is how GPUs without multiple
hardware queues behave; it is a simplification for newer GPUs.  A kernel is
assumed to fill the GPU, so kernels do not run at the same time.  Times are
Fractions.  No CUDA code is run.
"""
from fractions import Fraction as F


def engine_of(kind, copy_engines):
    if kind == "kernel":
        return "compute"
    if copy_engines >= 2:
        return kind
    return "copy"


def simulate(ops, copy_engines=2):
    """ops: list of (stream, kind, duration) in issue order. Returns [(start, end)] per op."""
    stream_end = {}
    engine_end = {}
    out = []
    for stream, kind, dur in ops:
        e = engine_of(kind, copy_engines)
        s = max(stream_end.get(stream, F(0)), engine_end.get(e, F(0)))
        t = s + F(dur)
        stream_end[stream] = t
        engine_end[e] = t
        out.append((s, t))
    return out


def makespan(ops, copy_engines=2):
    times = simulate(ops, copy_engines)
    return max(t for _, t in times) if times else F(0)


def chunked_ops(m, h, k, d, order="depth", overhead=0):
    """Split a job (total copy-in h, kernel k, copy-out d) into m chunks, one stream each.

    order="depth": for each chunk issue h2d, kernel, d2h.
    order="breadth": issue all h2d, then all kernels, then all d2h.
    overhead is a fixed time added to every operation.
    """
    h, k, d = F(h) / m + overhead, F(k) / m + overhead, F(d) / m + overhead
    steps = [("h2d", h), ("kernel", k), ("d2h", d)]
    if order == "depth":
        return [(c, kind, t) for c in range(m) for kind, t in steps]
    return [(c, kind, t) for kind, t in steps for c in range(m)]


def pipeline_time(m, h, k, d, overhead=0):
    """Closed form for order="depth" with two copy engines: first chunk, then m-1 bottleneck stages."""
    o = F(overhead)
    st = [F(h) / m + o, F(k) / m + o, F(d) / m + o]
    return sum(st) + (m - 1) * max(st)


def best_chunks(h, k, d, overhead, m_max):
    return min(range(1, m_max + 1), key=lambda m: (pipeline_time(m, h, k, d, overhead), m))
