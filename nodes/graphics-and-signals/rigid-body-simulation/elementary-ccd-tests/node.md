---
tag: RXJ8EY
kind: algorithm
slug: elementary-ccd-tests
name: Vertex-face and edge-edge continuous collision tests
aliases:
- cubic CCD test
area: graphics-and-signals/rigid-body-simulation
level: advanced
summary: Find when a moving vertex hits a moving triangle or two edges meet by solving the cubic coplanarity equation and checking the contact point.
solves: [continuous-collision-detection]
model: floating-point-model
complexity:
  vars: {k: the number of bisection steps per root}
  time: {test: O(k), roots: O(1)}
  space: {extra: O(1)}
properties: {deterministic: true, online: false, recursive: false, exact: false}
history:
  year: 1997
  people: [Xavier Provot]
  note: Provot used the cubic coplanarity equation of a vertex and a triangle, and of two edges, with a check at each root, to find the collisions of cloth during a time step.
prereqs: [continuous-collision-detection, cross-product, polynomial-root-finding, floating-point-model]
see_also: [conservative-advancement, robust-cloth-collision, impact-zones, incremental-potential-contact, sturm-sequence, bisection-method, exact-geometric-computation, interval-arithmetic]
sources:
  - paper: doi:10.1007/978-3-7091-6874-5_13
    title: Xavier Provot, Collision and self-collision handling in cloth model dedicated to design garments, Computer Animation and Simulation 97 (Proceedings of the Eurographics Workshop), Springer, 1997, 177 to 189
    locator: the vertex-face and edge-edge tests with the cubic coplanarity equation and the check at each root
  - paper: doi:10.1145/2185520.2185592
    title: Tyson Brochu, Essex Edwards and Robert Bridson, Efficient geometrically exact continuous collision detection, ACM Transactions on Graphics 31(4), 2012, article 96
    locator: the failure cases of floating point cubic solvers and the exact test by root parity
  - paper: doi:10.1145/3460775
    title: Bolun Wang, Zachary Ferguson, Teseo Schneider, Xin Jiang, Marco Attene and Daniele Panozzo, A large-scale benchmark and an inclusion-based algorithm for continuous collision detection, ACM Transactions on Graphics 40(5), 2021, article 188
    locator: the benchmark of vertex-face and edge-edge queries, the false negatives of the methods it compares, and the conservative inclusion-based method
---

The elementary continuous collision tests find the first time in a time step at which a moving vertex hits a moving triangle, or two moving edges cross. Each of the four points moves on a straight line during the step. The four points are coplanar exactly when a triple product is zero, and with linear motion this triple product is a cubic polynomial in time. A contact can only happen at a root of the cubic. So the tests find the roots in $[0, 1]$ in increasing order, and at each root they check if the vertex is really on the triangle, or if the edges really meet. They are the inner tests of [continuous collision detection](/continuous-collision-detection/) for triangle meshes and cloth, used by [robust cloth collision](/robust-cloth-collision/), [impact zones](/impact-zones/) and the line search of [incremental potential contact](/incremental-potential-contact/). In floating point they can miss contacts, and the choice of the tolerance is the hard part.

## In plain words

A corner of one mesh and a flat piece of another mesh both move in straight lines during a short time. You want to know if the corner hits the flat piece, and when.

The corner can hit the piece only when it is on the same flat sheet as the piece. That moment is the answer to an equation in time with at most three answers. Find these answers in order. At each one, check if the corner is really inside the piece, and not on the sheet but outside it. The first answer that passes is the moment of the hit.

The test for two moving sides works the same way. The two sides can cross only when their four ends are on one flat sheet.

## The problem

The input is four points with their positions $x_i^0$ at $t = 0$ and $x_i^1$ at $t = 1$, so that $x_i(t) = x_i^0 + t\,(x_i^1 - x_i^0)$, and a distance tolerance $\delta \ge 0$. For the vertex-face test the points are a vertex $p$ and the corners $a$, $b$, $c$ of a triangle. For the edge-edge test they are the ends of the edges $ab$ and $cd$. The output is the first time $t \in [0, 1]$ of a contact, or NO-CONTACT. A contact is a time at which $p$ is in the closed triangle, or at which the closed segments meet. The scenes on this page are 3D, because edge-edge contacts exist only in 3D.

## The algorithm

```pseudo id=main
VERTEX-FACE-CCD(p, a, b, c, δ)
L1  f ← the coefficients of (p - a) · ((b - a) × (c - a)) as a cubic in t
L2  z ← the roots of f' in (0, 1), sorted
L3  for each piece [lo, hi] between 0, the values of z, and 1
L4      if f(lo) = 0 then add lo to R, else if f(lo) and f(hi) have opposite signs then add the root of the piece, by bisection, to R
L5  for each t in R, in increasing order
L6      if the distance of p(t) to the triangle a(t) b(t) c(t) is at most δ then
L7          return t
L8  return NO-CONTACT
```

The edge-edge test is the same with $f(t) = (c - a) \cdot ((b - a) \times (d - c))$ and the distance between the segments at line L6. A root at $t = 1$ is added after the loop. The derivative $f'$ is a quadratic, so line L2 needs one square root. On each piece $f$ is monotone, so a piece has at most one root, and bisection finds it. The bisection keeps the end of the bracket that is before the root, so the reported time is not later than the root. The distance at line L6 uses the closest point of a triangle by its Voronoi regions and the closest points of two segments, as in Ericson's book.

If all four coefficients are zero, the four points stay coplanar during the whole step. The cubic then gives no information, and the test must fall back to a 2D test in the common plane. The implementation raises an error in this case.

## Example

The triangle has $a = (0, 0, 0)$ at rest, $b$ moves from $(4, 0, 0)$ to $(5, 2, 3)$, and $c$ moves from $(0, 4, 0)$ to $(1, -2, 0)$. The vertex $p$ moves from $(3, 1, 3)$ to $(1, 0, 0)$. Line L1 gives

$$f(t) = 48 - 144\,t + 117\,t^2 - 15\,t^3 = -3\,(5t - 4)(t^2 - 7t + 4).$$

The derivative $f'(t) = -144 + 234\,t - 45\,t^2$ has one root in $(0, 1)$, at $z_1 \approx 0.713204$, with $f(z_1) \approx -0.630$. So the pieces are $[0, z_1]$, where $f$ goes from 48 to $-0.630$, and $[z_1, 1]$, where it goes from $-0.630$ to 6. Each piece has one root: $t_1 = (7 - \sqrt{33})/2 \approx 0.627719$ and $t_2 = 4/5$. An exact Sturm count with fractions also gives two distinct roots in $(0, 1)$.

At $t_1$ the four points are coplanar, but $p(t_1) \approx (1.7446, 0.3723, 1.1168)$ has the barycentric weights $(2, 0.593, -1.593)$ for $(a, b, c)$. The weight of $c$ is negative, so $p$ is outside the triangle, at the distance $0.40048$ from it, and line L6 rejects this root. At $t_2 = 4/5$, $p = (1.4, 0.2, 0.6)$, $b = (4.8, 1.6, 2.4)$ and $c = (0.8, -0.8, 0)$. Then $p = \frac{1}{2} a + \frac{1}{4} b + \frac{1}{4} c$ exactly, the vertex is inside the triangle, and the test returns $t = 0.8$. A test that only looked at the sign of $f$ at the start and the end of the step would see $f(0) = 48$ and $f(1) = 6$, the same sign, and miss both roots.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). At a contact the three vectors of the triple product are linearly dependent, so a contact time is a root of $f$. The critical points split $[0, 1]$ into pieces on which $f$ is monotone, so the loop finds every root in $[0, 1]$, in increasing order, each to within $2^{-k}$ before the root after $k$ bisection steps. The distance from the vertex to the triangle changes at most at the speed $L$ of the points, so if $L\,2^{-k} \le \delta$, the check passes at the reported value of the first contact. So in exact arithmetic the test returns a time that is not after the first contact, and at which the distance is at most $\delta$. In floating point the proof does not hold, and the pitfalls below are real.

## Complexity

A test costs $O(1)$ arithmetic for the cubic and the critical points, at most three bisections of $k$ steps, and at most three distance checks, so $O(k)$. The implementation uses $k = 80$, and a bisection stops earlier when the bracket cannot be split in floating point. The extra space is $O(1)$. For meshes the cost is in the number of pairs: a mesh pair has a vertex-face test for each vertex and triangle and an edge-edge test for each pair of edges, so a broad phase with swept boxes must prune the pairs first.

## Properties

- **First contact.** The tests return the earliest contact in the step, not just whether one happens, as a simulator needs for a time of impact.
- **No missed sign changes.** Splitting at the critical points finds two roots that are close together, where $f$ has no sign change between the samples of a sampling method. In the tests of this page, a dense sampling with 600 steps missed one planted contact of 80, with two roots 0.00044 apart, and the critical point split found it.
- **Exact cubic with exact input.** With Fraction input the coefficients and the signs of $f$ are exact. The code also gives an exact Sturm count of the roots, which the tests compare with the float roots on 400 random cubics.
- **Not exact in floating point.** The roots, the critical points and the inside check have rounding errors. A tolerance $\delta > 0$ makes the test more conservative, at the cost of reporting near misses as contacts.

## Variants and improvements

- **Exact tests.** Brochu, Edwards and Bridson (2012) decide if a contact happens in the step with exact predicates, by the parity of the crossings of a ray with the space-time surface of the moving points. It never misses a contact, but it does not give the time directly.
- **Inclusion-based tests.** Wang, Ferguson, Schneider, Jiang, Attene and Panozzo (2021) solve the contact equations in the parameters of the step and of the two primitives with interval arithmetic and subdivision, with a guaranteed conservative answer. Their benchmark shows false negatives in floating point cubic solvers.
- **A minimum separation.** Cloth codes test for a time when the distance is at most a thickness $\eta$, not 0, so that the contact is found before the meshes touch. With $\delta = \eta$ this is the test of this page.
- **Rigid motion.** With rotation the points do not move on lines, and the equation is not a cubic. Use [conservative advancement](/conservative-advancement/), or approximate the motion by lines on sub-steps.

## When to use it

Use these tests for deformable triangle meshes, such as cloth and soft bodies, where each vertex moves on a line during the step. They are the narrow phase under a broad phase of swept bounding boxes. Use an exact or inclusion-based variant when a missed contact is not acceptable, for example in the line search of incremental potential contact, where a missed contact lets the meshes pass through each other.

## Pitfalls

- **A hit on a shared edge.** In the tests of this page, a vertex goes down through the shared edge of two triangles at $t = 1/3$, from $(0.15, 0.85, 1)$ to $(0.15, 0.85, -2)$. With $\delta = 0$ both triangles miss the hit, because $0.15 + 0.85$ is not exactly 1 after the rounding of the inputs, and the vertex passes through the mesh. With $\delta = 10^{-12}$ both find it.
- **Grazing contacts.** If the vertex only touches the plane, $f$ has a double root, and a rounding error can turn it into two close roots or none.
- **Coplanar motion.** If the four points stay coplanar, $f$ is zero for all $t$. Detect this case and use a 2D test.
- **Degenerate triangles and parallel edges.** A barycentric inside test divides by the area of the triangle. A closest-point test, as in the code, handles thin triangles and parallel edges without a division by zero.
- **Scale.** The coefficients of $f$ grow with the cube of the coordinates. Use a tolerance relative to the size of the scene and to the speeds, not a fixed number.

## Implementations

## History

Provot (1997) used the vertex-face and edge-edge cubics with a check at each root for the collisions and self-collisions of cloth, and Bridson, Fedkiw and Anderson (2002) used them with a thickness tolerance in their robust treatment of cloth collisions. Later work showed that floating point cubic solvers miss contacts. Brochu, Edwards and Bridson (2012) gave an exact test, and Wang and others (2021) gave a large benchmark of hard queries and a conservative inclusion-based method.

## References
