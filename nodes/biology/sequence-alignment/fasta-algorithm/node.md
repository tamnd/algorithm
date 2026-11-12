---
tag: VK9YGQ
kind: algorithm
slug: fasta-algorithm
name: FASTA
aliases:
- FASTA heuristic search
- FASTA search algorithm
area: biology/sequence-alignment
level: core
summary: Heuristic database search of Pearson and Lipman. Find ktup matches with a lookup table, score diagonal regions (init1), join them (initn), then run Smith-Waterman in a band (opt).
solves: [database-similarity-search]
model: word-ram
complexity:
  vars: {m: the query length, n: the database length, r: the number of database sequences, k: the ktup length, a: the alphabet size, h: the number of ktup matches, b: the band width}
  time: {worst: "O(a^k + m + n + h + r b m)"}
  space: {extra: "O(a^k + m + n)"}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1988
  people: [William R. Pearson, David J. Lipman]
  note: Lipman and Pearson published the protein program FASTP in 1985. Pearson and Lipman described FASTA, with initn and the banded opt score, in PNAS in 1988.
prereqs: [seed-and-extend, smith-waterman]
see_also: [blast, banded-smith-waterman, database-similarity-search, dot-matrix-plot, e-value, kmer-index, high-scoring-segment-pair, pam-matrix]
sources:
  - paper: doi:10.1073/pnas.85.8.2444
    title: William R. Pearson and David J. Lipman, Improved tools for biological sequence comparison, PNAS 85(8), 1988
    locator: pages 2444 to 2448 (the ktup lookup, the scores init1, initn and opt, and the band around the best initial region)
  - paper: "David J. Lipman and William R. Pearson, Rapid and sensitive protein similarity searches, Science 227(4693), 1985, pages 1435 to 1441"
    title: Lipman and Pearson 1985 (FASTP)
    locator: the lookup of ktup matches and the diagonal method for protein database search
  - paper: "William R. Pearson, Rapid and sensitive sequence comparison with FASTP and FASTA, Methods in Enzymology 183, 1990, pages 63 to 98"
    title: Pearson 1990
    locator: pages 71 to 73, the four steps (the diagonal method with its distance rule, rescoring with PAM250, joining with a penalty of 20, and the optimization in a band of 32 residues)
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 15, the section on FASTA
  - book: isbn:9780521629713
    title: Richard Durbin, Sean R. Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, Cambridge University Press, 1998
    locator: Chapter 2, the section on heuristic alignment algorithms (FASTA)
---

FASTA is a heuristic for [database similarity search](/database-similarity-search/) by Pearson and Lipman: for each database sequence it finds the short exact matches of length *ktup* with the query, scores the diagonals where they cluster, and runs a banded [Smith-Waterman](/smith-waterman/) only around the best one. It computes three scores per sequence: *init1* for the best single ungapped region, *initn* for the best chain of regions, and *opt* for the banded local alignment. The library is ranked by these scores. Like [BLAST](/blast/), it is a [seed and extend](/seed-and-extend/) method that can miss alignments, and it has no worst-case guarantee of sensitivity.

## In plain words

Picture a grid with the query along one side and a database sequence along the other. Put a dot wherever two letters match. A real similarity shows up as a line of dots along a diagonal, with a few breaks.

FASTA finds these lines fast. It does not look at single letters but at short words of one or two letters for proteins, or a few more for DNA, and uses a table to find every place where a word of the query occurs. It counts the dots on each diagonal and keeps the ten densest stretches. It scores the best stretch with a real scoring table. Then it tries to join nearby stretches into one longer match, with a cost for each jump. Last, it does a careful alignment, but only in a narrow strip around the best stretch.

## The problem

**Input.** A query $q$ of length $m$ and a library of $r$ sequences with $n$ letters in total, over the 20 amino acids or the 4 DNA bases. A [substitution matrix](/substitution-matrix/) $s(\cdot, \cdot)$: the 1988 programs used [PAM250](/pam-matrix/) for proteins, and the code on this page uses $+5/-4$ for DNA. A gap model for the last step: the code uses a linear cost $g(L) = dL$, and the FASTA programs use affine gap costs. The parameters are ktup (1 or 2 for proteins, 4 to 6 for DNA), the join penalty (20 in Pearson's description) and the band width (32).

**Output.** For each library sequence $y$, the scores init1, initn and opt, and the library sorted by one of them, with the best alignments shown.

**What is exact.** The ktup matches are exact, init1 is the exact best score of a trimmed region, and opt is the exact best local alignment score inside the band. Which part of the table is examined is a heuristic.

## The algorithm

A *ktup match* is a pair $(i, j)$ with $q[i \ldots i+k-1] = y[j \ldots j+k-1]$, on diagonal $d = j - i$. A *region* is an ungapped stretch $(i, j, \text{length}, \text{score})$ on one diagonal.

```pseudo id=main
FASTA-PAIR(q, y, k, s, value, penalty, gap, width)
L1  M ← all ktup matches (i, j), from a lookup table of the k-letter words of q
L2  R ← the 10 best regions: on each diagonal, join matches by the distance rule
L3  rescore each region of R with s and trim it to its best-scoring part
L4  init1 ← the best trimmed score;  c ← the diagonal of that region
L5  initn ← the best score of a chain of disjoint regions in order, minus penalty per join
L6  opt ← the Smith-Waterman score over the band of diagonals [c − width/2, c + width/2]
    return (init1, initn, opt)
```

**Line L1.** The query is indexed once in an array of the $a^k$ possible words, each with its list of positions. Scanning $y$ then gives every match in time linear in $|y|$ plus the number of matches.

**Line L2, the diagonal method.** On each diagonal, the matches are taken in order. A region starts at a match with the score *value* (Pearson's FASTP uses 16 for ktup 2 with proteins, and for DNA the value is a constant, the square of ktup in Pearson's description). A later match at distance $g$ after the end of the region joins it if $g$ is at most the current score, and the score becomes $\text{score} - g + \text{value}$. Otherwise the region is closed and a new one starts. Only the 10 best regions are kept.

**Line L3, rescoring.** Each region is rescored letter by letter with $s$ and trimmed to its best-scoring stretch, by the scan of [Kadane's algorithm](/kadane-algorithm/). Each trimmed region is a [high-scoring segment pair](/high-scoring-segment-pair/) inside the stretch.

**Line L5, joining.** Two regions can follow each other in a chain when the second starts after the first ends, in both $q$ and $y$. A dynamic program over the regions sorted by start position gives the best chain, with the penalty subtracted for each join. This is initn, which ranks the library in the 1988 programs.

**Line L6, the band.** A [banded Smith-Waterman](/banded-smith-waterman/) fills only the cells whose diagonal $j - i$ lies within $\text{width}/2$ of $c$. Cells outside the band count as $-\infty$, and the first row and column are 0.

## Example

Take $q = $ CTGACCTAGGATCAGT ($m = 16$) and $y = $ GCTGACCTATTCGGATCAGTA, ktup $k = 2$, DNA scores $+5/-4$, the region value 4, the penalty 20, a linear gap cost of 4 per letter, and a band of width 32. The subject is the query with three letters, TTC, put in the middle, and with one more letter at each end.

**Line L1.** There are 22 ktup matches. Seven lie on diagonal 1, at $i = 0, \ldots, 6$ (the words CT, TG, GA, AC, CC, CT, TA of CTGACCTA), seven on diagonal 4, at $i = 8, \ldots, 14$ (GGATCAGT), and eight are single matches on eight other diagonals.

**Line L2.** On diagonal 1, the seven matches overlap, so each one has distance 0 and adds 4: the region covers 8 letters with score 28. Diagonal 4 gives the same: 8 letters and score 28. The single matches give eight regions of score 4, for ten in all.

**Line L3.** Rescored with $+5/-4$, the two long regions are 8 matching letters each, score 40. Each 2-letter region scores 10.

| region | query part | subject part | diagonal | trimmed score |
|---|---|---|---|---|
| A | $q[0..7]$ CTGACCTA | $y[1..8]$ | 1 | 40 |
| B | $q[8..15]$ GGATCAGT | $y[12..19]$ | 4 | 40 |
| others | 2 letters each | | various | 10 |

**Line L4.** $\text{init1} = 40$, and the band is centered on diagonal 1 (the first of the two best regions).

**Line L5.** A ends at $q[7]$ and $y[8]$, and B starts at $q[8]$ and $y[12]$, so A then B is a chain: $40 + 40 - 20 = 60$. A small region adds $10 - 20 < 0$, so it is never worth joining. So $\text{initn} = 60$.

**Line L6.** The band covers the diagonals $-15$ to $17$, so it holds both A and B. The best local alignment aligns all 16 letters of $q$ with one gap of 3 letters: $80 - 3 \cdot 4 = 68$. So $\text{opt} = 68$, the same as the full Smith-Waterman score. With a gap cost of 6 or 8 per letter, opt is 62 or 56, and it again equals the full score.

The three scores tell different things: init1 sees one ungapped piece, initn sees both pieces with a fixed cost for the jump, and opt pays for the real gap.

## Correctness

FASTA is a heuristic, so the claims are the order of its scores and the exactness of each step. The proof is in [proofs/correctness.md](proofs/correctness.md). In short:

- Line L1 finds exactly the ktup matches.
- Line L3 returns the highest-scoring stretch of each region.
- Line L5 returns the best chain score over all chains of the kept regions.
- $\text{init1} \le \text{initn}$, since one region is a chain.
- $\text{init1} \le \text{opt} \le \mathrm{SW}(q, y)$: the best region lies on the center diagonal of the band, so it is one of the alignments that the banded DP scores, and the band only removes alignments.
- If the band holds all diagonals, then $\text{opt} = \mathrm{SW}(q, y)$.

**What can be lost.** A pair with no ktup match gets $0$ for all three scores: ACACACACAC against AGAGAGAGAG has no common 2-letter word, but Smith-Waterman with $+5/-4$ scores ACACACACA against AGAGAGAGA as $5 \cdot 5 - 4 \cdot 4 = 9$. An alignment that leaves the band is cut: if the second half of a match is shifted by 12 diagonals, a band of width 8 misses it, while a band of width 32 finds it. And a sequence with a low initn is not looked at in detail, even if its opt score would be high.

## Complexity

Let $m$ be the query length, $n$ the library length, $r$ the number of library sequences, $a$ the alphabet size, $k$ the ktup, $h$ the number of ktup matches and $b$ the band width.

- **The lookup table.** $O(a^k + m)$ time and space, built once per query.
- **The scan and the regions.** $O(|y| + h_y)$ for a sequence $y$ with $h_y$ matches, since the matches come out in order of $j$, and each one is placed on its diagonal in $O(1)$. Over the library, $O(n + h)$.
- **Rescoring and joining.** Ten regions, each at most $\min(m, |y|)$ long, and a join DP over ten regions: $O(\min(m, |y|))$ per sequence.
- **The band.** $O(b\, m)$ cells per sequence, so $O(r b m)$ if opt is computed for every sequence.

The worst case is $O(a^k + m + n + h + r b m)$ time. In the worst case $h = \Theta(mn)$ (a run of one letter against a run of it). For random sequences with uniform letters the expected number of ktup matches is about $mn / a^k$. For a protein query of 300 residues against $10^8$ residues with ktup 2 that is $7.5 \times 10^7$ matches, which is why ktup 1 is much slower than ktup 2.

## Properties

- **Heuristic.** No worst-case guarantee: an alignment with no ktup match, or outside the band, is missed.
- **Sound scores.** init1 and opt are scores of real alignments of $q$ and $y$. initn is the score of real regions with a fixed join cost, not of one alignment.
- **Deterministic.**
- **Query-indexed.** The table is built from the query and the library is read once.

## Variants and improvements

- **ktup.** ktup 1 for proteins is more sensitive and slower than ktup 2. For DNA, ktup 4 to 6.
- **Band width.** Later versions of FASTA use a band of 16 for ktup 2 and for DNA, and 32 for ktup 1.
- **Statistics.** Later FASTA versions estimate E-values from the distribution of the opt scores of the unrelated sequences in the same search.
- **Full Smith-Waterman.** The same package includes SSEARCH, the exact search, for when sensitivity matters more than time.
- **Other programs of the package.** TFASTA, FASTX and FASTY compare protein with translated DNA. LFASTA shows all local similarities of two sequences.

## When to use it

Use FASTA, like BLAST, for a fast search of a library with one query when some misses are acceptable. Its ktup 1 mode for proteins finds some weak similarities that word-based searches with longer words miss. For an exact search use Smith-Waterman (SSEARCH). For most protein and DNA database searches today BLAST is the more common choice; for distant homologs, use a profile method such as [HMMER](/hmmer/).

## Pitfalls

- **Comparing init1, initn and opt across libraries.** Raw scores depend on the lengths and the composition. Use the E-values that the program computes.
- **A band too narrow.** If an indel of more than half the band width lies between the two parts of a match, opt cannot join them.
- **Reading initn as an alignment score.** initn charges a fixed penalty per join, not the real gap cost. It can be above opt.
- **The value of a ktup match.** For proteins it comes from the substitution matrix; for DNA it is a constant. Using a constant for proteins changes which regions are kept.
- **Low-complexity regions.** As with any word method, repeats give many matches and false regions.

## Implementations

## History

Wilbur and Lipman (1983) used ktup matches to speed up the comparison of sequences. Lipman and Pearson published FASTP in Science in 1985, a protein database search with a ktup lookup table and the diagonal method. Pearson and Lipman published FASTA in PNAS in 1988, which added DNA searches, the initn score that joins regions, and the optimized score in a band. Pearson's chapter in Methods in Enzymology (1990) gives the steps in detail. The name FASTA also became the name of the plain text file format for sequences that the programs read, which is now used almost everywhere in bioinformatics.

## References
