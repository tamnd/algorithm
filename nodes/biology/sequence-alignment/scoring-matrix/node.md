---
tag: 27DFM0
kind: concept
slug: scoring-matrix
name: Scoring matrix
aliases:
- score matrix
area: biology/sequence-alignment
level: intro
summary: The table s(a, b) of scores for aligning residue a with residue b; any such table, from a DNA match/mismatch rule to BLOSUM62, used as the pair part of an alignment score.
prereqs: [weighted-edit-distance]
see_also: [substitution-matrix, pam-matrix, blosum-matrix, position-specific-scoring-matrix, gap-penalty, alignment-score, karlin-altschul-statistics, bit-score]
sources:
  - book: isbn:9780521629713
    title: Richard Durbin, Sean R. Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, Cambridge University Press, 1998
    locator: Chapter 2, Section 2.2 (substitution matrices and the log-odds score) and Section 2.8 (deriving score parameters from alignment data)
  - paper: doi:10.1073/pnas.87.6.2264
    title: Samuel Karlin and Stephen F. Altschul, Methods for assessing the statistical significance of molecular sequence features by using general scoring schemes, Proceedings of the National Academy of Sciences USA 87(6), 1990, 2264-2268
    locator: the conditions of negative expected score and a positive score, and the parameter lambda
  - paper: doi:10.1016/0022-2836(91)90193-A
    title: Stephen F. Altschul, Amino acid substitution matrices from an information theoretic perspective, Journal of Molecular Biology 219(3), 1991, 555-565
    locator: every such matrix is a log-odds matrix with implicit target frequencies; relative entropy of a matrix
---

A scoring matrix is a table $s(a, b)$ that gives the score for aligning residue $a$ of one sequence with residue $b$ of another. Together with a [gap penalty](/gap-penalty/), it defines the [alignment score](/alignment-score/) that alignment algorithms maximize. The term covers every such table: a DNA rule of $+1$ for a match and $-3$ for a mismatch, the identity matrix, and protein tables like [BLOSUM62](/blosum-matrix/). A [substitution matrix](/substitution-matrix/) is the narrower case of a scoring matrix built as log-odds scores from substitution data.

## In plain words

When two sequences are lined up, each column holds two letters. The scoring matrix is a lookup table that says how good each pair is. Equal letters get a positive score. Different letters get a lower score, often a negative one. Some different letters get a better score than others: in proteins, two amino acids with similar chemistry often replace each other without harm, so the table can reward that pair.

For DNA, the table is often just two numbers, one for a match and one for a mismatch. For proteins, it has a row and a column for each of the 20 amino acids, and its values come from counts in real alignments.

The choice of table decides which alignments win. A table that punishes mismatches hard finds near-identical sequences. A milder table finds distant relatives.

## The idea

**Definition.** Let $\Sigma$ be the residue alphabet: four bases for DNA, 20 amino acids for proteins, sometimes with extra codes such as $\texttt{N}$ or $\texttt{X}$ for an unknown residue. A scoring matrix is a function $s : \Sigma \times \Sigma \to \mathbb{R}$, written as a $|\Sigma| \times |\Sigma|$ table. Most scoring matrices are symmetric, $s(a, b) = s(b, a)$, because the order of the two sequences should not change the score. An alignment collects $s(a, b)$ over its pair columns and subtracts the gap penalty for its gaps.

**Kinds of scoring matrix.**

| kind | values | typical use |
|---|---|---|
| identity | $s(a, a) = 1$, $s(a, b) = 0$ | [longest common subsequence](/longest-common-subsequence/), counting matches |
| unit cost | $s(a, a) = 0$, $s(a, b) = -1$ | minus the [edit distance](/edit-distance/) |
| DNA match/mismatch | for example $+1/-3$, $+2/-3$, $+5/-4$ | nucleotide search and read mapping |
| DNA with transitions | a smaller penalty for $\texttt{A} \leftrightarrow \texttt{G}$ and $\texttt{C} \leftrightarrow \texttt{T}$ than for other mismatches | nucleotide alignment where transitions are more common |
| protein substitution matrix | log-odds scores, for example [PAM](/pam-matrix/) and [BLOSUM](/blosum-matrix/) | protein alignment and search |
| position-specific | a score for each residue at each position of a family | [position-specific scoring matrix](/position-specific-scoring-matrix/) |

The last row is not a $|\Sigma| \times |\Sigma|$ table. It replaces one of the two sequences by a column of scores per position. It is a scoring matrix in the wider sense.

**Scoring matrix versus substitution matrix.** A substitution matrix has a stated model: $s(a, b) = \frac{1}{\lambda} \log \frac{q_{ab}}{p_a p_b}$, where $q_{ab}$ is the frequency of the pair $a, b$ in correct alignments of related sequences and $p_a$ is the background frequency of $a$. A scoring matrix has no such requirement. It can be chosen by hand, like $+1/-3$, or come from a distance, like the unit cost. The two ideas are close, because of the next fact.

**Every useful local scoring matrix is a log-odds matrix.** For [local alignment](/local-alignment/), a scoring matrix needs two properties with respect to the background frequencies $p$:

1. the expected score $\sum_{a, b} p_a p_b\, s(a, b)$ is negative, and
2. at least one score $s(a, b)$ is positive.

If the expected score is positive, the best local alignment of two unrelated sequences grows with their length, and local alignment turns into global alignment. If no score is positive, the best local alignment is empty. Karlin and Altschul showed that under these two conditions the equation

$$\sum_{a, b} p_a p_b\, e^{\lambda s(a, b)} = 1$$

has exactly one positive root $\lambda$. Then $q_{ab} = p_a p_b e^{\lambda s(a, b)}$ are positive numbers that sum to 1, and $s(a, b) = \frac{1}{\lambda} \log \frac{q_{ab}}{p_a p_b}$. So a hand-made matrix is a substitution matrix whose target frequencies $q_{ab}$ are implicit. Altschul called them the matrix's target frequencies, and argued that a matrix is best at finding alignments whose pair frequencies match them. The proof is on the [substitution matrix](/substitution-matrix/) page.

**Scale does not matter.** Multiplying all of $s$ and the gap penalty by a constant $c > 0$ multiplies every alignment score by $c$, so the optimal alignments do not change, and $\lambda$ becomes $\lambda / c$. The unit of a matrix is the base of its logarithm divided by its scale: BLOSUM62 is in half-bits, each entry being $2 \log_2 \frac{q_{ab}}{p_a p_b}$ rounded to an integer, and the NCBI file for PAM250 states the scale $\ln 2 / 3$, which is third-bits. Only scores in the same unit can be compared, which is why search tools report a [bit score](/bit-score/).

## Examples

**$\lambda$ of the $+1/-1$ DNA matrix.** With uniform bases, $p_a = 1/4$, a random pair is a match with probability $1/4$. The equation for $\lambda$ is

$$\tfrac{1}{4} e^{\lambda} + \tfrac{3}{4} e^{-\lambda} = 1.$$

Put $u = e^{\lambda}$ and multiply by $4u$: $u^2 - 4u + 3 = 0$, so $u = 1$ or $u = 3$. The root $u = 1$ is $\lambda = 0$. The positive root is $\lambda = \ln 3 \approx 1.0986$. The implicit match frequency is $4 \cdot \frac{1}{16} \cdot 3 = \frac{3}{4}$. So the $+1/-1$ matrix is the log-odds matrix for alignments with 75% identity.

**Other DNA matrices.** The same calculation, with uniform bases, gives:

| match/mismatch | expected score | $\lambda$ | implicit identity |
|---|---|---|---|
| $+1/-1$ | $-0.5$ | $1.0986$ | $75.0\%$ |
| $+5/-4$ | $-1.75$ | $0.1915$ | $65.1\%$ |
| $+2/-3$ | $-1.75$ | $0.6337$ | $88.8\%$ |
| $+1/-2$ | $-1.25$ | $1.3327$ | $94.8\%$ |
| $+1/-3$ | $-2.0$ | $1.3741$ | $98.8\%$ |

A harsh mismatch penalty is tuned to near-identical sequences, such as reads mapped to the genome they came from. A mild one is tuned to more distant ones.

**A protein excerpt.** Part of BLOSUM62, from the NCBI matrix file, for six hydrophobic amino acids:

|   | I | L | V | F | Y | W |
|---|---|---|---|---|---|---|
| I | 4 | 2 | 3 | 0 | -1 | -3 |
| L | 2 | 4 | 1 | 0 | -1 | -2 |
| V | 3 | 1 | 4 | -1 | -1 | -3 |
| F | 0 | 0 | -1 | 6 | 3 | 1 |
| Y | -1 | -1 | -1 | 3 | 7 | 2 |
| W | -3 | -2 | -3 | 1 | 2 | 11 |

The diagonal differs by residue: W, the rarest of the six, scores 11 with itself, and I scores 4. Similar residues, I and V, score $+3$ for a mismatch, more than many identities in other tables. A plain match/mismatch rule cannot express either fact.

## Where it is used

- Every pairwise aligner, from [Needleman-Wunsch](/needleman-wunsch/) and [Smith-Waterman](/smith-waterman/) to [BLAST](/blast/), reads $s(a, b)$ in its inner loop.
- Statistical significance of local alignment scores, through [Karlin-Altschul statistics](/karlin-altschul-statistics/) and the [E-value](/e-value/), uses $\lambda$ of the scoring matrix.
- [Multiple sequence alignment](/multiple-sequence-alignment/) scores, such as the [sum-of-pairs score](/sum-of-pairs-score/), apply a scoring matrix to each pair of rows.
- Family models replace the fixed matrix by a [position-specific scoring matrix](/position-specific-scoring-matrix/) or a [profile HMM](/profile-hmm/).

## References
