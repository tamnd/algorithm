# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/viterbi-equalizer/. The authors are listed in prov/8TQVP4.jsonl.

"""The Viterbi equalizer: maximum likelihood sequence detection on an ISI channel.

The model is Forney's: y[k] = sum_{l=0}^{L-1} f[l] x[k-l] + n[k] with white
Gaussian noise, for example the output of a whitened matched filter. The state
at time k is the last L-1 symbols (x[k-1], ..., x[k-L+1]), so there are
M^(L-1) states and M branches leave each state. The branch metric is
|y[k] - sum_l f[l] x[k-l]|^2. The search over the trellis is the Viterbi
algorithm; this file only builds the ISI trellis and its metric.

A state is an integer s = i1 + M i2 + ... + M^(L-2) i_{L-1}, where i_t is the
alphabet index of x[k-t]. The symbol with index i0 moves s to
i0 + M (s mod M^(L-2)).
"""

import itertools


def _next_state(s: int, i0: int, m: int, mem: int) -> int:
    if mem == 0:
        return 0
    return i0 + m * (s % (m ** (mem - 1)))


def _state_of(symbols: list[int], m: int) -> int:
    """The state for the indices (i1, i2, ...) of the most recent symbols first."""
    s = 0
    for t, i in enumerate(symbols):
        s += i * m ** t
    return s


def viterbi_equalize(y: list[complex], f: list[complex], alphabet: list[complex], pre: list[complex] | None = None, tail: list[complex] | None = None) -> list[complex]:
    """The maximum likelihood sequence for y on the channel f.

    pre holds the L-1 known symbols before x[0], oldest first (zeros if absent).
    tail holds known symbols after the unknown ones; y covers the unknown symbols
    and then the tail. Returns the decisions on the len(y) - len(tail) unknown
    symbols.
    """
    m, mem = len(alphabet), len(f) - 1
    pre = list(pre) if pre is not None else [0j] * mem
    tail = list(tail) if tail is not None else []
    if len(pre) != mem:
        raise ValueError("pre must hold L-1 symbols")
    n = len(y) - len(tail)
    if n < 0:
        raise ValueError("y is shorter than the tail")
    index = {complex(a): i for i, a in enumerate(alphabet)}
    for v in tail:
        if complex(v) not in index:
            raise ValueError("tail symbols must be in the alphabet")
    states = m ** mem  # @line L1

    def out(s: int, i0: int, k: int) -> complex:
        # the noiseless output at time k for state s and new symbol i0; before x[0] the known pre symbols
        acc = f[0] * alphabet[i0]
        for t in range(1, mem + 1):
            if k - t >= 0:
                acc += f[t] * alphabet[(s // m ** (t - 1)) % m]
            else:
                acc += f[t] * pre[mem + (k - t)]
        return acc

    # for k >= L-1 the output depends only on (s, i0), so it is computed once: O(L M^L)
    steady = [[out(s, i0, mem) for i0 in range(m)] for s in range(states)]
    inf = float("inf")
    metric = [inf] * states
    metric[0] = 0.0  # @line L2
    back: list[list[tuple[int, int]]] = []
    for k in range(len(y)):  # @line L3
        new = [inf] * states
        ptr = [(-1, -1)] * states
        choices = range(m) if k < n else [index[complex(tail[k - n])]]
        for s in range(states):
            if metric[s] == inf:
                continue
            for i0 in choices:  # @line L4
                d = abs(y[k] - (steady[s][i0] if k >= mem else out(s, i0, k))) ** 2  # @line L5
                t = _next_state(s, i0, m, mem)
                cand = metric[s] + d
                if cand < new[t]:  # @line L6
                    new[t] = cand
                    ptr[t] = (s, i0)
        metric = new
        back.append(ptr)
    s = min(range(states), key=lambda q: metric[q])  # @line L7
    path = []
    for k in range(len(y) - 1, -1, -1):  # @line L8
        prev, i0 = back[k][s]
        path.append(alphabet[i0])
        s = prev
    path.reverse()
    return path[:n]  # @line L9


def sequence_metric(y: list[complex], f: list[complex], x: list[complex], pre: list[complex] | None = None) -> float:
    """sum_k |y[k] - sum_l f[l] x[k-l]|^2 over k = 0..len(y)-1, with x[k] for k < 0 from pre."""
    mem = len(f) - 1
    pre = list(pre) if pre is not None else [0j] * mem
    full = pre + list(x)
    total = 0.0
    for k in range(len(y)):
        acc = sum(f[l] * full[mem + k - l] for l in range(len(f)))
        total += abs(y[k] - acc) ** 2
    return total


def brute_force(y: list[complex], f: list[complex], alphabet: list[complex], pre: list[complex] | None = None, tail: list[complex] | None = None) -> list[complex]:
    """The ML sequence by trying all M^n sequences (for tests)."""
    tail = list(tail) if tail is not None else []
    n = len(y) - len(tail)
    best, arg = float("inf"), None
    for cand in itertools.product(alphabet, repeat=n):
        v = sequence_metric(y, f, list(cand) + tail, pre)
        if v < best:
            best, arg = v, list(cand)
    return arg


def min_distance_bpsk(f: list[float], max_len: int = 12) -> float:
    """The minimum squared distance between two BPSK (+-1) sequences through f.

    It is the minimum of ||f * e||^2 over error sequences e with e[0] != 0 and
    entries in {-2, 0, 2}, searched up to length max_len with pruning.
    """
    best = 4 * sum(abs(v) ** 2 for v in f)  # a single error: the matched filter bound
    mem = len(f) - 1

    def grow(e: list[int], acc: float) -> None:
        nonlocal best
        if acc >= best:
            return
        # close the event: the outputs after the last error symbol
        tail = 0.0
        for k in range(len(e), len(e) + mem):
            tail += abs(sum(f[l] * e[k - l] for l in range(len(f)) if 0 <= k - l < len(e))) ** 2
        if e[-1] != 0 and acc + tail < best:
            best = acc + tail
        if len(e) >= max_len:
            return
        for v in (-2, 0, 2):
            e2 = e + [v]
            k = len(e2) - 1
            out = sum(f[l] * e2[k - l] for l in range(len(f)) if k - l >= 0)
            grow(e2, acc + abs(out) ** 2)

    grow([2], abs(f[0] * 2) ** 2)
    return best
