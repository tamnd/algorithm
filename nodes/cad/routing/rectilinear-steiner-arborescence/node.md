---
tag: PZZJ0Y
kind: problem
slug: rectilinear-steiner-arborescence
name: Rectilinear Steiner arborescence
aliases:
- minimum rectilinear Steiner arborescence
area: cad/routing
level: advanced
summary: Find a shortest rectilinear tree from a source to sinks in which every path from the source is monotone, so each sink is reached by a shortest path.
prereqs: [rectilinear-steiner-tree-problem, shortest-path-tree]
see_also: [rectilinear-steiner-tree-problem, shortest-path-tree, minimum-arborescence, prim-dijkstra-tradeoff, bounded-radius-bounded-cost-tree, elmore-delay, clock-tree-synthesis, strong-np-hardness]
sources:
  - paper: doi:10.1007/BF01758762
    title: Sailesh K. Rao, P. Sadayappan, Frank K. Hwang and Peter W. Shor, The rectilinear Steiner arborescence problem, Algorithmica 7, 277 to 288, 1992
    locator: the definition for sinks in the first quadrant, basic properties, an O(n log n) heuristic with ratio 2, and the error in an earlier polynomial algorithm
  - paper: "Weiping Shi and Chen Su, The rectilinear Steiner arborescence problem is NP-complete, SIAM Journal on Computing 35(3), 729 to 740; first version in the Proceedings of the ACM-SIAM Symposium on Discrete Algorithms (SODA), 2000, 780 to 786"
    locator: the reduction from planar 3SAT that shows strong NP-completeness
  - paper: doi:10.1137/0114025
    title: M. Hanan, On Steiner's problem with rectilinear distance, SIAM Journal on Applied Mathematics 14(2), 255 to 265, 1966
    locator: the rectilinear Steiner tree problem without the path condition, for comparison
---

The rectilinear Steiner arborescence (RSA) problem asks for a shortest network of horizontal and vertical wires that joins a source to a set of sinks, with the condition that the path in the tree from the source to each sink is a shortest path in the L1 metric. Such a path never turns back: along it, $x$ only grows or only falls, and so does $y$. Without this condition the problem is the [rectilinear Steiner tree problem](/rectilinear-steiner-tree-problem/), which minimizes only the total wire. With it, the tree is also a [shortest path tree](/shortest-path-tree/) for the sinks, so every sink has the least possible path length, which keeps signal delay low. Rao, Sadayappan, Hwang and Shor (1992) studied the basic properties and gave a 2-approximation. Shi and Su (SODA 2000, journal in SIAM J. Comput.) proved that the decision form is NP-complete in the strong sense. In electronic design automation (EDA) it is the model of a net that must be short and also fast.

## In plain words

A signal starts at one pin, the source, and must reach several other pins, the sinks. You join them with wire that runs only left, right, up and down, and you may branch anywhere.

Each sink must be reached by a shortest route: no step away from the sink, so no detour. Within that rule, use as little wire in total as you can.

The rule costs wire. Without it, a sink can hang from a wire that first goes past it and then comes back, which is shorter in total but slower for that sink. With it, the wire to each sink is as short as possible, and the tree as a whole is the shortest one with this property.

## Definition

**Input.** A source point $s$ and a finite set $N$ of $n$ sink points in the plane. Distances are L1: $d(p, q) = |p_x - q_x| + |p_y - q_y|$.

**Feasible solutions.** A *rectilinear Steiner tree* of $\{s\} \cup N$ is a finite union of horizontal and vertical segments that is connected, has no cycle and contains $s$ and $N$. It is a *rectilinear Steiner arborescence* if for every sink $t \in N$ the path in the tree from $s$ to $t$ has length $d(s, t)$.

**Objective.** Minimize the total length of the tree. Write $\mathrm{RSA}(s, N)$ for the least length.

**Decision form.** Given $s$, $N$ with integer coordinates and an integer $L$, is there a rectilinear Steiner arborescence of length at most $L$? It is NP-complete in the strong sense (Shi and Su).

**Monotone paths.** A rectilinear path from $s$ to $t$ has length at least $d(s, t)$, since its horizontal pieces cover at least $|s_x - t_x|$ and its vertical pieces at least $|s_y - t_y|$. Equality holds exactly when the $x$ coordinate along the path never changes direction and the $y$ coordinate never changes direction. So the path condition says that every source to sink path is monotone in both coordinates.

**The quadrant form.** Rao, Sadayappan, Hwang and Shor state the problem with $s$ at the origin and all sinks in the first quadrant. Then a tree is an arborescence exactly when its segments can be oriented from left to right and from bottom to top, with every sink reachable from $s$. Sinks in other quadrants are handled by reflection. In the general form, sinks in different quadrants can share wire on the lines through $s$, so the problem does not split into independent quadrant problems.

## Variants

- **Directed grid form.** On a grid graph whose edges point only right and up, the problem is a directed Steiner tree problem with the source as root.
- **Online form.** The sinks arrive one at a time and each must be joined when it arrives, without moving earlier wire.
- **Obstacles.** Wire must avoid blocked regions of the chip, and paths must still be shortest among the paths that avoid them.
- **Bounded radius trees.** Relaxing the path condition to a path length of at most $(1 + \varepsilon)\, d(s, t)$ gives trees that trade radius for wire, as in [bounded-radius bounded-cost trees](/bounded-radius-bounded-cost-tree/) and the [Prim-Dijkstra tradeoff](/prim-dijkstra-tradeoff/). The arborescence is the case $\varepsilon = 0$.
- **Graph version.** In a general directed graph with a root, a cheapest subgraph that reaches all sinks, without the shortest path condition, is the directed Steiner tree problem. When all vertices are sinks it is the [minimum arborescence](/minimum-arborescence/) problem.

## Examples

**Two sinks.** For $s$ and two sinks $a, b$, let $m$ be the point with the median $x$ and the median $y$ of the three points. The median of three numbers lies between any two of them, so the paths $s \to m \to a$ and $s \to m \to b$ are monotone. The star at $m$ has length equal to the half perimeter of the bounding box, which is the least length of any rectilinear tree of three points. So for two sinks the arborescence and the rectilinear Steiner minimal tree have the same length.

**The path condition costs wire.** Let $s = (0, 0)$ and $N = \{(1, 0), (1, 1), (1, 2), (0, 2)\}$.

- The rectilinear Steiner minimal tree is the path $(0, 0) \to (1, 0) \to (1, 2) \to (0, 2)$, of length $1 + 2 + 1 = 4$. It cannot be shorter than 4, because the four corners of the 1 by 2 rectangle need length 4. But in it the sink $(0, 2)$ is at path length 4, while $d(s, (0, 2)) = 2$.
- In an arborescence the only monotone path from $(0, 0)$ to $(0, 2)$ is the segment on $x = 0$, and the only monotone path to $(1, 0)$ is the segment on $y = 0$. These two segments have length 3 and meet only at $s$. The sinks $(1, 1)$ and $(1, 2)$ are each at distance 1 from these segments. One segment of length 1 that holds both is $(1, 1)$ to $(1, 2)$, which then needs at least 1 more to reach the tree. So at least 2 more units are needed, and $\mathrm{RSA} \ge 5$.
- The tree of the two segments and the segment from $(1, 0)$ to $(1, 2)$ has length 5, and its paths to $(1, 1)$ and $(1, 2)$ go right and then up. So $\mathrm{RSA} = 5$, and the ratio to the Steiner minimal tree is $5/4$ here.

## Known algorithms

- **Exact.** Exponential time methods, such as search over the grid of lines through the points. No polynomial algorithm is known, and none exists unless P = NP, by the result of Shi and Su. Rao, Sadayappan, Hwang and Shor showed that a polynomial algorithm for the problem published earlier, by Trubin in 1985, is not correct.
- **The Rao, Sadayappan, Hwang and Shor heuristic.** A greedy method that runs in $O(n \log n)$ time and gives an arborescence of length at most twice the optimum (Rao et al. 1992).
- **Heuristics in routing tools.** Performance-driven routers build arborescences or near-arborescences with greedy merging, and the [Prim-Dijkstra tradeoff](/prim-dijkstra-tradeoff/) and [bounded-radius bounded-cost trees](/bounded-radius-bounded-cost-tree/) approach them from spanning trees. These are not covered here.

## Bounds

The following are proved on this page or cited.

- **Lower bound by the Steiner tree.** Every arborescence is a rectilinear Steiner tree, so $\mathrm{RSA}(s, N) \ge \mathrm{RSMT}(\{s\} \cup N)$. The example above shows that the inequality can be strict.
- **Lower bound by the box.** In the quadrant form with $s$ at the origin, a connected set that holds $s$ and a sink with $x = X$ has horizontal pieces of total length at least $X$, and the same holds for $y$. So $\mathrm{RSA} \ge \max_t t_x + \max_t t_y$.
- **Upper bound by the sum of distances.** The union of one monotone path per sink can contain cycles, but a shortest path tree from $s$ in a grid graph that contains all the points holds a shortest path to every sink. After removing the branches with no sink, its length is at most $\sum_{t \in N} d(s, t)$.
- **Approximation.** The heuristic of Rao et al. gives ratio 2 (cited).
- **Hardness.** The decision form is NP-complete in the strong sense (Shi and Su, cited), so there is no fully polynomial approximation scheme unless P = NP, by the usual argument for [strongly NP-hard](/strong-np-hardness/) problems with integer objective.

## Reductions

- **From planar 3SAT.** Shi and Su reduce planar 3SAT to the decision form. Planar 3SAT has no numbers, so the reduction builds instances whose coordinates are bounded by a polynomial in the size of the formula, and this makes the hardness strong.
- **To directed Steiner tree.** On a directed grid graph whose edges go away from the source, an arborescence of the grid is a directed Steiner tree with the source as the root. This is the variant above.

## Applications

- **Performance-driven routing.** In VLSI routing the delay from the driver of a net to a sink grows with the wire on the path to that sink, as the [Elmore delay](/elmore-delay/) model shows. An arborescence makes every source to sink path as short as it can be, and among such trees it uses the least total wire, which also lowers the load on the driver.
- **Clock trees.** A clock net also has one source and many sinks, but there the goal is equal delay to all sinks, zero skew, instead of shortest paths, see [clock tree synthesis](/clock-tree-synthesis/).
- **A reference for tradeoffs.** Trees that trade radius for wire are compared with the two extremes: the Steiner minimal tree for wire and the arborescence for radius.

## References
