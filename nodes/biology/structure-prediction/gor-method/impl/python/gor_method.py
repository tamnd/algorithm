# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gor-method/. The authors are listed in prov/KTTQKV.jsonl.

"""The GOR I method: directional information summed over a window.

The information that residue a at offset m carries about state S at the
centre is I(S; a, m) = ln(P(S | a at offset m) / P(S)), in nats. The score
of state S at position j is the sum of I(S; R[j+m], m) over the offsets
m = -h .. h that fall inside the sequence, plus an optional decision
constant for S. The prediction is the state with the largest score.
The original method uses h = 8, a window of 17 residues.
"""

from math import log
from typing import Optional


def train(seqs: list, labels: list, states: str = "HEC", half: int = 8, pseudo: float = 1.0) -> dict:
    """Estimate the information table info[(S, m, a)] from labelled sequences.

    P(S | a at m) = (f(S, m, a) + pseudo) / (f(m, a) + pseudo |states|), where
    f(S, m, a) counts the positions j with state S and residue a at j + m.
    P(S) = (N(S) + pseudo) / (N + pseudo |states|).
    """
    k = len(states)
    count: dict = {}  # @line L1
    total: dict = {}
    nstate = {s: 0 for s in states}
    alphabet = set()
    for seq, lab in zip(seqs, labels):  # @line L2
        n = len(seq)
        alphabet.update(seq)
        for j in range(n):
            s = lab[j]
            nstate[s] += 1  # @line L3
            for m in range(-half, half + 1):  # @line L4
                if 0 <= j + m < n:
                    a = seq[j + m]
                    count[(s, m, a)] = count.get((s, m, a), 0) + 1  # @line L5
                    total[(m, a)] = total.get((m, a), 0) + 1
    N = sum(nstate.values())
    info = {}
    for s in states:  # @line L6
        prior = (nstate[s] + pseudo) / (N + pseudo * k)
        for m in range(-half, half + 1):
            for a in alphabet:
                post = (count.get((s, m, a), 0) + pseudo) / (total.get((m, a), 0) + pseudo * k)
                info[(s, m, a)] = log(post / prior)  # @line L7
    return info  # @line L8


def gor_scores(seq: str, info: dict, states: str = "HEC", half: int = 8,
               decision: Optional[dict] = None) -> list:
    """Return score[j][S] for each position j.

    Each residue adds its information to the up to 2h + 1 centres that see it,
    so the cost is O(n (2h + 1) |states|) time.
    """
    n = len(seq)
    base = {s: (decision or {}).get(s, 0) for s in states}
    scores = [dict(base) for _ in range(n)]  # @line L9
    for i in range(n):  # @line L10
        a = seq[i]
        for m in range(-half, half + 1):  # @line L11
            j = i - m  # residue i is at offset m from centre j
            if 0 <= j < n:
                row = scores[j]
                for s in states:
                    row[s] += info.get((s, m, a), 0)  # @line L12
    return scores


def gor_predict(seq: str, info: dict, states: str = "HEC", half: int = 8,
                decision: Optional[dict] = None) -> str:
    """Return the predicted state at each position. Ties go to the earlier state."""
    out = []
    for row in gor_scores(seq, info, states, half, decision):
        best = states[0]
        for s in states[1:]:
            if row[s] > row[best]:
                best = s
        out.append(best)  # @line L13
    return "".join(out)  # @line L14
