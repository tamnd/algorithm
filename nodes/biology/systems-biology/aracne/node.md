---
tag: VF2D8H
kind: algorithm
slug: aracne
name: ARACNE
aliases:
- algorithm for the reconstruction of accurate cellular networks
area: biology/systems-biology
level: advanced
summary: Keep gene pairs with high mutual information, then delete the weakest edge of each triangle by the data processing inequality.
solves: [gene-regulatory-network-inference]
model: real-ram
complexity:
  vars: {m: the number of genes, n: the number of samples, b: the number of bins per gene}
  time: {worst: O(m n log n + m^2 (n + b^2) + m^3)}
  space: {extra: Θ(m^2 + m n)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2006
  people: [Adam A. Margolin, Ilya Nemenman, Katia Basso, Chris Wiggins, Gustavo Stolovitzky, Riccardo Dalla Favera, Andrea Califano]
  note: Margolin and coauthors published ARACNE in BMC Bioinformatics in 2006, after Basso et al. used it in 2005 to build a regulatory network of human B cells.
prereqs: [gene-regulatory-network-inference, kullback-leibler-divergence, shannon-entropy]
see_also: [genie3, gene-regulatory-network, gaussian-graphical-model, bayesian-network, permutation-test, kernel-density-estimation, maximum-spanning-tree, feed-forward-loop]
sources:
  - paper: doi:10.1186/1471-2105-7-S1-S7
    title: Adam A. Margolin, Ilya Nemenman, Katia Basso, Chris Wiggins, Gustavo Stolovitzky, Riccardo Dalla Favera and Andrea Califano, ARACNE, an algorithm for the reconstruction of gene regulatory networks in a mammalian cellular context, BMC Bioinformatics 7 (Suppl 1), S7, 2006
    locator: the sections on the algorithm (MI estimation, the threshold and the DPI with tolerance), Theorems 1 to 3 on exact reconstruction, and the complexity O(N^3 + N^2 M^2)
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, 2nd edition, Wiley, 2006
    locator: Section 2.8, the data-processing inequality (Theorem 2.8.1)
  - paper: doi:10.1038/ng1532
    title: Katia Basso, Adam A. Margolin, Gustavo Stolovitzky, Ulf Klein, Riccardo Dalla Favera and Andrea Califano, Reverse engineering of regulatory networks in human B cells, Nature Genetics 37(4), 2005
    locator: the application of ARACNE to B cell expression profiles
  - paper: doi:10.1093/bioinformatics/btw216
    title: Alexander Lachmann, Federico M. Giorgi, Gonzalo Lopez and Andrea Califano, ARACNe-AP, gene network reverse engineering through adaptive partitioning inference of mutual information, Bioinformatics 32(14), 2016
    locator: the adaptive partitioning estimator and the bootstrap consensus
  - paper: "Atul J. Butte and Isaac S. Kohane, Mutual information relevance networks, functional genomic clustering using pairwise entropy measurements, Pacific Symposium on Biocomputing 2000"
    title: Atul J. Butte and Isaac S. Kohane, Mutual information relevance networks, 2000
    locator: the relevance network, all gene pairs with mutual information above a threshold
  - paper: doi:10.1038/nmeth.2016
    title: Daniel Marbach et al., Wisdom of crowds for robust gene network inference, Nature Methods 9(8), 2012
    locator: the DREAM5 comparison, in which ARACNE is one of the mutual information methods
---

ARACNE builds an undirected network of genes from expression data in two steps. First it estimates the [mutual information](/kullback-leibler-divergence/) of every pair of genes and keeps the pairs above a threshold $I_0$. Then it looks at every triangle of kept pairs and deletes the edge with the smallest mutual information, because the data processing inequality says that an indirect link through a third gene can never carry more information than the two direct links it passes through. The method is one heuristic answer to [gene regulatory network inference](/gene-regulatory-network-inference/). With exact mutual information values and a true network that is a tree, it returns that tree exactly; with estimated values it has no such guarantee. For $m$ genes and $n$ samples it runs in $O(m n \log n + m^2 (n + b^2) + m^3)$ time with a binned estimator on $b$ bins.

## In plain words

Two genes whose levels rise and fall together across many samples share information: knowing one tells you something about the other. A first guess at the network joins every pair that shares a lot of information. That guess has too many links. If gene A controls B and B controls C, then A and C also move together, only because B sits between them.

ARACNE removes those extra links with one rule. Look at any three genes that are all joined. The weakest of the three links is the most likely to be the indirect one, so cut it. Do this for every such group of three, decide all the cuts first, and then remove them together. What is left is a sparse network that keeps the strongest direct links.

## The problem

**Input.** An expression matrix with $m$ genes and $n$ samples, $x_{g s}$ for gene $g$ and sample $s$; a threshold $I_0 \ge 0$; and a tolerance $\tau \in [0, 1)$. Genes are numbered 1 to $m$ on this page and 0 to $m - 1$ in the code.

**Output.** A set of undirected edges $\{i, j\}$, read as "genes $i$ and $j$ interact, directly". ARACNE gives no direction and no sign.

The mutual information of two random variables is the [Kullback-Leibler divergence](/kullback-leibler-divergence/) of their joint law from the product of the marginals,

$$I(X; Y) = D_{\mathrm{KL}}(P_{XY} \,\|\, P_X P_Y) = H(X) + H(Y) - H(X, Y),$$

with $H$ the [Shannon entropy](/shannon-entropy/) in nats. It is zero exactly when $X$ and $Y$ are independent, and for jointly normal variables with correlation $\rho$ it is $-\tfrac12 \ln(1 - \rho^2)$. This site has no separate page on mutual information.

## The algorithm

Write $I_{ij}$ for the estimate of $I(X_i; X_j)$.

```pseudo id=main
ARACNE(X, I0, τ)
L1  for each pair of genes i < j do
L2      I[i, j] ← estimated mutual information of rows i and j of X
L3  E ← { {i, j} : I[i, j] > I0 }
L4  D ← ∅                                   ▷ edges to delete
L5  for each triangle {i, j, k} whose three edges are all in E do
L6      for each edge e of the triangle do
L7          if I(e) < (1 - τ) · I(f) for both other edges f of the triangle then D ← D ∪ {e}
L8  return E \ D
```

Lines L1 and L2 fill the matrix of pairwise estimates. Line L3 is the *relevance network*: all pairs above the threshold. Lines L5 to L7 apply the data processing inequality to every triangle of the relevance network, and line L8 removes all marked edges at the end. Because the marks are made on the fixed set $E$, the result does not depend on the order in which the triangles are visited. With $\tau = 0$, line L7 marks the strict minimum of each triangle, and it marks nothing when the two smallest values are equal. A tolerance $\tau > 0$ marks an edge only when it is clearly the weakest, so it keeps more edges and some small loops. Margolin et al. write the condition as $I_{ij} \le I_{ik} (1 - \tau)$ and report that values of $\tau$ below 0.15 gave a reasonable trade-off on their test networks.

**Estimating $I_{ij}$.** The paper applies a rank (copula) transform to each gene, so that each marginal is uniform on $[0, 1]$, and then uses a Gaussian kernel density estimator with one fixed kernel width. The threshold $I_0$ comes from a null: shuffle the samples of each gene to break all dependence, estimate the mutual information of the shuffled pairs, and pick $I_0$ at a chosen p-value, with an exponential fit to the tail for small p-values. The implementation on this site uses a simpler estimator: it puts the ranks of each gene into $b$ bins of equal size and computes the plug-in value $\sum_{u, v} \hat p_{uv} \ln(\hat p_{uv} / (\hat p_u \hat p_v))$. It takes $I_0$ as a parameter, and it leaves out the kernel estimator, the permutation null and the bootstrap of later versions. The pruning step, lines L3 to L8, is the same as in the paper.

## Example

Take four genes A, B, C and D in a tree with B at the center: A, C and D each connect to B only. Let the expression be jointly normal with correlations 0.9 for A and B, 0.8 for B and C and 0.7 for B and D. In such a tree, the correlation of two genes is the product of the correlations along the path between them, so A and C have 0.72, A and D have 0.63, and C and D have 0.56. The exact mutual information values $-\tfrac12 \ln(1 - \rho^2)$ are:

| pair | AB | BC | AC | BD | AD | CD |
|---|---|---|---|---|---|---|
| $\rho$ | 0.9 | 0.8 | 0.72 | 0.7 | 0.63 | 0.56 |
| $I$ (nats) | 0.830366 | 0.510826 | 0.365321 | 0.336672 | 0.252836 | 0.188147 |

With $I_0 = 0.1$, line L3 keeps all six pairs, so all four triangles are present. With $\tau = 0$, line L7 marks AC in triangle ABC, AD in ABD, CD in ACD and CD again in BCD. Line L8 returns AB, BC and BD, the true tree. With $\tau = 0.15$ the result is the same, because in every triangle the weakest edge is below $0.85$ times the other two (the largest ratio is $0.252836 / 0.336672 = 0.751$, in ABD). With $\tau = 0.3$ the factor is 0.7. Then AC survives, since $0.365321 / 0.510826 = 0.715 > 0.7$, and so does AD, since $0.751 > 0.7$; CD is still marked in BCD, where its ratio to BD is $0.559$. So the result has five edges: the tree and the two indirect edges AC and AD.

**On sampled data.** The test of the implementation simulates a normal tree model with 8 genes, 7 edges with correlations from 0.7 to 0.85, and 250 samples (seed 7), and uses 4 bins and $I_0 = 0.05$. All 28 pairs pass the threshold, so the relevance network is the complete graph. After the DPI step, the result is exactly the 7 true edges. This is one measurement on easy data, not a guarantee: with fewer samples, weaker links or a network with many short loops, ARACNE deletes true edges and keeps false ones.

## Correctness

ARACNE is a heuristic, so its correctness has two parts. The first part is that the code computes what lines L3 to L8 define: the set of edges of the relevance network that are not the $(1 - \tau)$-weakest edge of any of its triangles. The loop visits each triangle once and the marks do not change $E$, so this holds by inspection; the test compares it with a direct check of the definition over all triples.

The second part is what the output means. The data processing inequality (Cover and Thomas, Theorem 2.8.1) says that if $X \to Y \to Z$ is a Markov chain, then $I(X; Z) \le I(X; Y)$, and since $Z \to Y \to X$ is also a Markov chain, $I(X; Z) \le \min(I(X; Y), I(Y; Z))$. Suppose the joint law of the genes is Markov with respect to a tree $T$, so that $X_i$ and $X_k$ are independent given $X_j$ whenever $j$ lies on the path from $i$ to $k$ in $T$.

**Theorem.** Assume the values $I_{ij}$ are exact, $I_0 < I_{ij}$ for every edge $\{i, j\}$ of $T$, and for any three distinct genes with $j$ on the path from $i$ to $k$ in $T$, $I_{ik} < (1 - \tau) \min(I_{ij}, I_{jk})$. Then ARACNE returns exactly the edges of $T$.

The proof has two steps. No edge of $T$ is marked: for an edge $\{i, j\}$ and a third gene $k$ on the side of $i$, gene $i$ is on the path from $k$ to $j$, so $I_{kj} < I_{ij}$, and line L7 cannot mark $\{i, j\}$ against $\{k, j\}$. Every other edge that passes the threshold is marked: for a pair $\{i, k\}$ at distance at least 2 in $T$, let $j$ be the neighbor of $i$ on the path; then $\{i, j\}$ passes the threshold by assumption, $\{j, k\}$ passes it because $I_{jk} > I_{ik} > I_0$, and line L7 marks $\{i, k\}$ in the triangle $\{i, j, k\}$. This is Theorem 1 of Margolin et al. The DPI gives the hypothesis with $\le$ in place of $<$ and $\tau = 0$; the strict form holds, for example, for a normal tree with all correlations in $(0, 1)$ in absolute value, because $|\rho_{ik}| = |\rho_{ij}| |\rho_{jk}|$. The full proof is below.

The theorem says nothing about networks with loops, such as a [feed-forward loop](/feed-forward-loop/), where the true triangle loses its weakest edge.

## Complexity

The model is the real RAM, with each logarithm and division as one step.

- **Estimates, lines L1 and L2.** Ranking each gene costs $O(n \log n)$, so $O(m n \log n)$ for all genes. Each of the $m(m - 1)/2$ pairs then costs $O(n)$ to fill a $b \times b$ table of counts and $O(b^2)$ to sum it, so $O(m^2 (n + b^2))$ in all. The kernel estimator of the paper costs $O(n^2)$ per pair instead, which gives the term $N^2 M^2$ of the paper for $N$ genes and $M$ samples.
- **Pruning, lines L3 to L8.** Line L3 is $O(m^2)$. The triangles are found by intersecting the neighbor sets of the two ends of each edge, which is $O(m)$ per edge and $O(m^3)$ in all, and each triangle costs $O(1)$. When all pairs pass the threshold there are $\binom{m}{3}$ triangles, so the bound $m^3$ is reached.
- **Space.** The matrix of estimates takes $\Theta(m^2)$ numbers and the bins take $\Theta(m n)$.

In practice the estimation term dominates for many samples. For the full genome ($m$ near 20000) the $m^3$ term is large too. A common remedy is to keep only the pairs that contain a known transcription factor.

## Properties

- **Deterministic.** For fixed estimates, the output does not depend on the gene order, by the two-phase marking.
- **Monotone in $\tau$.** A larger tolerance marks a subset of the edges, so the output grows with $\tau$.
- **Undirected and unsigned.** Mutual information is symmetric and ignores the sign of the dependence, so ARACNE cannot tell activation from repression or cause from effect.
- **Contains the Chow-Liu tree.** The Chow-Liu tree is a [maximum spanning tree](/maximum-spanning-tree/) of the complete graph weighted by mutual information. With $\tau = 0$ and $I_0 = 0$, every edge of positive weight of such a tree is in the output (Theorem 2 of the paper states this for exact values). The reason is the cycle property: line L7 marks only the strict minimum of a triangle, and the strict minimum of a cycle is in no maximum spanning tree.

## Variants and improvements

- **Relevance network.** Stop after line L3. This is the older method of Butte and Kohane, which keeps all indirect links.
- **Known regulators.** Keep only pairs with at least one transcription factor, and apply the DPI only to triangles that contain a transcription factor. This cuts the work and the number of target to target edges.
- **ARACNe-AP.** Lachmann et al. (2016) estimate the mutual information with adaptive partitioning, which is much faster than the kernel estimator, and run ARACNE on many bootstrap samples, keeping the edges that appear more often than chance.
- **Other uses of mutual information.** CLR scores each pair against the background distribution of the mutual information of each gene, and MRNET picks edges by a minimum redundancy rule. DREAM5 (Marbach et al. 2012) compared several mutual information methods with regression, correlation and Bayesian network methods, and found that mutual information and correlation methods recovered feed-forward loops better than the regression methods.
- **Conditional independence instead of the DPI.** A [Gaussian graphical model](/gaussian-graphical-model/) removes an edge when the partial correlation, given all other genes, is zero. It handles loops, but needs more samples than genes or a sparsity penalty.

## When to use it

Use ARACNE for many samples of one cell type, under many conditions, when you want a sparse, undirected list of candidate direct partners of each regulator, and you accept that true triangles are broken. The estimates need many samples: with a few dozen, the noise in the mutual information is of the same size as the gaps that line L7 compares. For directed links from regulators to targets, a regression method such as [GENIE3](/genie3/) ranks the candidates; for time series, a [dynamic Bayesian network](/dynamic-bayesian-network/) can use the time order.

## Pitfalls

- **Real loops are cut.** Every triangle loses one edge with $\tau = 0$. A feed-forward loop, common in transcription networks, always loses one of its three links.
- **Ties.** With $\tau = 0$ and the strict test of line L7, a triangle with two equal smallest values loses neither. Binned estimates on small samples give many ties; a small $\tau$ or a finer estimator avoids surprises.
- **Estimator bias.** The plug-in estimate on $b$ bins is biased upward by about $(b - 1)^2 / (2n)$ nats for independent genes, so the threshold must come from a null on the same $n$ and $b$, not from a fixed number.
- **Order of removal.** Deleting the weakest edge of each triangle at once, in a loop over triangles, gives a result that depends on the order. Mark first, then delete.
- **Not causal.** An edge means strong dependence that the DPI step did not explain away. A hidden common regulator that is not measured makes two targets look directly linked.

## Implementations

## History

Butte and Kohane proposed relevance networks of mutual information in 2000. Basso, Margolin, Stolovitzky, Klein, Dalla Favera and Califano used ARACNE in 2005 to reconstruct a regulatory network of human B cells. Margolin and coauthors gave the full description, the theorems and the tests on synthetic networks in BMC Bioinformatics in 2006. Lachmann, Giorgi, Lopez and Califano published the faster ARACNe-AP in 2016.

## References
