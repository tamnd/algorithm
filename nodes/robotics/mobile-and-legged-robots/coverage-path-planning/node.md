---
tag: A8C0KR
kind: problem
slug: coverage-path-planning
name: Coverage path planning
aliases:
- complete coverage path planning
area: robotics/mobile-and-legged-robots
level: core
summary: "Find a path that passes a tool over every point of a region, as for cleaning, mowing or demining."
prereqs: [motion-planning, configuration-space]
see_also: [boustrophedon-cell-decomposition, frontier-based-exploration, coverage-control, traveling-salesman-problem, art-gallery-problem, watchman-route-problem, pocket-machining, direction-parallel-toolpath]
sources:
  - paper: doi:10.1016/j.robot.2013.09.004
    title: "Enric Galceran and Marc Carreras, A survey on coverage path planning for robotics"
    locator: "Robotics and Autonomous Systems 61(12), pp. 1258-1276, the whole survey (the requirements of a coverage path and the classes of methods)"
  - paper: doi:10.1023/A:1016639210559
    title: "Howie Choset, Coverage for robotics: a survey of recent results"
    locator: "Annals of Mathematics and Artificial Intelligence 31, pp. 113-126, the whole survey (heuristic, approximate and exact cellular decomposition methods, offline and online)"
  - paper: doi:10.1016/S0925-7721(00)00015-8
    title: "Esther M. Arkin, Sándor P. Fekete and Joseph S. B. Mitchell, Approximation algorithms for lawn mowing and milling"
    locator: "Computational Geometry 17(1-2), pp. 25-50, the abstract (both problems are NP-hard; a (3 + ε)-approximation for lawn mowing and a 2.5-approximation for milling), Theorem 1 and its corollaries"
---

Coverage path planning asks for a path along which a tool of a given shape, such as a cleaning brush, a mower deck, a spray nozzle, a camera footprint or a milling cutter, passes over every point of a given region. The region is a part of the plane, or a surface, minus its obstacles. A path that covers everything always exists when the free region is connected and the tool fits through every passage; the hard part is to make it short, with few turns and little overlap, and to plan it when the map is not known in advance. The robotics form of the problem is the same as the tool path problem of pocket milling in manufacturing and the lawn mowing problem of computational geometry. In general it is NP-hard, so practical planners split the region into simple cells and cover each cell with back and forth lanes.

## In plain words

A cleaning robot must pass its brush over the whole floor of a room, around the furniture. It should not leave a strip uncleaned, it should not pass over the same place too often, and it should not waste time turning. Mowers, painting robots, mine detectors and survey drones have the same task with a different tool.

The question has two parts. First, which path passes over everything? Second, of those paths, which one is shortest or quickest? The first part is easy for most rooms. The second part is hard to answer exactly, so planners use simple patterns that are good, but not always the best.

## Definition

**Input.** A closed region $P$ in the plane (often a polygon with holes), a tool shape $T$ (a disc of diameter $w$, or an axis-aligned square of side $w$), and the allowed motions (any path, or only axis-parallel segments). In the robot form, $P$ is the free part of the [configuration space](/configuration-space/), so the obstacles are already grown by the robot's size.

**Output.** A path $\gamma : [0, 1] \to \mathbb{R}^2$ such that every point of $P$ lies in the tool placed at some point of the path:

$$P \subseteq \bigcup_{t \in [0, 1]} \bigl(\gamma(t) + T\bigr).$$

In the **milling** version, the tool must stay inside $P$, that is $\gamma(t) + T \subseteq P$ for all $t$. In the **lawn mowing** version, the tool may leave $P$. These names come from Arkin, Fekete and Mitchell.

**Objective.** Minimize the length of $\gamma$. Common other costs are the time, which counts turns because the robot slows down to turn, the number of turns, and the area covered more than once. A closed path (a tour) is often required, so that the robot returns to its dock.

## Variants

- **Offline and online.** In the offline version, the map is known. In the online, or sensor-based, version, the robot builds the map as it covers. Choset's survey sorts methods along this line and by the kind of decomposition they use.
- **Grid coverage.** The region is a set of grid cells of the tool's size, and the path must visit every cell. This is a [traveling salesman problem](/traveling-salesman-problem/) on the cell centers, with the grid steps as the edges.
- **Several robots.** The region is split among robots, and the objective is often the longest path of any robot. This is a different problem from [coverage control](/coverage-control/), which places static sensors at good positions.
- **Coverage of surfaces and volumes.** Inspection of a ship hull, painting of a car body and 3D printing cover a surface or a stack of layers.
- **Coverage with a sensor footprint.** For survey drones and search, the "tool" is the footprint of a camera or sonar. When the sensor sees far, the task becomes [next-best-view planning](/next-best-view-planning/) or the [watchman route problem](/watchman-route-problem/), where seeing a point is enough and the tool need not pass over it.

## Examples

**A rectangle with a square tool.** Let $P$ be the rectangle $[0, 4] \times [0, 3]$, let $T$ be an axis-aligned unit square, and let the tool move only along axis-parallel segments, in the milling version. The tool center must stay in $[0.5, 3.5] \times [0.5, 2.5]$.

- Vertical lanes at $x = 0.5, 1.5, 2.5, 3.5$, each from $y = 0.5$ to $2.5$, joined at their ends, have length $4 \cdot 2 + 3 \cdot 1 = 11$ and 6 turns.
- Horizontal lanes at $y = 0.5, 1.5, 2.5$, each from $x = 0.5$ to $3.5$, joined at their ends, have length $3 \cdot 3 + 2 \cdot 1 = 11$ and 4 turns.

The lower bound in the next section gives $L \ge (12 - 1)/1 = 11$, so both paths are shortest. They differ in the number of turns, which is why practical planners sweep along the longer side.

**A grid with no good path.** Take the grid cells as unit squares and a unit square tool, and let the region be a $3 \times 3$ block of cells. A closed tour through the 9 cell centers with unit steps would be a Hamiltonian cycle of the $3 \times 3$ grid graph. The grid graph is bipartite with 5 cells of one color and 4 of the other, and a cycle alternates colors, so no such cycle exists. Every covering tour needs at least one diagonal step or one repeated cell.

## Known algorithms

- **[Boustrophedon cell decomposition](/boustrophedon-cell-decomposition/)** (Choset and Pignon, 1998). It splits a known polygonal region into cells at the points where a sweep line changes its number of free intervals, and covers each cell with back and forth lanes. It is complete: it covers every point, given a tool that fits. It gives no bound on the length against the optimum.
- **The [trapezoidal decomposition](/trapezoidal-map/)** with back and forth lanes in each trapezoid. It is complete, with more cells and more turns than the boustrophedon decomposition.
- **Grid methods.** Wavefront distance transforms and spanning-tree coverage on an occupancy grid. They are complete at the resolution of the grid and easy to run online.
- **Approximation algorithms.** Arkin, Fekete and Mitchell give a $(3 + \varepsilon)$-approximation for lawn mowing and a $2.5$-approximation for milling (theorem, in their model).
- **Tool path patterns** from manufacturing: [direction-parallel](/direction-parallel-toolpath/) (zigzag) and [contour-parallel](/contour-parallel-toolpath/) (offset) paths; see [pocket machining](/pocket-machining/) and [toolpath planning](/toolpath-planning/).
- **Exploration first.** When the map is unknown, [frontier-based exploration](/frontier-based-exploration/) builds a map, and an offline method then covers it. Sensor-based versions of the boustrophedon decomposition find the critical points while they cover.

## Bounds

**Theorem (a length lower bound).** If a tool that is a disc of diameter $w$ covers a region of area $A$ along a path of length $L$, then $L \ge (A - \pi w^2/4)/w$. For an axis-aligned square of side $w$ that moves only along axis-parallel segments, $L \ge (A - w^2)/w$.

*Proof.* Let $r = w/2$, and let $p_0, \dots, p_N$ be points on the path with $\sum_i |p_{i+1} - p_i| \le L$. A disc of radius $r$ moved by a vector $\delta$ gains a new area of at most $2r |\delta|$, since the new part lies in the strip that the disc's diameter sweeps across $\delta$. So the union of the discs at $p_0, \dots, p_N$ has area at most $\pi r^2 + 2rL$. As the points become dense on the path, these unions increase to the whole swept set, which must contain $P$. The square case is the same, with a new area of at most $w|\delta|$ for an axis-parallel $\delta$, and $w^2$ for the first square. $\square$

The bound is tight for rectangles whose sides are multiples of $w$, as the example shows. It ignores the turns and the obstacles, so on cluttered regions it is far from the best path.

**Hardness.** Both lawn mowing and milling are NP-hard, by Arkin, Fekete and Mitchell. Their Theorem 1 shows it for lawn mowing with an aligned unit square tool in a connected polygonal region, and the corollaries extend it to simple polygons and to milling of regions with holes (theorem). The grid version contains the Hamiltonian cycle problem in grid graphs: a covering tour of length equal to the number of cells exists if and only if the grid graph has a [Hamiltonian cycle](/hamiltonian-cycle-problem/).

## Reductions

- **To the traveling salesman problem.** On a grid, a tour through all cell centers covers the region, so any [TSP](/traveling-salesman-problem/) method gives a coverage path. The same holds for a set of lanes: ordering the lanes, or the cells of a decomposition, with a choice of the end at which each one starts, is a generalized TSP.
- **From Hamiltonian cycle in grid graphs.** As in the Bounds section. This is the usual source of the NP-hardness of the grid version.
- **To set cover.** Choosing a smallest set of tool positions whose union covers $P$, ignoring the travel, is a geometric [set cover](/set-cover/) problem.

## Applications

Floor cleaning robots, lawn mowing, agriculture (seeding, spraying and harvesting along rows), humanitarian demining, aerial and underwater survey, ship hull inspection, spray painting, and the tool paths of [pocket machining](/pocket-machining/) and of the infill of each layer in additive manufacturing. The survey of Galceran and Carreras lists these uses and the methods that each one uses.

## References
