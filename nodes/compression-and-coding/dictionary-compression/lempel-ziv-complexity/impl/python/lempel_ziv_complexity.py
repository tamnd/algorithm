# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lempel-ziv-complexity/. The authors are listed in prov/EXZCS6.jsonl.

"""Lempel-Ziv (1976) complexity c(n) of a finite sequence.

The code computes the number of components of the exhaustive production
history of Lempel and Ziv (1976). A component that starts at position i is
the shortest t[i .. j] that is not a substring of t[0 .. j-1]; that is, the
longest prefix of t[i ..] with an occurrence that starts before i (it may
overlap the component), plus one new symbol. The last component may end
with the text and then has no new symbol.

Three ways to get the same number:
  * components(): the definition, with substring search;
  * kaspar_schuster(): the loop of Kaspar and Schuster (1987), with no
    substring search, in O(n^2) symbol comparisons in the worst case;
  * min_history(): the smallest number of components over all production
    histories, by dynamic programming (an oracle for small inputs).
"""

import math


def components(t) -> list:
    """The exhaustive history, as a list of slices of t."""
    n, out, i = len(t), [], 0
    while i < n:
        length = 0
        # t[i : i+L+1] has an occurrence that starts before i exactly when
        # it is a substring of t[: i+L].
        while i + length < n and _occurs(t, t[i:i + length + 1], i + length):
            length += 1
        end = min(n, i + length + 1)
        out.append(t[i:end])
        i = end
    return out


def _occurs(t, piece, limit: int) -> bool:
    if isinstance(t, (str, bytes)):
        return t.find(piece, 0, limit) >= 0
    k = len(piece)
    return any(list(t[s:s + k]) == list(piece) for s in range(limit - k + 1))


def lz76_complexity(t) -> int:
    """c(n), the number of components of the exhaustive history."""
    return len(components(t))


def kaspar_schuster(t) -> int:
    """c(n) by the scan of Kaspar and Schuster (1987).

    u is the start of the current component, i the start of the earlier
    copy that is tried, v - 1 the length matched so far and vmax - 1 the
    longest match over all i. The text is indexed from 1 inside the loop.
    """
    n = len(t)
    if n == 0:
        return 0
    s = [None] + list(t)
    i, c, u, v, vmax = 0, 1, 1, 1, 1
    while u + v <= n:
        if s[i + v] == s[u + v]:
            v += 1
        else:
            vmax = max(v, vmax)
            i += 1
            if i == u:  # all earlier starts tried: the component has length vmax
                c += 1
                u += vmax
                v, i, vmax = 1, 0, 1
            else:
                v = 1
    if v != 1:  # the last component reached the end of the text during a match
        c += 1
    return c


def min_history(t) -> int:
    """Smallest number of components of a production history of t.

    A history cuts t into components; each component is a copy (an
    occurrence that starts earlier, overlap allowed) followed by one symbol,
    and the last component may be a copy only. O(n^3) or more: an oracle.
    """
    n = len(t)
    inf = float("inf")
    best = [inf] * (n + 1)
    best[0] = 0
    for i in range(n):
        if best[i] == inf:
            continue
        for end in range(i + 1, n + 1):
            copy = end - i - 1  # all but the last symbol is a copy
            ok = copy == 0 or any(t[s:s + copy] == t[i:i + copy] for s in range(i))
            if not ok:
                break  # longer copies do not occur either
            best[end] = min(best[end], best[i] + 1)
        # The last component may be a pure copy of t[i:].
        if i > 0 and any(t[s:s + n - i] == t[i:] for s in range(i)):
            best[n] = min(best[n], best[i] + 1)
    return int(best[n])


def normalized(t, k: int = 2) -> float:
    """c(n) log_k(n) / n, the measure compared with the entropy rate in base k."""
    n = len(t)
    if n <= 1:
        return float(n)
    return lz76_complexity(t) * math.log(n, k) / n


def upper_bound(n: int, k: int = 2) -> float:
    """The bound of Lempel and Ziv (1976): c(n) < n / ((1 - eps_n) log_k n), for n >= 2.

    eps_n = 2 (1 + log_k log_k (k n)) / log_k n. The bound is only meaningful
    when eps_n < 1, that is, for large n.
    """
    lg = math.log(n, k)
    eps = 2 * (1 + math.log(math.log(k * n, k), k)) / lg
    return n / ((1 - eps) * lg) if eps < 1 else math.inf
