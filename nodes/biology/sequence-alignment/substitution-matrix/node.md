---
tag: EMJF66
kind: concept
slug: substitution-matrix
name: Substitution matrix
aliases:
- residue substitution matrix
- log-odds substitution matrix
area: biology/sequence-alignment
level: core
summary: A scoring matrix of log-odds scores s(a, b) = (1/λ) log(q_ab / (p_a p_b)), built from how often residue a is aligned with b in related sequences.
prereqs: [scoring-matrix]
see_also: [pam-matrix, blosum-matrix, karlin-altschul-statistics, bit-score, position-specific-scoring-matrix, pair-hmm, maximum-likelihood-estimation]
sources:
  - paper: doi:10.1016/0022-2836(91)90193-A
    title: Stephen F. Altschul, Amino acid substitution matrices from an information theoretic perspective, Journal of Molecular Biology 219(3), 1991, 555-565
    locator: target frequencies, relative entropy of a matrix, and the choice of a matrix for a given evolutionary distance
  - paper: doi:10.1073/pnas.87.6.2264
    title: Samuel Karlin and Stephen F. Altschul, Methods for assessing the statistical significance of molecular sequence features by using general scoring schemes, Proceedings of the National Academy of Sciences USA 87(6), 1990, 2264-2268
    locator: the parameter lambda as the unique positive root, and the target frequencies of high-scoring segments
  - paper: doi:10.1073/pnas.89.22.10915
    title: Steven Henikoff and Jorja G. Henikoff, Amino acid substitution matrices from protein blocks, Proceedings of the National Academy of Sciences USA 89(22), 1992, 10915-10919
    locator: the log-odds construction of the BLOSUM matrices and their relative entropy
  - book: isbn:9780521629713
    title: Richard Durbin, Sean R. Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, Cambridge University Press, 1998
    locator: Chapter 2, Section 2.2 (substitution matrices as log-odds ratios) and Section 2.8 (deriving score parameters from alignment data)
  - url: https://ftp.ncbi.nlm.nih.gov/blast/matrices/BLOSUM62
    title: NCBI BLAST matrix file BLOSUM62
    locator: the header lines giving the unit (1/2 bit), the entropy 0.6979 and the expected score -0.5209
---

A substitution matrix is a [scoring matrix](/scoring-matrix/) whose entries are log-odds scores,

$$s(a, b) = \frac{1}{\lambda} \log \frac{q_{ab}}{p_a\, p_b},$$

where $q_{ab}$ is the frequency with which residues $a$ and $b$ are aligned in true alignments of related sequences, $p_a$ is the background frequency of $a$, and $\lambda > 0$ sets the unit. A positive score means the pair is seen more often in related sequences than by chance. The [PAM](/pam-matrix/) and [BLOSUM](/blosum-matrix/) families are substitution matrices for proteins; they differ in how they estimate $q_{ab}$. By a theorem of Karlin and Altschul, every scoring matrix that works for local alignment is a substitution matrix for some implicit $q_{ab}$.

## In plain words

Take many pairs of proteins that are known to be related, and line them up correctly. Count how often each pair of amino acids stands in the same column. Some pairs show up far more often than chance would give, because one amino acid often replaces the other without breaking the protein. Other pairs show up less often than chance.

A substitution matrix turns these counts into scores. A pair that shows up more often than chance gets a positive score, and a pair that shows up less often gets a negative score. The size of the score says how much more or less often.

With such scores, the total score of an alignment measures how much more likely the alignment is under "these sequences are related" than under "these sequences are random". That is the right quantity for deciding whether two sequences share an ancestor.

## The idea

**Two hypotheses.** Consider an ungapped alignment of two sequences, $a_1 \cdots a_k$ over $b_1 \cdots b_k$. Under the *random* model, all $2k$ residues are independent with frequencies $p$. Under the *related* model, the columns are independent and the pair $(a, b)$ has probability $q_{ab}$. The likelihood ratio is

$$\frac{\prod_t q_{a_t b_t}}{\prod_t p_{a_t} p_{b_t}}, \qquad \log \text{ of it } = \sum_t \log \frac{q_{a_t b_t}}{p_{a_t} p_{b_t}} = \lambda \sum_t s(a_t, b_t).$$

So the alignment score is the log-likelihood ratio, up to the factor $\lambda$. By the Neyman-Pearson lemma, a threshold on this sum is the most powerful test between the two models. This is the reason for the log-odds form.

**Units and rounding.** With $\lambda = \ln 2$ the scores are in bits; with $\lambda = \ln 2 / 2$ they are in half-bits, the unit of BLOSUM62; the NCBI file for PAM250 states the scale $\ln 2 / 3$. Published matrices round the scores to integers. Rounding changes the matrix slightly, so its true $\lambda$, computed as below, differs a little from the nominal one.

**Target frequencies and $\lambda$.** Let $p$ be background frequencies with all $p_a > 0$, and let $s$ be any scoring matrix with

1. expected score $E = \sum_{a, b} p_a p_b\, s(a, b) < 0$, and
2. some $s(a, b) > 0$.

Then $f(\lambda) = \sum_{a, b} p_a p_b\, e^{\lambda s(a, b)}$ has exactly one root $\lambda^* > 0$ of $f(\lambda) = 1$. Proof: $f(0) = 1$ and $f'(0) = E < 0$, so $f < 1$ just right of $0$. Since some $s(a, b) > 0$, $f(\lambda) \to \infty$ as $\lambda \to \infty$, so a root $\lambda^* > 0$ exists. And $f''(\lambda) = \sum p_a p_b\, s(a, b)^2 e^{\lambda s(a, b)} > 0$, so $f$ is strictly convex, and a strictly convex function takes the value $1$ at most twice; one of these is $\lambda = 0$. Now set $q_{ab} = p_a p_b\, e^{\lambda^* s(a, b)}$. These are positive and sum to $f(\lambda^*) = 1$, and $s(a, b) = \frac{1}{\lambda^*} \log \frac{q_{ab}}{p_a p_b}$. Karlin and Altschul proved that in long random sequences, the pairs in the highest-scoring ungapped segments occur, in the limit, with these frequencies $q_{ab}$. Altschul (1991) called them the target frequencies of the matrix.

The implicit $q_{ab}$ need not have $p$ as their row sums. For a matrix built from data whose pair frequencies have marginals $p$, the root $\lambda^*$ is the scale used to build it, and the $q_{ab}$ are the data again.

**Relative entropy.** The average score per aligned pair in true alignments, in bits, is

$$H = \sum_{a, b} q_{ab} \log_2 \frac{q_{ab}}{p_a p_b},$$

the relative entropy of $q$ with respect to $p \times p$. It is never negative and is zero only when $q = p \times p$. $H$ measures how much one column of a true alignment tells about relatedness. A matrix with high $H$ is tuned to close relatives: short alignments already reach a significant score. A matrix with low $H$ is tuned to distant relatives and needs longer alignments. The NCBI file for BLOSUM62 gives $H = 0.6979$ bits and expected score $-0.5209$; the NCBI file for PAM250 gives $H = 0.354$ bits.

**Choosing a matrix.** Altschul (1991) argued that the best matrix for finding a given alignment is the one whose target frequencies match the alignment's actual pair frequencies. So each matrix of a family is built for one evolutionary distance: PAM by an explicit [Markov chain](/markov-chain/) of mutations, BLOSUM by counting pairs in blocks of sequences clustered at a chosen identity level.

## Examples

**A toy alphabet.** Take three residues with background $p_A = 1/2$, $p_B = p_C = 1/4$ and target frequencies

| $q$ | A | B | C |
|---|---|---|---|
| A | 2/5 | 1/20 | 1/20 |
| B | 1/20 | 3/20 | 1/20 |
| C | 1/20 | 1/20 | 3/20 |

Each row sums to its background frequency: $2/5 + 1/20 + 1/20 = 1/2$, and $1/20 + 3/20 + 1/20 = 1/4$. The scores $\log_2 \frac{q_{ab}}{p_a p_b}$ in bits are

| bits | A | B | C |
|---|---|---|---|
| A | 0.678 | -1.322 | -1.322 |
| B | -1.322 | 1.263 | -0.322 |
| C | -1.322 | -0.322 | 1.263 |

For example $\log_2 \frac{2/5}{1/4} = \log_2 1.6 = 0.678$. The common residue A gets a smaller self score than the rare residues B and C: matching two common residues is weaker evidence. The relative entropy is $H = 0.354$ bits and the expected score is $-0.374$ bits.

**Rounding moves the targets.** In half-bits and rounded, the matrix is

| half-bits | A | B | C |
|---|---|---|---|
| A | 1 | -3 | -3 |
| B | -3 | 3 | -1 |
| C | -3 | -1 | 3 |

Its expected score is $-1$, and the root of $f(\lambda) = 1$ is $\lambda^* = 0.3781$ instead of the nominal $\ln 2 / 2 = 0.3466$. The implicit target frequencies are $q_{AA} = 0.365$, $q_{BB} = q_{CC} = 0.194$, $q_{AB} = q_{AC} = 0.040$ and $q_{BC} = 0.043$, close to but not equal to the data.

**Two real matrices.** The NCBI BLOSUM62 file gives the self score of tryptophan, the rarest amino acid, as $11$, and of alanine as $4$; isoleucine and valine, which are chemically similar, score $+3$. The PAM250 file gives tryptophan $17$ and cysteine $12$ against itself. The two matrices are in different units, half-bits and third-bits, so these numbers cannot be compared directly.

## Where it is used

- Protein alignment and search: [BLAST](/blast/), [FASTA](/fasta-algorithm/) and Smith-Waterman search tools all score with a substitution matrix, BLOSUM62 by default in protein BLAST.
- Statistics of local alignment scores: [Karlin-Altschul statistics](/karlin-altschul-statistics/) use $\lambda^*$ of the matrix, and the [bit score](/bit-score/) of a raw score $S$ is $(\lambda^* S - \ln K)/\ln 2$, with a second constant $K$.
- The [high-scoring segment pair](/high-scoring-segment-pair/) of BLAST is a maximal ungapped segment under a substitution matrix.
- The same log-odds idea, with one distribution per position instead of one for the whole sequence, gives the [position-specific scoring matrix](/position-specific-scoring-matrix/) and the emission scores of a [profile HMM](/profile-hmm/). A [pair HMM](/pair-hmm/) has the joint distribution $q_{ab}$ as its match-state emissions.

## References
