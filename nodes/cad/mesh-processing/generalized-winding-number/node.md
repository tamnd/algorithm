---
tag: CVGJTP
kind: algorithm
slug: generalized-winding-number
name: Generalized winding number
aliases:
- Jacobson winding number
area: cad/mesh-processing
level: research
summary: Jacobson, Kavan and Sorkine's sum of signed solid angles of a mesh at a point, which is 1 inside and 0 outside a closed mesh and degrades smoothly for broken ones.
model: real-ram
complexity:
  vars: {F: the number of triangles}
  time: {direct: O(F), tree_worst: O(F)}
  space: {direct: O(1), tree: O(F)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 2013
  people: [Alec Jacobson, Ladislav Kavan, Olga Sorkine-Hornung]
  note: Jacobson, Kavan and Sorkine-Hornung used the sum of solid angles as a robust inside test for broken meshes in 2013, with a hierarchical evaluation.
prereqs: [winding-number-algorithm, orientation-test]
see_also: [mesh-boolean-operations, mesh-arrangements, ray-casting, point-in-polygon, mesh-repair-problem, bounding-volume-hierarchy, signed-distance-function, catastrophic-cancellation]
sources:
  - paper: doi:10.1145/2461912.2461916
    title: Alec Jacobson, Ladislav Kavan and Olga Sorkine-Hornung, Robust inside-outside segmentation using generalized winding numbers, ACM Transactions on Graphics 32(4), 2013, Article 33
    locator: the definition as a sum of solid angles, its jump across the surface, the hierarchical evaluation with closing patches, and the segmentation of a tetrahedral mesh by graph cut
  - paper: doi:10.1109/TBME.1983.325207
    title: A. van Oosterom and J. Strackee, The solid angle of a plane triangle, IEEE Transactions on Biomedical Engineering BME-30(2), 1983, 125 to 126
    locator: the closed formula for the tangent of half the solid angle of a triangle
  - paper: doi:10.1145/2897824.2925901
    title: Qingnan Zhou, Eitan Grinspun, Denis Zorin and Alec Jacobson, Mesh arrangements for solid geometry, ACM Transactions on Graphics 35(4), 2016, Article 39
    locator: the use of exact winding numbers of the cells of an arrangement for Booleans on self-intersecting input
---

The generalized winding number of a triangle mesh at a point $p$ is the sum of the signed solid angles of all triangles seen from $p$, divided by $4\pi$, the solid angle of the whole sphere. For a closed mesh this is the classical winding number: an integer, 1 inside and 0 outside a closed surface that does not cut itself, and the number of times the surface wraps around $p$ in general. The formula makes sense for any mesh, also one with holes, gaps, overlaps or self-intersections. Then the value is no longer an integer, but it changes by exactly 1 across each triangle and smoothly elsewhere, and it stays close to 1 deep inside and close to 0 far outside. Alec Jacobson, Ladislav Kavan and Olga Sorkine-Hornung proposed it in 2013 as an inside test for broken meshes. It is the 3D form of the [winding number algorithm](/winding-number-algorithm/) for polygons, and it is the inside rule behind robust [mesh Boolean operations](/mesh-boolean-operations/).

## In plain words

Stand at a point and look around. Each small triangle of the surface covers a patch of your view. Count that patch as positive if you see the back of the triangle, and negative if you see its front.

If the surface is closed and you are inside, the backs of the triangles cover your whole view once, so the total is one full view. If you are outside, every patch you see from the front is cancelled by a patch you see from the back, and the total is zero.

If the surface has a hole, the hole leaves a gap in your view. Inside, the total is then a bit less than one, but it is still much closer to one than to zero. So rounding the total still says inside or outside in most places.

## The problem

The input is a list of triangles with faces oriented so that the outward normal follows the right-hand rule, and a query point $p$ not on any triangle. The output is a number $w(p)$ that equals the winding number of the surface around $p$ when the mesh is closed, and that tells inside from outside as well as possible when it is not.

## The algorithm

The solid angle of a triangle $T = (A, B, C)$ seen from $p$ has a closed formula, due to Van Oosterom and Strackee. With $a = A - p$, $b = B - p$, $c = C - p$:

$$\tan\frac{\Omega_T}{2} = \frac{\det[a\ b\ c]}{|a||b||c| + (a \cdot b)|c| + (a \cdot c)|b| + (b \cdot c)|a|}.$$

The determinant is $-\mathrm{ORIENT3D}(A, B, C, p)$, the [orientation test](/orientation-test/) of $p$ against the plane of $T$, so $\Omega_T > 0$ when $p$ is behind $T$. Computing the angle with $\mathrm{atan2}$ keeps it in $(-2\pi, 2\pi)$.

```pseudo id=main
WINDING-NUMBER(M, p)
L1  s ← 0
L2  for each triangle T = (A, B, C) of M do
L3      a ← A − p; b ← B − p; c ← C − p; num ← det[a b c]
L4      den ← |a||b||c| + (a·b)|c| + (a·c)|b| + (b·c)|a|
L5      s ← s + 2 · atan2(num, den)
L6  return s / (4π)
```

**The tree version.** For many queries, Jacobson and coauthors build a tree of patches with bounding boxes. If $p$ is outside the box of a patch, the patch has the same total solid angle as any surface with the same boundary inside the box, for example a fan of triangles from one boundary vertex over the boundary edges. A patch of a smooth surface has a short boundary, so its fan has far fewer triangles than the patch. Patches whose box contains $p$ are split into their children or summed directly. A closed patch has an empty fan and contributes 0 from outside its box.

**Degenerate cases.** A point on a triangle has no defined value; at a point inside a face, the limits from the two sides differ by 1, and the formula returns one of them or a value between, depending on the sign of a zero. A triangle with zero area has $\Omega = 0$. Repeated triangles add up, and two copies with opposite orientations cancel. If $p$ is a vertex, $|a| = 0$, the formula gives atan2(0, 0) = 0 for the triangles at that vertex, and the result has no meaning.

## Example

Take the unit cube, 12 triangles with outward normals, and $p = (1/2, 1/2, 1/2)$. For the triangle $(0,0,0)$, $(0,1,0)$, $(1,1,0)$ of the bottom face, $a = (-\tfrac12, -\tfrac12, -\tfrac12)$, $b = (-\tfrac12, \tfrac12, -\tfrac12)$, $c = (\tfrac12, \tfrac12, -\tfrac12)$.

| step | value |
|---|---|
| L3 | $\det[a\,b\,c] = 1/2 > 0$: $p$ is behind the face |
| L4 | $|a| = |b| = |c| = \sqrt3/2$, $a \cdot b = 1/4$, $a \cdot c = -1/4$, $b \cdot c = 1/4$, so $den = 3\sqrt3/8 + \sqrt3/8 = \sqrt3/2$ |
| L5 | $\tan(\Omega/2) = 1/\sqrt3$, so $\Omega = \pi/3$ |
| L6 | by symmetry all 12 triangles give $\pi/3$, so $w = 4\pi / 4\pi = 1$ |

At $p = (3/2, 1/2, 1/2)$, outside, the six faces give angles of both signs, and the sum is 0. Now remove the bottom face. The cube is open, and at the centre $w = 5/6$, because the missing face covered one sixth of the view. At the centre of the missing face $w = 1/2$, halfway between inside and outside. Rounding $w$ still classifies the centre as inside.

**When the arithmetic is floating point.** Next to an edge of the mesh the formula loses its accuracy. Put $p$ at height $h$ above the midpoint of the diagonal of the bottom face, inside the cube. For the triangle whose diagonal is right under $p$, $a$ and $c$ point in nearly opposite directions, $a \cdot c \approx -|a||c|$, and the denominator is a difference of nearly equal numbers, a case of [catastrophic cancellation](/catastrophic-cancellation/). With doubles, $w$ is $0.99998$ at $h = 10^{-12}$, $0.98$ at $h = 10^{-15}$, $0.557$ at $h = 10^{-17}$ and $0.50006$ at $h = 10^{-20}$, while the exact value is 1. At $(0.3, 0.7, 10^{-20})$, away from the diagonal, the float value is correct. The fix depends on the use. For a closed mesh, the exact answer is a signed count of ray crossings with exact predicates, which the tests of this page compute in rational arithmetic, see [ray casting](/ray-casting/) and [exact predicates](/shewchuk-expansion-sum/); it can be used when $w$ is too close to $1/2$. For a broken mesh there is no exact answer to fall back on, and points that close to the surface are ambiguous anyway. This is the [robustness problem](/geometric-robustness-problem/) of geometry.

## Correctness

The solid angle of a triangle is the signed area of its shadow on the unit sphere around $p$, so the sum of the solid angles is the integral over all directions $d$ of the signed number of triangles that the ray from $p$ in direction $d$ hits. For a closed mesh this number does not change when $d$ crosses the shadow of an edge, because the two triangles at the edge change it by $+1$ and $-1$. So it is the same integer $k$ for almost all directions, and $w = k$, which is also what a signed ray count finds. As $p$ goes to infinity, $w$ goes to 0, so it is 0 on the outside. Crossing one face against its normal raises $w$ by exactly 1, because the solid angle of that face jumps from $-2\pi$ to $2\pi$; this holds for broken meshes too. So a closed surface that does not cut itself has $w = 1$ inside. The fan of a patch has the same boundary, so the patch minus its fan is closed and has winding number 0 at points outside the box. The full proof is below.

## Complexity

The direct sum takes $O(F)$ time per query for $F$ triangles and $O(1)$ extra space. The tree takes $O(F)$ space and $O(F)$ time per query in the worst case, but it is much faster in practice, because most patches are far from $p$ and are replaced by small fans. On a closed polycube with 728 triangles, 200 queries took 1.58 s with the direct sum and 0.19 s with the tree in the Python code of the page. Barill and coauthors (2018) replace the fans by a truncated multipole expansion of each patch, which brings the cost per query to about $O(\log F)$ for a given accuracy.

## Properties

- **Exact for closed meshes.** In exact arithmetic, $w$ is the integer winding number.
- **Robust for broken meshes.** Holes, gaps and small overlaps change $w$ by small amounts away from them, so rounding or thresholding at $1/2$ still classifies most points.
- **Harmonic.** Off the surface $w$ is a harmonic function of $p$, smooth, with no local maximum or minimum.
- **Jump of 1.** Across a triangle $w$ jumps by exactly 1, for any mesh.
- **Order independent.** The result does not depend on the order of the triangles or on how they are connected, only on their positions and orientations.

## Variants and improvements

- **Winding numbers in 2D.** For a polygon the same sum of signed angles over $2\pi$ is the [winding number algorithm](/winding-number-algorithm/), and for a closed polygon it gives the [point in polygon](/point-in-polygon/) answer.
- **Point clouds and triangle soups.** Barill, Dickson, Schmidt, Levin and Jacobson (2018) evaluate fast winding numbers for oriented point clouds with a multipole tree.
- **Segmentation of a volume mesh.** The original paper builds a tetrahedral mesh of the bounding box, evaluates $w$ at the tetrahedra, and chooses the inside by a graph cut that trades $w$ against a smooth boundary.
- **Exact winding numbers of cells.** [Mesh arrangements](/mesh-arrangements/) compute the winding number of every cell of the arrangement exactly, by propagating it across the faces with the jump of 1, which avoids solid angles altogether.

## When to use it

Use it to decide inside and outside for a mesh that is not watertight: for mesh repair, voxelization, the inside test of a [signed distance function](/signed-distance-function/), or Booleans on bad input. For a closed mesh where exact answers matter, a signed ray count with exact predicates is cheaper and exact, see [ray casting](/ray-casting/). For many queries, use the tree or a fast multipole version.

## Pitfalls

- **Wrong orientation.** A face with the wrong orientation counts with the wrong sign; a mesh with all faces reversed gives $-1$ inside. Fix the orientation first, see the [mesh repair problem](/mesh-repair-problem/).
- **Points next to the surface.** Near an edge the float value loses digits: at a distance of $10^{-12}$ of the edge length it is off by $2 \times 10^{-5}$, and at $10^{-17}$ it cannot tell inside from outside, as the example shows.
- **Nested or overlapping shells.** Two shells that overlap give $w = 2$ in the overlap. Testing $w > 1/2$ means union, and $w = 1$ exactly means something else.
- **Big holes.** A missing face of a cube gives $w = 5/6$ at the centre but $1/2$ at the hole. Points near a large hole cannot be classified, and no inside test can do better without more information.

## Implementations

## History

The winding number of a closed curve around a point is a classical idea of topology and complex analysis, and the solid angle of a surface is a classical idea of potential theory: Gauss's law says that the flux of the field of a point charge through a closed surface is the solid angle it subtends. Van Oosterom and Strackee gave the closed formula for the solid angle of a triangle in 1983, for electrocardiography. Jacobson, Kavan and Sorkine-Hornung used the sum of the solid angles as a robust inside test for broken meshes in 2013, with a hierarchical evaluation. Zhou, Grinspun, Zorin and Jacobson used exact winding numbers of cells for mesh Booleans in 2016, and Barill and coauthors made the evaluation fast for point clouds and soups in 2018.

## References
