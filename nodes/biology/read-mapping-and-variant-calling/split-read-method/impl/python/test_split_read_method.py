# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/split-read-method/. The authors are listed in prov/TDWFBV.jsonl.

import random
from collections import Counter

from bioseq import random_dna, revcomp
from split_read_method import grow_prefix, grow_suffix, split_read

EXAMPLE_REF = "CAGAACCTGCTGTGACATAAACTAGCTGATATGTGTTCCC"
EXAMPLE_READ = "ACCTGCTGTGACTAGCTGAT"


def normalize(ref, event):
    """Shift a DEL or INS to the left as far as the reference allows (VCF left alignment)."""
    kind, pos, size, ins = event
    if kind == "DEL":
        while pos > 0 and ref[pos - 1] == ref[pos + size - 1]:
            pos -= 1
        return kind, pos, size, ""
    while pos > 0 and ref[pos - 1] == ins[-1]:
        ins = ref[pos - 1] + ins[:-1]
        pos -= 1
    return kind, pos, size, ins


def brute_events(ref, r, lo, hi, min_part, max_ins, max_del):
    """Every DEL or INS that explains r as two exact parts of at least min_part bases in ref[lo:hi]."""
    L, out = len(r), set()
    for p in range(lo, hi):
        for i in range(min_part, L - min_part + 1):
            if ref[p:p + i] != r[:i]:
                break
            for D in range(1, max_del + 1):
                q = p + i + D
                if q + L - i <= hi and ref[q:q + L - i] == r[i:]:
                    out.add(normalize(ref, ("DEL", p + i, D, "")))
            for I in range(1, max_ins + 1):
                rest = L - i - I
                if rest >= min_part and p + i + rest <= hi and ref[p + i:p + i + rest] == r[i + I:]:
                    out.add(normalize(ref, ("INS", p + i, I, r[i:i + I])))
    return out


def longest_prefix_naive(ref, r, lo, hi):
    a = 0
    while a < len(r) and r[:a + 1] in ref[lo:hi]:
        a += 1
    return a


def test_grow_against_naive_search():
    rng = random.Random(1)
    for _ in range(200):
        ref = random_dna(rng, rng.randint(1, 30))
        r = random_dna(rng, rng.randint(1, 8))
        lo = rng.randrange(len(ref))
        hi = rng.randint(lo + 1, len(ref))
        a, P = grow_prefix(ref, r, lo, hi)
        assert a == longest_prefix_naive(ref, r, lo, hi)
        assert P == [x for x in range(lo, hi - a + 1) if ref[x:x + a] == r[:a]] or a == 0
        b, Q = grow_suffix(ref, r, lo, hi)
        rr = r[::-1]
        assert b == longest_prefix_naive(ref[::-1], rr, len(ref) - hi, len(ref) - lo)
        if b:
            assert Q == [e for e in range(lo + b, hi + 1) if ref[e - b:e] == r[len(r) - b:]]


def test_example_with_microhomology():
    a, P = grow_prefix(EXAMPLE_REF, EXAMPLE_READ, 0, 40)
    assert (a, P) == (12, [4])
    b, Q = grow_suffix(EXAMPLE_REF, EXAMPLE_READ, 4, 40)
    assert (b, Q) == (10, [30])
    # D = e - p - L = 30 - 4 - 20 = 6. The split point can be 10, 11 or 12 because "AC"
    # repeats; the leftmost gives the deletion of ref[14:20].
    assert split_read(EXAMPLE_REF, EXAMPLE_READ, 0, 40, min_part=5) == ("DEL", 14, 6, "")
    for s in (14, 15, 16):
        assert EXAMPLE_REF[:s] + EXAMPLE_REF[s + 6:] == EXAMPLE_REF[:14] + EXAMPLE_REF[20:]


def test_whole_match_and_too_short_parts():
    ref = EXAMPLE_REF
    assert split_read(ref, ref[3:23], 0, 40, min_part=5) is None
    # The read leaves only 3 bases after the deletion, fewer than min_part.
    r = ref[4:14] + ref[20:30]
    assert split_read(ref, r[:13], 0, 40, min_part=5) is None


def test_against_brute_force():
    rng = random.Random(7)
    checked = 0
    for trial in range(150):
        ref = random_dna(rng, 90)
        L = rng.randint(16, 30)
        kind = rng.choice(["DEL", "INS", "NONE", "MISMATCH"])
        s = rng.randint(20, 50)
        if kind == "DEL":
            alt = ref[:s] + ref[s + rng.randint(1, 25):]
        elif kind == "INS":
            alt = ref[:s] + random_dna(rng, rng.randint(1, 6)) + ref[s:]
        else:
            alt = ref
        start = rng.randint(max(0, s - L + 5), s - 5)
        r = alt[start:start + L]
        if kind == "MISMATCH":
            k = rng.randrange(L)
            r = r[:k] + ("A" if r[k] != "A" else "C") + r[k + 1:]
        call = split_read(ref, r, 0, len(ref), min_part=5, max_ins=8)
        truth = brute_events(ref, r, 0, len(ref), 5, 8, 60)
        if call is not None:
            assert normalize(ref, call) in truth
            ev_kind, pos, size, ins = call
            if ev_kind == "DEL":
                assert r in ref[:pos] + ref[pos + size:]
            else:
                assert r in ref[:pos] + ins + ref[pos:]
        if len(truth) == 1 and call is not None:
            checked += 1
        if len(truth) == 0:
            assert call is None
    assert checked >= 50


def test_simulated_sample():
    rng = random.Random(2009)
    ref = random_dna(rng, 6000)
    # The sample has the deletion of ref[2000:2040] and the insertion of GATTACA before ref[4000].
    sample = ref[:2000] + ref[2040:4000] + "GATTACA" + ref[4000:]
    truth = {normalize(ref, ("DEL", 2000, 40, "")), normalize(ref, ("INS", 4000, 7, "GATTACA"))}

    def to_ref(x):
        if x < 2000:
            return x
        if x < 3960:
            return x + 40
        if x < 3967:
            return None
        return x + 33

    L, mu, sigma = 60, 300, 20
    events = Counter()
    for _ in range(1500):
        f = round(rng.gauss(mu, sigma))
        s = rng.randrange(len(sample) - f)
        anchor = to_ref(s)
        if anchor is None or to_ref(s + L - 1) is None or to_ref(s + L - 1) - anchor != L - 1:
            continue
        mate = revcomp(sample[s + f - L:s + f])  # as sequenced, on the reverse strand
        r = revcomp(mate)
        lo, hi = anchor, anchor + 2 * mu + 100
        if r in ref[lo:hi]:
            continue
        call = split_read(ref, r, lo, hi, min_part=10)
        if call is not None:
            events[normalize(ref, call)] += 1
    top = [e for e, n in events.items() if n >= 3]
    assert set(top) == truth
    assert sum(events.values()) - sum(events[e] for e in truth) <= 1
