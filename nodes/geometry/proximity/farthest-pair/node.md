---
tag: 8ERCFT
kind: problem
slug: farthest-pair
name: Farthest pair of points
aliases:
- point-set diameter
- diameter of a point set
- farthest pair
area: geometry/proximity
level: core
summary: Find two points of a set at the largest distance; the pair lies on the convex hull and is found by rotating calipers in O(n log n).
prereqs: [euclidean-distance, convex-hull, rotating-calipers]
see_also: [polygon-diameter, antipodal-pairs, closest-pair-of-points, farthest-point-voronoi-diagram, minimum-enclosing-circle, polygon-width, convex-hull-problem, proximity-problems]
sources:
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 4, Convex hulls, extensions and applications (the diameter of a set, antipodal pairs, and the lower bound by reduction from set disjointness)
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, 2nd edition, Cambridge University Press, 1998
    locator: Chapter 4, the diameter of a convex polygon by antipodal pairs
  - paper: "Michael Ian Shamos, Computational Geometry, PhD thesis, Yale University, 1978"
    locator: the diameter of a convex polygon by antipodal pairs in linear time
  - paper: "Kenneth L. Clarkson and Peter W. Shor, Applications of random sampling in computational geometry, II, Discrete and Computational Geometry 4(5), 1989, 387-421"
    locator: the diameter of a point set in three dimensions in O(n log n) expected time
  - paper: "Edgar A. Ramos, An optimal deterministic algorithm for computing the diameter of a three-dimensional point set, Discrete and Computational Geometry 26(2), 2001, 233-244"
    locator: the deterministic O(n log n) algorithm in three dimensions
---

The farthest pair problem asks, for $n$ points in the plane, for two of them at the largest [Euclidean distance](/euclidean-distance/); that distance is the *diameter* of the set. The two points are always vertices of the [convex hull](/convex-hull/), and they form an [antipodal pair](/antipodal-pairs/), so after computing the hull in $O(n \log n)$ time, [rotating calipers](/rotating-calipers/) find the pair in $O(h)$ more time, where $h$ is the number of hull vertices. The total $O(n \log n)$ is optimal in the algebraic computation tree model. Unlike the [closest pair](/closest-pair-of-points/), the farthest pair is a global property: it depends only on the hull, and points inside the hull never matter.

## In plain words

You want the two dots on a map that are farthest apart. Checking every pair works but is slow for many dots.

The two farthest dots are always on the outside: if one of them were inside, you could move away from the other dot and still stay within the set, so some outer dot is even farther. So first find the outer boundary of the dots, the shape you get by stretching a rubber band around them.

Then squeeze the shape between two parallel rulers and turn them around it. The two farthest dots are touched by the rulers at the same moment, at some angle. Turning the rulers once around the shape visits every such touching pair, and only a few pairs need checking.

## Definition

**Input.** A list $P$ of $n \ge 2$ points $p = (x, y)$ in the plane, with integer or rational coordinates for exact algorithms. Duplicates and collinear points are allowed.

**Output.** Indices $i \ne j$ with

$$\|p_i - p_j\| = D(P) = \max_{a, b} \|p_a - p_b\|,$$

and usually the value $D(P)^2$. Any pair reaching the maximum is a correct answer. If all points are equal, $D(P) = 0$.

**Exactness.** As for the closest pair, compare the squared distances $(p_x - q_x)^2 + (p_y - q_y)^2$, which are exact integers for integer input. Rotating calipers also need the sign of a cross product to decide which caliper to advance; with integer coordinates it is an exact [orientation test](/orientation-test/).

**Model.** Algorithms are analyzed on the [real RAM](/real-ram/); the lower bound uses [algebraic computation trees](/algebraic-computation-tree/).

## Variants

- **Diameter of a convex polygon.** If the input is already the vertex list of a convex polygon in order, rotating calipers find the diameter in $O(n)$ time: see [polygon diameter](/polygon-diameter/).
- **All farthest neighbors.** For each point, find the point farthest from it. The [farthest-point Voronoi diagram](/farthest-point-voronoi-diagram/) answers this in $O(n \log n)$ time; each point's farthest neighbor is a hull vertex.
- **Bichromatic farthest pair.** The farthest red-blue pair; computable from the two hulls.
- **Higher dimensions.** In $\mathbb{R}^3$ the diameter takes $O(n \log n)$ expected time (Clarkson and Shor, 1989) and $O(n \log n)$ deterministic time (Ramos, 2001). In higher fixed dimensions no near-linear exact algorithm is known, and the hull can have $\Theta(n^{\lfloor d/2 \rfloor})$ faces, so the hull route fails.
- **Approximation.** For any point $p \in P$, the farthest point $q$ from $p$ satisfies $D(P)/2 \le \|p - q\| \le D(P)$, by the triangle inequality, in $O(n)$ time. Projecting on a few directions gives a $(1 + \varepsilon)$-approximation in $O(n / \sqrt{\varepsilon})$ time in the plane.
- **Width.** The smallest distance between two parallel lines enclosing the set is the [width](/polygon-width/), also found by rotating calipers on the hull.

## Examples

**Six points.** For $P = \{(1,1), (2,6), (3,4), (3,5), (4,8), (9,5)\}$ the convex hull, counterclockwise, is $(1,1), (9,5), (4,8), (2,6)$; the points $(3,4)$ and $(3,5)$ are inside. The squared distances between hull vertices are

| pair | $(1,1),(9,5)$ | $(1,1),(4,8)$ | $(9,5),(2,6)$ | $(9,5),(4,8)$ | $(1,1),(2,6)$ | $(4,8),(2,6)$ |
| --- | --- | --- | --- | --- | --- | --- |
| squared distance | 80 | 58 | 50 | 34 | 26 | 8 |

so the farthest pair is $(1,1)$, $(9,5)$ with $D^2 = 80$ and $D = 4\sqrt{5} \approx 8.94$. The same set is used on the [proximity problems](/proximity-problems/) page, where its closest pair is $(3,4)$, $(3,5)$.

**The 2-approximation.** From $p = (3,4)$ the farthest point is $(9,5)$ with squared distance $37$, about $6.08$. This is between $D/2 \approx 4.47$ and $D \approx 8.94$, as the bound promises.

**Points on a line.** For $\{(0,0), (2,1), (6,3), (4,2)\}$ the hull degenerates to the segment from $(0,0)$ to $(6,3)$, and the farthest pair is its two end points with $D^2 = 45$.

**Regular polygon.** For the $2m$ vertices of a regular polygon every vertex has an opposite vertex at distance $D$, so there are $m$ farthest pairs. Algorithms must handle ties.

## Known algorithms

| algorithm | time | idea |
| --- | --- | --- |
| brute force | $\Theta(n^2)$ | check every pair |
| [convex hull](/convex-hull-problem/) + [rotating calipers](/rotating-calipers/) (Shamos, 1978) | $O(n \log n)$ | the pair is antipodal on the hull; the calipers visit the $O(h)$ antipodal pairs |
| hull + calipers, output-sensitive | $O(n \log h)$ | an $O(n \log h)$ hull algorithm, then $O(h)$ |
| [farthest-point Voronoi diagram](/farthest-point-voronoi-diagram/) | $O(n \log n)$ | the farthest neighbor of each hull vertex; the largest gives $D$ |
| randomized in $\mathbb{R}^3$ (Clarkson and Shor, 1989) | $O(n \log n)$ expected | random sampling |
| deterministic in $\mathbb{R}^3$ (Ramos, 2001) | $O(n \log n)$ | derandomization |

Once the hull is known, the diameter of a convex polygon with $h$ vertices takes $\Theta(h)$, because it has at most $\lfloor 3h/2 \rfloor$ antipodal pairs and the calipers visit them in order.

## Bounds

- **Lower bound.** Deciding whether $D(P) \ge 2$ needs $\Omega(n \log n)$ operations in the algebraic computation tree model, so the hull plus calipers method is optimal. The proof reduces set disjointness: map the elements of two sets of reals injectively to points on an open quarter of the unit circle and the elements of the second set to the opposite points. Two points of the same set are less than $2$ apart, and an element of $A$ and one of $B$ are exactly $2$ apart when they are equal, so $D = 2$ exactly when the sets intersect. Set disjointness needs $\Omega(n \log n)$ by [Ben-Or's theorem](/ben-or-theorem/).
- **Upper bounds.** $O(n \log n)$ in the plane and in $\mathbb{R}^3$; $O(n \log h)$ in the plane with an output-sensitive hull; $O(h)$ after the hull.
- **No grid speedup.** The randomized grid trick that gives the closest pair in $O(n)$ expected time with floor has no direct analogue here, because the farthest pair is not local.

## Reductions

- **Farthest pair reduces to the convex hull.** After the hull, $O(h)$ time suffices. See [polygon diameter](/polygon-diameter/).
- **Set disjointness reduces to farthest pair**, as in the bound above.
- **Minimum enclosing circle.** The diameter gives a 2-approximation of the radius of the [minimum enclosing circle](/minimum-enclosing-circle/): $D/2 \le r \le D/\sqrt{3}$ (Jung's theorem in the plane).
- **Graph diameter is different.** The diameter of a graph, as in [tree diameter](/tree-diameter/), uses shortest-path distances, not straight-line ones, and needs different algorithms.

## Applications

- **Shape descriptors.** The diameter of a shape, sometimes called its Feret diameter or caliper length, is a basic size measure in image analysis and particle sizing.
- **Clustering.** The diameter of a cluster is the objective of [complete linkage clustering](/complete-linkage-clustering/) and of diameter-based $k$-clustering; [minimum diameter spanning trees](/minimum-diameter-spanning-tree/) are related in name but measure path length.
- **Bounding volumes.** The farthest pair gives the axis of a good bounding box or capsule, and a quick lower bound for the [minimum enclosing ball](/minimum-enclosing-ball/).
- **Coresets.** A small [coreset](/coreset/) of extreme points in a few directions preserves the diameter up to a factor $1 + \varepsilon$.

## References
