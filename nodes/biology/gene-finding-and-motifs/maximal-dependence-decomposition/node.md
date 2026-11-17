---
tag: 7S803Q
kind: algorithm
slug: maximal-dependence-decomposition
name: Maximal dependence decomposition
aliases:
- MDD splice model
area: biology/gene-finding-and-motifs
level: advanced
summary: Build a tree of weight matrices for a signal by splitting the sites on the position with the strongest dependence by chi-squared test.
model: real-ram
complexity:
  vars: {p: the length of a site, N: the number of training sites}
  time: {worst: O(p^3 N), average: O(p^3 N), best: Θ(p^2 N)}
  space: {extra: O(p N + p^2)}
properties: {deterministic: true, exact: true, online: false, recursive: true}
prereqs: [position-specific-scoring-matrix, chi-squared-test-of-independence]
see_also: [splice-site-prediction, generalized-hmm-gene-finder, gene-prediction, decision-tree, sequence-logo, naive-bayes-classifier, kullback-leibler-divergence, interpolated-markov-model]
sources:
  - paper: doi:10.1006/jmbi.1997.0951
    title: Chris Burge and Samuel Karlin, Prediction of complete gene structures in human genomic DNA, Journal of Molecular Biology 268(1), 1997
    locator: pp. 78 to 94; the maximal dependence decomposition model of the donor splice site, built from chi-squared tests of the consensus indicators against the other positions
  - paper: doi:10.1016/S0959-440X(98)80069-9
    title: Christopher B. Burge and Samuel Karlin, Finding the genes in genomic DNA, Current Opinion in Structural Biology 8(3), 1998
    locator: pp. 346 to 354; the list of splice site models and Table 1, the accuracy of the GENSCAN splice site models alone and inside the gene finder
  - paper: doi:10.1089/1066527041410418
    title: Gene Yeo and Christopher B. Burge, Maximum entropy modeling of short sequence motifs with applications to RNA splicing signals, Journal of Computational Biology 11(2-3), 2004
    locator: the maximum entropy models of 9 base donor sites and 23 base acceptor sites, compared with simpler splice site models
---

Maximal dependence decomposition (MDD) is a model of a short signal in DNA, such as the donor (5') splice site at the start of an intron. A [position weight matrix](/position-specific-scoring-matrix/) treats the positions of a site as independent. In real donor sites they are not, and Burge and Karlin found significant dependences between their positions. MDD finds such dependence in a set of aligned training sites and builds a binary tree from it. At each node it measures, with a [chi-squared test](/chi-squared-test-of-independence/), how strongly "the base at position $i$ is the consensus base" is linked to the base at each other position $j$. It splits the sites on the position $i$ with the largest total and repeats the work in both parts. Each leaf is a weight matrix. Burge and Karlin (1997) introduced MDD for the donor site model of the GENSCAN gene finder, a [generalized HMM](/generalized-hmm-gene-finder/).

## In plain words

You have a few thousand real splice sites, all aligned. Ask, for each position: if I know whether this position shows its usual base, how much does that tell me about the other positions? Take the position that tells the most and sort the sites into two piles: the ones that show the usual base there and the ones that do not. Then ask the same question in each pile, with that position removed. Stop when a pile is small, or when no position tells much any more. In the end, each pile has its own simple table of base frequencies. To score a new site, follow its bases down the tree to one pile, and multiply the frequencies along the way and in the table of that pile.

## The problem

**Input.** A list $D$ of $N$ aligned sites $x = x_0 \cdots x_{p-1}$ over $\Sigma = \{A, C, G, T\}$, a consensus string $c$ (by default the most frequent base at each position), a cutoff $\kappa$ for the chi-squared statistic, a minimum subset size $m$, and a pseudocount $\alpha > 0$.

**Output.** A probability model $P$ on $\Sigma^p$ that captures the strongest dependences of the training sites, and a way to compute $\ln P(x)$ for a new site. In a gene finder, the score of a candidate site is the log-likelihood ratio $\ln P(x) - \ln P_{\text{bg}}(x)$ against a background model.

For positions $i \ne j$, let $C_i$ be the indicator of $x_i = c_i$. The statistic $\chi^2(C_i, X_j)$ is Pearson's statistic of the $2 \times 4$ table of counts that crosses $C_i$ with the base $x_j$ over the sites of a node. With 3 degrees of freedom, the 0.001 critical value is about 16.27, so a cutoff of 16.3 marks the pairs that are clearly dependent. The sum $S_i = \sum_{j \ne i} \chi^2(C_i, X_j)$ is the total dependence of the other positions on $C_i$.

## The algorithm

```pseudo id=main
MDD-BUILD(D, R, c)
L1  if |R| ≤ 1 then return a leaf with the weight matrix of D on R
L2  for each pair i ≠ j in R: χ²[i][j] ← the chi-squared statistic of C_i against X_j over D
L3  if no χ²[i][j] is above the cutoff κ then return a leaf with the weight matrix of D on R
L4  i* ← the i in R with the largest S_i = Σ over j ≠ i of χ²[i][j], ties to the smaller i
L5  D⁺ ← the sites of D with x_i* = c_i*; D⁻ ← the other sites
L6  if |D⁺| < m or |D⁻| < m then return a leaf with the weight matrix of D on R
L7  return a split on i* with the base distribution q of D at i* and the children MDD-BUILD(D⁺, R - {i*}, c) and MDD-BUILD(D⁻, R - {i*}, c)

MDD-LOG-PROB(x, v)
L8  if v is a leaf then return Σ over j in R_v of ln w_v[j](x_j)
L9  return ln q_v(x_i*) + MDD-LOG-PROB(x, the child of v that x_i* = c_i* selects)
```

The first call is MDD-BUILD$(D, \{0, \ldots, p - 1\}, c)$. Every base distribution, in a leaf ($w_v[j]$) or at a split ($q_v$), is (count $+ \alpha$) $/$ ($|D_v| + 4\alpha$), so no probability is 0. The consensus stays the one of the full training set at every node, as in the original model.

## Example

Take the eight sites GAT, GAT, GCT, GAT, GAA, AAC, CAG and TCT, so $p = 3$, $N = 8$ and the consensus is GAT. Use the toy values $\kappa = 3$, $m = 3$ and $\alpha = \frac12$. For the pair $(0, 2)$, the five sites with G at position 0 have the bases T, T, T, T, A at position 2, and the other three have C, G, T. The table is:

| | A | C | G | T | total |
|---|---|---|---|---|---|
| $x_0 = G$ | 1 | 0 | 0 | 4 | 5 |
| $x_0 \ne G$ | 0 | 1 | 1 | 1 | 3 |
| total | 1 | 1 | 1 | 5 | 8 |

The expected counts are $5/8, 5/8, 5/8, 25/8$ in the first row and $3/8, 3/8, 3/8, 15/8$ in the second, and $\chi^2 = \frac{344}{75} \approx 4.587$. All six statistics are:

| $i$ | $j$ | $\chi^2(C_i, X_j)$ |
|---|---|---|
| 0 | 1 | $8/45 \approx 0.178$ |
| 0 | 2 | $344/75 \approx 4.587$ |
| 1 | 0 | $56/15 \approx 3.733$ |
| 1 | 2 | $8/5 = 1.600$ |
| 2 | 0 | $344/75 \approx 4.587$ |
| 2 | 1 | $8/5 = 1.600$ |

Three of them are above 3, so the node is split. The sums are $S_0 \approx 4.764$, $S_1 \approx 5.333$ and $S_2 \approx 6.187$, so line L4 picks position 2 with consensus T. The five sites with T at position 2 (GAT, GAT, GCT, GAT, TCT) go to $D^+$, and the other three (GAA, AAC, CAG) go to $D^-$. Both children have the positions $\{0, 1\}$, and neither can be split again without a part under $m = 3$ or a statistic above 3, so both are leaves.

- Root, position 2: $q(T) = \frac{11}{20}$ and $q(A) = q(C) = q(G) = \frac{3}{20}$.
- Leaf $+2$ (5 sites): position 0 has G $\frac{9}{14}$, T $\frac{3}{14}$, A and C $\frac{1}{14}$; position 1 has A $\frac{1}{2}$, C $\frac{5}{14}$, G and T $\frac{1}{14}$.
- Leaf $-2$ (3 sites): position 0 has A, C and G $\frac{3}{10}$ and T $\frac{1}{10}$; position 1 has A $\frac{7}{10}$ and C, G and T $\frac{1}{10}$.

Then $P(\mathrm{GAT}) = \frac{11}{20} \cdot \frac{9}{14} \cdot \frac{1}{2} = \frac{99}{560} \approx 0.177$, and $P(\mathrm{AAT}) = \frac{11}{20} \cdot \frac{1}{14} \cdot \frac{1}{2} = \frac{11}{560} \approx 0.020$. A single weight matrix of the same eight sites gives $0.197$ and $0.054$. In the training data, A at position 0 occurs only when position 2 is not T, and MDD has learned that: it gives AAT less than half of the weight-matrix probability.

## Correctness

MDD-BUILD is a recursive partition, and the proof has three parts. First, every split removes its position from $R$ and a node with at most one position is a leaf, so the recursion ends and the tree has depth at most $p - 1$. Second, a split puts each site into exactly one child, so the leaves partition the training sites. Third, the model is a probability distribution: by induction on the height of a node, the sum of $P_v$ over all bases at its positions is 1, because a leaf is a product of distributions on separate positions, and a split multiplies the distribution $q_v$ at its position by a child whose distribution, by induction, sums to 1 over the remaining positions. MDD-LOG-PROB is the logarithm of that product. The full proof is in the proofs folder, and the test file checks that the probabilities of all $4^4$ sites of length 4 sum to exactly 1.

## Complexity

- **Building.** At a node with $N_v$ sites and $r$ positions, line L2 fills $r(r - 1)$ tables, each in one pass over the sites, in $O(r^2 N_v)$ time. The nodes of one depth hold disjoint sets of sites, so a depth costs $O(p^2 N)$, and the depth is at most $p - 1$, which gives $O(p^3 N)$. If the root is a leaf, the time is $\Theta(p^2 N)$. Splice site models use about 9 positions for a donor site, so the build takes very little time.
- **Scoring.** A site follows one path and multiplies at most $p$ factors, so $\ln P(x)$ takes $O(p)$ time, the same as a weight matrix. To scan a sequence of length $n$, the cost is $O(n p)$.
- **Space.** The recursion holds the site lists of the current path, $O(p N)$ in the worst case, and the statistics of one node, $O(p^2)$. The tree has at most $\min(2^{p-1}, N / m)$ leaves, each with a matrix of $4p$ numbers.

## Properties

- **A tree of weight matrices.** Each leaf is a position weight matrix of the positions that its path has not used. A tree with one leaf is the weight matrix of all the data, and the test file checks this case.
- **Models dependence with little data.** A full first-order or higher-order model has many more parameters. MDD spends parameters only on the dependences that the test marks as strong, and the minimum size $m$ stops it from fitting small subsets.
- **Asymmetric, by design.** It conditions on the consensus indicator $C_i$, not on the full base $x_i$. Each split has two children, so the data are not cut into four parts at each level.
- **Greedy.** The split at each node is the best one by the sum of the statistics. It is not a search over all trees, and there is no claim that the tree is optimal for the likelihood.
- **Deterministic.** With the tie rule of line L4, the same data give the same tree.

## Variants and improvements

- **Other signals.** The same procedure can model acceptor sites, start codons or other short signals. Burge and Karlin used MDD for the donor site and a windowed weight array model, which conditions each position on the one before it, for the acceptor.
- **Other split tests.** Mutual information or a likelihood ratio can replace the chi-squared statistic. The tree is then a [decision tree](/decision-tree/) built for density estimation.
- **Maximum entropy models.** Yeo and Burge (2004) fit the distribution of largest entropy that matches chosen low-order marginal counts of real sites. The model uses all pairs of positions, not one tree, and they report it as more accurate than simpler splice site models.
- **Bayesian networks and discriminative models.** A Bayesian network learns a general graph of dependences between positions. Support vector machines and neural networks learn a classifier of true against false sites directly, at the cost of a less transparent model.

## When to use it

Use MDD for a short signal with a known alignment and a clear consensus, when the training set is a few hundred to a few thousand sites, and when there is evidence of dependence between positions that a weight matrix misses. It fits well inside a generalized HMM, where a signal model must return a probability in $O(p)$ time. For a signal with no clear consensus, or for very large training sets, a maximum entropy model or a discriminative classifier is often better.

## Pitfalls

- **The cutoff is not a test of the tree.** The statistics of a node are tested many times and on data chosen by earlier splits, so the 0.001 level is only a rule of thumb.
- **Small subsets.** Without a minimum size, deep leaves have few sites and their matrices are noise. Choose $m$ so that each leaf has enough sites for $4|R|$ frequencies, and use pseudocounts.
- **Consensus from the full data.** Using the consensus of the subset at a lower node changes the meaning of $C_i$ and the tree; keep one consensus, or say clearly which one is used.
- **Probability, not a score.** $P(x)$ alone ranks sites by how typical they are. To separate true sites from random sequence that happens to contain GT, compare it with a background model.
- **Alignment.** The model assumes that every site is aligned on the same exon and intron boundary. Sites from a wrong annotation add false dependence.

## Implementations

## History

Burge and Karlin introduced maximal dependence decomposition in their 1997 paper on GENSCAN, as the model of the donor splice site, after they found dependences between the positions of human donor sites that a weight matrix does not capture. Their 1998 review lists MDD with the weight array model, HMMs, decision trees and neural networks as the main models of splice sites, and reports in its Table 1 that the GENSCAN splice site models, on the Burset and Guigó set of vertebrate genes, are much more accurate inside the gene finder than alone. Yeo and Burge (2004) later proposed maximum entropy models of splice sites as a more general way to model the same dependences.

## References
