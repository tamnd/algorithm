---
tag: 9HFY19
kind: concept
slug: bit-score
name: Bit score
aliases:
- normalized bit score
area: biology/sequence-alignment
level: core
summary: "A raw alignment score rescaled by the Karlin-Altschul parameters: S' = (λS - ln K)/ln 2. Bit scores of different scoring schemes are comparable, and E = mn 2^(-S')."
prereqs: [e-value]
see_also: [e-value, karlin-altschul-statistics, high-scoring-segment-pair, blast, substitution-matrix, blosum-matrix]
sources:
  - paper: doi:10.1093/nar/25.17.3389
    title: Stephen F. Altschul, Thomas L. Madden, Alejandro A. Schäffer, Jinghui Zhang, Zheng Zhang, Webb Miller and David J. Lipman, Gapped BLAST and PSI-BLAST, a new generation of protein database search programs, Nucleic Acids Research 25(17), 1997
    locator: pages 3389 to 3402, Statistical Preliminaries (the normalized score in bits and the E-value from it)
  - paper: doi:10.1073/pnas.87.6.2264
    title: Samuel Karlin and Stephen F. Altschul, Methods for assessing the statistical significance of molecular sequence features by using general scoring schemes, PNAS 87(6), 1990
    locator: pages 2264 to 2268 (the parameters λ and K, and the target frequencies of a scoring scheme)
  - paper: "Stephen F. Altschul, Amino acid substitution matrices from an information theoretic perspective, Journal of Molecular Biology 219(3), 1991, pages 555 to 565"
    title: Altschul 1991
    locator: the relative entropy of a substitution matrix in bits per position, and the length of a significant alignment
  - url: https://raw.githubusercontent.com/ncbi/ncbi-cxx-toolkit-public/master/src/algo/blast/core/blast_stat.c
    title: NCBI C++ Toolkit, BLAST core, blast_stat.c
    locator: the table blosum62_values (λ, K and H for BLOSUM62, ungapped and for each pair of gap costs)
  - book: isbn:9780521629713
    title: Richard Durbin, Sean R. Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, Cambridge University Press, 1998
    locator: Chapter 2, the section on the significance of scores
---

The bit score of a local alignment is its raw score $S$ rescaled by the [Karlin-Altschul](/karlin-altschul-statistics/) parameters $\lambda$ and $K$ of the scoring scheme: $S' = (\lambda S - \ln K)/\ln 2$. The scale removes the units of the [substitution matrix](/substitution-matrix/) and the gap costs, so bit scores from different schemes can be compared. With it the [E-value](/e-value/) becomes $E = m n\, 2^{-S'}$, which needs only the search size $mn$. [BLAST](/blast/) reports the bit score next to the raw score of each hit.

## In plain words

A raw alignment score is like a price without a currency. A score of 50 can be very good with one scoring table and poor with another, because the tables use different units. The bit score converts every score into one common unit, the bit.

After the conversion, each extra bit makes a chance match half as likely. So a hit with 40 bits is twice as hard to get by chance as a hit with 39 bits, in any scoring system. To decide if a hit is real, you compare its bits with the size of the search: a bigger database needs a few more bits, because it gives chance more tries.

## The idea

**The model.** A query of length $m$ and a database of $n$ letters in total (written $N$ on the [database search](/database-similarity-search/) page), with letters drawn independently from background frequencies $p_a$. The scoring scheme is a substitution matrix $s(a, b)$ and, for gapped alignment, a gap model. $\lambda$ and $K$ are the Karlin-Altschul parameters of the scheme: computed exactly for ungapped scores, and fitted by simulation for gapped scores.

**Definition.** The bit score of a raw score $S$ is

$$S' = \frac{\lambda S - \ln K}{\ln 2}.$$

**Why it works.** Put $\lambda S = S' \ln 2 + \ln K$ into the Karlin-Altschul formula:

$$E = K m n\, e^{-\lambda S} = K m n\, e^{-S' \ln 2}/K = m n\, 2^{-S'}.$$

So $\lambda$ and $K$ disappear, and the E-value depends only on the bit score and the search size. Gapped BLAST (1997) writes the search size as $N = mn$ and the same relation as $S' = \log_2(N/E)$.

**Consequences.**

- One more bit halves the E-value. Doubling the database doubles $mn$, so it costs one bit.
- The bit score needed for a target E-value $E_0$ is $\log_2(mn/E_0)$. This number depends only on the search, not on the scoring scheme.
- The raw score is an integer, but the bit score is a real number, usually printed with one decimal place.
- Bit scores of two scoring schemes are comparable only if both use correct $\lambda$ and $K$ for the same background frequencies.

**Bits per position.** The scores of a matrix define *target frequencies* $q_{ab} = p_a p_b e^{\lambda s(a,b)}$, the pair frequencies in the alignments that the matrix favors. The relative entropy $H = \sum_{a,b} q_{ab}\, \lambda s(a, b)$, divided by $\ln 2$, is the mean bit score per aligned pair in such alignments (Altschul 1991). So an alignment at the target frequencies needs about $\log_2(mn/E_0)/H_{\text{bits}}$ positions to reach the E-value $E_0$. A matrix with a high $H$ is for close relatives and finds short alignments. A matrix with a low $H$ is for distant relatives and needs longer ones.

**Units of matrices.** Many matrices store $s(a, b) = \operatorname{round}(c \log_2(q_{ab}/(p_a p_b)))$ for a scale $c$. [BLOSUM62](/blosum-matrix/) uses $c = 2$, half-bit units, so its $\lambda$ is near $\ln 2 / 2 = 0.347$. Because of the rounding and the gap costs, the true $\lambda$ differs from this, and the bit score uses the true value.

## Examples

**One alignment, five DNA schemes.** Take an ungapped DNA alignment of 32 positions with 30 matches and 2 mismatches, uniform bases, and a search with $m = 500$ and $n = 10^9$, so $mn = 5 \times 10^{11} = 2^{38.86}$:

| scheme | $\lambda$ | $K$ | $H$ in bits | raw score | bit score | $E = mn\,2^{-S'}$ |
|---|---|---|---|---|---|---|
| $+1/-1$ | 1.0986 | 0.3333 | 0.79 | 28 | 45.96 | 0.0073 |
| $+1/-2$ | 1.3327 | 0.6210 | 1.62 | 26 | 50.68 | 0.00028 |
| $+1/-3$ | 1.3741 | 0.7106 | 1.89 | 24 | 48.07 | 0.0017 |
| $+2/-3$ | 0.6337 | 0.4080 | 1.32 | 54 | 50.66 | 0.00028 |
| $+5/-4$ | 0.1915 | 0.1755 | 0.51 | 142 | 41.75 | 0.135 |

The raw scores run from 24 to 142 and say little by themselves. The bit scores say that the $+1/-2$ and $+2/-3$ schemes rate this alignment the same, and that $+5/-4$, which is tuned for less similar DNA, rates it lowest. To pass $E = 1$ here a hit needs $38.86$ bits, and to pass $E = 0.001$ it needs $48.83$ bits, in every scheme.

**BLOSUM62, ungapped and gapped.** The NCBI BLAST source lists $\lambda = 0.3176$ and $K = 0.134$ for ungapped BLOSUM62 scores, and $\lambda = 0.267$ and $K = 0.041$ for gapped scores with the gap cost $11 + L$ (open 11, extend 1). For a protein query of $m = 300$ against $n = 10^8$ residues ($mn = 2^{34.80}$):

| raw score | bits (ungapped) | $E$ (ungapped) | bits (gapped, 11/1) | $E$ (gapped, 11/1) |
|---|---|---|---|---|
| 50 | 25.81 | 510 | 23.87 | 1960 |
| 100 | 48.72 | $6.5 \times 10^{-5}$ | 43.13 | 0.0031 |

The same raw score is worth fewer bits with gaps allowed, because gaps let random sequences reach high scores more easily.

**How long must a match be?** With $+1/-2$ the relative entropy is $1.62$ bits per position. In the search above, $E = 0.001$ needs $48.83$ bits, so an alignment at the target frequencies of this scheme needs about $48.83 / 1.62 \approx 30$ positions.

## Where it is used

- **BLAST output.** Each hit has a raw score, a bit score and an E-value. The bit score does not change with the database size, so it is the number to compare across searches of different databases.
- **Comparing scoring schemes.** To choose a matrix or gap costs, compare the bit scores that each gives to known true alignments.
- **Thresholds.** Tools that work with many databases set cutoffs in bits, for example a minimum bit score for a hit to be kept.
- **Matrix design.** The relative entropy in bits per position tells which evolutionary distance a matrix suits. See [substitution matrix](/substitution-matrix/).

The bit score is a log-scale form of the E-value, not a new statistic. Its meaning holds only as far as the Karlin-Altschul model holds: for ungapped scores it rests on a theorem, for gapped scores on fitted parameters.

## References
