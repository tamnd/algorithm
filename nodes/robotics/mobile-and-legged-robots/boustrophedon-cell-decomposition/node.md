---
tag: E8C6B2
kind: algorithm
slug: boustrophedon-cell-decomposition
name: Boustrophedon cell decomposition
aliases:
- boustrophedon coverage
area: robotics/mobile-and-legged-robots
level: core
summary: Splits free space into cells at critical points of a sweep line and covers each cell by back and forth lanes.
model: real-ram
complexity:
  vars: {n: "the number of obstacle vertices", m: "the number of lanes"}
  time: {worst: O(n log^2 n + m log n)}
  space: {extra: O(n + m)}
properties: {deterministic: true, randomized: false, online: false, exact: true}
history:
  year: 1998
  people: [Howie Choset, Philippe Pignon]
  note: "Choset and Pignon merged the cells of the trapezoidal decomposition that a back and forth motion can cover in one pass, so that cells change only where the connectivity of the sweep line changes."
prereqs: [cell-decomposition, sweep-line-technique]
see_also: [coverage-path-planning, trapezoidal-map, depth-first-search, frontier-based-exploration, shoelace-formula, convex-decomposition, traveling-salesman-problem, watchman-route-problem]
sources:
  - paper: doi:10.1007/978-1-4471-1273-0_32
    title: "Coverage path planning: the boustrophedon cellular decomposition"
    locator: "Field and Service Robotics, edited by A. Zelinsky, Springer, 1998, pp. 203-209, the whole paper (the decomposition at the points where the slice changes connectivity, and the coverage of each cell by back and forth motion)"
  - paper: doi:10.1023/A:1008958800904
    title: "Coverage of known spaces: the boustrophedon cellular decomposition"
    locator: "Autonomous Robots 9(3), pp. 247-253, the whole paper"
  - paper: doi:10.1016/j.robot.2013.09.004
    title: A survey on coverage path planning for robotics
    locator: "Robotics and Autonomous Systems 61(12), pp. 1258-1276, the part on exact cellular decompositions"
---

The boustrophedon cell decomposition splits the free part of a known planar region into cells that a robot can cover with simple back and forth lanes, like an ox plowing a field (the Greek word means "as the ox turns"). A vertical line sweeps across the region. At each position, the free part of the line is a set of intervals. The number of intervals changes only at a few critical points: where an obstacle begins, one interval splits into two, and where an obstacle ends, two intervals merge into one. Each interval traces a cell between two critical points. Inside a cell, the robot moves up and down along lanes spaced by its tool width; the cells are then visited one by one along their adjacency graph. Howie Choset and Philippe Pignon introduced it for [coverage path planning](/coverage-path-planning/) as a coarser version of the [trapezoidal decomposition](/trapezoidal-map/): it cuts only where the connectivity of the sweep line changes, not at every vertex, so it has fewer cells and fewer turns.

## In plain words

Think of mowing a lawn that has some flower beds in it. The easiest way to mow is in long straight strips, up and down, moving over by one mower width each time. That works until a flower bed splits a strip in two. So you divide the lawn into pieces where this happens: one piece before the flower bed, one piece above it, one piece below it, and one piece after it. Each piece can be mowed in plain strips with no surprises.

The method finds those pieces by sliding a line across the lawn and watching where it gets split or joined. Then it mows the pieces one after another.

## The problem

**Input.** A rectangle $[0, W] \times [0, H]$ and $k$ disjoint convex polygons inside it, with $n$ vertices in total, given with exact rational coordinates; and a tool width $w > 0$. In general position: each polygon has one leftmost and one rightmost vertex, and no two of these share an $x$. Arithmetic on the coordinates costs one step, as in the [real RAM](/real-ram/).

**Output.** A set of cells whose interiors are disjoint and whose union is the free space; the adjacency graph of the cells; and a coverage path made of vertical lane segments, such that every free point is at horizontal distance at most $w/2$ from a lane of its own cell.

**How it differs from close pages.** The [trapezoidal decomposition](/trapezoidal-map/) cuts at every vertex, which gives trapezoids for point location and [cell decomposition](/cell-decomposition/) planners; the boustrophedon decomposition merges trapezoids into cells that one back and forth pattern covers. [Convex decomposition](/convex-decomposition/) also splits a region, but into convex pieces, and has no notion of a sweep. [Frontier-based exploration](/frontier-based-exploration/) works on an unknown map; this method needs the whole map in advance.

## The algorithm

```pseudo id=main
BOUSTROPHEDON(W, H, obstacles, w)
L1  events ← the leftmost and the rightmost vertex of each obstacle, sorted by x
L2  open one cell for the whole slice at x = 0;  active ← no obstacles
L3  for each event (x, o):
L4      if x is the leftmost vertex of o: close the cell that contains the vertex; open a cell below o and a cell above o; link both to the closed cell; insert o into active
L5      else: close the cells just below and just above o; open one cell that spans both; link it to both; remove o from active
L6  close every open cell at x = W
L7  order ← the cells in depth-first order of the adjacency graph, from the first cell
L8  in each cell of order: cover it with ⌈(x1 - x0)/w⌉ evenly spaced vertical lanes, alternately up and down
```

The [sweep line](/sweep-line-technique/) keeps the active obstacles in their order from bottom to top; disjoint convex obstacles never cross, so this order changes only at events. The gap between two consecutive active obstacles, or between an obstacle and the bottom or top of the rectangle, is one open cell. Line L4 finds the gap that contains the new vertex by comparing it with the active obstacles at that $x$. A cell's walls may bend at vertices of the obstacles between its two events; the cell does not split there, because the slice stays one interval. That is the difference from the trapezoidal decomposition.

Line L8 uses $\lceil(x_1 - x_0)/w\rceil$ lanes at the centers of equal strips, so each lane is at most $w$ from the next and the end lanes are at most $w/2$ from the ends of the cell. Each lane runs from the lower wall to the upper wall of the cell at its $x$.

## Example

The region is $10 \times 6$, with a diamond obstacle with vertices $(3, 3)$, $(5, 1)$, $(7, 3)$ and $(5, 5)$. The events are the IN event at $x = 3$ and the OUT event at $x = 7$.

| Cell | $x$ range | Lower wall | Upper wall | Area | Lanes for $w = 1$ |
|---|---|---|---|---|---|
| 0 | 0 to 3 | bottom | top | 18 | 3 |
| 1 | 3 to 7 | bottom | diamond, lower edges | 8 | 4 |
| 2 | 3 to 7 | diamond, upper edges | top | 8 | 4 |
| 3 | 7 to 10 | bottom | top | 18 | 3 |

The areas add up to $60 - 8 = 52$, the area of the free space. The vertex $(5, 1)$ bends the upper wall of cell 1, but the slice stays one interval, so cell 1 is not cut there. A trapezoidal decomposition would cut at $x = 5$ too and give 6 cells. The adjacency graph is a 4-cycle: 0 is linked to 1 and 2, and both are linked to 3. Depth-first order from cell 0 is 0, 1, 3, 2: the robot covers the left part, the part below the diamond, the right part, and then the part above, which it reaches from cell 3. The lanes of cell 1 are at $x = 3.5, 4.5, 5.5, 6.5$, from $y = 0$ up to $2.5, 1.5, 1.5, 2.5$.

## Correctness

The [proof](proofs/correctness/) shows that the cells partition the free space, that each cell is bounded by two walls that do not cross, that the adjacency graph is connected, and that $k$ obstacles in general position give exactly $1 + 3k$ cells: each IN event closes one cell and opens two, and each OUT event closes two and opens one. It also shows that every free point is within horizontal distance $w/2$ of a lane of its cell. The tests check the partition on random points of random scenes in exact rational arithmetic, the total area against the [shoelace formula](/shoelace-formula/), the cell count, that linked cells share a boundary segment, and the spacing of the lanes.

## Complexity

- **Time.** Sorting the $2k$ events costs $O(k \log k)$. With the active obstacles in a balanced search tree, each event makes $O(\log k)$ comparisons, and each comparison evaluates a chain of an obstacle at $x$ by binary search in $O(\log n)$. The decomposition takes $O(n + k \log k \log n)$, which is $O(n \log^2 n)$, and each of the $m$ lanes needs two chain evaluations, $O(\log n)$ each. The code uses lists and linear scans instead, so it takes $O(kn + mn)$, which is enough for a few hundred vertices.
- **Space.** $O(n)$ for the obstacles, the cells and the graph, and $O(m)$ for the path.

## Properties

- **Complete coverage.** For a tool of width $w$ that moves along the lanes, every free point is within $w/2$ horizontally of a lane of its cell. Near a slanted wall, the tool may miss a thin sliver at the end of a lane, which practical planners cover by a pass along the wall.
- **Few cells.** $1 + 3k$ cells for $k$ convex obstacles, independent of the number of vertices. The trapezoidal decomposition has a cell count that grows with the number of vertices.
- **Exact.** With rational input, the decomposition, the areas and the lanes are exact.
- **Direction matters.** The number of turns, and so the time of the coverage, depends on the sweep direction. Turning the sweep to follow the longest dimension of the region usually reduces the turns.

## Variants and improvements

- **Morse decompositions.** Acar, Choset and others generalized the critical points to those of a Morse function: a circle that grows from a point gives spiral coverage, and other functions give other patterns.
- **Nonconvex obstacles.** A nonconvex obstacle has more IN and OUT events: every vertex where the slice splits or merges is critical, not only the leftmost and rightmost ones.
- **Online coverage.** The robot can detect the critical points with its sensors while it covers an unknown region, and build the adjacency graph as it goes.
- **Better cell order.** Ordering the cells is a kind of [traveling salesman problem](/traveling-salesman-problem/) on the adjacency graph; depth-first order is simple, but a tour that also chooses the start corner of each cell is shorter.

## When to use it

Use the boustrophedon decomposition when the map is known, the obstacles are polygons, and the robot covers with a tool of fixed width: floor cleaning, lawn mowing, painting, field work and seabed or aerial surveys. When the map is a grid, a grid-based method or a spanning-tree coverage is often simpler. When the map is unknown, use an online coverage method, or explore first.

## Pitfalls

- **Degenerate input.** Vertical edges at the leftmost or rightmost point, or two events at the same $x$, need extra care: merge the events, or perturb the input.
- **Lane ends near slanted walls.** A lane that ends where the wall is steep leaves a thin wedge uncovered next to the wall. Add a pass along the boundary.
- **Too narrow cells.** A cell narrower than the tool still gets one lane; the tool may not fit. Inflate the obstacles by half the tool width first, as in the [configuration space](/configuration-space/).
- **Travel between cells.** Depth-first order can send the robot back through covered cells. Count that travel in the path length.

## Implementations

## History

The trapezoidal decomposition, used in motion planning since the 1980s, cuts the free space at every vertex. Choset and Pignon presented the boustrophedon cellular decomposition at the Field and Service Robotics conference in 1997, published in 1998: cut only at the critical points where the sweep line's free part splits or merges, and cover each cell by back and forth motion. Choset described it again in Autonomous Robots in 2000. Later work generalized the critical points through Morse functions, and the survey of Galceran and Carreras lists it among the main exact cellular decompositions for coverage.

## References
