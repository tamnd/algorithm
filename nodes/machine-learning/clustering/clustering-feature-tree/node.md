---
tag: 0PD5NK
kind: data-structure
slug: clustering-feature-tree
name: Clustering feature tree
aliases:
- CF tree
- CF-tree of BIRCH
area: machine-learning/clustering
level: advanced
summary: Height-balanced tree whose nodes store clustering-feature summaries, used by BIRCH.
model: external-memory-model
prereqs: [b-tree, clustering-problem]
see_also: [birch, b-tree, r-tree, bfr-algorithm, agglomerative-clustering, ward-method, coreset, kd-tree]
sources:
  - paper: "T. Zhang, R. Ramakrishnan and M. Livny, BIRCH: an efficient data clustering method for very large databases, Proceedings of SIGMOD 1996, pp. 103-114"
    title: Zhang, Ramakrishnan and Livny 1996
    locator: "Section 4 (clustering feature, Definition 4.1 and the CF additivity theorem; CF tree with branching factor B, leaf size L and threshold T; insertion and splitting)"
  - paper: "T. Zhang, R. Ramakrishnan and M. Livny, BIRCH: a new data clustering algorithm and its applications, Data Mining and Knowledge Discovery 1(2), 1997, pp. 141-182"
    title: Zhang, Ramakrishnan and Livny 1997
    locator: the journal version, with the rebuilding algorithm and the reducibility theorem
---

A clustering feature tree (CF tree) is the data structure of [BIRCH](/birch/). It stores a large set of points as a small number of summaries. A summary, the clustering feature, is $\mathrm{CF} = (N, \mathrm{LS}, \mathrm{SS})$: the number of points, their vector sum and the sum of their squared norms. Clustering features add, and the centroid, the radius and the diameter of a set follow from its CF. The tree is height balanced like a [B-tree](/b-tree/). A nonleaf node holds at most $B$ entries, each the CF of a subtree and a pointer to it. A leaf holds at most $L$ entries, and each leaf entry is a small cluster whose radius is at most a threshold $T$. A new point goes down to the closest leaf entry and is absorbed if the radius stays at most $T$.

## In plain words

Suppose you want to keep a summary of a huge set of points in a small memory. For a group of points, you need only three things: how many points there are, the sum of the points, and the sum of their squared lengths. From these three things you get the center of the group and how spread out it is. And two groups join by adding their three things.

A CF tree keeps such summaries in a tree. The bottom level holds many small, tight groups. Each node above holds the sum of the groups below it. To add a point, go down the tree, each time into the child whose center is closest, and at the bottom join the closest small group if it stays tight. If not, start a new group. If a node gets too full, split it in two, as in a B-tree.

## The abstract type

A CF tree stores a multiset of points in $\mathbb{R}^d$ as a partition into small clusters, the leaf entries. It supports:

- `insert(x)`: add a point (or more generally add a CF, which is how a rebuild works);
- `leaf entries`: list the CFs of the small clusters, which a global clustering method then uses as weighted points;
- `rebuild(T')`: make a smaller tree with a larger threshold $T' \ge T$ from the leaf entries;
- `summary`: the CF of all points, the sum of the entries of the root.

It does not support deletion, and it does not store the points.

## Representation

**Clustering feature.** For a set $P$ of $N$ points, $\mathrm{CF}(P) = (N, \mathrm{LS}, \mathrm{SS})$ with $\mathrm{LS} = \sum_{x \in P} x$ and $\mathrm{SS} = \sum_{x \in P}\|x\|^2$. It takes $d + 2$ numbers. For disjoint sets, $\mathrm{CF}(P \cup Q) = \mathrm{CF}(P) + \mathrm{CF}(Q)$. With the centroid $\mu = \mathrm{LS}/N$:

$$R^2 = \frac{1}{N}\sum_{x \in P}\|x - \mu\|^2 = \frac{\mathrm{SS}}{N} - \|\mu\|^2, \qquad D^2 = \frac{1}{N(N-1)}\sum_{x, y \in P}\|x - y\|^2 = \frac{2N\,\mathrm{SS} - 2\|\mathrm{LS}\|^2}{N(N-1)}.$$

$R$ is the radius (the root mean square distance to the centroid) and $D$ the diameter (the root mean square distance between two different points). Distances between two clusters, such as the distance between centroids or the increase of the sum of squares when they are joined, also follow from the two CFs.

**Nodes.** A nonleaf node holds up to $B$ entries $[\mathrm{CF}_i, \mathrm{child}_i]$, where $\mathrm{CF}_i$ is the sum of the entries of $\mathrm{child}_i$. A leaf holds up to $L$ entries $[\mathrm{CF}_i]$, each with $R \le T$ (the paper also allows the test $D \le T$). The leaves are linked in a chain so that all leaf entries can be read in one scan. In the paper, $B$ and $L$ are chosen so that a node fills one disk page of size $P$.

**Invariants.** (1) A nonleaf entry is the sum of the entries of its child. (2) All leaves are at the same depth. (3) A leaf has at most $L$ entries and a nonleaf node at most $B$. (4) Each leaf entry has radius at most $T$. (5) The leaf entries partition the inserted points. There is no lower bound on how full a node is.

## Operations

```pseudo id=main
INSERT(tree, c)              ▷ c is the CF of a point x, that is (1, x, ‖x‖²), or any CF
    at a nonleaf node:
L1      i ← the entry whose centroid is closest to the centroid of c
L2      INSERT into child_i
L7      if child_i did not split then CF_i ← CF_i + c
L8      else replace entry i by the two entries (sum of each half, half)
        if the node now has B + 1 entries then split it
    at a leaf:
L3      e ← the entry whose centroid is closest to the centroid of c
L4      if R(e + c) ≤ T then e ← e + c; return
L5      add c as a new entry
L6      if the leaf now has L + 1 entries then split it
    SPLIT(node): take the two entries with the farthest centroids as seeds;
        each other entry goes with the closer seed; the node keeps one group,
        a new right sibling gets the other
L9  if the root split then make a new root with the two halves as its children
```

The insertion follows one path down and then updates the path on the way up, like a [B-tree](/b-tree/) insertion. A split can go up to the root, and then the tree grows by one level. The paper adds a merging refinement: after a split that stops at some nonleaf node, the two closest entries of that node may be merged and split again, to improve the use of space.

**Rebuild.** When the tree is too large for the memory, BIRCH chooses a larger threshold $T'$ and inserts the old leaf entries into a new tree. Each old entry has $R \le T \le T'$, so it can be inserted as one CF, and the new tree has at most as many leaf entries as the old one. The paper does this path by path and shows that it needs only $h$ extra pages for a tree of height $h$.

## Example

Take points on a line ($d = 1$), $B = 2$, $L = 2$, $T = 1$, and insert $0, 1, 10, 11, 20, 5, 21$. An entry is written $(N, \mathrm{LS}, \mathrm{SS})$.

| insert | what happens | leaves after the step |
|---|---|---|
| 0 | first entry | $(1, 0, 0)$ |
| 1 | joins $(1,0,0)$: $R^2 = 1/2 - 1/4 = 1/4 \le 1$ | $(2, 1, 1)$ |
| 10 | joining $(2,1,1)$ gives $R^2 = 101/3 - (11/3)^2 > 1$: new entry | $(2, 1, 1), (1, 10, 100)$ |
| 11 | joins $(1, 10, 100)$: $R^2 = 1/4$ | $(2, 1, 1), (2, 21, 221)$ |
| 20 | closest is $(2, 21, 221)$, but $R^2 = 621/3 - (41/3)^2 = 182/9 > 1$: new entry, the leaf has 3 entries and splits with seeds $(2,1,1)$ and $(1,20,400)$; the root splits and a new root appears | $(2, 1, 1)$ and $(2, 21, 221), (1, 20, 400)$ |
| 5 | the root entries have centroids $0.5$ and $41/3$; go left; joining gives $R^2 = 26/3 - 4 > 1$: new entry | $(2, 1, 1), (1, 5, 25)$ and $(2, 21, 221), (1, 20, 400)$ |
| 21 | go right; closest entry is $(1, 20, 400)$; joining gives $R^2 = 1/4$ | $(2, 1, 1), (1, 5, 25)$ and $(2, 21, 221), (2, 41, 841)$ |

The root has the entries $(3, 6, 26)$ and $(4, 62, 1062)$, the sums of its two leaves, and their sum $(7, 68, 1088)$ is the CF of all seven points. For the right leaf entry $(2, 41, 841)$, the diameter is $D^2 = (2 \cdot 2 \cdot 841 - 2 \cdot 41^2)/(2 \cdot 1) = 1$, which is $(21 - 20)^2$.

## Correctness

The CF of a union of disjoint sets is the sum of their CFs, and the formulas for $R^2$ and $D^2$ follow by expanding $\|x - \mu\|^2$ and $\|x - y\|^2$. So every test in the insertion uses exact statistics of the points. The insertion keeps the invariants: a leaf entry changes only by a merge that passes the threshold test, a nonleaf entry is updated by the same CF that was added below it, and a split keeps the leaves at one depth because it makes siblings, while a root split adds one level above all leaves at once. The full proof is on the correctness page.

## Complexity

Let $h$ be the height and $d$ the dimension. One CF operation costs $O(d)$.

| operation | time | disk pages read and written |
|---|---|---|
| insert a point | $O(h(B + L)d)$ without splits; a split costs $O((B + L)^2 d)$ for the farthest pair | $O(h)$ |
| summary of all points | $O(Bd)$ | 1 |
| scan of all leaf entries | $O(\text{leaf entries} \cdot d)$ | the number of leaves |
| rebuild with a larger $T$ | $O(\text{leaf entries} \cdot h(B + L)d)$ | $O(\text{nodes})$, with $h$ extra pages in the paper's method |

The space is $O(d + 2)$ numbers per entry, so a tree with $m$ leaf entries takes $O(md)$ space whatever the number of points. Because there is no lower fill bound, the height is not bounded by $\log_B$ of the number of entries in the worst case, but in practice the tree is shallow.

## Variants

- **Threshold on the diameter.** The leaf test can use $D \le T$ in place of $R \le T$.
- **Other distances.** The descent can use any of the distances $D_0$ to $D_4$ of BIRCH between clusters, all computed from CFs: centroid Euclidean, centroid Manhattan, average inter-cluster, average intra-cluster and the variance increase.
- **Outlier handling.** BIRCH can write sparse leaf entries to disk during a rebuild and try to insert them again later.
- **Weighted points and CFs.** Inserting a CF in place of a point is how rebuilding works, and it lets a CF tree merge summaries from several sources.
- **BFR statistics.** The [BFR algorithm](/bfr-algorithm/) keeps the sum of squares per dimension, which gives the variance in each dimension and not only the total.

## When to use it

Use a CF tree to compress a large Euclidean data set in one scan into a few thousand weighted micro-clusters, which a slower method such as [agglomerative clustering](/agglomerative-clustering/) or k-means can then cluster. It suits round clusters in low or moderate dimension. For range or nearest neighbor queries on the points, use an index such as an [R-tree](/r-tree/) or a [kd-tree](/kd-tree/): a CF tree does not keep the points.

## Pitfalls

- **Order of insertion.** The leaf entries depend on the order of the points. A cluster can be split between two branches if its points arrive late.
- **Node size, not natural size.** A split is forced by $B$ or $L$, not by the data, so one natural cluster can end up in several leaves.
- **Precision.** $\mathrm{SS}/N - \|\mu\|^2$ subtracts two large numbers; in floating point it can lose all digits or become slightly negative. Center the data first or clamp at zero.
- **Euclidean only.** The CF needs vector sums, so the tree does not work for a general metric. BIRCH* variants for metric spaces keep other summaries.
- **The threshold.** A $T$ too small gives a huge tree, and too large merges different clusters into one entry, which no later step can split.

## Implementations

## History

Zhang, Ramakrishnan and Livny introduced clustering features and the CF tree as part of BIRCH at SIGMOD 1996. The journal version of 1997 gives the rebuilding algorithm and the result that a rebuild with a larger threshold needs only a few extra pages. Clustering features with per-dimension sums of squares were used in the [BFR algorithm](/bfr-algorithm/), and summaries of the same kind, called micro-clusters, are the base of many later stream clustering methods.

## References
