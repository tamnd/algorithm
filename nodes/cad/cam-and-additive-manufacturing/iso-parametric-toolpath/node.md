---
tag: SQ9VDF
kind: algorithm
slug: iso-parametric-toolpath
name: Iso-parametric toolpath
aliases:
- isoparametric machining
area: cad/cam-and-additive-manufacturing
level: core
summary: Machines a parametric surface along curves of constant u or v, simple to compute but uneven in spacing where the parameterization is distorted.
solves: [toolpath-planning]
model: real-ram
complexity:
  vars: {N: number of passes}
  time: {worst: "O(N)"}
  space: {extra: "O(1)"}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1987
  people: [Gary C. Loney, Tulga M. Ozsoy]
  note: Loney and Ozsoy machined free-form surface patches along their iso-parametric curves. The method is the first that CAM systems used for sculptured surfaces, because the curves come straight from the surface equations.
prereqs: [toolpath-planning, parametric-surface, bilinear-interpolation]
see_also: [iso-planar-toolpath, iso-scallop-toolpath, scallop-height, cutter-location-data, tensor-product-surface, ruled-surface, arc-length-parametrization, fundamental-forms]
sources:
  - book: isbn:978-0-412-78020-2
    title: Byoung K. Choi and Robert B. Jerard, Sculptured Surface Machining, Theory and Applications, Kluwer Academic Publishers, 1998
    locator: chapter 6, introduction to tool-path generation methods, the part on iso-parametric machining
  - title: Gary C. Loney and Tulga M. Ozsoy, NC machining of free form surfaces, Computer-Aided Design 19(2), 85-90, 1987
    locator: the tool paths along the iso-parametric curves of a surface patch, and the choice of the step between them
  - title: Gershon Elber and Elaine Cohen, Toolpath generation for freeform surface models, Computer-Aided Design 26(6), 490-496, 1994
    locator: adaptive iso-curves, which add iso-parametric passes only where the gap between the passes is too large
---

An iso-parametric toolpath machines a [parametric surface](/parametric-surface/) $S(u, v)$ by moving the tool along the curves where one parameter is constant, $v = v_0, v_1, \dots$, back and forth. The curves come directly from the surface equation, so the path is easy to compute and lies on the surface exactly. The cost is uneven spacing: equal steps in $v$ give equal steps on the surface only where the parameterization is even, and elsewhere the passes crowd together or spread apart. This is a manufacturing method of mechanical CAD: placement and routing here mean where a cutter goes and how it moves, not the placement and routing of a circuit. The code builds the path on a bilinear patch, where every iso-curve is straight and the largest gap between passes has an exact formula.

## In plain words

A surface in a CAD model is made like a sheet of graph paper that has been stretched and bent. The grid lines of the paper are still there on the bent sheet. An iso-parametric path just traces these grid lines, one after the other, back and forth.

This is simple, because the grid lines are known. The problem is that the sheet was stretched more in some places than in others. Where it was stretched a lot, the grid lines are far apart, and the tool leaves ridges. Where it was squeezed, the lines are close, and the tool cuts the same place many times.

To be safe, the gap must be small enough at the widest place. Then the path is denser than needed everywhere else.

## The problem

The input is a surface patch $S : [0, 1]^2 \to \mathbb{R}^3$ and a path interval $w$, the largest allowed distance between neighbouring passes. For a ball end mill of radius $r$ on a nearly flat surface, the interval $w$ that gives a [scallop height](/scallop-height/) $h$ is about $\sqrt{8rh}$. The output is a cutter contact path on the surface, which a CAM system turns into [cutter location data](/cutter-location-data/) by offsetting along the surface normal.

The gap between the passes $v_j$ and $v_{j+1}$ at the parameter $u$ is about $(v_{j+1} - v_j)\,|S_v(u, v_j)|$, where $S_v$ is the partial derivative. The length $|S_v|$ is the stretch of the parameterization across the passes, and it comes from the first [fundamental form](/fundamental-forms/). The passes are $v_j = j/N$, with $N$ chosen so that the largest gap is at most $w$.

On a bilinear patch $S(u, v) = (1-u)(1-v)P_{00} + u(1-v)P_{10} + (1-u)vP_{01} + uvP_{11}$, the surface is linear in $v$ for fixed $u$, so the gap is exactly $|S_v(u)|/N$ with $S_v(u) = (1-u)(P_{01} - P_{00}) + u(P_{11} - P_{10})$. Every iso-curve of a bilinear patch is a straight line, which makes it a doubly [ruled surface](/ruled-surface/).

## The algorithm

```pseudo id=main
ISO-PARAMETRIC(S, w)
L1  M ← max(|S_v(0)|², |S_v(1)|²)          ▷ the largest squared gap factor is at an end
L2  N ← the smallest positive integer with M ≤ N² w²
L3  for j ← 0 to N do
L4      C_j ← the curve u ↦ S(u, j/N), forward for even j and backward for odd j
L5      append C_j, joined to the previous pass along the boundary curve u = 0 or u = 1
L6  return the path
```

Line L1 uses the fact that $|S_v(u)|^2$ is a convex quadratic in $u$ on a bilinear patch, so its largest value is at $u = 0$ or $u = 1$. Line L2 compares rationals, so $N$ is exact. For a [tensor-product](/tensor-product-surface/) [B-spline](/b-spline/) or [NURBS](/nurbs/) surface, line L1 bounds $|S_v|$ over the patch, and line L4 also steps along each curve with a chord tolerance, since the curves are not straight.

## Example

Take the flat trapezoid with $P_{00} = (0, 0, 0)$, $P_{10} = (4, 0, 0)$, $P_{01} = (0, 1, 0)$ and $P_{11} = (4, 4, 0)$, and $w = 1$. Then $S_v(0) = (0, 1, 0)$ and $S_v(1) = (0, 4, 0)$, so $M = 16$ and $N = 4$.

| step | pass | from | to | gap to the next pass at $u = 0$ and $u = 1$ |
|---|---|---|---|---|
| L4, L5 | $v = 0$ | $(0, 0, 0)$ | $(4, 0, 0)$ | $\tfrac14$ and $1$ |
| L4, L5 | $v = \tfrac14$ | $(4, 1, 0)$ | $(0, \tfrac14, 0)$ | $\tfrac14$ and $1$ |
| L4, L5 | $v = \tfrac12$ | $(0, \tfrac12, 0)$ | $(4, 2, 0)$ | $\tfrac14$ and $1$ |
| L4, L5 | $v = \tfrac34$ | $(4, 3, 0)$ | $(0, \tfrac34, 0)$ | $\tfrac14$ and $1$ |
| L4, L5 | $v = 1$ | $(0, 1, 0)$ | $(4, 4, 0)$ | |

The passes fan out: they are $w$ apart at the long side and $w/4$ apart at the short side. The path has length about $24.43$, with $21.93$ on the passes and $2.5$ on the links. Any path that keeps every point of this region within $w/2 = 0.5$ has length at least $(10 - \pi/4)/1 \approx 9.2$, because a path of length $L$ widened by $0.5$ covers at most $L + \pi/4$ of area, and the trapezoid has area 10.

## Correctness

**Theorem.** On a bilinear patch, $N$ is the smallest number of passes with all gaps at most $w$, the path lies on the patch, and every point of the patch is within $w/2$ of the path.

For fixed $u$ the patch is linear in $v$, so the points $S(u, v)$ with $v_j \le v \le v_{j+1}$ form a straight segment on the patch of length $|S_v(u)|/N$ between two passes. The function $|S_v(u)|^2$ is the squared norm of an affine map of $u$, so it is convex and largest at an end, and line L2 makes every such segment at most $w$ long. A point on a segment of length at most $w$ is within $w/2$ of one of its ends. The full proof is in the proof file.

The bound is about the distance between passes. The scallop height that a tool leaves also depends on the tool and the curvature, see [scallop height](/scallop-height/).

## Complexity

Line L2 counts up to $N$, and lines L3 to L5 write $2(N + 1)$ points, so the time is $O(N)$ with $N = \lceil \sqrt{M}/w \rceil$. Integer square roots would give $N$ in time polynomial in the bit size, but the count is cheap next to the path. The extra space is $O(1)$ apart from the output. On a curved patch, each pass also costs one point per forward step, and the number of steps grows with the curvature and shrinks with the chord tolerance.

## Properties

- **Exact passes.** The passes are curves of the surface model, with no intersection to solve and no projection.
- **Patch by patch.** Each patch of a model gets its own passes. The passes of neighbouring patches do not line up, and the boundaries between patches need extra care.
- **Uneven spacing.** The gap varies with $|S_v|$, so the path is longer than needed wherever $|S_v|$ is below its largest value.
- **Conservative.** With $N$ set by the largest gap, no gap exceeds $w$.

## Variants and improvements

- **Adaptive iso-curves.** Elber and Cohen (1994) add passes only where two neighbouring passes are too far apart, so the spacing becomes more even.
- **Iso-planar paths.** Cutting the surface with parallel planes gives passes that run across patch boundaries. See [iso-planar toolpath](/iso-planar-toolpath/).
- **Iso-scallop paths.** Placing each pass from the last one so that the scallop height is constant removes the waste of uneven passes. See [iso-scallop toolpath](/iso-scallop-toolpath/).
- **Reparameterization.** An [arc-length parametrization](/arc-length-parametrization/) of the boundary curves makes the passes more even at the boundaries, but not in general inside the patch.

## When to use it

Use an iso-parametric path for a single patch whose parameterization is close to even, such as a gently bent sheet, and for finishing along the flow of a surface. Avoid it on trimmed patches, on patches that are very distorted, and on models with many small patches, where an iso-planar or iso-scallop path is shorter and more even.

## Pitfalls

- **Trimmed surfaces.** A trimmed patch keeps only part of its parameter square. The iso-curves must be clipped to the trim curves in the parameter plane, or the tool cuts outside the face.
- **Degenerate patches.** At a pole, where a whole boundary of the parameter square maps to one point, all passes meet, and the tool cuts the same point many times.
- **First-order gap only.** On a curved surface, $\Delta v\,|S_v|$ is only an estimate of the gap. The true gap can be larger where $|S_v|$ changes fast.
- **Contact path, not tool path.** The iso-curves give cutter contact points. The tool center is offset from them, and on concave parts with small radius the offset can [gouge](/gouge-detection/) the part.

## Implementations

## History

Iso-parametric paths were the first tool paths for sculptured surfaces, because they come straight from the surface equations of Bezier and B-spline patches. Loney and Ozsoy (1987) described iso-parametric machining of free-form patches. Elber and Cohen (1994) made the passes adaptive, and Choi and Jerard (1998) compare it with the iso-planar and iso-scallop methods in their book.

## References
