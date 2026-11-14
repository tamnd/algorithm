---
tag: K6TS7H
kind: algorithm
slug: pencil-cut-machining
name: Pencil-cut clean-up machining
aliases:
- pencil curve machining
- clean-up toolpath
area: cad/cam-and-additive-manufacturing
level: advanced
summary: Traces the curves along concave corners where a ball end tool touches two surfaces at once, to remove material left by larger tools, as Choi and Jerard describe.
model: real-ram
complexity:
  vars: {m: number of traced points, k: number of corrector steps per point}
  time: {worst: "O(m k)"}
  space: {extra: "O(1)"}
properties: {deterministic: true, recursive: false}
history:
  year: 1998
  people: [Byoung K. Choi, Robert B. Jerard]
  note: Choi and Jerard described pencil-cut paths for clean-up in their 1998 book on sculptured surface machining. Later papers traced pencil curves on polyhedral models.
prereqs: [offset-surface, cutter-location-data, toolpath-planning]
see_also: [pocket-machining, gouge-detection, scallop-height, z-map-model, medial-axis, iso-scallop-toolpath, surface-curvature, nc-verification]
sources:
  - book: isbn:978-0-412-78020-2
    title: Byoung K. Choi and Robert B. Jerard, Sculptured Surface Machining, Theory and Applications, Kluwer Academic Publishers, 1998
    locator: the material on clean-up machining of concave corners and on offset surfaces of the part
  - paper: doi:10.1016/j.cad.2005.03.004
    title: Sang C. Park, Pencil curve detection from visibility data, Computer-Aided Design 37(14), 1492-1498, 2005
    locator: the pencil curve as the path of the ball center sliding along a concave edge, and its computation from an offset triangle mesh
  - paper: "D.-S. Kim, C.-S. Jun and S. C. Park, Tool path generation for clean-up machining by a curve-based approach, Computer-Aided Design 37(9), 967-973, 2005"
    locator: the detection of pencil points from points with two contacts, and the tracing of pencil-cut and fillet-cut paths on polyhedral models
---

Pencil-cut machining is a finishing pass that runs a small ball end mill along the concave corners of a part, where two surfaces meet in a valley or a sharp inside edge. A larger tool used before cannot reach into such corners, so it leaves a strip of material there. The pencil path is the curve along which the ball touches both surfaces at once. Its ball centers are the points at the distance $r$ from both surfaces, which is the intersection of the two [offset surfaces](/offset-surface/) at the distance $r$. The algorithm here traces that intersection with a predictor step along the tangent and a Newton corrector. For two planes the curve is a straight line parallel to the edge at the distance $r/\sin(\alpha/2)$, where $\alpha$ is the opening angle, and the tracer follows it exactly.

## In plain words

A big round cutter cannot get into an inside corner. It always leaves a little rib of material in the corner, like dust in the corner of a room that a broom cannot reach.

The clean-up pass uses a smaller round cutter and pushes it into the corner as far as it goes, so that it touches both walls. Then it slides the cutter along the corner, always touching both walls. The line that the center of the cutter follows is the pencil line, because it looks like a pencil stroke drawn along the corner.

To find the line on curved walls, the computer takes a small step along the corner, and then pulls the cutter back until it touches both walls again.

## The problem

Two surfaces $S_1$ and $S_2$ meet along a concave edge, or come close in a valley, and the free side is where both signed distances are positive. For a ball end mill of radius $r$, let $g_i(x)$ be the signed distance from $x$ to $S_i$ minus $r$. The ball with center $x$ touches $S_i$ from the free side when $g_i(x) = 0$. The pencil curve is
$$
\{\, x : g_1(x) = 0,\ g_2(x) = 0 \,\},
$$
the curve of ball centers that touch both surfaces. The task is to compute it as a sequence of [cutter locations](/cutter-location-data/), with the contact points $x - r n_1$ and $x - r n_2$, where $n_i$ is the unit normal of $S_i$ at the contact. Pencil curves are needed only where the edge is sharper than the ball, that is where the corner fillet has a radius smaller than $r$. Elsewhere the ball touches one surface at a time.

## The algorithm

```pseudo id=main
PENCIL-TRACE(g₁, ∇g₁, g₂, ∇g₂, x₀, h, m)
L1  x ← CORRECT(x₀)                         ▷ the nearest point with g₁ = g₂ = 0
L2  path ← [x]
L3  repeat m times
L4      t ← ∇g₁(x) × ∇g₂(x), normalized and turned to agree with the last t
L5      y ← x + h t                         ▷ predictor along the tangent of the curve
L6      x ← CORRECT(y)                       ▷ Newton steps back onto the curve
L7      append x to path
L8  return path
```

CORRECT repeats the step $x \leftarrow x - J^{\mathsf T}(J J^{\mathsf T})^{-1} g(x)$, where $g = (g_1, g_2)$ and $J$ has the rows $\nabla g_1$ and $\nabla g_2$, until $|g|$ is below a tolerance. It is the smallest move that solves the linearized equations. The tangent of the curve is orthogonal to both gradients, so it is their cross product. The contact points are $x - r\nabla g_i(x)$, since the gradient of a signed distance is the unit normal.

## Example

The floor is $z = 0$ with $n_1 = (0, 0, 1)$. A wall leans out from the line $x = 10$, $z = 0$, with the normal $n_2 = (-4, 0, 3)/5$, so the free side of the wall is $x \le 10 + 0.75 z$. The ball has $r = 5$.

| quantity | value |
|---|---|
| $n_1 \cdot n_2$ | $3/5$ |
| opening angle $\alpha$ | $\arccos(-3/5) = 126.87°$ |
| $r(n_1 + n_2)/(1 + n_1 \cdot n_2)$ | $5 \cdot (-4/5, 0, 8/5)/(8/5) = (-2.5, 0, 5)$ |
| pencil line | $(7.5, y, 5)$ for all $y$ |
| distance from the edge | $\sqrt{2.5^2 + 5^2} = 5.590 = 5/\sin 63.43°$ |
| contact with the floor | $(7.5, y, 0)$ |
| contact with the wall | $(7.5, y, 5) - 5(-0.8, 0, 0.6) = (11.5, y, 2)$ |

The wall contact is on the wall, since $10 + 0.75 \cdot 2 = 11.5$. Started at the origin, the tracer reaches $(7.5, 0, 5)$ in one corrector step and then moves along $y$. For a vertical wall, $n_2 = (-1, 0, 0)$, the line is at $(10 - r, y, r)$, at the distance $r\sqrt 2$ from the edge.

On a floor and a concave cylinder wall of radius $\rho = 20$ with $r = 3$, the traced pencil curve is the circle of radius $\rho - r = 17$ at the height 3, to within $10^{-9}$, and with the step $h = 0.05$ it goes once round in 2136 steps.

## Correctness

**Theorem.** For two planes with unit normals $n_1 \ne \pm n_2$ pointing into the free wedge, the centers of the balls of radius $r$ that lie in the wedge and touch both planes form the line
$$
p + \frac{r}{1 + n_1 \cdot n_2}(n_1 + n_2) + t\,(n_1 \times n_2), \qquad t \in \mathbb{R},
$$
where $p$ is a point of the edge. The line is parallel to the edge at the distance $r/\sin(\alpha/2)$, the contacts are $c - r n_1$ and $c - r n_2$, and no ball in the wedge has its center closer to the edge.

The proof is in the proof file. A ball lies on the free side of a plane and touches it exactly when its center is at the distance $r$, so the centers solve two independent linear equations, and the given point solves them because $n_i \cdot (n_1 + n_2) = 1 + n_1 \cdot n_2$. The distance follows from $|n_1 + n_2|^2 = 2(1 + n_1 \cdot n_2) = 4\sin^2(\alpha/2)$. For two planes the corrector is exact after one step, since the equations are linear, and the predictor moves along the line. So every traced point is on the closed-form line. The tests check this in exact rational arithmetic, with normals such as $(1, 2, 2)/3$ and $(2, 3, 6)/7$, together with the contacts, the squared distance $2r^2/(1 + n_1 \cdot n_2)$, and a brute force search that finds no admissible center closer to the edge.

For curved surfaces the result is local: Newton's method converges near the curve where the gradients are independent. The tracer does not check the ball against other parts of the model.

## Complexity

Each traced point costs one tangent and $k$ corrector steps, and each corrector step evaluates $g_1$, $g_2$ and their gradients and solves a $2 \times 2$ system. With $O(1)$ evaluation, $m$ points take $O(mk)$ time and $O(1)$ extra space besides the path. For planes $k = 1$. On a triangle mesh, the evaluation of the offset distances is the main cost, and practical systems use spatial search structures or the [z-map](/z-map-model/) of the offset surface.

## Properties

- **Exact for planar corners.** The pencil path of two planes is a straight line at a closed-form position.
- **Deepest reach.** The pencil ball is the one that goes furthest into the corner. No ball in the corner is closer to the edge.
- **Two contacts.** Along the path the tool touches both surfaces, so it cuts the rest material from both sides of the corner.
- **Local tracing.** The tracer follows one branch of the curve from a start point. Finding the start points is a separate step.

## Variants and improvements

- **Mesh-based detection.** On triangle meshes, Park computed pencil curves from an offset mesh and the visibility of its intersections. Kim, Jun and Park found pencil points from scanning paths with two contacts and traced the pencil-cut path from them.
- **Bitangency angle.** CAM systems mark a point as a pencil point when the two contact normals differ by more than a chosen angle. Small angles find shallow valleys too.
- **Multiple pencil passes.** Parallel passes on both sides of the pencil curve, at offsets set by the [scallop height](/scallop-height/), clean a wider band after the main pass.
- **Five-axis pencil cuts.** Tilting the tool lets a longer tool reach deep corners and keeps the holder clear of the walls.
- **Corners in 2D.** In [pocket machining](/pocket-machining/), the same formula gives the position of a tool touching both walls of a corner with angle $\alpha$, at the distance $r/\sin(\alpha/2)$ from the corner point.

## When to use it

Use pencil cuts after roughing and finishing with a larger ball, on molds and dies with fillets and sharp inside edges. The pass is short and removes the material that the larger tool left in the corners, before the final finishing with a small tool or before a smaller pencil pass. Where the fillet radius is larger than the ball, no pencil curve exists there, and ordinary finishing reaches the corner.

## Pitfalls

- **Global gouges.** The tracer looks only at two surfaces. Near a third surface the ball can gouge, so the path must be checked by [gouge detection](/gouge-detection/).
- **Tangent surfaces.** Where the two surfaces become tangent, the gradients are parallel, the pencil curve ends, and the corrector fails. The trace must stop there.
- **Branch jumps.** A long step can land the predictor near another branch of the curve, and the corrector then follows the wrong corner. Keep $h$ small compared with the size of the features.
- **Full load in the corner.** The pencil tool cuts on both sides of the corner at once, and the material left by the larger tool can be thick. Several passes with growing depth, or a lower feed, protect the tool.
- **Sign of the normals.** The formula needs the normals that point into the free region. With one normal reversed the line lies inside the material.

## Implementations

## History

Clean-up machining of corners came with the CAM systems for sculptured surfaces in the 1990s. Choi and Jerard described pencil-cut paths in their 1998 book, as the path of a ball that touches two surfaces at once. In 2005 Park computed pencil curves from the visibility of intersections on an offset triangle mesh, and Kim, Jun and Park traced pencil-cut and fillet-cut paths on polyhedral models from points with two contacts. Commercial CAM systems offer pencil passes with a bitangency angle as the main setting.

## References
