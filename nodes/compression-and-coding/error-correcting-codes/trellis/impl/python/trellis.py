# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/trellis/. The authors are listed in prov/ZSECMK.jsonl.

"""Code trellises for binary codes.

A trellis is a list of sections. Section i holds the edges from depth i to
depth i + 1; an edge is (from_state, bit, to_state). The paths from the root
(depth 0) to the toor (depth n) spell the codewords. Vectors are rows of bits;
a parity-check matrix is a list of rows, each row a list of 0 and 1.
"""

import itertools
from typing import Dict, Iterator, List, Sequence, Set, Tuple

Edge = Tuple[int, int, int]
Trellis = List[List[Edge]]


def _columns(h: Sequence[Sequence[int]]) -> List[int]:
    """Column j of H as an integer, bit r for row r."""
    return [sum(row[j] << r for r, row in enumerate(h)) for j in range(len(h[0]))]


def syndrome_trellis(h: Sequence[Sequence[int]]) -> Trellis:
    """The Wolf (BCJR) trellis of the code with parity-check matrix H.

    The state at depth i is the partial syndrome c_1 h_1 + ... + c_i h_i. A
    forward pass keeps the states that the root reaches, and a backward pass
    keeps the states that reach syndrome 0 at depth n. Cost: O(n 2^(n-k)).
    """
    cols = _columns(h)
    n = len(cols)
    fwd: List[Set[int]] = [{0}]
    for j in range(n):
        fwd.append({s ^ (b * cols[j]) for s in fwd[j] for b in (0, 1)})
    back: List[Set[int]] = [set() for _ in range(n + 1)]
    back[n] = {0}
    for j in range(n - 1, -1, -1):
        back[j] = {s for s in fwd[j] if s in back[j + 1] or (s ^ cols[j]) in back[j + 1]}
    sections: Trellis = []
    for j in range(n):
        sec = []
        for s in sorted(back[j]):
            for b in (0, 1):
                t = s ^ (b * cols[j])
                if t in back[j + 1]:
                    sec.append((s, b, t))
        sections.append(sec)
    return sections


def state_profile(t: Trellis) -> List[int]:
    """The number of states at each depth 0 .. n."""
    prof = [len({e[0] for e in sec}) for sec in t]
    return prof + [len({e[2] for e in t[-1]})] if t else [1]


def paths(t: Trellis, start: int = 0, end: int = 0) -> Iterator[Tuple[int, ...]]:
    """All label sequences of paths from state start at depth 0 to state end
    at depth n. Iterative depth-first search; exponential output."""
    out: Dict[int, List[Tuple[int, ...]]] = {start: [()]}
    for sec in t:
        nxt: Dict[int, List[Tuple[int, ...]]] = {}
        for s, b, u in sec:
            for p in out.get(s, []):
                nxt.setdefault(u, []).append(p + (b,))
        out = nxt
    yield from out.get(end, [])


def codewords_from_generator(g: Sequence[Sequence[int]]) -> Set[Tuple[int, ...]]:
    """All 2^k codewords m G, by brute force."""
    n = len(g[0])
    words = set()
    for m in itertools.product((0, 1), repeat=len(g)):
        words.add(tuple(sum(m[r] * g[r][j] for r in range(len(g))) % 2 for j in range(n)))
    return words


def minimal_profile(words: Set[Tuple[int, ...]]) -> List[int]:
    """State counts of the minimal trellis: 2^(k - k_past(i) - k_future(i)),
    where k_past(i) is the dimension of the subcode that is zero after
    position i and k_future(i) of the subcode that is zero before it."""
    n = len(next(iter(words)))
    k = len(words).bit_length() - 1
    prof = []
    for i in range(n + 1):
        past = sum(1 for c in words if not any(c[i:]))
        fut = sum(1 for c in words if not any(c[:i]))
        prof.append(2 ** (k - (past.bit_length() - 1) - (fut.bit_length() - 1)))
    return prof


def convolutional_trellis(gens: Sequence[int], k: int, length: int, terminate: bool = True, all_starts: bool = False) -> Trellis:
    """The trellis of a rate 1/n feedforward convolutional code over length
    input steps, plus K - 1 tail steps if terminate. Each step has n output
    bits, so it is drawn as n sections of one bit; the inner states are
    (state, input, place) codes that keep the trellis bit-wise."""
    def step(state: int, u: int) -> Tuple[int, Tuple[int, ...]]:
        w = (u << (k - 1)) | state
        return w >> 1, tuple(bin(g & w).count("1") & 1 for g in gens)

    nsec = len(gens)
    secs: Trellis = []
    states = set(range(2 ** (k - 1))) if all_starts else {0}
    total = length + (k - 1 if terminate else 0)
    for t in range(total):
        inputs = (0,) if t >= length else (0, 1)
        group: List[List[Edge]] = [[] for _ in range(nsec)]
        nxt = set()
        for s in sorted(states):
            for u in inputs:
                ns, out = step(s, u)
                node = s
                for j in range(nsec):
                    to = ns if j == nsec - 1 else (1 << 40) + (s << 2 | u) * 16 + j
                    group[j].append((node, out[j], to))
                    node = to
                nxt.add(ns)
        secs.extend(group)
        states = nxt
    return secs


def tail_biting_paths(gens: Sequence[int], k: int, length: int) -> Set[Tuple[int, ...]]:
    """Codewords of the tail-biting code: paths that start and end in the
    same state, with no tail steps."""
    t = convolutional_trellis(gens, k, length, terminate=False, all_starts=True)
    words: Set[Tuple[int, ...]] = set()
    for s in range(2 ** (k - 1)):
        words.update(paths(t, s, s))
    return words
