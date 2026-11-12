---
tag: R802SX
kind: problem
slug: hierarchical-clustering-problem
name: Hierarchical clustering problem
aliases:
- tree clustering
area: machine-learning/clustering
level: core
summary: "Build a nested family of clusters of n points, from single points up to the full set, as a tree. There is no single objective in general."
prereqs: [clustering-problem, dendrogram]
see_also: [agglomerative-clustering, divisive-clustering, linkage-criterion, ultrametric, dasgupta-cost, single-linkage-clustering, hdbscan, upgma]
sources:
  - paper: doi:10.1007/BF02289588
    title: "Stephen C. Johnson, Hierarchical clustering schemes, Psychometrika 32(3) (1967), 241-254"
    locator: the hierarchy as a sequence of nested clusterings with levels, and its match with ultrametrics
  - book: isbn:9780130222787
    title: Anil K. Jain and Richard C. Dubes, Algorithms for Clustering Data
    locator: Chapter 3, Section 3.2 (hierarchical clustering, nested clusterings and dendrograms)
  - paper: doi:10.1002/widm.53
    title: "Fionn Murtagh and Pedro Contreras, Algorithms for hierarchical clustering: an overview, WIREs Data Mining and Knowledge Discovery 2(1) (2012), 86-97"
    locator: the survey of agglomerative and divisive methods and their running times
  - paper: doi:10.1145/2897518.2897527
    title: "Sanjoy Dasgupta, A cost function for similarity-based hierarchical clustering, Proceedings of the 48th ACM Symposium on Theory of Computing (STOC 2016), 118-127"
    locator: the remark that hierarchical clustering lacks an objective, and the cost function that it proposes
  - paper: "Gunnar Carlsson and Facundo Mémoli, Characterization, stability and convergence of hierarchical clustering methods, Journal of Machine Learning Research 11 (2010), 1425-1470"
    locator: the axioms for hierarchical clustering methods, under which single linkage is the only method
  - paper: "Mirko Křivánek and Jaroslav Morávek, NP-hard problems in hierarchical-tree clustering, Acta Informatica 23(3) (1986), 311-323"
    locator: the NP-hardness of fitting an ultrametric to a dissimilarity in the least-squares and least-absolute-deviation senses
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schütze, Introduction to Information Retrieval
    locator: Chapter 17 (hierarchical clustering of documents)
---

The hierarchical clustering problem asks for a whole family of nested clusters of a set of $n$ points, instead of one partition. The family runs from the $n$ single points up to the full set, and any two of its clusters are either disjoint or one inside the other. Such a family is a rooted tree with the points as leaves, and with a height at each internal node it is a [dendrogram](/dendrogram/). Unlike the [k-means problem](/k-means-problem/), the problem has no single standard objective: most methods define the tree by a procedure, such as [agglomerative clustering](/agglomerative-clustering/) with a [linkage criterion](/linkage-criterion/), and the objectives that exist, such as [Dasgupta's cost](/dasgupta-cost/), are NP-hard to optimize.

## In plain words

You have a set of items and a way to say how different two items are. You do not know how many groups to make. So you make all of them at once, in layers.

At the bottom, each item is a group of its own. At each step up, two groups join into one. At the top, all items are in one group. The record of the joins is a tree. If you want a fixed number of groups, you cut the tree at the right level.

There are many reasonable ways to choose which groups join, and they give different trees. No single score says which tree is the best one. So each method is a rule, and you pick the rule that suits your data.

## Definition

**Input.** A finite set $X$ of $n$ points and a dissimilarity $d : X \times X \to \mathbb{R}_{\ge 0}$ with $d(x, x) = 0$ and $d(x, y) = d(y, x)$. Often $X \subset \mathbb{R}^p$ and $d$ is the [Euclidean distance](/euclidean-distance/) or its square. Some methods take a similarity graph with weights $w_{ij} \ge 0$ instead.

**Output.** A *hierarchy* on $X$: a family $\mathcal{H}$ of non-empty subsets of $X$, the clusters, such that

1. $X \in \mathcal{H}$ and $\{x\} \in \mathcal{H}$ for each $x \in X$, and
2. any two clusters $A, B \in \mathcal{H}$ satisfy $A \cap B = \emptyset$, $A \subseteq B$ or $B \subseteq A$.

A hierarchy is the same as a rooted tree whose leaves are the points: each cluster is the leaf set of a node. A hierarchy is *binary* if each cluster with two or more points is the union of exactly two clusters; it then has $n - 1$ such clusters. A binary hierarchy is the same as a chain of partitions $P_0, P_1, \ldots, P_{n-1}$, where $P_0$ has the $n$ single points, $P_{n-1} = \{X\}$, and each $P_{t}$ comes from $P_{t-1}$ by the union of two blocks. With heights $0 \le h_1 \le \cdots \le h_{n-1}$ for the steps, the output is a monotone dendrogram, and by the theorem on the [ultrametric](/ultrametric/) page it is the same as an ultrametric $u$ on $X$.

**No objective in general.** The problem as stated has no cost to minimize. Each method gives a tree by a rule, and the methods are compared by their properties. There are $(2n - 3)!! = 1 \cdot 3 \cdot 5 \cdots (2n - 3)$ binary hierarchies on $n$ labeled points, so a search over all trees is not practical beyond about ten points.

## Variants

- **With or without heights.** A dendrogram has heights and gives an ultrametric. Objectives such as Dasgupta's cost score only the tree shape.
- **Bottom up or top down.** [Agglomerative clustering](/agglomerative-clustering/) merges the two closest clusters at each step. [Divisive clustering](/divisive-clustering/) splits a cluster into two at each step.
- **Ultrametric fitting.** Find an ultrametric $u$ that is close to $d$ in a norm. The largest ultrametric below $d$ is the subdominant ultrametric, which [single linkage](/single-linkage-clustering/) gives. Fitting in the least-squares or least-absolute-deviation sense is NP-hard (Křivánek and Morávek 1986).
- **Objective-based trees.** [Dasgupta's cost](/dasgupta-cost/) and its dual, the revenue of Moseley and Wang, score a tree on a similarity graph. They turn the problem into an optimization problem with approximation algorithms.
- **Axiomatic methods.** Carlsson and Mémoli (2010) state axioms for methods that map a finite metric space to an ultrametric. Single linkage is the only method that satisfies them.
- **Constrained hierarchies.** Some applications allow only merges of neighbors in a graph, for example of adjacent pixels or regions on a map.

## Examples

Take six points on a line: $a, b, c, d, e, f$ at $0, 2, 3, 7, 13, 21$, with $d(x, y) = |x - y|$. All 15 distances are distinct. Three common linkage criteria give three different trees. Each row lists a merge and its height.

| step | single linkage | complete linkage | average linkage |
|---|---|---|---|
| 1 | $\{b, c\}$ at 1 | $\{b, c\}$ at 1 | $\{b, c\}$ at 1 |
| 2 | $\{a, b, c\}$ at 2 | $\{a, b, c\}$ at 3 | $\{a, b, c\}$ at $5/2$ |
| 3 | $\{a, b, c, d\}$ at 4 | $\{d, e\}$ at 6 | $\{a, b, c, d\}$ at $16/3$ |
| 4 | $\{a, \ldots, e\}$ at 6 | $\{a, \ldots, e\}$ at 13 | $\{e, f\}$ at 8 |
| 5 | all at 8 | all at 21 | all at 14 |

The cuts into three clusters are $\{a, b, c, d\}, \{e\}, \{f\}$ for single linkage, $\{a, b, c\}, \{d, e\}, \{f\}$ for complete linkage, and $\{a, b, c, d\}, \{e\}, \{f\}$ for average linkage. The cuts into two clusters are $\{a, \ldots, e\}, \{f\}$ for single and complete linkage, but $\{a, b, c, d\}, \{e, f\}$ for average linkage. Single linkage adds one point at a time, which is called chaining. None of the three trees is "the" answer: each one is the right output of its own rule.

## Known algorithms

| method | time | memory | notes |
|---|---|---|---|
| [agglomerative clustering](/agglomerative-clustering/), naive | $O(n^3)$ | $\Theta(n^2)$ | any [linkage](/linkage-criterion/) with the [Lance-Williams formula](/lance-williams-formula/) |
| agglomerative clustering with a priority queue | $O(n^2 \log n)$ | $\Theta(n^2)$ | any linkage |
| [nearest-neighbor chain](/nearest-neighbor-chain/) | $O(n^2)$ | $\Theta(n^2)$ | single, complete, average, weighted and Ward |
| [SLINK](/slink/) | $O(n^2)$ | $O(n)$ | single linkage |
| [minimum spanning tree](/minimum-spanning-tree/) | $O(n^2)$, or $O(n \log n)$ in the plane | $O(n)$ | single linkage |
| [divisive clustering](/divisive-clustering/) (DIANA) | $O(n^3)$ | $\Theta(n^2)$ | top down; the matrix, and $O(n)$ beyond it |
| recursive sparsest cut | polynomial | | $O(\sqrt{\log n})$ approximation of Dasgupta's cost |

[Ward's method](/ward-method/) and the [complete-linkage](/complete-linkage-clustering/) method are agglomerative methods with their own linkage. [Bisecting k-means](/bisecting-k-means/) is a divisive method. [BIRCH](/birch/) and [HDBSCAN](/hdbscan/) build hierarchies for large or noisy data.

## Bounds

For a general dissimilarity matrix, each exact algorithm for single, complete or average linkage must read all $n(n - 1)/2$ entries in the worst case, for $n \ge 3$. Answer each read with a distinct value in $[3/2, 2]$. If a pair $x, y$ is never read, both $d(x, y) = 1$ and a value just below $2$ that is larger than all read values are possible, and the values in $[1, 2]$ always form a metric. In the first input, $\{x, y\}$ is the first merge, and in the second it is not. So $O(n^2)$ time, as for SLINK and the nearest-neighbor chain, is optimal for these methods on a matrix. For points in a space of low dimension, faster methods exist, for example single linkage in the plane in $O(n \log n)$ time with the [Euclidean minimum spanning tree](/euclidean-minimum-spanning-tree/).

For Dasgupta's cost, the best tree is NP-hard to find. Under the small set expansion hypothesis there is no constant factor approximation.

## Reductions

- **Single linkage and minimum spanning trees.** The single linkage tree is Kruskal's algorithm on the complete graph, recorded as a tree (Gower and Ross 1969). A minimum spanning tree gives the single linkage tree in $O(n \log n)$ extra time: sort its $n - 1$ edges and replay them with a [disjoint-set](/disjoint-set/) structure.
- **Flat clustering from a tree.** A cut of the tree at $k$ clusters gives a flat clustering. For single linkage, this cut is the [maximum spacing k-clustering](/maximum-spacing-k-clustering/).
- **Dasgupta's cost and sparsest cut.** A tree that splits each cluster by an approximate [sparsest cut](/sparsest-cut-problem/) approximates Dasgupta's cost within $O(\alpha)$, where $\alpha$ is the sparsest cut ratio.
- **Phylogenetics.** [UPGMA](/upgma/) is average linkage, and [WPGMA](/wpgma/) is weighted linkage. Both build a rooted tree of species from a distance matrix.

## Applications

- Taxonomy and [phylogenetics](/phylogenetic-tree/): trees of species from distances between their genes.
- Gene expression: clustered heat maps sort the rows and columns of a matrix by the leaf order of two dendrograms.
- Documents: topic trees and cluster browsing of search results.
- Density-based clustering: [HDBSCAN](/hdbscan/) and [OPTICS](/optics/) read clusters from a hierarchy of density levels.
- Image segmentation: region merging is agglomerative clustering with a constraint that only adjacent regions merge.

## References
