---
tag: 5REJ5X
kind: data-structure
slug: z-map-model
name: Z-map model
aliases:
- height field stock model
area: cad/cam-and-additive-manufacturing
level: core
summary: Represents the stock in 3-axis machining simulation as a grid of heights, each lowered by the tool as it passes over, fast but blind to undercuts.
model: real-ram
complexity:
  vars: {N: number of grid columns, c: number of columns in the bounding box of one linear tool move}
  time: {cut: "O(c)", query: "O(1)"}
  space: {extra: "O(N)"}
properties: {deterministic: true, exact: false}
history:
  year: 1978
  people: [Robert O. Anderson]
  note: Later authors credit Anderson's 1978 paper on collisions in NC machining with the grid of heights. Jerard, Drysdale and coauthors analysed discrete simulation with such grids in 1989.
prereqs: [nc-verification, cutter-location-data]
see_also: [dexel-representation, swept-volume, gouge-detection, scallop-height, toolpath-planning, z-buffer, spatial-occupancy-enumeration, convex-function]
sources:
  - paper: doi:10.1016/0010-4485(78)90058-1
    title: Robert O. Anderson, Detecting and eliminating collisions in NC machining, Computer-Aided Design 10(4), 1978, 231 to 237
    locator: the stock and the tool as heights over a grid, and the collision test on it
  - paper: "Robert B. Jerard, Robert L. Drysdale, Kenneth Hauck, Barry Schaudt and John Magewick, Methods for detecting errors in numerically controlled machining of sculptured surfaces, IEEE Computer Graphics and Applications 9(1), 1989, 26 to 39"
    locator: simulation with vectors along the surface normals and with height grids, and the errors each one finds
  - paper: "Robert L. Drysdale, Robert B. Jerard, Barry Schaudt and Ken Hauck, Discrete simulation of NC machining, Algorithmica 4(1), 1989, 33 to 60"
    locator: the cost and the accuracy of point-sample simulation as a function of the grid spacing
  - book: isbn:978-0-412-78020-2
    title: Byoung K. Choi and Robert B. Jerard, Sculptured Surface Machining, Theory and Applications, Kluwer, 1998
    locator: the part on controlling accuracy and quality, on the z-map model and NC verification
---

A z-map is a model of the stock in 3-axis milling. It puts a grid of vertical lines over the workpiece and stores one number per line: the height of the top of the material there. A cut by a tool that points down lowers each height to the lowest point of the tool's [swept volume](/swept-volume/) on that line, if that point is below the old height. The model is the oldest and simplest stock model for [NC verification](/nc-verification/), and it is usually credited to Anderson (1978). A cut costs a constant time per grid line under the tool, and a query of one height costs $O(1)$. The price is that a column can hold only one interval of material, from the bottom to the top. The model cannot show an undercut, a hole across the tool axis or a cut by a tilted tool. The [dexel representation](/dexel-representation/) removes this limit.

## In plain words

Think of a bed of nails pushed up from below through a board, so that their heads form the top of a block. Each nail has its own height. The block is everything below the nail heads.

A milling cutter comes down from above and moves over the block. Wherever it passes over a nail, it pushes that nail down to the lowest point the cutter reaches there. A nail that the cutter does not reach keeps its height.

To show the result, draw the nail heads as a surface. To check for an error, compare each nail with the height the part should have at that point.

The nails can only show material that goes straight down to the floor. A pocket cut in from the side has nowhere to go.

## The abstract type

The domain is a rectangle $[x_0, x_0 + (n_x - 1)h] \times [y_0, y_0 + (n_y - 1)h]$ with a grid of spacing $h$, and $N = n_x n_y$ grid points $q_{ij} = (x_0 + ih, y_0 + jh)$. The model stands for the solid
$$M = \bigcup_{i,j} \{q_{ij}\} \times [z_b, H_{ij}],$$
a set of vertical segments, one per grid point, above a fixed bottom $z_b$. The operations are:

- $\mathrm{INIT}(top)$: a block with all $H_{ij} = top$.
- $\mathrm{CUT}(c_0, c_1, r)$: remove the volume swept by a ball-end mill of radius $r$, axis along $+z$, whose ball center moves on the segment from $c_0$ to $c_1$.
- $\mathrm{HEIGHT}(i, j)$ and $\mathrm{INSIDE}(i, j, z)$: read a height, and test $z_b \le z \le H_{ij}$.
- $\mathrm{VOLUME}$: the estimate $h^2 \sum_{ij} (H_{ij} - z_b)$.

A toolpath given as [cutter location data](/cutter-location-data/) is a sequence of such moves. This page uses the ball center as the reference point of the tool. Many systems use the tip, which is the center minus $r$ along the axis.

## Representation

The model is an $n_x \times n_y$ array of heights, nothing more. The grid is often the pixel grid of the screen in a view from above, so that the z-map is close to a [z-buffer](/z-buffer/) that is kept between frames. Two facts about the tool make one height enough:

- The tool axis is parallel to $z$, and the tool includes its shank, which goes up without end. So on each vertical line, the swept tool is a ray $[z_{lo}, \infty)$, and the material that stays is again one segment $[z_b, \min(H, z_{lo})]$.
- The removal is a set difference, so the order of the moves does not change the result: the final height is the minimum over all moves.

On the vertical line at $q$, write $d(t)$ for the horizontal distance from $q$ to the ball center $c(t) = c_0 + t(c_1 - c_0)$. Where $d(t) \le r$, the lowest point of the ball on the line is $f(t) = c_z(t) - \sqrt{r^2 - d(t)^2}$. So $z_{lo} = \min f(t)$ over the $t \in [0, 1]$ with $d(t) \le r$. The function $f$ is [convex](/convex-function/), and its minimum has a closed form, the stationary point clamped to the interval.

## Operations

```pseudo id=main
CUT(H, c0, c1, r)                      ▷ ball centers c0, c1; radius r
L1  box ← the xy box of c0 and c1, grown by r on each side
L2  for each grid point q = (x_i, y_j) in box do
L3      zlo ← LOWEST(q, c0, c1, r)
L4      if zlo ≠ none and zlo < H[i][j] then
L5          H[i][j] ← max(zlo, z_bottom)

LOWEST(q, c0, c1, r)                   ▷ lowest z of the swept tool on the line at q
L6  a ← c0.xy − q;  b ← c1.xy − c0.xy;  s ← c1.z − c0.z
L7  A ← a·a;  k ← a·b;  B ← b·b;  R ← r² − A
L8  if B = 0 then                                   ▷ a vertical move, or no move
L9      if R < 0 then return none
L10     t ← 0 if s ≥ 0 else 1;  return c0.z + t s − √R
L11 D ← k² + B R
L12 if D < 0 then return none                       ▷ the line misses the cylinder
L13 lo ← max(0, (−k − √D)/B);  hi ← min(1, (−k + √D)/B)
L14 if lo > hi then return none                     ▷ the line misses the end balls too
L15 t* ← (−k − s √(D/(B + s²)))/B                   ▷ the zero of f'
L16 t ← min(max(t*, lo), hi)
L17 return c0.z + t s − √(r² − |a + t b|²)
```

Line L1 limits the work to the grid points that the tool can reach. Lines L6 and L7 write the squared horizontal distance as $g(t) = A + 2kt + Bt^2$. Lines L11 to L14 find the interval of $t$ where $g(t) \le r^2$, the times at which the tool is over $q$. Line L15 is the zero of the derivative of $f$, which lies inside that interval. Since $f$ is convex, line L16 clamps it to $[0, 1]$, and line L17 evaluates $f$ there.

**Numbers.** The heights are measured quantities, so the code uses floating point. The only branches on float values are at lines L9, L12 and L14. They decide whether the tool touches the column at all, and a wrong answer there happens only when the tool is tangent to the line, where the lowest point is the equator of the ball at the height of the center. So a rounding error changes a height by a rounding error, not more. The tests compare each height with an exact rational test of membership in the swept volume, one part in $10^9$ above and below it.

## Example

Take a ball-end mill of radius $r = 2$, a grid with $h = 1$, a block with top $3$ and bottom $-2$, and one move of the ball center from $c_0 = (1, 1, 3)$ to $c_1 = (5, 1, 1)$. The tool goes down a slope of $m = -1/2$. Along the row $y = 1$, the path is right above the grid points.

| column $q$ | case | $z_{lo}$ | new $H$ |
|---|---|---|---|
| $(0, 1)$ | behind the start: $t = 0$, $d = 1$ | $3 - \sqrt 3 \approx 1.268$ | $1.268$ |
| $(1, 1)$ | on the cylinder: axis height $3$ | $3 - \sqrt 5 \approx 0.764$ | $0.764$ |
| $(2, 1)$ | axis height $2.5$ | $2.5 - \sqrt 5 \approx 0.264$ | $0.264$ |
| $(3, 1)$ | axis height $2$ | $2 - \sqrt 5 \approx -0.236$ | $-0.236$ |
| $(4, 1)$ | axis height $1.5$ | $1.5 - \sqrt 5 \approx -0.736$ | $-0.736$ |
| $(5, 1)$ | the end ball, $t = 1$, $d = 0$ | $1 - 2 = -1$ | $-1$ |
| $(6, 1)$ | after the end, $t = 1$, $d = 1$ | $1 - \sqrt 3 \approx -0.732$ | $-0.732$ |
| $(7, 1)$ | $d = 2$: the equator of the end ball | $1$ | $1$ |
| $(3, 3)$ | $d = 2$ from the path line | $2$ | $2$ |
| $(3, 3.5)$ | not on the grid, but $d > r$ there | none | unchanged |

On the cylinder part, the cut is $r\sqrt{1 + m^2} = \sqrt 5 \approx 2.236$ below the axis, not $r = 2$. A tilted cylinder of radius $r$ meets a vertical line in a longer chord than a vertical one. At $(5, 1)$ the cylinder would reach $1 - \sqrt 5$, but the move ends there, and the end ball reaches only $-1$. The column at $(1, 1)$ is cut to $0.764$, below the bottom of the ball when its center was over that column, which is $1$. The lowest point comes later, when the ball is past $q$ and lower.

## Correctness

On a vertical line, a ball position at horizontal distance $d \le r$ meets the line in a segment, and the shank above it covers the rest of the line upward. So each position removes a ray $[f(t), \infty)$, and the move removes the union of these rays, which is the ray from $\min f$. The distance $d(t)^2$ is a convex quadratic, so the set of $t$ where the tool is over the line is an interval. On it $f$ is convex as a linear term plus a convex nondecreasing function of a convex function. Writing $u = k + tB$ gives $r^2 - g(t) = (D - u^2)/B$ with $D = k^2 + BR$. This gives the interval of line L13, and shows that the derivative of $f$ is zero at $t^*$ of line L15. A convex function is smallest at the point of the interval nearest to its stationary point, which is line L16. Grid points outside the box of line L1 are more than $r$ from the path in $x$ or $y$, so the tool misses them. The full proof is in proofs/correctness.md.

## Complexity

A move whose ball centers span $L_x$ by $L_y$ in plan touches $c = (\lfloor (L_x + 2r)/h \rfloor + 1)(\lfloor (L_y + 2r)/h \rfloor + 1)$ grid points, and LOWEST takes $O(1)$ time on each, so a move costs $O(c)$. A toolpath with $m$ moves costs $O(\sum c)$. For a diagonal move the box holds many columns that the tool does not touch. A walk over the band of width $2r$ around the path, row by row, cuts this to the columns within $r$ of the path. A height query is $O(1)$, and the model takes $N$ numbers of space. The error does not depend on the toolpath: between grid points the model knows nothing, so a feature narrower than $h$ can be missed, and halving $h$ multiplies $N$ and the cost of every cut by 4. Drysdale, Jerard, Schaudt and Hauck (1989) analyse how the grid spacing bounds the size of the errors that a point sample simulation can find.

## Variants

- **Other tools.** A flat-end mill of radius $r$ sweeps a different volume. On a line at horizontal distance $d(t) \le r$ from the axis, the lowest point is the tip height $c_z(t)$. A bull-nose (toroidal) mill gives a quartic, and many codes then sample the move at small steps and take the minimum of exact single-position heights.
- **Error maps.** Store, beside each height, the height of the design surface on the same line. The difference is the stock left. A negative difference is a gouge, and a large positive one is missed material. See [gouge detection](/gouge-detection/).
- **Extended z-map.** Some systems store more than one sample per cell, for example points on the cell edges, so that steep walls are drawn better. The model still has one interval per line.
- **Normal vectors.** Jerard and coauthors (1989) cut short vectors that stand on the design surface along its normals, instead of vertical lines. This handles steep walls, which a z-map samples badly, but it needs the design surface in advance.
- **Dexels.** Keep a sorted list of intervals per line, not one height. The cut becomes an interval subtraction, and undercuts are allowed. See [dexel representation](/dexel-representation/).
- **Voxels.** A 3D grid of cells is the [spatial occupancy enumeration](/spatial-occupancy-enumeration/) of the stock. It allows any shape, at a cost of $n^3$ cells in place of $n^2$ heights.

## When to use it

Use a z-map for 3-axis milling with a tool along $z$, for roughing and finishing of dies, molds and other parts that are a function of $(x, y)$. It is fast, easy to draw as a height field, and easy to compare with the design surface. Do not use it for 5-axis machining, for turning, for parts with undercuts, or when the tool can come in from the side. Do not use it when the walls are steep and their position matters, because the grid samples a vertical wall at only one column.

## Pitfalls

- **Ball bottom under the center.** Lowering each column to $c_z - r$ when the center passes over it is wrong for a tilted move. In the example it gives $0$ at $(3, 1)$, but the true value is $2 - \sqrt 5$. Use the lowest point over the whole move.
- **Sampling the move.** Cutting only at the ball positions at fixed steps along a move misses the material between them, so the simulation shows ridges that the real tool removes.
- **No shank.** A tool model with only the ball can leave material above the ball inside the cut. Real tools have a shank. In a z-map, model it, or the columns become two intervals that the model cannot hold.
- **Grid aliasing.** A slot narrower than $h$ can fall between columns. Choose $h$ from the smallest feature to find, not from the screen.
- **Tolerances.** A height that is lower than the design height by a rounding error is not a gouge. Compare with a tolerance stated in the units of the part.
- **Undercuts.** A z-map cannot show them. A part that has them looks solid in the simulation.

## Implementations

## History

Anderson (1978) modelled the stock and the tool as heights over a grid to find collisions in NC programs, and later work on NC verification refers to this grid of heights as the z-map. In the 1980s the same idea served for fast shaded displays of milling, close to the z-buffer of graphics. In 1986 van Hook stored lists of depth intervals per pixel, the dexels, which allow more than one interval per line. Jerard, Drysdale, Hauck, Schaudt and Magewick (1989) compared height grids with vectors along the surface normals, and Drysdale, Jerard, Schaudt and Hauck (1989) analysed the cost and the accuracy of such discrete simulation. Choi and Jerard (1998) present the z-map as the standard model for 3-axis NC verification.

## References
