---
tag: 8XQFAN
kind: concept
slug: geometric-cutting
name: Geometric cutting
aliases:
- cutting
- Chazelle-Friedman cutting
- cutting lemma
- hierarchical cutting
area: geometry/range-searching
level: advanced
summary: Partition of space into few simplices each crossed by few hyperplanes of a given set, the key tool behind partition trees.
prereqs: [epsilon-net-theorem, line-arrangement]
see_also: [shallow-cutting, partition-theorem, partition-tree, simplex-range-searching, halfspace-range-searching, epsilon-net-theorem, trapezoidal-map, line-arrangement]
sources:
  - paper: doi:10.1007/BF02122778
    title: Bernard Chazelle and Joel Friedman, A deterministic view of random sampling and its use in geometry, Combinatorica 10(3), 1990, pages 229 to 249
    locator: the existence of (1/r)-cuttings of size O(r^d) (DOI to be checked)
  - paper: doi:10.1007/BF02189314
    title: Bernard Chazelle, Cutting hyperplanes for divide-and-conquer, Discrete and Computational Geometry 9, 1993, pages 145 to 158
    locator: deterministic construction in O(n r^(d-1)) time and hierarchical cuttings (DOI to be checked)
  - paper: doi:10.1007/BF02573972
    title: Jiří Matoušek, Range searching with efficient hierarchical cuttings, Discrete and Computational Geometry 10, 1993, pages 157 to 182
    locator: simplex range searching with O(n^d / log^d n) space and O(log n) query, and the space and query trade-off (DOI to be checked)
  - paper: doi:10.1007/BF02187740
    title: Kenneth L. Clarkson and Peter W. Shor, Applications of random sampling in computational geometry, II, Discrete and Computational Geometry 4, 1989, pages 387 to 421
    locator: random samples and the expected number of conflicts of their cells (DOI to be checked)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 16, Section 16.3, Cutting trees (the cutting lemma in the plane and its use for counting queries)
---

A cutting of a set $H$ of $n$ hyperplanes in $\mathbb{R}^d$ is a subdivision of space into simplices such that the interior of each simplex is crossed by few hyperplanes of $H$. With a parameter $r$, a **$(1/r)$-cutting** allows at most $n/r$ crossing hyperplanes per simplex. The cutting lemma of Chazelle and Friedman says that a $(1/r)$-cutting of size $O(r^d)$ always exists, and Chazelle showed how to build it deterministically in $O(n r^{d-1})$ time. Cuttings turn problems on arrangements into divide and conquer: each simplex leaves a subproblem with $n/r$ hyperplanes. They are the main tool for [simplex range searching](/simplex-range-searching/) with large space, for the [partition theorem](/partition-theorem/) behind [partition trees](/partition-tree/), and, in the form of [shallow cuttings](/shallow-cutting/), for halfspace reporting.

## In plain words

Draw many straight lines across a sheet of paper. The goal is to cut the sheet into a small number of triangles so that each triangle is crossed by only a few of the lines, for example at most one tenth of them.

A simple way is to pick a few lines at random, draw only those, and cut the pieces they form into triangles. A line that was not picked may cross a triangle, but a triangle crossed by very many lines would most likely have been cut by one of the picked lines. So few lines cross each triangle. A finer version of this idea uses the smallest possible number of triangles.

Once the sheet is cut, a hard question about all the lines splits into small questions, one per triangle, each with fewer lines.

## The idea

**Definition.** Let $H$ be a set of $n$ hyperplanes in $\mathbb{R}^d$ and $1 \le r \le n$. A hyperplane $h$ **crosses** a simplex $\sigma$ if $h$ meets the interior of $\sigma$. A **$(1/r)$-cutting** for $H$ is a set $\Xi$ of (possibly unbounded) $d$-dimensional simplices with pairwise disjoint interiors that together cover $\mathbb{R}^d$, such that each $\sigma \in \Xi$ is crossed by at most $n/r$ hyperplanes of $H$. Its **size** is $|\Xi|$. Often a cutting of a given simplex or box is used instead of all of $\mathbb{R}^d$. In the plane, trapezoids are used in place of triangles; each splits into two triangles.

**The cutting lemma (Chazelle and Friedman 1990).** For each fixed $d$ there is a constant $C_d$ such that for every set $H$ of $n$ hyperplanes in $\mathbb{R}^d$ and every $1 \le r \le n$, there is a $(1/r)$-cutting for $H$ of size at most $C_d r^d$.

The size $O(r^d)$ is optimal: if the hyperplanes are in general position, their arrangement has $\binom{n}{d}$ vertices, and a simplex crossed by at most $n/r$ hyperplanes contains at most $\binom{n/r}{d}$ vertices in its interior, so $\Omega(r^d)$ simplices are needed.

**First construction: random sampling.** Let $R$ be a random sample of $H$, and decompose the arrangement of $R$ into simplices, by the bottom vertex triangulation in $\mathbb{R}^d$ or by the vertical decomposition in the plane. No hyperplane of $R$ crosses any of these simplices. The range space whose ranges are the sets of hyperplanes of $H$ crossing a simplex has bounded VC dimension, so by the [epsilon-net theorem](/epsilon-net-theorem/) a sample of size $O(r \log r)$ is a $(1/r)$-net with good probability, and then every simplex is crossed by fewer than $n/r$ hyperplanes. The arrangement of $O(r \log r)$ hyperplanes has $O((r \log r)^d)$ simplices, so this gives a $(1/r)$-cutting of size $O((r \log r)^d)$. Clarkson's random sampling bound gives a similar result: for a sample of size $r$, every simplex is crossed by $O((n / r) \log r)$ hyperplanes with high probability.

**Second construction: refinement.** Chazelle and Friedman take a random sample of size $r$ only. Most simplices are then crossed by $O(n/r)$ hyperplanes, and the expected number of simplices crossed by at least $t n / r$ hyperplanes decays exponentially in $t$. Each heavy simplex, crossed by $t n/r$ hyperplanes with $t > 1$, is cut again by a $(1/t)$-cutting of its own crossing hyperplanes, built by the first construction. The extra simplices sum to $O(r^d)$ in expectation, which gives the lemma. Derandomizing this, Chazelle (1993) builds a $(1/r)$-cutting of size $O(r^d)$ in $O(n r^{d-1})$ deterministic time, together with the list of hyperplanes crossing each simplex.

**Hierarchical cuttings.** Chazelle's construction also gives a sequence of cuttings $\Xi_0, \Xi_1, \dots, \Xi_k$ for $r_i = \rho^i$, with a constant $\rho$, such that each simplex of $\Xi_i$ lies inside one simplex of $\Xi_{i-1}$ and each simplex of $\Xi_{i-1}$ contains $O(1)$ simplices of $\Xi_i$. The total size is still $O(r^d)$. A point is located in all levels by walking down the hierarchy with $O(1)$ tests per level, so in $O(\log r)$ time.

## Examples

**One dimension.** In $\mathbb{R}^1$ the hyperplanes are points. For the $8$ values $H = \{2, 3, 4, 5, 6, 7, 8, 9\}$ and $r = 4$, the intervals $(-\infty, 3]$, $[3, 5]$, $[5, 7]$, $[7, \infty)$ form a $(1/4)$-cutting of size $4$: their interiors contain the values $\{2\}$, $\{4\}$, $\{6\}$ and $\{8, 9\}$, at most $n/r = 2$ each. In one dimension a $(1/r)$-cutting of size $r$ always exists: cut at every $(n/r)$-th value in sorted order.

**Eight lines in the plane.** Take $H$ to be the lines $y = 0$, $y = x$, $y = 6 - x$, $y = 3$, $y = 2x - 6$, $y = x/2 + 1$, $y = 9 - 2x$ and $y = 5 - x/2$, called $h_1, \dots, h_8$, and the box $[-20, 20]^2$, which contains all their crossing points. The counts below were computed exactly with rational arithmetic, by cutting the box into vertical slabs at every vertex of the sample and every point where a sample line meets the box, cutting each slab into trapezoids by the sample lines, and testing each line of $H$ against each open trapezoid. This slab decomposition is finer than the vertical decomposition, which only extends vertical segments from each vertex to the nearest lines above and below.

| sample $R$ | trapezoids | most lines of $H$ crossing one trapezoid | a cutting for |
|---|---|---|---|
| $h_1, h_2, h_3$ | 19 | 4 | $r = 2$, since $4 \le 8/2$ |
| $h_2, h_4, h_7$ | 14 | 5 | not $r = 2$: one trapezoid is too heavy |
| $h_3, h_4, h_5$ | 24 | 3 | $r = 2$ |
| $h_1, h_3, h_4, h_5$ | 36 | 2 | $r = 4$, since $2 \le 8/4$ |

The second row shows why a sample can fail and why the constructions either take a larger sample or refine the heavy cells. The trapezoid with $-4 < x < 0$ between $y = 0$ and $y = 6 - x$ in the first row is crossed by $h_4$, $h_6$ and $h_8$.

## Where it is used

- **Simplex and halfspace range counting with large space.** By duality the query halfspace becomes a point and the stored points become hyperplanes. A hierarchical $(1/r)$-cutting of these hyperplanes with $r = n$ stores, for each simplex, how many hyperplanes that cross its parent pass above it; the query point is located level by level and these counts are added, giving $O(\log n)$ query time with $O(n^d)$ space for halfspace counting, and $O(n^d / \log^d n)$ space after Matoušek's refinement. See [halfspace range searching](/halfspace-range-searching/) and [simplex range searching](/simplex-range-searching/).
- **Space and query trade-offs.** A cutting at the top levels and [partition trees](/partition-tree/) below give $O((n / m^{1/d}) \log^{O(1)} n)$ query time with $O(m)$ space.
- **The partition theorem.** Matoušek's proof uses a cutting of a small test set of hyperplanes to choose each cell; see the [partition theorem](/partition-theorem/).
- **Halfspace reporting.** [Shallow cuttings](/shallow-cutting/) cover only the points of low depth and are much smaller.
- **Point location in arrangements** in $O(\log n)$ time, and divide and conquer for problems on lines and points such as counting incidences or segment intersections.
- **Derandomization.** Cuttings give deterministic versions of many random sampling algorithms, including linear programming in fixed dimension.

## References
