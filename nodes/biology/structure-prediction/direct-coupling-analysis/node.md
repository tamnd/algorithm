---
tag: 4X9C5V
kind: algorithm
slug: direct-coupling-analysis
name: Direct coupling analysis
aliases:
- DCA
- Mean-field DCA
area: biology/structure-prediction
level: research
summary: Fits a Potts model to a protein family alignment and ranks residue pairs by their direct couplings. The mean-field form inverts one correlation matrix.
solves: [contact-map-prediction]
model: real-ram
complexity:
  vars: {m: the number of sequences, n: the number of alignment columns, q: the number of states per column}
  time: {worst: "O(m^2 n + m n^2 + n^3 q^3)"}
  space: {extra: "O(m n + n^2 q^2)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2009
  people: [Martin Weigt, Robert A. White, Hendrik Szurmant, James A. Hoch, Terence Hwa]
  note: Weigt et al. (2009) separated direct from indirect correlations with a Potts model fitted by message passing. Morcos et al. (2011) replaced the fit by a mean-field inversion and predicted contacts across many families. Ekeberg et al. (2013) fitted the model by pseudo-likelihood.
prereqs: [contact-map-prediction, potts-model, mean-field-approximation]
see_also: [alphafold, markov-random-field, gaussian-graphical-model, ising-model, belief-propagation, maximum-likelihood-estimation, matrix-inversion, shannon-entropy]
sources:
  - paper: doi:10.1073/pnas.0805923106
    title: Martin Weigt, Robert A. White, Hendrik Szurmant, James A. Hoch and Terence Hwa, Identification of direct residue contacts in protein-protein interaction by message passing, PNAS 106(1), 2009, 67-72
    locator: the Potts model of an alignment, direct information, and the separation of direct from indirect correlations
  - paper: doi:10.1073/pnas.1111471108
    title: Faruck Morcos, Andrea Pagnani, Bryan Lunt, Arianna Bertolino, Debora S. Marks, Chris Sander, Riccardo Zecchina, José N. Onuchic, Terence Hwa and Martin Weigt, Direct-coupling analysis of residue coevolution captures native contacts across many protein families, PNAS 108(49), 2011, E1293-E1301
    locator: mean-field DCA, with sequence reweighting, pseudocounts, the couplings as the negative inverse correlation matrix, and direct information
  - paper: doi:10.1103/PhysRevE.87.012707
    title: Magnus Ekeberg, Cecilia Lövkvist, Yueheng Lan, Martin Weigt and Erik Aurell, Improved contact prediction in proteins, using pseudolikelihoods to infer Potts models, Physical Review E 87(1), 2013, 012707
    locator: plmDCA, and the Frobenius norm score in the zero-sum gauge with the average product correction
  - paper: doi:10.1093/bioinformatics/btm604
    title: Stanley D. Dunn, Lindi M. Wahl and Gregory B. Gloor, Mutual information without the influence of phylogeny or entropy dramatically improves residue contact prediction, Bioinformatics 24(3), 2008, 333-340
    locator: the average product correction
  - paper: doi:10.1371/journal.pone.0028766
    title: Debora S. Marks, Lucy J. Colwell, Robert Sheridan, Thomas A. Hopf, Andrea Pagnani, Riccardo Zecchina and Chris Sander, Protein 3D structure computed from evolutionary sequence variation, PLoS One 6(12), 2011, e28766
    locator: folding with DCA contacts as distance restraints
  - paper: doi:10.1088/1361-6633/aa9965
    title: Simona Cocco, Christoph Feinauer, Matteo Figliuzzi, Rémi Monasson and Martin Weigt, Inverse statistical physics of protein sequences, a key issues review, Reports on Progress in Physics 81(3), 2018, 032601
    locator: a review of Potts model inference from sequences, gauges and the mean-field and pseudo-likelihood methods
---

Direct coupling analysis (DCA) predicts residue contacts from a [multiple sequence alignment](/multiple-sequence-alignment/) of a protein family. Two columns that are in contact tend to mutate together, but so do two columns that are both in contact with a third one. A local score such as mutual information cannot tell these cases apart. DCA fits one global [Potts model](/potts-model/) to all columns at once, so that each correlation is explained by a chain of direct couplings, and ranks the pairs by the strength of their own coupling. Weigt et al. (2009) introduced the method. The mean-field version of Morcos et al. (2011), described here, gets the couplings from the inverse of one correlation matrix, and made the method fast enough for routine use on large families.

## In plain words

Line up many related proteins, one per row. Each column is one place in the protein. When two places touch in the folded protein, a change at one often comes with a change at the other, so their columns change together.

The trouble is that the effect passes along. If A touches B and B touches C, then A and C also change together, even though they do not touch. Counting how often two columns change together finds all three pairs.

DCA asks a different question: what is the smallest set of direct links that explains all the patterns in the table at once? The link between A and C then comes out near zero, because the links A to B and B to C already explain it. The pairs with the strongest links are the predicted contacts.

## The problem

**Input.** An alignment $X$ of $m$ sequences and $n$ columns over $q$ states (twenty amino acids and the gap give $q = 21$), an identity threshold $\theta$, usually $0.8$, and a pseudocount weight $\lambda > 0$.

**Model.** The Potts model of the family is

$$P(x) = \frac{1}{Z} \exp\Big( \sum_{i} h_i(x_i) + \sum_{i < j} J_{ij}(x_i, x_j) \Big),$$

with fields $h_i$ and couplings $J_{ij}$. Many parameter sets give the same $P$; the *gauge* removes this freedom. Here state $q$ is the reference: $J_{ij}(a, q) = J_{ij}(q, b) = 0$ and $h_i(q) = 0$.

**Output.** An estimate $e_{ij}$ of the couplings and a ranking of the pairs $i < j$ by a score $S_{ij}$ of the size of $e_{ij}$. The top pairs are the predicted contacts.

## The algorithm

Mean-field DCA reweights the sequences, computes the one- and two-column frequencies, and inverts their correlation matrix. The reason for the inversion is the mean-field theory of the Potts model: with the marginals of a product distribution fitted to the model, the inverse of the response matrix $\partial f / \partial h$ is minus the couplings off the diagonal blocks (Correctness). DCA uses the observed correlations in place of the response matrix.

```pseudo id=main
MEAN-FIELD-DCA(X, q, θ, λ)
L1  for each sequence s: w_s ← 1 / |{t : identity(X_s, X_t) ≥ θ}|;  M_eff ← Σ_s w_s
L2  f_i(a) ← (λ/q + Σ_s w_s [X_si = a]) / (λ + M_eff)
L3  f_ij(a, b) ← (λ/q^2 + Σ_s w_s [X_si = a][X_sj = b]) / (λ + M_eff)        ▷ i ≠ j
L4  C_(i,a),(j,b) ← f_ij(a, b) − f_i(a) f_j(b) for a, b < q, with f_ii(a, b) = f_i(a) [a = b]
L5  e ← −C^(−1) by Gaussian elimination;  e_ij(a, q) ← e_ij(q, b) ← 0
L6  F_ij ← ‖ e_ij − row means − column means + total mean ‖_Frobenius for all i < j
L7  S_ij ← F_ij − F_i· F_·j / F_··                                          ▷ average product correction
L8  return the pairs (i, j) sorted by decreasing S_ij
```

Line L1 down-weights groups of near-identical sequences, which come from shared ancestry and not from independent tests of the fold. Lines L2 and L3 add a pseudocount, which is the same as mixing the data with a uniform distribution of weight $\lambda / (\lambda + M_{\mathrm{eff}})$; Morcos et al. take $\lambda = M_{\mathrm{eff}}$, a weight of one half. Without it $C$ is singular as soon as a state is missing from a column. Line L6 puts each $q \times q$ block in the zero-sum gauge before the norm, so the score does not depend on the reference state (Ekeberg et al. 2013). Line L7 is the average product correction of Dunn, Wahl and Gloor (2008): $F_{i\cdot}$ is the mean of $F_{ij}$ over $j \ne i$ and $F_{\cdot\cdot}$ the mean over all pairs.

Morcos et al. (2011) ranked the pairs by *direct information* instead of lines L6 and L7. For one pair, they fit a two-column model $P^{\mathrm{dir}}_{ij}(a, b) \propto \exp(e_{ij}(a, b) + \tilde h_i(a) + \tilde h_j(b))$, with the fields chosen so that its marginals are $f_i$ and $f_j$, and take the mutual information of $P^{\mathrm{dir}}_{ij}$. The implementation provides both scores.

## Example

**Why mutual information fails.** Take five binary columns A to E, with states 1 and 0 (0 is the reference), all fields $h = -1$, couplings $J_{AB} = J_{BC} = 2$ and $J_{DE} = 0.5$, and no other couplings. So A touches B, B touches C, D touches E, and A does not touch C. Enumerating all 32 sequences gives the exact frequencies, and from them:

| pair | true coupling | mutual information (nats) | mean-field coupling $e$ |
|---|---|---|---|
| A, B | 2 | 0.0880 | 2.3504 |
| B, C | 2 | 0.0880 | 2.3504 |
| A, C | 0 | 0.0154 | 0.0000 |
| D, E | 0.5 | 0.0058 | 0.5216 |
| all others | 0 | 0 | 0 |

Mutual information puts the false pair (A, C) third, above the true contact (D, E), because the strong chain A-B-C passes its correlation on. The mean-field couplings put (D, E) third and give (A, C) a value of 0 up to rounding. The table also shows the error of the mean-field step: the strong couplings come out 18% too large, while the weak one is within 5%.

**Sequence weights.** Take $n = 5$, $\theta = 0.8$ and the three sequences AAAAA, AAAAC and CCCCC. The first two agree at 4 of 5 positions, which reaches $0.8$, so each has two close sequences, itself included, and weight $1/2$. The third has weight 1. So $M_{\mathrm{eff}} = 2$: the two near copies count as one sequence.

**A planted model.** The tests fit weak random couplings on four columns with $q = 3$, compute the exact frequencies by enumeration of all 81 sequences and run lines L4 and L5 on them. The largest error $|e_{ij}(a, b) - J_{ij}(a, b)|$ is $0.0029$ for couplings of size up to $0.1$, and $0.00069$ for size up to $0.05$. Halving the couplings divides the error by about 4, as the second-order error of mean-field theory predicts.

## Correctness

DCA is not exact: the mean-field couplings are estimates, and a large coupling is not always a contact. What can be proved is what each step computes. The [proof](proofs/correctness.md) shows four facts. With $\lambda > 0$, $C$ is the covariance matrix of a distribution with full support on the sequences, so it is positive definite and line L5 is well defined. In the mean-field approximation of the Potts model, the inverse of the response matrix $\partial f / \partial h$ equals $-J_{ij}(a, b)$ in each off-diagonal block, which is why line L5 estimates the couplings. If the frequencies factor over the columns, every $e_{ij}$ is 0. The zero-sum gauge of line L6 does not depend on the gauge of $e$, and it has the least Frobenius norm among all gauge-equivalent forms of a block. The tests check each step against a direct computation, the couplings against the exact frequencies of planted models, and the full method against alignments sampled from a planted chain of couplings.

## Complexity

Line L1 compares all pairs of sequences, $O(m^2 n)$ time. Lines L2 and L3 visit each sequence and each pair of columns, $O(m n^2)$. The matrix $C$ has side $n(q - 1)$, so lines L4 and L5 take $O(n^2 q^2)$ and $O(n^3 q^3)$ time; the inversion dominates for long proteins. Lines L6 and L7 take $O(n^2 q^2)$ and line L8 takes $O(n^2 \log n)$. The space is the alignment, $O(m n)$, and the matrix, $O(n^2 q^2)$.

For a domain of 200 residues with $q = 21$, the matrix has side 4000, and one dense inversion of that size is a routine job for a numerical library. This speed is what the mean-field method bought over the message passing of Weigt et al. (2009).

## Properties

- **Deterministic.** The same alignment and parameters give the same ranking.
- **Approximate.** The couplings are first-order estimates; they are biased for strong couplings and noisy for few sequences.
- **Global.** Each coupling depends on the whole alignment, which is what removes the indirect correlations.
- **Gauge free score.** The Frobenius score in the zero-sum gauge, and direct information, do not depend on the choice of the reference state.
- **Unsupervised.** No known structure is used; the alignment alone is the input.

## Variants and improvements

- **Message-passing DCA.** The first version (Weigt et al. 2009) fitted the model by iterating belief-propagation-like equations; it was accurate but slow.
- **Pseudo-likelihood DCA.** plmDCA (Ekeberg et al. 2013) maximizes the product of the conditional probabilities of each column given the others, with regularization, and predicts contacts more precisely than mean field at a higher cost.
- **Sparse inverse covariance.** PSICOV treats the one-hot alignment as Gaussian and estimates a sparse inverse covariance by the graphical lasso, a [Gaussian graphical model](/gaussian-graphical-model/) view of the same step.
- **Boltzmann machine learning.** Fit the model by gradient ascent on the likelihood, with the model frequencies estimated by Monte Carlo. This is the most faithful fit and the slowest.
- **Deep networks on top.** Methods such as RaptorX-Contact feed DCA scores into a network trained on known structures; see [contact map prediction](/contact-map-prediction/).

## When to use it

Use DCA when the family has many diverse sequences, so that $M_{\mathrm{eff}}$ is well above the length of the protein. It gives contacts with no template and no training on structures, it finds interface residues between two families from a paired alignment, and its couplings also serve as a model of the effect of mutations. For the best contact precision, a learned predictor or [AlphaFold](/alphafold/) does better, and both use the same coevolution signal as input.

## Pitfalls

- **Few sequences.** With $M_{\mathrm{eff}}$ small next to $n$, the estimated $C$ is dominated by noise and so is its inverse. The pseudocount keeps $C$ invertible but does not add information.
- **No reweighting.** Without line L1, a large group of close relatives looks like strong coevolution at every pair, through shared ancestry alone.
- **Small pseudocount.** A small $\lambda$ makes $C$ almost singular, and the inverse then amplifies noise. The mean-field method needs a large pseudocount.
- **Raw couplings in the reference gauge.** The size of $e_{ij}$ in the gauge of line L5 depends on which state is the reference. Score after the zero-sum gauge, or use direct information.
- **Neighbours in the chain.** Pairs with $|i - j|$ small always score high and say little about the fold; contact predictions are scored for $|i - j| \ge 6$ and judged on long-range pairs.
- **Gappy columns and rows.** Columns or sequences that are mostly gaps add false couplings between the gap states. Filter them before the analysis.

## Implementations

## History

The idea that contacting residues coevolve is older than DCA: Göbel et al. (1994) predicted contacts from correlated mutations, and Dunn, Wahl and Gloor (2008) improved mutual information with the average product correction. The local scores still mixed direct and indirect signals. Weigt et al. (2009) fitted a Potts model to the alignments of bacterial two-component signalling proteins and found the residues at their interface by direct information. Morcos et al. (2011) made the fit a single matrix inversion with the mean-field approximation and showed that the top predictions were native contacts across many families. Marks et al. (2011) then folded proteins with these contacts as restraints. Ekeberg et al. (2013) replaced the mean-field step by pseudo-likelihood, and the coevolution scores became the main input of the deep contact predictors that followed.

## References
