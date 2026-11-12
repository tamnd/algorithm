---
tag: 2GBS7F
kind: data-structure
slug: dendrogram
name: Dendrogram
aliases:
- cluster tree
- merge tree
area: machine-learning/clustering
level: intro
summary: "Rooted binary tree of a hierarchical clustering: each internal node merges two clusters and is drawn at the height of that merge."
model: real-ram
prereqs: [binary-tree, clustering-problem]
see_also: [hierarchical-clustering-problem, ultrametric, agglomerative-clustering, divisive-clustering, lowest-common-ancestor, phylogenetic-tree, newick-format, dasgupta-cost]
sources:
  - paper: doi:10.2307/1217208
    title: "Robert R. Sokal and F. James Rohlf, The comparison of dendrograms by objective methods, Taxon 11(2) (1962), 33-40"
    locator: the cophenetic value of a pair and the cophenetic correlation coefficient
  - paper: doi:10.1007/BF02289588
    title: "Stephen C. Johnson, Hierarchical clustering schemes, Psychometrika 32(3) (1967), 241-254"
    locator: the nested sequence of clusterings with levels, and its one-to-one match with ultrametric distances
  - book: isbn:9780130222787
    title: Anil K. Jain and Richard C. Dubes, Algorithms for Clustering Data
    locator: Chapter 3, Section 3.2 (dendrograms, threshold cuts and the cophenetic matrix)
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, second edition
    locator: Section 14.3.12 (hierarchical clustering, the dendrogram and the cophenetic correlation coefficient)
---

A dendrogram is the output of [hierarchical clustering](/hierarchical-clustering-problem/). It is a rooted [binary tree](/binary-tree/) whose leaves are the $n$ points. Each internal node is a cluster, made by the merge of the clusters of its two children, and it carries a height: the dissimilarity at which the merge happens. A cut of the tree at a height, or at a number $k$ of clusters, gives one flat clustering, so one tree holds a whole nested family of clusterings. The height of the [lowest common ancestor](/lowest-common-ancestor/) of two points is their *cophenetic distance*. When the heights increase toward the root, these distances form an [ultrametric](/ultrametric/).

## In plain words

Draw each point as a short line at the bottom of a page. When two groups join, draw a bar above both of them, at a height that tells how far apart the groups were. The bar becomes a new group, and later it can join other groups. At the end, one bar at the top holds all the points.

To get a fixed number of groups, slide a ruler across the drawing from the top down. The lines that the ruler crosses are the groups. A low ruler gives many small groups, and a high ruler gives few large groups.

For any two points, look for the lowest bar that holds both of them. Its height says how close the drawing thinks the two points are.

## The abstract type

A dendrogram on the leaves $1, \ldots, n$ stores a rooted binary tree with $n$ leaves and $n - 1$ internal nodes, and a height $h(v) \ge 0$ for each internal node $v$. The leaves have height $0$. The operations are:

- `build(merges)`: make the tree from the list of $n - 1$ merges, each one a pair of current clusters and a height.
- `cophenetic(i, j)`: the height of the lowest common ancestor of the leaves $i$ and $j$.
- `cut-height(t)`: the clusters of the maximal nodes of height at most $t$.
- `cut-k(k)`: the $k$ clusters that remain when the last $k - 1$ merges are undone.
- `leaves(v)`: the cluster of node $v$.

The tree is *monotone* when $h(\text{parent}(v)) \ge h(v)$ for each internal node $v$ other than the root. Single, complete, average and [Ward](/ward-method/) linkage give monotone trees. Centroid and median linkage can give an *inversion*, a parent lower than its child (see [linkage criterion](/linkage-criterion/)).

## Representation

Number the leaves $1$ to $n$, and give the node made by merge $t$ the number $n + t$. Store four arrays of length $2n - 1$: left child, right child, parent and height. Add a fifth array with the number of leaves below each node. A node is made after both of its children, so the node numbers are a topological order of the tree, from the leaves to the root $2n - 1$. This is also the format of the merge matrix of SciPy and R: one row per merge, with the two children, the height and the size.

## Operations

```pseudo id=main
COPHENETIC(T)                     ▷ C[i, j] = h(lca(i, j)) for all pairs
L1  below[i] ← {i} for each leaf i
L2  for v ← n + 1 to 2n − 1 do     ▷ the nodes in the order of the merges
L3      (a, b) ← the two children of v
L4      for each i in below[a] and each j in below[b] do
L5          C[i, j] ← C[j, i] ← h(v)
L6      below[v] ← below[a] ∪ below[b]
L7  return C

CUT-K(T, k)                       ▷ undo the last k − 1 merges
L8  R ← {2n − 1}
L9  while |R| < k do
L10     v ← the node of R with the largest number
L11     R ← (R − {v}) ∪ {left(v), right(v)}
L12 return the leaf sets of the nodes in R
```

```pseudo id=cut-height
CUT-HEIGHT(T, t)                  ▷ for a monotone tree
1  R ← empty, S ← {2n − 1}
2  while S is not empty do
3      take a node v out of S
4      if v is a leaf or h(v) ≤ t then add v to R
5      else add left(v) and right(v) to S
6  return the leaf sets of the nodes in R
```

COPHENETIC writes each pair one time, at the merge where the two points first meet. CUT-K uses the numbering: the latest merge among the nodes of $R$ is the node with the largest number. CUT-HEIGHT walks down from the root and stops at the first node on each path that is low enough.

## Example

Complete linkage on the six points $a, b, c, d, e, f$ at $0, 2, 3, 7, 13, 21$ on a line, with $|x - y|$ as the dissimilarity, makes these merges.

| node | children | height | cluster |
|---|---|---|---|
| 7 | $b$, $c$ | 1 | $\{b, c\}$ |
| 8 | $a$, 7 | 3 | $\{a, b, c\}$ |
| 9 | $d$, $e$ | 6 | $\{d, e\}$ |
| 10 | 8, 9 | 13 | $\{a, b, c, d, e\}$ |
| 11 | $f$, 10 | 21 | all six points |

The heights increase, so the tree is monotone. Some cophenetic distances are $C(b, c) = 1$, $C(a, c) = 3$, $C(d, e) = 6$, $C(a, d) = 13$ and $C(e, f) = 21$. The input distance $|a - d| = 7$ grows to $13$, because $a$ and $d$ meet only at node 10.

A cut at height $6$ keeps the nodes 8 and 9 and the leaf $f$. It gives $\{a, b, c\}$, $\{d, e\}$, $\{f\}$. The cut at $k = 3$ undoes the merges 11 and 10 and gives the same three clusters. A cut at height $5$ gives four clusters: $\{a, b, c\}$, $\{d\}$, $\{e\}$, $\{f\}$.

The cophenetic correlation of this tree, the Pearson correlation of the 15 pairs of input distances with the 15 cophenetic distances, is about $0.825$. The single linkage tree of the same points is a chain, and its cophenetic correlation is about $0.861$.

## Correctness

COPHENETIC keeps the invariant that, before node $v$ is handled, $\text{below}[u]$ is the leaf set of each node $u < v$, and $C[i, j]$ is set exactly for the pairs that have a common ancestor below $v$. Two distinct leaves $i$ and $j$ are in different children of exactly one node, their lowest common ancestor. So line L5 writes $C[i, j]$ one time, with the right height. CUT-K holds the roots of the forest after the first $n - |R|$ merges: the root after all merges at the start, and one merge fewer after each step, because the latest merge is always a root of the current forest. For a monotone tree, CUT-HEIGHT gives the classes of the relation $C(i, j) \le t$, and these are the clusters after all merges of height at most $t$. The full proofs are in [the correctness proof](proofs/correctness.md).

## Complexity

Let $n$ be the number of leaves.

| operation | time |
|---|---|
| build from $n - 1$ merges | $\Theta(n)$ |
| leaves$(v)$ | $\Theta(\lvert v \rvert)$ |
| cut-height$(t)$ | $O(n)$ |
| cut-k$(k)$ | $O(n + k^2)$ as written, $O(n)$ by a scan of the node numbers |
| cophenetic matrix | $\Theta(n^2)$ |
| one cophenetic distance | $O(1)$ after $O(n)$ preprocessing for lowest common ancestors |
| cophenetic correlation | $\Theta(n^2)$ |
| space | $\Theta(n)$ words |

The cophenetic matrix has $n(n - 1)/2$ entries, so $\Theta(n^2)$ is optimal for it. A single cophenetic distance needs no matrix: a [lowest common ancestor](/lowest-common-ancestor/) structure answers each query in $O(1)$ time. A cut at $k$ can also scan the nodes $1, \ldots, 2n - k$ and keep those whose parent is above $2n - k$, which takes $O(n)$ time.

## Variants

- **Non-binary trees.** Merges at the same height can be drawn as one node with three or more children. This form is unique for each set of nested partitions, which makes it the right form for the bijection with ultrametrics.
- **Divisive dendrograms.** A [divisive](/divisive-clustering/) method builds the same kind of tree from the top. The height of a node is then often the diameter of its cluster.
- **Trees with inversions.** Centroid and median linkage can put a parent below a child. Such a tree is still a tree of nested clusters, but a cut at a height is not well defined, and the cophenetic matrix is not an ultrametric.
- **Phylogenetic trees.** A [phylogenetic tree](/phylogenetic-tree/) with a root and equal distances from the root to each leaf is a dendrogram. Such trees are often stored in the [Newick format](/newick-format/).
- **Condensed trees.** [HDBSCAN](/hdbscan/) prunes a single linkage tree so that each node is a cluster of at least a minimum size.

## When to use it

Use a dendrogram to store the result of any agglomerative or divisive method, and to choose a flat clustering after the run. One run gives the clusters for each $k$, so you can compare many cuts without new runs. Draw it to see how many natural groups the data has: long vertical gaps between merges show a good place to cut. Use the cophenetic correlation to compare linkage criteria on the same data.

## Pitfalls

- **Inversions.** A cut at a height assumes a monotone tree. With centroid or median linkage, sort out the inversions before a cut, or cut at $k$.
- **The order of the leaves is not data.** Each internal node can swap its two children, so there are $2^{n-1}$ drawings of one tree. Two points side by side in the drawing can be far apart in the tree.
- **The heights depend on the method.** SciPy reports $\sqrt{2\,\Delta}$ for Ward linkage, where $\Delta$ is the increase in the sum of squares, and other tools report $\Delta$. Do not compare heights from two tools without a check.
- **Ties.** With equal dissimilarities, the binary tree is not unique, but the non-binary tree and the cophenetic matrix are unique for single linkage.

## Implementations

## History

Dendrograms come from numerical taxonomy, where they drew the relations between species. Sokal and Rohlf (1962) defined the cophenetic value of a pair and the cophenetic correlation to measure how well a tree fits the data. Johnson (1967) showed that the nested clusterings with levels match the distances that satisfy the ultrametric inequality. Jardine and Sibson (1971) made this match exact and studied it as a map from dissimilarities to trees.

## References
