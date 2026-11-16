---
tag: MJFAZ4
kind: data-structure
slug: occupancy-grid-map
name: Occupancy grid map
aliases:
- occupancy grid
- evidence grid
area: robotics/localization-and-slam
level: intro
summary: A grid of cells, each holding the probability that the cell is occupied, assumed independent of the others.
model: word-ram
complexity:
  vars: {g: the number of cells, L: the length of a ray in meters, s: the side of a cell in meters}
  time: {index: O(1), update: O(1), probability: O(1), cells_on_segment: O(1 + L / s), insert_ray: O(1 + L / s)}
  space: {total: O(g)}
history:
  year: 1985
  people: [Hans Moravec, Alberto Elfes]
  note: Moravec and Elfes stored the evidence of many sonar readings in a grid of occupancy probabilities, and Elfes described the grid as a random field of cell states in 1989.
prereqs: [array, bayes-theorem]
see_also: [occupancy-grid-mapping, inverse-sensor-model, octree-occupancy-map, spatial-occupancy-enumeration, uniform-grid, amanatides-woo-traversal, topological-map, likelihood-field-model]
sources:
  - book: isbn:9780262201629
    title: "Sebastian Thrun, Wolfram Burgard and Dieter Fox, Probabilistic Robotics, MIT Press, 2005"
    locator: "Chapter 9, Section 9.2 (the grid of binary cells, the factorization of the map posterior over cells and the log odds form), and Chapter 4, Section 4.2 (the binary Bayes filter with static state)"
  - paper: doi:10.1109/ROBOT.1985.1087316
    title: "Hans P. Moravec and Alberto Elfes, High resolution maps from wide angle sonar, Proceedings of the 1985 IEEE International Conference on Robotics and Automation, volume 2, pages 116 to 121"
    locator: the grid of cells that holds the evidence of sonar readings for empty and occupied space
  - paper: doi:10.1109/2.30720
    title: "Alberto Elfes, Using occupancy grids for mobile robot perception and navigation, Computer 22(6), 1989, pages 46 to 57"
    locator: the occupancy grid as a multidimensional random field of cell states with stochastic estimates
  - paper: "John Amanatides and Andrew Woo, A fast voxel traversal algorithm for ray tracing, Eurographics 1987"
    locator: the traversal of the cells that a ray crosses, with the next crossing parameters tMaxX and tMaxY and the steps tDeltaX and tDeltaY
---

An occupancy grid map divides a bounded part of the plane into square cells of one size, and stores for each cell the probability that an obstacle occupies it. The robotics literature stores the log odds $l = \log(p / (1 - p))$ instead of $p$, because the Bayes update of one cell is then a sum. The cells are treated as independent random variables: the map is the product of $g$ separate binary distributions, which is an approximation that makes the update and the storage linear in $g$. This page describes the grid itself, its fields and its operations: cell lookup, the log odds update with optional clamping, and the traversal of the cells that a sensor beam crosses. The algorithm that fills the grid from scans is [occupancy grid mapping](/occupancy-grid-mapping/), and the model that turns one reading into cell values is the [inverse sensor model](/inverse-sensor-model/). In computer-aided design the same grid of cells, with a yes or no value per cell, is called [spatial occupancy enumeration](/spatial-occupancy-enumeration/).

## In plain words

Lay a sheet of squared paper over the floor plan of a building. In each square, write a number that says how sure you are that something stands there: a wall, a box, a table leg. At the start every square says "I do not know". A robot with a laser walks around. When a beam passes through a square, the square becomes a little more sure that it is empty. When a beam stops in a square, that square becomes a little more sure that it holds something. Each square keeps its own number and does not look at its neighbors. To find the square under a point, you divide the position by the size of a square. To find the squares a beam passes through, you walk from square to square along the beam, always to the next square that the beam enters.

## The abstract type

The grid is a map from the cells of a bounded rectangle to probabilities, with these operations:

- `index(x, y)`: the cell that holds the point $(x, y)$, or none outside the grid.
- `update(i, j, l_meas)`: combine the evidence $l_{\mathrm{meas}}$ of one reading with the value of cell $(i, j)$ by the binary Bayes rule in log odds.
- `probability(i, j)`: the occupancy probability of the cell.
- `cells_on_segment(a, b)`: the cells that the segment from $a$ to $b$ crosses, in order.
- `insert_ray(a, b, hit)`: update the cells of one beam from the sensor at $a$ to the end point $b$.

It is a [uniform grid](/uniform-grid/) over the plane with one number per cell, stored in an [array](/array/).

## Representation

- The origin $(o_x, o_y)$ in meters, the cell side $s$ in meters, and the size $W \times H$ in cells, so $g = W H$.
- Cell $(i, j)$ is the half-open square $[o_x + i s, o_x + (i + 1) s) \times [o_y + j s, o_y + (j + 1) s)$. Its center is $(o_x + (i + \tfrac12) s, o_y + (j + \tfrac12) s)$.
- One flat array $l$ of $g$ log odds values, in row-major order: cell $(i, j)$ is at index $j W + i$.
- The prior log odds $l_0 = \log(p_0 / (1 - p_0))$, where $p_0$ is the prior occupancy probability of every cell, often $0.5$, so $l_0 = 0$.
- Optional clamping bounds $l_{\min} \le l_0 \le l_{\max}$.

**Invariant (G).** (1) The array has exactly $W H$ entries. (2) Each entry is in $[l_{\min}, l_{\max}]$. (3) The entry of cell $(i, j)$ is the result of applying, in order, the clamped updates of that cell to $l_0$; without clamping, it is $l_0 + \sum_k (l_k - l_0)$ over the updates $l_k$ of that cell.

Part 3 says that the cells do not interact: an update of one cell never changes another one. A cell whose value is still exactly $l_0$ has never received evidence, or has received evidence that cancels out. Programs that need to tell "unknown" from "seen" keep a separate flag or count per cell.

## Operations

```pseudo id=main
INDEX(G, x, y)                         ▷ the cell that holds (x, y), or none
L1  i ← floor((x - o_x) / s);  j ← floor((y - o_y) / s)
L2  if 0 ≤ i < W and 0 ≤ j < H then return (i, j) else return none

UPDATE(G, i, j, l_meas)                ▷ binary Bayes rule in log odds
L3  k ← j W + i
L4  G.l[k] ← min(l_max, max(l_min, G.l[k] + l_meas - l_0))

PROBABILITY(G, i, j)
L5  return 1 - 1 / (1 + exp(G.l[j W + i]))
```

Line L4 is the log odds form of the binary Bayes filter with a static state: the evidence $l_{\mathrm{meas}}$ is the log odds of $p(m_i \mid z_t, x_t)$ from the inverse sensor model, and the prior is subtracted once per update so that it is counted only once in total. Line L5 is the logistic function; the implementation computes it in a form that cannot overflow.

```pseudo id=ray
CELLS-ON-SEGMENT(G, a, b)              ▷ Amanatides-Woo traversal on the infinite lattice
L6  (i, j) ← the cell of a;  (i_b, j_b) ← the cell of b;  d ← b - a
L7  t_x ← the t in [0, 1] where a + t d meets the next vertical cell edge; Δt_x ← s / |d_x|; the same for y
L8  output (i, j)
L9  repeat |i_b - i| + |j_b - j| times:
L10     if j = j_b or (i ≠ i_b and t_x < t_y) then i ← i + sign(d_x); t_x ← t_x + Δt_x
L11     else j ← j + sign(d_y); t_y ← t_y + Δt_y
L12     output (i, j)

INSERT-RAY(G, a, b, hit)
L13 for each cell c of CELLS-ON-SEGMENT(G, a, b) except the last, inside the grid: UPDATE(G, c, l_free)
L14 if the last cell is inside the grid: UPDATE(G, last, l_occ if hit else l_free)
```

The traversal keeps $t_x$ and $t_y$, the parameters of the next crossings of a vertical and a horizontal cell edge, and always crosses the nearer one. A coordinate with $d_x = 0$ has $t_x = \infty$. The segment crosses exactly $|i_b - i_a|$ vertical edges and $|j_b - j_a|$ horizontal ones, so line L9 runs a fixed number of steps; the tests $j = j_b$ and $i \ne i_b$ of line L10 make the last cell the cell of $b$ even when rounding makes $t_x$ and $t_y$ slightly wrong. When the segment passes exactly through a corner of four cells, the traversal steps in $y$ first and outputs one cell that the segment touches only at the corner.

Line L14 uses $l_{\mathrm{free}}$ for a max range reading: the beam passed through the last cell and hit nothing. The implementation uses $l_{\mathrm{occ}} = \log(0.7/0.3) = 0.84730$ and $l_{\mathrm{free}} = \log(0.4/0.6) = -0.40547$ by default. These are rules of thumb, not values derived from a sensor.

## Example

A grid of $5 \times 3$ cells of side $s = 1$ m with its origin at $(0, 0)$ and the prior $p_0 = 0.5$. The sensor is at $a = (0.5, 0.5)$, the center of cell $(0, 0)$.

The segment to $b = (3.7, 2.4)$ has $d = (3.2, 1.9)$. It crosses $x = 1$ at $t = 0.5/3.2 = 0.156$, $y = 1$ at $t = 0.5/1.9 = 0.263$, $x = 2$ at $t = 0.469$, $x = 3$ at $t = 0.781$ and $y = 2$ at $t = 0.789$. So CELLS-ON-SEGMENT returns $(0,0), (1,0), (1,1), (2,1), (3,1), (3,2)$: five steps, since $|3 - 0| + |2 - 0| = 5$.

Now insert three rays, all with a hit: first to $(3.7, 2.4)$, then to $(4.5, 0.5)$ along row 0, then to $(3.7, 2.4)$ again. The log odds, with the probability below each value, are then:

| row | $i = 0$ | $i = 1$ | $i = 2$ | $i = 3$ | $i = 4$ |
|---|---|---|---|---|---|
| $j = 2$ | 0 | 0 | 0 | 1.69460 | 0 |
| | 0.5 | 0.5 | 0.5 | 0.8448 | 0.5 |
| $j = 1$ | 0 | -0.81093 | -0.81093 | -0.81093 | 0 |
| | 0.5 | 0.3077 | 0.3077 | 0.3077 | 0.5 |
| $j = 0$ | -1.21640 | -1.21640 | -0.40547 | -0.40547 | 0.84730 |
| | 0.2286 | 0.2286 | 0.4 | 0.4 | 0.7 |

Cell $(3, 2)$ got two hits, $2 \cdot 0.84730 = 1.69460$, which is $0.49/(0.49 + 0.09) = 0.8448$. Cells $(0, 0)$ and $(1, 0)$ are on all three rays, so they have three misses, $(0.4/0.6)^3 = 8/27$ in odds, or $8/35 = 0.2286$. The cells with the value 0 are on no ray and keep the prior.

**Clamping.** With $p_{\min} = 0.12$ and $p_{\max} = 0.97$, the bounds are $l_{\min} = -1.992$ and $l_{\max} = 3.476$. Five hits and then one miss give $\min(3.476, 4.236) - 0.405 = 3.071$. One miss and then five hits give $-0.405 + 4.236 = 3.831$, clamped to $3.476$. With clamping, the order of the updates matters.

## Correctness

Each operation keeps the invariant (G). INDEX returns the cell whose half-open square holds the point, because the floor of $(x - o_x)/s$ is the only integer $i$ with $o_x + i s \le x < o_x + (i + 1) s$. UPDATE changes only the entry of its own cell, and the clamp of line L4 keeps it in the bounds, so parts 2 and 3 hold. Without clamping, line L4 is the log odds form of Bayes' rule for one binary cell, and the value after the updates is the posterior log odds of the cell under the assumption that the readings are independent given the cell; [occupancy grid mapping](/occupancy-grid-mapping/) proves this. CELLS-ON-SEGMENT returns, for a segment that passes through no corner of a cell, exactly the cells whose open square meets the segment, in the order of the segment, each once. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The model is the [word RAM](/word-ram/), with one step for each arithmetic operation on a floating-point log odds value held in one word, and for the floor, exp and comparison of line L1, L5 and L10.

| operation | time | case |
|---|---|---|
| index | $O(1)$ | worst |
| update | $O(1)$ | worst |
| probability | $O(1)$ | worst |
| cells_on_segment | $O(1 + L / s)$ | worst |
| insert_ray | $O(1 + L / s)$ | worst |
| space | $O(g)$ | total |

A segment of length $L$ crosses at most $|d_x| / s + 1$ vertical and $|d_y| / s + 1$ horizontal edges, and $|d_x| + |d_y| \le \sqrt 2\, L$, so it visits $O(1 + L / s)$ cells.

The space is the real cost. A floor of 100 m by 100 m at $s = 0.05$ m has $2000 \times 2000 = 4 \cdot 10^6$ cells, which is 16 MB with 4-byte floats. A volume of 100 m by 100 m by 10 m at the same resolution has $8 \cdot 10^8$ cells, which is 3.2 GB, mostly free or unknown space. That is why 3D maps use an [octree occupancy map](/octree-occupancy-map/).

## Variants

- **Bytes instead of floats.** Store each cell as a small integer. The ROS message `nav_msgs/OccupancyGrid` stores one signed byte per cell, a probability in percent from 0 to 100, or $-1$ for unknown, in row-major order.
- **Clamping.** Bounds on the log odds keep the map able to change when the world changes, and make a fully certain cell recognizable. The OctoMap software uses this in 3D.
- **Growing grids.** Store the grid in fixed-size tiles in a hash table, keyed by the tile index, and create a tile when a ray first reaches it. The robot can then explore without a size known in advance.
- **Multi-resolution grids.** A [quadtree](/quadtree/) in 2D or the [octree occupancy map](/octree-occupancy-map/) in 3D merges large regions with the same value.
- **Other cell contents.** A cell can hold counts of hits and misses, a height (an elevation map), or the distance to the nearest occupied cell (a [distance transform](/distance-transform/), used by the [likelihood field model](/likelihood-field-model/)).
- **Coverage maps.** Some variants store the fraction of a cell that is filled, a value between 0 and 1, instead of the probability of a binary state. This handles cells that are half wall and half free space.

## When to use it

Use an occupancy grid map for a 2D map of a building or a site for a ground robot. It gives constant time lookups for planning and for sensor models, a simple update from range sensors, and an explicit notion of free and unknown space, which [frontier-based exploration](/frontier-based-exploration/) needs. It handles any shape of obstacle at the chosen resolution. Use an octree in 3D or for large mostly empty volumes, a feature map with landmarks when the world has few distinct objects, and a [topological map](/topological-map/) when only the connections between places matter.

## Pitfalls

- **Treating the cells as independent.** The map is a product of independent cells. Two cells of one wall, or the cells behind a door, are clearly dependent. The probabilities in the grid are therefore too confident, and the grid is not a sample from any real map distribution.
- **Resolution.** A thin obstacle such as a table leg can fall between two beams or occupy only part of a cell, and a cell that is half wall and half free space has no correct binary value. Halving $s$ multiplies the memory by 4 in 2D and by 8 in 3D.
- **Row-major against column-major.** Image libraries, ROS messages and textbooks differ in the order of $(i, j)$ and in where the origin is. A wrong order mirrors the map along a diagonal; check with an asymmetric test map.
- **Points on cell edges.** Use half-open cells and floor, not rounding, in INDEX. With `int()` instead of floor, negative coordinates are rounded towards zero, and the cells $-1$ and $0$ are merged.
- **Unknown against probability 0.5.** A cell at exactly $l_0$ can be unknown or have balanced evidence. Planners that treat unknown cells as free need a separate flag.
- **Clamping changes the result.** With clamping, the order of updates matters, as the example shows. Tests that compare a clamped map with a closed-form sum must take this into account.

## Implementations

## History

Moravec and Elfes (1985) used a grid of cells to combine many wide angle sonar readings on the robots of the Carnegie Mellon Mobile Robot Laboratory. Each reading made the cells of its cone more likely to be empty and the cells near its arc more likely to be occupied. Elfes (1989) described the occupancy grid as a random field of cell states with stochastic estimates, updated by Bayes' rule, and used it for path planning and navigation. Thrun, Burgard and Fox (2005) present the log odds form and the binary Bayes filter per cell that most software uses today. The traversal of cells along a beam is the voxel traversal of Amanatides and Woo (1987), first written for ray tracing.

## References
