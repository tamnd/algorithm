# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chou-fasman-method/. The authors are listed in prov/Q8MXAA.jsonl.

"""The Chou-Fasman rules for helix and strand, with integer propensities.

Propensities are stored times 100, so that each test on a mean is an exact
integer test on a sum. The default table is the one reprinted in later
teaching material from Chou and Fasman's 29-protein table; it is used here
as an example. (Reprints give 1.14 or 1.16 for the helix value of Lys.)
Turn prediction is not implemented: residues not in a helix or a strand
are labelled C.
"""

# residue: (P_alpha, P_beta), times 100
PROPENSITY = {
    "A": (142, 83), "R": (98, 93), "N": (67, 89), "D": (101, 54), "C": (70, 119),
    "Q": (111, 110), "E": (151, 37), "G": (57, 75), "H": (100, 87), "I": (108, 160),
    "L": (121, 130), "K": (114, 74), "M": (145, 105), "F": (113, 138), "P": (57, 55),
    "S": (77, 75), "T": (83, 119), "W": (108, 137), "Y": (69, 147), "V": (106, 170),
}

# (nucleus window w, formers needed k, former threshold f, accept threshold a)
HELIX = (6, 4, 103, 103)
STRAND = (5, 3, 100, 105)


def nuclei(p: list, window: int, need: int, former: int) -> list:
    """Start indices of windows with at least `need` residues of propensity > former."""
    n = len(p)
    return [s for s in range(n - window + 1) if sum(1 for v in p[s:s + window] if v > former) >= need]


def extend(p: list, s: int, e: int) -> tuple:
    """Grow [s, e) while the four residues at the new end have mean >= 1.00."""
    n = len(p)
    while s > 0 and sum(p[s - 1:s + 3]) >= 400:  # @line L6
        s -= 1
    while e < n and sum(p[e - 3:e + 1]) >= 400:  # @line L7
        e += 1
    return s, e  # @line L8


def segments(p: list, q: list, rule: tuple) -> list:
    """Accepted segments [s, e) for the state whose propensities are p; q is the other state."""
    w, k, f, a = rule
    out = []  # @line L1
    for s0 in nuclei(p, w, k, f):  # @line L2
        s, e = extend(p, s0, s0 + w)  # @line L3
        if sum(p[s:e]) > a * (e - s) and sum(p[s:e]) > sum(q[s:e]):  # @line L4
            out.append((s, e))
    return out  # @line L5


def chou_fasman(seq: str, table: dict = PROPENSITY) -> str:
    """Return a string over H, E and C, one letter per residue.

    A run of residues that both a helix and a strand cover goes to H when the
    sum of P_alpha over the run is larger than the sum of P_beta, else to E.
    """
    pa = [table[c][0] for c in seq]  # @line L9
    pb = [table[c][1] for c in seq]
    n = len(seq)
    h, b = [False] * n, [False] * n  # @line L10
    for s, e in segments(pa, pb, HELIX):  # @line L11
        for r in range(s, e):
            h[r] = True
    for s, e in segments(pb, pa, STRAND):  # @line L12
        for r in range(s, e):
            b[r] = True
    out = ["H" if h[r] and not b[r] else "E" if b[r] and not h[r] else "C" for r in range(n)]  # @line L13
    r = 0  # @line L14
    while r < n:  # @line L15
        if h[r] and b[r]:  # @line L16
            t = r  # @line L17
            while t < n and h[t] and b[t]:
                t += 1
            lab = "H" if sum(pa[r:t]) > sum(pb[r:t]) else "E"  # @line L18
            for u in range(r, t):
                out[u] = lab
            r = t
        else:
            r += 1  # @line L19
    return "".join(out)  # @line L20
