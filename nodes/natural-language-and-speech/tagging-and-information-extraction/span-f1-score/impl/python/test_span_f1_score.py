# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/span-f1-score/. The authors are listed in prov/Q2NAGZ.jsonl.

import random
from fractions import Fraction

from span_f1_score import bio_to_spans, counts, macro_f1, per_type, prf, span_f1, token_accuracy

# The example of the page: John Smith works for Acme Corp in Paris
GOLD = ["B-PER", "I-PER", "O", "O", "B-ORG", "I-ORG", "O", "B-LOC"]
PRED = ["B-PER", "O", "O", "O", "B-ORG", "I-ORG", "O", "B-ORG"]


def test_page_example():
    assert bio_to_spans(GOLD) == [(0, 2, "PER"), (4, 6, "ORG"), (7, 8, "LOC")]
    assert bio_to_spans(PRED) == [(0, 1, "PER"), (4, 6, "ORG"), (7, 8, "ORG")]
    assert counts([set(bio_to_spans(GOLD))], [set(bio_to_spans(PRED))]) == (1, 2, 2)
    assert span_f1([GOLD], [PRED]) == (Fraction(1, 3), Fraction(1, 3), Fraction(1, 3))
    assert token_accuracy([GOLD], [PRED]) == Fraction(3, 4)
    table = per_type([set(bio_to_spans(GOLD))], [set(bio_to_spans(PRED))])
    assert table["PER"] == (0, 0, 0)
    assert table["ORG"] == (Fraction(1, 2), Fraction(1), Fraction(2, 3))
    assert table["LOC"] == (0, 0, 0)
    assert macro_f1([set(bio_to_spans(GOLD))], [set(bio_to_spans(PRED))]) == Fraction(2, 9)


def test_partial_overlap_is_a_false_positive_and_a_false_negative():
    assert counts([{(0, 2, "PER")}], [{(0, 1, "PER")}]) == (0, 1, 1)
    assert counts([{(0, 2, "PER")}], [{(0, 2, "ORG")}]) == (0, 1, 1)
    assert prf(0, 1, 1) == (0, 0, 0)


def test_chunk_rules():
    assert bio_to_spans(["O", "I-X", "I-X"]) == [(1, 3, "X")]  # I-X after O starts a span
    assert bio_to_spans(["B-X", "I-Y"]) == [(0, 1, "X"), (1, 2, "Y")]
    assert bio_to_spans(["I-X", "I-X", "B-X", "O"]) == [(0, 2, "X"), (2, 3, "X")]  # IOB1
    assert bio_to_spans(["B-X", "B-X"]) == [(0, 1, "X"), (1, 2, "X")]
    assert bio_to_spans([]) == [] and bio_to_spans(["O", "O"]) == []


def repair_then_read(tags):
    """An independent reader: first rewrite each I-X that cannot continue a span as B-X, then read runs."""
    fixed = []
    for p, t in enumerate(tags):
        if t.startswith("I-") and (p == 0 or tags[p - 1] == "O" or tags[p - 1][2:] != t[2:]):
            t = "B-" + t[2:]
        fixed.append(t)
    spans, p = [], 0
    while p < len(fixed):
        if fixed[p].startswith("B-"):
            q = p + 1
            while q < len(fixed) and fixed[q] == "I-" + fixed[p][2:]:
                q += 1
            spans.append((p, q, fixed[p][2:]))
            p = q
        else:
            p += 1
    return spans


def test_reader_against_repair():
    rng = random.Random(1)
    alphabet = ["O", "B-X", "I-X", "B-Y", "I-Y"]
    for _ in range(2000):
        tags = [rng.choice(alphabet) for _ in range(rng.randint(0, 8))]
        assert bio_to_spans(tags) == repair_then_read(tags)


def random_spans(rng, n):
    out, i = set(), 0
    while i < n:
        if rng.random() < 0.4:
            j = rng.randint(i + 1, min(n, i + 3))
            out.add((i, j, rng.choice("XY")))
            i = j
        else:
            i += 1
    return out


def test_identities_on_random_data():
    rng = random.Random(2)
    for _ in range(500):
        gold = [random_spans(rng, 8) for _ in range(3)]
        pred = [random_spans(rng, 8) for _ in range(3)]
        tp, fp, fn = counts(gold, pred)
        p, r, f = prf(tp, fp, fn)
        # Brute force over all spans of the corpus, tagged with the sentence number.
        g = {(k,) + s for k, sent in enumerate(gold) for s in sent}
        q = {(k,) + s for k, sent in enumerate(pred) for s in sent}
        assert (tp, fp, fn) == (len(g & q), len(q - g), len(g - q))
        if tp:
            assert f == Fraction(2 * tp, 2 * tp + fp + fn)
            assert f == 1 / ((1 / p + 1 / r) / 2)
            assert min(p, r) <= f <= max(p, r)
        else:
            assert f == 0
        # Micro average: the corpus counts are the sums of the sentence counts.
        parts = [counts([a], [b]) for a, b in zip(gold, pred)]
        assert (tp, fp, fn) == tuple(sum(c[k] for c in parts) for k in range(3))


def test_perfect_and_empty():
    assert span_f1([GOLD], [GOLD]) == (1, 1, 1)
    assert prf(0, 0, 0) == (0, 0, 0)
    assert prf(0, 0, 3) == (0, 0, 0)
