---
tag: 2JME3F
kind: problem
slug: database-similarity-search
name: Database similarity search
aliases:
- homology search
- sequence database search
area: biology/sequence-alignment
level: core
summary: Given a query sequence and a database of sequences, find the database sequences with a significant local alignment to the query, ranked by score or E-value.
prereqs: [local-alignment, smith-waterman]
see_also: [blast, fasta-algorithm, seed-and-extend, e-value, hmmer, read-mapping, alignment-free-comparison, edit-distance-seth-lower-bound]
sources:
  - paper: doi:10.1016/S0022-2836(05)80360-2
    title: Stephen F. Altschul, Warren Gish, Webb Miller, Eugene W. Myers and David J. Lipman, Basic local alignment search tool, Journal of Molecular Biology 215(3), 1990
    locator: pages 403 to 410 (the search for maximal segment pairs between a query and a database, and the statistics that set the cutoff)
  - paper: doi:10.1093/nar/25.17.3389
    title: Stephen F. Altschul, Thomas L. Madden, Alejandro A. Schäffer, Jinghui Zhang, Zheng Zhang, Webb Miller and David J. Lipman, Gapped BLAST and PSI-BLAST, a new generation of protein database search programs, Nucleic Acids Research 25(17), 1997
    locator: pages 3389 to 3402 (gapped database search, its statistics, and the iterated profile search PSI-BLAST)
  - paper: doi:10.1073/pnas.85.8.2444
    title: William R. Pearson and David J. Lipman, Improved tools for biological sequence comparison, PNAS 85(8), 1988
    locator: pages 2444 to 2448 (FASTA and the rapid search of a protein or DNA library)
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 15, Sequence databases and their uses (database search, FASTA and BLAST)
  - book: isbn:9780521629713
    title: Richard Durbin, Sean R. Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, Cambridge University Press, 1998
    locator: Chapter 2, Pairwise alignment (local alignment, heuristic search and the significance of scores)
---

Database similarity search is the problem of finding, for one query sequence, the sequences in a large database that share a significant [local alignment](/local-alignment/) with it, and of ranking them by score or by [E-value](/e-value/). [Smith-Waterman](/smith-waterman/) on each database sequence solves it exactly in time proportional to the product of the query and database lengths. That is too slow for databases of billions of letters, so the common tools, such as [BLAST](/blast/) and [FASTA](/fasta-algorithm/), are heuristics that can miss a match. Biologists use the search to find homologs, sequences that share an ancestor, which is why the problem is also called homology search.

## In plain words

You have a new gene or protein and want to know what it is like. A public database holds hundreds of millions of known sequences. You ask: which of them look like mine, in some part, more than chance would explain?

The answer is a list. Each line names a database sequence, shows the best matching part of it next to your sequence, and gives a score and a number that says how often a match this good would show up by chance. The top of the list is the most likely relative. To compare your sequence with every database sequence in full takes too long, so most tools first look for short exact matches and only look closer where they find one.

## Definition

**Input.**

- A query $q$ of length $m$ over an alphabet $\Sigma$: the four DNA bases or the 20 amino acids.
- A database $\mathcal{D} = \{y_1, \ldots, y_r\}$ of $r$ sequences with a total length of $N = \sum_k |y_k|$ letters.
- A scoring scheme for local alignment: a [substitution matrix](/substitution-matrix/) $s(a, b)$, such as [BLOSUM62](/blosum-matrix/) for proteins or $+1/-2$ for DNA, and a gap model. This page uses the [affine gap penalty](/affine-gap-penalty/) $g(L) = d + (L - 1)e$ for a gap of length $L$. NCBI BLAST writes the same cost as $a + bL$ (for example $a = 11$ and $b = 1$ with BLOSUM62), which is $d = a + b$ and $e = b$.
- A threshold: a score $S$, or an E-value $E_0$.

**Output.** Each database sequence $y_k$ whose best local alignment score $\mathrm{SW}(q, y_k)$ is at least $S$ (or whose E-value is at most $E_0$), with an alignment that reaches the score, sorted by score. A common variant asks for the top $t$ sequences only.

**Exact and heuristic answers.** An *exact* method returns exactly the sequences of the definition. A *heuristic* returns a list of true alignments with true scores, but it can leave out sequences that qualify. Its quality is measured by *sensitivity*, the fraction of the qualifying (or of the truly homologous) sequences that it finds, and by its speed. BLAST and FASTA are heuristics of this kind. They have no worst-case guarantee on sensitivity.

**Significance.** A raw score means little without the scoring scheme and the lengths. The [Karlin-Altschul statistics](/karlin-altschul-statistics/) turn a score $S$ into an E-value $E = K m N e^{-\lambda S}$, the expected number of chance hits at least as good in a search of this size. The search reports what passes $E_0$, so the threshold depends on $N$: a score that is significant against a small database can be noise against a large one.

## Variants

- **Protein against protein, DNA against DNA.** BLASTP and BLASTN in BLAST terms.
- **Translated search.** Compare a DNA sequence with a protein database through the six reading frames (BLASTX), a protein with a translated DNA database (TBLASTN), or both translated (TBLASTX).
- **Profile search.** Replace the query by a profile of a protein family: a [position-specific scoring matrix](/position-specific-scoring-matrix/) (PSI-BLAST builds one by iterated search) or a [profile HMM](/profile-hmm/) (as in [HMMER](/hmmer/)). This finds more distant homologs.
- **Many short queries.** Map millions of reads against one reference genome with few differences. This is [read mapping](/read-mapping/), and it uses an index of the reference.
- **All against all.** Compare each sequence of a set with each other one, for example to cluster a proteome.
- **Alignment-free search.** Rank database sequences by shared [k-mers](/kmer/) or sketches instead of alignments. See [alignment-free comparison](/alignment-free-comparison/).

## Examples

**A small search.** A random DNA query $q$ of length $m = 40$ is searched against five random sequences of length 200 each ($N = 1000$). Into sequence 2 we plant a copy of 30 letters of $q$ with three substitutions and one deletion. The scores are $+1/-2$, and the gapped score uses a linear gap cost of 3 per letter. The E-value below uses the ungapped parameters $\lambda = 1.3327$ and $K = 0.621$ of this scheme with uniform bases, applied to the best ungapped score (the MSP):

| sequence | best ungapped score | E-value | Smith-Waterman score |
|---|---|---|---|
| 0 | 7 | 2.21 | 7 |
| 1 | 6 | 8.36 | 6 |
| 2 | 13 | 0.00074 | 18 |
| 3 | 6 | 8.36 | 6 |
| 4 | 8 | 0.58 | 8 |

Only sequence 2 is significant. The four random sequences each have a chance match of 6 to 8 points, which is what the statistics predict for 40 by 1000 letters. The gapped score of sequence 2 is higher because one gap of cost 3 joins two ungapped pieces.

**A heuristic miss.** In the planted copy the longest run with no difference has 7 letters. A BLAST-style search with exact words of length $w = 7$ finds the HSP of score 13 in sequence 2. With $w = 8$ or $w = 11$ it finds nothing in any sequence, while Smith-Waterman finds the score 18. So the answer of a heuristic depends on its seed length, and an empty result is not proof that no match exists.

## Known algorithms

| method | type | cost and guarantee |
|---|---|---|
| [Smith-Waterman](/smith-waterman/) on each sequence (SSEARCH) | exact | $O(mN)$ time in the worst case, $O(m)$ space for the scores |
| [FASTA](/fasta-algorithm/) | heuristic | ktup lookup and diagonal scan, then a banded DP on the best regions; no sensitivity guarantee |
| [BLAST](/blast/), Gapped BLAST | heuristic | word hits, X-drop extension, gapped extension; no sensitivity guarantee |
| PSI-BLAST | heuristic | BLAST with a position-specific matrix built from earlier rounds |
| [HMMER](/hmmer/) | heuristic filters, then exact profile scores | a pipeline of filters, then the profile HMM score of the survivors |
| [BLAT](/blat/) and other index-based tools | heuristic | an index of the database; fast for near-identical matches |

All the heuristics follow [seed and extend](/seed-and-extend/). They differ in the kind of seed, in how many hits they ask for before they extend, and in the extension.

## Bounds

- **Exact search.** The Smith-Waterman recurrence fills an $m \times |y_k|$ table for each database sequence, so the total time is $\Theta(mN)$ in every case, and the score needs $O(m)$ space when the table is filled row by row. Hardware speeds up the constant (vector instructions and GPUs), not the order.
- **Conditional lower bounds.** No algorithm is known that computes local alignment scores for general scoring schemes in time $O((mN)^{1 - \varepsilon})$. For the close global measures, edit distance and the longest common subsequence, such an algorithm would refute the [strong exponential time hypothesis](/strong-exponential-time-hypothesis/) (Backurs and Indyk 2015; Abboud, Backurs and Vassilevska Williams 2015). See [the edit distance bound](/edit-distance-seth-lower-bound/) and [the LCS bound](/lcs-seth-lower-bound/).
- **Heuristics.** For a seed of exact $k$-mers in a uniform random database, the expected number of chance hits is $mN\sigma^{-k}$ for an alphabet of size $\sigma$, so the expected work after a linear scan is small when $k$ is large. This is an expected bound under a random model. On repetitive input the hits can number $\Theta(mN)$, and on any input a heuristic can miss qualifying sequences.
- **Reading the input.** Any method that returns exact answers must read the whole database in the worst case, so it takes $\Omega(m + N)$ time.

## Reductions

- **To local alignment.** The problem is $r$ instances of local alignment, one per database sequence. Equivalently, join the database into one text with a separator letter that scores $-\infty$ against everything, and run one local alignment of $q$ against it.
- **To the maximum subarray problem.** With no gaps, the best score on one diagonal of $q$ against $y_k$ is a [maximum subarray](/maximum-subarray-problem/) of the scores on that diagonal. The best ungapped score of a pair is the maximum over the $m + |y_k| - 1$ diagonals. This is the MSP of a [high-scoring segment pair](/high-scoring-segment-pair/).
- **From approximate string matching.** When all scores are those of the unit cost edit distance, finding the database positions that match $q$ with at most $e$ differences is approximate string matching, and filters for it ([q-gram filtering](/q-gram-filtering/), [pigeonhole filtering](/pigeonhole-filtering/)) become lossless seeds.

## Applications

- Annotation of new genes and proteins by the function of their best matches.
- Search for members of a protein family, and for distant homologs with profile searches.
- Classification of reads in metagenomics by their best database match.
- Checks for contamination, vector sequence or primer specificity against a reference.
- The first step of many pipelines: clustering of proteomes, orthology inference and multiple alignment of the hits.

## References
