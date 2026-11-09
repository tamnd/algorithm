---
tag: P4B1EQ
kind: problem
slug: minimum-enclosing-circle
name: Minimum enclosing circle
aliases:
- smallest enclosing circle
- 1-center problem
- minimum enclosing disk
- smallest enclosing disk
area: geometry/geometric-optimization
level: intro
summary: Find the smallest circle containing a given set of points in the plane.
prereqs: [circumcircle, convex-hull, real-ram]
see_also: [welzls-algorithm, minimum-enclosing-ball, megiddo-fixed-dimension-lp, lp-type-problem, farthest-point-voronoi-diagram, k-center-problem, largest-empty-circle, prune-and-search]
sources:
  - paper: doi:10.1137/0212052
    title: Nimrod Megiddo, Linear-time algorithms for linear programming in R^3 and related problems, SIAM Journal on Computing 12(4), 1983
    locator: the section on the minimum enclosing circle (the deterministic O(n) prune-and-search algorithm)
  - paper: doi:10.1007/BFb0038202
    title: Emo Welzl, Smallest enclosing disks (balls and ellipsoids), in New Results and New Trends in Computer Science, Lecture Notes in Computer Science 555, Springer, 1991
    locator: Section 1 (history of the problem from Sylvester 1857) and Section 2 (Lemma 1 and the expected O(n) algorithm)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, 3rd edition, Springer, 2008
    locator: Chapter 4, Section 4.7, Smallest enclosing discs
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 6, the farthest-point Voronoi diagram and the smallest enclosing circle
  - paper: "Nimrod Megiddo, The weighted Euclidean 1-center problem, Mathematics of Operations Research 8(4), 1983"
    locator: the O(n) algorithm for the weighted version
  - paper: "Nimrod Megiddo and Kenneth J. Supowit, On the complexity of some common geometric location problems, SIAM Journal on Computing 13(1), 1984"
    locator: NP-hardness of the Euclidean p-center problem when p is part of the input
  - paper: "J. Elzinga and D. W. Hearn, Geometrical solutions for some minimax location problems, Transportation Science 6(4), 1972"
    locator: the iterative algorithm that moves between circles through two and three points
---

The minimum enclosing circle problem asks for the circle of smallest radius that contains a given finite set of points in the plane. It is the Euclidean 1-center problem: place one facility so that the largest distance to a client is as small as possible. The answer is unique, and it is fixed by two or three of the points. It can be found in $O(n)$ time, deterministically by Megiddo's [prune-and-search](/prune-and-search/) method or in expectation by the much simpler [Welzl's algorithm](/welzls-algorithm/).

## In plain words

You have a set of dots on a sheet of paper and a set of coins of every size. Find the smallest coin that covers all the dots. Either two dots sit on opposite sides of the coin's rim, or three dots sit on the rim and no gap between two neighboring rim dots is more than half the rim. If no dots touched the rim at all, a smaller coin would do. If the rim dots all sat on one side, you could slide the coin toward them and shrink it. This is why a few rim dots decide the whole answer, and the other dots do not matter.

## Definition

Notation: $P$ is the input point set, $n = |P|$, and a point is $p = (x, y)$. A disk with center $z \in \mathbb{R}^2$ and radius $r \ge 0$ is $D(z, r) = \{x : |x - z| \le r\}$.

**Input.** A finite nonempty set $P \subset \mathbb{R}^2$.

**Output.** The center $z^*$ and radius $r^*$ of the disk that contains $P$ and has the smallest radius:

$$r^* = \min_{z \in \mathbb{R}^2} \max_{p \in P} |p - z|.$$

The function $z \mapsto \max_p |p - z|$ is convex and tends to infinity, so the minimum exists. It is attained at exactly one center (two smallest disks give, by averaging, a strictly smaller one; see the proof on [Welzl's algorithm](/welzls-algorithm/)). The disk $D(z^*, r^*)$ has these properties.

- Let $B$ be the points of $P$ on its circle. Then $z^* \in \operatorname{conv} B$, and conversely a disk that contains $P$ and has its center in the [convex hull](/convex-hull/) of the points on its circle is the smallest one.
- So either $z^*$ is the midpoint of two points of $P$ (and then $r^*$ is half their distance), or $z^*$ is the circumcenter of three points of $P$ that form a triangle with no obtuse angle.
- The disk depends only on the vertices of $\operatorname{conv} P$, and $r^*$ is at least half the diameter of $P$ and at most $1/\sqrt{3}$ times the diameter (Jung's theorem in the plane).

No general position is needed. Duplicates change nothing. If all points are collinear, the answer is the disk on the two extreme points. If many points lie on the answer circle, any of the triples or pairs above fixes it.

## Variants

- **Ball in $\mathbb{R}^d$.** The [minimum enclosing ball](/minimum-enclosing-ball/), fixed by at most $d + 1$ points.
- **Weighted 1-center.** Minimize $\max_p w_p |p - z|$ with positive weights. Megiddo also solves this in $O(n)$ time.
- **$k$ centers.** Cover $P$ by $k$ disks of the smallest common radius: the Euclidean [k-center problem](/k-center-problem/). It is NP-hard when $k$ is part of the input (Megiddo and Supowit 1984). For $k = 2$ there are near-linear algorithms.
- **Other shapes.** The smallest enclosing ellipse ([minimum-volume enclosing ellipsoid](/minimum-volume-enclosing-ellipsoid/)), the smallest enclosing rectangle ([minimum-area enclosing rectangle](/minimum-area-enclosing-rectangle/)), the smallest enclosing triangle ([minimum-area enclosing triangle](/minimum-area-enclosing-triangle/)), and the thinnest enclosing ring ([minimum-width annulus](/minimum-width-annulus/)).
- **Outliers.** The smallest disk that contains all but $k$ of the points.
- **The dual problem.** The [largest empty circle](/largest-empty-circle/) with center in a given region.

## Examples

All numbers below are exact. A disk is given by its center and its squared radius.

| points | center | $r^2$ | fixed by |
|---|---|---|---|
| (0, 0), (2, 0), (2, 2), (0, 2) | (1, 1) | 2 | either diagonal pair |
| (0, 0), (6, 0), (1, 1) | (3, 0) | 9 | the pair (0, 0), (6, 0) |
| (0, 0), (6, 0), (2, 4), (3, 1), (5, 3), (1, 2) | (3, 1) | 10 | the triangle (0, 0), (6, 0), (2, 4) |
| (0, 0), (1, 1), (2, 2), (5, 5), (5, 5) | (5/2, 5/2) | 25/2 | the pair (0, 0), (5, 5) |

The second row is the standard trap. The circumcircle of the three points has center $(3, -2)$ and $r^2 = 13$, larger than the answer, because the angle at $(1, 1)$ is obtuse: the vectors to the other two points have dot product $(-1)(5) + (-1)(-1) = -4 < 0$. In the third row the triangle $(0, 0), (6, 0), (2, 4)$ is acute (its three angle dot products are $12$, $24$ and $8$), so its circumcircle is the answer; the inner points are at squared distances $8$ and $5$ from the center.

## Known algorithms

| algorithm | time | notes |
|---|---|---|
| brute force over pairs and triples | $O(n^4)$ | test each of the $O(n^3)$ candidate disks against all points |
| Elzinga and Hearn (1972) | polynomial | moves between 2-point and 3-point disks until the disk covers all points |
| farthest-point Voronoi diagram (Shamos and Hoey 1975) | $O(n \log n)$ | the center is a vertex of the [farthest-point Voronoi diagram](/farthest-point-voronoi-diagram/) or the midpoint of a [farthest pair](/farthest-pair/) |
| Megiddo (1983) | $O(n)$ worst case | [prune and search](/prune-and-search/); a large constant |
| [Welzl's algorithm](/welzls-algorithm/) (1991) | $O(n)$ expected | at most $10n$ expected containment tests |
| [Clarkson's algorithm](/clarksons-algorithm/), [LP-type](/lp-type-problem/) solvers | $O(n)$ expected | the problem has combinatorial dimension 3 |

On the [real RAM](/real-ram/) with rational input, the brute force and Welzl's algorithm work with exact rationals: the centers and the squared radii are rational, and no square root is needed.

## Bounds

- **Lower bound.** Every algorithm must read each point, because an unread point could lie outside any candidate disk. So $\Omega(n)$ time is needed in every model, and the $O(n)$ algorithms are optimal.
- **Deterministic upper bound.** $O(n)$ in the worst case, by Megiddo's algorithm.
- **Randomized upper bound.** $O(n)$ expected for every input, by Welzl's algorithm, with a small constant: at most $10n$ expected point-in-disk tests.
- **Output size.** The answer is a constant amount of data: a center, a radius and at most three points that fix them.

## Reductions

- **To a convex program.** Minimize $t$ subject to $|p - z|^2 \le t$ for all $p \in P$. Each constraint is a convex quadratic in $(z, t)$. The program is a [second-order cone program](/second-order-cone-programming/).
- **As an LP-type problem.** The pair (constraints $P$, value $r^*$) is an [LP-type problem](/lp-type-problem/) of combinatorial dimension 3. So every LP-type algorithm (Clarkson, Sharir and Welzl, Matoušek, Sharir and Welzl) solves it in expected linear time.
- **To linear programming in 3 variables.** Lifting $p \mapsto (x, y, x^2 + y^2)$ turns "the disk with center $z$ and squared radius $r^2$ contains $p$" into a linear inequality in $(z_x, z_y, r^2 - |z|^2)$. The objective $r^2$ stays quadratic in $z$, so this is not a plain linear program. Megiddo's 1983 paper solves the circle problem with its own prune-and-search step.
- **From the farthest-point Voronoi diagram.** Given the diagram, the answer is found in $O(n)$ time by checking its vertices and the midpoint of the farthest pair.

## Applications

- **Facility location.** Place a siren, an antenna or a hospital so that the farthest client is as near as possible (the minimax criterion). See [facility location](/facility-location-problem/).
- **Bounding volumes.** A bounding circle or sphere gives a cheap first test in [collision detection](/collision-detection/) and in ray tracing.
- **Clustering.** It is the step that evaluates one cluster in [k-center](/k-center-problem/) clustering.
- **Robust statistics and shape.** The radius is a measure of spread that ignores the inner points.

## References
