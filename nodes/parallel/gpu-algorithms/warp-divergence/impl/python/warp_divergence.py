# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/warp-divergence/.
"""Cost of divergent control flow in the SIMT model.

Each thread produces the list of instruction labels that it runs. The lanes of one warp that run
the same label run it together, under an active mask, in one issue. So the warp issues one
instruction for each distinct label among its lanes: a branch costs the sum of the paths that
some lane takes, and a loop costs the largest trip count among the lanes.
"""

WARP = 32


def warp_issues(traces):
    """traces[l] is the list of labels of lane l. Returns (issued, lane instructions, masks)."""
    masks = {}
    for lane, tr in enumerate(traces):
        for label in tr:
            masks[label] = masks.get(label, 0) | (1 << lane)
    issued = len(masks)
    lanes = sum(len(tr) for tr in traces)
    return issued, lanes, masks


def kernel_issues(n, thread_trace):
    """Sum of warp_issues over the warps of n threads, thread_trace(i) gives the labels of thread i."""
    issued = lanes = 0
    for w in range(-(-n // WARP)):
        traces = [thread_trace(i) for i in range(w * WARP, min(n, (w + 1) * WARP))]
        a, b, _ = warp_issues(traces)
        issued, lanes = issued + a, lanes + b
    return issued, lanes


def branch(cond_of, then_len, else_len):
    """if (cond) { then_len instructions } else { else_len instructions }, then one after."""
    def trace(i):
        body = [("then", j) for j in range(then_len)] if cond_of(i) else [("else", j) for j in range(else_len)]
        return ["cond"] + body + ["after"]
    return trace


def loop(trips_of, body_len=1):
    """for (j = 0; j < trips(i); j++) { body }: each trip also runs the loop test."""
    def trace(i):
        t = trips_of(i)
        out = []
        for j in range(t):
            out += [("test", j)] + [("body", j, k) for k in range(body_len)]
        return out + [("test", t)]
    return trace


def tree_reduction_issues(T, interleaved):
    """Warp issues of the add in each level of a shared-memory tree sum over a block of T threads.

    interleaved:  if (tid % (2 * s) == 0) s[tid] += s[tid + s];  for s = 1, 2, 4, ...
    sequential:   if (tid < s) s[tid] += s[tid + s];             for s = T/2, T/4, ..., 1
    Returns (warp issues of the add, adds).
    """
    levels = []
    s = 1
    while s < T:
        levels.append(s)
        s *= 2
    issues = adds = 0
    for s in levels:
        if interleaved:
            active = [t for t in range(T) if t % (2 * s) == 0]
        else:
            active = list(range(T // (2 * s)))  # the same number of adds, packed at the front
        issues += len({t // WARP for t in active})
        adds += len(active)
    return issues, adds
