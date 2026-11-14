---
tag: QH2CZJ
kind: data-structure
slug: dexel-representation
name: Dexel representation
aliases:
- depth element representation
- tri-dexel
area: cad/cam-and-additive-manufacturing
level: advanced
summary: Van Hook's solid model as a grid of rays, each holding the depth intervals where it is inside, which makes Boolean subtraction of the tool fast.
model: real-ram
complexity:
  vars: {k: total number of intervals on the two rays, c: number of rays in the bounding box of one tool move, M: number of intervals in the model}
  time: {boolean: "O(k)", cut: "O(c k)"}
  space: {extra: "O(M)"}
properties: {deterministic: true, exact: true}
history:
  year: 1986
  people: [Tim Van Hook]
  note: Van Hook introduced dexels in 1986 to show NC milling in real time. Benouamer and Michelucci used three orthogonal ray grids in 1997, the tri-dexel model.
prereqs: [z-map-model, interval-list-intersection, regularized-set-operations]
see_also: [nc-verification, swept-volume, csg-ray-casting, ray-casting, depth-peeling, spatial-occupancy-enumeration, interval-merging, two-pointers]
sources:
  - paper: doi:10.1145/15922.15887
    title: Tim Van Hook, Real-time shaded NC milling display, Computer Graphics 20(4) (SIGGRAPH 86), 1986, 15 to 20
    locator: the dexel structure (near and far depth per pixel, linked lists per pixel) and the subtraction of the tool in image space
  - paper: doi:10.1145/267734.267755
    title: Mohand Ourabah Benouamer and Dominique Michelucci, Bridging the gap between CSG and Brep via a triple ray representation, ACM Symposium on Solid Modeling and Applications 1997
    locator: the triple ray representation, three orthogonal grids of ray intervals, and the conversion to a boundary representation
  - book: isbn:978-0-412-78020-2
    title: Byoung K. Choi and Robert B. Jerard, Sculptured Surface Machining, Theory and Applications, Kluwer, 1998
    locator: the part on controlling accuracy and quality, on stock models for NC verification
  - paper: doi:10.1016/0010-4485(78)90058-1
    title: Robert O. Anderson, Detecting and eliminating collisions in NC machining, Computer-Aided Design 10(4), 1978, 231 to 237
    locator: the earlier single-height grid that dexels extend
---

A dexel representation models a solid by a grid of parallel rays. For each ray it stores the depths where the ray enters and leaves the solid, as a sorted list of intervals. A single interval on a ray is a dexel, short for depth element. Van Hook (1986) introduced the structure to show NC milling in real time: the rays were the pixels of the screen, and cutting the stock was a subtraction of the tool's intervals from the stock's intervals, pixel by pixel. Unlike a [z-map](/z-map-model/), which stores one height per line, a dexel ray can hold any number of intervals, so undercuts, holes across the ray direction and tilted tools are no problem. Each Boolean operation on two rays is one merge of two sorted lists, in time linear in the number of intervals. The model still samples the solid only on the rays, so details between rays are lost. A tri-dexel model uses three grids along $x$, $y$ and $z$ to lower that loss.

## In plain words

Push many thin straight wires through a block, all in the same direction, in a regular grid. On each wire, write down where it goes into the material and where it comes out. If the block has a hole across the wire, the wire goes in and out twice, and you write two pieces.

That list of pieces per wire is the whole model. To cut away the volume of a tool, find the piece of each wire that is inside the tool, and remove it from the pieces of the block. Joining two solids or keeping only their common part works the same way, wire by wire.

The model only knows the material on the wires. Anything thinner than the gap between wires can be missed.

## The abstract type

The rays are the vertical lines through a grid of points $q_{ij} = (x_0 + ih, y_0 + jh)$, $0 \le i < n_x$, $0 \le j < n_y$, all in the direction $+z$. A dexel list on a ray is $I = [(l_1, u_1), \dots, (l_m, u_m)]$ with
$$l_1 < u_1 < l_2 < u_2 < \dots < l_m < u_m,$$
and stands for the union of the closed intervals $[l_k, u_k]$. Intervals do not touch: two intervals that share an end are one interval. The model stands for the set of points $(q_{ij}, z)$ with $z$ in the list of ray $(i, j)$. The operations are:

- $\mathrm{BOX}(z_0, z_1)$: every ray holds $[(z_0, z_1)]$.
- $\mathrm{COMBINE}(I, J, \mathrm{op})$: the regularized result of a Boolean function on two rays, for union ($a \vee b$), intersection ($a \wedge b$) and difference ($a \wedge \neg b$).
- $\mathrm{CUT}(c_0, c_1, r)$: subtract the volume swept by a ball-end mill of radius $r$ whose ball center moves from $c_0$ to $c_1$, with or without its shank.
- $\mathrm{INSIDE}(i, j, z)$ and $\mathrm{VOLUME}$: membership on a ray, and the estimate $h^2 \sum (u_k - l_k)$.

The results are regularized, as in [regularized set operations](/regularized-set-operations/): the result is the closure of the interior of the pointwise result. On a ray this drops pieces of length zero, such as the common end point of two touching intervals in an intersection.

## Representation

Each ray stores its list as an array of pairs, or as a linked list as in Van Hook's paper, where each node held a near depth, a far depth and a color for display. The grid of rays is an $n_x \times n_y$ array of such lists. The space is linear in the total number of intervals. A block with no holes needs one interval per ray, which is the same as a z-map with a bottom. Each hole that a ray crosses adds one interval.

In the tri-dexel model of Benouamer and Michelucci (1997), the same solid is stored three times, with rays along $x$, along $y$ and along $z$. A surface that is parallel to the rays of one grid, such as a vertical wall in a $z$ grid, cuts the rays of the other two grids at a good angle. This allows a boundary to be rebuilt from the three grids with much less error than from one.

## Operations

```pseudo id=main
COMBINE(I, J, op)                    ▷ two dexel lists; op(false, false) = false
L1  P ← the endpoints of I and of J, merged in increasing order, without repeats
L2  out ← empty list;  i ← 1;  j ← 1
L3  for each pair (p, p') of consecutive values in P do
L4      while i ≤ |I| and I[i].u ≤ p do i ← i + 1
L5      while j ≤ |J| and J[j].u ≤ p do j ← j + 1
L6      a ← (i ≤ |I| and I[i].l ≤ p);  b ← (j ≤ |J| and J[j].l ≤ p)
L7      if op(a, b) then
L8          if out is not empty and last(out).u = p then last(out).u ← p'
L9          else append (p, p') to out
L10 return out

CUT(D, c0, c1, r)                    ▷ ball centers c0, c1; radius r
L11 for each ray q in the xy box of the move, grown by r do
L12     S ← the segment of the ray inside the swept tool       ▷ [lo, hi], or [lo, ∞) with a shank
L13     if S has positive length then D[q] ← COMBINE(D[q], [S], a and not b)
```

The endpoints cut the ray into open cells, and on each cell both inputs are constant. Lines L4 and L5 move each pointer to the first interval that is not over yet, and line L6 reads whether the current cell is inside it. Line L8 joins the cell to the previous output interval when they meet, so the output never has two touching intervals.

Line L12 needs the part of the ray inside the swept tool. Without the shank, the tool sweeps a capsule, the set of points within $r$ of the segment $c_0 c_1$, which is convex, so the part is one interval. Its lower end is the lowest point of the swept ball on the line, computed in closed form on the [z-map page](/z-map-model/). Its upper end is the same quantity for the mirror image of the move in the plane $z = 0$, with the sign changed. With the shank, the part runs up to $+\infty$.

**Exact arithmetic.** COMBINE only compares endpoints, so with integer or rational endpoints it is exact, and the result of a long sequence of operations does not drift. The ends of the tool segment have square roots. The code computes them in floating point and the tests compare them with an exact rational test of membership in the swept tool, to one part in $10^9$. A ray that is tangent to the tool gives a segment of length about zero, and line L13 leaves the ray unchanged, which is the right regularized answer.

## Example

Take the ray $I = [(0, 2), (4, 6)]$ and $J = [(1, 5)]$, and compute $I \setminus J$, so $\mathrm{op}(a, b) = a \wedge \neg b$. Line L1 gives $P = (0, 1, 2, 4, 5, 6)$.

| cell | $i$ after L4 | $a$ | $j$ after L5 | $b$ | op | out |
|---|---|---|---|---|---|---|
| $(0, 1)$ | 1 | true | 1 | false | true | $[(0, 1)]$ |
| $(1, 2)$ | 1 | true | 1 | true | false | $[(0, 1)]$ |
| $(2, 4)$ | 2 | false | 1 | true | false | $[(0, 1)]$ |
| $(4, 5)$ | 2 | true | 1 | true | false | $[(0, 1)]$ |
| $(5, 6)$ | 2 | true | 2 | false | true | $[(0, 1), (5, 6)]$ |

The union gives $[(0, 6)]$, the intersection $[(1, 2), (4, 5)]$, and $J \setminus I$ gives $[(2, 4)]$. The union of the touching rays $[(0, 1)]$ and $[(1, 2)]$ is $[(0, 2)]$, and their intersection is empty after regularization.

Now a cut that a z-map cannot store. The stock is the box $[0, 4] \times [0, 2] \times [0, 4]$ on a grid with $h = 1$, so every ray holds $[(0, 4)]$. A ball of radius $1$ with no shank moves from $(0, 1, 2)$ to $(4, 1, 2)$, inside the block, as when a tool with a ball on a thin neck reaches under an overhang. The ray at $(2, 1)$ passes through the axis of the tunnel, and becomes $[(0, 1), (3, 4)]$: two intervals. The ray at $(2, 0)$ is at distance $1$ from the axis, so it only touches the tool at $z = 2$, and it stays $[(0, 4)]$. With the shank, the ray at $(2, 1)$ becomes $[(0, 1)]$, the open slot that a z-map would also show.

## Correctness

The endpoints of both lists cut the ray into open cells. On each cell, each input is constant, because no endpoint lies inside it, so the pointwise result is constant too. Outside the endpoints both inputs are empty, and the result is empty because $\mathrm{op}(\text{false}, \text{false})$ is false. So the regularized result is the union of the closed cells where op is true. After lines L4 and L5, the pointers stand at the first interval of each list that ends after the cell starts. That interval contains the cell if it starts at or before the cell, and otherwise the cell is in a gap, which is what line L6 reads. Lines L7 to L9 output the true cells and merge neighbours, so the output is a valid dexel list. For the cut, the swept capsule is convex, so it meets a ray in one interval, and with a shank the interval is unbounded above. The full proof is in proofs/correctness.md.

## Complexity

COMBINE on lists of $m_1$ and $m_2$ intervals takes $O(m_1 + m_2)$ time: the merge of line L1 is linear, the loop runs fewer than $2(m_1 + m_2)$ times, and the two pointers only move forward. The output has at most $m_1 + m_2$ intervals for union, intersection and difference. A cut of one move visits the $c$ rays in its bounding box and does one COMBINE on each, so it costs $O(c\,(m + 1))$ for $m$ intervals per ray. For a block that the tool only cuts from above, $m$ stays 1, and a cut costs $O(c)$, like a z-map. The space is the total number of intervals. A tri-dexel model keeps three grids, so for $n$ rays per side it stores $3n^2$ rays in place of $n^2$, but far fewer than the $n^3$ cells of a voxel grid of the same resolution.

## Variants

- **Image space dexels.** Van Hook took the rays to be the pixels of the view, so the display is free: draw the near end of the first interval of each ray. The model must be rebuilt if the view changes.
- **Tri-dexel.** Three orthogonal grids, as above. A boundary mesh can be built from them, for example with a variant of [marching cubes](/marching-cubes/) that uses the exact crossing points on the rays.
- **Ray representation in solid modeling.** The same structure, sampled by [ray casting](/ray-casting/) through a CSG tree, can serve for mass properties and for Boolean operations of solids (see [CSG ray casting](/csg-ray-casting/)).
- **Depth layers in graphics.** [Depth peeling](/depth-peeling/) on the GPU builds the intervals of all pixels from a mesh, one layer per pass.
- **Run-length view.** On a ray, a dexel list is a [run-length encoding](/run-length-encoding/) of a column of voxels with real end points.
- **Normals and colors.** Store the surface normal and a tag of the cutting move at each end of an interval, to shade the result and to find the move that made a gouge.

## When to use it

Use dexels for machining simulation when the z-map is not enough: 5-axis milling, tools that reach under an overhang, turning and mill-turn, and parts with holes across the view direction. Use them when Boolean operations must be fast and robust and an approximate result on a grid is acceptable. When an exact boundary is needed, as in a final B-rep of the machined part, use [solid Boolean operations](/solid-boolean-operations/) on a [boundary representation](/boundary-representation/) instead, or rebuild a boundary from a tri-dexel model and accept its error.

## Pitfalls

- **Touching intervals.** If the code keeps $[(0, 1), (1, 2)]$ as two intervals, the number of intervals grows with each operation, and two lists for the same set compare as different. Merge them, as line L8 does.
- **Pieces of length zero.** A tool that touches a ray at one point must not split an interval into two with a gap of length zero. Regularize the result.
- **Steep surfaces.** A surface almost parallel to the rays is sampled badly, the same as in a z-map. Use three grids, or rays along the tool axis.
- **The view changes.** Image space dexels belong to one view. Rotating the view needs new rays, so most simulators keep the dexels in object space and draw them separately.
- **Floating point drift.** If the tool segments are rounded, a later pass of the same tool can leave slivers of $10^{-15}$. Drop intervals shorter than a stated tolerance, or keep the endpoints exact.
- **Memory.** A part with many holes across the rays has many intervals per ray. Budget for the worst ray, not for the mean.

## Implementations

## History

Anderson (1978) stored one height per grid point for NC simulation. Van Hook (1986) generalized this to lists of depth intervals per pixel, called them dexels, and used them for a shaded display of NC milling in real time on the hardware of the time, with the tool subtracted pixel by pixel. Ray representations of solids came up in solid modeling around the same time, as the output of ray casting through CSG trees. Benouamer and Michelucci (1997) used three orthogonal grids of rays, the triple ray or tri-dexel representation, to convert CSG models to boundary representations. Later work on the simulation of multi-axis machining uses the tri-dexel model as a stock model.

## References
