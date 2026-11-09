---
tag: YZ6SAX
kind: problem
slug: watchman-route-problem
name: Watchman route problem
aliases:
- shortest watchman route
- watchman tour
- shortest watchman route problem
area: geometry/polygons
level: advanced
summary: Find the shortest closed route inside a polygon from which every point is visible.
prereqs: [simple-polygon, art-gallery-problem, euclidean-shortest-path-in-polygon]
see_also: [art-gallery-problem, traveling-salesman-problem, euclidean-tsp, euclidean-shortest-path-in-polygon, visibility-polygon, polygon-kernel, np-hard, funnel-algorithm]
sources:
  - paper: "Wei-Pang Chin and Simeon Ntafos, Shortest watchman routes in simple polygons, Discrete and Computational Geometry 6(1), 9 to 31 (1991)"
    locator: the essential cuts, the lemma that a route sees the polygon exactly when it meets every essential cut, the reflection principle, and the polynomial algorithm for a fixed starting point
  - paper: doi:10.1007/PL00009467
    title: Svante Carlsson, Håkan Jonsson and Bengt J. Nilsson, Finding the shortest watchman route in a simple polygon, Discrete and Computational Geometry 22(3), 377 to 402 (1999)
    locator: the polynomial algorithm for the floating watchman route, with no given starting point
  - paper: "Moshe Dror, Alon Efrat, Anna Lubiw and Joseph S. B. Mitchell, Touring a sequence of polygons, Proceedings of the 35th ACM Symposium on Theory of Computing, 473 to 482 (2003)"
    locator: the shortest path visiting a sequence of convex regions, and its application to the fixed watchman route in O(n^3 log n) time
  - paper: "Joseph S. B. Mitchell, Approximating watchman routes, Proceedings of the 24th ACM-SIAM Symposium on Discrete Algorithms (2013)"
    locator: the polylogarithmic approximation for polygons with holes and the matching logarithmic inapproximability
---

The watchman route problem asks for the shortest closed route inside a polygon $P$ such that every point of $P$ is seen from some point of the route. It is the mobile version of the [art gallery problem](/art-gallery-problem/): one guard walks instead of many guards standing still. In a [simple polygon](/simple-polygon/) it is solvable in polynomial time, because a route sees all of $P$ exactly when it touches a set of at most $n$ segments, the **essential cuts**, in boundary order, which turns the problem into a shortest path that touches a sequence of segments. Chin and Ntafos introduced it in 1986 and solved the version with a fixed starting point in 1991; the version without a starting point was solved by Carlsson, Jonsson and Nilsson in 1999. In a polygon with holes the problem is NP-hard, since it contains the [Euclidean traveling salesman problem](/euclidean-tsp/).

## In plain words

A night guard must walk through a building with many corners and come back to where they started. Every spot of the building has to come into view at some moment during the walk. Among all such walks, you want the shortest one.

In a building without pillars, each corner that points into the room hides a pocket behind it. Standing anywhere in the room, you see into the pocket only from places that are in line with the wall behind the corner or beyond it. So the walk must touch a line drawn by extending that wall, one line for each hidden pocket. Then the task becomes: find the shortest loop that touches all these lines, in their order around the building.

## Definition

**Input.** A simple polygon $P$ with $n$ vertices, identified with its closed region, and, in the **fixed** version, a starting point $s$ on $\partial P$ or in $P$. In the **floating** version there is no starting point.

**Output.** A shortest closed curve $R \subseteq P$, through $s$ in the fixed version, such that every point $q \in P$ sees some point $z \in R$, that is, the segment $zq$ lies in $P$.

**Model.** The [real RAM](/real-ram/) with square roots, since lengths of routes are sums of square roots. Comparing two such sums exactly is a known open problem in itself; algorithms are stated with exact comparisons of lengths assumed.

**General position.** No three vertices are collinear, so cuts end in the relative interior of an edge. Degenerate input is handled by closed visibility, where a segment may run along $\partial P$.

**Essential cuts.** Let $v$ be a reflex vertex of $P$ and $e$ an edge incident to $v$, with line $\ell$. Extend $e$ beyond $v$ into $P$ until it first meets $\partial P$; this segment $C$ is a **cut**. It splits $P$ into two parts; call the closed part that contains $e$ the **pocket** $\Pi(C)$.

**Lemma.** If a route $R \subseteq P$ sees every point of $P$, it meets $\Pi(C)$ for every cut $C$.

*Proof.* Suppose $R \cap \Pi(C) = \emptyset$, and take $q$ in the relative interior of $e$. Let $z \in R$ see $q$. As $z \notin \Pi(C)$ and $q \in \Pi(C)$, the segment $zq$ crosses $C$ at some point $c \ne q$. Then $c$ and $q$ are both on $\ell$, so $z \in \ell$ as well, and the segment $zq$ runs along $\ell$. The point $z$ lies on the side of $v$ away from $q$, and the segment $zq$ stays in $P$, so it can only run along $C$ there, since $C$ ends where $\ell$ crosses $\partial P$; so $z \in C \subseteq \Pi(C)$, a contradiction. $\square$

The converse also holds (Chin and Ntafos): a closed route that meets every pocket sees all of $P$. If $\Pi(C) \subseteq \Pi(C')$, meeting $\Pi(C)$ implies meeting $\Pi(C')$, so only the minimal pockets matter; their cuts are the **essential cuts**. In the fixed version, cuts whose pocket contains $s$ are met automatically and are dropped. There are at most $2r$ cuts for $r$ reflex vertices, and they are found in $O(n \log n)$ time by ray shooting in $P$.

**Shortest route.** A shortest route meets the essential cuts in their order along $\partial P$, and where it touches a cut without crossing it, it reflects like a light ray: the angle of arrival equals the angle of departure. Between cuts it follows [shortest paths inside $P$](/euclidean-shortest-path-in-polygon/). Unfolding the polygon by reflecting across the cuts turns the route into a straight geodesic, which is the basis of the algorithms.

**Star-shaped polygons.** If $P$ is [star-shaped](/star-shaped-polygon/), one point of the [kernel](/polygon-kernel/) sees all of $P$, and the floating route has length 0. The problem is interesting only when the kernel is empty or a starting point is given outside it.

## Variants

- **Fixed or floating.** With a given start point on the boundary or not.
- **Orthogonal polygons.** For [rectilinear polygons](/rectilinear-polygon/), Chin and Ntafos gave an $O(n)$ algorithm.
- **Polygons with holes.** NP-hard; approximation algorithms exist.
- **Limited visibility.** The watchman sees only within a distance $d$, which turns the problem into a covering tour, closer to lawn mowing and milling.
- **Several watchmen.** Minimize the longest or the total length of $k$ routes that together see $P$.
- **Related tours.** The zookeeper problem, where the route must touch convex cages attached to the boundary without entering them; the safari problem, where it must enter them; and the aquarium keeper problem.
- **Watchman paths.** Open routes between two given points.

## Examples

All polygons are counterclockwise; visibility is closed.

- **A convex polygon or any star-shaped polygon.** The floating route is a single point of the kernel, length 0.
- **The U-shape.** $(0,0), (3,0), (3,3), (2,3), (2,1), (1,1), (1,3), (0,3)$ has an empty kernel. Its reflex vertices $(2,1)$ and $(1,1)$ give four cuts. Extending the edge from $(2,3)$ to $(2,1)$ down to $(2,0)$ gives the pocket $[2,3] \times [0,3]$, and extending the edge from $(1,1)$ to $(1,3)$ down to $(1,0)$ gives $[0,1] \times [0,3]$. The other two cuts, $(2,1)\text{--}(3,1)$ and $(0,1)\text{--}(1,1)$, have larger pockets that contain these, so the two vertical cuts are the essential ones. A closed route must meet $\{x \le 1\}$ and $\{x \ge 2\}$, so its length is at least 2, and the route from $(1, \frac12)$ to $(2, \frac12)$ and back, of length 2, sees all of $P$. The shortest floating route has length 2.
- **The same U-shape from a start point.** With $s = (\frac32, 0)$, the route $(\frac32, 0), (1,0), (2,0), (\frac32, 0)$ has length 2 and is again optimal by the same bound.

## Known algorithms

| setting | time | source |
| --- | --- | --- |
| orthogonal simple polygon | $O(n)$ | Chin and Ntafos, 1986 |
| simple polygon, fixed start | $O(n^4)$, after a correction of the original analysis | Chin and Ntafos, 1991; corrected by Tan, Hirata and Inagaki |
| simple polygon, fixed start | $O(n^3 \log n)$ | Dror, Efrat, Lubiw and Mitchell, 2003, by touring a sequence of polygons |
| simple polygon, floating | $O(n^6)$ | Carlsson, Jonsson and Nilsson, 1999 |
| simple polygon, floating | $O(n^5)$ | Tan |
| polygon with holes | NP-hard; polylogarithmic approximation | Chin and Ntafos; Mitchell, 2013 |

The fixed-start algorithms compute the essential cuts, then find the shortest route touching them in boundary order by an iterative unfolding or by the touring-polygons method. For the floating version no start point is known, and the algorithms reduce it to fixed-start problems for a polynomial number of candidate positions on the essential cuts, which gives the extra factors of $n$.

## Bounds

- **Lower bound.** $\Omega(n)$, to read the input; the polynomial upper bounds above are far from it, and no superlinear lower bound is known for simple polygons.
- **Hardness with holes.** A polygon with tiny square holes placed at given points forces the route to visit each hole, up to a small error, so it solves the Euclidean [traveling salesman problem](/traveling-salesman-problem/), which is [NP-hard](/np-hard/). Mitchell (2013) showed that the problem with holes is also hard to approximate within a factor $o(\log n)$, and gave an $O(\log^2 n)$-approximation.

## Reductions

- **Watchman route to touring segments.** By the lemma, the fixed version is the shortest closed path in $P$ from $s$ that touches the essential cuts in order, a case of touring a sequence of convex regions.
- **TSP to watchman route with holes.** As above, which gives the NP-hardness.
- **Single guard to watchman route.** A route of length 0 exists exactly when $P$ is star-shaped, so testing it is the [kernel](/polygon-kernel/) computation.
- **Shortest paths as a subroutine.** Each part of the route between two cuts is an [Euclidean shortest path in the polygon](/euclidean-shortest-path-in-polygon/), computed with the [funnel algorithm](/funnel-algorithm/).

## Applications

- **Security patrols.** Planning a guard's tour through a building or a warehouse.
- **Robot inspection and mapping.** A robot with a camera or a laser scanner that must see every wall of an indoor space, for example to build a map or to inspect for damage.
- **Search.** Searching a polygon for a stationary target, where every point must come into view once.
- **Computer graphics.** Camera paths that show every part of a scene.

## References
