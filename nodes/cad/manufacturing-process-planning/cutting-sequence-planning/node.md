---
tag: Z3M3JK
kind: problem
slug: cutting-sequence-planning
name: Cutting sequence planning
aliases:
- laser cutting path planning
- cutting path optimization
area: cad/manufacturing-process-planning
level: advanced
summary: Order the contours cut from a sheet and choose their pierce points to minimise idle travel, a generalized traveling salesman problem with precedence.
prereqs: [traveling-salesman-problem]
see_also: [nesting-problem, operation-sequencing, toolpath-planning, computer-aided-process-planning, dag-shortest-paths, genetic-algorithm, simulated-annealing, euclidean-tsp]
sources:
  - paper: doi:10.1007/s00170-016-8609-1
    title: Reginald Dewil, Pieter Vansteenwegen and Dirk Cattrysse, A review of cutting path algorithms for laser cutters, International Journal of Advanced Manufacturing Technology 87(5 to 8), 2016, 1865 to 1884
    locator: the classes of cutting path problems, from fixed pierce points to free pierce points and contours cut in several pieces, with the precedence and heat constraints of laser cutting
  - paper: doi:10.1080/07408179708966382
    title: Jeffrey Hoeft and Udatta S. Palekar, Heuristics for the plate-cutting traveling salesman problem, IIE Transactions 29(9), 1997, 719 to 731
    locator: the plate-cutting TSP, in which the cutter visits each contour once with a choice of the entry point, and heuristics for it
  - paper: doi:10.1080/03155986.1993.11732212
    title: Charles E. Noon and James C. Bean, An efficient transformation of the generalized traveling salesman problem, INFOR 31(1), 1993, 39 to 44
    locator: the transformation of the generalized TSP into an asymmetric TSP on the same nodes
  - paper: doi:10.1016/0304-3975(77)90012-3
    title: Christos H. Papadimitriou, The Euclidean travelling salesman problem is NP-complete, Theoretical Computer Science 4(3), 1977, 237 to 244
    locator: the NP-completeness of the TSP with Euclidean distances, the source of the hardness result on this page
---

Cutting sequence planning chooses the order in which a laser, plasma or water jet cutter cuts the contours of the parts on a sheet, and the pierce point where each cut starts. The layout of the parts on the sheet is fixed before, by [nesting](/nesting-problem/). The cutting time itself does not depend on the order, since every contour is cut once at its own speed. What the plan can change is the idle travel: the moves of the head with the beam off, from the end of one contour to the pierce point of the next. Some orders are not allowed. A hole in a part must be cut before the outer contour of the part, since the part can drop or move once it is free. So the problem is a traveling salesman problem in which each city is a contour with a choice of points, the *generalized* traveling salesman problem, with precedence constraints. This page states it, proves that it is NP-hard, and solves a small instance.

## In plain words

A laser cutter cuts many parts from one sheet of metal. For each shape, the head goes to a point on the shape, burns a hole there (a pierce), and follows the shape around until it is back at the pierce. Then it moves with the beam off to the next shape. These moves cost time and add nothing to the parts.

The planner picks the order of the shapes and the point on each shape where the cut starts, so that the moves are short. One rule limits the order: holes inside a part come first, and the outside of the part comes last, because a part that is cut free can drop, tilt or shift, and then its holes would be cut in the wrong place.

## Definition

There is no standard formal statement of cutting sequence planning. The following version is the common core of the work that Dewil, Vansteenwegen and Cattrysse (2016) review.

**The generalized TSP.** The generalized traveling salesman problem (GTSP) is defined here, since it has no page of its own. Its input is a set of nodes split into disjoint clusters $V_1, \dots, V_m$, and a cost for each ordered pair of nodes. A solution is a closed tour that visits exactly one node of each cluster. The goal is a tour of least total cost. With one node per cluster it is the [traveling salesman problem](/traveling-salesman-problem/).

**Input.**
- Closed contours $K_1, \dots, K_m$ on the sheet, from the nesting layout.
- For each contour $K_j$, a finite set $P_j \subset K_j$ of allowed pierce points.
- A home point $h$ of the head.
- A travel time $d(p, q)$ between points: the Euclidean distance over the speed for a head that moves along straight lines, or $\max(\lvert p_x - q_x \rvert / v_x, \lvert p_y - q_y \rvert / v_y)$ for a gantry whose axes move at the same time with their own top speeds.
- A precedence relation $\prec$ on the contours: $K_i \prec K_j$ when $K_i$ lies inside $K_j$, so $K_i$ must be cut before $K_j$.

**Output.** An order $\pi$ of the contours that is a linear extension of $\prec$, and a pierce point $p_j \in P_j$ for each contour.

**Objective.** A closed contour starts and ends at its pierce point, so the idle travel is
$$d(h, p_{\pi_1}) + \sum_{i=1}^{m-1} d(p_{\pi_i}, p_{\pi_{i+1}}) + d(p_{\pi_m}, h),$$
and the goal is to minimize it. This is a GTSP with the home point as a cluster of its own, the clusters $P_1, \dots, P_m$, and precedence between clusters. In versions where the head does not return home, drop the last term.

## Variants

- **Free pierce points.** The pierce point can be any point of the contour, not one of a finite set. Then the choice is continuous, and a common method is to sample each contour.
- **Contours cut in pieces.** A contour may be cut in several pieces with moves between them, for example to spread the heat. This gives more freedom and more choices.
- **Common line cutting.** Two parts that share an edge in the layout are cut with one pass along that edge. This changes the contours, so it joins sequencing with nesting.
- **Heat constraints.** The cutter must not cut near a region that it has just cut, to limit distortion of the sheet.
- **Tip-up avoidance.** A part that is cut free can tilt up, and the head must not travel over it. This adds rules on the order and on the travel paths.
- **Single tool sequencing in machining.** The same model, with holes or pockets as contours, is the hole sequencing case of [operation sequencing](/operation-sequencing/).

## Examples

**Two parts with holes.** A sheet holds two rectangular parts with a round hole each. All lengths are in mm, and the travel time is the Euclidean distance. The home point is $h = (0, 0)$. Each contour has four allowed pierce points.

| contour | shape | pierce points |
|---|---|---|
| $A$ | rectangle $[10, 40] \times [10, 30]$ | its four corners |
| $a$ | circle of radius 5 at $(25, 20)$, inside $A$ | $(30, 20), (25, 25), (20, 20), (25, 15)$ |
| $B$ | rectangle $[50, 80] \times [10, 30]$ | its four corners |
| $b$ | circle of radius 5 at $(65, 20)$, inside $B$ | $(70, 20), (65, 25), (60, 20), (65, 15)$ |

The precedence is $a \prec A$ and $b \prec B$. The head does not return home.

- *A careless plan.* Order $a, A, b, B$, with the first listed pierce point of each contour: $(30, 20), (10, 10), (70, 20), (50, 10)$. The travel is $36.06 + 22.36 + 60.83 + 22.36 = 141.61$ mm.
- *Optimum.* The same order with the pierce points $(25, 15), (40, 10), (60, 20), (50, 10)$. The travel is $29.15 + 15.81 + 22.36 + 14.14 = 81.47$ mm.

There are 6 orders that respect the precedence and $4^4 = 256$ choices of pierce points, so 1536 plans. A check of all of them finds 81.47 mm as the minimum, 42 percent less travel than the careless plan. The good plan pierces each contour on the side that faces the next one.

## Known algorithms

- **Pierce points for a fixed order.** For a fixed order, the best pierce points are a shortest path in a layered graph: one layer per contour, one node per pierce point, and an arc of cost $d(p, q)$ between nodes of consecutive layers. With $k$ points per contour this takes $O(m k^2)$ time, as a [shortest path in a graph with no cycle](/dag-shortest-paths/). Many heuristics alternate this step with a change of the order.
- **Transformation to the TSP.** Noon and Bean (1993) turn a GTSP into an asymmetric TSP on the same nodes. Then any exact or heuristic TSP method applies. The precedence needs extra care in the transformed problem.
- **Construction and local search.** Nearest neighbor rules on the pierce points, with inner contours first, then 2-opt and other local moves (Hoeft and Palekar 1997).
- **Metaheuristics.** [Genetic algorithms](/genetic-algorithm/), [simulated annealing](/simulated-annealing/) and tabu search, which Dewil, Vansteenwegen and Cattrysse (2016) review.

There are no standard benchmarks for cutting sequence planning. Papers test their methods on nesting layouts of their own, so their numbers cannot be compared from paper to paper.

## Bounds

**NP-hardness.** The decision version is NP-hard by a reduction from the [Euclidean TSP](/euclidean-tsp/), which is NP-complete (Papadimitriou 1977): put a tiny contour at each city with the city as its only pierce point and no precedence, so the travel of a plan is the length of a tour through the cities with the home point at one of them. The problem with free pierce points and precedence contains this case, so all versions above are NP-hard.

**Easy parts.** For a fixed order, the pierce points are found in polynomial time, as above. So the hard part is the order.

**Approximation.** The GTSP with precedence has, in the cited sources, no approximation guarantee for general instances. Since the Euclidean TSP is the special case above, no version is easier than it.

## Reductions

- **From the Euclidean TSP.** As above.
- **To the GTSP.** A plan is a GTSP tour with precedence between clusters, as in the definition. The transformation of Noon and Bean then gives an asymmetric TSP.
- **Relation to operation sequencing.** With the tool fixed and only travel costs, [operation sequencing](/operation-sequencing/) is the case with one pierce point per contour.

## Applications

- **Laser, plasma, flame and water jet cutting.** Idle travel and the number of pierces are part of the cycle time of every sheet, and the cutting order also affects heat distortion and safety of the parts.
- **CAM for sheet metal.** The planner runs after [nesting](/nesting-problem/) and writes the cutting order and the lead-ins of each contour into the NC program.
- **Other path problems.** Engraving, drilling of printed circuit boards and pen plotters have the same structure: visit many shapes and choose where each one starts.

## References
