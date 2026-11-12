---
tag: 9C1XPZ
kind: concept
slug: position-specific-scoring-matrix
name: Position-specific scoring matrix
aliases:
- PSSM
- position weight matrix
area: biology/sequence-alignment
level: core
summary: "A table of log-odds scores, one row per alignment position and one column per residue, estimated from aligned sites with pseudocounts. A window scores the sum of its entries."
prereqs: [multiple-sequence-alignment, substitution-matrix]
see_also: [sequence-logo, consensus-sequence, sequence-profile-alignment, profile-hmm, blast, scoring-matrix, maximum-a-posteriori-estimation, psipred]
sources:
  - paper: doi:10.1093/nar/10.9.2997
    title: Gary D. Stormo, Thomas D. Schneider, Larry Gold and Andrzej Ehrenfeucht, Use of the Perceptron algorithm to distinguish translational initiation sites in E. coli, Nucleic Acids Research 10(9), 1982, pages 2997 to 3011
    locator: a weight matrix over the positions around the start codon, scored as a sum of position weights
  - paper: doi:10.1093/nar/25.17.3389
    title: Stephen F. Altschul, Thomas L. Madden, Alejandro A. Schäffer, Jinghui Zhang, Zheng Zhang, Webb Miller and David J. Lipman, Gapped BLAST and PSI-BLAST, a new generation of protein database search programs, Nucleic Acids Research 25(17), 1997, pages 3389 to 3402
    locator: "the PSI-BLAST sections: the construction of the position-specific score matrix from the hits (purging, sequence weights, the pseudocount formula Q_i = (alpha f_i + beta g_i)/(alpha + beta) with alpha = N_C - 1 and beta = 10)"
  - book: isbn:9780521629713
    title: Richard Durbin, Sean R. Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, Cambridge University Press, 1998
    locator: "Chapter 5: ungapped score matrices (Section 5.1), pseudocounts and Dirichlet priors (Section 5.6), and sequence weighting (Section 5.8)"
  - paper: doi:10.1093/bioinformatics/12.4.327
    title: Kimmen Sjölander, Kevin Karplus, Michael Brown, Richard Hughey, Anders Krogh, I. Saira Mian and David Haussler, Dirichlet mixtures, a method for improved detection of weak but significant protein sequence homology, CABIOS 12(4), 1996, pages 327 to 345
    locator: Dirichlet mixture priors as pseudocounts for the columns of a profile
  - paper: doi:10.1016/0022-2836(94)90032-9
    title: Steven Henikoff and Jorja G. Henikoff, Position-based sequence weights, Journal of Molecular Biology 243(4), 1994, pages 574 to 578
    locator: the position-based weights that PSI-BLAST and HMMER use to reduce the effect of redundant sequences
---

A position-specific scoring matrix (PSSM) is a table with one row for each position of a motif or an alignment and one column for each residue, where entry $W_j(a)$ is the log-odds score of residue $a$ at position $j$. The score of a window of a sequence is the sum of the entries of its residues, and it equals the log of the likelihood ratio of the window under a position-by-position model of the family and under a background model. The probabilities come from the counts in an aligned set of sites, with *pseudocounts* added so that a residue never seen in a column does not get a score of minus infinity. PSSMs score DNA binding sites, drive the iterations of PSI-BLAST, and are the ungapped core of the [profile HMM](/profile-hmm/).

## In plain words

Collect a few short sequences that all do the same job, for example sites where one protein binds DNA, and line them up. For each position, count how often each letter appears.

Now turn the counts into points. A letter that is common at a position, more common than in random sequence, gets positive points there. A letter that is rare at that position gets negative points. This gives a table with one row of points for each position.

To test a new piece of sequence, read its letters one position at a time, look up the points for that letter at that position, and add them up. A high total means the piece looks like the collected sites.

A letter that was never seen at a position should not get infinitely bad points, because the sample was small. So add a few imaginary counts before you compute the points.

## The idea

**The model behind the table.** Fix a length $L$ and an alphabet $\Sigma$ with background frequencies $q_a > 0$. The *site model* $P$ says that a site $x = x_1 \ldots x_L$ has independent positions, with $P(x) = \prod_{j=1}^{L} p_j(x_j)$. The *background model* $Q$ says $Q(x) = \prod_j q_{x_j}$. Put

$$W_j(a) = \log_2 \frac{p_j(a)}{q_a}.$$

Then for every window $x$,

$$S(x) = \sum_{j=1}^{L} W_j(x_j) = \log_2 \prod_{j=1}^{L} \frac{p_j(x_j)}{q_{x_j}} = \log_2 \frac{P(x)}{Q(x)},$$

because the log of a product is the sum of the logs. So the PSSM score is the log-likelihood ratio of the two models, in bits, and by the Neyman-Pearson lemma a threshold on $S$ is the most powerful test between them at each false positive rate. The same log-odds idea gives a [substitution matrix](/substitution-matrix/), with one row for each residue instead of one for each position.

**Expected scores.** If $x$ comes from the site model, the expected score of position $j$ is $\sum_a p_j(a) \log_2 (p_j(a)/q_a)$, the relative entropy of $p_j$ to $q$. It is at least 0, with equality only when $p_j = q$. If $x$ comes from the background, the expected score is $-\sum_a q_a \log_2 (q_a / p_j(a)) \le 0$. A good PSSM has a large gap between the two. The relative entropy of each row is also the stack height of a [sequence logo](/sequence-logo/) drawn against the background $q$.

**Names.** The table of counts $n_j(a)$ is a position frequency matrix; the table of $p_j(a)$ is a position probability matrix; the log-odds table is the PSSM. "Position weight matrix" is used for the log-odds table, and also, loosely, for the others. Stormo et al. (1982) scored start sites in *E. coli* with a weight matrix in this additive form.

**Estimating the rows.** From $N_j$ residues in column $j$ with counts $n_j(a)$, the maximum likelihood estimate is $p_j(a) = n_j(a)/N_j$. A residue that is absent gets $p_j(a) = 0$ and $W_j(a) = -\infty$, so one unseen residue rules out a window, however well the rest fits. With few sites this is wrong more often than not. The standard fix adds pseudocounts:

$$p_j(a) = \frac{n_j(a) + \alpha\, b_a}{N_j + \alpha},$$

where $b$ is a distribution over $\Sigma$ and $\alpha > 0$ is the total weight of the pseudocounts. This is the mean of the posterior distribution of $p_j$ under a Dirichlet prior with parameters $\alpha b_a$ (Durbin et al., Section 5.6). With $b_a = 1/|\Sigma|$ and $\alpha = |\Sigma|$ it is Laplace's rule, one extra count for each residue. As $N_j$ grows, the counts dominate and $p_j(a) \to n_j(a)/N_j$; as $\alpha$ grows, the row moves to $b$ and the scores move to $\log_2(b_a/q_a)$.

**Better pseudocounts for proteins.** For proteins the 20 residues are not equally related. Substitution-matrix pseudocounts put more pseudocount weight on residues that often replace the ones seen in the column. PSI-BLAST (Altschul et al. 1997) uses

$$g_i = \sum_j \frac{f_j}{P_j}\, q_{ij}, \qquad Q_i = \frac{\alpha f_i + \beta g_i}{\alpha + \beta},$$

where $f_j$ are the weighted observed frequencies of the column, $P_j$ the background frequencies, $q_{ij}$ the target frequencies implicit in the BLOSUM62 matrix, $\beta = 10$, and $\alpha = N_C - 1$, with $N_C$ the mean number of different residue types (gaps included) per column of the part of the alignment that the column belongs to. The score is then a scaled $\log(Q_i/P_i)$. Dirichlet mixtures (Sjölander et al. 1996) go one step further and choose among several Dirichlet components by how well each explains the column.

**Sequence weights.** Ten near-identical sequences and one distant sequence should not give a 10 to 1 vote. Weighting schemes, such as the position-based weights of Henikoff and Henikoff (1994), give each sequence a weight and use weighted counts in place of $n_j(a)$.

**Scanning a sequence.** To find sites in a sequence of length $n$, compute $S$ for each of the $n - L + 1$ windows, in $\Theta(nL)$ time, and report the windows above a threshold. Under the background model the columns are independent, so the distribution of $S$ is the convolution of the $L$ column distributions. With scores rounded to a grid, a dynamic program over the positions computes this distribution exactly, and with it the P-value of a threshold.

## Examples

Take the six match columns (1, 2, 3, 4, 6 and 7) of the DNA alignment on the [consensus sequence](/consensus-sequence/) page, a uniform background $q_a = 1/4$, and Laplace pseudocounts. Column 1 has T 5 and C 1, so $p_1(T) = 6/10$, $p_1(C) = 2/10$ and $p_1(A) = p_1(G) = 1/10$. The scores in bits are:

| position | A | C | G | T |
|---|---|---|---|---|
| 1 | $-1.322$ | $-0.322$ | $-1.322$ | $1.263$ |
| 2 | $1.263$ | $-1.322$ | $-0.322$ | $-1.322$ |
| 3 | $-1.170$ | $-1.170$ | $-1.170$ | $1.415$ |
| 4 | $0.678$ | $-1.322$ | $0.678$ | $-1.322$ |
| 5 | $1.263$ | $-1.322$ | $-0.322$ | $-1.322$ |
| 6 | $-0.322$ | $-0.322$ | $-1.322$ | $1.000$ |

Position 3 has only five residues (one row has a gap), so its T gets $6/9 = 2/3$ and a higher score, 1.415, than the T of position 1. Position 4 is the A and G tie, and both get $\log_2(8/5) = 0.678$.

**Scores of windows.** TATAAT and TATGAT both score $1.263 + 1.263 + 1.415 + 0.678 + 1.263 + 1.000 = 6.882$ bits, the maximum over all $4^6 = 4096$ windows. CATAAT scores 5.297, TACGAT 4.297, and CGCGCG $-3.780$; the minimum is $-7.780$. Under the uniform background, 2 of the 4096 windows score at least 6.882, so the P-value of a perfect site is $2/4096 \approx 0.00049$; 34 windows score at least 4.297, a P-value of about 0.0083. The expected score is $+2.358$ bits for a window drawn from the site model and $-2.364$ bits for a window drawn from the background.

Scanning GCTATAATGCGTATGATC gives 13 windows. Two of them, TATAAT at offset 2 and TATGAT at offset 11, score 6.882; the next best is $-0.610$.

**The effect of the pseudocount weight.** In column 1 (T 5, C 1, A 0, G 0, so $N = 6$) spread a total weight $\alpha$ evenly, $\alpha/4$ to each base:

| $\alpha$ | $p(A)$ | $p(T)$ | $W(A)$ | $W(T)$ |
|---|---|---|---|---|
| 0 | 0 | 5/6 | $-\infty$ | 1.737 |
| 1/2 | 1/52 | 41/52 | $-3.700$ | 1.657 |
| 1 | 1/28 | 3/4 | $-2.807$ | 1.585 |
| 2 | 1/16 | 11/16 | $-2.000$ | 1.459 |
| 4 | 1/10 | 3/5 | $-1.322$ | 1.263 |
| 10 | 5/32 | 15/32 | $-0.678$ | 0.907 |
| 100 | 25/106 | 15/53 | $-0.084$ | 0.179 |

Without pseudocounts, one A at position 1 makes a window impossible. A small $\alpha$ keeps the penalty for A large but finite. A very large $\alpha$ washes out the data: at $\alpha = 100$ the column says almost nothing. The row $\alpha = 4$ is Laplace's rule, used in the table above.

## Where it is used

- **PSI-BLAST.** PSI-BLAST runs a [BLAST](/blast/) search, builds a PSSM from the alignments of the hits with $E$-value below an inclusion threshold, and searches again with the PSSM in place of the query and its [substitution matrix](/substitution-matrix/). The query is the master row: columns where the query has a gap are left out, rows identical to the query are removed, and only one copy of rows more than 98 percent identical is kept. The gap costs stay the same as in BLAST. Each round finds more distant members of the family.
- **Binding sites and motifs.** DNA binding sites of transcription factors are stored and scanned as PSSMs, and motif finders such as those based on [Gibbs sampling](/gibbs-sampling/) report their motifs as PSSMs.
- **Profile alignment.** A PSSM with gap costs is a profile, and [profile alignment](/sequence-profile-alignment/) aligns a sequence to it with gaps.
- **Profile HMMs.** The match states of a [profile HMM](/profile-hmm/) are the rows of a PSSM, with insert and delete states and their transition probabilities added.
- **Structure prediction.** Programs such as [PSIPRED](/psipred/) take the PSI-BLAST PSSM of a protein as the input of a predictor of secondary structure.

## References
