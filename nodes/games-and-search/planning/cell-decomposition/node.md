---
tag: 9HY0M9
kind: technique
slug: cell-decomposition
name: Cell decomposition
aliases:
- cell decomposition method
area: games-and-search/planning
level: core
summary: Partitions free space into simple cells and searches the adjacency graph of cells.
prereqs: [motion-planning, configuration-space, trapezoidal-map]
see_also: [quadtree, cylindrical-algebraic-decomposition, visibility-graph, breadth-first-search, convex-decomposition, piano-movers-problem, probabilistic-roadmap, vertical-ray-shooting]
sources:
  - book: isbn:9780792391296
    title: Jean-Claude Latombe, Robot Motion Planning, Kluwer Academic Publishers, 1991
    locator: the chapters on exact and on approximate cell decomposition (general locator, chapter numbers not checked)
  - book: isbn:9780521862059
    title: Steven M. LaValle, Planning Algorithms, Cambridge University Press, 2006
    locator: Section 6.2.2 (vertical cell decomposition of a polygonal free space), Section 6.3 (cell decompositions in higher dimensions), Section 6.4.2 (cylindrical algebraic decomposition)
  - book: isbn:9780262033275
    title: Howie Choset, Kevin M. Lynch, Seth Hutchinson, George Kantor, Wolfram Burgard, Lydia E. Kavraki and Sebastian Thrun, Principles of Robot Motion, MIT Press, 2005
    locator: Chapter 6 (cell decompositions, trapezoidal and Morse decompositions, coverage)
  - paper: doi:10.1109/TSMC.1985.6313352
    title: Rodney A. Brooks and Tomás Lozano-Pérez, A subdivision algorithm in configuration space for findpath with rotation, IEEE Transactions on Systems, Man, and Cybernetics SMC-15(2), 1985
    locator: pages 224 to 233 (recursive subdivision of the configuration space into empty, full and mixed cells)
  - paper: doi:10.1016/0196-8858(83)90014-3
    title: Jacob T. Schwartz and Micha Sharir, On the piano movers' problem II, general techniques for computing topological properties of real algebraic manifolds, Advances in Applied Mathematics 4(3), 1983
    locator: pages 298 to 351 (exact decomposition of a semi-algebraic free space into cylindrical cells)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 13 (the trapezoidal map of the free space of a point robot and the road map through its cells; section numbers not checked)
---

Cell decomposition is a [motion planning](/motion-planning/) technique that cuts the free part of the [configuration space](/configuration-space/) into cells of a simple shape, links the cells that touch, and searches the graph of cells for a chain from the start cell to the goal cell. An *exact* decomposition covers the free space exactly and gives a complete planner. An *approximate* decomposition uses boxes of a fixed shape, such as the cells of a [quadtree](/quadtree/), and gives a planner that is complete only down to the size of its smallest box. The technique finds a path, not a shortest one.

## In plain words

Think of a floor plan with furniture on it. Draw vertical lines through every corner of every piece of furniture. The open floor falls apart into simple pieces, each with straight sides. Inside one piece you can walk in a straight line from any point to any other. Two pieces that share a side have a door between them.

Now forget the shapes and keep only the list of pieces and doors. That is a small map of rooms and doors. Find a chain of rooms from the room of the start to the room of the goal. Walk to the first door, through the room, to the next door, and so on.

If the furniture is hard to cut exactly, use squares. Split any square that is part free and part blocked into four smaller squares, and stop at some small size.

## When it applies

- The free space has an explicit description, for example polygons in the plane or polyhedra in space, so that cells can be computed. This is the case for a point robot or a translating robot, after the C-obstacles are built as [Minkowski sums](/minkowski-sum/).
- The dimension $d$ is small: 2 or 3 for exact methods in practice, and up to about 4 or 5 for approximate methods. The number of cells of an approximate decomposition at resolution $h$ in a box of side $L$ can reach $(L/h)^d$, so the cost is exponential in $d$.
- A planner must report correctly that no path exists. An exact decomposition does that, which sampling planners such as the [probabilistic roadmap](/probabilistic-roadmap/) cannot do.
- An approximate decomposition needs only a test that says whether a box is fully free, fully blocked or mixed. It does not need the exact shape of $\mathcal{C}_{free}$.
- It does not apply when a shortest path is the goal. For a point among polygons, the [visibility graph](/visibility-graph/) gives a [Euclidean shortest path](/euclidean-shortest-path/). It does not apply in high dimensions, where sampling planners are used.

## The template

Let $\mathcal{C}_{free}$ be the free space, $q_I$ the start and $q_G$ the goal. A *cell* is a connected set in which any two points can be joined by a simple path inside the cell, in this page a straight segment, because every cell is convex. A *door* is a point on the common boundary of two adjacent cells.

```pseudo id=main
CELL-DECOMPOSITION-PLAN(C_free, q_I, q_G)
L1  K ← DECOMPOSE(C_free)              ▷ convex cells with disjoint interiors
L2  G ← the graph with one node per cell of K
L3  for each pair of cells c, c′ of K that share a boundary piece do
L4      add the edge {c, c′} to G, with a door point on the shared piece
L5  c_I ← LOCATE(K, q_I), c_G ← LOCATE(K, q_G)
L6  if c_I = nil or c_G = nil then return failure
L7  π ← GRAPH-SEARCH(G, c_I, c_G)       ▷ breadth-first search, Dijkstra or A*
L8  if π = nil then return failure
L9  return q_I, door(π₁, π₂), center(π₂), door(π₂, π₃), …, q_G

APPROXIMATE-DECOMPOSE(C_free, B, h)    ▷ B a box, h the smallest side
L10 if B ⊆ C_free then return {B}       ▷ a free cell
L11 if B ∩ C_free = ∅ then return ∅     ▷ a full cell
L12 if side(B) ≤ h then return ∅        ▷ a mixed cell at the limit, treated as blocked
L13 return the union of APPROXIMATE-DECOMPOSE(C_free, B′, h) over the 2^d children B′ of B
```

**Why it works.** Every cell is convex, so the segment from a door to the center of a cell and from the center to the next door lies in the closure of the cell. Routing through the center, and not from one door straight to the next, keeps the path away from a vertex when two doors lie on the same side of a cell. So every path that line L9 returns is free. Conversely, if an exact decomposition is used and a free path from $q_I$ to $q_G$ exists, the cells that the path crosses, in order, form a walk in $G$ from $c_I$ to $c_G$, because the path can only leave a cell through its boundary into an adjacent cell. So the search of line L7 finds a chain, and the planner is complete. The approximate version keeps only boxes that are fully free, so its paths are free too. It loses the passages that lie only in mixed boxes of side $h$. So it is *resolution complete*: it finds a path whenever one exists in the union of the free boxes, and a failure says nothing about passages narrower than about $h$ (Brooks and Lozano-Pérez 1985).

**Cost.** For a point among polygons with $n$ vertices in total, the vertical decomposition, the [trapezoidal map](/trapezoidal-map/), has $O(n)$ cells and can be built in $O(n \log n)$ time, by a sweep or by the randomized incremental method in expected time. A point is located in $O(\log n)$ time with the search structure of the map, or by [vertical ray shooting](/vertical-ray-shooting/). The graph has $O(n)$ nodes and edges, so [breadth-first search](/breadth-first-search/) takes $O(n)$ time. The simple slab version used in the implementation below cuts the whole map at every vertex and every crossing, which gives $O(n^2)$ cells in the worst case and is easier to code. For a semi-algebraic free space of dimension $d$ given by $n$ constraints, the [cylindrical algebraic decomposition](/cylindrical-algebraic-decomposition/) has a number of cells polynomial in $n$ and doubly exponential in $d$. The approximate method costs one box test per box, and the number of boxes depends on the area of the obstacle boundaries at scale $h$, with up to $(L/h)^d$ boxes. These bounds are proved. The times of the box tests are measured.

## Classic examples

**An exact slab decomposition.** The map is the square $[0, 10]^2$. The obstacles are the triangle with corners $(2, 1)$, $(5, 2)$, $(3, 6)$ and the rectangle $[6, 8] \times [3, 10]$, which touches the top of the map. The vertical lines go through the $x$ of every vertex, $x \in \{0, 2, 3, 5, 6, 8, 10\}$. The free part of each slab splits into trapezoids. There are 8 cells.

| cell | slab | below | above |
|---|---|---|---|
| 0 | $[0, 2]$ | the bottom $y = 0$ | the top $y = 10$ |
| 1 | $[2, 3]$ | $y = 0$ | the edge from $(2, 1)$ to $(5, 2)$ |
| 2 | $[2, 3]$ | the edge from $(3, 6)$ to $(2, 1)$ | $y = 10$ |
| 3 | $[3, 5]$ | $y = 0$ | the edge from $(2, 1)$ to $(5, 2)$ |
| 4 | $[3, 5]$ | the edge from $(5, 2)$ to $(3, 6)$ | $y = 10$ |
| 5 | $[5, 6]$ | $y = 0$ | $y = 10$ |
| 6 | $[6, 8]$ | $y = 0$ | the rectangle at $y = 3$ |
| 7 | $[8, 10]$ | $y = 0$ | $y = 10$ |

The doors are the midpoints of the shared vertical pieces: cells 0 and 1 at $(2, 0.5)$, 0 and 2 at $(2, 5.5)$, 1 and 3 at $(3, 0.667)$, 2 and 4 at $(3, 8)$, 3 and 5 at $(5, 1)$, 4 and 5 at $(5, 6)$, 5 and 6 at $(6, 1.5)$, and 6 and 7 at $(8, 1.5)$. The start $(1, 8)$ lies in cell 0 and the goal $(9, 8)$ in cell 7. Breadth-first search returns the chain $0, 1, 3, 5, 6, 7$, and the path is

$$(1, 8), (2, 0.5), (2.5, 0.583), (3, 0.667), (4, 0.833), (5, 1), (5.5, 5), (6, 1.5), (7, 1.5), (8, 1.5), (9, 8)$$

of length 26.751. The chain $0, 2, 4, 5, 6, 7$ has the same number of cells, and the search takes the first one it finds. The shortest path in the closure of the free space, from the visibility graph, goes $(1, 8), (6, 3), (8, 3), (9, 8)$ and has length 14.170. Cell decomposition answers "is there a path" and gives one. It does not give the shortest one.

**The same map with a quadtree.** The approximate method starts with the whole square and splits every mixed box until its side reaches the smallest size.

| smallest side | free boxes | mixed boxes at the limit | path found |
|---|---|---|---|
| 1.25 | 22 | 25 | no |
| 0.625 | 61 | 51 | yes |
| 0.3125 | 125 | 101 | yes |
| 0.15625 | 199 | 204 | yes |

At side 1.25 the boxes near the triangle and the rectangle are all mixed, and the free boxes do not connect the start to the goal.

**A narrow gap.** Two walls $[4, 6] \times [0, 4.7]$ and $[4, 6] \times [5.3, 10]$ leave a gap of width 0.6. The start is $(1, 5)$ and the goal $(9, 5)$.

| smallest side | free boxes | mixed boxes at the limit | path found |
|---|---|---|---|
| 1.25 | 24 | 16 | no |
| 0.625 | 24 | 36 | no |
| 0.3125 | 24 | 76 | no |
| 0.15625 | 180 | 148 | yes |

The quadtree finds the gap only when its boxes are small enough to fit in it. Its three failures are not proofs that no path exists. The exact slab decomposition of the same map has 3 cells and finds the path at once.

**Cylindrical decomposition.** Schwartz and Sharir solved the general [piano movers' problem](/piano-movers-problem/) by a cylindrical algebraic decomposition of $\mathcal{C}_{free}$, an exact decomposition into cells that are cylinders over the cells of a lower dimension. It is the exact template in any dimension, at a cost doubly exponential in $d$.

## Variations

- **Trapezoidal or vertical decomposition.** Extend a vertical segment up and down from each vertex only until it hits an obstacle. This gives $O(n)$ cells, against $O(n^2)$ for full slabs. It is the [trapezoidal map](/trapezoidal-map/) of the obstacle edges.
- **Triangulation.** Triangulate the free space, or split it with a [convex decomposition](/convex-decomposition/). Every triangle is convex, so the same template works.
- **Critical curves.** For a ladder or a polygon that rotates, cut $\mathcal{C} = \mathbb{R}^2 \times S^1$ where the combinatorial type of the free slice changes. This is the method of the first Schwartz and Sharir paper.
- **Weighted search.** Give each edge of $G$ the length of the segment between the two doors through the cell center, and run [Dijkstra](/dijkstra/) or [A*](/a-star-search/). The path is shorter, but it is still not the shortest path in the free space.
- **Octrees and $2^d$-trees.** The approximate template in 3 or $d$ dimensions. Each mixed box has $2^d$ children.
- **Morse and boustrophedon decompositions.** For coverage, where a robot must sweep every point of the free space, cells are chosen so that a back-and-forth motion covers each one (Choset et al., Chapter 6).
- **Grids.** A uniform grid is the approximate method without the tree. [A*](/a-star-search/) on the grid cells, with speedups such as [jump point search](/jump-point-search/), is grid pathfinding. It treats the cells as a fixed graph and does not refine them.

## Pitfalls

- **Treating mixed boxes as free.** Then a path can cross an obstacle. A mixed box at the size limit must count as blocked, which makes the method conservative.
- **Reading a failure as a proof.** An approximate decomposition that finds no path proves only that no path exists through its free boxes. Refine and try again, or use an exact method.
- **Doors at vertices.** Two doors on the same side of a trapezoid can be joined by a segment that runs along an obstacle edge or through a shared vertex. Go through the center of the cell, or place the doors at the midpoints of the shared pieces.
- **Degenerate input.** Two vertices with the same $x$, or a vertical obstacle edge, make slabs of width zero. Perturb the input or handle these cases in the sweep.
- **Ignoring the wrap of angles.** For a rotating robot, the cells at angle $0$ and angle $2\pi$ touch. A decomposition that treats the angle as an interval misses these adjacencies, as the two-link arm on the [configuration space](/configuration-space/) page shows.
- **Expecting short paths.** The path follows doors and centers. Smooth it afterward, or use the visibility graph when length matters.

## Exercises

1. For the slab example above, list the cells of slab $[2, 3]$ and say why there are two of them. *Answer:* cells 1 and 2, below and above the triangle, because the vertical line at $x = 2.5$ crosses the triangle between $y \approx 1.17$ and $y = 3.5$.
2. Show that the vertical decomposition of a free space bounded by $n$ obstacle edges in general position has at most $3n + 1$ trapezoids. *Answer:* charge each trapezoid to the point that fixes its left side. The left end of a segment fixes at most two, the right end of a segment at most one, and the corner of the bounding box one, so there are at most $3n + 1$ (de Berg et al., Chapter 6).
3. A quadtree in a square of side 10 must resolve a gap of width 0.6. What smallest side guarantees that some free box lies in the gap, whatever its position? *Answer:* a side $s$ with $2s \le 0.6$, so $s \le 0.3$; the first power of two below that in the example is $10/64 = 0.15625$. The run with $10/32 = 0.3125$ fails.
4. Why is the exact decomposition complete while the approximate one is not? *Answer:* the exact cells cover all of $\mathcal{C}_{free}$, so every free path crosses a chain of adjacent cells; the approximate cells miss the free parts of mixed boxes.

## References
