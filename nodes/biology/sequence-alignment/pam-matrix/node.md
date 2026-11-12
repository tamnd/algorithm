---
tag: BSGV62
kind: concept
slug: pam-matrix
name: PAM matrix
aliases:
- Dayhoff matrix
- point accepted mutation matrix
- PAM250
area: biology/sequence-alignment
level: core
summary: Dayhoff's protein substitution matrices; PAM1 is a Markov chain with one accepted point mutation per 100 residues, PAMn is its n-th power, and the scores are its log-odds.
prereqs: [substitution-matrix, markov-chain]
see_also: [blosum-matrix, matrix-exponentiation, stationary-distribution, scoring-matrix, karlin-altschul-statistics]
sources:
  - paper: "Margaret O. Dayhoff, Robert M. Schwartz and Bruce C. Orcutt, A model of evolutionary change in proteins, in Atlas of Protein Sequence and Structure, Volume 5, Supplement 3, National Biomedical Research Foundation, Washington DC, 1978, pages 345-352"
    locator: the accepted point mutations, the PAM1 mutation probability matrix, its powers, and the log-odds matrix for 250 PAMs
  - paper: doi:10.1016/0022-2836(91)90193-A
    title: Stephen F. Altschul, Amino acid substitution matrices from an information theoretic perspective, Journal of Molecular Biology 219(3), 1991, 555-565
    locator: the relative entropy of PAM matrices as a function of the PAM distance
  - book: isbn:9780521629713
    title: Richard Durbin, Sean R. Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, Cambridge University Press, 1998
    locator: Chapter 2, Section 2.8 (PAM matrices)
  - url: https://ftp.ncbi.nlm.nih.gov/blast/matrices/PAM250
    title: NCBI BLAST matrix file PAM250
    locator: the header (scale ln(2)/3, expected score -0.844, entropy 0.354 bits) and the rows I, L, V, F, Y, W
---

A PAM matrix is a protein [substitution matrix](/substitution-matrix/) built from an explicit model of evolution, introduced by Margaret Dayhoff and colleagues in 1978. The model is a [Markov chain](/markov-chain/) on the 20 amino acids: the matrix PAM1 gives the probability that one amino acid is replaced by another over a time in which one residue in 100 changes, one *point accepted mutation* per 100 residues. The model for $n$ such units is the matrix power $\text{PAM1}^n$, and the scoring matrix PAMn holds the log-odds $\log \frac{(\text{PAM1}^n)_{ab}}{p_b}$. PAM250, for distant proteins, was the standard protein scoring matrix before [BLOSUM](/blosum-matrix/).

## In plain words

Over time, proteins change: now and then one amino acid is replaced by another, and if the protein still works the change is kept. Dayhoff's team collected families of very similar proteins, where the changes are few and easy to see, and counted which amino acid had turned into which.

From these counts they built a table for a short time step: the step in which, on average, one amino acid in a hundred changes. To model a longer time, you apply the same step again and again. After many steps, the table describes proteins that have drifted far apart.

Each table of change chances becomes a table of scores: a pair gets a positive score when the model says it occurs more often in related proteins than by chance. PAM250 is the table for 250 steps, for distant relatives.

## The idea

**Accepted point mutations.** A point mutation replaces one amino acid by another. It is *accepted* when it is fixed in the species, so that it shows up in present-day sequences. Dayhoff, Schwartz and Orcutt took groups of closely related proteins, built their evolutionary trees, and counted the accepted replacements $a \to b$ on the branches. Close relatives were used because for them each observed difference is very likely one single replacement.

**The PAM1 chain.** From the counts and the amino acid frequencies $p$, they built a $20 \times 20$ matrix $M$ in which $M_{ab}$ is the probability that a site holding $a$ holds $b$ one time unit later. The rows sum to 1, and the unit is scaled so that the expected fraction of sites that change is $1/100$:

$$\sum_a p_a (1 - M_{aa}) = \frac{1}{100}.$$

This is PAM1. Dayhoff's tables print the transpose, with columns that sum to 1; this page uses rows.

**Longer distances by matrix powers.** The model assumes that every site evolves by the same chain, independently, and that the chain does not change with time. Then the substitution probabilities for $n$ units are the matrix power $M^n$, which [matrix exponentiation](/matrix-exponentiation/) computes with $O(\log n)$ products of $20 \times 20$ matrices. PAM250 is $M^{250}$. As $n$ grows, every row of $M^n$ tends to the [stationary distribution](/stationary-distribution/) $p$, and an old alignment looks random.

**From probabilities to scores.** For the related model, the probability of seeing the pair $(a, b)$ in two sequences at distance $n$ is $q_{ab} = p_a (M^n)_{ab}$. The log-odds score is

$$s_n(a, b) = \frac{1}{\lambda} \log \frac{p_a (M^n)_{ab}}{p_a\, p_b} = \frac{1}{\lambda} \log \frac{(M^n)_{ab}}{p_b}.$$

For this to be symmetric the chain must be reversible, $p_a M_{ab} = p_b M_{ba}$, and then every power is reversible too. Dayhoff counted each replacement in both directions, which gives this.

**PAM distance is not percent difference.** A distance of 250 PAMs means 250 accepted mutations per 100 sites, many of them at the same site, some changing a residue back. The observed identity at that distance is still about 20%, against roughly 6% for two random sequences with amino acid frequencies.

**Powers versus multiples.** The scores of PAMn come from the $n$-th power of the probabilities, not from $n$ times the PAM1 scores. Log-odds scores do not add up over time.

## Examples

**A three-letter model.** Take the alphabet $\{A, B, C\}$ with frequencies $p = (1/2, 1/4, 1/4)$. Let the off-diagonal entries be $M_{ab} = c\, w_{ab}\, p_b$ with symmetric weights $w_{AB} = 2$, $w_{AC} = w_{BC} = 1$. Then $p_a M_{ab} = c\, w_{ab}\, p_a p_b$ is symmetric, so the chain is reversible, and its stationary distribution is $p$. The expected change per unit is $c \sum_{a \ne b} w_{ab} p_a p_b = \frac{7}{8} c$, so $c = \frac{1}{100} \cdot \frac{8}{7} = \frac{2}{175}$. With exact fractions, PAM1 is

| $M$ | A | B | C |
|---|---|---|---|
| A | 347/350 | 1/175 | 1/350 |
| B | 2/175 | 69/70 | 1/350 |
| C | 1/175 | 1/350 | 347/350 |

Check the A row: $M_{AB} = \frac{2}{175} \cdot 2 \cdot \frac{1}{4} = \frac{1}{175}$, $M_{AC} = \frac{2}{175} \cdot 1 \cdot \frac{1}{4} = \frac{1}{350}$, and $M_{AA} = 1 - \frac{3}{350} = \frac{347}{350}$. The square is

| $M^2$ | A | B | C |
|---|---|---|---|
| A | 120419/122500 | 277/24500 | 174/30625 |
| B | 277/12250 | 59517/61250 | 174/30625 |
| C | 348/30625 | 174/30625 | 30103/30625 |

**Identity and scores against distance.** The expected identity at distance $n$ is $\sum_a p_a (M^n)_{aa}$. The half-bit scores $2 \log_2 \frac{(M^n)_{ab}}{p_b}$, rounded, are:

| $n$ | identity | A-A | A-B | A-C | B-B | B-C | C-C |
|---|---|---|---|---|---|---|---|
| 1 | 0.990 | 2 | -11 | -13 | 4 | -13 | 4 |
| 10 | 0.907 | 2 | -5 | -6 | 4 | -6 | 4 |
| 50 | 0.661 | 1 | -1 | -2 | 2 | -2 | 3 |
| 100 | 0.512 | 1 | 0 | -1 | 1 | -1 | 2 |
| 250 | 0.394 | 0 | 0 | 0 | 0 | 0 | 0 |

The identity falls toward $\sum_a p_a^2 = 3/8$, the identity of two random sequences, and is $0.375003$ at $n = 1000$. The scores shrink toward $0$ as the model forgets the starting residue. At $n = 250$ this toy model has almost no signal left: the unrounded scores are between $-0.17$ and $0.45$ half-bits. Real proteins keep more signal at 250 PAMs, because many amino acids change slowly. By contrast, $250$ times the PAM1 score of A-A is about $494$ half-bits, nothing like the PAM250 score.

**The real PAM250.** An excerpt of the NCBI file, whose header gives the scale $\ln 2 / 3$, expected score $-0.844$ and entropy $0.354$ bits:

|   | I | L | V | F | Y | W |
|---|---|---|---|---|---|---|
| I | 5 | 2 | 4 | 1 | -1 | -5 |
| L | 2 | 6 | 2 | 2 | -1 | -2 |
| V | 4 | 2 | 4 | -1 | -2 | -6 |
| F | 1 | 2 | -1 | 9 | 7 | 0 |
| Y | -1 | -1 | -2 | 7 | 10 | 0 |
| W | -5 | -2 | -6 | 0 | 0 | 17 |

Tryptophan W scores $17$ with itself: it is rare and seldom replaced. Phenylalanine and tyrosine, both aromatic, score $+7$. The same pairs in [BLOSUM62](/blosum-matrix/) are $11$ and $3$, in half-bits.

## Where it is used

- PAM250 was the default protein matrix of early database search programs such as [FASTA](/fasta-algorithm/). PAM30 and PAM70 are offered by protein [BLAST](/blast/) for short or close queries.
- The PAM idea, a reversible Markov chain fitted to data and raised to a power, is the basis of the later JTT and WAG models and of the substitution models of phylogenetics, which use the continuous-time form $e^{Qt}$.
- Altschul (1991) used the PAM family to show how the relative entropy of a matrix falls with distance, and how to pick the matrix for an expected distance.
- [Karlin-Altschul statistics](/karlin-altschul-statistics/) treat PAM matrices like any other scoring matrix, through $\lambda$.

## References
