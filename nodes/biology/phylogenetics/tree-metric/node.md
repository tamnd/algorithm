---
tag: CB9NAY
kind: definition
slug: tree-metric
name: Tree metric
aliases:
- additive metric
- additive distance
area: biology/phylogenetics
level: core
summary: A metric on a finite set that equals the path length between the points in some tree with positive edge lengths. It is the exact distance model of distance-based phylogenetics.
prereqs: [metric-space, tree]
see_also: [four-point-condition, additive-tree-reconstruction, ultrametric, neighbor-joining, four-point-method, splits-of-a-tree, metric-tree-embedding, phylogenetic-tree]
sources:
  - book: isbn:9780198509424
    title: Charles Semple and Mike Steel, Phylogenetics, 2003
    locator: Section 7.2, Definition 7.2.1 (tree metric) and Theorem 7.2.6 (the tree-metric theorem)
  - paper: doi:10.1016/0095-8956(74)90047-1
    title: Peter Buneman, A note on the metric properties of trees, Journal of Combinatorial Theory, Series B 17(1), 1974, pages 48 to 50
    locator: the four-point characterization of tree metrics
  - paper: "J. M. S. Simões-Pereira, A note on the tree realizability of a distance matrix, Journal of Combinatorial Theory 6(3), 1969"
    title: Simões-Pereira 1969
    locator: pages 303 to 310, tree realizations of a distance matrix and their uniqueness
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, 2004
    locator: Chapter 11, Distance matrix methods, additive trees and the additivity of distances on a tree
  - book: isbn:9781107184718
    title: Tandy Warnow, Computational Phylogenetics, Cambridge University Press, 2017
    locator: Chapter 5, distance-based tree estimation, additive matrices
---

A tree metric is a distance on a finite set of points that is the path length between them in some [tree](/tree/) with positive edge lengths. In phylogenetics the points are taxa at the leaves of a [phylogenetic tree](/phylogenetic-tree/), and a tree metric is what an ideal evolutionary distance would be: the sum of the branch lengths between two taxa. The [four-point condition](/four-point-condition/) tells exactly which metrics are tree metrics, and the tree is then unique. Matrices of tree metrics are also called additive matrices.

## Definition

Let $X$ be a finite set and $D$ a [metric](/metric-space/) on $X$. $D$ is a **tree metric** if there are a tree $T$ with $X \subseteq V(T)$ and a length $\ell(e) > 0$ for each edge $e$ such that, for all $x, y \in X$,
$$D(x, y) = \sum_{e \in P_{xy}} \ell(e),$$
where $P_{xy}$ is the set of edges on the path from $x$ to $y$ in $T$. The pair $(T, \ell)$ is a **realization** of $D$. It is **minimal** if every vertex of $T$ that is not in $X$ has degree at least 3. Every realization becomes minimal after removing leaves not in $X$ (with their edges) and suppressing vertices of degree 2 not in $X$ (joining their two edges into one, with the lengths added); this does not change any distance between points of $X$.

**Characterization and uniqueness.** By the [four-point condition](/four-point-condition/) theorem (Buneman 1974), $D$ is a tree metric if and only if, for all $x, y, z, w \in X$,
$$D(x, y) + D(z, w) \le \max\bigl(D(x, z) + D(y, w),\ D(x, w) + D(y, z)\bigr),$$
and then its minimal realization is unique up to an isomorphism that fixes $X$ and keeps lengths.

**Phylogenetic case.** When $X$ is the set of leaves of $T$ and $T$ has no vertex of degree 2, the realization is an unrooted phylogenetic tree with branch lengths, and $D$ is its **leaf metric**. A tree metric in which some points of $X$ are internal vertices or vertices of degree 2 corresponds to a tree in which some taxa are ancestors of others, or to branch lengths of 0 after the taxa are moved to new leaves.

Some texts allow lengths $\ell(e) \ge 0$; then the realization is unique only after edges of length 0 are contracted, and $D$ may be a pseudometric.

## Examples and non-examples

- **A leaf metric.** The tree `((A:2,B:7):1,E:5,(C:3,D:6):2);` gives $D(A, B) = 9$, $D(A, C) = 2 + 1 + 2 + 3 = 8$, $D(B, D) = 7 + 1 + 2 + 6 = 16$, and so on; the matrix is on the page of the [four-point condition](/four-point-condition/), where each of its five quartets passes the test.
- **Every metric on three points.** For $X = \{x, y, z\}$ the star with a center $c$ and edges of lengths $\frac{1}{2}(D(x, y) + D(x, z) - D(y, z))$ and the two similar values realizes $D$. The triangle inequality makes the lengths at least 0; a length of 0 puts the point at the center.
- **Ultrametrics.** Each [ultrametric](/ultrametric/) is a tree metric, realized by a rooted tree whose root is at the same distance from every point. A tree metric on the leaves of its realization is an ultrametric exactly when some point of the realization is at the same distance from all points of $X$; most tree metrics are not.
- **Path metrics on a line.** Points $x_1 < x_2 < \cdots < x_n$ on the real line with $D(x_i, x_j) = |x_i - x_j|$ form a tree metric, realized by a path.
- **Not a tree metric: the 4-cycle.** Four points with $D = 1$ between neighbors on a cycle and $D = 2$ across. The three pair sums are $2$, $4$ and $2$, so the largest one is alone and the four-point condition fails.
- **Not a tree metric: a perturbed tree.** The matrix with $D(A, B) = 2$, $D(A, C) = D(A, D) = D(B, C) = 6$, $D(B, D) = 9$, $D(C, D) = 4$ has pair sums $6$, $15$ and $12$. It is close to the tree with split AB|CD, but no tree realizes it exactly; [least squares](/least-squares-phylogeny/) methods fit such data.
- **Not a tree metric: the plane.** Four corners of a unit square in the Euclidean plane have pair sums $2$, $2$ and $2\sqrt{2}$, so the largest is alone.

## Related definitions

- **[Four-point condition](/four-point-condition/):** the test on quartets that characterizes tree metrics, with the proof of the theorem and of uniqueness.
- **[Ultrametric](/ultrametric/):** the special case of a rooted realization with all points at the same height, characterized by the three-point condition $D(x, z) \le \max(D(x, y), D(y, z))$.
- **[Splits of a tree](/splits-of-a-tree/):** each edge $e$ of the minimal realization splits $X$ into two parts, and $D = \sum_e \ell(e)\, \delta_e$, where $\delta_e(x, y) = 1$ when $e$ separates $x$ from $y$. Tree metrics are exactly the nonnegative combinations of split metrics of pairwise compatible splits; [split decomposition](/split-decomposition/) extends this to more general metrics.
- **[Additive tree reconstruction](/additive-tree-reconstruction/):** the problem of finding the realization from $D$, exactly or approximately.
- **[Metric tree embedding](/metric-tree-embedding/):** the approximation of a general metric by a tree metric with bounded distortion, as in the [FRT embedding](/frt-tree-embedding/).
- **Additive distances in biology.** An evolutionary distance is additive when it equals the sum of the branch lengths along the path; distances corrected with a [substitution model](/substitution-model/), such as the [Jukes-Cantor model](/jukes-cantor-model/), aim at this property.

## References
