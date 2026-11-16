---
tag: GS7MJP
kind: data-structure
slug: randomized-kd-forest
name: Randomized k-d forest
aliases:
- randomized kd-trees
- FLANN kd-forest
area: computer-vision/local-features
level: advanced
summary: Several k-d trees that split on dimensions chosen at random among those of highest variance, searched together through one priority queue for approximate neighbors.
implements: [similarity-index]
model: real-ram
complexity:
  vars: {n: the number of points, d: the dimension, T: the number of trees, h: the height of a tree, C: the number of points to check, k: the number of neighbors}
  time: {build: O(T d n h), insert: O(T (h + d)), search: O(T C h (d + log(T C h)) + C log k)}
  space: {total: O(T n + n d)}
properties: {randomized: true, exact: false, anytime: true, exact_when_unbounded: true, dynamic: true}
history:
  year: 2008
  people: [Chanop Silpa-Anan, Richard Hartley, Marius Muja, David G. Lowe]
  note: Silpa-Anan and Hartley searched several k-d trees with one priority queue at CVPR 2008. Muja and Lowe chose the split dimension at random among the top 5 by variance and built FLANN in 2009.
prereqs: [kd-tree, best-bin-first-search]
see_also: [kd-tree-nearest-neighbor-search, approximate-nearest-neighbor-search, feature-matching, sift, rp-tree, locality-sensitive-hashing, hnsw, random-forest]
sources:
  - paper: doi:10.1109/CVPR.2008.4587638
    title: "Chanop Silpa-Anan and Richard Hartley, Optimised KD-trees for fast image descriptor matching, IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2008"
    locator: the multiple randomized trees searched at the same time with one priority queue, and the experiments on SIFT descriptors
  - paper: doi:10.5220/0001787803310340
    title: "Marius Muja and David G. Lowe, Fast approximate nearest neighbors with automatic algorithm configuration, International Conference on Computer Vision Theory and Applications (VISAPP), 2009, volume 1, 331-340"
    locator: "Section 3.1 (the split dimension drawn at random from the 5 dimensions of greatest variance, one priority queue across all trees, a fixed number of leaves)"
  - paper: doi:10.1109/TPAMI.2014.2321376
    title: "Marius Muja and David G. Lowe, Scalable nearest neighbor algorithms for high dimensional data, IEEE Transactions on Pattern Analysis and Machine Intelligence 36(11), 2014, 2227-2240"
    locator: the section on the randomized k-d tree algorithm and the comparison with the priority search k-means tree
  - paper: "Jeffrey S. Beis and David G. Lowe, Shape indexing using approximate nearest-neighbour search in high-dimensional spaces, IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 1997, 1000-1006"
    locator: "Section 4 (the single k-d tree and the best bin first search that the forest extends)"
---

A randomized k-d forest is an index for approximate nearest neighbor search that holds $T$ [k-d trees](/kd-tree/) over the same points. Each tree splits a node on a dimension drawn at random from the few dimensions where its points vary most, so the trees cut space in different ways. A search runs [best bin first](/best-bin-first-search/) on all trees at once with one priority queue and checks each point at most once. A point that one tree puts in a far bin is often in a near bin of another tree, so with the same number of checks the forest finds the true neighbor more often than one tree. Silpa-Anan and Hartley (2008) and Muja and Lowe (2009) built it for matching [SIFT](/sift/) descriptors, and it is the default index of the FLANN library.

## In plain words

One k-d tree cuts space into boxes. If the true nearest point sits just over the edge of the box of the query, the search may have to look at many boxes before it finds it. Now build four trees, each with its own random choice of cuts. The edges are in different places in each tree, so the true neighbor is likely close to the query box in at least one of them. The search keeps one list of boxes from all four trees, sorted by distance from the query, and always opens the closest box. It remembers which points it has already measured, so no point is measured twice. It stops after a fixed number of points.

## The abstract type

The forest stores a set of points in $\mathbb{R}^d$ and supports:

- **BUILD(P)**: make the forest for a set of points.
- **INSERT(x)**: add a point.
- **SEARCH(q, k, C)**: return $k$ points close to $q$, after at most about $C$ distance computations, and say whether the answer is proved exact.

With $C = \infty$, SEARCH returns the exact [k nearest neighbors](/k-nearest-neighbor-search/). With a finite $C$ it is an [approximate nearest neighbor search](/approximate-nearest-neighbor-search/) with no bound on the error. Distances are Euclidean.

## Representation

Each tree is a binary tree. An internal node holds a dimension $j$ and a split value $s$. Points with $x_j < s$ go to the left child and points with $x_j \ge s$ go to the right child. A leaf holds the indices of at most $\ell$ points, or any number of equal points. FLANN uses $\ell = 1$. The points themselves are stored once, in an array that all trees share.

The split rule is the random part. At a node with point set $S$, compute the mean $m_t$ and the variance of each dimension $t$ over $S$. Take the $D$ dimensions of largest variance, draw one of them, $j$, uniformly at random, and split at $s = m_j$. Muja and Lowe use $D = 5$. FLANN estimates the mean and the variance from a sample of the first 100 points of the node and uses 4 trees by default; our code uses all points of the node.

## Operations

```pseudo id=main
BUILD(P, T, D)
L1  for t = 1 to T do root_t ← MAKE(all indices of P)
MAKE(S)
L2  if |S| ≤ ℓ or all points of S are equal then return a leaf holding S
L3  compute the mean m_t and the variance v_t of each dimension t over S
L4  K ← the D dimensions with the largest v_t > 0
L5  j ← a dimension drawn uniformly at random from K
L6  L ← {i ∈ S : x_ij < m_j}; R ← S \ L
L7  return a node with dimension j, split m_j and children MAKE(L) and MAKE(R)
```

```pseudo id=insert
INSERT(x)
L8  store x with a new index i
L9  for each tree t do
L10     go down from root_t: left if x_j < s, else right, until a leaf
L11     add i to the leaf
L12     if the leaf has more than ℓ points then replace it by MAKE(its indices)
```

```pseudo id=search
SEARCH(q, k, C)
L13 best ← empty list of at most k (distance, index) pairs; seen ← empty set; checked ← 0
L14 Q ← min-priority queue holding (0, root_t, zero offsets) for each tree t
L15 while Q is not empty and checked < C do
L16     (b, node, o) ← remove the entry with the smallest key from Q
L17     if best has k items and b ≥ the largest distance in best then stop: the answer is exact
L18     while node is an internal node do
L19         j ← dimension of node; δ ← q_j - split of node
L20         if δ < 0 then near, far ← left, right else near, far ← right, left
L21         insert (b - o_j^2 + δ^2, far, o with o_j = δ) into Q
L22         node ← near
L23     for each index i in the leaf with i ∉ seen do
L24         add i to seen; checked ← checked + 1; put (‖x_i - q‖^2, i) in best if it is among the k closest
L25 return best
```

The key $b$ of a queue entry is the squared distance from $q$ to the bin of its subtree, with the offset vector $o$ as in [best bin first search](/best-bin-first-search/). Line L21 replaces the offset of dimension $j$; it does not add to it. The shared queue of line L14 is what makes the trees work together: the next bin is the closest one in any tree. The set of line L23 keeps a point that sits in near bins of several trees from being counted several times.

## Example

Take the eight points $(1,1)$, $(2,6)$, $(3,3)$, $(5,8)$, $(6,2)$, $(7,6)$, $(8,4)$, $(9,9)$, with $T = 2$, $D = 2$, $\ell = 1$ and seed 5 in our code. The variances are 7.36 for $x$ and 7.11 for $y$, and the means are 5.125 and 4.875. Tree 1 drew $y$ at the root and splits at $y = 4.875$; tree 2 drew $x$ and splits at $x = 5.125$. The query is $q = (5.2, 4.6)$. Its nearest neighbor is $(7, 6)$ at squared distance 5.2, and the next one is $(3,3)$ or $(6, 2)$ at 7.4.

The search with a budget of $C = 2$ checks:

1. The queue holds both roots with key 0. It pops the root of tree 1. At $y < 4.875$ the query goes left, $\delta = -0.275$, and the right subtree gets key $0.0756$. At $y < 2.5$ it goes right and pushes the left subtree with key $2.1^2 = 4.41$. At $y < 3.5$ it goes right to the leaf $(8, 4)$, at squared distance 8.2, and pushes $(3,3)$ with key $1.1^2 = 1.21$. One check.
2. The smallest key is now the root of tree 2, with 0. At $x < 5.125$ the query goes right, $\delta = 0.075$, and pushes the left subtree with key $0.0056$. At $x < 7.5$ it goes left and pushes the right subtree with key $2.3^2 = 5.29$. At $y < 4$ it goes right to the leaf $(7, 6)$, at squared distance 5.2. Two checks, and the search stops.

The forest returns $(7, 6)$, the true neighbor. Tree 1 alone with the same budget pops its key 0.0756 next, reaches the leaf $(5, 8)$ at 11.6, and returns $(8, 4)$ at 8.2; it needs a third check to reach $(7, 6)$. The answer of the forest is not yet proved exact: the queue still holds a key of 0.0056, which is less than 5.2.

A measured example: we built the forest in our code on 5000 points uniform in $[0, 1]^{16}$ with seed 11 and ran 100 uniform queries. The table gives the number of queries, out of 100, whose true nearest neighbor was returned.

| trees | $C = 50$ | $C = 200$ | $C = 800$ |
| --- | --- | --- | --- |
| 1 | 65 | 89 | 100 |
| 4 | 71 | 92 | 100 |
| 8 | 76 | 92 | 100 |

On this uniform data the gain from more trees is small. Silpa-Anan and Hartley and Muja and Lowe report larger gains on real SIFT descriptors. These are measurements, and they depend on the data.

## Correctness

The proof in `proofs/correctness.md` shows these facts:

- **Every tree indexes every point.** After BUILD and after each INSERT, each index is in exactly one leaf of each tree, and each point lies in the cell of its leaf. MAKE ends because a dimension with positive variance always has points on both sides of its mean.
- **The key is a lower bound.** Every point in the subtree of a queue entry is at squared distance at least its key from $q$.
- **One check per point.** No distance is computed twice in one search.
- **Exact when it stops by itself.** If the queue empties or line L17 stops the loop, the answer is the exact $k$ nearest neighbors.
- **More checks do not hurt.** A larger budget never returns a worse $i$-th neighbor.

That several random trees beat one tree at the same budget is a measured result, not a theorem.

## Complexity

The model is the real RAM. Let $h$ be the largest height of a tree. With mean splits the trees are not always balanced: for points with coordinates $1, 2, 4, 8, \dots$ each mean split puts one point on the right, and $h = n - 1$. On typical descriptor data $h$ is close to $\log_2 n$.

- **Build.** Each level of a tree computes $d$ means and variances over at most $n$ points, so one tree costs $O(d n h)$ and the forest $O(T d n h)$. Sorting the variances adds $O(d \log d)$ per node. FLANN's sample of 100 points makes the statistics $O(d)$ per node.
- **Insert.** One descent of length $h$ per tree, and a split of a leaf of $\ell + 1$ points at $O(d \ell)$, so $O(T (h + d))$ for a constant $\ell$.
- **Search.** With $\ell = 1$, each tree reaches each leaf at most once, and a leaf whose point was already seen does not count as a check. So the search reaches at most $T (C + 1)$ leaves. Each leaf costs one descent of at most $h$ pushes of $O(d + \log(\text{queue size}))$, and each check costs $O(d + \log k)$. The total is $O(T C h (d + \log(T C h)) + C \log k)$. In practice most reached leaves are new, and the cost is close to that of $C$ leaves of one tree.
- **Space.** $O(T n)$ nodes and $O(n d)$ for the points, which all trees share.

## Variants

- **Rotated data.** Silpa-Anan and Hartley also studied trees built on rotated copies of the data, so that the trees differ by their axes and not only by the random split.
- **Priority search k-means tree.** Muja and Lowe (2009, 2014) offer a tree that splits by k-means clustering, and an automatic choice between the two indexes and their parameters for a given data set and target precision.
- **Random projection trees.** The [RP tree](/rp-tree/) splits on a random direction instead of a coordinate axis.
- **Other indexes.** [Locality-sensitive hashing](/locality-sensitive-hashing/) and graph indexes such as [HNSW](/hnsw/) are the common alternatives in high dimension.
- **Random forests.** The name is shared with the [random forest](/random-forest/) classifier, which also builds trees with random splits, but for a different task.

## When to use it

Use a randomized k-d forest to match many descriptors of moderate dimension, such as 128-value SIFT vectors, when an approximate answer is acceptable and a later step such as the [ratio test](/lowe-ratio-test/) or [RANSAC](/ransac/) removes wrong matches. Set the budget $C$ for the precision you need; Muja and Lowe tune the number of trees and $C$ on a sample of the data. For binary descriptors use Hamming distance and an index made for it, such as multi-probe LSH. For very large sets, graph indexes or product quantization often give a better trade of memory and speed.

## Pitfalls

- **An overestimated key.** The key must not exceed the distance to the bin. In the FLANN code the key of a far child is the parent key plus $\delta^2$, and a comment there says that it does not correct for an earlier split on the same dimension. Such a key can be too large, and a rule that prunes a bin when its key exceeds the current $k$-th distance can then skip a bin that holds a closer point. Line L21 replaces the old offset to avoid this.
- **Counting checks.** A budget in checked points and a budget in reached leaves differ when leaves hold several points or when points are reached in several trees. Report which one you use.
- **Equal points.** A set of equal points has zero variance in every dimension. Keep it in one leaf, or MAKE does not end.
- **Unbalanced trees.** Mean splits on skewed data can give deep trees. A median split keeps the height at $\lceil \log_2 n \rceil$ but changes the trees.
- **Seeds.** The trees depend on the random generator. Fix the seed to make the index and the results repeatable.
- **Distance.** The bin distance is for Euclidean distance. Another metric needs another lower bound.

## Implementations

The Python code in `impl/python/randomized_kd_forest.py` is a class with BUILD, INSERT, SEARCH and a check of the invariant. SEARCH uses the replaced offset of line L21, a set of seen points, a budget in checked points and the exact stop rule of line L17. The tests compare searches with no budget against a brute force scan after random sequences of inserts and queries, check the invariant, check that each point is measured at most once, check that a larger budget never gives a worse answer, and check that the split dimension is among the top $D$ by variance.

## History

Beis and Lowe (1997) introduced [best bin first](/best-bin-first-search/) search in one k-d tree. Silpa-Anan and Hartley (2008) built several k-d trees with random choices and searched them at the same time with one priority queue, for matching image descriptors. Muja and Lowe (2009) chose the split dimension at random among the 5 dimensions of greatest variance, compared the forest with a hierarchical k-means tree, and released both in the FLANN library with an automatic choice of the index and its parameters. Their 2014 journal paper extended this work to larger data sets and to search on a cluster of machines.

## References
