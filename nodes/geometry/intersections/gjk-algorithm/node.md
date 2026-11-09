---
tag: QSXJNC
kind: algorithm
slug: gjk-algorithm
name: Gilbert-Johnson-Keerthi algorithm
aliases:
- gjk
- gilbert-johnson-keerthi-algorithm
area: geometry/intersections
level: advanced
summary: Compute the distance between two convex shapes, or detect overlap, by walking a small simplex inside their Minkowski difference toward the origin using only support points.
solves: [convex-collision-detection]
model: real-ram
complexity:
  vars: {n: the total number of points of the two shapes, I: the number of iterations}
  time: {worst: O(I n)}
  space: {extra: Θ(1)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1988
  people: [Elmer G. Gilbert, Daniel W. Johnson, S. Sathiya Keerthi]
  note: Gilbert, Johnson and Keerthi published the distance algorithm for convex polytopes in three dimensions in 1988; later work extended it to general convex shapes, to incremental use between frames, and to penetration depth.
prereqs: [convex-collision-detection, minkowski-sum, support-function]
see_also: [separating-axis-theorem, chazelle-dobkin-algorithm, convex-polygon-intersection, collision-detection, convex-hull, bounding-volume-hierarchy, minkowski-sum-convex-polygons]
sources:
  - paper: doi:10.1109/56.2083
    title: Elmer G. Gilbert, Daniel W. Johnson and S. Sathiya Keerthi, A fast procedure for computing the distance between complex objects in three-dimensional space, IEEE Journal of Robotics and Automation 4(2), 1988
    locator: the iteration on the Minkowski difference with support points, the distance subalgorithm for a simplex, and the termination test
  - book: isbn:9781558607323
    title: Christer Ericson, Real-Time Collision Detection, Morgan Kaufmann, 2005
    locator: Chapter 9, Section 9.5, The Gilbert-Johnson-Keerthi algorithm (support mappings, the closest point of a simplex, and the stopping rule)
---

The Gilbert-Johnson-Keerthi algorithm, GJK for short, computes the distance between two convex shapes $P$ and $Q$. It never builds the Minkowski difference $M = P - Q$; it only asks for *support points*, the points of a shape that are farthest in a given direction. It keeps a simplex of at most three points of $M$ in the plane, or four in space, and the point $v$ of the simplex nearest to the origin. In each step it adds the support point of $M$ in direction $-v$ and moves $v$ closer to the origin, until no point of $M$ is closer. The shapes meet if and only if the final distance is $0$, so GJK is also an overlap test, and it is the usual narrow phase of physics engines.

## In plain words

Imagine all the arrows that go from a point of one shape to a point of the other. The shapes touch exactly when one of these arrows has length zero. These arrows, put at a common start, fill a new convex shape, and the question is whether it covers the start point, and if not, how close it comes.

GJK does not draw the new shape. It keeps a small triangle of known arrows and the point of the triangle closest to the start point. Then it asks each shape for its extreme point in the direction that could get closer, which gives a new arrow. If that arrow does not get closer, the answer is found. If it does, the triangle is updated and the search goes on.

## The problem

**Input.** Two finite nonempty point sets $P$ and $Q$ in $\mathbb{R}^2$ with rational coordinates; the shapes are their convex hulls. In general GJK needs only a support function for each shape.

**Output.** The squared distance $\delta^2 = \min \{|p - q|^2 : p \in \operatorname{conv} P, q \in \operatorname{conv} Q\}$, and the point $v \in M$ with $|v| = \delta$. If $\delta > 0$, the vector $-v$ points from $P$ toward $Q$ and separates them.

**Notation.** $M = \operatorname{conv} P - \operatorname{conv} Q$ is the Minkowski difference. $S_P(d)$ is a point of $P$ that maximizes $d \cdot p$, and $S_M(d) = S_P(d) - S_Q(-d)$ is a support point of $M$. $W$ is the current simplex, a set of at most $3$ points of $M$. $I$ is the number of passes through the loop.

**Model.** The [real RAM](/real-ram/). The implementation uses `Fraction`s, so the stopping test of line L5 is exact and the result is the exact squared distance.

## The algorithm

```pseudo id=main
GJK-DISTANCE(P, Q)
L1  v ← p₁ − q₁, W ← {v}                     ▷ any point of M
L2  loop
L3    if v = 0 then return 0                  ▷ 0 ∈ M: the shapes meet
L4    w ← S_P(−v) − S_Q(v)                     ▷ support point of M in direction −v
L5    if v·v − v·w ≤ 0 then return v·v         ▷ no point of M is nearer than v
L6    W ← W ∪ {w}
L7    v ← the point of conv W nearest to 0
L8    W ← a smallest subset of W with v in its hull
```

Line L4 costs one pass over each point set. Line L7 is the distance subalgorithm: for one point it is the point, for two points the projection of the origin on the segment, clamped to the end points, and for three points either $0$, if the triangle contains the origin, or the nearest of the three edge points. Line L8 keeps only the end points of the feature that holds $v$: a vertex, an edge or the full triangle, so $W$ never has more than $3$ points in the plane.

## Example

$P$ is the triangle $(0, 0), (4, 0), (0, 4)$ and $Q$ the triangle $(4, 3), (6, 3), (4, 5)$; on ties, the support takes the first point in the list.

| pass | $v$ | $S_P(-v)$ | $S_Q(v)$ | $w$ | $v \cdot v - v \cdot w$ | $W$ after L8 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | $(-4, -3)$ | $(4, 0)$ | $(4, 3)$ | $(0, -3)$ | $25 - 9 = 16$ | $\{(0, -3)\}$ |
| 2 | $(0, -3)$ | $(0, 4)$ | $(4, 3)$ | $(-4, 1)$ | $9 + 3 = 12$ | $\{(0, -3), (-4, 1)\}$ |
| 3 | $(-3/2, -3/2)$ | $(4, 0)$ | $(4, 3)$ | $(0, -3)$ | $9/2 - 9/2 = 0$ | stop |

In pass 1 the segment from $(-4, -3)$ to $(0, -3)$ is nearest to the origin at its end $(0, -3)$, so line L8 drops the first point. In pass 2 the origin projects onto the segment from $(0, -3)$ to $(-4, 1)$ at parameter $3/8$, which gives $v = (-3/2, -3/2)$. In pass 3 the new support point is already in $W$, the test of line L5 holds with equality, and the answer is $\delta^2 = 9/2$, so $\delta = 3 / \sqrt{2}$: the distance from the vertex $(4, 3)$ of $Q$ to the edge $x + y = 4$ of $P$.

## Correctness

Every point of $W$ is a point of $M$, so $v \in M$ by convexity. The support point $w$ minimizes $v \cdot m$ over $m \in M$, so every $m \in M$ has $v \cdot m \ge v \cdot w$. If $v \cdot w \ge |v|^2$, then $v \cdot m \ge |v|^2$ for all $m \in M$, and by the Cauchy-Schwarz inequality $|m| \ge |v|$: $v$ is the nearest point, which is line L5. Otherwise the segment from $v$ to $w$ starts in a direction that decreases $|x|^2$, since its derivative is $2 v \cdot (w - v) < 0$, so the new $v$ of line L7 is strictly nearer to $0$. Each $v$ is the nearest point of $\operatorname{conv} W$ for a set $W$ of at most $3$ points from the finite set $\{p - q\}$, and the norms strictly decrease, so no $W$ repeats and the loop ends. The full proof is in the proof file.

## Complexity

Each pass costs $O(n)$ for the two support points of line L4 and $O(1)$ for lines L5 to L8, so the time is $O(I n)$ and the extra space is $\Theta(1)$. The proof of termination gives only $I \le \binom{|P| |Q|}{3} + \binom{|P| |Q|}{2} + |P| |Q|$, the number of possible simplices; in practice $I$ is small, at most $5$ in the 1500 random tests of the implementation. With a hill-climbing support function on a polygon or polyhedron, line L4 costs much less than $O(n)$, and when the shapes move little between calls, starting from the last simplex makes most calls take one or two passes.

## Properties

- **Only support points.** The shapes enter only through $S_P$ and $S_Q$, so the same code works for polygons, polytopes, disks, capsules, and their Minkowski sums and convex hulls.
- **Distance and witness.** The result gives the distance, the nearest point $v$ of $M$ and a separating direction; the nearest points of $P$ and $Q$ follow from the same convex combination applied to the parts $S_P$ and $S_Q$ of the points of $W$.
- **Monotone.** $|v|$ strictly decreases in exact arithmetic, and $v \cdot w / |v|$ gives a lower bound on the distance at each pass.
- **Dimension.** In $\mathbb{R}^d$ the simplex has at most $d + 1$ points, and line L7 searches its faces.

## Variants and improvements

- **Boolean GJK.** For a pure overlap test, stop as soon as $v \cdot w > 0$: then the plane through the origin normal to $v$ separates, and the shapes are disjoint.
- **Johnson's subalgorithm.** The original paper computes line L7 by solving for the barycentric coordinates on all faces of the simplex with a recursive formula; later implementations use Voronoi region tests on the simplex.
- **Penetration depth.** When the shapes overlap, the expanding polytope algorithm grows a polytope inside $M$ from the final simplex toward the boundary of $M$ and returns the nearest boundary point, which gives the depth and the contact normal.
- **Incremental GJK.** Keep the simplex between calls for moving objects; this gives near-constant time per frame.
- **Floating point.** Implementations stop when $|v|^2 - v \cdot w \le \varepsilon |v|^2$ and guard against cycling, since rounding can make the strict decrease fail.

## When to use it

Use GJK as the narrow phase for convex shapes, after a broad phase with [bounding boxes](/axis-aligned-bounding-box/) or a [bounding volume hierarchy](/bounding-volume-hierarchy/), when you need the distance or the shapes are not polytopes. For two small polygons and a yes or no answer, the [separating axis test](/separating-axis-theorem/) is simpler. For an exact test with a proven logarithmic bound on large polygons stored in arrays, use the [Chazelle-Dobkin algorithm](/chazelle-dobkin-algorithm/).

## Pitfalls

- **A floating-point stop rule in line L5.** With rounding, $|v|^2 - v \cdot w$ can stay slightly positive while $v$ no longer moves, and a test for exact $0$ loops forever; float code needs a relative tolerance and an iteration limit, while exact code can use the test as written.
- **Wrong subset in line L8.** Keeping all of $W$, or keeping the wrong edge, breaks the invariant that $v$ is the nearest point of $\operatorname{conv} W$, and the loop may cycle.
- **Degenerate simplices in line L7.** Three collinear points have no triangle; the edge search must still return the right point, and a test for "origin inside the triangle" by orientation signs must skip a zero area.
- **Touching shapes in line L3.** Shapes that touch at one point give $\delta = 0$; code that treats $0$ as "no contact" misreports resting contact.
- **The sign of the direction in line L4.** The support of $M$ in direction $-v$ is $S_P(-v) - S_Q(v)$; swapping the signs gives the farthest point instead of the nearest.

## Implementations

## History

Gilbert, Johnson and Keerthi presented the algorithm in 1988 for the distance between convex polytopes in three dimensions, given by their vertices. Gilbert and Foo extended it to general convex sets in 1990, and Cameron and others made it incremental for moving objects. In games and physics engines it became the standard narrow-phase test through the work of van den Bergen around 1999 and the textbook of Ericson in 2005.

## References
