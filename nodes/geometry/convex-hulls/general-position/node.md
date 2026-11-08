---
tag: DECE75
kind: definition
slug: general-position
name: General position
aliases:
- general position assumption
- non-degenerate input
area: geometry/convex-hulls
level: intro
summary: An assumption that no three points are collinear, used to avoid degenerate cases.
prereqs: [orientation-test]
see_also: [in-circle-test, general-position-delaunay, degeneracy-in-sweeps, collinear-points, lp-degeneracy, facet, andrew-monotone-chain]
sources:
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 1, Section 1.2, Degeneracies and Robustness
  - book: isbn:9780387953748
    title: Jiri Matousek, Lectures on Discrete Geometry, Graduate Texts in Mathematics 212, Springer, 2002
    locator: Chapter 1, Section 1.1 (general position of points in R^d)
  - paper: doi:10.1145/77635.77639
    title: Herbert Edelsbrunner and Ernst Peter Mucke, Simulation of Simplicity, a technique to cope with degenerate cases in geometric algorithms, ACM Transactions on Graphics 9(1), 1990
    locator: the whole paper (symbolic perturbation of the coordinates and the sign rules for determinants)
---

A set of points is in general position for an algorithm when none of the predicates that the algorithm evaluates is exactly zero on the input. For planar [convex hulls](/convex-hull/) and segment problems this means that no three points are collinear, which is the case where the [orientation test](/orientation-test/) returns $0$. Many proofs and textbook algorithms assume general position to skip the degenerate cases, and an implementation must then either handle those cases or remove them by a perturbation.

## Definition

Let $P = (p_1, \ldots, p_n)$ be a finite sequence of points in $\mathbb{R}^d$, and let $\Phi$ be a finite family of predicates, each of the form $\operatorname{sign} f(p_{i_1}, \ldots, p_{i_k})$, where $f$ is a polynomial in the coordinates of $k$ points. The input $P$ is in **general position with respect to $\Phi$** if $p_i \ne p_j$ for $i \ne j$, and $f(p_{i_1}, \ldots, p_{i_k}) \ne 0$ for every $f$ in $\Phi$ and every choice of pairwise distinct indices $i_1, \ldots, i_k$. An input that is not in general position is **degenerate**, and a tuple on which some $f$ vanishes is a **degenerate case**.

The usual instances name the predicate:

- **No three collinear** (planar hulls, triangulations, segment arrangements): $\mathrm{orient}(p_i, p_j, p_k) \ne 0$ for all distinct $i, j, k$.
- **Affine general position in $\mathbb{R}^d$** (hulls in $d$ dimensions): no $d + 1$ of the points lie on a common hyperplane. Equivalently, every $d + 1$ of the points are affinely independent, so the $d$-dimensional orientation determinant of each $(d+1)$-tuple is nonzero. For $d = 2$ this is "no three collinear".
- **No four cocircular** (Delaunay triangulations and Voronoi diagrams): the [in-circle test](/in-circle-test/) is nonzero on each 4-tuple. See [general position for Delaunay](/general-position-delaunay/).
- **Distinct $x$-coordinates** (sweep algorithms): no two points, and no two segment end points, share an $x$-coordinate. See [degeneracy in sweeps](/degeneracy-in-sweeps/).

**Genericity.** Degenerate inputs are rare in a precise sense. Let $F(p_1, \ldots, p_n) = \prod f(p_{i_1}, \ldots, p_{i_k})$ over all predicates and index tuples, times $\prod_{i<j} |p_i - p_j|^2$. If each $f$ is a nonzero polynomial, then $F$ is a nonzero polynomial in $dn$ variables, and $P$ is degenerate exactly when $F(P) = 0$.

**Lemma.** The zero set of a nonzero real polynomial $g$ in $m$ variables has Lebesgue measure zero in $\mathbb{R}^m$.

*Proof.* By induction on $m$. For $m = 1$, $g$ has finitely many roots. For $m > 1$, write $g = \sum_{k=0}^{t} c_k(x_1, \ldots, x_{m-1})\, x_m^k$ with $c_t$ a nonzero polynomial. By the induction hypothesis, the set $Z$ where $c_t = 0$ has measure zero in $\mathbb{R}^{m-1}$. For each $(x_1, \ldots, x_{m-1}) \notin Z$, the polynomial in $x_m$ is nonzero, so its section of the zero set is finite. By Fubini's theorem the zero set of $g$ has measure zero. $\square$

So the degenerate inputs form a closed set of measure zero in $\mathbb{R}^{dn}$, and each input has general-position inputs arbitrarily close to it. This justifies the assumption for random real input. It does not justify it for real data, which is often on a grid, and it does not make an algorithm correct on the degenerate input itself.

**Symbolic perturbation.** Simulation of Simplicity (Edelsbrunner and Mücke) replaces each coordinate by $p_{i,j} + \varepsilon_{i,j}$, where the $\varepsilon_{i,j}$ are powers of one infinitesimal $\varepsilon > 0$ that grow so fast with the index that the terms of each perturbed determinant have pairwise different orders in $\varepsilon$. Each predicate then has a sign that is never zero: the sign of the first nonzero coefficient in a fixed sequence of minors. The algorithm runs as if the input were in general position, with the same exact arithmetic, and a post-processing step removes the artifacts, such as hull edges of length zero.

## Examples and non-examples

- **Example.** The points $(0,0)$, $(4,0)$, $(1,2)$, $(3,5)$ are in general position for the orientation test: the orientation determinants of its four triples, taken in the order $(1,2,3)$, $(1,2,4)$, $(1,3,4)$, $(2,3,4)$ of the indices, are $8$, $20$, $-1$ and $-13$, and none is $0$.
- **Collinear but not degenerate for Delaunay.** The square $(0,0)$, $(1,0)$, $(1,1)$, $(0,1)$ has no three collinear points, so it is in general position for planar hulls. Its four points lie on one circle, and the in-circle determinant is $0$, so it is degenerate for Delaunay: it has two Delaunay triangulations. The points $(0,0)$, $(1,0)$, $(0,1)$, $(2,2)$ have in-circle determinant $-4 \ne 0$.
- **Non-example: a small grid.** The $3 \times 3$ grid $\{0,1,2\}^2$ has 84 triples of points, and 8 of them are collinear: the three rows, the three columns and the two diagonals. It also has 14 sets of four points on one circle with no three of them collinear. The $4 \times 4$ grid has 44 collinear triples out of 560, and the $5 \times 5$ grid has 152 out of 2300.
- **Non-example: random integers.** Ten random points with coordinates in $\{0, \ldots, 9\}$ were degenerate (a repeat or a collinear triple) in 1964 of 2000 seeded trials. With coordinates in $\{0, \ldots, 99\}$ the count was 175 of 2000, and with $\{0, \ldots, 999\}$ it was 2 of 2000. So tests with small integer coordinates are the cheap way to hit the degenerate cases on purpose.
- **Non-example: duplicates.** Any input with a repeated point is degenerate, since $\mathrm{orient}(p, p, r) = 0$ for every $r$.

How hull algorithms meet the degenerate cases:

- [Andrew's monotone chain](/andrew-monotone-chain/) and the [Graham scan](/graham-scan/) pop on $\mathrm{orient} \le 0$, which removes the collinear boundary points, and a test $< 0$ keeps them.
- The [Jarvis march](/jarvis-march/) breaks ties between collinear candidates by distance.
- [Quickhull](/quickhull/) must choose among several farthest points.
- In three dimensions, four coplanar points make a hull facet that is not a triangle, so algorithms that assume general position, such as the randomized incremental method of [3D convex hull](/convex-hull-3d/), either merge coplanar triangles or use a perturbation.
- In $\mathbb{R}^d$, points in affine general position have a simplicial hull: each [facet](/facet/) is a $(d-1)$-simplex.

## Related definitions

- [Orientation test](/orientation-test/) and [in-circle test](/in-circle-test/): the predicates whose zero sets define the degenerate cases.
- [Collinear points](/collinear-points/): the degenerate case of the planar hull.
- [Affine hull](/affine-hull/): points are affinely independent when none lies in the affine hull of the others.
- [General position for Delaunay](/general-position-delaunay/): no four points on a circle.
- [Degeneracy in sweeps](/degeneracy-in-sweeps/): equal $x$-coordinates and other events at the same time.
- [LP degeneracy](/lp-degeneracy/): the analogue in linear programming, where more than $d$ constraints are tight at a vertex.
- [Facet](/facet/) and [convex polytope](/convex-polytope/): general position makes the hull simplicial.

## References
