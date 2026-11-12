---
tag: C4PQD6
kind: algorithm
slug: plucker-ray-triangle-test
name: Plücker ray-triangle test
aliases:
- Plücker coordinates test
area: graphics-and-signals/ray-tracing
level: advanced
summary: Decide whether a ray passes through a triangle by the signs of the permuted inner products of the ray line with the three edge lines, written in Plücker coordinates.
solves: [ray-object-intersection]
model: real-ram
complexity:
  time: {worst: Θ(1)}
  space: {extra: O(1)}
properties: {deterministic: true, recursive: false}
history:
  year: 1997
  people: [John Amanatides, Jeff Erickson, Ray Jones]
  note: Plücker coordinates are from the nineteenth century; their use for ray-triangle tests spread in the late 1990s through Amanatides and Choi and the Ray Tracing News.
prereqs: [ray-object-intersection, cross-product, orientation-test]
see_also: [moller-trumbore, watertight-ray-triangle-intersection, ray-plane-intersection, polygon-mesh, determinant, edge-function]
sources:
  - url: https://www.realtimerendering.com/resources/RTNews/html/rtnv10n3.html
    title: Jeff Erickson, Plücker coordinates, Ray Tracing News 10(3), 1997
    locator: the article of that title (the ray-triangle test by the orientation of the ray against each edge)
  - url: https://www.realtimerendering.com/resources/RTNews/html/rtnv13n1.html
    title: Ray Jones, Intersecting a ray and a triangle with Plücker coordinates, Ray Tracing News 13(1), 2000
    locator: the article of that title, including the remark on edge values shared by adjacent triangles
  - url: http://jcgt.org/published/0002/01/05/
    title: Sven Woop, Carsten Benthin and Ingo Wald, Watertight ray/triangle intersection, Journal of Computer Graphics Techniques 2(1), 2013, 65 to 82
    locator: Section 2 and Figure 1 (a Plücker test is watertight along edges but not at vertices), and Table 2
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Section 3.6.2 Triangle Intersection and its Further Reading
---

The Plücker ray-triangle test decides whether a ray passes through a triangle by three signs. It writes the ray and the three directed edges of the triangle as lines in Plücker coordinates, a pair of 3-vectors for each line. The permuted inner product of two lines is zero when they meet and otherwise has a sign that says on which side one line passes the other. The ray goes through the triangle exactly when its three products with the edges have one sign. The distance to the hit then comes from the plane of the triangle. The test solves [ray-object intersection](/ray-object-intersection/) for triangles, and in a mesh each edge value can be shared by the two triangles of the edge.

## In plain words

Two lines in space that do not meet pass each other in one of two ways, like the two ways a screw can turn. One number, computed from the two lines, tells which way: it is positive for one turn, negative for the other, and zero when the lines meet or are parallel.

Walk around the three edges of a triangle in order. A line through the inside of the triangle passes all three edges with the same turn. A line that misses the triangle passes at least one edge the other way. So the test computes three such numbers, one per edge, and checks their signs. Each number depends only on the ray and one edge, so two triangles that share an edge can share the number too.

## The problem

The input is a ray $o + t\,d$ with $d \ne 0$, an interval $(t_{\min}, t_{\max})$, and a triangle $a b c$. The output is $(t, w_a, w_b, w_c)$ with $w_a + w_b + w_c = 1$, all weights $\ge 0$, $t_{\min} < t < t_{\max}$ and $o + t\,d = w_a a + w_b b + w_c c$, or MISS. Points on edges count as hits. A ray parallel to the plane of the triangle gives MISS.

## The algorithm

**Plücker coordinates.** The directed line through $p$ and then $q$ has the coordinates $L = (U, V)$ with the direction $U = q - p$ and the moment $V = p \times q$. Any two points of the line, in the same order, give the same pair up to a positive factor. The ray is the line $(d, o \times d)$. For two lines $L_1 = (U_1, V_1)$ and $L_2 = (U_2, V_2)$ the permuted inner product is

$$\mathrm{side}(L_1, L_2) = U_1 \cdot V_2 + U_2 \cdot V_1.$$

For the ray and the edge from $p$ to $q$, expanding the products gives $\mathrm{side} = \det[d,\ p - o,\ q - o]$, a triple product. It is zero when the ray line and the edge line meet or are parallel. Its sign is the [orientation](/orientation-test/) of the four points $o$, $o + d$, $p$, $q$.

```pseudo id=main
PLUCKER-RAY-TRIANGLE(o, d, a, b, c, tmin, tmax)
L1  R ← (d, o × d);  Lab ← (b − a, a × b);  Lbc ← (c − b, b × c);  Lca ← (a − c, c × a)
L2  sab ← side(R, Lab);  sbc ← side(R, Lbc);  sca ← side(R, Lca)
L3  if some s < 0 and some s > 0 then return MISS     ▷ mixed signs: the ray passes outside
L4  total ← sab + sbc + sca;  if total = 0 then return MISS
L5  n ← (b − a) × (c − a);  t ← n · (a − o) / total
L6  if not (tmin < t < tmax) then return MISS
L7  return (t, sbc / total, sca / total, sab / total)
```

Line L3 is the two-sided test: three values of one sign, with zeros allowed, mean that the ray line passes through the closed triangle. Line L4 uses the identity $s_{ab} + s_{bc} + s_{ca} = d \cdot n$ for the normal $n$ of line L5, so total is zero exactly when the ray is parallel to the plane. Line L5 then intersects the ray line with the plane of the triangle, as in [ray-plane intersection](/ray-plane-intersection/), with the denominator $n \cdot d$ already known. The weight of a vertex at line L7 is the value of the edge opposite it divided by the total, because each value is six times the signed volume of the tetrahedron that the ray segment of length one forms with that edge, and these volumes are proportional to the areas of the sub-triangles in a projection along the ray.

The sign test of line L3 is a test on the ray line, not on the ray: line L6 checks that the hit is in the interval. A renderer that culls back faces accepts only one sign at line L3, the negative one for counterclockwise triangles seen from the ray, as in the example.

## Example

The triangle $a = (0, 0, 0)$, $b = (1, 0, 0)$, $c = (0, 1, 0)$, and the ray from $o = (\tfrac14, \tfrac14, 1)$ with $d = (0, 0, -1)$.

| line | value |
|---|---|
| L1 | $R = ((0, 0, -1), (-\tfrac14, \tfrac14, 0))$, $L_{ab} = ((1, 0, 0), (0, 0, 0))$, $L_{bc} = ((-1, 1, 0), (0, 0, 1))$, $L_{ca} = ((0, -1, 0), (0, 0, 0))$ |
| L2 | $s_{ab} = 0 + (1, 0, 0) \cdot (-\tfrac14, \tfrac14, 0) = -\tfrac14$ |
| L2 | $s_{bc} = (0, 0, -1) \cdot (0, 0, 1) + (-1, 1, 0) \cdot (-\tfrac14, \tfrac14, 0) = -1 + \tfrac12 = -\tfrac12$ |
| L2 | $s_{ca} = 0 + (0, -1, 0) \cdot (-\tfrac14, \tfrac14, 0) = -\tfrac14$ |
| L3 | all three negative: the ray line passes through the triangle |
| L4 | $\mathrm{total} = -1 = d \cdot n$ |
| L5 | $n = (0, 0, 1)$, $n \cdot (a - o) = -1$, $t = 1$ |
| L7 | $(t, w_a, w_b, w_c) = (1, \tfrac12, \tfrac14, \tfrac14)$ |

The hit is $(\tfrac14, \tfrac14, 0)$, as for the [Möller-Trumbore test](/moller-trumbore/).

**A shared edge.** With the two triangles and the ray of the leak example on the [Möller-Trumbore page](/moller-trumbore/) ($T_1 = (P, A, Q)$, $T_2 = (P, Q, B)$, a ray aimed at a point of $PQ$), the Plücker test in double precision misses $T_1$ and hits $T_2$ at $t \approx 1$. The exact answer for the rounded inputs is a hit in $T_1$, so the floating point answer is not the exact one, but the ray does not leak: the edge value of $PQ$ is the same number, with opposite signs, in both triangles.

## Correctness

In exact arithmetic, the ray line passes through the closed triangle if and only if the three values $\det[d, a - o, b - o]$, $\det[d, b - o, c - o]$, $\det[d, c - o, a - o]$ do not have opposite signs, because each value is the signed area, in a projection along $d$, of the triangle that the projected ray point forms with one edge, and a point is inside a triangle exactly when these three areas agree in sign. Lines L4 and L5 then give the unique point of the line in the plane, and line L6 restricts it to the interval. The full proof is in the proofs folder.

In floating point, the value of an edge is computed from the ray and the two endpoints only. The reversed edge $(p - q, q \times p)$ is the exact negation of $(q - p, p \times q)$, because a difference of two rounded products changes sign exactly when the products are swapped, so the two triangles of a shared edge compute exactly opposite values, whether they store the edge or rebuild it. That makes the test watertight along edges. At a vertex it is not: the values of the edges around a vertex are rounded independently, and their signs can form a pattern in which no triangle around the vertex has three agreeing signs, so a ray very close to the vertex can miss all of them (Figure 1 of Woop, Benthin and Wald). The method is only usually correct at vertices.

## Complexity

Line L1 costs one cross product for the ray and three cross products and three subtractions for the edges, line L2 costs three permuted inner products of 6 multiplications and 5 additions each, and lines L4 to L7 cost a cross product, a dot product, one division and three more divisions for the weights. All of this is a constant, so the test takes $\Theta(1)$ time and $O(1)$ extra space.

The ray line is computed once per ray. The edge lines do not depend on the ray, so a mesh can store them, six numbers per edge, and share each edge between its two triangles; then the per-triangle work for a miss is the three products of line L2 and the comparisons of line L3. A ray against $n$ triangles by a linear scan costs $\Theta(n)$; a [bounding volume hierarchy](/bounding-volume-hierarchy/) reduces the number of tests on typical scenes but is $O(n)$ per ray in the worst case.

## Properties

- **Exact with rational inputs.** All steps are additions, multiplications and a division, so with rational arithmetic the result is the exact one.
- **Watertight along edges, not at vertices.** See the section on correctness.
- **Line test first.** Lines L2 and L3 decide whether the line meets the triangle before any distance is computed, so a miss costs only three signs.
- **Shared work.** The values of an edge can be computed once for a ray and reused by both triangles of the edge, which is the benefit that Amanatides and Choi pointed out.
- **Orientation from the signs.** The common sign of the three values tells from which side the ray comes.

## Variants and improvements

- **Stored edge lines.** Store the six coordinates of each edge with the mesh, so that the test needs only the inner products per ray.
- **Ray-polygon and ray-tetrahedron tests.** The same sign test works for any convex polygon, with one value per edge, and for the faces of a tetrahedron, where a ray that enters through one face leaves through another and the face values are shared.
- **Visibility between lines.** Plücker coordinates describe sets of lines, and the side relation decides whether a line passes through a polygon; this is how they enter visibility computations between portals and cells.
- **The watertight test.** The [watertight ray-triangle intersection](/watertight-ray-triangle-intersection/) replaces the 6D products by 2D [edge functions](/edge-function/) on a sheared projection and computes exact signs, which closes the gaps at vertices too.
- **The Möller-Trumbore test.** The [Möller-Trumbore test](/moller-trumbore/) solves the same linear system by Cramer's rule with fewer stored numbers, but it is not watertight along edges.

## When to use it

Use the Plücker test when the edges of a mesh can be shared, so that each edge value is computed once per ray, or when the test must work for convex polygons and tetrahedra in the same way. It is also a natural fit when a ray traverses a tetrahedral mesh, since the shared face values tell the exit face. When the mesh must be closed for rays at vertices too, use the [watertight test](/watertight-ray-triangle-intersection/); when memory per triangle matters most, use the [Möller-Trumbore test](/moller-trumbore/).

## Pitfalls

- **The order of the coordinates.** The permuted inner product is $U_1 \cdot V_2 + U_2 \cdot V_1$, not $U_1 \cdot U_2 + V_1 \cdot V_2$. Writing `side ← U1 · U2 + V1 · V2` at line L2 gives a number with no geometric meaning. Pair each direction with the other line's moment.
- **Edges in a consistent order.** The three edges must go around the triangle in one direction, $a \to b \to c \to a$. Using the edge $b \to a$ in line L1 flips one sign, and line L3 then rejects every hit. Build the three lines head to tail.
- **The line is not the ray.** Lines L2 and L3 test the whole line, so they accept a triangle behind the origin. Keep the interval test of line L6.
- **A strict sign test.** Writing line L3 as `if some s ≤ 0 then return MISS` rejects rays exactly on an edge in both triangles, which opens a crack. Accept zeros.
- **Assuming watertight vertices.** Rays aimed at a vertex can miss all triangles around it in floating point. Use the watertight test when that matters.

## Implementations

## History

Julius Plücker introduced the coordinates of lines that carry his name in his work on line geometry in the 1860s. In computer graphics they were used for visibility between lines and polygons before they were used for ray-triangle tests. In the late 1990s Amanatides and Choi, in a paper on ray tracing triangular meshes, and Jeff Erickson, in the Ray Tracing News, described the ray-triangle test with Plücker coordinates and the sharing of edge values between triangles; Ray Jones wrote it up in the Ray Tracing News in 2000. Woop, Benthin and Wald showed in 2013 that such tests are watertight along edges but not at vertices.

## References
