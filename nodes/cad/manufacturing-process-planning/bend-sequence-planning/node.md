---
tag: 8PNVFQ
kind: problem
slug: bend-sequence-planning
name: Bend sequence planning
aliases:
- bending sequence planning
area: cad/manufacturing-process-planning
level: core
summary: Order the bends of a sheet metal part on a press brake so no bend collides with the tools or the part, with few tool changes and regrips.
prereqs: [flat-pattern-development, state-space-search]
see_also: [a-star-bend-sequencing, collision-detection, bend-allowance, springback-compensation, computer-aided-process-planning, operation-sequencing, manufacturability-analysis, motion-planning]
sources:
  - paper: doi:10.1016/s0278-6125(98)80002-2
    title: S. K. Gupta, D. A. Bourne, K. H. Kim and S. S. Krishnan, Automated process planning for sheet metal bending operations, Journal of Manufacturing Systems 17(5), 1998, 338 to 360
    locator: the robotic press brake planner with a central operation planner and tooling, grasping and moving planners, the state-space search over partial bend sequences, and the costs of tool setups and regrips
  - paper: doi:10.1016/s0007-8506(07)62155-6
    title: M. Shpitalni and D. Saddan, Automatic determination of bending sequence in sheet metal products, CIRP Annals 43(1), 1994, 23 to 26
    locator: the bend sequence and the choice of tools stated together as a graph search problem
  - paper: doi:10.1115/1.2826245
    title: B. Radin, M. Shpitalni and I. Hartman, Two-stage algorithm for determination of the bending sequence in sheet metal products, Journal of Mechanical Design 119(2), 1997, 259 to 266
    locator: a first stage that finds a feasible sequence fast, and a second stage that looks for a cheaper one within a time limit, with costs from tool changes and handling
  - paper: doi:10.1016/0924-0136(94)90169-4
    title: L. J. de Vin, J. de Vries, A. H. Streppel, E. J. W. Klaassen and H. J. J. Kals, The generation of bending sequences in a CAPP system for sheet-metal components, Journal of Materials Processing Technology 41(3), 1994, 331 to 339
    locator: bend sequences that respect collisions and tolerances, with handling rules to guide the search
---

Bend sequence planning chooses the order in which a press brake makes the bends of a sheet metal part, and for each bend the tool, the side of the part that faces the operator, and whether the part is turned over. The part starts as a flat blank, the [flat pattern](/flat-pattern-development/), and each bend folds it along a line. A bend is possible only if the part, as it is at that moment, does not hit the punch, the die or the machine while it folds. So the order matters: a flange bent too early can block a later bend. Among the orders with no collision, the planner wants one with few tool changes, few turns of the part and few regrips, since these take most of the time at the machine. This problem page differs from [A* bend sequencing](/a-star-bend-sequencing/): this page states what a good bend order is, and that page is one method that searches the orders with A* and finds a cheapest one when its heuristic is admissible.

## In plain words

A press brake bends sheet metal with a long punch that presses the sheet into a groove, the die. Each bend makes the sheet a little more three-dimensional. A box with four sides needs its sides bent in some order, and after some bends the part may be shaped so that the next bend makes a side swing into the punch. That order does not work.

So the planner must find an order in which every bend is possible. Usually many orders work, and some are faster. A good order makes all bends that need one tool before it changes to the next tool, turns the part over as few times as it can, and lets the robot or the operator hold the part in one place for as many bends as possible.

## Definition

There is no standard formal statement of bend sequence planning. The following version covers the cited work.

**Input.**
- The part: its flat pattern and a set $B = \{b_1, \dots, b_n\}$ of bends, each with a bend line, an angle and a radius.
- The machine: the punch and die profiles, the back gauge, and the space around the tools.
- A tool library $T$. A tool fits a bend when its length, its die opening and its radius suit the bend and the flanges next to it.
- For a robotic cell, a gripper and the regrip station.
- Costs: the time of a tool change (or of a change between tool stations on the brake), of a turn of the part (over, or end for end), and of a regrip.

**The state after a set of bends.** Each bend, once done, is done fully, so the shape of the part after a set $S \subseteq B$ of bends does not depend on the order in which they were made. Write $P(S)$ for this shape.

**Feasible step.** Bend $b \notin S$ can be made next with tool $t$ and an orientation $o$ of the part if $t$ fits $b$, the motion of the part from $P(S)$ to $P(S \cup \{b\})$ with the bend line of $b$ on the die does not collide with the tools or the machine, and the part can be gauged and held in that position.

**Output.** An order $b_{\pi_1}, \dots, b_{\pi_n}$ of all bends, with a tool and an orientation for each, such that every step is feasible from the set of bends made before it.

**Objective.** Minimize the total time of the changes: tool changes, turns of the part and regrips, each counted between consecutive steps. The decision version asks only for a feasible order.

The choice of tool and of the bend order are coupled: Shpitalni and Saddan (1994) state the two together as one graph search problem, with the sets $S$ (and the last tool and orientation) as nodes.

## Variants

- **Feasibility only.** Find any order with no collision. This is the core of all versions.
- **Manual press brake.** The operator turns the part, so the costs are turns and tool changes.
- **Robotic press brake.** A robot holds the part, so each grip must stay valid over several bends, and a regrip costs time. Gupta, Bourne, Kim and Krishnan (1998) plan the bend order with a tooling planner, a grasping planner and a planner of robot motion.
- **Staged tooling.** Several tool sets stand along the brake in stages, and the plan chooses the stages and their layout as well as the order (Gupta, Bourne, Kim and Krishnan 1998).
- **Tolerances.** A bend adds an error to the dimensions that cross it, so the order and the choice of gauging faces decide which dimensions meet their tolerances (de Vin and others 1994).
- **Accuracy of each bend.** The flat length and the angle of each bend depend on the [bend allowance](/bend-allowance/) and on [springback compensation](/springback-compensation/). These do not change the order, but a planner that checks collisions needs the real formed shape.

## Examples

**A lipped channel.** A channel has a base of 6, two walls of 4 and two lips of 1, in any unit of length, and all four bends turn the same way: lip, wall, base, wall, lip. Call the bends $b_1$ (lip to wall), $b_2$ (wall to base), $b_3$ (base to wall) and $b_4$ (wall to lip). Two punches are available: a standard punch, which fits the short lips, and a narrow gooseneck punch, whose die needs flanges of at least 2, so it does not fit the lips.

- A lip must be bent before the wall next to it. If $b_2$ is done first, the base stands up at the far end of the wall, and when $b_1$ is made it swings into the punch. The same holds for $b_4$ and $b_3$.
- The second wall bend closes the channel, and the far wall and its lip swing over the punch. With the standard punch they collide, and with the narrow punch they do not.

So of the $4! = 24$ orders, the 6 with $b_1$ before $b_2$ and $b_4$ before $b_3$ are feasible, and each needs exactly one tool change, from the standard punch to the gooseneck before the second wall bend. An example is $b_1, b_2, b_4, b_3$, with the standard punch for the first three bends. The [A* bend sequencing](/a-star-bend-sequencing/) page models this part as a planar profile and checks the collisions exactly.

## Known algorithms

- **Search over the sets of done bends.** By the definition, a state is the set $S$ of done bends, with the last tool and orientation when the cost depends on them. A depth-first search with pruning finds a feasible order. A best-first search finds a cheap one.
- **A\* search.** [A* bend sequencing](/a-star-bend-sequencing/) searches the states with an estimate of the cost to finish. With an admissible estimate, it returns a cheapest order. Gupta, Bourne, Kim and Krishnan (1998) use A* with estimates from each specialized planner. For speed, they choose on purpose estimates that may be too high, so their plans are near optimal but not proved optimal.
- **Two stages.** Radin, Shpitalni and Hartman (1997) first find a feasible order fast, then look for a cheaper one until a time limit.
- **Rules.** Planners also use rules from the shop: bend the short and inner flanges first, and bend the flanges that would block the punch before the bends that close the part (de Vin and others 1994).

There are no standard benchmarks for bend sequence planning. Papers test their planners on parts of their own, so the results cannot be compared from paper to paper.

## Bounds

- **Search space.** There are $n!$ orders, and with $k$ tools and two orientations, $(2k)^n n!$ plans. The search over sets of done bends has $2^n$ sets, times the number of last tools and orientations.
- **Hardness.** No hardness result for bend sequence planning is known to the author of this page. The cited sources treat it as a combinatorial search and do not state its complexity.
- **Cost of one test.** Each feasibility test is a collision test of a moving part against the tools, so in practice the time of the search is the number of tests times the cost of one test.

## Reductions

- **To a shortest path problem.** With states $(S, \text{last tool}, \text{last orientation})$, a feasible step is an arc with the cost of the changes, and a cheapest plan is a cheapest path from $\emptyset$ to any state with $S = B$. This is the model that the A* page uses.
- **Relation to operation sequencing.** Like [operation sequencing](/operation-sequencing/), the cost depends on consecutive steps. Here the precedence is not given in advance: whether a bend can follow a set of bends is known only from the geometry.

## Applications

- **Process planning for sheet metal.** The bend order is the core of the plan for a press brake, and it is part of [computer-aided process planning](/computer-aided-process-planning/) for sheet metal.
- **Design feedback.** If no order is feasible, the part cannot be made on that brake with those tools. This is a [manufacturability](/manufacturability-analysis/) result that the designer can act on, for example by a shorter lip or a different flange order.
- **Robotic bending cells.** A full plan for a robotic cell also needs the grips and the robot motion, which come from the same search.

## References
