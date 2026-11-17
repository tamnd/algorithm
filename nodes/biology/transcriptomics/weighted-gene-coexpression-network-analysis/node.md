---
tag: WN4DQ5
kind: algorithm
slug: weighted-gene-coexpression-network-analysis
name: Weighted gene coexpression network analysis
aliases:
- WGCNA
area: biology/transcriptomics
level: advanced
summary: Build a soft-thresholded correlation network of genes, then find modules by hierarchical clustering of topological overlap.
model: real-ram
complexity:
  vars: {n: the number of genes, m: the number of samples}
  time: {worst: Θ(n^2 m + n^3), best: Θ(n^2 m + n^3)}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2005
  people: [Bin Zhang, Steve Horvath]
  note: Zhang and Horvath described weighted gene coexpression networks with soft thresholding and topological overlap in Statistical Applications in Genetics and Molecular Biology in 2005. Langfelder and Horvath released the WGCNA R package in 2008.
prereqs: [hierarchical-clustering-problem, linkage-criterion, principal-component-analysis]
see_also: [hierarchical-clustering-problem, linkage-criterion, biclustering-problem, scale-free-network, principal-component-analysis, power-iteration, over-representation-analysis, gene-regulatory-network-inference]
sources:
  - paper: doi:10.2202/1544-6115.1128
    title: Bin Zhang and Steve Horvath, A general framework for weighted gene co-expression network analysis, Statistical Applications in Genetics and Molecular Biology 4(1) (2005), Article 17
    locator: the soft-threshold adjacency, the scale-free topology criterion for choosing the power, the generalized topological overlap for weighted networks, and modules from average-linkage clustering of the dissimilarity 1 - TOM
  - paper: doi:10.1186/1471-2105-9-559
    title: Peter Langfelder and Steve Horvath, WGCNA, an R package for weighted correlation network analysis, BMC Bioinformatics 9 (2008), article 559
    locator: the package, module eigengenes, module membership, and the relation of modules to sample traits
  - paper: doi:10.1126/science.1073374
    title: E. Ravasz, A. L. Somera, D. A. Mongru, Z. N. Oltvai and A.-L. Barabási, Hierarchical organization of modularity in metabolic networks, Science 297(5586) (2002), pages 1551 to 1555
    locator: the topological overlap of two nodes of an unweighted network, used to cluster metabolic networks into modules
  - paper: doi:10.1093/bioinformatics/btm563
    title: Peter Langfelder, Bin Zhang and Steve Horvath, Defining clusters from a hierarchical cluster tree, the Dynamic Tree Cut package for R, Bioinformatics 24(5) (2008), pages 719 to 720
    locator: the adaptive branch cutting used by WGCNA in place of a cut at one fixed height
---

Weighted gene coexpression network analysis builds a network in which every pair of genes is joined with a weight that grows with the correlation of their expression across samples, and then finds modules, groups of genes that are tightly connected in this network. The weight is a power of the absolute correlation, $a_{ij} = |r_{ij}|^\beta$, a soft threshold that keeps all edges but pushes weak correlations toward zero. The similarity used for clustering is the topological overlap, which counts how much two genes share their neighbours, not only how strongly they are joined. Modules come from [hierarchical clustering](/hierarchical-clustering-problem/) of $1 - \text{TOM}$ with average [linkage](/linkage-criterion/), and each module is summarized by its eigengene, the first [principal component](/principal-component-analysis/) of its genes. Zhang and Horvath (2005) introduced the method. It finds modules over all samples; a [biclustering](/biclustering-problem/) method instead looks for genes that are coexpressed in a subset of the samples only.

## In plain words

Genes that work together often go up and down together across samples. So you measure, for every pair of genes, how closely their patterns match. Instead of keeping only the strong pairs, you keep all pairs but make weak links much weaker than strong ones. Then you ask a second question for each pair: do these two genes have the same friends? Two genes count as close if they are linked to each other and to the same other genes. You group genes that are close in this sense into modules, and you describe each module by one pattern across the samples, the pattern that its genes share most. You can then ask which modules follow a disease or a treatment.

## The problem

**Input.** An expression matrix of $n$ genes in $m$ samples, a power $\beta \ge 1$, a cut height $H$ and a minimum module size.

**Output.** A module label for each gene, with 0 for genes in no module, and an eigengene for each module, a vector of length $m$.

**Aim.** Modules should be sets of genes with high topological overlap among themselves and lower overlap with other genes. There is no single objective function; the result is defined by the steps below.

## The algorithm

```pseudo id=main
WGCNA(X, β, H, minSize)                        ▷ X: n genes by m samples
L1  r_ij ← Pearson correlation of genes i and j across the samples
L2  a_ij ← |r_ij|^β  (or ((1 + r_ij) / 2)^β for a signed network);  a_ii ← 1
L3  k_i ← Σ_{u ≠ i} a_iu                                  ▷ connectivity
L4  TOM_ij ← (Σ_{u ≠ i, j} a_iu a_uj + a_ij) / (min(k_i, k_j) + 1 - a_ij)
L5  d_ij ← 1 - TOM_ij
L6  T ← average-linkage hierarchical clustering of d
L7  labels ← clusters of T cut at height H; clusters smaller than minSize get label 0
L8  for each module: eigengene ← first right singular vector of its standardized genes
L9  return labels, eigengenes
```

Line L1 computes all pairwise correlations. Line L2 is the soft threshold. In the unsigned network, strong negative correlations count as strong links; in the signed network, they count as weak ones. Line L3 sums the weights of each gene. Line L4 is the topological overlap of Ravasz et al. (2002), generalized by Zhang and Horvath to weights: the numerator adds the direct link to the weight of all paths of length 2, and the denominator is the largest value the numerator can take, so TOM lies in $[0, 1]$. Lines L5 and L6 cluster the genes, using the Lance-Williams update for average linkage. Line L7 cuts the tree at one fixed height. This is a static cut; the WGCNA package uses Dynamic Tree Cut, which cuts branches at different heights and can give different modules. Line L8 computes the eigengene by [power iteration](/power-iteration/) on the $m \times m$ matrix $Z^\top Z$, where $Z$ holds the genes of the module, each standardized, and fixes its sign so that it agrees with the mean of those genes.

**Choosing the power.** Zhang and Horvath chose $\beta$ by the scale-free topology criterion: for each candidate power, fit a line to $\log p(k)$ against $\log k$, where $p(k)$ is the fraction of genes with connectivity near $k$, and take the smallest $\beta$ for which the $R^2$ of the fit is high. The idea is that many biological networks look roughly like a [scale-free network](/scale-free-network/). This is a heuristic, and the code gives the fit so that it can be checked.

## Example

Take four genes whose adjacency matrix, after the soft threshold, is already given:

| | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| 1 | 1 | 0.9 | 0.8 | 0 |
| 2 | 0.9 | 1 | 0.7 | 0.1 |
| 3 | 0.8 | 0.7 | 1 | 0 |
| 4 | 0 | 0.1 | 0 | 1 |

The connectivities are $k = (1.7, 1.7, 1.5, 0.1)$. For genes 1 and 3, the paths of length 2 give $a_{12}a_{23} + a_{14}a_{43} = 0.63$, so $\text{TOM}_{13} = (0.63 + 0.8)/(1.5 + 1 - 0.8) = 0.8412$. All values:

| | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| 1 | 1 | 0.8111 | 0.8412 | 0.0818 |
| 2 | 0.8111 | 1 | 0.7889 | 0.1 |
| 3 | 0.8412 | 0.7889 | 1 | 0.0636 |
| 4 | 0.0818 | 0.1 | 0.0636 | 1 |

Genes 1 and 4 have no direct link, but $\text{TOM}_{14} = 0.0818$, because both are joined to gene 2. Average linkage on $1 - \text{TOM}$ first joins genes 1 and 3 at height 0.1588, then adds gene 2 at height $(0.1889 + 0.2111)/2 = 0.2$, and last adds gene 4 at height 0.9182. A cut at $H = 0.5$ gives the labels $(1, 1, 1, 2)$: one module of three genes and gene 4 on its own.

## Correctness

The [proof](proofs/correctness.md) shows that each step computes what it claims. The adjacency is symmetric with entries in $[0, 1]$. The topological overlap is symmetric and in $[0, 1]$, because the shared weight $\sum_u a_{iu}a_{uj}$ is at most $\min(k_i, k_j) - a_{ij}$. The Lance-Williams update gives the exact average distance between clusters, and the merge heights never decrease, because average linkage is reducible. So a cut at height $H$ keeps a prefix of the merges, and the labels are the clusters after that prefix. The power iteration converges to the first right singular vector of the standardized module matrix when the top eigenvalue is simple. The proof does not claim that the modules are biologically meaningful or that the network is scale free; those are questions about data.

## Complexity

On a [real RAM](/real-ram/), line L1 takes $\Theta(n^2m)$ time for the $n^2/2$ correlations. Line L4 takes $\Theta(n^3)$, since each of the $n^2/2$ pairs sums over $n$ genes; this is the cost of a product of two $n \times n$ matrices, and a fast matrix product lowers it. The code finds each merge of line L6 by a scan over all current pairs, so the clustering also takes $\Theta(n^3)$ in total; the nearest-neighbour chain algorithm does it in $O(n^2)$. The eigengenes take $O(nm^2)$ to form the matrices plus $O(m^2)$ per iteration. The extra space is $\Theta(n^2)$ for the matrices, which is why the package splits large data sets into blocks.

## Properties

- **Soft.** No correlation is thrown away by a hard threshold, so small changes in the data change the network a little, not by adding or removing edges.
- **Neighbourhood based.** Topological overlap is high for genes that share many neighbours, which makes modules more robust to noise in single correlations.
- **Bounded.** All adjacencies and overlaps lie in $[0, 1]$, and $\text{TOM}_{ij} = 0$ exactly when $a_{ij} = 0$ and no third gene is joined to both.
- **Not invariant to $\beta$.** The modules depend on the power and on the cut, and there is no correct choice in a mathematical sense.
- **Unsupervised.** The modules are found without the sample traits; traits are related to the eigengenes afterwards.

## Variants and improvements

- **Signed networks.** The adjacency $((1 + r)/2)^\beta$ separates genes that go up together from genes that go in opposite directions.
- **Dynamic Tree Cut.** Langfelder, Zhang and Horvath (2008) cut the branches of the tree adaptively, by their shape, instead of at one height.
- **Merging modules.** Modules whose eigengenes are highly correlated are merged after the cut.
- **Robust correlation.** The biweight midcorrelation or Spearman's [rank correlation](/spearman-rank-correlation/) can replace Pearson's correlation, so that a few outlying samples do not create links.
- **Consensus modules.** Modules found in several data sets at once, by taking the smallest overlap over the data sets.
- **Module membership.** The correlation of each gene with each eigengene shows how central the gene is to the module, and its hub genes.

## When to use it

Use it to reduce thousands of genes to tens of modules, when there are enough samples to estimate correlations, say 20 or more, and when the samples vary in a way that moves groups of genes together, such as different patients, tissues or conditions. Relate the eigengenes to clinical traits, and test the modules for function with [over-representation analysis](/over-representation-analysis/). Do not use it as a method to find regulators; correlation does not give direction, which is what [gene regulatory network inference](/gene-regulatory-network-inference/) tries to find.

## Pitfalls

- **Few samples.** Correlations from few samples are noisy, and the modules are unstable.
- **Batch effects.** A batch or a technical factor makes many genes correlated and gives large modules of no biological meaning. Remove or model it first.
- **Unsigned networks.** In an unsigned network, a gene and its repressor can fall into the same module, which mixes processes.
- **Overreading the scale-free fit.** The fit of a line to a few binned points on a log scale is a weak test, and real coexpression networks often do not fit well at any power.
- **The cut.** The modules change with the cut height and the minimum size. Report them, and check that the main modules survive other choices.
- **Memory.** The $n \times n$ matrices of 20,000 genes take several gigabytes. Filter genes, or work in blocks.

## Implementations

## History

Ravasz et al. (2002) defined the topological overlap for unweighted metabolic networks and used it to cluster them into modules. Zhang and Horvath (2005) replaced the hard threshold on correlations by a soft power, generalized the overlap to weighted networks, and proposed the scale-free criterion for the power. Langfelder and Horvath (2008) released the WGCNA R package, with module eigengenes, module membership and Dynamic Tree Cut, and it became a common tool for the analysis of microarray and RNA-seq data.

## References
