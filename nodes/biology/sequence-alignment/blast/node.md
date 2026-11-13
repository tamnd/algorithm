---
tag: 0132T2
kind: algorithm
slug: blast
name: BLAST
aliases:
- Basic Local Alignment Search Tool
- BLASTN
- BLASTP
area: biology/sequence-alignment
level: core
summary: Heuristic database search. Find word pairs that score at least T, extend each one without gaps to a high-scoring segment pair, and report those that score at least S, with E-values.
solves: [database-similarity-search]
model: word-ram
complexity:
  vars: {m: the query length, n: the database length, w: the word length, a: the alphabet size, h: the number of word hits}
  time: {worst: "O(w m a^w + n + h min(m, n))"}
  space: {extra: "O(a^w + m a^w)"}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1990
  people: [Stephen F. Altschul, Warren Gish, Webb Miller, Eugene W. Myers, David J. Lipman]
  note: The 1990 paper in the Journal of Molecular Biology gave the word list, the ungapped extension and the use of the Karlin-Altschul statistics. Gapped BLAST and PSI-BLAST followed in 1997.
prereqs: [seed-and-extend, high-scoring-segment-pair, substitution-matrix]
see_also: [fasta-algorithm, smith-waterman, x-drop-extension, e-value, karlin-altschul-statistics, spaced-seed, blat, hmmer]
sources:
  - paper: doi:10.1016/S0022-2836(05)80360-2
    title: Stephen F. Altschul, Warren Gish, Webb Miller, Eugene W. Myers and David J. Lipman, Basic local alignment search tool, Journal of Molecular Biology 215(3), 1990
    locator: pages 403 to 410, Methods (the word list of words that score at least T, the scan with a table or a finite automaton, the extension with a drop-off, and the choice of w and T)
  - paper: doi:10.1093/nar/25.17.3389
    title: Stephen F. Altschul, Thomas L. Madden, Alejandro A. Schäffer, Jinghui Zhang, Zheng Zhang, Webb Miller and David J. Lipman, Gapped BLAST and PSI-BLAST, a new generation of protein database search programs, Nucleic Acids Research 25(17), 1997
    locator: pages 3389 to 3402, sections The Two-Hit Method, Triggering the Generation of Gapped Alignments, and The Construction and Statistical Evaluation of Gapped Local Alignments
  - paper: doi:10.1073/pnas.87.6.2264
    title: Samuel Karlin and Stephen F. Altschul, Methods for assessing the statistical significance of molecular sequence features by using general scoring schemes, PNAS 87(6), 1990
    locator: pages 2264 to 2268 (the statistics that BLAST uses to set S and to report E-values)
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 15, the section on BLAST
  - book: isbn:9780262101066
    title: Neil C. Jones and Pavel A. Pevzner, An Introduction to Bioinformatics Algorithms, MIT Press, 2004
    locator: Chapter 9, Combinatorial Pattern Matching (the section on BLAST)
---

BLAST (Basic Local Alignment Search Tool) is a heuristic for [database similarity search](/database-similarity-search/): it finds local alignments between a query and each database sequence without filling the full dynamic programming table. It looks up short word pairs that score at least a threshold $T$, extends each word hit without gaps into a [high-scoring segment pair](/high-scoring-segment-pair/) (HSP), and reports the HSPs that score at least $S$, with [E-values](/e-value/) from the [Karlin-Altschul statistics](/karlin-altschul-statistics/). It is much faster than [Smith-Waterman](/smith-waterman/), but it can miss alignments that Smith-Waterman finds, and it has no worst-case guarantee of sensitivity. Gapped BLAST (1997) adds a two-hit trigger and gapped extension.

## In plain words

Two related proteins often share a short stretch of three or four letters that match well. BLAST makes a list of all short words that match some piece of your query well, not only the exact pieces. Then it reads the database once and stops at each place where a word from the list occurs.

At each such place it lines up the query and the database sequence and walks outward in both directions, one letter at a time, adding up the scores. When the total falls too far below the best total so far, it stops, because a good match there is unlikely. If the best stretch it found has a high score, it is a hit. Most of the database never matches a word, so most of it is read only once. A real match that has no good short word in it is never seen.

## The problem

**Input.** A query $q$ of length $m$ and a database of sequences with $n$ letters in total, over an alphabet of size $a$: 20 amino acids (BLASTP) or 4 bases (BLASTN). A [substitution matrix](/substitution-matrix/) $s(\cdot, \cdot)$, such as [BLOSUM62](/blosum-matrix/) or PAM-120 for proteins, or $+5/-4$ or $+1/-2$ for DNA. The parameters are the word length $w$, the word threshold $T$, the drop-off $X$ and the score cutoff $S$.

**Output.** Segment pairs between $q$ and database sequences, with no gaps, whose score is at least $S$. Each is reported with its true score and an E-value. The ideal output is every HSP of score at least $S$. BLAST returns a subset of it. With gapped extension (1997), it returns gapped local alignments under an affine gap cost, written $a + bL$ for a gap of length $L$ in NCBI BLAST (for example $11 + L$ with BLOSUM62).

**What is exact.** The neighborhood list is exact, and every reported score is the true score of the reported segment pair. Which HSPs are found is a heuristic.

## The algorithm

A *word pair* is a word $q[i \ldots i+w-1]$ of the query and a word $y[j \ldots j+w-1]$ of a database sequence $y$; its score is the sum of $s$ over the $w$ aligned pairs. A *hit* is a word pair with score at least $T$. It lies on the diagonal $d = j - i$.

```pseudo id=main
BLAST(q, D, w, T, X, S)
L1  H ← for each word u of length w, the positions i with score(q[i .. i+w−1], u) ≥ T
L2  for each sequence y in D do
L3      for j ← 0 to |y| − w do
L4          for each i in H[y[j .. j+w−1]] do
L5              d ← j − i
L6              if j < covered[d] then continue          ▷ inside the last extension on d
L7              if two-hit mode and no earlier hit on d at distance w .. A then remember j and continue
L8              h ← EXTEND(q, y, i, j, X);  covered[d] ← end of h in y
L9              if score(h) ≥ S then report h with its E-value
```

**The neighborhood (line L1).** For each query word, BLAST builds the words $u$ letter by letter and cuts a prefix as soon as its score plus the best possible score of the remaining positions is below $T$. The 1990 paper stores the list in an array indexed by the word, or in a finite automaton (a Mealy machine) that reads the database once. For DNA it uses only the exact words of the query, often with $w = 12$.

**The extension (line L8).** EXTEND starts with the score of the word pair and walks right along the diagonal, adding $s(q[i'], y[j'])$ for each new pair. It keeps the best running total and stops when the total falls more than $X$ below that best, or at the end of a sequence. It then does the same to the left. The result is the segment from the best left end to the best right end. This is [X-drop extension](/x-drop-extension/) without gaps.

**The two-hit trigger (line L7, 1997).** Gapped BLAST extends a hit only if there is an earlier hit on the same diagonal that does not overlap it and starts at most $A$ letters before it. A hit that overlaps the most recent one is ignored. With two hits required, $T$ can be lower ($T = 11$ instead of $T = 13$ for $w = 3$, with $A = 40$), which finds more true seeds while it starts fewer extensions.

**Gapped extension (1997).** An HSP with a normalized score of at least about 22 bits triggers a gapped extension. Its seed is the central pair of the length-11 segment of the HSP with the highest score. A dynamic program then runs forward and backward from the seed, over the cells whose score is within $X_g$ of the best so far. E-values for gapped scores use $\lambda$ and $K$ estimated beforehand by simulation.

## Example

**The protein neighborhood.** With BLOSUM62, $w = 3$ and $T = 13$, the query word PQG has 9 neighbors:

| word | PQG | PEG | PKG | PRG | PDG, PHG, PMG, PNG, PSG |
|---|---|---|---|---|---|
| score | $7 + 5 + 6 = 18$ | 15 | 14 | 14 | 13 each |

With $T = 12$ there are 16 neighbors and with $T = 11$ there are 21. A lower $T$ gives more hits, more sensitivity and more work.

**A DNA trace.** Take $q = $ TACGGATCCAGTTAC ($m = 15$), $y = $ GGTACGGTTCCAGTAAC, scores $+1/-2$, $w = 4$ with exact words (so $T = 4$), $X = 3$ and $S = 6$. Line L1 lists the 12 words of $q$. The scan of lines L3 and L4 finds five hits, all on diagonal $d = 2$: $(i, j) = (0, 2), (1, 3), (6, 8), (7, 9), (8, 10)$. On this diagonal the pairs from $i = 0$ are

| $i$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pair | T/T | A/A | C/C | G/G | G/G | A/T | T/T | C/C | C/C | A/A | G/G | T/T | T/A | A/A | C/C |

The first hit $(0, 2)$ has the word score 4. Walking right from $i = 4$, the running totals are $1, -1, 0, 1, 2, 3, 4, 5, 3, 4, 5$. The best is 5, first reached at $i = 11$, and the total never falls more than $X = 3$ below the best, so the walk reaches the end. The left walk is empty, because $i = 0$. The HSP is $q[0 \ldots 11]$ against $y[2 \ldots 13]$ with score $4 + 5 = 9 \ge S$, so line L9 reports it. Line L8 sets $\mathrm{covered}[2] = 14$, and line L6 skips the other four hits, which all start before position 14 of $y$. The best ungapped score of this pair is 9, and the Smith-Waterman score with a linear gap cost of 2 or 3 is also 9, so here BLAST finds the optimum with one extension.

**A miss.** Let $q$ be a random DNA sequence of length 64, and let $y$ be $q$ with every eighth base changed ($i = 7, 15, \ldots, 63$). The longest run of matches has 7 bases, so with exact words of length $w = 11$ there is no hit at all, and BLAST reports nothing. The best ungapped alignment covers the first 63 positions, with 56 matches and 7 mismatches, and scores $56 - 14 = 42$ with $+1/-2$. Smith-Waterman finds a score of at least 42. Against $10^9$ bases that score has an E-value near $2 \times 10^{-14}$, so BLAST misses a hit that is far from chance. A [spaced seed](/spaced-seed/) of the same weight would hit some such patterns.

## Correctness

BLAST is a heuristic, so the correct claims are about what it reports and about when it finds an HSP. The proof is in [proofs/correctness.md](proofs/correctness.md). In short:

- **The neighborhood is exact.** Line L1 lists a word if and only if it scores at least $T$ against the query word, because a prefix is cut only when no completion can reach $T$.
- **Scores are true.** Each reported segment pair has the reported score, and that score is at least $S$.
- **Extension with $X = \infty$.** EXTEND returns a segment pair of the highest score among those on the diagonal that contain the word pair. The left and right parts add independently, so the best left end and the best right end can be chosen apart.
- **Completeness under conditions.** In one-hit mode, with $X = \infty$ and without the skip of line L6, each segment pair of score at least $S$ that contains a hit is matched by a reported segment pair on the same diagonal that contains the hit and scores at least as much. With $w = 1$ and $T$ at most the lowest score, every letter pair is a hit, and the best reported score is the MSP score.
- **Where it fails.** A finite $X$, the skip of line L6 and the two-hit rule can each lose an HSP, and a segment pair with no hit is never found, as the example shows.

## Complexity

Let $m$ be the query length, $n$ the total database length, $a$ the alphabet size, $w$ the word length and $h$ the number of hits that reach line L8.

- **Neighborhood.** At most $a^w$ words per query position, each built in $O(w)$ steps, so $O(w m a^w)$ time in the worst case. With pruning, the real list is much shorter for a high $T$. The table takes $O(a^w)$ space for the array plus the position lists, at most $m a^w$ entries.
- **Scan.** Line L3 visits $n - w + 1$ positions per sequence. With the array or the automaton, each lookup is $O(1)$ after the first word (a rolling index), so the scan is $O(n)$ plus the number of hits.
- **Extensions.** One extension takes time proportional to its length, at most $\min(m, n)$. So the total is $O(w m a^w + n + h \min(m, n))$ in the worst case.
- **The number of hits.** In the worst case $h = \Theta(mn)$, for example for a run of one letter against another run of it. For random sequences with independent letters, the expected number of hits is $mn$ times the probability that a random word pair scores at least $T$. This expected count, not a worst-case bound, is why BLAST is fast in practice.

The 1990 paper reports that with $w = 4$ and $T = 17$ for proteins, BLAST missed about a fifth of the MSPs of score 55 in its tests; it is a trade of sensitivity for speed. The Gapped BLAST paper reports that the new program, with the two-hit method and the gapped stage, runs about three times faster than the original one.

## Properties

- **Heuristic.** No worst-case guarantee of sensitivity: a significant alignment with no hit is missed.
- **Sound.** Every reported alignment and score is real.
- **Deterministic.** The same input and parameters give the same output.
- **Query-indexed.** The index is built from the query, and the database is read once per query. Database-indexed tools such as [BLAT](/blat/) do the opposite.
- **Scores are local and ungapped in the 1990 version.** Gaps come only from the 1997 gapped stage.

## Variants and improvements

- **Gapped BLAST** (1997). The two-hit trigger and gapped X-drop extension, with λ and K for gapped scores from simulation.
- **PSI-BLAST** (1997). After each round, build a position-specific scoring matrix from the significant hits and search again with it. This finds distant members of a family.
- **Translated searches.** BLASTX, TBLASTN and TBLASTX compare through the six reading frames of DNA.
- **Megablast.** Long exact words (28 by default) and a greedy gapped extension, for near-identical DNA.
- **Discontiguous megablast.** A [spaced seed](/spaced-seed/) instead of a contiguous word, for more sensitivity on cross-species DNA.
- **Defaults today.** The NCBI BLAST+ programs use $w = 3$ for BLASTP and $w = 11$ for the blastn task of BLASTN; the default task of BLASTN is megablast, with $w = 28$. These are later defaults; the 1990 paper used $w = 4$ for proteins and $w = 12$ for DNA.

## When to use it

Use BLAST to search one or a few queries against a large protein or DNA database when you want significant local matches and their E-values fast. Use [Smith-Waterman](/smith-waterman/) (SSEARCH) when you must not miss a hit and the database is small enough. Use a profile method, PSI-BLAST or [HMMER](/hmmer/), for remote homologs. For mapping many short reads to one genome, use a read mapper with an index of the genome, such as [BWA](/bwa/) or [minimap2](/minimap2/).

## Pitfalls

- **Treating "no hit" as "no homolog".** The miss example has an E-value near $10^{-14}$ and BLAST finds nothing. Lower $w$ or $T$, use a spaced seed, or use Smith-Waterman to check.
- **Low-complexity queries.** Runs and short repeats give many hits and high scores by chance. Masking (DUST for DNA, SEG for proteins) removes them before the search.
- **E-values across databases.** The E-value grows with the database size, so a hit has different E-values in different databases. Compare [bit scores](/bit-score/) instead.
- **Overlapping hits.** Without line L6 each hit on a long match starts its own extension, the work grows and the output has copies.
- **Mixing up parameter sets.** λ and K belong to one matrix, one set of gap costs and one composition. Using the ungapped values for gapped scores makes E-values too small.
- **Word size and the 1990 values.** Quotes of "w = 3 and w = 11" are the modern defaults of BLASTP and of the blastn task, not the values of the 1990 paper.

## Implementations

## History

Before BLAST, FASTA (Lipman and Pearson 1985, Pearson and Lipman 1988) already used short word matches to speed up database search. Altschul, Gish, Miller, Myers and Lipman published BLAST in 1990. It added the list of neighborhood words that score at least $T$, which let short protein words with substitutions seed a match, and it based its cutoff on the statistics of Karlin and Altschul from the same year. The 1990 paper defined the maximal segment pair and the locally maximal segment pairs that BLAST reports. In 1997 Altschul and coworkers published Gapped BLAST and PSI-BLAST, with the two-hit method, gapped extension and iterated profile search. BLAST became a standard tool of molecular biology, and the 1990 paper is one of the most cited papers in science.

## References
