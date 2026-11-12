---
tag: 9E03GX
kind: definition
slug: ultrametric
name: Ultrametric
aliases:
- ultrametric space
area: machine-learning/clustering
level: intro
summary: "A distance with d(x, z) at most max(d(x, y), d(y, z)) for all x, y, z. On a finite set, ultrametrics are the same as monotone dendrograms."
prereqs: [metric-space, dendrogram]
see_also: [single-linkage-clustering, hierarchical-clustering-problem, tree-metric, ultrametric-tree-reconstruction, upgma, minimum-bottleneck-spanning-tree, frt-tree-embedding]
sources:
  - paper: doi:10.1007/BF02289588
    title: "Stephen C. Johnson, Hierarchical clustering schemes, Psychometrika 32(3) (1967), 241-254"
    locator: the ultrametric inequality and the one-to-one match between hierarchical clustering schemes and ultrametrics
  - paper: "Gunnar Carlsson and Facundo Mémoli, Characterization, stability and convergence of hierarchical clustering methods, Journal of Machine Learning Research 11 (2010), 1425-1470"
    locator: the equivalence of dendrograms and ultrametrics, and single linkage as the subdominant ultrametric
  - paper: doi:10.1103/RevModPhys.58.765
    title: "R. Rammal, G. Toulouse and M. A. Virasoro, Ultrametricity for physicists, Reviews of Modern Physics 58(3) (1986), 765-788"
    locator: the properties of ultrametric spaces and the subdominant ultrametric from the minimum spanning tree
  - book: isbn:9780130222787
    title: Anil K. Jain and Richard C. Dubes, Algorithms for Clustering Data
    locator: Chapter 3, Section 3.2 (the cophenetic matrix and the ultrametric inequality)
---

## Definition

Let $X$ be a set and $u : X \times X \to \mathbb{R}_{\ge 0}$ a function with $u(x, x) = 0$ and $u(x, y) = u(y, x)$. Then $u$ is an **ultrametric** if, for all $x, y, z \in X$,

$$u(x, z) \le \max\bigl(u(x, y),\ u(y, z)\bigr).$$

This is the *ultrametric inequality*, or the strong triangle inequality. It implies the triangle inequality, because $\max(a, b) \le a + b$ for $a, b \ge 0$. If also $u(x, y) > 0$ for all $x \ne y$, then $(X, u)$ is a [metric space](/metric-space/), called an **ultrametric space**. In clustering, $u(x, y) = 0$ for $x \ne y$ is often allowed, and $u$ is then a pseudo-ultrametric.

Three facts follow at once from the inequality.

- **Isosceles triangles.** In each triangle the two largest sides are equal. If $u(x, y) \le u(y, z) \le u(x, z)$, the inequality for $x, z$ gives $u(x, z) \le u(y, z)$, so $u(x, z) = u(y, z)$.
- **Threshold classes.** For each $t \ge 0$, the relation $u(x, y) \le t$ is an equivalence relation. Transitivity is the inequality itself. The classes for a larger $t$ are unions of the classes for a smaller $t$.
- **Nested balls.** Each point of a closed ball $\{y : u(x, y) \le t\}$ is a center of it, and two balls are either disjoint or one contains the other.

**Ultrametrics are dendrograms.** On a finite set $X$, the map $u \mapsto (t \mapsto \text{the classes of } u \le t)$ is a bijection from the ultrametrics on $X$ to the monotone [dendrograms](/dendrogram/) on $X$ that merge equal heights into one node. The inverse map sends a dendrogram to its cophenetic distance: the height of the lowest common ancestor of two leaves. One direction is the threshold fact above. For the other, the lowest common ancestors $\text{lca}(x, y)$ and $\text{lca}(y, z)$ are both on the path from $y$ to the root, so the higher of the two is above $x$, $y$ and $z$, and monotone heights give the inequality. The code of the [dendrogram](/dendrogram/) page checks this bijection on all matrices with values in $\{1, 2, 3\}$ for up to four points.

**The subdominant ultrametric.** For a dissimilarity $d$ on a finite set, there is a largest ultrametric $u^*$ with $u^* \le d$ at each pair. It is the minimax path distance

$$u^*(x, y) = \min_{\text{paths } x = p_0, p_1, \ldots, p_m = y} \ \max_{1 \le i \le m} d(p_{i-1}, p_i),$$

which is the largest edge on the path from $x$ to $y$ in a [minimum spanning tree](/minimum-spanning-tree/), and the cophenetic distance of [single linkage](/single-linkage-clustering/). It is an ultrametric because two paths join into one path. It is at most $d$ because the single edge $x, y$ is a path. Each ultrametric $u \le d$ gives, by the inequality along a path, $u(x, y) \le \max_i u(p_{i-1}, p_i) \le \max_i d(p_{i-1}, p_i)$, so $u \le u^*$.

## Examples and non-examples

- **Cophenetic distances.** Single linkage on the points $0, 2, 3, 7, 13, 21$ of a line, named $a$ to $f$, gives $u(b, c) = 1$, $u(a, b) = u(a, c) = 2$, $u(d, x) = 4$ for $x \in \{a, b, c\}$, $u(e, x) = 6$ for $x \in \{a, b, c, d\}$, and $u(f, x) = 8$ for the other five points. Each triangle has two equal largest sides, for example $u(a, d) = u(c, d) = 4 \ge u(a, c) = 2$. Each value is at most the distance on the line.
- **Equal-depth trees.** The leaves of a rooted tree with edge lengths, where each leaf is at the same distance from the root, form an ultrametric under the path distance. The distance of two leaves is twice the height of their lowest common ancestor above the leaves. Such trees are called ultrametric trees. [UPGMA](/upgma/) builds one from a distance matrix.
- **The p-adic distance.** On the rational numbers, $|x - y|_p = p^{-v}$, where $p^v$ is the largest power of the prime $p$ that divides $x - y$, is an ultrametric.
- **The discrete metric.** $u(x, y) = 1$ for $x \ne y$ is an ultrametric. Its dendrogram has one node with all points as children.
- **Not an ultrametric: points on a line.** The points $0, 1, 2$ with $|x - y|$ have $u(0, 2) = 2 > \max(1, 1)$. The triangle inequality holds, but the strong one fails.
- **Not an ultrametric: an inversion.** Centroid linkage, with squared Euclidean distances, on the corners of an equilateral triangle of side $1$ merges two corners at height $1$ and then the third at height $3/4$. The cophenetic values $1, 3/4, 3/4$ have the largest side $1$ alone, so they break the inequality.

## Related definitions

- [Metric space](/metric-space/): a set with a distance that satisfies the triangle inequality. Each ultrametric with positive distances is one.
- [Tree metric](/tree-metric/): a distance that is the path distance of a tree with edge lengths. It satisfies the four-point condition, and each ultrametric is a tree metric.
- [Dendrogram](/dendrogram/): the tree form of an ultrametric on a finite set.
- **Cophenetic distance:** the ultrametric that a monotone dendrogram puts on its leaves.
- **Subdominant ultrametric:** the largest ultrametric below a given dissimilarity, made by single linkage. [Ultrametric tree reconstruction](/ultrametric-tree-reconstruction/) asks for the ultrametric closest to a given one in other senses.
- [Minimum bottleneck spanning tree](/minimum-bottleneck-spanning-tree/): the minimax path value on a graph, which is the subdominant ultrametric on its vertices.

## References
