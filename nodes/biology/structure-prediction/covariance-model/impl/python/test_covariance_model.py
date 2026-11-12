# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/covariance-model/. The authors are listed in prov/9XQKJ4.jsonl.

import random
from math import comb

from covariance_model import CM, NEG, cyk, cyk_align, cyk_scan, guide_tree, parse_pairs, toy_scores


def all_parse_scores(cm, x, v, i, j):
    """Return the list of the scores of every parse of x[i:j] from state v."""
    st = cm.states[v]
    typ, ch, d = st["type"], st["children"], j - i
    out = []
    if typ == "E":
        return [0] if d == 0 else []
    if typ == "B":
        for k in range(i, j + 1):
            for s1 in all_parse_scores(cm, x, ch[0], i, k):
                for s2 in all_parse_scores(cm, x, ch[1], k, j):
                    out.append(s1 + s2)
        return out
    if typ == "P":
        if d < 2:
            return []
        e, ii, jj = cm.emit[v][x[i] + x[j - 1]], i + 1, j - 1
    elif typ == "L":
        if d < 1:
            return []
        e, ii, jj = cm.emit[v][x[i]], i + 1, j
    elif typ == "R":
        if d < 1:
            return []
        e, ii, jj = cm.emit[v][x[j - 1]], i, j - 1
    else:
        e, ii, jj = 0, i, j
    for w in ch:
        for s in all_parse_scores(cm, x, w, ii, jj):
            out.append(e + cm.trans[(v, w)] + s)
    return out


def random_scores(cm, rng):
    cm.set_scores(lambda v, w: rng.randint(-3, 2), lambda v, a: rng.randint(-3, 3))


def test_guide_tree_and_state_count() -> None:
    types = [n["type"] for n in guide_tree("((...))")]
    assert types == ["ROOT", "MATP", "MATP", "MATL", "MATL", "MATL", "END"]
    assert len(CM("((...))").states) == 3 + 2 * 6 + 3 * 3 + 1
    types = [n["type"] for n in guide_tree("(.)(.)")]
    assert types == ["ROOT", "BIF", "BEGL", "MATP", "MATL", "END", "BEGR", "MATP", "MATL", "END"]
    cm = CM("(.)(.)")
    assert len(cm.states) == 3 + 1 + 1 + 6 + 3 + 1 + 2 + 6 + 3 + 1
    assert cm.bifurcations == 1


def test_example() -> None:
    cm = CM("((...))", "GGAAACC")
    toy_scores(cm)
    score, parse = cyk_align(cm, "GGAAACC")
    assert score == 9 and parse_pairs(cm, parse) == [(0, 6), (1, 5)]
    # Compensatory changes keep the pairs and the score.
    score, parse = cyk_align(cm, "CUAAAAG")
    assert score == 9 and parse_pairs(cm, parse) == [(0, 6), (1, 5)]
    # Breaking a pair lowers the score.
    assert cyk_align(cm, "GGAAACA")[0] == 4
    # An insertion and a deletion in the loop.
    assert cyk_align(cm, "GGAAAACC")[0] == 6
    assert cyk_align(cm, "GGACC")[0] == 1
    # A local hit inside a longer sequence.
    assert cyk_scan(cm, "UUCUAAAAGUU", 9) == (9, 2, 9)


def test_against_brute_force() -> None:
    rng = random.Random(1994)
    for struct in ["", ".", "()", "(.)", ".(.).", "(.)(.)", "((.))"]:
        cm = CM(struct)
        for _ in range(6):
            random_scores(cm, rng)
            x = "".join(rng.choice("ACGU") for _ in range(rng.randint(0, 4)))
            a, _ = cyk(cm, x)
            L = len(x)
            for i in range(L + 1):
                for j in range(i, L + 1):
                    scores = all_parse_scores(cm, x, 0, i, j)
                    want = max(scores) if scores else NEG
                    assert a[0][i][j] == want, (struct, x, i, j)


def test_traceback_scores_match() -> None:
    rng = random.Random(5)
    cm = CM("((..)).(..)")
    for _ in range(5):
        random_scores(cm, rng)
        x = "".join(rng.choice("ACGU") for _ in range(8))
        score, parse = cyk_align(cm, x)
        total = 0
        for v, i, j in parse:
            st = cm.states[v]
            if st["type"] == "P":
                total += cm.emit[v][x[i] + x[j - 1]]
            elif st["type"] == "L":
                total += cm.emit[v][x[i]]
            elif st["type"] == "R":
                total += cm.emit[v][x[j - 1]]
        # Add the transitions along the parse.
        index = {(v, i, j): k for k, (v, i, j) in enumerate(parse)}
        for k, (v, i, j) in enumerate(parse):
            st = cm.states[v]
            if st["type"] in ("B", "E"):
                continue
            w = parse[k + 1][0]
            total += cm.trans[(v, w)]
        assert total == score and len(index) == len(parse)


def test_operation_counts() -> None:
    cm = CM("(.)(.)")
    toy_scores(cm)
    M, B = len(cm.states), cm.bifurcations
    for L in range(0, 9):
        x = "ACGUACGU"[:L]
        _, (cells, splits) = cyk(cm, x)
        assert cells == M * (L + 1) * (L + 2) // 2
        assert splits == B * comb(L + 3, 3)
