# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximal-mappable-prefix-alignment/. The authors are listed in prov/YWMA4M.jsonl.

import random
import re
from itertools import product

from maximal_mappable_prefix_alignment import (MATCH, MISMATCH, Alignment, junction_penalty, mmp,
                                               mmp_align, stitch, suffix_array)

G = "CCCT" + "CGATTCAAAT" + "GTGGCCGGGAGTAG" + "GACGGCAGCA" + "GAGA"


def dna(rng, n, alphabet="ACGT"):
    return "".join(rng.choice(alphabet) for _ in range(n))


def occurrences(g, p):
    return [i for i in range(len(g) - len(p) + 1) if g.startswith(p, i)]


def cigar_score(read, g, pos, cigar):
    """Score an alignment from its CIGAR, and check that it uses the whole read."""
    x, y, score, last_m = 0, pos, 0, None
    for n, op in re.findall(r"(\d+)([MNS])", cigar):
        n = int(n)
        if op == "S":
            x += n
        elif op == "M":
            score += sum(MATCH if read[x + j] == g[y + j] else MISMATCH for j in range(n))
            x, y = x + n, y + n
        else:
            score -= junction_penalty(g, y, y + n)
            y += n
    assert x == len(read)
    return score


def test_worked_example():
    read = "ATTCAAAT" + "GACGGCAG"
    sa = suffix_array(G)
    trace = []
    aln = mmp_align(read, G, sa, s_min=5, min_intron=10, trace=trace)
    assert trace == [(0, 9, 1), (10, 6, 1)]
    assert mmp(G, sa, read) == (9, [6])
    assert mmp(G, sa, read[10:]) == (6, [30])
    assert aln == Alignment(14, 6, "8M14N8M")
    # The other place for the junction, one base later, also has 16 matches but a TG-GG motif.
    assert G[14:28].startswith("GT") and G[14:28].endswith("AG")
    assert junction_penalty(G, 15, 29) == 8
    assert cigar_score(read, G, 6, "9M14N7M") == 8
    # Without the second seed the read cannot cross the intron and is soft-clipped.
    assert stitch(read, G, [6], 10) == Alignment(9, 6, "9M7S")


def test_mmp_against_brute_force():
    rng = random.Random(1)
    for _ in range(400):
        g = dna(rng, rng.randint(1, 60), rng.choice(["AC", "ACGT"]))
        s = dna(rng, rng.randint(1, 15), "ACGT")
        sa = suffix_array(g)
        l = max((m for m in range(len(s) + 1) if s[:m] in g), default=0)
        want = (l, occurrences(g, s[:l])) if l else (0, [])
        assert mmp(g, sa, s) == want


def brute_stitch(read, g, D, lo, hi):
    best = None
    L = len(read)
    for s in range(L):
        for e in range(s, L):
            for ds in product(D, repeat=e - s + 1):
                if any(not 0 <= s + j + d < len(g) for j, d in enumerate(ds)):
                    continue
                sc, ok = 0, True
                for j, d in enumerate(ds):
                    x = s + j
                    sc += MATCH if read[x] == g[x + d] else MISMATCH
                    if j and d != ds[j - 1]:
                        if not lo <= d - ds[j - 1] <= hi:
                            ok = False
                            break
                        sc -= junction_penalty(g, x + ds[j - 1], x + d)
                if ok and (best is None or sc > best):
                    best = sc
    return best


def test_stitch_against_brute_force():
    rng = random.Random(2)
    for _ in range(80):
        g = dna(rng, 30, rng.choice(["ACGT", "AGT"]))
        read = dna(rng, rng.randint(1, 6), "AGT")
        D = sorted(rng.sample(range(-3, 25), rng.randint(1, 3)))
        want = brute_stitch(read, g, D, 3, 15)
        got = stitch(read, g, D, 3, 15)
        if want is None or want <= 0:
            assert got is None
        else:
            assert got.score == want
            assert cigar_score(read, g, got.pos, got.cigar) == want


def gene(rng, n_exons):
    """A genome with one gene: the genome, the exon intervals and the transcript."""
    parts, exons, pos = [dna(rng, 200)], [], 200
    for e in range(n_exons):
        ex = dna(rng, rng.randint(60, 120))
        exons.append((pos, pos + len(ex)))
        parts.append(ex)
        pos += len(ex)
        if e < n_exons - 1:
            intron = "GT" + dna(rng, rng.randint(50, 300)) + "AG"
            parts.append(intron)
            pos += len(intron)
    parts.append(dna(rng, 200))
    g = "".join(parts)
    return g, exons, "".join(g[a:b] for a, b in exons)


def truth(exons, start, L):
    """The genome position and CIGAR of the transcript substring [start, start + L)."""
    ops, t, pos, prev_end = [], 0, None, None
    for a, b in exons:
        lo = max(start, t)
        hi = min(start + L, t + b - a)
        if lo < hi:
            g0 = a + lo - t
            if pos is None:
                pos = g0
            else:
                ops.append(f"{g0 - prev_end}N")
            ops.append(f"{hi - lo}M")
            prev_end = a + hi - t
        t += b - a
    return pos, "".join(ops)


def test_exact_unspliced_reads_get_the_full_score():
    rng = random.Random(3)
    g = dna(rng, 3000)
    sa = suffix_array(g)
    for _ in range(100):
        p = rng.randrange(len(g) - 50)
        read = g[p:p + 50]
        if len(occurrences(g, read)) != 1:
            continue
        assert mmp_align(read, g, sa) == Alignment(50, p, "50M")


def test_spliced_reads_are_placed_exactly_unless_an_overhang_is_short():
    rng = random.Random(4)
    long_ok = long_total = short_ok = short_total = 0
    for _ in range(6):
        g, exons, tx = gene(rng, 4)
        sa = suffix_array(g)
        for _ in range(40):
            start = rng.randrange(len(tx) - 50)
            read = tx[start:start + 50]
            aln = mmp_align(read, g, sa, min_intron=20, max_intron=1000)
            assert aln is not None
            assert aln.score == cigar_score(read, g, aln.pos, aln.cigar)
            want = truth(exons, start, 50)
            ok = (aln.pos, aln.cigar) == want
            if min(int(m) for m in re.findall(r"(\d+)M", want[1])) >= 12:
                long_ok, long_total = long_ok + ok, long_total + 1
            else:
                short_ok, short_total = short_ok + ok, short_total + 1
    # Measured with this seed: 183 of 183 reads whose blocks all have 12 bases or more,
    # and 16 of 57 reads with a shorter block, are placed exactly.
    assert (long_ok, long_total, short_ok, short_total) == (183, 183, 16, 57)


def test_reads_with_mismatches_are_found():
    rng = random.Random(5)
    found = total = 0
    for _ in range(6):
        g, exons, tx = gene(rng, 3)
        sa = suffix_array(g)
        for _ in range(30):
            start = rng.randrange(len(tx) - 50)
            read = list(tx[start:start + 50])
            for x in rng.sample(range(50), 2):
                read[x] = rng.choice([c for c in "ACGT" if c != read[x]])
            read = "".join(read)
            total += 1
            aln = mmp_align(read, g, sa)
            found += aln is not None and aln.pos == truth(exons, start, 50)[0]
    assert found >= 0.85 * total


def test_random_reads_are_unmapped():
    rng = random.Random(6)
    g = dna(rng, 3000)
    sa = suffix_array(g)
    for _ in range(100):
        assert mmp_align(dna(rng, 50), g, sa) is None
