---
tag: 5FFE0B
kind: algorithm
slug: markov-clustering
name: Markov clustering
aliases:
- MCL
- Markov cluster algorithm
area: graphs/network-analysis
level: advanced
summary: Alternates matrix expansion and inflation to converge to clusters.
solves: [community-detection]
model: word-ram
complexity:
  vars: {n: the number of vertices, T: the number of iterations}
  time: {worst: O(T n^3)}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, recursive: false}
history:
  year: 2000
  people: [Stijn van Dongen]
  note: Introduced in the PhD thesis Graph clustering by flow simulation, University of Utrecht, 2000, and analysed in a 2008 paper in the SIAM Journal on Matrix Analysis and Applications.
prereqs: [markov-chain, adjacency-matrix, community-detection]
see_also: [louvain-method, leiden-algorithm, infomap, label-propagation-algorithm, spectral-clustering, sparse-matrix-multiplication, modularity]
sources:
  - paper: doi:10.1137/040608635
    title: Stijn van Dongen, Graph clustering via a discrete uncoupling process, SIAM Journal on Matrix Analysis and Applications 30(1), 121 to 141 (2008)
    locator: the definition of the MCL process (alternating expansion and inflation), the structure of its doubly idempotent limits and the interpretation of a limit as a clustering, and the stability results near the limits
  - paper: doi:10.1093/nar/30.7.1575
    title: Anton J. Enright, Stijn van Dongen and Christos A. Ouzounis, An efficient algorithm for large-scale detection of protein families, Nucleic Acids Research 30(7), 1575 to 1584 (2002)
    locator: the TRIBE-MCL method, which runs MCL on a graph of sequence similarities, and the choice of the inflation value
  - paper: doi:10.1186/1471-2105-7-488
    title: Sylvain Brohée and Jacques van Helden, Evaluation of clustering algorithms for protein-protein interaction networks, BMC Bioinformatics 7, 488 (2006)
    locator: the comparison of MCL with three other methods on networks with known complexes and with added and removed edges, where MCL was the most robust
  - paper: doi:10.1145/1557019.1557101
    title: Venu Satuluri and Srinivasan Parthasarathy, Scalable graph clustering using stochastic flows, applications to community discovery, Proceedings of KDD 2009, 737 to 746
    locator: the fragmentation of MCL on graphs with skewed degrees, the regularized MCL that fixes it, and the multilevel version
---

Markov clustering, or MCL, finds the [clusters](/community-detection/) of a graph by simulating random walks on it and sharpening them until the walks cannot leave the dense regions. It keeps a column-stochastic matrix $M$ of transition probabilities. *Expansion* replaces $M$ by $M^2$, which spreads each walk one step further. *Inflation* raises every entry to a power $r > 1$ and rescales each column, which boosts the likely moves and starves the unlikely ones. Alternating the two drives $M$ to a limit in which each column points to a few *attractor* vertices, and the vertices that point to the same attractors form a cluster. Stijn van Dongen introduced it in 2000. The parameter $r$ sets the granularity, the number of clusters is not given in advance, and with dense matrices one iteration costs $O(n^3)$ time.

## In plain words

Drop many walkers on a graph and let each one wander along the edges. A walker that starts inside a tightly knit group tends to stay there for a while, because most of the edges around it lead back into the group. Few edges cross from one group to another, so few walkers cross.

MCL makes this effect stronger, round after round. After each round of wandering, it looks at where the walkers from each start vertex ended up, makes the popular places more popular and the rare places rarer, and lets them wander again. Soon all walkers from a group end up at one or two vertices of the group, and none of them leave. The groups that share these end points are the clusters.

## The problem

The input is an undirected [weighted graph](/weighted-graph/) $G = (V, E)$ with $n$ vertices, $V = \{0, \ldots, n-1\}$, and positive weights $A_{ij} = A_{ji}$; an unweighted graph has all weights 1. The output is a partition of $V$ into clusters, so that there are many edges, or much weight, inside the clusters and few between them. There is no single objective that MCL optimises; the clusters are defined by the process. Two parameters control it: the expansion power $e$, an integer at least 2, usually $e = 2$, and the inflation power $r > 1$, usually between 1.4 and 6. Larger $r$ gives smaller clusters.

Write $\Gamma_r$ for inflation: for a nonnegative matrix $X$ whose columns are not zero,

$$(\Gamma_r X)_{ij} = \frac{X_{ij}^r}{\sum_k X_{kj}^r}.$$

A matrix is *column stochastic* if its entries are nonnegative and each column sums to 1. Column $j$ of such a matrix is a probability distribution, the place of a walker that started at $j$.

## The algorithm

```pseudo id=main
MCL(G, e, r, θ, ε)
L1  A ← the weighted adjacency matrix of G, plus a self-loop of weight 1 at each vertex
L2  M ← A with each column divided by its sum                       ▷ column stochastic
L3  repeat
L4      M_old ← M
L5      M ← M^e                                                     ▷ expansion
L6      M_ij ← M_ij^r for all i, j                                  ▷ inflation
L7      divide each column of M by its sum; set the entries below θ to 0 and divide each column by its sum again
L8  until every entry of M differs from that of M_old by at most ε, or an iteration limit is reached
L9  H ← the undirected graph on V with an edge {i, j} for each M_ij > 0
L10 return the connected components of H
```

Lines L6 and L7 together compute $\Gamma_r(M)$ and prune it. The self-loops of line L1 let a walker stay where it is. Without them, a walk on a bipartite graph alternates between the two sides, $M^2$ only connects vertices of the same side, and the clusters follow the parity: the 4-cycle $0, 1, 2, 3$ gives $\{0, 2\}$ and $\{1, 3\}$, and a single edge gives two singletons. The prune threshold $\theta$ must be smaller than $1/n$, so that the largest entry of each column survives; it keeps $M$ sparse and makes the entries that tend to 0 become exactly 0.

**The read-out.** In a limit, the vertices $a$ with $M_{aa} > 0$ are the *attractors*. Column $j$ is spread evenly over the attractors that $j$ flows to, and its other entries are 0. Line L9 joins $j$ to these attractors, and line L10 returns the connected components. When a vertex flows to attractors of two different groups, which happens on graphs with symmetries, the read-out merges the two groups. This page fixes this rule because it always returns a partition; van Dongen's tools can also keep the overlap.

**Ties, order and disconnected graphs.** No step depends on an order of the vertices, so there are no ties to break. All matrices are block diagonal over the [connected components](/connected-components/) of $G$, so every cluster lies inside one component, and an isolated vertex is a cluster of its own. The implementation stops after 1000 iterations if the change is still above $\varepsilon = 10^{-9}$, and uses $\theta = 10^{-6}$.

## Example

Take the two triangles $\{0,1,2\}$ and $\{3,4,5\}$ joined by the edge $\{2,3\}$, all weights 1, with $e = r = 2$. After line L2, the column of vertex 2 is $\frac14$ at each of 0, 1, 2 and 3, and the column of vertex 0 is $\frac13$ at each of 0, 1 and 2. The column of vertex 2 then changes as follows.

| step | at 0 | at 1 | at 2 | at 3 | at 4 | at 5 |
|---|---|---|---|---|---|---|
| line L2 | 1/4 | 1/4 | 1/4 | 1/4 | 0 | 0 |
| expansion, line L5 | 11/48 | 11/48 | 7/24 | 1/8 | 1/16 | 1/16 |
| inflation, lines L6 and L7 | 121/492 | 121/492 | 49/123 | 3/41 | 3/164 | 3/164 |

Expansion lets the walker from vertex 2 reach vertices 4 and 5, but only with probability $\frac1{16}$ each. Inflation squares the entries, so these small values fall to $\frac{3}{164} \approx 0.018$, while the entry at 2 grows from $0.29$ to $0.40$. After 9 iterations the change is below $10^{-9}$, and the matrix is

$$M = \begin{pmatrix} 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 \\ 1 & 1 & 1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 1 & 1 & 1 \\ 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 \end{pmatrix}.$$

The attractors are 2 and 3. Vertices 0, 1 and 2 flow to 2, and 3, 4 and 5 flow to 3, so the clusters are $\{0, 1, 2\}$ and $\{3, 4, 5\}$. With $r = 1.4$ the inflation is too weak, the flow crosses the edge $\{2, 3\}$, and MCL returns one cluster after 15 iterations; with $r = 4$ it returns the two triangles after 5.

## Correctness

MCL has no objective that it provably optimises, and no proof is known that the iteration always converges, so its correctness is a set of facts about the process. Each matrix $M$ is column stochastic: a product of column-stochastic matrices is column stochastic, inflation rescales each column to sum 1, and since the largest entry of a column is at least $1/n > \theta$, pruning never empties a column. Each $M$ is zero outside the blocks of the connected components of $G$, because $A$ is, and products and entrywise powers keep this pattern; so each cluster lies inside one component. Line L10 returns a partition of $V$ whatever matrix the loop ends with. At a fixed point of inflation, $\Gamma_r M = M$ with $r > 1$, every column is uniform on its nonzero entries, which is the shape of the limit in the example. These facts are proved in [the proof page](proofs/correctness.md). Van Dongen proved more about the limits that are both idempotent and fixed by inflation, the *doubly idempotent* matrices: their columns are spread over attractor systems, and the clustering they define is stable under small perturbations of the matrix.

## Complexity

- **One iteration.** With dense matrices and $e = 2$, the product of line L5 costs $\Theta(n^3)$, and inflation and pruning cost $\Theta(n^2)$. With $e > 2$, it is $e - 1$ products.
- **Number of iterations.** $T$ is not bounded by any known function of $n$. In practice the change shrinks fast once the attractors appear, because inflation squares the small entries, and $T$ is a few tens. In the random tests of the implementation, graphs with up to 12 vertices took at most 15 iterations.
- **Sparse matrices.** The real program keeps at most $k$ entries per column after pruning, for a fixed $k$ such as 1000. A column of $M^2$ is then a combination of at most $k$ columns with $k$ entries each, so an iteration costs $O(n k^2)$ time and the method runs on graphs with millions of vertices. The first iterations, before pruning bites, are the expensive ones.
- **Space.** $\Theta(n^2)$ words for a dense $M$; $O(nk)$ with $k$ entries per column.

## Properties

- **No number of clusters in advance.** The inflation power $r$ controls the granularity: larger $r$ gives more and smaller clusters.
- **Deterministic.** There is no randomness and no vertex order, unlike [label propagation](/label-propagation-algorithm/) or the [Louvain method](/louvain-method/).
- **Clusters stay inside components.** Flow cannot cross between components, so the clusters refine the connected components.
- **Robust to noise.** In the comparison of Brohée and van Helden on protein interaction networks with added and removed edges, MCL recovered the known complexes better than the other methods tested.
- **Fragmentation on skewed degrees.** Satuluri and Parthasarathy show that on graphs with a few vertices of very high degree, MCL tends to return many tiny clusters and a few huge ones.
- **Overlap.** In a limit, a vertex can flow evenly to attractors of two groups, for example the middle vertex of a path of 7 vertices. The read-out of line L10 then merges the two groups.

## Variants and improvements

- **Regularized MCL.** Satuluri and Parthasarathy replace the expansion $M^2$ by $M M_G$, the product with the transition matrix of the original graph, which keeps the clusters balanced, and add a multilevel scheme that coarsens the graph first.
- **TRIBE-MCL.** Enright, van Dongen and Ouzounis run MCL on a graph whose edge weights come from sequence similarity scores, to group proteins into families. It is a standard tool in bioinformatics.
- **Different loop weights.** The self-loop weight of line L1 can be the largest weight of the column instead of 1, which makes the result less sensitive to the scale of the weights.
- **Overlapping read-out.** Keep each vertex in all the clusters of the attractors it flows to, instead of merging them.

## When to use it

Use MCL for clusters of a sparse graph of similarities, for example protein families or groups of co-expressed genes, when the number of clusters is unknown and a deterministic answer is wanted. It is the standard choice in protein network analysis. For social networks with hub vertices, prefer the [Louvain method](/louvain-method/), the [Leiden algorithm](/leiden-algorithm/) or [Infomap](/infomap/), which handle skewed degrees better and scale further. For a fixed number of clusters, use [spectral clustering](/spectral-clustering/).

## Pitfalls

- **Forgetting the self-loops.** Without line L1, the walks of a bipartite component alternate sides and MCL splits it by parity, so that no cluster contains an edge. The 4-cycle splits into its two diagonals.
- **Pruning too hard.** A threshold $\theta \ge 1/n$ can remove every entry of a column, and the division by its sum fails. Pruning with a top-$k$ rule also changes the result, so report the pruning used.
- **Dense matrices.** $M^2$ fills in fast on a graph of small diameter, so a dense or poorly pruned run takes $\Theta(n^2)$ memory and $\Theta(n^3)$ time per iteration.
- **Reading inflation as a resolution with a fixed meaning.** The same $r$ gives very different cluster sizes on graphs of different density; scan a few values and compare.
- **Overlap in the read-out.** Decide what to do with vertices that flow to two attractor systems, and say which rule was used.

## Implementations

## History

Stijn van Dongen developed MCL for his PhD thesis, Graph clustering by flow simulation, at the University of Utrecht and the CWI in Amsterdam in 2000, and released the mcl program. In 2002 Enright, van Dongen and Ouzounis used it in TRIBE-MCL to cluster protein sequences into families, which made it widely used in bioinformatics. Brohée and van Helden found it the most robust of four methods on protein interaction networks in 2006. Van Dongen published the analysis of the limits and their stability in the SIAM Journal on Matrix Analysis and Applications in 2008, and Satuluri and Parthasarathy proposed regularized and multilevel MCL in 2009.

## References
