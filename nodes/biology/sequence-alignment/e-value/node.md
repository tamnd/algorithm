---
tag: 9Q4D76
kind: concept
slug: e-value
name: E-value
aliases:
- expect value
- expectation value of a hit
area: biology/sequence-alignment
level: core
summary: The expected number of alignments with score at least S that a search of the same size finds by chance between unrelated sequences. E = Kmn e^(-λS); smaller is more significant.
prereqs: [high-scoring-segment-pair, poisson-distribution]
see_also: [bit-score, karlin-altschul-statistics, blast, database-similarity-search, high-scoring-segment-pair, fasta-algorithm]
sources:
  - paper: doi:10.1073/pnas.87.6.2264
    title: Samuel Karlin and Stephen F. Altschul, Methods for assessing the statistical significance of molecular sequence features by using general scoring schemes, PNAS 87(6), 1990
    locator: pages 2264 to 2268 (the Poisson number of high-scoring segments with mean K m n e^(-λS), and the P-value of the best score)
  - paper: doi:10.1093/nar/25.17.3389
    title: Stephen F. Altschul, Thomas L. Madden, Alejandro A. Schäffer, Jinghui Zhang, Zheng Zhang, Webb Miller and David J. Lipman, Gapped BLAST and PSI-BLAST, a new generation of protein database search programs, Nucleic Acids Research 25(17), 1997
    locator: pages 3389 to 3402, Statistical Preliminaries (E-values for gapped alignments with λ and K estimated by simulation, and the edge-effect correction)
  - paper: "Stephen F. Altschul and Warren Gish, Local alignment statistics, Methods in Enzymology 266, 1996, pages 460 to 480"
    title: Altschul and Gish 1996
    locator: the fitted λ and K of gapped scores and the edge-effect correction with effective lengths
  - book: isbn:9780521629713
    title: Richard Durbin, Sean R. Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, Cambridge University Press, 1998
    locator: Chapter 2, the section on the significance of scores (the extreme value distribution and E-values)
---

The E-value of a local alignment score $S$ is the expected number of distinct local alignments with score at least $S$ that a search of the same size would find by chance, between a query and a database that are not related. For a query of $m$ letters and a database of $n$ letters, the [Karlin-Altschul statistics](/karlin-altschul-statistics/) give $E = K m n\, e^{-\lambda S}$, where $\lambda$ and $K$ depend on the scoring scheme and the letter frequencies. A small E-value, such as $10^{-10}$, means that the hit is very unlikely to be chance. [BLAST](/blast/), [FASTA](/fasta-algorithm/) and other [database search](/database-similarity-search/) tools report it with each hit.

## In plain words

Even two unrelated sequences share some short similar pieces. If you search a big database, some of these chance matches get quite high scores. The question for each hit is: how many hits this good should I expect if nothing in the database were related to my query?

That number is the E-value. An E-value of 5 means that about five chance hits this good are normal for this search, so the hit tells you nothing. An E-value of 0.001 means a chance hit this good would come up in about one search out of a thousand. The number grows with the size of the database, because a bigger database gives chance more tries. It falls fast when the score goes up.

## The idea

**The model.** The query has length $m$ and the database has $n$ letters in total, treated as one long sequence. Letters are independent, with background frequencies $p_a$. The score of a local alignment uses a [substitution matrix](/substitution-matrix/) $s(a, b)$ whose expected score $\sum_{a,b} p_a p_b s(a, b)$ is negative and which has at least one positive score. For gapped alignment there is also a gap model, for example the affine cost $a + bL$ of NCBI BLAST.

**Definition.** For a score $S$,

$$E(S) = K m n\, e^{-\lambda S},$$

where $\lambda > 0$ solves $\sum_{a,b} p_a p_b e^{\lambda s(a,b)} = 1$ and $K > 0$ is a second constant of the scheme. For ungapped alignments this is a theorem: as $m, n \to \infty$ the number of [high-scoring segment pairs](/high-scoring-segment-pair/) with score at least $S$ tends to a Poisson variable with mean $E$. For gapped alignments no such theorem is known. Simulations show that the same form fits well, and BLAST uses $\lambda$ and $K$ estimated by simulation for each matrix and gap cost pair.

**From E-value to P-value.** If the count is Poisson with mean $E$, the chance of at least one hit with score at least $S$ is

$$P = 1 - e^{-E}.$$

For $E < 0.01$ the two are almost equal. For large $E$ the P-value tends to 1 and stops telling hits apart, which is one reason the tools report $E$.

| $E$ | 0.001 | 0.01 | 0.1 | 1 | 3 | 10 |
|---|---|---|---|---|---|---|
| $P = 1 - e^{-E}$ | 0.001000 | 0.009950 | 0.095163 | 0.632121 | 0.950213 | 0.999955 |

**What changes it.**

- $E$ is linear in $m$ and in $n$. A database twice as large doubles every E-value, with the same raw score.
- $E$ falls exponentially in $S$. A score higher by $\ln 2/\lambda$ halves $E$. On the scale of the [bit score](/bit-score/), each bit halves $E$.
- $\lambda$ and $K$ belong to one scoring scheme and one set of background frequencies. A query with an odd composition (rich in a few residues) breaks the model, and modern BLAST adjusts the scores for composition.

**Edge effects.** An alignment that starts near the end of a sequence has no room to grow, so the true count is below $Kmn e^{-\lambda S}$ for short sequences. BLAST uses effective lengths $m - \ell$ and $n - r\ell$ for a database of $r$ sequences, where $\ell = \ln(Kmn)/H$ is the expected length of an alignment with score near the cutoff and $H$ is the relative entropy of the scheme in nats. This is the edge-effect correction of Altschul and Gish (1996).

**Search E-value and pair E-value.** BLAST computes $E$ with $n$ equal to the length of the whole database, so the E-value of a hit is a statement about the whole search, not about one sequence pair. FASTA estimates its statistics from the scores of the many unrelated library sequences in the same search, and scales them to the library size in the same spirit.

## Examples

**Scores, E-values and P-values.** DNA with uniform bases and scores $+1/-2$ has $\lambda = 1.3327$ and $K = 0.621$. For a query of $m = 500$ against $n = 10^9$ bases:

| score $S$ | $E$ | $P$ |
|---|---|---|
| 20 | 0.82 | 0.56 |
| 25 | $1.05 \times 10^{-3}$ | $1.05 \times 10^{-3}$ |
| 30 | $1.34 \times 10^{-6}$ | $1.34 \times 10^{-6}$ |
| 35 | $1.72 \times 10^{-9}$ | $1.72 \times 10^{-9}$ |
| 40 | $2.19 \times 10^{-12}$ | $2.19 \times 10^{-12}$ |

Each 5 points of score divide $E$ by $e^{5\lambda} \approx 780$. The score with $E = 1$ is $19.86$ and the score with $E = 0.001$ is $25.04$. The same alignments against a database of $10^6$ bases would have E-values 1000 times smaller.

**A strong hit.** The [BLAST](/blast/) page shows a DNA pair of 64 bases with a mismatch at every eighth position, with ungapped score 42. In a search of $m = 64$ against $n = 10^9$ with $+1/-2$, its E-value is $0.621 \cdot 64 \cdot 10^9 \cdot e^{-1.3327 \cdot 42} \approx 2.0 \times 10^{-14}$. So it is highly significant, even though a seed-based search with 11-letter words does not find it.

**Simulated counts.** For 200 pairs of random DNA sequences of length 400 each (uniform bases, generated with the seed 2026), the HSPs on every diagonal were counted as the excursions of the running score $\max(0, h + s)$ with a peak of at least $S$. The mean count per pair against the predicted $E$, with plain and with effective lengths ($\ell = 10.2$):

| $S$ | observed mean per pair | $E$, plain lengths | $E$, effective lengths |
|---|---|---|---|
| 6 | 32.58 | 33.46 | 31.77 |
| 8 | 2.315 | 2.328 | 2.21 |
| 10 | 0.175 | 0.162 | 0.154 |

At these short lengths the formula is within about 15% of the observed means. The sample at $S = 10$ has only 35 events, so its noise is about 17%.

## Where it is used

- **Ranking and cutoffs in search.** BLAST reports hits with $E$ below a cutoff (10 by default in NCBI BLAST) and sorts them by $E$. Users often treat $E < 10^{-3}$ or a stricter value as a likely homolog. Such thresholds are conventions, not results.
- **Iterated profile search.** PSI-BLAST adds hits with $E$ below an inclusion threshold to its profile for the next round. A false hit that gets in can pull in a whole wrong family.
- **Comparing searches.** E-values depend on the database size, so the same hit has different E-values in different databases. To compare raw strength across databases, use the [bit score](/bit-score/).
- **Profile HMM search.** [HMMER](/hmmer/) reports E-values for its log-odds scores, with its own fitted distributions.
- **Multiple testing.** The E-value is the expected number of false positives at a threshold, the same quantity as the per-family error rate in multiple testing. Searching more sequences raises it in proportion.

The E-value measures chance under a random model with independent letters. It says nothing about whether two sequences have the same function, and it can be badly wrong for low-complexity or biased sequences, which is why search tools mask such regions first.

## References
