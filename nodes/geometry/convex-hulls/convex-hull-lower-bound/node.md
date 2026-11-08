---
tag: T6J9NW
kind: theorem
slug: convex-hull-lower-bound
name: Convex hull lower bound
aliases:
- Omega(n log n) convex hull bound
- Omega(n log n) lower bound for convex hull
- sorting reduces to convex hull
area: geometry/convex-hulls
level: advanced
summary: Computing the convex hull requires Omega(n log n) in the algebraic decision tree model, by reduction from sorting.
prereqs: [convex-hull-problem, sorting-problem, algebraic-computation-tree, ben-or-theorem, element-distinctness-lower-bound]
see_also: [convex-hull-output-sensitive-lower-bound, andrew-monotone-chain, graham-scan, comparison-sort-lower-bound, reduction-lower-bound, algebraic-decision-tree, real-ram, paraboloid-lifting-map]
sources:
  - paper: doi:10.1145/322276.322289
    title: Andrew Chi-Chih Yao, A lower bound to finding convex hulls, Journal of the ACM 28(4), 1981
    locator: the main theorem (identifying the hull vertices needs Omega(n log n) quadratic tests)
  - paper: doi:10.1145/800061.808735
    title: "Michael Ben-Or, Lower bounds for algebraic computation trees, Proceedings of the 15th Annual ACM Symposium on Theory of Computing (STOC 1983), 80-86"
    locator: the main theorem and its applications to problems of computational geometry
  - paper: doi:10.1016/0196-6774(82)90002-5
    title: "J. Michael Steele and Andrew C. Yao, Lower bounds for algebraic decision trees, Journal of Algorithms 3(1) (1982), 1-8"
    locator: the main theorem (algebraic decision trees of fixed degree)
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 3, Convex hulls, basic algorithms (the reduction from sorting to the ordered hull and the discussion of the lower bound)
---

The convex hull lower bound says that computing the [convex hull](/convex-hull/) of $n$ points in the plane takes $\Omega(n \log n)$ operations in the algebraic models of computation, so [Graham's scan](/graham-scan/) and [Andrew's monotone chain](/andrew-monotone-chain/) are optimal. There are two versions. The ordered hull, the vertices in counterclockwise order, is at least as hard as [sorting](/sorting-problem/): put the numbers on the parabola $y = x^2$ and read the sorted order off the hull. The unordered question, which points are vertices, is at least as hard as [element distinctness](/element-distinctness-lower-bound/), and [Ben-Or's theorem](/ben-or-theorem/) gives $\Omega(n \log n)$ for it too.

## Statement

**Models.** An [algebraic computation tree](/algebraic-computation-tree/) on input $z \in \mathbb{R}^m$ has computation nodes with $+, -, \times, \div, \sqrt{\ }$ on inputs, constants and earlier values, binary branch nodes that test $u > 0$, $u \ge 0$ or $u = 0$ for an earlier value $u$, and leaves. Its *height* is the largest number of computation and branch nodes on a root-to-leaf path, the worst-case cost with unit cost per operation. A program on the [real RAM](/real-ram/) without the floor function and without indirect addressing by real values unfolds, for each $n$, into such a tree whose height is its worst-case running time. An [algebraic decision tree](/algebraic-decision-tree/) of degree $k$ branches three ways on the sign of a polynomial of degree at most $k$ in the inputs and has no computation nodes.

The input is a list of $n$ points $p_1, \ldots, p_n$, given as $2n$ real coordinates.

**Theorem 1 (ordered hull).** Let $n \ge 3$. Let $T$ be a tree with binary branching (for example an algebraic computation tree) whose leaves are labelled with sequences of indices in $\{1, \ldots, n\}$. Suppose that for every input of $n$ distinct points in convex position, the leaf reached is labelled with the indices of the hull vertices in counterclockwise order, starting at any vertex. Then $T$ has a path with at least $\lg((n-1)!) \ge n \lg n - n \lg e - \lg n$ branch nodes. With three-way branching, as in an algebraic decision tree, the bound is $\log_3((n-1)!)$.

**Theorem 2 (extreme points).** Let $\mathrm{EXT}_n \subseteq \mathbb{R}^{2n}$ be the set of inputs whose $n$ points are pairwise distinct and are all vertices of their convex hull.

1. Every valid algebraic computation tree that decides $\mathrm{EXT}_n$ has height at least $(\lg n! - n \lg 3)/\lg 18 - n$.
2. For each fixed $k$, every algebraic decision tree of degree $k$ that decides $\mathrm{EXT}_n$ has height $\Omega(n \log n)$, with the constant depending on $k$.

So computing the number of hull vertices, or deciding whether all input points are hull vertices, takes $\Omega(n \log n)$ time even when the order of the vertices is not needed.

## In plain words

Put numbers on a bowl-shaped curve, one point for each number. Every point is then a corner of the hull, and walking around the hull visits the points from left to right. So a hull program also sorts, and sorting needs about one step for each bit of the answer. There are many possible orders, so the answer has many bits, which gives a cost that grows like the number of points times its logarithm.

Even a program that only says whether every point is a corner must do this much work. On the bowl, two points fall on top of each other exactly when two numbers are equal. So the program can test whether all numbers are different, and that test is known to need the same cost.

## Proof

**The parabola.** For reals $x_1, \ldots, x_n$ put $p_i = (x_i, x_i^2)$. If the $x_i$ are pairwise distinct, each $p_i$ is a vertex of $\mathrm{conv}\{p_1, \ldots, p_n\}$: the linear function $\ell_i(x, y) = y - 2 x_i x$ takes the value $(x - x_i)^2 - x_i^2$ on the parabola, so on the points $p_j$ it has its unique minimum at $p_i$, and $p_i$ is not a [convex combination](/convex-combination/) of the other points. Order the indices so that $x_{\sigma(1)} < \cdots < x_{\sigma(n)}$. Then the counterclockwise order of the hull is $p_{\sigma(1)}, p_{\sigma(2)}, \ldots, p_{\sigma(n)}$ up to a cyclic rotation: for $j < k < l$, $\mathrm{orient}(p_{\sigma(j)}, p_{\sigma(k)}, p_{\sigma(l)})$ has the sign of $(x_k - x_j)(x_l - x_j)(x_l - x_k) > 0$ (writing $x_j$ for $x_{\sigma(j)}$), so each triple in this order turns left.

**Proof of Theorem 1.** Restrict $T$ to the inputs $(x_1, x_1^2, \ldots, x_n, x_n^2)$ with distinct $x_i$. These are inputs of distinct points in convex position, so for each such input the label of its leaf is a rotation of $\sigma(1), \ldots, \sigma(n)$. A fixed label is a rotation of the sorted order for at most $n$ permutations $\sigma$, one for each starting point. All $n!$ permutations occur as sorted orders of some input, so $T$ has at least $n!/n = (n-1)!$ leaves. A binary tree whose paths have at most $b$ branch nodes has at most $2^b$ leaves, since computation nodes do not branch, so $b \ge \lg((n-1)!)$. From $n! \ge (n/e)^n$ we get $\lg((n-1)!) = \lg n! - \lg n \ge n \lg n - n \lg e - \lg n$. With three-way branching the count gives $3^b \ge (n-1)!$. $\square$

**Proof of Theorem 2, part 1.** Let $T$ be a valid algebraic computation tree of height $h$ that decides $\mathrm{EXT}_n$. Build a tree $T'$ on input $x \in \mathbb{R}^n$: it first computes $y_i = x_i \times x_i$ for $i = 1, \ldots, n$ with $n$ computation nodes, and then runs $T$ on $(x_1, y_1, \ldots, x_n, y_n)$. $T'$ is valid, because $T$ is valid on every input in $\mathbb{R}^{2n}$, and it has height at most $h + n$.

$T'$ decides the set $W = \{x \in \mathbb{R}^n : x_i \ne x_j \text{ for all } i \ne j\}$. If the $x_i$ are distinct, the points $p_i$ are distinct and all are vertices by the parabola paragraph, so the input is in $\mathrm{EXT}_n$. If $x_i = x_j$ for some $i \ne j$, then $p_i = p_j$ and the input is not in $\mathrm{EXT}_n$.

The set $W$ has exactly $n!$ connected components. For each permutation $\sigma$ the set $W_\sigma = \{x : x_{\sigma(1)} < \cdots < x_{\sigma(n)}\}$ is convex, hence connected, and $W$ is the disjoint union of these $n!$ sets. Two points of different sets $W_\sigma \ne W_\tau$ have some pair $i, j$ in opposite orders, and on any path between them the continuous function $x_i - x_j$ changes sign, so it is $0$ somewhere and the path leaves $W$. So the $W_\sigma$ are the components.

By [Ben-Or's theorem](/ben-or-theorem/) applied to $T'$ with $C = \mathrm{cc}(W) = n!$, we get $h + n \ge (\lg n! - n \lg 3)/\lg 18$. $\square$

**Proof of Theorem 2, part 2.** In a degree-$k$ algebraic decision tree for $\mathrm{EXT}_n$, replace each $y_i$ by $x_i^2$ in each test polynomial. The result is a degree-$2k$ algebraic decision tree on $\mathbb{R}^n$ of the same height that decides $W$ by the argument above. The theorem of Steele and Yao bounds the height of a degree-$2k$ algebraic decision tree that decides a set with $C$ components below by $\Omega(\log C) - O(n)$, with constants that depend on $k$. With $C = n!$ this is $\Omega(n \log n)$. $\blacksquare$

## Consequences

- **Optimal planar algorithms.** [Graham's scan](/graham-scan/), [Andrew's monotone chain](/andrew-monotone-chain/), the [divide-and-conquer hull](/divide-and-conquer-convex-hull/) and [Chan's algorithm](/chan-algorithm/) take $O(n \log n)$ time on the real RAM, so they are optimal up to a constant factor in the worst case.
- **Every dimension.** Planar inputs embed in $\mathbb{R}^d$ with the other coordinates zero, so the [3D convex hull](/convex-hull-3d/) and the hull in any dimension $d \ge 2$ also need $\Omega(n \log n)$.
- **Points known to be in convex position.** Theorem 1 holds for inputs that are promised to be in convex position. So knowing that every point is a vertex does not help; only the order is costly.
- **No fast hull from fast arithmetic.** The models allow multiplication, division and square roots, so the bound holds for algorithms that compute angles, slopes or distances, not only for algorithms that compare.
- **Reductions from the hull.** Problems that yield the hull in $O(n)$ extra time inherit the bound, for example the [Delaunay triangulation](/delaunay-triangulation/) and the [Voronoi diagram](/voronoi-diagram/), whose unbounded cells are in the hull order.

## Tightness

The bound is tight in both models: Andrew's algorithm makes $O(n \log n)$ orientation tests, each a polynomial of degree 2, and so runs as an algebraic decision tree of degree 2 and as an algebraic computation tree of height $O(n \log n)$. In Theorem 1 the leading term $n \lg n$ is matched up to a constant factor by the comparisons of a sort.

The bound needs the hard inputs to have many hull vertices: the inputs of the proofs have $h = n$. When $h$ is small, $O(n \log h)$ time suffices, and the [output-sensitive lower bound](/convex-hull-output-sensitive-lower-bound/) shows that $\Omega(n \log h)$ is the right answer.

The bound also depends on the model. With integer coordinates on a word RAM, a planar hull takes the time of an integer sort plus $O(n)$, because the scans of Andrew's algorithm are linear after the sort, and integer sorting is faster than $n \log n$ there. With a sorted input, the hull takes $O(n)$ time.

## History

Shamos noted in his 1978 thesis that the ordered planar hull lets one sort, by lifting the numbers to a parabola, so a hull algorithm with $o(n \log n)$ comparisons would give a sort that is too fast. That argument needs a model in which sorting is hard, and it does not cover the unordered question. Yao proved in 1981 that even identifying the hull vertices needs $\Omega(n \log n)$ quadratic tests. Steele and Yao (1982) and Ben-Or (1983) bounded the height of algebraic decision trees and algebraic computation trees by the number of connected components, and the reduction from element distinctness then gives the bound in both models.

## References
