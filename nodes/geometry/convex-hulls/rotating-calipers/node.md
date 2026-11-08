---
tag: KS3298
kind: technique
slug: rotating-calipers
name: Rotating calipers
aliases:
- calipers method
- rotating callipers
- rotating caliper method
area: geometry/convex-hulls
level: core
summary: Sweeps a pair of parallel supporting lines around a convex polygon to find diameter, width and antipodal pairs in linear time.
prereqs: [convex-hull-problem, orientation-test, supporting-hyperplane, two-pointers]
see_also: [antipodal-pairs, polygon-diameter, polygon-width, minimum-area-enclosing-rectangle, minkowski-sum-convex-polygons, convex-polygon-intersection, farthest-pair, graham-scan]
sources:
  - paper: "Godfried T. Toussaint, Solving geometric problems with the rotating calipers, Proceedings of IEEE MELECON 1983, Athens"
    locator: the whole paper (the name, the template, and linear-time solutions for the minimum-area rectangle and other problems)
  - paper: "Michael Ian Shamos, Computational Geometry, PhD thesis, Yale University, 1978"
    locator: the diameter of a convex polygon by antipodal pairs
  - paper: doi:10.1145/360881.360919
    title: Herbert Freeman and Ruth Shapira, Determining the minimum-area encasing rectangle for an arbitrary closed curve, Communications of the ACM 18(7), 1975
    locator: the whole paper (a minimum-area enclosing rectangle has a side collinear with an edge of the hull)
  - paper: doi:10.1109/34.6790
    title: Michael E. Houle and Godfried T. Toussaint, Computing the width of a set, IEEE Transactions on Pattern Analysis and Machine Intelligence 10(5), 1988
    locator: the whole paper (the width is attained at an edge and an antipodal vertex, found by rotating calipers)
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 4, the diameter of a convex polygon by antipodal pairs
---

Rotating calipers is a technique for convex polygons. It places two parallel lines that touch the polygon on opposite sides, like the jaws of a caliper, and turns them once around the polygon. At every moment each line touches a vertex or an edge, and the jaws only move forward, so the whole turn visits $O(h)$ pairs of touching points on a polygon with $h$ vertices, in $O(h)$ time. Many questions about a convex shape, such as its diameter, its width, its smallest enclosing rectangle or the bridges between two convex polygons, have their answer at one of these positions.

## In plain words

Hold a convex shape in a caliper so that both jaws touch it. Now turn the caliper slowly around the shape, keeping both jaws in touch. One jaw lies flat on some side for a moment, then rolls over a corner onto the next side. The other jaw does the same on the far side.

Each jaw goes around the shape exactly once, and it never goes back. So the number of positions where something changes is small: about the number of corners, twice.

Many measurements of the shape are best at one of those positions. The greatest distance across is between two corners that the jaws touch at the same time. The smallest gap between the jaws comes when one jaw lies flat on a side. So you check only these positions, not every pair of corners.

## When it applies

- **The input is a convex polygon**, or can be made one: the [convex hull](/convex-hull-problem/) of a point set, a convex obstacle, or the sum of two convex shapes. The vertices are in counterclockwise order.
- **The answer is fixed by a direction.** The quantity to optimize is a function of a direction $u$ and of the vertices extreme in $u$ and in $-u$ (or in a few directions at fixed angles to $u$). Examples are the distance between the two supporting lines, the length of a chord between their touching points, or the area of a rectangle with sides along $u$ and $u^\perp$.
- **Optimum at a critical direction.** One can prove that the optimum is reached at a direction where a supporting line contains an edge, or at a pair of vertices that are touched together. Then only $O(h)$ candidate directions need checking.
- **Two pointers on a cycle.** The extreme vertex in a direction moves forward monotonically as the direction turns counterclockwise. This is the signal: a nested loop over pairs of vertices can be replaced by two (or four) pointers that each go around once, like [two pointers](/two-pointers/) on a sorted array.

## The template

Notation: $Q = q_0, \ldots, q_{h-1}$ are the vertices of a convex polygon in counterclockwise order, with indices modulo $h$, $h \ge 3$, and no three consecutive vertices collinear (strictly convex). $P$ is the original point set when $Q$ is its hull, $n = |P|$. $\mathrm{orient}(p, q, r)$ is the sign of

$$D(p, q, r) = (q_x - p_x)(r_y - p_y) - (q_y - p_y)(r_x - p_x),$$

positive for a counterclockwise turn ([orientation test](/orientation-test/)). For a fixed edge $q_i q_{i+1}$, $D(q_i, q_{i+1}, r)$ is $|q_{i+1} - q_i|$ times the distance from $r$ to the edge line, so the vertex with the largest $D$ is the one farthest from the edge. A vertex $q_j$ is **antipodal** to the edge $q_i q_{i+1}$ if it is farthest from its line; two vertices form an **antipodal pair** if they admit parallel supporting lines.

```pseudo id=main
ROTATING-CALIPERS(Q)
L1  h ← |Q|; j ← 1; INIT
L2  for i ← 0 to h − 1 do
L3      while D(q_i, q_{i+1}, q_{j+1}) > D(q_i, q_{i+1}, q_j) do j ← j + 1
L4      VISIT(i, j)        ▷ q_j is a vertex farthest from the line of the edge q_i q_{i+1}
L5  return RESULT
```

The holes are `INIT` (the starting value of the answer and of any further pointers), `VISIT(i, j)` (what to compute for the edge $q_i q_{i+1}$ and its antipodal vertex $q_j$) and `RESULT`.

- **Line L3, why it finds the farthest vertex.** Walk along the polygon from $q_{i+1}$. The step along the edge $q_k q_{k+1}$ changes $D(q_i, q_{i+1}, \cdot)$ by $D(q_i, q_{i+1}, q_i + (q_{k+1} - q_k))$, the cross product of the two edge directions. The edge directions turn counterclockwise through one full turn, so this change is positive while the turn angle from edge $i$ is below $\pi$, zero for one edge parallel to edge $i$ (if there is one), and negative after. So the distance to the edge line rises, stays flat for at most one step, then falls. The loop stops at the first farthest vertex.
- **Line L3, why $j$ never goes back.** When $i$ moves to $i + 1$, the edges before the current $j$ have turn angles from edge $i + 1$ that are smaller than from edge $i$, and still nonnegative, so the distance to the new edge line is still rising up to $q_j$. The pointer can continue from where it is.
- **Cost.** The pointer $j$ starts at $1$, ends below $2h$, and only increases, so line L3 runs $O(h)$ times in total. With $O(1)$ work in `VISIT`, the template takes $\Theta(h)$ time and $O(1)$ extra space. Every test is a comparison of integer polynomials of degree 2 in the coordinates, so it is exact on integer input.
- **Antipodal pairs.** All antipodal vertex pairs appear as $(q_i, q_j)$ or $(q_{i+1}, q_j)$ at line L4, plus $(q_i, q_{j+1})$ and $(q_{i+1}, q_{j+1})$ when the edge $q_j q_{j+1}$ is parallel to $q_i q_{i+1}$ (the test of line L3 is then an equality). There are at most $\lfloor 3h/2 \rfloor$ of them; see [antipodal pairs](/antipodal-pairs/).

### Example

Take the convex polygon $(0,0)$, $(4,0)$, $(5,3)$, $(3,5)$, $(0,4)$ (the hull of the ten points used on the [Graham scan](/graham-scan/) page). Fill the holes for the squared diameter (`VISIT` takes the larger of $|q_i - q_j|^2$ and $|q_{i+1} - q_j|^2$, `RESULT` the maximum) and for the squared width (`VISIT` takes $D^2 / |q_{i+1} - q_i|^2$, `RESULT` the minimum).

| $i$ | edge $q_i q_{i+1}$ | antipodal $q_j$ | $D$ | $\lvert e \rvert^2$ | height$^2 = D^2 / \lvert e \rvert^2$ | $\lvert q_i - q_j \rvert^2$ | $\lvert q_{i+1} - q_j \rvert^2$ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | (0,0), (4,0) | (3,5) | 20 | 16 | 25 | 34 | 26 |
| 1 | (4,0), (5,3) | (0,4) | 16 | 10 | 25.6 | 32 | 26 |
| 2 | (5,3), (3,5) | (0,0) | 16 | 8 | 32 | 34 | 34 |
| 3 | (3,5), (0,4) | (4,0) | 16 | 10 | 25.6 | 26 | 32 |
| 4 | (0,4), (0,0) | (5,3) | 20 | 16 | 25 | 26 | 34 |

The pointer $j$ moved 6 times in total. The diameter is $\sqrt{34}$, between $(0,0)$ and $(5,3)$ and also between $(0,0)$ and $(3,5)$. The width is $5$, reached at the edges $0$ and $4$. With two more calipers for the extreme vertices along the edge direction, the smallest enclosing rectangle has area 25, the $5 \times 5$ square with a side on the edge $(0,0), (4,0)$. These values were checked against a brute force over all pairs and all edges, on this polygon and on about 3000 random hulls.

## Classic examples

- **[Antipodal pairs](/antipodal-pairs/).** `VISIT` reports the pairs listed above. This is the base of the other examples.
- **[Diameter of a convex polygon](/polygon-diameter/) and [farthest pair](/farthest-pair/).** The two farthest points of a set are an antipodal pair of its hull. `VISIT` checks $|q_i - q_j|$ and $|q_{i+1} - q_j|$, `RESULT` is the maximum. With a hull algorithm such as the [Graham scan](/graham-scan/), the farthest pair of $n$ points takes $O(n \log n)$ time, against $\Theta(n^2)$ for all pairs. Shamos gave this method in 1978.
- **[Width of a convex polygon](/polygon-width/).** The width is the smallest distance between two parallel supporting lines. It is reached when one line contains an edge (Houle and Toussaint), so `VISIT` takes the distance from $q_j$ to the line of the edge, and `RESULT` is the minimum.
- **[Minimum-area enclosing rectangle](/minimum-area-enclosing-rectangle/).** Freeman and Shapira proved that some smallest enclosing rectangle has a side on a hull edge. `INIT` adds two more pointers, for the vertices with the largest and the smallest projection on the edge direction; both also move forward only. `VISIT` computes the area $D \cdot (\langle e, q_k \rangle - \langle e, q_l \rangle) / |e|^2$, exactly as a fraction. Toussaint gave this four-caliper version in linear time in 1983.
- **[Minkowski sum of convex polygons](/minkowski-sum-convex-polygons/).** Two calipers, one on each polygon, turn together in the same direction; at each step the polygon whose next edge has the smaller angle advances. The edges come out sorted by angle, and their sum is the boundary of the sum polygon, in $O(h_1 + h_2)$ time.
- **[Intersection of convex polygons](/convex-polygon-intersection/).** Calipers on both polygons find the bridges and the pockets between them; linear-time methods for the intersection and for the hull of the union use this idea.

## Variations

- **Two polygons.** Put one jaw on each polygon. With the jaws on opposite sides and pointing the same way, they find the largest distance between the polygons; with both jaws on the same side, they find the common tangents (bridges) used to merge hulls, as in the [divide-and-conquer hull](/divide-and-conquer-convex-hull/).
- **More than two calipers.** Rectangles use four lines at right angles, and other enclosing shapes use lines at other fixed angles. Each extra caliper is one more pointer that only moves forward.
- **Vertex-vertex form.** Instead of stepping edge by edge on one side, advance whichever jaw has the smaller angle to its next edge. This visits each antipodal pair once and is the form used for the Minkowski sum.
- **Upper and lower hull form.** For the diameter, run one pointer on the [upper hull](/upper-and-lower-hull/) and one on the lower hull, both from left to right. This avoids the modular indices.
- **Point sets in higher dimensions.** The idea does not carry over directly: in three dimensions the antipodal pairs of a polytope can number $\Theta(n^2)$, and the diameter of $n$ points in $\mathbb{R}^3$ needs other methods.

## Pitfalls

- **Collinear vertices.** The template assumes a strictly convex polygon. With a vertex in the middle of an edge, the distance stays flat for one step before its maximum, line L3 stops too early, and the answer is wrong. For $Q = (0,3), (1,2), (2,1), (4,2)$, where $(1,2)$ lies on the edge from $(0,3)$ to $(2,1)$, the squared diameter computed is 9, but the true value is 17, from $(0,3)$ to $(4,2)$. Build the hull with collinear points removed, or skip them before the turn.
- **Clockwise input.** With the vertices in clockwise order, $D$ is negative for every vertex, and the loop of line L3 stops at once. Reverse the order first, or test the sign of the area.
- **Degenerate hulls.** If the hull has one or two vertices, the polygon has no edges in the sense of the template. Handle $h \le 2$ separately: the diameter is the segment, and the width is 0.
- **Square roots and floating point.** Compare $D$ values and squared lengths, or fractions such as $D^2 / |e|^2$, and take a square root only at the end. Floating-point heights can make line L3 move past the true maximum when two vertices are almost equally far.
- **Checking only $(q_i, q_j)$.** For the diameter, each step must also check $q_{i+1}$ against $q_j$; with only one of the two, some antipodal pairs are missed.

## Exercises

1. Prove that the two farthest points of a finite point set form an antipodal pair of its convex hull. (Hint: the lines through each of them perpendicular to the segment between them support the hull.)
2. Prove that a strictly convex polygon with $h$ vertices has at most $\lfloor 3h/2 \rfloor$ antipodal pairs, and give a polygon that reaches the bound.
3. Adapt the four-caliper rectangle method to find an enclosing rectangle of minimum perimeter in $O(h)$ time. Is the perimeter also smallest when a side lies on an edge?
4. Given two disjoint convex polygons with $h_1$ and $h_2$ vertices, find the largest distance between a point of the first and a point of the second in $O(h_1 + h_2)$ time.

## References
