---
tag: G4DBR6
kind: algorithm
slug: ward-method
name: Ward's method
aliases:
- Ward linkage
- Ward's minimum variance
area: machine-learning/clustering
level: core
summary: "Agglomerative clustering that merges the two clusters whose union increases the within-cluster sum of squares the least: (n_i n_j/(n_i+n_j))|c_i-c_j|^2."
solves: [hierarchical-clustering-problem]
model: real-ram
complexity:
  vars: {n: the number of points, d: the dimension}
  time: {worst: "Θ(n^3 d)"}
  space: {extra: "Θ(n d)"}
properties: {deterministic: true, online: false, recursive: false}
history:
  year: 1963
  people: [Joe H. Ward Jr., David Wishart]
  note: Ward (1963) proposed merging the groups that lose the least value of an objective, with the error sum of squares as the main case. Wishart (1969) gave its Lance-Williams update.
prereqs: [agglomerative-clustering]
see_also: [k-means-problem, k-means, lance-williams-formula, nearest-neighbor-chain, bisecting-k-means, linkage-criterion, complete-linkage-clustering, euclidean-distance]
sources:
  - paper: doi:10.1080/01621459.1963.10500845
    title: "Joe H. Ward Jr., Hierarchical grouping to optimize an objective function, Journal of the American Statistical Association 58(301) (1963), 236-244"
    locator: the stepwise grouping that loses the least value of an objective, with the error sum of squares as the example
  - paper: doi:10.2307/2528688
    title: "David Wishart, An algorithm for hierarchical classifications, Biometrics 25(1) (1969), 165-170"
    locator: the update of Ward's criterion by the Lance-Williams recurrence
  - paper: doi:10.1007/s00357-014-9161-z
    title: "Fionn Murtagh and Pierre Legendre, Ward's hierarchical agglomerative clustering method: which algorithms implement Ward's criterion?, Journal of Classification 31(3) (2014), 274-295"
    locator: the input of squared distances, and the two Ward options of R (ward.D and ward.D2)
  - url: https://arxiv.org/abs/1109.2378
    title: "Daniel Müllner, Modern hierarchical, agglomerative clustering algorithms, arXiv:1109.2378 (2011)"
    locator: Section 2 (the Ward update on squared Euclidean distances and the reported heights)
  - book: isbn:9780130222787
    title: Anil K. Jain and Richard C. Dubes, Algorithms for Clustering Data
    locator: Chapter 3, Section 3.2 (Ward's method as the minimum variance method)
---

Ward's method is [agglomerative clustering](/agglomerative-clustering/) for points in $\mathbb{R}^d$ that, at each step, merges the two clusters whose union increases the total within-cluster sum of squares the least. The increase for clusters $i$ and $j$, with sizes $n_i$, $n_j$ and centroids $c_i$, $c_j$, is

$$\Delta(i, j) = \frac{n_i n_j}{n_i + n_j} \lVert c_i - c_j \rVert^2.$$

So the method needs only the sizes and the centroids, and it is the greedy, bottom-up form of the [k-means objective](/k-means-problem/). Its clusters are compact and of similar size. The direct form takes $\Theta(n^3 d)$ time and $\Theta(n d)$ memory. On a matrix of squared distances, the [Lance-Williams formula](/lance-williams-formula/) updates the values, and since the method is reducible, the [nearest-neighbor chain](/nearest-neighbor-chain/) runs it in $O(n^2)$ time. A cut of the tree is not an optimal k-means partition in general.

## In plain words

Measure how spread out a group is: add up, over its items, the square of the distance to the middle of the group. Add these sums over all groups. At the start each item is alone, so the total is zero.

Each join of two groups makes the total grow. At each step, make the join that makes it grow the least. The growth is easy to get. It is large when the two middles are far apart, and also when both groups are large. So two big groups join late, and small groups join early.

The final tree tends to have round groups of similar size.

## The problem

The input is $n$ points $p_1, \ldots, p_n$ of $\mathbb{R}^d$. For a cluster $A$ with centroid $c_A$, let $\text{SSE}(A) = \sum_{p \in A} \lVert p - c_A \rVert^2$. The output is the $n - 1$ merges of the greedy rule that merges the two current clusters $A$, $B$ with the smallest increase $\text{SSE}(A \cup B) - \text{SSE}(A) - \text{SSE}(B)$, with that increase as the height. It solves the [hierarchical clustering problem](/hierarchical-clustering-problem/) for the Ward linkage.

## The algorithm

Each active slot keeps the centroid and the size of its cluster. Lines L3 and L4 compute the increase for each pair from these values, and line L5 makes the centroid of the union as the weighted mean.

```pseudo id=main
WARD(P)                               ▷ P holds n points of R^d
L1  c[i] ← P[i], size[i] ← 1 for each i, active ← {1, …, n}
L2  while |active| > 1 do
L3      for each pair i, j of active slots do
L4          keep the pair with the least Δ = size[i] size[j] / (size[i] + size[j]) · ‖c[i] − c[j]‖²
L5      c[i] ← (size[i] c[i] + size[j] c[j]) / (size[i] + size[j])
L6      append (i, j, Δ) to merges
L7      size[i] ← size[i] + size[j], remove j from active
L8  return merges
```

**The matrix form.** Store $D[i, j] = \Delta(i, j)$ for all pairs, which is half the squared distance for two single points. After a merge, the Lance-Williams row for Ward,

$$D[k, i \cup j] = \frac{n_i + n_k}{n_i + n_j + n_k} D[k, i] + \frac{n_j + n_k}{n_i + n_j + n_k} D[k, j] - \frac{n_k}{n_i + n_j + n_k} D[i, j],$$

gives the new values without the points. This form runs with the heap or the nearest-neighbor chain.

## Example

Take the points $a, b, c, d, e, f$ at $0, 2, 3, 7, 13, 21$ on a line.

| step | merge | height $\Delta$ | runner-up |
|---|---|---|---|
| 1 | $b$, $c$ | $\frac{1}{2} \cdot 1^2 = 1/2$ | $a$, $b$ at $2$ |
| 2 | $a$, $\{b, c\}$ | $\frac{2}{3} (0 - 5/2)^2 = 25/6$ | $d$, $\{b, c\}$ at $27/2$ |
| 3 | $d$, $e$ | $\frac{1}{2} \cdot 6^2 = 18$ | $d$, $\{a, b, c\}$ at $64/3$ |
| 4 | $f$, $\{d, e\}$ | $\frac{2}{3} (21 - 10)^2 = 242/3$ | $\{a, b, c\}$, $\{d, e\}$ at $250/3$ |
| 5 | $\{a, b, c\}$, $\{d, e, f\}$ | $\frac{9}{6} (5/3 - 41/3)^2 = 216$ | |

The heights add up to $1/2 + 25/6 + 18 + 242/3 + 216 = 958/3$, which is the sum of squares of all six points about their mean $23/3$. The cut into two clusters is $\{a, b, c\}$, $\{d, e, f\}$, unlike single and complete linkage, which keep $f$ alone. Step 4 is close: $242/3$ against $250/3$.

**Not an optimal k-means partition.** On the points $0, 1, 2, 3, 5$, Ward's method makes $\{0, 1, 2, 3\}$ before it joins 5, so its cut into two clusters is $\{0, 1, 2, 3\}$, $\{5\}$ with a sum of squares of $5$. The partition $\{0, 1, 2\}$, $\{3, 5\}$ has a sum of squares of $2 + 2 = 4$.

## Correctness

The key fact is the identity for the increase. By the parallel axis rule, $\sum_{p \in S} \lVert p - z \rVert^2 = \text{SSE}(S) + |S| \lVert c_S - z \rVert^2$ for each point $z$. Apply it to $A$ and $B$ with $z$ the centroid of $A \cup B$, which is $(n_A c_A + n_B c_B)/(n_A + n_B)$. The two extra terms add up to $\frac{n_A n_B}{n_A + n_B} \lVert c_A - c_B \rVert^2$. So line L4 computes the exact increase, line L5 the exact new centroid, and the loop follows the greedy rule. The heights add up to $\text{SSE}$ of all points, because the increases telescope from $0$. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

- **Direct form.** Each round scans $O(n^2)$ pairs at $O(d)$ each, so $n - 1$ rounds take $\Theta(n^3 d)$ time. The memory is $\Theta(n d)$ for the centroids.
- **Matrix form.** With the Lance-Williams row, the naive loop takes $\Theta(n^3)$ time after $\Theta(n^2 d)$ time to build the matrix, and $\Theta(n^2)$ memory. The heap version takes $O(n^2 \log n)$ time.
- **Nearest-neighbor chain.** Ward's linkage is reducible, so the [nearest-neighbor chain](/nearest-neighbor-chain/) gives the same tree in $O(n^2)$ time on the matrix, or in $O(n^2 d)$ time and $O(n d)$ memory with centroids.

## Properties

- **Monotone.** Ward's linkage is reducible, so the heights never decrease.
- **The heights add up to the total sum of squares.** The cut into $k$ clusters has the sum of squares of the merges that it keeps.
- **Greedy for k-means.** Each merge is the best single step for the k-means objective, but the cut at $k$ is not always the best k-means partition, as the example shows.
- **Euclidean only.** The method needs centroids, so it assumes points in $\mathbb{R}^d$ with the [Euclidean distance](/euclidean-distance/). On other dissimilarities, the update formula still runs but has no sum of squares meaning.
- **Similar sizes.** The factor $n_i n_j/(n_i + n_j)$ grows with both sizes, which delays merges of two large clusters and favors clusters of similar size.

## Variants and improvements

- **Ward's general scheme.** Ward (1963) stated the method for any objective function that is a sum over the groups. The sum of squares is the case that everyone uses.
- **Nearest-neighbor chain.** The fastest exact method, in $O(n^2)$ time.
- **Ward as a start for [k-means](/k-means/).** Use the centroids of a Ward cut as the start of Lloyd's algorithm. The result is at least as good as the Ward cut.
- **[Bisecting k-means](/bisecting-k-means/).** A divisive method for the same objective, which splits the cluster with the largest sum of squares by 2-means.
- **Constrained Ward.** Allow only merges of neighbors in a graph, for example adjacent regions of an image or of a map.

## When to use it

Use Ward's method for points in a Euclidean space when you expect compact clusters of similar size, and when you want a hierarchy with the k-means objective at each level. It is the common default for numeric data in many fields, and the default linkage of scikit-learn. Do not use it for clusters with long or uneven shapes, where single linkage or density methods are better, or for dissimilarities that are not Euclidean.

## Pitfalls

- **Squared distances.** The Lance-Williams row is exact only on squared Euclidean distances (or their half). With plain distances, the update computes a different method. In R, `ward.D` on plain distances is this mistake, and `ward.D2` squares them first.
- **The reported heights.** SciPy reports $\sqrt{2 \Delta}$ as the height of a Ward merge, so that two single points merge at their plain distance. Other tools report $\Delta$ or $2\Delta$. Know the scale before you cut at a height or compare tools.
- **Not the k-means optimum.** Do not use a Ward cut as the solution of the k-means problem without a check. A few Lloyd steps can improve it.
- **Exact arithmetic for ties.** The increases of two pairs are often equal in integer data. With floating point, rounding can break such ties in a way that depends on the order of the input.

## Implementations

## History

Ward (1963) proposed hierarchical grouping in which each step loses the least value of an objective function, and used the error sum of squares as the main example. Wishart (1969) showed that the method fits the Lance-Williams recurrence. Murtagh (1983) noted that it is reducible, which gives $O(n^2)$ time by reciprocal nearest neighbors. Murtagh and Legendre (2014) explained why different programs called Ward give different trees: some of them use plain distances where squared distances are needed.

## References
