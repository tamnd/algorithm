---
tag: YKECVQ
kind: concept
slug: hirsch-conjecture
name: Hirsch conjecture
aliases:
- diameter conjecture
- polynomial Hirsch conjecture
area: optimization/linear-programming
level: research
summary: Conjectured bound on the combinatorial diameter of polytopes; relevant to simplex pivot counts.
prereqs: [polyhedron, basic-feasible-solution, simplex-method]
see_also: [klee-minty-cube, simplex-method, smoothed-simplex-analysis, dantzig-pivot-rule, convex-polytope, flip-graph-diameter-theorem, lp-degeneracy, lp-in-p]
sources:
  - paper: doi:10.4007/annals.2012.176.1.7
    title: Francisco Santos, A counterexample to the Hirsch conjecture, Annals of Mathematics 176(1), 2012
    locator: pages 383 to 412, spindles and the 43-dimensional counterexample with 86 facets
  - paper: doi:10.1007/BF02395040
    title: Victor Klee and David W. Walkup, The d-step conjecture for polyhedra of dimension d < 6, Acta Mathematica 117, 1967
    locator: pages 53 to 78, the reduction to the d-step case and the unbounded counterexample
  - paper: doi:10.1090/S0273-0979-1992-00285-9
    title: Gil Kalai and Daniel J. Kleitman, A quasi-polynomial bound for the diameter of graphs of polyhedra, Bulletin of the AMS 26(2), 1992
    locator: pages 315 to 316, the bound n to the power log d + 2
  - paper: doi:10.1137/140962310
    title: Michael J. Todd, An improved Kalai-Kleitman bound for the diameter of a polyhedron, SIAM Journal on Discrete Mathematics 28(4), 2014
    locator: pages 1944 to 1947, the bound (n - d) to the power log2 d
  - paper: doi:10.1007/s00454-018-0016-y
    title: Noriyoshi Sukegawa, An asymptotically improved upper bound on the diameter of polyhedra, Discrete and Computational Geometry 62, 2019
    locator: pages 690 to 699, the improved exponent
  - paper: doi:10.1112/plms/s3-20.1.161
    title: D. G. Larman, Paths on polytopes, Proceedings of the London Mathematical Society s3-20(1), 1970
    locator: pages 161 to 178, the linear bound in n for fixed d
  - paper: doi:10.1007/BF01589099
    title: Denis Naddef, The Hirsch conjecture is true for (0,1)-polytopes, Mathematical Programming 45, 1989
    locator: pages 109 to 110, the proof for 0/1 polytopes
  - book: isbn:9780387943657
    title: Günter M. Ziegler, Lectures on Polytopes, Graduate Texts in Mathematics 152, Springer, 1995
    locator: Chapter 3, Graphs of polytopes (diameters and the Hirsch conjecture)
---

The Hirsch conjecture stated that the graph of every $d$-dimensional [polytope](/convex-polytope/) with $n$ facets has diameter at most $n - d$: any two vertices are joined by a path of at most $n - d$ edges. Warren Hirsch proposed it in 1957 in a letter to Dantzig, as a question about how few pivots the [simplex method](/simplex-method/) could need from any start. Santos disproved it in 2010, with a polytope of dimension 43 with 86 facets and diameter at least 44. The weaker *polynomial Hirsch conjecture*, which asks for a bound polynomial in $n$ and $d$, is still open, and the best known bound is quasi-polynomial.

## In plain words

The corners and edges of a polytope form a network, like a road map. The simplex method travels on this map, one edge per step. However clever the rule for choosing the next edge, the trip from a starting corner to the best corner needs at least as many steps as the shortest route between them.

Hirsch guessed that the shortest route between any two corners is never longer than the number of flat sides of the polytope minus its dimension. A cube shows that this would be the best possible. The guess held for fifty years and then turned out false, but only by a little. Nobody knows whether the shortest routes are always short in a weaker sense, growing only like a fixed power of the size. If they are not, no rule for the simplex method can be fast on all problems.

## The idea

**Definitions.** For a polytope $P$, the graph $G(P)$ has the vertices of $P$ as nodes and the edges of $P$ as arcs. Its diameter $\operatorname{diam}(P)$ is the largest distance between two vertices. Let $\Delta(d, n)$ be the largest diameter of a $d$-dimensional polytope with $n$ facets. In [standard form](/lp-standard-form/) with $m$ equations and $N$ variables, the feasible region has dimension at most $N - m$ and at most $N$ facets, and two vertices are adjacent when some pair of [bases](/basic-feasible-solution/) for them differ by one [pivot](/pivot-operation/).

**The conjecture.** $\Delta(d, n) \le n - d$ for all $n > d \ge 2$.

**Why $n - d$ is natural.** A simple polytope has $d$ facets through each vertex. Going from $u$ to $v$, one could hope to leave each facet at $u$ that does not contain $v$ once and enter each facet at $v$ once, without ever leaving a facet that contains $v$. That needs at most $n - d$ steps when the facets at $u$ and $v$ are disjoint. The conjecture says that such a path, which never revisits a facet, always exists. Santos's example shows that sometimes it does not.

**Reductions.** Klee and Walkup (1967) showed that it is enough to prove the case $n = 2d$, the *$d$-step conjecture*, and that one may assume the polytope is simple. They proved the $d$-step conjecture for $d \le 5$, and they found an unbounded 4-dimensional polyhedron with 8 facets and diameter 5, so the statement fails for unbounded polyhedra.

**The counterexample.** Santos built a *spindle*: a polytope with two special vertices $u$ and $v$ such that every facet contains exactly one of them. If the distance from $u$ to $v$ is more than $d$, the $d$-step conjecture, and so the Hirsch conjecture, fails. He found a 5-dimensional spindle with 48 facets and length 6, and a construction that keeps the excess while it raises the dimension and the number of facets until $n = 2d$. This gives the polytope of dimension 43 with 86 facets.

**Upper bounds.** The best known bounds are far above $n - d$:

- Larman (1970): $\Delta(d, n) \le 2^{d-3} n$, linear in $n$ for fixed $d$.
- Kalai and Kleitman (1992): $\Delta(d, n) \le n^{\log_2 d + 2}$. The argument takes the balls of growing radius around $u$ and around $v$. When each ball touches more than half of the $n$ facets, the two balls touch a common facet, and the rest of the path stays inside that facet, a polytope of dimension $d - 1$. A recursion on $n$ and $d$ then gives the bound.
- Todd (2014): $\Delta(d, n) \le (n - d)^{\log_2 d}$, and Sukegawa (2019) improved the base of the logarithm in the exponent.

**Special classes.** The conjecture holds for $d \le 3$, and Naddef (1989) proved it for all 0/1 polytopes, which include the polytopes of many combinatorial problems.

## Examples

**The cube.** The $d$-cube $[0,1]^d$ has $n = 2d$ facets and diameter $d$: the vertices $0$ and $(1, \ldots, 1)$ differ in all $d$ coordinates, and one edge changes one coordinate. So $\operatorname{diam} = d = n - d$, and the bound of the conjecture cannot be lowered. The [Klee-Minty cube](/klee-minty-cube/) has the same graph, so its exponential pivot count comes from the rule, not from a long diameter.

**Small cases.** A simplex in dimension $d$ has $n = d + 1$ facets and every two vertices adjacent, so its diameter is $1 = n - d$. A convex polygon with $n$ edges has diameter $\lfloor n/2 \rfloor$, which is at most $n - 2$ for $n \ge 3$.

**Products.** For polytopes $P$ and $Q$, the product $P \times Q$ has $n_P + n_Q$ facets, dimension $d_P + d_Q$, and diameter $\operatorname{diam}(P) + \operatorname{diam}(Q)$. So if both satisfy the conjecture, the product does too, and a counterexample stays one under products with a cube. Santos's construction uses a different operation, which raises the dimension and the facets by one each.

## Where it is used

- **Lower bounds for pivot rules.** The number of pivots of any pivot rule, from a bad start, is at least the distance in $G(P)$ from the start to the optimum. A pivot rule that is polynomial on all programs needs the polynomial Hirsch conjecture to be true.
- **Analysis of the simplex method.** Results on the [smoothed](/smoothed-simplex-analysis/) and average behavior of the simplex method bound the length of the specific paths that a rule follows, which also bounds the diameter of the polytopes they cover.
- **Combinatorial polytopes.** The polytopes of matchings, of assignments and of many other combinatorial programs have 0/1 vertices, so by Naddef's theorem their diameter is at most $n - d$, and short pivot paths exist for them.
- **Flip graphs.** The graph of flips between the triangulations of a convex polygon is the graph of a polytope, the associahedron, and its [diameter](/flip-graph-diameter-theorem/) is a related question in geometry.

## References
