---
tag: 5WDHQF
kind: problem
slug: escape-routing
name: Escape routing
aliases:
- pin escape routing
area: cad/routing
level: advanced
summary: Route a wire from each pin of a dense pin array on a package or board to the array's boundary, without crossings, often solved by network flow.
prereqs: [max-flow-problem, vertex-capacities-flow]
see_also: [vertex-disjoint-paths, edge-disjoint-paths, menger-theorem, max-flow-min-cut-theorem, dinic, min-cost-flow-problem, river-routing, detailed-routing]
sources:
  - book: isbn:9780262033848
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, third edition, MIT Press, 2009
    locator: Chapter 26, Problem 26-1, the escape problem (vertex-disjoint paths from given grid points to the boundary, solved with vertex capacities and maximum flow)
  - paper: doi:10.1145/1629911.1630001
    title: Tan Yan and Martin D. F. Wong, A correct network flow model for escape routing, Proceedings of the 46th Design Automation Conference (DAC), 332 to 335, 2009
    locator: the failure of earlier flow models to capture the diagonal capacity between pins, and a flow model that captures it, which gives an optimal method for the unordered problem
  - paper: doi:10.1007/s00453-003-1023-8
    title: Wun-Tat Chan, Francis Y. L. Chin and Hing-Fung Ting, Escaping a grid by edge-disjoint paths, Algorithmica 36(4), 343 to 359, 2003
    locator: the condition that no rectangle holds more sources than outlets, which is necessary and sufficient for the edge-disjoint version, and a quadratic time test (general locator)
---

Escape routing is the first routing step for a component with a dense array of pins, such as a ball grid array (BGA) package or a flip-chip die. Each pin that carries a signal must get a wire that leaves the pin array, so that the board router can continue it outside. The pins are close together, only a few wires fit between two neighbor pins, and on one layer the wires cannot cross. The problem asks for one wire per pin, from the pin to the boundary of the array, within these capacities. When any wire may end at any point of the boundary, the problem is a [maximum flow](/max-flow-problem/) problem with [vertex capacities](/vertex-capacities-flow/), and it is solved exactly in polynomial time. When the order of the wires on the boundary is fixed, or with several layers and pairs of wires that must stay together, the problem gets harder, and the methods are measured on industrial cases.

## In plain words

Picture a crowded room with seats in a square pattern, and a person in each seat. Everyone must walk to a door on the outer wall. Between two neighbor seats there is room for only one person at a time, and no two people may use the same spot. The people in the front row walk straight out. The people in the middle must squeeze between the front-row seats, and there are only so many gaps.

Escape routing asks whether everyone can get out, and if not, how many can. On one layer the wires cannot cross.

If it does not matter which door each person uses, the question has an exact answer from network flow: each gap is a pipe of capacity one, and the largest flow from the seats to the doors is the largest number of people who get out.

## Definition

**Input.**

- A routing graph $G = (V, E)$ drawn in the plane without crossings, for one routing layer. Its nodes are the routing points around and between the pins.
- A capacity $c_v \ge 0$ for each node and $c_e \ge 0$ for each edge: the number of wires that can pass there.
- A set $S \subseteq V$ of *pins* to escape, and a set $X \subseteq V$ of *exits* on the boundary of the array.

**Feasible solution.** A set of paths, one for each pin of a chosen subset $S' \subseteq S$, where the path of pin $s$ starts at $s$ and ends at an exit. At most $c_v$ paths use node $v$ and at most $c_e$ paths use edge $e$, a pin node is used only by its own path, and the paths can be drawn without crossings.

**Objective.** The decision version asks whether $S' = S$ is possible: can every pin escape? The optimization version maximizes $|S'|$, and among the solutions with the most escaped pins it minimizes the total wire length.

**Grid model.** The usual model, and the one in CLRS, is an $N \times N$ grid with $c_v = 1$ for every node. Then the paths are *vertex-disjoint*, and vertex-disjoint paths in a plane graph never cross, so the condition on crossings is automatic.

## Variants

- **Unordered and ordered.** In the unordered version a wire may end at any exit. In the ordered version the wires must reach the boundary in a given order, the order of the pins on the next component, so that the board can be routed without crossing outside the array.
- **Edge-disjoint escape.** The paths may share nodes but not edges, as in the problem of Chan, Chin and Ting.
- **Diagonal routing.** Boards and packages often route at 45 degrees. Two pins on a diagonal are farther apart than two neighbor pins in a row, so more wires fit between them. This *diagonal capacity* must be part of the model.
- **Multilayer escape.** Each pin also chooses a layer, through a via under the pin, and the layers share the via sites.
- **Differential pairs.** Two wires of a pair must run side by side to the boundary.
- **Missing pins and blockages.** Some positions of the array have no pin, or hold power pins that need no escape wire, and they open more room.

## Examples

**All pins of a block, vertex-disjoint.** Take the $5 \times 5$ grid with nodes $(x, y)$, $0 \le x, y \le 4$, capacity 1 on every node, and the 16 border nodes as exits. The pins are the 9 inner nodes $(x, y)$ with $1 \le x, y \le 3$. The 8 pins of the inner ring each have a border neighbor and escape in one step. The center pin $(2,2)$ has only pins as neighbors, and each of them is already used by its own path. So at most 8 of the 9 pins escape. If the pin at $(2,1)$ is removed, all 8 remaining pins escape: the center goes through the free node $(2,1)$ to $(2,0)$.

**A ball grid array with one track between balls.** Take an $n \times n$ array of balls and a routing grid in which one wire fits between two neighbor balls. In the grid coordinates, ball $(i, j)$ is at the point $(1 + 2i, 1 + 2j)$, the routing grid has $(2n+1) \times (2n+1)$ points, the points of its outer ring are the exits, and every point that is not a ball has capacity 1. Wires run along the grid lines, with no diagonal steps. The maximum flow gives these counts of escaped balls:

| $n$ | 5 | 6 | 7 | 8 | 9 | 10 |
| --- | --- | --- | --- | --- | --- | --- |
| balls | 25 | 36 | 49 | 64 | 81 | 100 |
| escaped, one track between balls | 25 | 36 | 44 | 52 | 60 | 68 |
| escaped, two tracks between balls | 25 | 36 | 49 | 64 | 81 | 96 |

A cut proves the count for $n = 7$ with one track. The outer ring has $4(n - 1) = 24$ balls, and each side of it has $n - 1 = 6$ gaps, 24 gaps in all. A wire from an inner ball must leave through one of these gaps. At each corner, the two gaps next to the corner ball can be reached from the inside only through one grid point, the point diagonal to the corner ball, which has capacity 1. So at most $24 - 4 = 20$ inner balls escape, and at most $24 + 20 = 44$ balls in all. The flow reaches 44. The same count gives the bound $8n - 12$ for every $n$, and the table shows that it is reached for $7 \le n \le 10$.

With diagonal steps, the corner points are no longer a bottleneck of capacity 1, and the counts change. This is the reason why the diagonal capacity must be modeled.

## Known algorithms

| Method | Version | What is known |
| --- | --- | --- |
| [Maximum flow](/max-flow-problem/) with [vertex capacities](/vertex-capacities-flow/), for example by [Dinic's algorithm](/dinic/) | unordered, one layer, grid model | exact; the flow value is the largest number of escaped pins |
| [Min-cost flow](/min-cost-flow-problem/) | unordered, one layer, grid model | exact; the most escaped pins with the least total length |
| Flow model with extra nodes inside each tile (Yan and Wong 2009) | unordered, one layer, with diagonal capacity | exact for this model; earlier flow models could violate the diagonal capacity or miss a legal routing |
| Rectangle test (Chan, Chin and Ting 2003) | edge-disjoint, grid | exact decision in quadratic time |
| Integer programming and [SAT](/sat/) formulations | ordered, multilayer, differential pairs | exact with exponential worst-case time, or heuristic; measured on industrial designs |

What is proved: the unordered one-layer versions above are solved exactly in polynomial time by flow. What is only measured: the methods for the ordered, multilayer and pair versions, which are compared on test boards and packages.

## Bounds

**Cut bound.** For a set $U$ of nodes that contains no exit, every path from a pin in $U$ leaves $U$. So the number of pins in $U$ that escape is at most the capacity of any set of nodes that separates the pins of $U$ from the exits. By the [max-flow min-cut theorem](/max-flow-min-cut-theorem/), in the grid model the least capacity of a separator between all pins and the exits equals the maximum number of escaped pins. With capacity 1 this is [Menger's theorem](/menger-theorem/) for [vertex-disjoint paths](/vertex-disjoint-paths/).

**Rectangles are enough for edge-disjoint paths.** In the edge-disjoint grid version, Chan, Chin and Ting showed that every pin escapes exactly when no rectangle of the grid holds more pins than outlets, the edges by which a path can leave the rectangle. So the cut bound needs to be checked only on rectangles.

**One track between balls.** As in the example, at most $\min(n^2, 8n - 12)$ balls of an $n \times n$ array escape in the rectilinear model with one track between balls. So beyond $n = 6$, a single layer cannot escape the whole array, and the other balls need more layers.

**Running time.** The flow network of an $n \times n$ array with $k$ tracks between balls has $O(n^2 k^2)$ nodes and edges, and at most $n^2$ units of flow. Augmenting paths give time $O(n^4 k^2)$, and faster flow algorithms do better.

## Reductions

- **To maximum flow.** Add a source joined to every pin and a sink joined from every exit. Split each node $v$ into an in-node and an out-node joined by an arc of capacity $c_v$, and give each edge its capacity in both directions. An integral maximum flow gives the escape wires, because a maximum flow with integer capacities can be chosen integral.
- **To vertex-disjoint paths.** In the grid model with capacity 1, an escape routing is a set of [vertex-disjoint paths](/vertex-disjoint-paths/) from the pins to a new node joined to all exits.
- **Ordered version and river routing.** With the order on the boundary fixed, the wires outside the array form a [river routing](/river-routing/) problem, in which the wires on one layer keep their order.

## Applications

- **Package and board design.** The balls of a BGA must escape to the board, and the bumps of a flip-chip die must escape to the package, before the rest of the board or package is routed.
- **Layer count.** The number of balls that escape on one layer decides how many board layers a component needs, which is a large part of the board cost.
- **Teaching flows.** The grid model is a standard exercise on [maximum flow](/max-flow-problem/) with vertex capacities.

## References
