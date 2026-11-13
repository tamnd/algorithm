---
tag: 9NFKG0
kind: problem
slug: additive-tree-reconstruction
name: Additive tree reconstruction
aliases:
- tree fitting from distances
- additive tree fitting
area: biology/phylogenetics
level: core
summary: Given a distance matrix on n taxa, find the tree with positive edge lengths whose path lengths equal it, or the tree metric closest to it under a norm. Exact in O(n^2) time.
prereqs: [tree-metric, four-point-condition, phylogenetic-tree-reconstruction]
see_also: [four-point-method, neighbor-joining, least-squares-phylogeny, ultrametric-tree-reconstruction, minimum-evolution, metric-tree-embedding, split-decomposition, bionj]
sources:
  - paper: doi:10.1016/0022-5193(77)90351-4
    title: M. S. Waterman, T. F. Smith, M. Singh and W. A. Beyer, Additive evolutionary trees, Journal of Theoretical Biology 64(2), 1977, pages 199 to 213
    locator: the four-point condition for additive trees and the construction of the tree by adding one taxon at a time
  - paper: "Joseph C. Culberson and Piotr Rudnicki, A fast algorithm for constructing trees from distance matrices, Information Processing Letters 30(4), 1989, pages 215 to 220"
    title: Culberson and Rudnicki 1989
    locator: the O(n^2) algorithm for the exact problem
  - paper: doi:10.1016/0095-8956(74)90047-1
    title: Peter Buneman, A note on the metric properties of trees, Journal of Combinatorial Theory, Series B 17(1), 1974, pages 48 to 50
    locator: the four-point characterization that the exact problem tests
  - paper: doi:10.1137/S0097539796309764
    title: Richa Agarwala, Vineet Bafna, Martin Farach, Mike Paterson and Mikkel Thorup, On the approximability of numerical taxonomy (fitting distances by tree metrics), SIAM Journal on Computing 28(3), 1999
    locator: the 3-approximation for the L-infinity fit by a tree metric through ultrametrics, and the hardness of approximating it within 9/8
  - paper: doi:10.1007/BF02458863
    title: William H. E. Day, Computational complexity of inferring phylogenies from dissimilarity matrices, Bulletin of Mathematical Biology 49(4), 1987, pages 461 to 467
    locator: NP-hardness of the L1 and L2 fits by a tree metric
  - book: isbn:9780198509424
    title: Charles Semple and Mike Steel, Phylogenetics, 2003
    locator: Chapter 7, tree metrics, the tree-metric theorem and the reconstruction of the tree
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, 1997
    locator: Chapter 17, additive-distance trees and their construction
---

Additive tree reconstruction is the problem of finding, from a matrix of distances between $n$ taxa, a tree with edge lengths whose path lengths between the taxa reproduce the matrix. In the exact version the matrix is a [tree metric](/tree-metric/), the tree is unique by the [four-point condition](/four-point-condition/), and the [four-point method](/four-point-method/) finds it in $O(n^2)$ time. In the approximate version the matrix comes from data and the goal is the closest tree metric under a norm; this is NP-hard for the usual norms. It is the distance-based part of [phylogenetic tree reconstruction](/phylogenetic-tree-reconstruction/).

## In plain words

You have measured how far apart each pair of species is. You want a tree with a length on each branch such that, for every pair, walking along the branches from one species to the other covers exactly the measured distance. If the measurements are perfect, such a tree exists only when every group of four species passes a simple test, and then there is only one such tree, which is fast to build. Real measurements have errors, so no tree fits exactly. Then you look for the tree whose walking distances are closest to the measurements, and finding the very best one is hard. Fast methods give a good tree instead.

## Definition

**Exact version.** The input is a set $X$ of $n$ taxa and a symmetric matrix $D$ with zero diagonal and $D_{xy} > 0$ for $x \ne y$. The output is a tree $T$ with $X \subseteq V(T)$, positive edge lengths and every vertex outside $X$ of degree at least 3, such that $D_{xy}$ is the path length between $x$ and $y$, or the answer that no such tree exists. In the usual phylogenetic setting the taxa are the leaves of $T$.

**Approximate version.** For a norm $\lVert \cdot \rVert$ on symmetric matrices, the output is a tree $T$ with leaf set $X$ and edge lengths $b$ that minimize $\lVert D - d_{T,b} \rVert$, where $d_{T,b}$ is the tree metric of $(T, b)$. The common norms are
$$\lVert E \rVert_\infty = \max_{x<y} |E_{xy}|, \qquad \lVert E \rVert_1 = \sum_{x<y} |E_{xy}|, \qquad \lVert E \rVert_2^2 = \sum_{x<y} w_{xy} E_{xy}^2.$$
The $L_2$ case with weights is the [least squares phylogeny](/least-squares-phylogeny/) problem. Lengths are usually required to be at least 0.

## Variants

- **Rooted with a clock.** If the tree must be rooted with all leaves at the same distance from the root, the metric is an [ultrametric](/ultrametric/) and the problem is [ultrametric tree reconstruction](/ultrametric-tree-reconstruction/).
- **Leaves only.** Most phylogenetic programs require all taxa at leaves and the tree binary; a taxon at an internal vertex then appears as a leaf on an edge of length 0.
- **Criteria other than fit.** [Minimum evolution](/minimum-evolution/) chooses the topology with the smallest total length of the fitted tree instead of the best fit.
- **Splits instead of a tree.** [Split decomposition](/split-decomposition/) and [Neighbor-Net](/neighbor-net/) represent a metric by a weighted system of splits, which may not be compatible, and draw a network.
- **Query model.** The entries are not given but can be asked for one at a time, and the cost is the number of questions.

## Examples

**An exact instance.** The matrix

| | A | B | C | D | E |
|---|---|---|---|---|---|
| A | 0 | 9 | 8 | 11 | 8 |
| B | 9 | 0 | 13 | 16 | 13 |
| C | 8 | 13 | 0 | 9 | 10 |
| D | 11 | 16 | 9 | 0 | 13 |
| E | 8 | 13 | 10 | 13 | 0 |

passes the four-point test on all five quartets, and the unique tree is `((A:2,B:7):1,E:5,(C:3,D:6):2);`. The page of the [four-point method](/four-point-method/) builds it step by step.

**Through an ultrametric.** Fix the taxon $r = A$ and let $M = \max_x D_{Ax} = 11$. The Farris transform $u_{xy} = 2M - D_{Ax} - D_{Ay} + D_{xy}$ on B to E gives $u_{BC} = u_{BD} = u_{BE} = 18$, $u_{CE} = u_{DE} = 16$ and $u_{CD} = 12$. This is an ultrametric: its tree joins C and D at height 6, adds E at height 8 and B at height 9. Attach A to the top node by an edge of length $M - 9 = 2$, and shorten the edge of each leaf $x$ by $M - D_{Ax}$: B gets $9 - 2 = 7$, E gets $8 - 3 = 5$, C gets $6 - 3 = 3$ and D gets $6 - 0 = 6$. The internal edges keep the height differences 1 and 2. The result is the same tree.

**A matrix with no exact tree.** The matrix with $D_{AB} = 2$, $D_{AC} = D_{AD} = D_{BC} = 6$, $D_{BD} = 9$ and $D_{CD} = 4$ has the pair sums 6, 15 and 12, so no tree fits exactly. On the topology AB|CD the ordinary least squares lengths are $1/4$, $7/4$, $15/4$, $5/4$ and $11/4$ for A, B, the internal edge, C and D, with sum of squared errors $9/4$; the page of the [Fitch-Margoliash method](/fitch-margoliash/) shows the weighted fit of the same data.

## Known algorithms

| algorithm | setting | time | result |
|---|---|---|---|
| [Four-point method](/four-point-method/) | exact, binary tree | $O(n^2)$ | the tree, by one quartet test per step of a walk |
| Waterman, Smith, Singh and Beyer (1977) | exact | polynomial | adds taxa one at a time using the four-point condition |
| Culberson and Rudnicki (1989) | exact | $O(n^2)$ | the tree, also for vertices of high degree |
| [Neighbor-joining](/neighbor-joining/) | exact and noisy | $O(n^3)$ | exact on tree metrics, correct within half the shortest edge length (Atteson 1999) |
| [BIONJ](/bionj/) | noisy | $O(n^3)$ | NJ with variance-based reduction |
| [Fitch-Margoliash](/fitch-margoliash/) | $L_2$, weights $1/D^2$ | heuristic | local optimum of weighted least squares |
| Agarwala et al. (1999) | $L_\infty$ | $O(n^2)$ | within 3 times the optimal error, through the Farris transform and an optimal ultrametric fit |

To test whether a matrix is a tree metric, build a tree with the four-point method and compare its leaf metric with $D$; both steps take $O(n^2)$ time.

## Bounds

- **Exact version.** $O(n^2)$ time, which is linear in the $n(n-1)/2$ entries of the input.
- **$L_1$ and $L_2$.** Finding the best tree metric is NP-hard (Day 1987); with a fixed topology, the $L_2$ fit is a linear [least squares problem](/least-squares-problem/) and the $L_1$ and $L_\infty$ fits are [linear programs](/linear-programming-problem/).
- **$L_\infty$.** NP-hard to approximate within a factor $9/8$, and approximable within 3 (Agarwala et al. 1999).
- **Number of topologies.** An exhaustive search over unrooted binary topologies checks $(2n-5)!!$ trees, which is 2,027,025 for $n = 10$.

## Reductions

- **To ultrametrics (the Farris transform).** For a fixed taxon $r$ and $M \ge \max_x D_{rx}$, $D$ is a tree metric if and only if $u_{xy} = 2M - D_{rx} - D_{ry} + D_{xy}$ is an ultrametric on $X \setminus \{r\}$. This is the [four-point condition](/four-point-condition/) for quadruples that contain $r$, written with the Gromov product $(x \mid y)_r = \frac{1}{2}(D_{rx} + D_{ry} - D_{xy})$, since $u_{xy} = 2(M - (x \mid y)_r)$; the quadruples without $r$ follow from these. The example above runs the reduction and its inverse. A fit to $u$ within error $\varepsilon$ in $L_\infty$ gives a tree metric within $O(\varepsilon)$ of $D$, which is how Agarwala et al. obtain their factor 3.
- **From the fixed-topology fit to linear algebra.** With the topology known, the lengths solve the [normal equations](/normal-equations/) of a linear model with one column per edge.
- **To splits.** A tree metric is a nonnegative combination of the split metrics of the [splits of its tree](/splits-of-a-tree/), so reconstruction is the same as finding these splits and their weights.

## Applications

- **Distance-based phylogenetics.** Distances between sequences, corrected with a [substitution model](/substitution-model/) such as the [Jukes-Cantor model](/jukes-cantor-model/), are approximately additive on the true tree, and methods for this problem estimate the tree from them.
- **Guide trees.** [Progressive alignment](/progressive-alignment/) builds a tree from pairwise distances and aligns sequences in its order.
- **Metric embedding.** Approximating a general metric by a tree metric is a tool for approximation algorithms; see [metric tree embedding](/metric-tree-embedding/).
- **Other fields.** Tree fits of distances are used in linguistics, in the study of manuscripts, and in network measurement to infer a routing tree from end-to-end delays.

## References
