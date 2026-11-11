# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/uniquely-decodable-code/. The authors are listed in prov/JYNM78.jsonl.
"""Classes of codes, and the Sardinas-Patterson test for unique decodability."""

from collections import deque
from typing import Sequence


def is_nonsingular(code: Sequence[str]) -> bool:
    """Distinct symbols get distinct codewords."""
    return len(set(code)) == len(code)


def is_prefix(code: Sequence[str]) -> bool:
    """No codeword is a prefix of another codeword."""
    if not is_nonsingular(code):
        return False
    return not any(a != b and b.startswith(a) for a in code for b in code)


def sardinas_patterson(code: Sequence[str]) -> tuple[bool, str | None]:
    """Decide if the code is uniquely decodable. Return (True, None) or (False, an ambiguous string).

    A dangling suffix w is reached with two codeword sequences A and B where
    concat(A) = concat(B) + w. The sets S_1, S_2, ... of the test are the
    suffixes reached in 1, 2, ... steps; their union is the closure computed
    here by breadth-first search. The code is uniquely decodable exactly when no
    reachable dangling suffix is a codeword.
    """
    words = list(code)
    if any(w == "" for w in words):
        return False, ""  # the empty codeword makes any string ambiguous
    if not is_nonsingular(words):
        dup = next(w for w in words if words.count(w) > 1)
        return False, dup
    cw = set(words)
    # parent[w] = (ahead, behind): two parses with concat(ahead) = concat(behind) + w.
    parent: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {}
    queue: deque[str] = deque()
    for u in words:
        for v in words:
            if u != v and v.startswith(u):
                w = v[len(u):]
                if w not in parent:
                    parent[w] = ((v,), (u,))
                    queue.append(w)
    while queue:
        w = queue.popleft()
        ahead, behind = parent[w]
        if w in cw:
            # behind + w is a second parse of concat(ahead).
            return False, "".join(ahead)
        for c in words:
            if w.startswith(c):  # c is a proper prefix of w (c != w here)
                nxt, pair = w[len(c):], (ahead, behind + (c,))
            elif c.startswith(w):  # w is a proper prefix of c: the other parse moves ahead
                nxt, pair = c[len(w):], (behind + (c,), ahead)
            else:
                continue
            if nxt not in parent:
                parent[nxt] = pair
                queue.append(nxt)
    return True, None


def is_uniquely_decodable(code: Sequence[str]) -> bool:
    return sardinas_patterson(code)[0]


def parses(s: str, code: Sequence[str], limit: int = 2) -> list[list[int]]:
    """Up to `limit` ways to write s as a concatenation of codewords (indices into code)."""
    out: list[list[int]] = []

    def go(i: int, acc: list[int]) -> None:
        if len(out) >= limit:
            return
        if i == len(s):
            out.append(acc[:])
            return
        for j, c in enumerate(code):
            if c and s.startswith(c, i):
                acc.append(j)
                go(i + len(c), acc)
                acc.pop()

    go(0, [])
    return out


def brute_force_ambiguous(code: Sequence[str], max_len: int) -> str | None:
    """The shortest string of length at most max_len with two parses, or None.

    Dynamic programming: count the parses of every binary string up to max_len by
    extending parsed strings with one codeword at a time.
    """
    if not is_nonsingular(code):
        return min((w for w in code if list(code).count(w) > 1), key=len)
    count: dict[str, int] = {"": 1}
    for length in range(1, max_len + 1):
        for c in code:
            if 0 < len(c) <= length:
                for s, k in list(count.items()):
                    if len(s) == length - len(c):
                        t = s + c
                        count[t] = count.get(t, 0) + k
        hits = sorted(s for s, k in count.items() if len(s) == length and k > 1)
        if hits:
            return hits[0]
    return None
