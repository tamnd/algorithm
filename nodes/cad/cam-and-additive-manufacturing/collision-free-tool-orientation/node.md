---
tag: E9RNYT
kind: algorithm
slug: collision-free-tool-orientation
name: Collision-free tool orientation in C-space
aliases:
- tool orientation C-space
area: cad/cam-and-additive-manufacturing
level: research
summary: Maps the tool, holder and machine obstacles into the space of tool axis angles at each contact point and picks a smooth path of feasible axes, after Morishige and coauthors.
solves: [five-axis-tool-orientation]
model: real-ram
complexity:
  vars: {m: number of tool positions, k: number of candidate directions per position, n: number of obstacle boxes}
  time: {worst: "O(m k n + m k^2)"}
  space: {extra: "O(m k)"}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1997
  people: [Koichi Morishige, Kiwamu Kase, Y. Takeuchi]
  note: Morishige, Kase and Takeuchi mapped the collisions of a five-axis tool into a two-dimensional C-space of tool directions at each point and chose collision-free directions there.
prereqs: [five-axis-tool-orientation, configuration-space, accessibility-cone]
see_also: [ray-casting, line-clipping, viterbi-algorithm, collision-detection, motion-planning, gouge-detection, principal-axis-method, swept-volume]
sources:
  - paper: "Koichi Morishige, Kiwamu Kase and Y. Takeuchi, Collision-free tool path generation using 2-dimensional C-space for 5-axis control machining, The International Journal of Advanced Manufacturing Technology 13(6), 393-400, 1997"
    locator: the two-dimensional C-space of tool directions at a contact point and the choice of collision-free directions in it
  - paper: "Cha-Soo Jun, Kyungduck Cha and Yuan-Shin Lee, Optimizing tool orientations for 5-axis machining by configuration-space search method, Computer-Aided Design 35(6), 549-566, 2003"
    locator: the feasible region of tool orientations in the space of two angles and the smoothing of the orientations along the path in both directions
  - paper: doi:10.1109/TC.1983.1676196
    title: Tomás Lozano-Pérez, Spatial planning, a configuration space approach, IEEE Transactions on Computers C-32(2), 108-120, 1983
    locator: the configuration space and the images of obstacles in it
  - paper: doi:10.1145/357332.357333
    title: You-Dong Liang and Brian A. Barsky, A new concept and method for line clipping, ACM Transactions on Graphics 3(1), 1-22, 1984
    locator: the parametric clipping of a segment against a rectangle, used for the exact test of a direction against a box
---

Collision-free tool orientation in C-space chooses the tool axis at each point of a five-axis toolpath from a map of the directions that are free of collisions. At each tool position, every obstacle (a wall of the part, a clamp, a block of the fixture) is turned into a region of a plane whose points are tool directions, the C-space of orientations. A direction is free when it lies outside all the regions. The planner then picks one free direction per position so that the axis stays close to a preferred direction, such as the tilt of the [principal axis method](/principal-axis-method/), and changes little from one position to the next. This is the manufacturing side of mechanical CAD, about the motion of a cutter, not the placement and routing of a circuit. The version here models the tool as a half-line from the tool center and the obstacles as boxes. In the gnomonic chart of directions each box becomes an exact polygonal shadow, the test needs only rational arithmetic, and the smooth choice is a shortest path over the layers of free directions, solved exactly by dynamic programming.

## In plain words

Stand where the cutter is and look up. Some directions are open sky, and some are blocked by a wall, a post or a clamp. Draw a map of the sky with the blocked parts shaded. A tool that points into the open sky does not hit anything.

The cutter moves along a path, so you draw one such map at each stop and mark a few candidate directions in the open part. You want a good direction for cutting, but you also want the tool to swing little from stop to stop, because big swings are slow and rough.

So you pick one open direction on each map, and you score the whole choice by how far each pick is from the good direction and how far it moves between stops. The best choice is found by working through the stops one at a time.

## The problem

**Directions.** The tool is a half-line from the tool center $p$, the center of the ball of a ball end mill, in a direction $d$ above the horizon. Write $d = (q_x, q_y, 1)$, so the direction is a point $q$ of the plane. This is the gnomonic chart: $q = 0$ is the vertical axis, and the tilt from vertical is $\arctan|q|$. Lines through the center of the sphere of directions map to straight lines in this chart.

**Obstacles.** Closed boxes $[x_0, x_1] \times [y_0, y_1] \times [z_0, z_1]$. A box blocks $q$ at $p$ when the ray $p + t\, d$, $t > 0$, meets it. A tool of radius $r$ is handled by growing each box by $r$ on every side, which is safe but can reject a few free directions near the edges.

**Output.** Given tool centers $p_1, \dots, p_m$, a grid of candidate directions $q = h g$ with $g \in G \subset \mathbb{Z}^2$, preferred grid points $\pi_i$ and a weight $w$, choose free $g_1, \dots, g_m$ that minimize
$$
J = w \sum_i |g_i - \pi_i|^2 + \sum_{i \ge 2} |g_i - g_{i-1}|^2 .
$$

**The image of a box.** With $T_0 = \max(z_0 - p_z, 0)$, $T_1 = z_1 - p_z$ and the rectangle $\bar R = [x_0 - p_x, x_1 - p_x] \times [y_0 - p_y, y_1 - p_y]$, the box blocks $q$ exactly when $T_1 > 0$ and the segment from $T_0 q$ to $T_1 q$ meets $\bar R$. For a block that stands on the floor, $T_0 = 0$, and the blocked set is the shadow of the rectangle $\bar R / T_1$ seen from the origin: every $q$ whose segment from $0$ meets it.

## The algorithm

```pseudo id=main
PLAN-ORIENTATIONS(p[1..m], boxes, G, h, π[1..m], w)
L1  for i ← 1 to m do
L2      F_i ← {g ∈ G : for every box, the segment from T_0·hg to T_1·hg misses the rectangle}
L3      if F_i is empty then fail: no free direction at p_i
L4  C_1[g] ← w·|g − π_1|² for g ∈ F_1
L5  for i ← 2 to m do
L6      for g ∈ F_i: C_i[g] ← w·|g − π_i|² + min over g' ∈ F_{i−1} of (C_{i−1}[g'] + |g − g'|²); keep the best g' as back_i[g]
L7  g_m ← argmin C_m; g_{i−1} ← back_i[g_i] for i = m, …, 2
L8  return (min C_m, g_1, …, g_m)
```

Line L2 is the C-space map. The segment test is [line clipping](/line-clipping/) of a segment against a rectangle in parameter form, as Liang and Barsky do it, and with rational data it is exact, including directions that graze an edge or a corner. Lines L4 to L7 are a shortest path through the layers $F_1, \dots, F_m$, the same recurrence as the [Viterbi algorithm](/viterbi-algorithm/).

## Example

The tool center moves toward a wall, the box $[4, 5] \times [-10, 10] \times [0, 6]$, along $p_i = (i - 1, 0, 1)$ for $i = 1, \dots, 4$. The candidates are $q = (g/8, 0)$ for $g = -4, \dots, 4$, and the preferred direction is $g = 4$, a lead of $26.57°$ toward the wall.

For the wall, $T_0 = 0$ and $T_1 = 5$, so $q$ is blocked when $5 q_x \ge 4 - p_x$ (and $|5q_y| \le 10$).

| position $i$ | $p_x$ | blocked when $q_x \ge$ | largest free tilt | largest free $g$ |
|---|---|---|---|---|
| 1 | 0 | 0.8 | below $38.66°$ | 4 |
| 2 | 1 | 0.6 | below $30.96°$ | 4 |
| 3 | 2 | 0.4 | below $21.80°$ | 3 |
| 4 | 3 | 0.2 | below $11.31°$ | 1 |

With $w = 1$ the program returns $g = (4, 4, 3, 1)$ with $J = (0 + 0 + 1 + 9) + (0 + 1 + 4) = 15$: it follows the preference until the wall forces it back, then drops from $20.56°$ to $7.13°$ in one step. With $w = 1/4$ smoothness counts more, and it returns $(3, 3, 2, 1)$ with $J = 15/4 + 2 = 5.75$: the tool starts to stand up at once, and the largest step is one grid cell. Both answers equal a search over all $9^4$ choices.

At the exact grid point $q = (0.4, 0)$ at $p_3$, the ray goes through the top edge of the wall, $(4, 0, 6)$. The closed box counts this as a hit. A float test can decide such a case either way, and the exact test is the reason the code uses fractions.

## Correctness

**Theorem.** Line L2 marks a grid direction as free exactly when its ray from $p_i$ misses every box. If every $F_i$ is nonempty, the program returns the least $J$ over all choices of free grid directions and a choice that attains it. With boxes grown by $r$, every point of each chosen ray is more than $r$ from the original boxes.

The ray $p + t\,d$ is at height $p_z + t$, so it is in the slab of the box for $t \in [z_0 - p_z, z_1 - p_z]$, and for such $t$ it is in the box exactly when $t q \in \bar R$. The points $t q$ form the segment of line L2, and the end $t = 0$ does not matter because $p$ is outside the box. The program is optimal by the usual argument for layered shortest paths: the best choice that ends in $g$ at layer $i$ is a best choice ending at some $g'$ at layer $i - 1$, plus the step. The full proof is in the proof file.

What is exact is the test and the optimum over the grid for this cost. The model is not exact: a half-line or a grown box is not a full tool with its holder, and the grid can miss a narrow free gap. The tests compare line L2 with a direct slab test of the 3D ray against each box, in exact fractions, on random boxes and on directions aimed exactly at edges and corners, and compare the program with a search over all choices.

## Complexity

Building the free sets tests each of $k$ grid directions against each of $n$ boxes at each of $m$ positions, $O(mkn)$ time. Line L6 compares every pair of directions in neighboring layers, $O(mk^2)$ time, and the back pointers take $O(mk)$ space. A grid of $41 \times 41$ directions, 1000 positions and 50 boxes is about $8.4 \cdot 10^7$ box tests and $2.8 \cdot 10^9$ pair steps, so real systems restrict the steps to a window of nearby directions, which brings line L6 down to $O(mk\,s)$ for a window of $s$ cells, or rasterize the shadows of the boxes on the grid instead of testing every pair.

## Properties

- **Exact test.** The C-space image of a box is computed with rational arithmetic, with no tolerance.
- **Conservative for thick tools.** Growing the boxes by the tool radius never accepts a colliding direction.
- **Optimal on the grid.** The dynamic program finds the best choice for the stated cost.
- **Local in space.** Each position is tested on its own. Collisions of the tool while it moves between two positions are not tested.
- **Above the horizon.** The chart covers directions with a positive vertical part, which is the range of most five-axis machines.

## Variants and improvements

- **Angle charts.** Morishige, Kase and Takeuchi used two angles of the tool axis as the coordinates of the C-space. The gnomonic chart here makes box shadows polygons. Other obstacles, such as triangles of a mesh, also map to polygons in it.
- **Feasible regions and smoothing.** Jun, Cha and Lee (2003) built at each contact point a feasible region bounded by gouge and collision limits and smoothed the orientations by searching forward and backward along the path.
- **Full tool shapes.** A tool with a holder is a stack of cylinders and cones. Each part maps to its own C-space region, found by distance tests, by [ray casting](/ray-casting/) from many points of the tool, or on graphics hardware.
- **Machine axes.** The cost can be measured in the rotary angles of the machine instead of in the chart, which adds the kinematics and the pole singularity of the [orientation problem](/five-axis-tool-orientation/).
- **Accessibility maps.** Over a whole region, the intersection of the free sets is an [accessibility cone](/accessibility-cone/), used to choose fixed axes for 3+2 machining.

## When to use it

Use a C-space planner when a five-axis path runs close to walls, between blades of an impeller, or past clamps, and the tool must lean away from them. Use the [principal axis method](/principal-axis-method/) or another local method to get the preferred direction, and the C-space step to make it safe and smooth. On open parts with no nearby obstacles, a local method alone is enough.

## Pitfalls

- **Ray instead of tool.** A collision test of the axis line alone misses collisions of the body of the tool. Grow the obstacles by the radius, or test the full tool.
- **Float tests at edges.** A direction that grazes an edge or a corner of an obstacle is decided by the sign of a rounding error in float code. Use exact arithmetic, or a margin that is applied the same way everywhere.
- **Grid gaps.** A narrow free gap between two obstacles can fall between grid directions. A finer grid near the boundary of the free set helps.
- **Moves between positions.** Two free positions can be joined by a move that collides, when the tool swings through an obstacle. Check the [swept volume](/swept-volume/) of each move.
- **Gouges.** Collision-free is not gouge-free. A direction that misses all obstacles can still cut into the part near the contact point. Combine with [gouge detection](/gouge-detection/).
- **Too strong a preference.** With a large weight on the preferred direction, the path follows it until an obstacle forces a sudden turn, as in the example with $w = 1$.

## Implementations

## History

Lozano-Pérez (1983) introduced the configuration space for spatial planning, in which a moving object is a point and the obstacles grow into regions. Morishige, Kase and Takeuchi (1997) applied the idea to five-axis machining with a two-dimensional C-space of tool directions at each point of the path, and Morishige, Takeuchi and Kase (1999) extended it. Jun, Cha and Lee (2003) used feasible regions in a C-space of two angles together with gouge limits, and optimized and smoothed the orientation along the path. The exact shadow test and the layered dynamic program on this page are a compact form of the same scheme.

## References
