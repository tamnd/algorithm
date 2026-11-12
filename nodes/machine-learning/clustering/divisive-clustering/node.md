---
tag: 9ERGNS
kind: algorithm
slug: divisive-clustering
name: Divisive clustering
aliases:
- top-down clustering
- DIANA
area: machine-learning/clustering
level: advanced
summary: "Top-down hierarchical clustering: start with one cluster and split clusters until each point is alone. DIANA splits off a splinter group at each step."
solves: [hierarchical-clustering-problem]
model: real-ram
complexity:
  vars: {n: the number of points}
  time: {worst: "O(n^3)"}
  space: {extra: "O(n)"}
properties: {deterministic: true, online: false, recursive: false}
history:
  year: 1964
  people: [P. Macnaughton-Smith, Leonard Kaufman, Peter J. Rousseeuw]
  note: Macnaughton-Smith and others (1964) split a group by moving a splinter group out of it. Kaufman and Rousseeuw (1990) made this the program DIANA.
prereqs: [hierarchical-clustering-problem, dendrogram]
see_also: [agglomerative-clustering, bisecting-k-means, single-linkage-clustering, maximum-spacing-k-clustering, complete-linkage-clustering, partitioning-around-medoids, linkage-criterion, k-means]
sources:
  - book: isbn:9780471878766
    title: "Leonard Kaufman and Peter J. Rousseeuw, Finding Groups in Data: An Introduction to Cluster Analysis"
    locator: Chapter 6 (Divisive Analysis, program DIANA), with the count of 2^(n-1) - 1 possible splits of a cluster
  - paper: doi:10.1038/2021034a0
    title: "P. Macnaughton-Smith, W. T. Williams, M. B. Dale and L. G. Mockett, Dissimilarity analysis: a new technique of hierarchical sub-division, Nature 202 (1964), 1034-1035"
    locator: the splitting of a group by a splinter group, built one object at a time
  - book: isbn:9780130222787
    title: Anil K. Jain and Richard C. Dubes, Algorithms for Clustering Data
    locator: Chapter 3 (hierarchical clustering, agglomerative and divisive)
---

Divisive clustering builds a hierarchy from the top down. It starts with all points in one cluster and splits a cluster into two at each step, until each point is alone. The $n - 1$ splits, read in reverse, are the merges of a [dendrogram](/dendrogram/). The best split of a cluster of $m$ points, for most criteria, needs a search over $2^{m-1} - 1$ ways, so practical methods use a heuristic. DIANA, the method of Kaufman and Rousseeuw, splits the cluster with the largest diameter: it starts a *splinter group* with the point that is farthest from the others on average, and moves points into it while they are closer to it than to the rest. It takes $O(n^3)$ time.

## In plain words

Put all items in one group. Take the widest group, and find the item that is the most unlike the others. Take it out and start a new group with it. Then look at the items that are left. If one of them is, on average, more like the new group than like the old one, move it. Go on until no item wants to move. Now the wide group is two groups.

Do this again and again, each time with the widest group, until each item is alone. Each split is a fork in the tree, at the height of the width of the group that was split.

## The problem

The input is an $n \times n$ symmetric dissimilarity matrix $D$ with a zero diagonal. The output is a hierarchy for the [hierarchical clustering problem](/hierarchical-clustering-problem/), as $n - 1$ splits $(S, R, h)$: the cluster $S \cup R$ splits into $S$ and $R$ at height $h$. DIANA uses the diameter $\text{diam}(C) = \max_{i, j \in C} D(i, j)$ as the height, so the heights never increase from a cluster to its parts.

## The algorithm

```pseudo id=main
DIANA(D)
L1  clusters ← {{1, …, n}}
L2  while some cluster has two or more points do
L3      C ← a cluster with two or more points and the largest diameter
L4      (S, R) ← SPLINTER(D, C)
L5      replace C by S and R in clusters
L6      record the split (S, R) at height diam(C)
L7  return the splits

SPLINTER(D, C)
L8  x ← the point of C with the largest mean dissimilarity to the other points of C
L9  S ← {x}, R ← C − {x}
L10 while |R| ≥ 2 do
L11     g(i) ← mean of D(i, j) over j ∈ R − {i}, minus mean of D(i, j) over j ∈ S, for each i ∈ R
L12     y ← the point of R with the largest g(y), the smaller index on a tie
L13     if g(y) ≤ 0 then break
L14     move y from R to S
L15 return (S, R)
```

A point with $g(i) > 0$ is, on average, closer to the splinter group than to the rest. Running sums of $D(i, \cdot)$ over $S$ and over $R$ give each $g(i)$ in $O(1)$ time, and each move updates the sums in $O(m)$ time.

## Example

Take the points $a, b, c, d, e, f$ at $0, 2, 3, 7, 13, 21$ on a line, with $D(x, y) = |x - y|$.

**The first split.** The mean dissimilarities to the others are $a$ 9.2, $b$ 7.6, $c$ 7.2, $d$ 7.2, $e$ 9.6 and $f$ 16, so $f$ starts the splinter group. Then $e$ has $g(e) = (13 + 11 + 10 + 6)/4 - 8 = 2 > 0$, the largest, and moves. With $S = \{e, f\}$, each point of $\{a, b, c, d\}$ has a negative $g$, for example $g(d) = 16/3 - 10$. So the root splits into $\{e, f\}$ and $\{a, b, c, d\}$ at height 21.

| step | split cluster | diameter | splinter group | rest |
|---|---|---|---|---|
| 1 | $\{a, \ldots, f\}$ | 21 | $\{e, f\}$ | $\{a, b, c, d\}$ |
| 2 | $\{e, f\}$ | 8 | $\{e\}$ | $\{f\}$ |
| 3 | $\{a, b, c, d\}$ | 7 | $\{d\}$ | $\{a, b, c\}$ |
| 4 | $\{a, b, c\}$ | 3 | $\{a\}$ | $\{b, c\}$ |
| 5 | $\{b, c\}$ | 1 | $\{b\}$ | $\{c\}$ |

In reverse, the merges are $\{b, c\}$ at 1, $\{a, b, c\}$ at 3, $\{a, b, c, d\}$ at 7, $\{e, f\}$ at 8, and the root at 21. The cut into three clusters is $\{a, b, c, d\}$, $\{e\}$, $\{f\}$, as for single linkage, but the cut into two clusters is $\{a, b, c, d\}$, $\{e, f\}$, unlike single linkage, which keeps $f$ alone.

## Correctness

Two facts make the output a valid hierarchy. First, SPLINTER returns two nonempty parts of $C$: $S$ starts with one point, and the loop of line L10 moves points only while $R$ keeps at least two, so $R$ is never empty. Second, the heights do not increase: each part of a cluster has a diameter at most that of the cluster, so each cluster in the list has a diameter at most the height of the last split, and the next split is at most that height. Each split makes one more cluster, so after $n - 1$ splits each point is alone. The reverse of the splits is a monotone list of merges. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

- **SPLINTER.** For a cluster of $m$ points, the start takes $O(m^2)$ time, and each of at most $m - 2$ moves takes $O(m)$ time with running sums. So one split takes $O(m^2)$ time.
- **Total.** There are $n - 1$ splits. A scan of all current clusters for the diameters of line L3 takes $O(n^2)$ time per round, and the split itself takes $O(n^2)$, so the total is $O(n^3)$. When each split cuts off one point, the splits alone cost $\sum_m \Theta(m^2) = \Theta(n^3)$.
- **Memory.** The matrix is the input. Beyond it, the sums and the clusters take $O(n)$ space.
- **The exact best split.** For a fixed criterion, the best split of $m$ points needs, in general, a search over all $2^{m-1} - 1$ splits into two nonempty parts. For the sum of squares, this best split is NP-hard in a general dimension.

## Properties

- **Monotone.** The heights never increase from a cluster to its parts, so the tree has no inversions.
- **Top levels first.** The first splits are the large-scale structure. A user who needs only a few clusters can stop early, which saves the work of the fine splits.
- **Greedy.** Each split is fixed once made. A wrong split near the top cannot be undone.
- **Not the reverse of an agglomerative method.** DIANA and the agglomerative methods can give different trees on the same data, as the example shows.
- **Divisive coefficient.** Kaufman and Rousseeuw define a coefficient from the heights at which each point is split off, to measure how strong the structure is.

## Variants and improvements

- **[Bisecting k-means](/bisecting-k-means/).** Split the chosen cluster by 2-means, a few times from different starts, and keep the best result. It is fast on large sets of vectors.
- **Split by a minimum spanning tree.** Cut the largest edge of a [minimum spanning tree](/minimum-spanning-tree/) of the cluster. This split has the largest gap between the parts, as in [maximum-spacing clustering](/maximum-spacing-k-clustering/), and the top-down tree is the single linkage tree.
- **Monothetic splits.** For binary attributes, split on one attribute at a time. Kaufman and Rousseeuw give this as MONA.
- **Other choices of the cluster to split.** Split the cluster with the largest size, the largest sum of squares, or the lowest quality, in place of the largest diameter.
- **Spectral splits.** Split by the sign of the second eigenvector of a graph Laplacian, which is a heuristic for a sparsest cut.

## When to use it

Use divisive clustering when the top of the hierarchy matters most, for example when only a few large groups are needed, or when the data has a clear large-scale structure. Agglomerative methods make their first choices among the smallest clusters, so a small error can spread up the tree. A divisive method makes its first choice on all the data. For large sets of vectors, bisecting k-means is the usual choice.

## Pitfalls

- **Exponential search.** Do not try all splits of a large cluster. Even for 30 points, there are more than $5 \times 10^8$.
- **Ties.** With equal mean dissimilarities, the start point and the order of moves depend on the rule for ties.
- **Heights.** DIANA uses the diameter as the height. Other divisive methods use other values, which can be not monotone.
- **The cost of the bottom.** The splits near the leaves cost much time and add little. Stop at the needed number of clusters if the full tree is not needed.

## Implementations

## History

Macnaughton-Smith, Williams, Dale and Mockett (1964) split a group by a splinter group, moved one object at a time. Edwards and Cavalli-Sforza (1965) split by the least sum of squares, with a search over all splits. Kaufman and Rousseeuw (1990) gave the method as the program DIANA, with the diameter as the height and the choice of the widest cluster at each step. Steinbach, Karypis and Kumar (2000) made bisecting k-means popular for documents.

## References
