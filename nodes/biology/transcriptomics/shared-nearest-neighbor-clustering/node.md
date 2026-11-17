---
tag: 6JJNPV
kind: algorithm
slug: shared-nearest-neighbor-clustering
name: Shared nearest neighbor graph clustering
aliases:
- SNN clustering
- PhenoGraph
area: biology/transcriptomics
level: core
summary: Build a k-nearest-neighbor graph of cells in PCA space, weight edges by shared neighbors, and cut it into clusters by modularity.
model: real-ram
complexity:
  vars: {n: the number of cells, d: the number of principal components, k: the number of neighbors, E: the number of edges, P: the number of moving passes}
  time: {worst: O(n^2 d + n k^2 + P E log k)}
  space: {extra: O(n k)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2015
  people: [Jacob H. Levine, Dana Pe'er, Garry P. Nolan]
  note: PhenoGraph (Levine et al. 2015) put Jaccard weights on a k-nearest-neighbor graph and cut it with the Louvain method. Shared neighbor similarity goes back to Jarvis and Patrick (1973), and SNN-Cliq (Xu and Su 2015) used it on single-cell RNA-seq.
prereqs: [k-nearest-neighbor-graph, jaccard-similarity, modularity, louvain-method, principal-component-analysis]
see_also: [leiden-algorithm, community-detection, nearest-neighbor-graph, k-means, umap, t-sne, highly-variable-gene-selection, doublet-detection]
sources:
  - paper: doi:10.1016/j.cell.2015.05.047
    title: Jacob H. Levine et al., Data-driven phenotypic dissection of AML reveals progenitor-like cells that correlate with prognosis, Cell 162(1), 184 to 197 (2015)
    locator: the description of PhenoGraph, with the k-nearest-neighbor graph, the Jaccard weights and the Louvain partition
  - paper: doi:10.1088/1742-5468/2008/10/P10008
    title: Vincent D. Blondel, Jean-Loup Guillaume, Renaud Lambiotte and Etienne Lefebvre, Fast unfolding of communities in large networks, Journal of Statistical Mechanics, Theory and Experiment 2008, P10008 (2008)
    locator: Section 2, the local moving phase with the modularity gain and the aggregation phase
  - paper: doi:10.1109/T-C.1973.223640
    title: R. A. Jarvis and E. A. Patrick, Clustering using a similarity measure based on shared near neighbors, IEEE Transactions on Computers C-22(11), 1025 to 1034 (1973)
    locator: the shared near neighbor similarity
  - paper: doi:10.1093/bioinformatics/btv088
    title: Chen Xu and Zhengchang Su, Identification of cell types from single-cell transcriptomes using a novel clustering method, Bioinformatics 31(12), 1974 to 1980 (2015)
    locator: the SNN graph of cells and the search for quasi-cliques in it
  - paper: doi:10.1038/s41598-019-41695-z
    title: V. A. Traag, L. Waltman and N. J. van Eck, From Louvain to Leiden, guaranteeing well-connected communities, Scientific Reports 9, 5233 (2019)
    locator: the section on the Louvain algorithm, which shows that it can return badly connected communities
  - paper: doi:10.1109/TKDE.2007.190689
    title: Ulrik Brandes, Daniel Delling, Marco Gaertler, Robert Görke, Martin Hoefer, Zoran Nikoloski and Dorothea Wagner, On modularity clustering, IEEE Transactions on Knowledge and Data Engineering 20(2), 172 to 188 (2008)
    locator: the NP-completeness of maximizing modularity
---

Shared nearest neighbor (SNN) graph clustering is the standard way to find groups of cells, such as cell types, in single-cell RNA-seq data. It takes the cells as points in a space of a few tens of [principal components](/principal-component-analysis/), joins each cell to its $k$ nearest neighbors, gives each edge a weight equal to the share of neighbors that its two ends have in common, and splits the graph into communities of high [modularity](/modularity/) with the [Louvain method](/louvain-method/). PhenoGraph (Levine et al. 2015) put these steps together, and Seurat and Scanpy use the same plan. The weights make edges inside a dense group strong and edges between groups weak, so the cut follows the gaps between cell types.

## In plain words

Each cell lists the cells most like it. Two cells are strongly linked when their lists share many names, and weakly linked when they are close but have different lists, which happens at the border between two groups. Then the cells are put into groups so that strong links stay inside groups: start with every cell alone, move each cell to the group of its neighbors that gains the most, then treat each group as one cell and repeat. The method stops when no move helps. The number of groups is not given in advance. It comes from the graph, and it changes with the number of neighbors and with a resolution setting.

## The problem

**Input.** A matrix of $n$ cells by $g$ features, usually log-normalized counts of the [highly variable genes](/highly-variable-gene-selection/), a number of neighbors $k$, a number of principal components $d$ and a resolution $\gamma \ge 0$.

**Output.** A label for each cell.

**Goal.** Labels that match the cell types. This is not a well-defined objective. The method maximizes the modularity of the SNN graph as a stand-in, and finds a local maximum.

## The algorithm

```pseudo id=main
SNN-CLUSTER(X, k, d, γ)
L1  P ← the first d principal component scores of the rows of X
L2  N(i) ← the k nearest cells of i in P, for each cell i; N⁺(i) ← N(i) ∪ {i}
L3  E ← all pairs {i, j} with j ∈ N(i) or i ∈ N(j)
L4  w_ij ← |N⁺(i) ∩ N⁺(j)| / |N⁺(i) ∪ N⁺(j)| for each {i, j} ∈ E
L5  put each vertex of the graph G in its own community
L6  for each vertex i, in order: take i out of its community
L7      put i in the neighboring community C with the largest gain k_{i,C} - γ k_i Σ_C / 2m, or back if none is larger
L8  repeat L6 and L7 until a full pass moves no vertex
L9  G ← the graph with one vertex per community; the weight of (C, D) is the sum of the weights from C to D
L10 if L5 to L8 moved some vertex then go to L5 with the new G
L11 return the community of each cell
```

Lines L1 to L4 build the graph. The neighbor search of line L2 is brute force here; real tools use an approximate index. Line L2 gives the directed [nearest neighbor graph](/nearest-neighbor-graph/), and line L3 makes it undirected, which gives the [k-nearest-neighbor graph](/k-nearest-neighbor-graph/). The SNN graph has the same edges as that graph and differs only in the weights of line L4. Line L4 is the [Jaccard similarity](/jaccard-similarity/) of the two neighbor sets, each with the cell itself. Lines L5 to L10 are the Louvain method. In line L7, $k_{i,C}$ is the weight of the edges from $i$ to $C$, $k_i$ the weighted degree of $i$, $\Sigma_C$ the sum of the degrees in $C$, and $2m$ the sum of all degrees. The gain is $m$ times the change of modularity, so each move raises the modularity. Line L9 shrinks each community to one vertex with a self-loop for the weight inside it, and the moving starts again on the smaller graph.

## Example

Nine cells in two dimensions, with $k = 3$: a square of four cells at $(0, 0), (1, 0), (0, 1), (1, 1)$, a second square at $(4, 0), (5, 0), (4, 1), (5, 1)$, and cell 4 at $(2.6, 0.5)$ between them. The cells are numbered 0 to 8 in this order.

The neighbors of cell 4 are cells 5 and 7, at distance 1.49, and cell 1, at 1.68 (it ties with cell 3 and wins by index). Cell 1 has its own square as neighbors, so the edge from cell 4 to cell 1 has $N^+(4) = \{1, 4, 5, 7\}$ and $N^+(1) = \{0, 1, 2, 3\}$, which share only cell 1: the weight is $1/7$. The edges from cell 4 to cells 5 and 7 share cells 5 and 7 out of six, so they weigh $1/3$. Every edge inside a square weighs 1.

| edge | shared | union | weight |
|---|---|---|---|
| inside a square | 4 | 4 | 1 |
| 4 to 5, 4 to 7 | 2 | 6 | 1/3 |
| 4 to 1 | 1 | 7 | 1/7 |

In the plain $k$-nearest-neighbor graph, cell 4 has one edge to the left and two to the right, all of the same weight. With the SNN weights the left edge is much weaker. The first pass of the moving phase ends with communities $\{0, 1, 2, 3\}$ and $\{4, 5, 6, 7, 8\}$, with modularity $0.4875$; with cell 4 on the left it would be lower. The second level moves nothing, and an exhaustive search over all partitions of the nine cells finds no better one.

## Correctness

Correct here means that each step computes what it claims; whether communities are cell types is measured, not proved. The [proof](proofs/correctness.md) shows that every edge of the $k$-nearest-neighbor graph gets a weight between $1/(2k+1)$ and 1, that the gain of line L7 is the change of modularity, and that line L9 keeps the modularity of every partition. So each move raises the modularity, and the method stops. At the end no single move of a vertex of the last graph raises it, and no community spans two connected components. Maximizing modularity is NP-hard (Brandes et al. 2008), so this is a local optimum. Traag, Waltman and van Eck (2019) show that the Louvain method can even return a community that is not connected inside.

## Complexity

The neighbor search takes $O(n^2d)$ time by brute force, and the weights take $O(nk^2)$ expected time with hash sets, for at most $nk$ edges. One pass of the moving phase takes $O(|E|\log k)$ time, because the communities next to a vertex are sorted. The number of passes and levels has no useful proved bound; in the tests it is small. The graph needs $O(nk)$ space. For many cells the brute force neighbor search dominates, which is why real tools use approximate indexes.

## Properties

- **The number of clusters is an output.** It usually grows with $\gamma$ and falls as $k$ grows. This is an observation, not a theorem.
- **Deterministic in this version.** The vertices are visited in index order and ties go to the smaller label. Most tools visit them in a random order, so the labels change with the seed.
- **Local optimum.** No single vertex move at the last level improves the modularity.
- **Never joins disconnected parts.** A cell only joins a community it has an edge to.
- **Not stable under adding cells.** One new cell can change the neighbor sets of others and move a border.

## Variants and improvements

- **Leiden instead of Louvain.** The [Leiden algorithm](/leiden-algorithm/) refines each community before aggregation, which guarantees connected communities. Seurat and Scanpy both offer it.
- **Without the cell itself.** PhenoGraph computes the Jaccard index of $N(i)$ and $N(j)$ without the cells, so an edge can get weight 0. Seurat includes the cells and removes edges below a small weight.
- **Rank-based weights.** SNN-Cliq (Xu and Su 2015) and scran give weights from the ranks of the shared neighbors instead of their count.
- **Other partitions.** Any [community detection](/community-detection/) method can cut the graph, for example Walktrap or Infomap.
- **Plain $k$-means on the principal components.** [K-means](/k-means/) needs the number of clusters and prefers round groups of similar size; the graph method needs neither.

## When to use it

Use it to find cell types and states in thousands to millions of cells after normalization, gene selection and principal component analysis. Tune $k$ and $\gamma$ to the level of detail you want, and check clusters with marker genes. Draw the clusters on a [UMAP](/umap/) or [t-SNE](/t-sne/) map, but do not cluster on those maps: they are for display, and their distances between groups have no fixed meaning.

## Pitfalls

- **Clusters at any resolution.** Modularity finds communities even in data without structure. A cluster is a hypothesis to test, not a cell type.
- **Small $k$ splits groups.** In the tests, three groups of 40 cells came back exactly with $k = 15$, but with $k = 10$ one group split in two. The split groups were pure, so the error is too many clusters, not mixed ones.
- **Doublets and low quality cells** form their own small clusters. Remove them first, for example with [doublet detection](/doublet-detection/).
- **Batch effects** give clusters by batch. Correct them before building the graph.
- **Disconnected or badly connected communities** from the Louvain method. Use Leiden, or check that each cluster is connected.

## Implementations

## History

Jarvis and Patrick (1973) defined clusters by shared near neighbors: two points belong together when they share many of their nearest neighbors. Blondel and co-authors (2008) published the Louvain method for large networks. In 2015, SNN-Cliq (Xu and Su) used a shared neighbor graph to find cell types in single-cell RNA-seq, and PhenoGraph (Levine et al.) put Jaccard weights on a $k$-nearest-neighbor graph of mass cytometry data and cut it with Louvain. Seurat adopted the plan for single-cell RNA-seq, and Traag, Waltman and van Eck (2019) replaced Louvain with Leiden to fix its badly connected communities.

## References
