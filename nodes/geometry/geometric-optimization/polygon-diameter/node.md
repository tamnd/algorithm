---
tag: 08DX54
kind: problem
slug: polygon-diameter
name: Polygon diameter
aliases:
- farthest pair of a convex polygon
- diameter of a convex polygon
area: geometry/geometric-optimization
level: core
summary: Find the two points of a convex polygon at the largest distance. The answer is an antipodal vertex pair, so rotating calipers find it in O(n) time.
prereqs: [convex-polygon, antipodal-pairs, rotating-calipers]
see_also: [farthest-pair, polygon-width, minimum-area-enclosing-rectangle, minimum-enclosing-circle, farthest-point-voronoi-diagram, convex-hull-problem, element-distinctness-lower-bound, coreset]
sources:
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 4, the diameter of a set (the antipodal-pair theorem, the O(n) algorithm for a convex polygon, and the Omega(n log n) lower bound for point sets)
  - paper: "Michael Ian Shamos, Computational Geometry, PhD thesis, Yale University, 1978"
    locator: the linear-time diameter of a convex polygon
  - paper: "Godfried T. Toussaint, Solving geometric problems with the rotating calipers, Proceedings of IEEE MELECON 1983, Athens"
    locator: the diameter as the first application of the rotating calipers
  - paper: "David Avis, Godfried T. Toussaint and Binay K. Bhattacharya, On the multimodality of distances in convex polygons, Computers and Mathematics with Applications 8(2), 1982"
    locator: the distance from a vertex along a convex polygon can have many local maxima, which breaks several published diameter algorithms
  - paper: "Edgar A. Ramos, An optimal deterministic algorithm for computing the diameter of a three-dimensional point set, Discrete and Computational Geometry 26(2), 2001"
    locator: the deterministic O(n log n) diameter in three dimensions
  - paper: doi:10.1007/BF02187740
    title: Kenneth L. Clarkson and Peter W. Shor, Applications of random sampling in computational geometry, II, Discrete and Computational Geometry 4, 1989
    locator: the randomized O(n log n) expected-time diameter in three dimensions
---

The polygon diameter problem asks for the largest distance between two points of a [convex polygon](/convex-polygon/), and for a pair that attains it. The farthest pair is always a pair of vertices, and more precisely an [antipodal pair](/antipodal-pairs/), so the [rotating calipers](/rotating-calipers/) find it in $O(n)$ time from the vertex list. For a set of points that is not yet a polygon, this is the [farthest pair](/farthest-pair/) problem: compute the [convex hull](/convex-hull-problem/) first, which costs $\Theta(n \log n)$ in the worst case.

## In plain words

You have a convex shape with straight sides, and you want the two points of it that are farthest apart, as for the longest stick that fits in it. The two points are always corners. You could test every pair of corners, but that is slow for a shape with many corners.

A faster way uses a caliper. Close the two jaws on the shape. The two touching corners are a candidate pair. Turn the shape. The touching corners change one at a time, and each new contact gives a new candidate. The farthest pair is always one of these candidates, so half a turn finds it. The number of candidates is at most one and a half times the number of corners.

## Definition

Notation: $P$ is a convex polygon with vertices $p_0, \ldots, p_{n-1}$ in counterclockwise order, $n \ge 2$; a point is $p = (x, y)$; $\mathrm{orient}(p, q, r)$ is the sign of $(q - p) \times (r - p)$.

**Input.** The vertices of $P$ in counterclockwise order. Collinear consecutive vertices and repeated vertices are allowed if the code first removes them; the standard walk assumes a strictly convex list.

**Output.** $\operatorname{diam} P = \max_{a, b \in P} |a - b|$ and a pair of vertices $(p_i, p_j)$ that attains it.

**Theorem 1 (vertices).** The maximum is attained at two vertices. *Proof.* For a fixed $b$, the function $a \mapsto |a - b|$ is convex, so its maximum over the polygon $P = \operatorname{conv}\{p_k\}$ is attained at a vertex. Apply this to $a$, then to $b$. $\square$

**Theorem 2 (antipodal).** If $|p_i - p_j| = \operatorname{diam} P$, then $p_i$ and $p_j$ are antipodal: the two lines through $p_i$ and $p_j$ perpendicular to $p_i p_j$ support $P$. *Proof.* Let $u = (p_j - p_i)/|p_j - p_i|$. If a point $a \in P$ had $\langle u, a \rangle > \langle u, p_j \rangle$, then $|a - p_i| \ge \langle u, a - p_i \rangle > |p_j - p_i|$, a contradiction. The same holds at $p_i$ with $-u$. So $P$ lies in the slab between the two perpendicular lines, and they are distinct parallel supporting lines. $\square$

So the diameter is the largest distance over the at most $\lfloor 3n/2 \rfloor$ antipodal pairs. With integer vertices, compare squared distances, which are integers; the only square root is the final one, if a length is needed.

## Variants

- **Point sets.** The [farthest pair](/farthest-pair/) of $n$ points: the answer is a pair of hull vertices.
- **Simple polygons.** The Euclidean diameter of a simple polygon equals that of its convex hull, which takes $O(n)$ time for a simple polygon by [Melkman's algorithm](/melkman-algorithm/).
- **Higher dimensions.** In $\mathbb{R}^3$ the diameter of $n$ points takes $O(n \log n)$ expected time by the random sampling of Clarkson and Shor, and the same bound deterministically by Ramos (2001). In fixed dimension $d \ge 4$ no near-linear exact algorithm is known.
- **Approximation.** A $(1 + \varepsilon)$-approximation needs only the extent in a set of directions, or a [coreset](/coreset/) of the input.
- **Other metrics.** In the plane, the $L_1$ diameter is the larger of the ranges of $x + y$ and of $x - y$, and the $L_\infty$ diameter is the larger of the ranges of $x$ and of $y$, so both take $O(n)$ time for any point set.

## Examples

**The pentagon** $(0, 0), (4, 0), (5, 3), (3, 5), (0, 4)$. Its five antipodal pairs have squared distances

| pair | squared distance |
|---|---|
| (0, 0), (5, 3) | 34 |
| (0, 0), (3, 5) | 34 |
| (4, 0), (3, 5) | 26 |
| (4, 0), (0, 4) | 32 |
| (5, 3), (0, 4) | 26 |

so $\operatorname{diam} P = \sqrt{34}$, attained by two pairs. The brute force over all $\binom{5}{2} = 10$ pairs gives the same value; the pairs that are not antipodal are neighbors on an edge.

**The hexagon** $(0, 0), (4, 0), (6, 2), (6, 4), (2, 4), (0, 2)$ has 9 antipodal pairs, and the diameter is $\sqrt{52}$, between $(0, 0)$ and $(6, 4)$.

**A trap.** In the hexagon $(1, 3), (3, 0), (8, 3), (7, 7), (5, 8), (4, 7)$, the squared distances from $(8, 3)$ to the other vertices, in counterclockwise order, are $17, 34, 32, 49, 34$. They rise to 34, fall to 32 and rise again to 49. A walk that stops at the first local maximum reports 34, but the farthest vertex from $(8, 3)$ is $(1, 3)$ at squared distance 49.

## Known algorithms

| algorithm | input | time |
|---|---|---|
| all pairs | any $n$ points | $\Theta(n^2)$ |
| [rotating calipers](/rotating-calipers/) over antipodal pairs (Shamos 1978) | convex polygon | $\Theta(n)$ |
| hull, then rotating calipers | $n$ points in the plane | $O(n \log n)$, or $O(n \log h)$ with an output-sensitive hull |
| Clarkson and Shor (1989) | $n$ points in $\mathbb{R}^3$ | $O(n \log n)$ expected |
| Ramos (2001) | $n$ points in $\mathbb{R}^3$ | $O(n \log n)$ worst case |

The calipers walk for a convex polygon. For each edge $p_i p_{i+1}$, advance $j$ while the triangle $p_i p_{i+1} p_{j+1}$ has a larger area than $p_i p_{i+1} p_j$, that is while the cross product $(p_{i+1} - p_i) \times (p_{j+1} - p_j)$ is positive. The vertex $p_j$ that is farthest from the line of the edge is antipodal to both $p_i$ and $p_{i+1}$, so test the two distances $|p_i p_j|$ and $|p_{i+1} p_j|$. The distance to the line of a fixed edge is unimodal along the polygon, so the pointer $j$ only moves forward, and it moves $O(n)$ times in total. The walk is exact: it uses only cross products and squared distances.

## Bounds

- **Convex polygon.** $\Theta(n)$: each vertex must be read, and the calipers take $O(n)$.
- **Point sets in the plane.** $\Theta(n \log n)$ in the [algebraic decision tree](/algebraic-decision-tree/) model. The lower bound is by reduction from set disjointness, which needs $\Omega(n \log n)$ by [Ben-Or's theorem](/ben-or-theorem/): map each number $a$ of the first set to the point at angle $a$ on the unit circle, and each number $b$ of the second set to the point at angle $b + \pi$. The diameter is 2 iff the two sets meet.
- **Output-sensitive.** $O(n \log h)$ for $n$ points with $h$ hull vertices, because the walk itself takes $O(h)$.

## Reductions

- **To antipodal pairs.** Theorems 1 and 2 reduce the diameter to a maximum over the $O(n)$ [antipodal pairs](/antipodal-pairs/).
- **To the farthest-point Voronoi diagram.** The farthest point from each vertex is read off the [farthest-point Voronoi diagram](/farthest-point-voronoi-diagram/). For a convex polygon this diagram takes $O(n)$ time, but the calipers are simpler.
- **Bounds on other measures.** $\operatorname{diam} P / 2 \le r^* \le \operatorname{diam} P / \sqrt{3}$ for the radius $r^*$ of the [minimum enclosing circle](/minimum-enclosing-circle/), and the width is at most the diameter.

## Applications

- **Shape description.** The diameter is the "length" of a shape in image analysis and in the inspection of parts, together with the [width](/polygon-width/).
- **Clustering.** The diameter of a cluster is the cost in diameter-based clustering.
- **Bounds for other algorithms.** Many approximation algorithms, such as those for [coresets](/coreset/) and enclosing shapes, start from a farthest pair to fix a scale and a direction.

## References
