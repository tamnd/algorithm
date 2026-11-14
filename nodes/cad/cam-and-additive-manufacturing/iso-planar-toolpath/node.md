---
tag: 4X99MA
kind: algorithm
slug: iso-planar-toolpath
name: Iso-planar toolpath
aliases:
- drive plane toolpath
area: cad/cam-and-additive-manufacturing
level: core
summary: Machines a surface along its cuts by a family of parallel planes, which run across patch boundaries, but the spacing on the surface grows where the surface is steep.
solves: [toolpath-planning]
model: real-ram
complexity:
  vars: {K: number of drive planes, m: depth limit of the chord refinement}
  time: {worst: "O(K 2^m)"}
  space: {extra: "O(m)"}
properties: {deterministic: true, recursive: true, exact: true}
history:
  year: 1994
  people: [Yunching Huang, James H. Oliver]
  note: Huang and Oliver built tool paths for sculptured surfaces from their cuts by parallel planes, in place of constant-parameter curves. The drive surfaces of APT part programs are older.
prereqs: [toolpath-planning, parametric-surface, iso-parametric-toolpath]
see_also: [iso-scallop-toolpath, direction-parallel-toolpath, scallop-height, cutter-location-data, offset-surface, triangle-mesh-slicing, surface-curvature, z-map-model]
sources:
  - book: isbn:978-0-412-78020-2
    title: Byoung K. Choi and Robert B. Jerard, Sculptured Surface Machining, Theory and Applications, Kluwer Academic Publishers, 1998
    locator: chapter 6, introduction to tool-path generation methods, the part on Cartesian (iso-planar) machining
  - paper: doi:10.1007/BF01781282
    title: Yunching Huang and James H. Oliver, Non-constant parameter NC tool path generation on sculptured surfaces, International Journal of Advanced Manufacturing Technology 9(5), 281-290, 1994
    locator: the tool paths from the cuts of the surface by parallel planes, and the choice of the plane spacing
---

An iso-planar toolpath machines a surface along the curves where it meets a family of parallel drive planes, $x = c_0, c_1, \dots$, one pass per plane. Seen from above, the passes are straight and evenly spaced, as in a [direction-parallel path](/direction-parallel-toolpath/), but in space they follow the surface. The planes do not care how the surface is cut into patches, so one pass runs across many patches. The cost is that the spacing on the surface is not the spacing of the planes: where the surface climbs steeply along $x$, the passes lie farther apart on it. This is a manufacturing method of mechanical CAD: placement and routing here mean where a cutter goes and how it moves, not the placement and routing of a circuit. The code cuts a bilinear patch with exact rational points and a recursive chord refinement.

## In plain words

Slice a loaf of bread with evenly spaced cuts. Each cut leaves a curve on the crust. An iso-planar path moves the tool along these curves, one after the other.

On the flat top of the loaf the curves are as far apart as the cuts. On the steep ends of the loaf the cuts still go straight down at the same spacing, but the crust is tilted, so the curves on the crust are farther apart than the cuts. A tool that leaves a smooth finish on top leaves ridges on the steep parts.

Each curve is drawn as a chain of short straight pieces. A piece is split when the curve bends too far away from it.

## The problem

The input is a surface, a plane spacing $g$ and a chord tolerance $\varepsilon$. The output is a set of passes, one for each plane $x = c_k$ that meets the surface, each a polyline of cutter contact points on the surface. A CAM system turns them into [cutter location data](/cutter-location-data/), or it cuts the [offset surface](/offset-surface/) of the part by the planes and gets the tool centers directly.

The spacing on the surface follows from the gradient of $x$ along the surface. If $n$ is the unit normal, this gradient has length $\sqrt{1 - n_x^2}$, so two passes whose planes are $g$ apart lie about
$$
\frac{g}{\sqrt{1 - n_x^2}}
$$
apart on the surface. On a flat floor ($n_x = 0$) this is $g$. On the plane $z = mx$ it is exactly $g\sqrt{1 + m^2}$. On a wall that faces the $x$ direction ($n_x = \pm 1$) it is unbounded: such a wall lies in one plane or between two planes.

On a bilinear patch $S(u, v)$, the coordinate $x = A + Bu + Cv + Duv$ is bilinear. The code requires $x_v = C + Du > 0$ on the patch. Then each plane meets the patch in one curve $v(u) = (c - A - Bu)/(C + Du)$, and the range of $u$ comes from two linear inequalities.

## The algorithm

```pseudo id=main
ISO-PLANAR(S, g, ε)
L1  for k ← 0, 1, ... while c_k = xmin + g/2 + k g < xmax do
L2      [u_lo, u_hi] ← the u for which the plane x = c_k meets the patch at 0 ≤ v ≤ 1
L3      if there is no such u then go to the next plane
L4      the cut curve is u ↦ S(u, v(u)) with v(u) = (c_k - A - B u)/(C + D u)
L5      REFINE(u_lo, u_hi): if the curve point at the middle is farther than ε from the chord, refine both halves, else keep the chord
L6      append the pass, forward for even k and backward for odd k
L7  return the passes
```

Line L5 is a recursive midpoint test with a depth limit. It is a heuristic: it checks one point of the curve per chord, not all of them. On a general surface, line L4 is replaced by a surface-plane intersection, which marches along the curve with Newton steps or follows it across the patches of a model.

## Example

Take the plane $z = \tfrac34 x$ over $0 \le x \le 10$, $0 \le y \le 4$, as the bilinear patch with corners $(0, 0, 0)$, $(0, 4, 0)$, $(10, 0, 7.5)$ and $(10, 4, 7.5)$, and take $g = 1$.

| step | plane | pass | length |
|---|---|---|---|
| L1 to L6 | $x = 0.5$ | $(0.5, 0, 0.375) \to (0.5, 4, 0.375)$ | 4 |
| L1 to L6 | $x = 1.5$ | $(1.5, 4, 1.125) \to (1.5, 0, 1.125)$ | 4 |
| ... | ... | ... | |
| L1 to L6 | $x = 9.5$ | $(9.5, 4, 7.125) \to (9.5, 0, 7.125)$ | 4 |

Each cut curve is straight, so line L5 keeps one chord. Neighbouring passes are $\sqrt{1 + (3/4)^2} = 1.25$ apart on the surface, not 1. With slope $\tfrac43$ they would be $\tfrac53$ apart. A floor at $z = 0$ next to the ramp gets passes 1 apart from the same planes, so a single $g$ gives two different finishes.

## Correctness

**Theorem.** If $x_v > 0$ on the patch, each plane meets it in one connected curve over the $u$-interval of line L2, every returned point lies exactly on its plane and on the patch, and the refinement stops with at most $2^m$ chords per pass, each of which passes the midpoint test unless the depth limit was hit.

For fixed $u$, $x$ grows linearly in $v$, so each plane value is reached at exactly one $v(u)$, and the condition $0 \le v(u) \le 1$ is a pair of linear inequalities in $u$. The points are rational, so they are exact. The full proof is in the proof file.

**What is measured.** The chord error between midpoints is not bounded by the test. The spacing formula is a first-order estimate. The tests measure the spacing on curved random patches within 10 percent of $g/\sqrt{1 - n_x^2}$ for $g = \tfrac14$, and they measure every inner sample point within about half the local spacing of a pass. Near a patch boundary that runs almost parallel to the planes, the passes end at a grazing angle and some boundary points are farther from the passes.

## Complexity

There are $K \le \lceil (x_{\max} - x_{\min})/g \rceil$ planes. Each refinement makes at most $2^m - 1$ splits, each with a constant number of rational operations, so the time is $O(K 2^m)$ in the worst case. In practice the number of chords on a pass is about $L/\sqrt{8\rho\varepsilon}$, where $L$ is the length of the pass and $\rho$ the radius of curvature of the curve, because a chord with sagitta $\varepsilon$ on a circle of radius $\rho$ has length about $\sqrt{8\rho\varepsilon}$. The extra space is the recursion depth $O(m)$.

## Properties

- **Across patches.** The passes depend only on the planes and the geometry, not on the patches, so they run across the boundaries of a model of many patches.
- **Even when seen from above.** The passes project to equally spaced lines in the plane of the machine table.
- **Spacing grows on steep slopes.** On the surface the spacing is about $g/\sqrt{1 - n_x^2}$, so the passes spread on slopes that are steep along $x$ and leave larger scallops there.
- **Steady along slopes in $y$.** A slope that climbs along $y$, parallel to the planes, keeps the spacing $g$, because $n_x = 0$ there.

## Variants and improvements

- **Cutter location surface.** Cutting the offset of the part surface by the planes gives the tool centers directly, and a ball end mill on these centers does not gouge the part. On a grid this is the idea of the [inverse tool offset](/inverse-tool-offset/).
- **Two directions.** A second pass set with planes $y = c$ machines the slopes that the first set treats badly. Some systems choose the direction per region from the normals.
- **Adaptive plane spacing.** Choosing each next plane from the [scallop height](/scallop-height/) of the last pass gives an [iso-scallop toolpath](/iso-scallop-toolpath/).
- **Z-level paths.** Horizontal planes $z = c$ give the waterline passes of steep walls, the other half of the steep and shallow split. The same operation on a mesh is [triangle mesh slicing](/triangle-mesh-slicing/).

## When to use it

Use iso-planar passes for parts of many patches, and for shallow parts where $n_x$ stays small. On parts with steep walls, combine them with waterline passes for the steep areas, or use an iso-scallop path.

## Pitfalls

- **Walls that face the planes.** A wall with normal along $x$ gets one pass or none. The code rejects a patch with $x_v \le 0$ for this reason.
- **Grazing boundaries.** A patch boundary that runs almost parallel to the planes is crossed at a grazing angle, and the material along it can be far from every pass. A last pass along the boundary fixes this.
- **Midpoint test only.** A curve can bend away from a chord and come back at the middle. A tighter test checks more points or bounds the curvature.
- **Contact points, not centers.** Offsetting the contact points along the normal can make the tool centers leave the planes and can [gouge](/gouge-detection/) concave regions. Cutting the offset surface avoids both.

## Implementations

## History

The drive surface of APT part programs, a plane that the tool follows while it touches the part surface, is the older form of the method. Huang and Oliver (1994) studied tool paths from the cuts of sculptured surfaces by parallel planes as an alternative to constant-parameter paths, and Choi and Jerard (1998) present iso-planar machining next to the iso-parametric and iso-scallop methods.

## References
