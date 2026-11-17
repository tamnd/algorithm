---
tag: MJ06W1
kind: algorithm
slug: mst-pseudotime
name: Minimum spanning tree pseudotime
aliases:
- Monocle ordering
- TSCAN
area: biology/transcriptomics
level: advanced
summary: Build a minimum spanning tree over cells or cluster centers in reduced space and order cells by their position along its longest path.
solves: [trajectory-inference]
model: real-ram
complexity:
  vars: {n: the number of cells, d: the number of dimensions, m: the number of clusters}
  time: {worst: O(n^2 d)}
  space: {extra: O(n)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2014
  people: [Cole Trapnell, Davide Cacchiarelli, John L. Rinn]
  note: "Trapnell and co-authors (2014) ordered single cells along a minimum spanning tree in Monocle. Ji and Ji (2016) built the tree on cluster centers instead, in TSCAN."
prereqs: [minimum-spanning-tree, prim, tree-diameter, depth-first-search, euclidean-distance, single-cell-rna-sequencing]
see_also: [trajectory-inference, diffusion-pseudotime, rna-velocity, kruskal, principal-component-analysis, independent-component-analysis, gaussian-mixture-model, shared-nearest-neighbor-clustering]
sources:
  - paper: doi:10.1038/nbt.2859
    title: Cole Trapnell et al., The dynamics and regulators of cell fate decisions are revealed by pseudotemporal ordering of single cells, Nature Biotechnology 32(4), 381 to 386 (2014)
    locator: the Monocle method, with independent component analysis, the minimum spanning tree on the cells and the longest path through it
  - paper: doi:10.1093/nar/gkw430
    title: "Zhicheng Ji and Hongkai Ji, TSCAN: Pseudo-time reconstruction and evaluation in single-cell RNA-seq analysis, Nucleic Acids Research 44(13), e117 (2016)"
    locator: the method section, with the clusters, the minimum spanning tree on the cluster centers and the projection of the cells onto its edges
  - paper: doi:10.1038/s41587-019-0071-9
    title: Wouter Saelens, Robrecht Cannoodt, Helena Todorov and Yvan Saeys, A comparison of single-cell trajectory inference methods, Nature Biotechnology 37(5), 547 to 554 (2019)
    locator: the benchmark of trajectory inference methods, which includes methods built on minimum spanning trees
---

Minimum spanning tree pseudotime orders single cells along a process such as differentiation. It joins the cells, or the centers of cell clusters, with a [minimum spanning tree](/minimum-spanning-tree/) in a space of few dimensions. It takes the longest path of the tree as the main line of the process, and it gives each cell a pseudotime: its distance along the tree from a root cell at the start. Trapnell and co-authors (2014) used a tree on the cells in Monocle, and Ji and Ji (2016) used a tree on the cluster centers in TSCAN. It is one answer to the [trajectory inference](/trajectory-inference/) problem. The tree is exact, but the claim that the pseudotime follows the real time of the process is a heuristic.

## In plain words

Cells that change slowly from one state to another leave a trail of points, one for each cell. Connect every cell to the cells nearest to it so that all cells are joined with the least total length of line and no loops. The result is a tree that runs along the trail. Its longest path is the main line. Pick the cell where the process starts. The pseudotime of a cell is how far you walk along the tree from that start cell to reach it. Where the tree splits into arms, the process splits into branches. With clusters, do the same with one point for each cluster, and place each cell on the line between its cluster and the next one.

## The problem

**Input.** Cells $x_1, \dots, x_n$ in $\mathbb{R}^d$, usually the first principal components of the log expression values, and a root cell. The cluster version also takes a cluster label for each cell and a root cluster.

**Output.** A tree on the cells, its longest path (the backbone), a pseudotime $\tau_i \ge 0$ for each cell, and the cells where the tree branches.

## The algorithm

```pseudo id=main
MST-PSEUDOTIME(x_1..x_n, r)
L1  grow a tree from cell 1: for each cell v outside it, w ← ‖x_u - x_v‖ to the cell u just added
L2  if w < best(v): best(v) ← w; parent(v) ← u; then add the outside cell with the smallest best(v)
L3  a ← the cell farthest from cell 1 along the tree; backbone ← the tree path from a to the cell farthest from a
L4  if no root r is given: r ← the first end of the backbone
L5  τ_i ← the length of the tree path from r to i, for every cell i
L6  branch points ← the cells of degree 3 or more in the tree
CLUSTER-PSEUDOTIME(x_1..x_n, labels, root cluster)
L7  c_j ← the mean of the cells of cluster j; build the tree on the centers c_j as in L1 and L2; take the tree path from the root cluster to the farthest cluster
L8  project each cell of a cluster on the path onto the nearest path edge at its cluster, clipped to the edge, and set τ ← the offset of the edge + the position on it
```

Lines L1 and L2 are [Prim's algorithm](/prim/) on the complete graph with Euclidean weights. It needs no distance matrix, so it takes $O(n)$ extra space. Line L3 finds a longest path of the tree with two farthest-vertex searches, the usual way to find a [tree diameter](/tree-diameter/). Line L5 is one [depth-first search](/depth-first-search/) from the root. Line L4 is only a default: the data do not tell which end of the process is the start, so a user should give the root from known biology, for example a stem cell marker. Lines L7 and L8 are the TSCAN version. Cells of clusters that are not on the main path get no pseudotime from line L8.

## Example

Eight cells in two dimensions: three on a stem and two arms of the shape Y.

| cell | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| $x$ | $(0, 0)$ | $(1, 0)$ | $(2, 0)$ | $(3, 1)$ | $(4, 2)$ | $(3, -1)$ | $(4, -2)$ | $(5, -3)$ |

The tree has the edges $0$-$1$ and $1$-$2$ of length 1, and $2$-$3$, $3$-$4$, $2$-$5$, $5$-$6$, $6$-$7$ of length $\sqrt 2$. Cell 2 has degree 3, so it is the branch point. The longest path is $7, 6, 5, 2, 3, 4$, of length $5\sqrt 2 \approx 7.07$. It runs from the tip of one arm to the tip of the other, and it does not contain the stem. So the default root is cell 7, a tip, and not cell 0, where the process starts. With the root $r = 0$ the pseudotimes are:

| cell | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| $\tau$ | 0 | 1 | 2 | 3.414 | 4.828 | 3.414 | 4.828 | 6.243 |

The two arms get the same pseudotimes at the same depth, as they should.

## Correctness

The [proof](proofs/correctness.md) shows four things. Lines L1 and L2 give a minimum spanning tree, by the cut property. The two searches of line L3 give a longest path of a tree with nonnegative weights, by the four-point property of tree distances. If the distance between two cells grows strictly with the gap between their true times, the tree is the path of consecutive cells, so the pseudotime from the first cell gives the true order (a theorem). In the cluster version every cell gets a pseudotime between 0 and the length of the path of centers. For noisy cells the order is a measurement: in the tests, 200 cells near a line in five dimensions with noise of standard deviation 0.05 per coordinate give a rank correlation of 0.993 with the true time, and the cluster version on five clusters along a line gives 0.998.

## Complexity

Prim's algorithm on the complete graph takes $O(n^2d)$ time and $O(n)$ extra space. The searches of lines L3 and L5 take $O(n)$ time. The cluster version with $m$ clusters takes $O(nd)$ time for the centers and projections and $O(m^2d)$ for the tree, which is much less than $O(n^2d)$ when $m$ is small. For many cells, the cluster version is the usual way to keep the tree small.

## Properties

- **Deterministic.** Ties are broken by the smaller index.
- **Exact tree.** The tree is a minimum spanning tree of the cells; only its meaning as a trajectory is a heuristic.
- **Shows branches.** The cells of degree 3 or more mark where the tree splits.
- **Needs a root.** The pseudotime depends on the root, which the data do not fix.
- **Sensitive to noise.** One cell more or less can change the tree and its longest path.

## Variants and improvements

- **Monocle 1.** Trapnell and co-authors (2014) reduce the data with [independent component analysis](/independent-component-analysis/), build the tree on the cells, and order the cells along the longest path with a PQ tree to place the branches.
- **TSCAN.** Ji and Ji (2016) cluster the cells in a space of [principal components](/principal-component-analysis/) with a [Gaussian mixture model](/gaussian-mixture-model/), build the tree on the cluster centers, and project the cells onto its edges. A tree on a few centers is much less sensitive to noise than a tree on all cells.
- **Slingshot** builds the tree on the clusters and then fits a smooth principal curve along each lineage.
- **Graph methods.** [Diffusion pseudotime](/diffusion-pseudotime/) uses random walks on a neighbor graph instead of a tree, and [RNA velocity](/rna-velocity/) gives a direction to the process from unspliced and spliced counts.

## When to use it

Use it for a first look at a process with a simple shape, a line or a tree with few branches, when you can name the start cell or the start cluster. Use the cluster version when the data are noisy or large. The benchmark of Saelens and co-authors (2019) found that no method was best for all shapes of trajectory, so compare it with a graph method such as diffusion pseudotime.

## Pitfalls

- **Spurious branches.** In the tests, a Y of 180 cells with noise of standard deviation 0.02 gives 39 cells of degree 3 or more, although only one branch point lies near the junction. Count only branches with long arms, or use the cluster version.
- **The wrong root.** The default end of the longest path can be a tip, as in the example. Give the root from biology.
- **Cycles and gaps.** A tree cannot show a cycle, such as the cell cycle, and it joins separate groups of cells with long edges that are not a real process.
- **The space matters.** The tree depends on the reduced space and the number of components; a different space can give a different order.
- **Pseudotime is not time.** It is a distance in expression space, not hours or days.

## Implementations

## History

Trapnell and co-authors (2014) introduced pseudotemporal ordering of single cells with Monocle, which built a minimum spanning tree on the cells. The tree on cells was sensitive to noise, so Ji and Ji (2016) built it on cluster centers in TSCAN. Later methods such as Slingshot kept the cluster tree and fitted curves along it. The benchmark of Saelens and co-authors (2019) compared many trajectory inference methods, including several built on spanning trees.

## References
