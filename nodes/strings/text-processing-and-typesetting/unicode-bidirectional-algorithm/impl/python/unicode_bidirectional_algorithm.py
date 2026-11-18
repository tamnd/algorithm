# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unicode-bidirectional-algorithm/. The authors are listed in prov/2X2V4H.jsonl.
"""The Unicode Bidirectional Algorithm of UAX 9 (revision 50, Unicode 16.0.0) for one
paragraph that is also one line.

The Bidi_Class values come from unicodedata. Unassigned code points get '' from
unicodedata; they are treated as L here, while DerivedBidiClass.txt gives some ranges
other defaults. The paired brackets are the lines of BidiBrackets-16.0.0.txt for
U+0028/0029, U+005B/005D, U+007B/007D, U+2329/232A and U+3008/3009; BD16 compares
brackets after canonical decomposition, so U+2329 and U+3008 count as the same opening
bracket.
"""

import unicodedata

MAX_DEPTH = 125  # BD2
BRACKET_STACK = 63  # BD16

OPENING = {"(": ")", "[": "]", "{": "}", "〈": "〉", "〈": "〉"}
CLOSING = {v: k for k, v in OPENING.items()}

REMOVED = ("RLE", "LRE", "RLO", "LRO", "PDF", "BN")  # X9
INITIATORS = ("LRI", "RLI", "FSI")
NEUTRAL_OR_ISOLATE = ("B", "S", "WS", "ON", "LRI", "RLI", "FSI", "PDI")  # NI of N1


def bidi_class(c: str) -> str:
    return unicodedata.bidirectional(c) or "L"


def _canon(c: str) -> str:
    return unicodedata.normalize("NFD", c)


def matching_pdi(t: list) -> tuple:
    """BD9. match[i] is the index of the PDI that matches the isolate initiator at i, or
    None; opener[j] is the initiator that a PDI at j matches, or None."""
    n = len(t)
    match, opener = [None] * n, [None] * n
    open_stack = []
    for i, x in enumerate(t):
        if x in INITIATORS:
            open_stack.append(i)
        elif x == "PDI" and open_stack:
            k = open_stack.pop()
            match[k], opener[i] = i, k
        elif x == "B":
            open_stack = []
    return match, opener


def first_strong(t: list, start: int, end: int, match: list):
    """P2 and P3 on t[start:end]: 0 for L, 1 for R or AL, None if there is no strong
    character outside isolates."""
    i = start
    while i < end:
        x = t[i]
        if x == "L":
            return 0
        if x in ("R", "AL"):
            return 1
        if x in INITIATORS:
            if match[i] is None:
                return None
            i = match[i]
        i += 1
    return None


def _odd_above(v):
    return (v + 1) | 1


def _even_above(v):
    return (v + 2) & ~1


def explicit_levels(t: list, p: int, match: list) -> tuple:
    """Rules X1 to X8. Return the levels and the classes after the overrides."""
    n = len(t)
    lev, ty = [p] * n, list(t)
    stack = [(p, None, False)]  # (level, override, isolate) of X1
    over_iso = over_emb = valid_iso = 0
    for i, x in enumerate(t):
        level, override, _ = stack[-1]
        if x in ("RLE", "LRE", "RLO", "LRO"):  # X2 to X5
            lev[i] = level
            new = _odd_above(level) if x[0] == "R" else _even_above(level)
            if new <= MAX_DEPTH and over_iso == 0 and over_emb == 0:
                stack.append((new, {"RLO": "R", "LRO": "L"}.get(x), False))
            elif over_iso == 0:
                over_emb += 1
        elif x in INITIATORS:  # X5a to X5c
            lev[i] = level
            if override:
                ty[i] = override
            if x == "FSI":
                end = match[i] if match[i] is not None else n
                x = "RLI" if first_strong(t, i + 1, end, match) == 1 else "LRI"
            new = _odd_above(level) if x == "RLI" else _even_above(level)
            if new <= MAX_DEPTH and over_iso == 0 and over_emb == 0:
                valid_iso += 1
                stack.append((new, None, True))
            else:
                over_iso += 1
        elif x == "PDI":  # X6a
            if over_iso > 0:
                over_iso -= 1
            elif valid_iso > 0:
                over_emb = 0
                while not stack[-1][2]:
                    stack.pop()
                stack.pop()
                valid_iso -= 1
            lev[i] = stack[-1][0]
            if stack[-1][1]:
                ty[i] = stack[-1][1]
        elif x == "PDF":  # X7
            lev[i] = level
            if over_iso > 0:
                pass
            elif over_emb > 0:
                over_emb -= 1
            elif not stack[-1][2] and len(stack) >= 2:
                stack.pop()
        elif x == "B":  # X8
            lev[i] = p
        else:  # X6, and BN, which X9 removes
            lev[i] = level
            if override and x != "BN":
                ty[i] = override
    return lev, ty


def isolating_run_sequences(t: list, lev: list, match: list) -> list:
    """X10 and BD13: the isolating run sequences as lists of indices, in order."""
    kept = [i for i in range(len(t)) if t[i] not in REMOVED]
    runs = []
    for i in kept:
        if runs and lev[runs[-1][-1]] == lev[i]:
            runs[-1].append(i)
        else:
            runs.append([i])
    run_at = {r[0]: k for k, r in enumerate(runs)}
    used = [False] * len(runs)
    seqs = []
    for k, r in enumerate(runs):
        if used[k]:
            continue
        seq, used[k] = list(r), True
        while t[seq[-1]] in INITIATORS and match[seq[-1]] is not None \
                and match[seq[-1]] in run_at and not used[run_at[match[seq[-1]]]]:
            nxt = run_at[match[seq[-1]]]
            seq.extend(runs[nxt])
            used[nxt] = True
        seqs.append(seq)
    return seqs


def _strong(x):
    """Strong direction for N0 and N1: EN and AN count as R."""
    if x == "L":
        return "L"
    if x in ("R", "EN", "AN"):
        return "R"
    return None


def resolve_sequence(s: str, t: list, ty: list, lev: list, seq: list, sos: str, eos: str) -> None:
    """Rules W1 to W7, N0 to N2 and I1 to I2 on one isolating run sequence."""
    m = len(seq)
    x = [ty[i] for i in seq]
    level = lev[seq[0]]
    e = "L" if level % 2 == 0 else "R"
    original = list(x)  # the classes before W1, for N0
    # W1
    for k in range(m):  # @line L6
        if x[k] == "NSM":
            if k == 0:
                x[k] = sos
            elif t[seq[k - 1]] in INITIATORS + ("PDI",):
                x[k] = "ON"
            else:
                x[k] = x[k - 1]
    # W2 and W3
    last = sos
    for k in range(m):
        if x[k] in ("L", "R", "AL"):
            last = x[k]
        elif x[k] == "EN" and last == "AL":
            x[k] = "AN"
    x = ["R" if v == "AL" else v for v in x]
    # W4
    for k in range(1, m - 1):
        if x[k] == "ES" and x[k - 1] == "EN" and x[k + 1] == "EN":
            x[k] = "EN"
        elif x[k] == "CS" and x[k - 1] == x[k + 1] and x[k - 1] in ("EN", "AN"):
            x[k] = x[k - 1]
    # W5
    k = 0
    while k < m:
        if x[k] == "ET":
            j = k
            while j < m and x[j] == "ET":
                j += 1
            if (k > 0 and x[k - 1] == "EN") or (j < m and x[j] == "EN"):
                for q in range(k, j):
                    x[q] = "EN"
            k = j
        else:
            k += 1
    # W6
    x = ["ON" if v in ("ES", "ET", "CS") else v for v in x]
    # W7
    last = sos
    for k in range(m):
        if x[k] in ("L", "R"):
            last = x[k]
        elif x[k] == "EN" and last == "L":
            x[k] = "L"
    # N0: BD16 finds the bracket pairs.
    stack, pairs = [], []
    for k in range(m):
        c = s[seq[k]]
        if x[k] != "ON":
            continue
        if c in OPENING:
            if len(stack) == BRACKET_STACK:  # BD16: stop and return an empty list
                pairs = []
                break
            stack.append((_canon(OPENING[c]), k))
        elif c in CLOSING:
            cc = _canon(c)
            for d in range(len(stack) - 1, -1, -1):
                if stack[d][0] == cc:
                    pairs.append((stack[d][1], k))
                    del stack[d:]
                    break
    pairs.sort()
    for o, c in pairs:  # @line L7
        inside = {_strong(x[k]) for k in range(o + 1, c)} - {None}
        if e in inside:  # N0 b
            new = e
        elif inside:  # N0 c: the opposite direction is inside
            new = sos
            for k in range(o - 1, -1, -1):
                if _strong(x[k]):
                    new = _strong(x[k])
                    break
        else:  # N0 d
            continue
        for b in (o, c):
            x[b] = new
            k = b + 1
            while k < m and original[k] == "NSM":
                x[k] = new
                k += 1
    # N1 and N2
    k = 0
    while k < m:  # @line L8
        if x[k] in NEUTRAL_OR_ISOLATE:
            j = k
            while j < m and x[j] in NEUTRAL_OR_ISOLATE:
                j += 1
            left = _strong(x[k - 1]) if k > 0 else sos
            right = _strong(x[j]) if j < m else eos
            for q in range(k, j):
                x[q] = left if left == right else e
            k = j
        else:
            k += 1
    # I1 and I2
    for k in range(m):  # @line L9
        i = seq[k]
        if lev[i] % 2 == 0:
            lev[i] += 1 if x[k] == "R" else 2 if x[k] in ("AN", "EN") else 0
        elif x[k] in ("L", "EN", "AN"):
            lev[i] += 1


def visual_order(levels: list) -> list:
    """Rule L2 on one line: the indices of the kept characters from left to right."""
    order = [i for i, v in enumerate(levels) if v is not None]  # @line L11
    if not order:
        return []
    vals = [levels[i] for i in order]
    high = max(vals)
    low = min(v for v in vals if v % 2 == 1) if any(v % 2 for v in vals) else high + 1
    for v in range(high, low - 1, -1):  # @line L12
        k = 0
        while k < len(order):
            if levels[order[k]] >= v:
                j = k
                while j < len(order) and levels[order[j]] >= v:
                    j += 1
                order[k:j] = order[k:j][::-1]
                k = j
            else:
                k += 1
    return order


def bidi(s: str, direction=None) -> tuple:
    """Run the algorithm on s, one paragraph that is shown as one line.

    direction is 0 (left to right), 1 (right to left) or None (rules P2 and P3).
    Return (paragraph level, levels, visual order). The level of a character that X9
    removes is None, and the visual order skips it.
    """
    n = len(s)
    t = [bidi_class(c) for c in s]  # @line L1
    match, _ = matching_pdi(t)
    p = direction  # @line L2
    if p is None:
        p = first_strong(t, 0, n, match) or 0
    lev, ty = explicit_levels(t, p, match)  # @line L3
    kept = [i for i in range(n) if t[i] not in REMOVED]  # @line L4
    pos = {i: k for k, i in enumerate(kept)}
    for seq in isolating_run_sequences(t, lev, match):  # @line L5
        level = lev[seq[0]]
        before = lev[kept[pos[seq[0]] - 1]] if pos[seq[0]] > 0 else p
        if t[seq[-1]] in INITIATORS or pos[seq[-1]] + 1 == len(kept):
            after = p
        else:
            after = lev[kept[pos[seq[-1]] + 1]]
        sos = "L" if max(level, before) % 2 == 0 else "R"
        eos = "L" if max(level, after) % 2 == 0 else "R"
        resolve_sequence(s, t, ty, lev, seq, sos, eos)
    levels = [None if t[i] in REMOVED else lev[i] for i in range(n)]
    trailing = True  # @line L10
    for i in range(n - 1, -1, -1):
        if t[i] in REMOVED:
            continue
        if t[i] in ("S", "B"):
            levels[i], trailing = p, True
        elif trailing and t[i] in ("WS",) + INITIATORS + ("PDI",):
            levels[i] = p
        else:
            trailing = False
    order = visual_order(levels)
    return p, levels, order  # @line L13


def reorder(s: str, direction=None) -> str:
    """The characters of s in visual order, without the characters that X9 removes."""
    return "".join(s[i] for i in bidi(s, direction)[2])
