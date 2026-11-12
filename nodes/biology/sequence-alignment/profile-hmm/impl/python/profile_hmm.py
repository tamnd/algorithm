# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/profile-hmm/. The authors are listed in prov/MM4SQ5.jsonl.
"""A global profile HMM in the form of Durbin et al. (1998), Chapter 5.

There are m match states M1..Mm, insert states I0..Im and delete states D1..Dm,
with Begin = M0 and End = M(m+1). A state of node k moves to M(k+1), to Ik or to D(k+1).
A transition key is (from type, k, to type): ("M", 2, "D") is M2 -> D3, ("I", 2, "I") is
I2 -> I2, and ("D", m, "M") is Dm -> End. With plan7=True the transitions D -> I and
I -> D are not allowed, as in the Plan 7 architecture of HMMER.

Probabilities are Fractions when the model is built from counts, so results are exact.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Callable, Dict, List, Sequence, Tuple, Union

Num = Union[float, Fraction]
Key = Tuple[str, int, str]
State = Tuple[str, int]


@dataclass
class ProfileHMM:
    m: int
    alphabet: str
    match_emit: List[Dict[str, Num]]  # index 1..m, index 0 unused
    insert_emit: List[Dict[str, Num]]  # index 0..m
    trans: Dict[Key, Num]

    def t(self, key: Key) -> Num:
        return self.trans.get(key, 0)


def allowed_transitions(m: int, plan7: bool = False) -> List[Key]:
    """All transitions of a model with m match states. Cost O(m)."""
    keys: List[Key] = []
    for k in range(m + 1):
        for a in ("M", "I", "D"):
            if a == "D" and k == 0:
                continue
            for b in ("M", "I", "D"):
                if b == "D" and k == m:
                    continue
                if plan7 and {a, b} == {"D", "I"}:
                    continue
                keys.append((a, k, b))
    return keys


def match_columns(msa: Sequence[str], symfrac: float = 0.5) -> List[int]:
    """Columns whose fraction of residues (not gaps) is at least symfrac."""
    rows = len(msa)
    return [c for c in range(len(msa[0])) if sum(r[c] != "-" for r in msa) >= symfrac * rows]


def state_path(row: str, matches: Sequence[int]) -> List[State]:
    """The state path of one aligned row, from ("M", 0) = Begin to ("M", m + 1) = End."""
    is_match = set(matches)
    path: List[State] = [("M", 0)]
    k = 0
    for c, ch in enumerate(row):
        if c in is_match:
            k += 1
            path.append(("M", k) if ch != "-" else ("D", k))
        elif ch != "-":
            path.append(("I", k))
    path.append(("M", len(matches) + 1))
    return path


def build(msa: Sequence[str], alphabet: str, symfrac: float = 0.5, pseudo: int = 1, plan7: bool = False) -> ProfileHMM:
    """Estimate a profile HMM from a multiple alignment by counting, with `pseudo` added to each count.

    Cost O(rows * columns + m * |alphabet|).
    """
    matches = match_columns(msa, symfrac)
    m = len(matches)
    keys = allowed_transitions(m, plan7)
    count: Dict[Key, Fraction] = {key: Fraction(pseudo) for key in keys}
    mcount = [{a: Fraction(pseudo) for a in alphabet} for _ in range(m + 1)]
    icount = [{a: Fraction(pseudo) for a in alphabet} for _ in range(m + 1)]
    for row in msa:
        path = state_path(row, matches)
        residues = [ch for ch in row if ch != "-"]
        r = 0
        for s in path[1:-1]:
            if s[0] == "M":
                mcount[s[1]][residues[r]] += 1
                r += 1
            elif s[0] == "I":
                icount[s[1]][residues[r]] += 1
                r += 1
        for (a, k), (b, _) in zip(path, path[1:]):
            key = (a, k, b)
            if key not in count:
                raise ValueError("the alignment uses a transition that the model does not allow: %r" % (key,))
            count[key] += 1
    trans: Dict[Key, Num] = {}
    for a in ("M", "I", "D"):
        for k in range(m + 1):
            out = [key for key in keys if key[0] == a and key[1] == k]
            total = sum(count[key] for key in out)
            for key in out:
                trans[key] = count[key] / total if total else Fraction(0)

    def norm(c: Dict[str, Fraction]) -> Dict[str, Num]:
        total = sum(c.values())
        return {a: (v / total if total else Fraction(0)) for a, v in c.items()}

    match_emit = [norm(c) for c in mcount]
    match_emit[0] = {}
    return ProfileHMM(m, alphabet, match_emit, [norm(c) for c in icount], trans)


def _dp(h: ProfileHMM, x: str, op: Callable[[List[Num]], Num]):
    """Shared recurrence of Viterbi (op = max) and Forward (op = sum). Cost O(m n)."""
    n, m = len(x), h.m
    zero = Fraction(0)
    vm = [[zero] * (n + 1) for _ in range(m + 1)]
    vi = [[zero] * (n + 1) for _ in range(m + 1)]
    vd = [[zero] * (n + 1) for _ in range(m + 1)]
    vm[0][0] = Fraction(1)
    t = h.t
    for i in range(n + 1):
        for k in range(m + 1):
            if k >= 1 and i >= 1:
                vm[k][i] = h.match_emit[k][x[i - 1]] * op([vm[k - 1][i - 1] * t(("M", k - 1, "M")), vi[k - 1][i - 1] * t(("I", k - 1, "M")), vd[k - 1][i - 1] * t(("D", k - 1, "M"))])
            if i >= 1:
                vi[k][i] = h.insert_emit[k][x[i - 1]] * op([vm[k][i - 1] * t(("M", k, "I")), vi[k][i - 1] * t(("I", k, "I")), vd[k][i - 1] * t(("D", k, "I"))])
            if k >= 1:
                vd[k][i] = op([vm[k - 1][i] * t(("M", k - 1, "D")), vi[k - 1][i] * t(("I", k - 1, "D")), vd[k - 1][i] * t(("D", k - 1, "D"))])
    end = op([vm[m][n] * t(("M", m, "M")), vi[m][n] * t(("I", m, "M")), vd[m][n] * t(("D", m, "M"))])
    return end, vm, vi, vd


def forward(h: ProfileHMM, x: str) -> Num:
    """P(x | model), the sum over all state paths. Cost O(m n) time."""
    return _dp(h, x, sum)[0]


def viterbi(h: ProfileHMM, x: str) -> Tuple[Num, List[State]]:
    """The most probable state path (Begin and End left out) and P(x, path). Cost O(m n)."""
    best, vm, vi, vd = _dp(h, x, max)
    if best == 0:
        return best, []
    table = {"M": vm, "I": vi, "D": vd}
    t = h.t
    path: List[State] = []
    n, m = len(x), h.m
    # find the state before End, then walk back by recomputing which predecessor gives the value
    cur_val, cur, i, k = best, ("M", m + 1), n, m + 1
    while cur != ("M", 0):
        a, kk = cur
        if a == "M":
            src_k, src_i = kk - 1, i - 1 if kk <= m else i
            factor = h.match_emit[kk][x[i - 1]] if kk <= m else 1
        elif a == "I":
            src_k, src_i, factor = kk, i - 1, h.insert_emit[kk][x[i - 1]]
        else:
            src_k, src_i, factor = kk - 1, i, 1
        for b in ("M", "I", "D"):
            if b == "D" and src_k == 0:
                continue
            val = table[b][src_k][src_i] * t((b, src_k, a))
            if val > 0 and val * factor == cur_val:
                cur, cur_val, i = (b, src_k), table[b][src_k][src_i], src_i
                break
        else:
            raise ArithmeticError("traceback failed; use exact (Fraction) parameters")
        if cur != ("M", 0):
            path.append(cur)
    path.reverse()
    return best, path


def path_probability(h: ProfileHMM, x: str, path: Sequence[State]) -> Num:
    """P(x, path) for a path given without Begin and End. Cost O(len(path))."""
    full = [("M", 0)] + list(path) + [("M", h.m + 1)]
    prob: Num = Fraction(1)
    r = 0
    for (a, k), (b, kk) in zip(full, full[1:]):
        prob *= h.t((a, k, b))
        if (b, kk) != ("M", h.m + 1) and b in "MI":
            prob *= (h.match_emit[kk] if b == "M" else h.insert_emit[kk])[x[r]]
            r += 1
    return prob if r == len(x) else Fraction(0)
