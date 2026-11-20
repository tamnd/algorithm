# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reduced-state-sequence-estimation/. The authors are listed in prov/J2DFVA.jsonl.

"""Reduced-state sequence estimation (Eyuboglu and Qureshi) on an ISI channel.

The channel is y[k] = sum_{l=0}^{L-1} f[l] x[k-l] + n[k] with white noise, for
example the minimum-phase output of a whitened matched filter. The full Viterbi
equalizer has M^(L-1) states. RSSE chooses K <= L-1 partitions of the alphabet:
partition i splits it into J_i subsets, and partition i must refine partition
i+1 (so J_1 >= J_2 >= ... >= J_K). The state at time k is the tuple of subset
labels (label_1(x[k-1]), ..., label_K(x[k-K])), so there are J_1 J_2 ... J_K
states. Each survivor keeps its own symbol history, and the ISI of the symbols
that the state does not hold comes from that history (decision feedback per
survivor). Symbols with the same label_1 are parallel branches; the best one is
kept.

Special cases: every J_i = M gives the full Viterbi equalizer (exact ML);
J_1 = ... = J_mu = M and K = mu gives DDFSE (Duel-Hallen and Heegard) with M^mu
states; K = 0 gives one state, the zero-forcing DFE on f.
"""


def check_partitions(parts: list[list[int]], m: int) -> list[int]:
    """Check the labels and the nesting; return J_1, ..., J_K."""
    sizes = []
    for p in parts:
        if len(p) != m or sorted(set(p)) != list(range(len(set(p)))):
            raise ValueError("a partition labels each point with 0..J-1")
        sizes.append(len(set(p)))
    for i in range(len(parts) - 1):
        # partition i must refine partition i+1: the same label in i means the same label in i+1
        seen: dict[int, int] = {}
        for a in range(m):
            if seen.setdefault(parts[i][a], parts[i + 1][a]) != parts[i + 1][a]:
                raise ValueError("each partition must refine the next one")
    return sizes


def ddfse_partitions(m: int, mu: int) -> list[list[int]]:
    """The DDFSE choice: the first mu symbols are kept in full."""
    return [list(range(m)) for _ in range(mu)]


def rsse(y: list[complex], f: list[complex], alphabet: list[complex], parts: list[list[int]], pre: list[complex] | None = None) -> list[complex]:
    """The RSSE decisions for y on the channel f with the given partitions.

    pre holds the L-1 known symbols before x[0], oldest first.
    """
    m, mem = len(alphabet), len(f) - 1
    if len(parts) > mem:
        raise ValueError("at most L-1 partitions")
    check_partitions(parts, m)
    pre = list(pre) if pre is not None else [alphabet[0]] * mem
    if len(pre) != mem:
        raise ValueError("pre must hold L-1 symbols")
    index = {complex(a): i for i, a in enumerate(alphabet)}
    hist0 = tuple(index[complex(v)] for v in reversed(pre))  # most recent first

    def state_of(hist: tuple[int, ...]) -> tuple[int, ...]:
        return tuple(parts[i][hist[i]] for i in range(len(parts)))

    # each survivor: state -> (metric, last mem symbol indices, most recent first)
    surv = {state_of(hist0): (0.0, hist0)}  # @line L1
    back: list[dict] = []
    for k in range(len(y)):  # @line L2
        new: dict[tuple[int, ...], tuple[float, tuple[int, ...]]] = {}
        ptr: dict[tuple[int, ...], tuple[tuple[int, ...], int]] = {}
        for t, (met, hist) in surv.items():
            isi = sum(f[l] * alphabet[hist[l - 1]] for l in range(1, mem + 1))  # @line L3
            for i0 in range(m):  # @line L4
                d = abs(y[k] - f[0] * alphabet[i0] - isi) ** 2  # @line L5
                h2 = ((i0,) + hist)[:mem]
                t2 = state_of(h2)  # @line L6
                if t2 not in new or met + d < new[t2][0]:  # @line L7
                    new[t2] = (met + d, h2)
                    ptr[t2] = (t, i0)
        surv = new
        back.append(ptr)
    t = min(surv, key=lambda q: surv[q][0])  # @line L8
    out = []
    for k in range(len(y) - 1, -1, -1):
        t, i0 = back[k][t][0], back[k][t][1]
        out.append(alphabet[i0])
    out.reverse()
    return out  # @line L9


def number_of_states(parts: list[list[int]]) -> int:
    n = 1
    for p in parts:
        n *= len(set(p))
    return n
