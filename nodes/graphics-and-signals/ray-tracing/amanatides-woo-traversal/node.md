---
tag: 4NS679
kind: algorithm
slug: amanatides-woo-traversal
name: Amanatides-Woo grid traversal
aliases:
- 3D-DDA
- voxel traversal
area: graphics-and-signals/ray-tracing
level: advanced
summary: Walk a ray through the cells of a uniform 3D grid in order, one face step at a time, with per-axis values tMax and tDelta. Each step costs two comparisons and one addition.
solves: [closest-hit-query, any-hit-query]
model: real-ram
complexity:
  vars: {k: "the number of cells visited, 1 + |Δi| + |Δj| + |Δk|", g: "the number of cells along the longest axis of the grid"}
  time: {worst: Θ(k), best: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, exact: true, incremental: true, recursive: false}
history:
  year: 1987
  people: [John Amanatides, Andrew Woo]
  note: Amanatides and Woo presented the traversal at Eurographics 1987 as a variant of the DDA line algorithm without a preferred axis, together with the ray ID mailbox that avoids testing an object twice.
prereqs: [uniform-grid, slab-method]
see_also: [digital-differential-analyzer, bresenham-line-algorithm, octree, kd-tree-traversal, bvh-traversal, ray-marching, ray-coherence, ieee-754]
sources:
  - paper: doi:10.2312/egtp.19871000
    title: John Amanatides and Andrew Woo, A fast voxel traversal algorithm for ray tracing, Eurographics 1987, North-Holland, pages 3 to 10
    locator: the whole paper (the initialization with tMaxX and tDeltaX, the incremental loop with its comparisons, the 3D version with the justOut test, the rule that a hit must lie in the current voxel, and the rayID mailbox with its table of results)
  - paper: doi:10.1109/MCG.1986.276715
    title: Akira Fujimoto, Takayuki Tanaka and Kansei Iwata, ARTS, accelerated ray-tracing system, IEEE Computer Graphics and Applications 6(4), 1986, pages 16 to 26
    locator: the 3D digital differential analyzer that walks a uniform grid along a driving axis, the method that Amanatides and Woo simplify
  - paper: doi:10.1109/MCG.1984.6429331
    title: Andrew S. Glassner, Space subdivision for fast ray tracing, IEEE Computer Graphics and Applications 4(10), 1984, pages 15 to 24
    locator: the octree subdivision of space and the step from one cell to the next along the ray
---

The Amanatides and Woo traversal lists, in order along a ray, the cells of a [uniform grid](/uniform-grid/) that the ray passes through. It keeps for each axis the ray parameter $t_{\max}$ at which the ray crosses the next cell boundary on that axis, and the parameter distance $t_\Delta$ between two such boundaries. At each step it moves to the face neighbor on the axis with the smallest $t_{\max}$ and adds $t_\Delta$ to that value. The loop has no multiplication and no division. Ray tracers use it to visit only the objects stored in the cells along a ray, nearest first, so that they can stop at the first cell that holds a hit. The same walk serves voxel rendering, line of sight on a tile map and the sampling of volume data cell by cell.

## In plain words

Picture a room full of equal boxes stacked in rows, columns and layers, and a thin straight wire through it. You want the list of boxes the wire passes through, from the near end to the far end. A box has six walls. From the box where you are, the wire leaves through one wall, into the box on the other side of that wall.

So for each of the three directions you keep one number: how far along the wire you are when you hit the next wall in that direction. The smallest of the three numbers tells you which wall comes first. You step through it, and then that direction's number grows by the same fixed amount every time, because the walls are evenly spaced. Nothing else changes.

## The problem

Given a grid of $n_x \times n_y \times n_z$ cubic cells of side $s$ with lowest corner $\ell$, and a ray segment $r(t) = o + t d$ for $t \in [t_0, t_1]$, list the cells that the segment meets, ordered by the parameter at which the segment enters them. For a ray tracing query, also find the closest object hit, given a list of objects stored in each cell that they overlap.

When the segment crosses an edge or a corner of the grid exactly, it touches cells at a single point. The walk then visits only some of them, as described in Properties. For all other segments the list is exact.

This is not the same output as the [digital differential analyzer](/digital-differential-analyzer/) or [Bresenham's algorithm](/bresenham-line-algorithm/) for lines. Those draw one pixel per step of the major axis of a 2D line, so the pixels are 8-connected and some cells that the line crosses are left out. The grid walk has no major axis: it visits every cell crossed, and consecutive cells share a face.

## The algorithm

```pseudo id=main
L1  clip [t0, t1] to the grid box with the slab method → [tenter, tend]; stop if empty
L2  cell ← the cell that contains o + tenter·d (clamped to the grid)
L3  for each axis a:
        step[a] ← sign(d[a])
        tMax[a] ← t where the ray meets the next a-boundary of cell (∞ if d[a] = 0)
        tDelta[a] ← s / |d[a]| (∞ if d[a] = 0)
L4  loop
L5      a ← an axis with the smallest tMax:
            if tMax[x] < tMax[y] then a ← (x if tMax[x] < tMax[z] else z)
            else a ← (y if tMax[y] < tMax[z] else z)
L6      visit cell for t in [tin, min(tMax[a], tend)]
L7      if tMax[a] > tend then stop               ▷ the segment ends in this cell
L8      cell[a] ← cell[a] + step[a]
L9      if cell[a] is outside 0 .. n[a] − 1 then stop   ▷ justOut
L10     tin ← tMax[a], tMax[a] ← tMax[a] + tDelta[a]
```

Line L5 is the comparison chain of the paper. It always picks an axis with the minimum value. When two values are equal it picks the later axis: $y$ over $x$, $z$ over $x$ and $z$ over $y$.

In a ray tracer, line L6 tests the objects of the cell. A hit with parameter $t$ counts only if $t \le \min(t_{\max}[a], t_\text{end})$, the exit of the cell. Amanatides and Woo state this rule: an object that spans several cells can be hit at a point beyond the current cell, and a nearer object can wait in the next cell. If the cell gives a hit, the walk stops. They also store in each object the ID of the last ray that tested it, a *mailbox*, so that an object in many cells is tested only once per ray.

## Example

A $4 \times 4 \times 4$ grid of unit cells with $\ell = (0, 0, 0)$. The ray starts at $o = (0.2, 0.3, 0.1)$ inside the grid with $d = (1, 0.5, 0.25)$. Line L3 gives $t_{\max} = (0.8, 1.4, 3.6)$ and $t_\Delta = (1, 2, 4)$.

| visit | cell | $t_{\max}$ before the step | axis | entry $t$ |
|---|---|---|---|---|
| 1 | (0, 0, 0) | (0.8, 1.4, 3.6) | x | 0 |
| 2 | (1, 0, 0) | (1.8, 1.4, 3.6) | y | 0.8 |
| 3 | (1, 1, 0) | (1.8, 3.4, 3.6) | x | 1.4 |
| 4 | (2, 1, 0) | (2.8, 3.4, 3.6) | x | 1.8 |
| 5 | (3, 1, 0) | (3.8, 3.4, 3.6) | y | 2.8 |
| 6 | (3, 2, 0) | (3.8, 5.4, 3.6) | z | 3.4 |
| 7 | (3, 2, 1) | (3.8, 5.4, 7.6) | x | 3.6 |

After visit 7 the step on $x$ gives $i = 4$, outside the grid, at $t = 3.8$, where the ray leaves through the face $x = 4$. The walk visited $7 = 1 + 3 + 2 + 1$ cells: one start cell and one cell per boundary crossed. The implementation reproduces these cells and entry parameters exactly with rational arithmetic, and the tests compare the walk with a brute force list of every cell that the segment meets, computed with exact fractions.

## Correctness

The invariant at line L6 is: for every $t \in [t_\text{in}, \min_b t_{\max}[b]]$, the point $r(t)$ is in the closed current cell, and for each axis $a$ with $d_a \ne 0$, $t_{\max}[a]$ is the parameter at which the ray leaves the current cell's slab on axis $a$. Line L2 makes it true at the start. A step on the axis $a$ with the smallest $t_{\max}$ moves to the cell on the other side of the face that the ray crosses at $t_{\max}[a]$. That cell's slab on axis $a$ ends one cell width later, at $t_{\max}[a] + t_\Delta[a]$, and its slabs on the other axes are unchanged. So the visited cells cover $[t_\text{enter}, t_\text{end}]$ in consecutive closed pieces.

When no two boundary crossings happen at the same $t$ and the endpoints do not lie on a boundary, the minimum in line L5 is unique, each crossing changes the cell that contains the open piece of the segment, and the walk lists exactly the cells that the segment meets, in order of entry. In every case, the walk lists distinct face-adjacent cells, each met by the segment, including every cell whose interior the segment meets. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Each pass of the loop does at most two comparisons in line L5, one comparison with $t_\text{end}$, one index test and one addition. Each pass moves one cell on one axis in the direction of $d$, and the walk never turns back, so the number of cells is $k = 1 + |\Delta i| + |\Delta j| + |\Delta k|$, where $\Delta$ is the difference of the indices of the first and the last cell. This is at most $n_x + n_y + n_z - 2 \le 3g$. So the traversal takes $\Theta(k)$ time, and $\Theta(1)$ in the best case, when the segment stays in one cell. The extra space is $\Theta(1)$. The initialization costs a constant number of divisions; the paper counts 33 floating-point operations for a ray that starts inside the grid.

For a closest-hit query the cost adds the object tests in the visited cells. With a mailbox, each object is tested at most once per ray, so the total is $O(k + n)$ for $n$ objects, which is the worst case for every [closest-hit query](/closest-hit-query/) structure. Whether a grid beats a [BVH](/bvh-traversal/) or a [kd-tree](/kd-tree-traversal/) depends on how evenly the objects fill space. That comparison is measured on scenes, not proved.

## Properties

- **Exact with exact arithmetic.** With rational coordinates the walk is exact. With floating point, $t_{\max}$ grows by repeated addition and drifts; see Pitfalls.
- **Face-connected.** Consecutive cells share a face. A ray that crosses an edge exactly visits one of the two side cells, not both, and a ray through a corner visits two of the three.
- **Monotone.** Each index changes in one direction only, so no cell is visited twice.
- **Ordered by distance.** The cells come in order of entry along the ray. A ray tracer can stop at the first cell that holds a hit inside that cell.
- **No preferred axis.** Unlike the 3D DDA of Fujimoto, Tanaka and Iwata, which drives one axis and corrects the other two, the walk treats the three axes the same way.
- **Tie rule depends on the direction.** At an exact corner crossing, the walk of a reversed ray can pick different side cells, as with the tie rule of [Bresenham's algorithm](/bresenham-line-algorithm/).

## Variants and improvements

- **2D and $n$-D.** The same loop works in any dimension with one $t_{\max}$ and one $t_\Delta$ per axis. The paper presents the 2D loop first.
- **Hierarchical grids and octrees.** In an [octree](/octree/) or a grid of grids, the same step runs inside each node, and the walk goes up or down a level at the node boundary. Large empty regions then cost one step.
- **Sparse voxel data.** Voxel engines run the walk over a hash of occupied blocks ([spatial hashing](/spatial-hashing/)) and skip empty blocks with a coarser walk.
- **Volume sampling.** Visiting every cell with its entry and exit parameters gives the exact length of the ray in each cell, which a volume renderer can use in place of the fixed step of [ray marching](/ray-marching/).
- **Integer version.** With integer endpoints, all $t_{\max}$ values have the common denominators $|d_x|$, $|d_y|$, $|d_z|$. Multiply through and compare integers, which makes the walk exact without fractions.
- **Supercover lines.** When the cells touched at a corner must all be listed, add the side cells at each tie. The result is the closed set of cells met, at the cost of extra cells at each tie.

## When to use it

Use the grid walk when the scene or the data already lives on a uniform grid: voxel scenes, volume data, occupancy maps, tile maps, and ray tracing of many small objects that are spread evenly. It is short, fast per step, and easy to make exact. Prefer a [BVH](/bounding-volume-hierarchy/) or a [kd-tree](/kd-tree-traversal/) when object sizes and densities vary widely. A grid fine enough for a dense part of the scene wastes steps in the empty parts, and a coarse grid puts many objects in one cell. This is the "teapot in a stadium" problem of uniform grids.

## Pitfalls

- **Accepting a hit beyond the current cell.** An object that spans several cells can be hit beyond the cell exit. If the walk stops there, it can return that object although a nearer one is in the next cell. The tests build this case: without the check of line L6 the far object wins.
- **Drift of tMax.** Adding $t_\Delta$ thousands of times in floating point accumulates rounding error (see [machine epsilon](/machine-epsilon/)). On long rays the walk can step one cell early or late at a corner. Recompute $t_{\max}[a] = (\ell_a + (c_a + 1)s - o_a)/d_a$ from the cell index when exactness matters, or use rational or integer arithmetic.
- **Zero direction components.** For $d_a = 0$, set $t_{\max}[a] = t_\Delta[a] = \infty$ explicitly. Dividing by a negative zero in [IEEE 754](/ieee-754/) arithmetic gives $-\infty$, and the walk then steps forever on that axis.
- **The start cell.** When the ray starts outside the grid, clip it first with the [slab method](/slab-method/), then compute the start cell from the entry point. Rounding can put the entry point just outside the grid; clamp the index to the valid range.
- **Testing an object many times.** Without a mailbox, an object in $m$ cells is tested up to $m$ times per ray. Store the last ray ID in the object, or keep a small set per ray as the implementation does. In parallel code, a per-object mailbox is shared state; use a per-ray cache instead.
- **Ties at grid corners.** A test that expects a closed set of cells (all cells touched) fails for rays through exact corners and along grid planes, because the walk visits a face-connected path. Decide which set the caller needs.

## Implementations

## History

Fujimoto, Tanaka and Iwata (1986) introduced the 3D digital differential analyzer for walking a uniform grid in their ARTS system. Their walk followed a driving axis, as a line drawing DDA does, and corrected the two other axes. Glassner (1984) had stepped through an octree by locating the next cell from a point just past the current cell boundary. Amanatides and Woo (1987) observed that the walk needs no driving axis: one comparison chain on three values decides each step. Their paper also gave the rule that a hit counts only inside the current voxel, and the rayID mailbox. The walk is often called the 3D DDA or simply voxel traversal.

## References
