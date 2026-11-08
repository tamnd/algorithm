---
tag: RBJT65
kind: theorem
slug: convex-hull-output-sensitive-lower-bound
name: Output-sensitive convex hull lower bound
aliases:
- Omega(n log h) lower bound
- multiset size verification bound
area: geometry/convex-hulls
level: advanced
summary: Computing a hull with h vertices needs Omega(n log h) time in the algebraic decision tree model.
prereqs: [convex-hull-lower-bound, ben-or-theorem, algebraic-computation-tree, convex-hull-problem]
see_also: [chan-algorithm, kirkpatrick-seidel, jarvis-march, element-distinctness-lower-bound, algebraic-decision-tree, reduction-lower-bound]
sources:
  - paper: doi:10.1137/0215021
    title: David G. Kirkpatrick and Raimund Seidel, The ultimate planar convex hull algorithm?, SIAM Journal on Computing 15(1), 1986
    locator: the lower bound part (the multiset size verification problem and its reduction to the convex hull)
  - paper: doi:10.1145/800061.808735
    title: "Michael Ben-Or, Lower bounds for algebraic computation trees, Proceedings of the 15th Annual ACM Symposium on Theory of Computing (STOC 1983), 80-86"
    locator: the main theorem on the height of algebraic computation trees
  - paper: doi:10.1016/0196-6774(82)90002-5
    title: "J. Michael Steele and Andrew C. Yao, Lower bounds for algebraic decision trees, Journal of Algorithms 3(1) (1982), 1-8"
    locator: the main theorem (algebraic decision trees of fixed degree)
  - paper: doi:10.1007/BF02712873
    title: Timothy M. Chan, Optimal output-sensitive convex hull algorithms in two and three dimensions, Discrete and Computational Geometry 16(4), 1996
    locator: the introduction (the matching O(n log h) upper bound and the lower bound it meets)
---

The output-sensitive convex hull lower bound says that an algorithm that finds the vertices of the [convex hull](/convex-hull/) of $n$ points in the plane must, for each $k$, spend $\Omega(n \log k)$ steps on some input whose hull has at most $k$ vertices. So the time $O(n \log h)$ of [Chan's algorithm](/chan-algorithm/) and of the [Kirkpatrick-Seidel algorithm](/kirkpatrick-seidel/) is optimal, where $h$ is the number of hull vertices. The proof, due to Kirkpatrick and Seidel, reduces from the *multiset size verification* problem: decide whether $n$ real numbers take exactly $k$ distinct values. That set has at least $k^{n-k} k!$ connected components, and [Ben-Or's theorem](/ben-or-theorem/) turns this count into a lower bound.

## Statement

The model is the [algebraic computation tree](/algebraic-computation-tree/), as on the page [convex hull lower bound](/convex-hull-lower-bound/): binary tests $u > 0$, $u \ge 0$, $u = 0$ and unit-cost operations $+, -, \times, \div, \sqrt{\ }$. The input is $n$ points in the plane, $2n$ reals, repeats allowed. The leaves are labelled with sequences of indices. A tree *finds the hull vertices* if on every input its leaf lists, for each vertex $v$ of the convex hull, exactly one index $i$ with $p_i = v$, and no other index. The order of the list is free. The *cost* of an input is the number of nodes on its path.

**Theorem (Kirkpatrick and Seidel).** Let $1 \le k \le n$, and let $T$ be a valid algebraic computation tree that finds the hull vertices of $n$ points. Let $L_k$ be the largest cost of an input whose hull has at most $k$ vertices. Then

$$L_k \ \ge\ \frac{n \lg k - n \lg (3e)}{\lg 18} - n.$$

So $L_k = \Omega(n \log k)$ as $k$ grows. The same holds for algebraic decision trees of each fixed degree, with constants that depend on the degree.

In words: there is no algorithm in these models whose worst-case time on inputs with $h$ hull vertices is $o(n \log h)$. For $h = n$ this is the $\Omega(n \log n)$ bound.

## In plain words

Put numbers on a bowl-shaped curve, one point for each number. Equal numbers give the same point, so the hull has one corner for each different number. A hull program then tells you how many different numbers there are.

Checking that a list of numbers has exactly a given count of different values is hard: there are very many ways to group the numbers into that many classes and to order the classes, and a program must tell all of these apart. That count grows like the number of points times the logarithm of the number of classes.

If a hull program were faster on small hulls, you could stop it after its time limit and use its answer to check the count. That would be too fast, so no such program exists.

## Proof

**The multiset size verification problem.** For $1 \le k \le n$ let

$$W_k = \{x \in \mathbb{R}^n : \text{the set } \{x_1, \ldots, x_n\} \text{ has exactly } k \text{ elements}\}.$$

**Lemma 1.** $W_k$ has at least $k! \, k^{n-k}$ connected components, so $\lg \mathrm{cc}(W_k) \ge n \lg k - n \lg e$.

*Proof.* For $x \in W_k$ with distinct values $y_1 < \cdots < y_k$, let the *pattern* of $x$ be the map $\phi_x : \{1, \ldots, n\} \to \{1, \ldots, k\}$ with $x_i = y_{\phi_x(i)}$. It is onto.

*The pattern is locally constant on $W_k$.* Fix $x \in W_k$ and let $\delta > 0$ be the smallest gap $y_{c+1} - y_c$. Let $x' \in W_k$ with $|x'_i - x_i| < \delta / 3$ for all $i$. The coordinates $x'_i$ with $\phi_x(i) = c$ lie in the open interval $I_c$ of radius $\delta/3$ around $y_c$, and these intervals are disjoint and in increasing order of $c$. Each interval contains at least one value of $x'$, and $x'$ has exactly $k$ distinct values, so each interval contains exactly one. So $x'_i = x'_j$ exactly when $\phi_x(i) = \phi_x(j)$, and the values keep their order, so $\phi_{x'} = \phi_x$.

A locally constant map is constant on each connected component, so inputs with different patterns are in different components. Each onto map $\phi$ is the pattern of some $x$, for example $x_i = \phi(i)$. So $\mathrm{cc}(W_k)$ is at least the number of onto maps from $\{1, \ldots, n\}$ to $\{1, \ldots, k\}$. The maps that send $1, \ldots, k$ to $1, \ldots, k$ in some order and the rest anywhere are onto and pairwise distinct, and there are $k! \, k^{n-k}$ of them. Finally $\lg(k! \, k^{n-k}) \ge k \lg k - k \lg e + (n - k) \lg k = n \lg k - k \lg e \ge n \lg k - n \lg e$, by $k! \ge (k/e)^k$. $\square$

**Lemma 2.** Every valid algebraic computation tree that decides $W_k$ has height at least $(n \lg k - n \lg(3e)) / \lg 18$.

*Proof.* By [Ben-Or's theorem](/ben-or-theorem/), a tree of height $h$ that decides $W_k$ has $\mathrm{cc}(W_k) \le 2 \cdot 3^{n-1} \cdot 18^h \le 3^n \cdot 18^h$. Take logarithms and use Lemma 1. $\square$

**The reduction.** Let $T$ and $L_k$ be as in the theorem. Build a tree $T'$ on input $x \in \mathbb{R}^n$:

1. Compute $y_i = x_i \times x_i$ for $i = 1, \ldots, n$, with $n$ computation nodes.
2. Run $T$ on the points $p_i = (x_i, y_i)$, but cut each path after $L_k$ nodes of $T$: a path of $T$ that is longer is replaced by a reject leaf after its first $L_k$ nodes.
3. At a leaf of $T$ reached within $L_k$ nodes, accept if its label has exactly $k$ indices, and reject otherwise.

$T'$ is valid, because each of its paths is a prefix of a path of the valid tree $T$ after $n$ multiplications, and it has height at most $L_k + n$.

*The hull of the lifted points.* Let $x$ have exactly $j$ distinct values. Points $p_i$ and $p_l$ coincide exactly when $x_i = x_l$, so there are $j$ distinct points, and each is a vertex of their hull, because distinct points on the parabola $y = x^2$ are in convex position (see the page [convex hull lower bound](/convex-hull-lower-bound/)). So the hull has exactly $j$ vertices.

*$T'$ decides $W_k$.* If $j \le k$, the input of $T$ has at most $k$ hull vertices, so its path has at most $L_k$ nodes and is not cut. Its leaf lists $j$ indices, so $T'$ accepts exactly when $j = k$. If $j > k$, either the path is cut and $T'$ rejects, or the leaf lists $j \ne k$ indices and $T'$ rejects. In both cases $T'$ is correct.

By Lemma 2, $L_k + n \ge (n \lg k - n \lg (3e)) / \lg 18$, which is the theorem.

*Fixed-degree decision trees.* In a degree-$d$ algebraic decision tree, substitute $x_i^2$ for $y_i$ in each test. This gives a degree-$2d$ decision tree on $\mathbb{R}^n$, with the same cut-off and the same leaves, of height at most $L_k$. The theorem of Steele and Yao bounds its height below by $\Omega(\log \mathrm{cc}(W_k)) - O(n)$, with constants that depend on $d$, and Lemma 1 gives $\Omega(n \log k)$ for $k$ larger than a constant that depends on $d$. $\blacksquare$

## Consequences

- **Optimal output-sensitive algorithms.** [Chan's algorithm](/chan-algorithm/) and the [Kirkpatrick-Seidel algorithm](/kirkpatrick-seidel/) run in $O(n \log h)$ time on the real RAM, so they are optimal in these models for every range of $h$. The [Jarvis march](/jarvis-march/) with $O(nh)$ time is optimal only for $h = O(1)$.
- **Order is free.** The bound holds when the vertices may be listed in any order, so it is not the cost of sorting the output. Chan's algorithm also returns them in counterclockwise order within the same bound.
- **Three dimensions.** Planar inputs embed in $\mathbb{R}^3$, so $\Omega(n \log h)$ also holds for the [3D convex hull](/convex-hull-3d/), where Chan's three-dimensional algorithm matches it.
- **Other problems.** The same reduction works for problems whose output size counts distinct values. For example, the distinct points among $(x_i, -x_i)$ are all maximal, so finding the maximal points of a planar set with at most $k$ maximal points also needs $\Omega(n \log k)$.

## Tightness

The bound is tight for every $h$, by Chan's algorithm. For $h \le 2$ the right answer is $\Theta(n)$, which the formula $n \log h$ misses; the usual statement is $\Theta(n \log h)$ for $h \ge 2$, or $\Theta(n (1 + \log h))$.

The hard inputs of the proof have many repeated points, because the parabola puts distinct numbers on distinct hull vertices. Points with integer coordinates on a word RAM fall outside the model, as in the [$\Omega(n \log n)$ bound](/convex-hull-lower-bound/).

## History

Kirkpatrick and Seidel gave the first planar hull algorithm with $O(n \log h)$ time in 1986 and proved the matching lower bound in the same paper. They introduced the multiset size verification problem for this purpose and used the component bound of Steele and Yao for algebraic decision trees of fixed degree. Ben-Or's theorem of 1983 gives the same bound for algebraic computation trees. Chan's simpler algorithm of 1996 meets the bound in two and three dimensions.

## References
