---
tag: 8VTFPV
kind: problem
slug: assembly-sequence-planning
name: Assembly sequence planning
aliases:
- assembly planning
area: cad/mechanism-and-assembly-design
level: core
summary: Find an order in which parts can be joined so that each step is collision-free and stable, and the plan is cheap, as the base of an assembly process plan.
prereqs: [liaison-graph, state-space-search, directed-acyclic-graph]
see_also: [and-or-graph-of-assembly-plans, de-fazio-whitney-precedence-method, non-directional-blocking-graph, motion-space-assembly-planning, assembly-partitioning, disassembly-sequence-planning, design-for-assembly, precedence-constrained-scheduling]
sources:
  - paper: doi:10.1109/70.54734
    title: Luiz S. Homem de Mello and Arthur C. Sanderson, AND/OR graph representation of assembly plans, IEEE Transactions on Robotics and Automation 6(2), 188 to 199 (1990)
    locator: assembly plans as solution trees of the AND/OR graph of subassemblies, and the count of plans
  - paper: doi:10.1109/JRA.1987.1087132
    title: Thomas L. De Fazio and Daniel E. Whitney, Simplified generation of all mechanical assembly sequences, IEEE Journal of Robotics and Automation 3(6), 640 to 658 (1987)
    locator: linear assembly sequences as orders of liaisons, generated from precedence relations
  - paper: doi:10.1177/027836499501400403
    title: Randall H. Wilson, Lydia E. Kavraki, Jean-Claude Latombe and Tomás Lozano-Pérez, Two-handed assembly sequencing, International Journal of Robotics Research 14(4) (1995)
    locator: the monotone two-handed model, plans by repeated partitioning, and the role of connected subassemblies
  - paper: doi:10.1016/0020-0190(93)90085-N
    title: Lydia E. Kavraki, Jean-Claude Latombe and Randall H. Wilson, On the complexity of assembly partitioning, Information Processing Letters 48(5), 229 to 235 (1993)
    locator: the NP-completeness of finding a removable subassembly in the plane
  - paper: "B. K. Natarajan, On planning assemblies, Proceedings of the Fourth Annual Symposium on Computational Geometry, 299 to 308 (1988)"
    locator: the complexity of deciding whether an assembly can be put together, and the PSPACE-hardness result
---

Assembly sequence planning asks how to build a product from its parts: in what order to join them, which parts or subassemblies meet at each step, and along which motion they come together. Each step must be possible: the moving piece must not collide with the parts already in place, and each subassembly must hold together. Among the possible plans the planner wants a cheap one, for example with few turns of the product, few tool changes or short reach. The answer is the base of an assembly process plan for a line or a robot cell. This page states the problem and its models, and the planners of this group solve parts of it: the [AND/OR graph](/and-or-graph-of-assembly-plans/) holds all two-handed plans, the [De Fazio and Whitney method](/de-fazio-whitney-precedence-method/) lists the linear ones from precedence rules, and the [non-directional blocking graph](/non-directional-blocking-graph/) and the [motion space approach](/motion-space-assembly-planning/) find the possible splits of one subassembly.

## In plain words

You have a box of parts and a picture of the finished product. You must find an order to put the parts together. Some orders do not work. If you put the lid on first, you cannot put anything inside. Some orders work but are slow, because the product must be turned over many times.

A planner tries orders and checks each step: can the new part reach its place without hitting other parts, and does the product hold together after the step? It is often easier to think backwards. Take the finished product apart in your head, one piece at a time. Each way to take it apart, read in reverse, is a way to build it.

## Definition

There is no one standard formal statement, because the models of motion and of hands change from paper to paper. The following version covers the cited work, with the choices named.

**Input.**

- Parts $P = \{1, \ldots, n\}$, each a rigid solid placed in its final position, with disjoint interiors.
- The [liaison graph](/liaison-graph/) $L$: one node per part and one liaison per contact or fastener.
- A **motion model**: the set of motions that a moving piece may make. Common choices are one translation to infinity along a direction from a fixed set $M$, one translation along any direction, a sequence of translations, or any collision-free rigid motion.
- A **hand model**: what a step may move. In the *linear* model, each step adds one part to one growing subassembly. In the *two-handed* model, each step joins two subassemblies, one held by each hand. A plan is *monotone* when no step moves a part relative to the other parts of its own subassembly, so no step undoes an earlier one.
- Extra conditions: each subassembly must be connected in $L$, stable under gravity, and reachable by the tools and grippers.
- A cost for each step, such as the cost of a turn of the product or of a change of tool.

**Output.** A plan. A linear plan is an order $p_1, \ldots, p_n$ of the parts. A two-handed plan is a binary tree whose leaves are the parts and whose inner nodes are subassemblies, each joined from its two children by one allowed motion.

**Constraints.** Each step is feasible: one side can move from far away into its final place relative to the other side by an allowed motion with no collision, and both sides meet the extra conditions.

**Objective.** The decision version asks whether a feasible plan exists. The search version asks for one plan. The optimization version asks for a plan of least total cost. The listing version asks for all feasible plans, for example to give a line designer a choice.

## Variants

- **Linear or two-handed.** Linear plans fit one fixture and one robot. Two-handed plans allow parallel work on subassemblies. Every linear plan is a two-handed plan whose steps each move one part.
- **Monotone or not.** Some products need a part to be moved to a temporary place and back. Nonmonotone plans are much harder to find, and most planners do not allow them.
- **Motion model.** The motion model decides the feasibility test of a step. The [non-directional blocking graph](/non-directional-blocking-graph/) covers one small translation in any direction, and the [motion space approach](/motion-space-assembly-planning/) covers other families of motion.
- **More hands.** A step can join three or more subassemblies at the same time. Some products cannot be built with two hands but can be built with more.
- **Disassembly.** [Disassembly sequence planning](/disassembly-sequence-planning/) asks for the reverse process, often for one part only, for repair or recycling.
- **Cost and line balance.** The plan can be chosen to balance the work between the stations of a line, which links the problem to [precedence-constrained scheduling](/precedence-constrained-scheduling/).

## Examples

**A frame of five boxes.** Part 0 is a base plate, parts 1 and 2 are left and right posts on it, part 3 is a block on the base between the posts, and part 4 is a top plate on the two posts. All parts have the same depth. Take the linear, monotone model with connected subassemblies, and let the parts move by one translation along $\pm x$ or $\pm z$, in the plane of the frame.

- Of the $5! = 120$ orders, 80 add at each step a part that touches a part already placed.
- An order with the block after the posts and the top plate fails: once 0, 1, 2 and 4 are in place, the block is closed in on all four sides. For example $0, 1, 2, 4, 3$ is not feasible, and $0, 3, 1, 2, 4$ is.
- The geometry removes 16 of the 80 connected orders, so 64 are feasible. They give 32 different liaison sequences, because the first two parts can come in either order.
- In the two-handed model there are 54 plans, of which 32 are linear. One plan that is not linear builds $\{0, 1, 3\}$ and $\{2, 4\}$ apart, then slides the right post with the top plate on it in from the right along $-x$.
- If the parts may also move along $\pm y$, out of the plane, all 80 connected orders are feasible, because every set of parts of the frame can slide out along $y$.

The [AND/OR graph](/and-or-graph-of-assembly-plans/) and [De Fazio and Whitney](/de-fazio-whitney-precedence-method/) pages compute these numbers, and their tests check them against all orders.

## Known algorithms

- **Generate and test.** Try all $n!$ orders, or all two-handed trees, and test each step. This is exact and works only for a few parts.
- **Precedence relations.** The [De Fazio and Whitney method](/de-fazio-whitney-precedence-method/) asks two questions per liaison and draws the diagram of liaison states. Under the linear monotone model with connected steps, its paths are exactly the feasible linear plans. Its size is at most the number of connected sets of parts.
- **AND/OR graph.** The [AND/OR graph of assembly plans](/and-or-graph-of-assembly-plans/) of Homem de Mello and Sanderson decomposes the product by the cut sets of its liaison graph. It holds every monotone two-handed plan with connected subassemblies exactly once, and it gives the count of plans and a cheapest plan by a recursion over its nodes. Homem de Mello and Sanderson proved the decomposition correct and complete in 1991.
- **Assembly by disassembly with blocking graphs.** Take the product apart by repeated [partitioning](/assembly-partitioning/). With one translation, the [non-directional blocking graph](/non-directional-blocking-graph/) finds a removable subassembly in polynomial time. In the monotone two-handed model with one translation and no connection rule, this greedy method is complete. If a plan exists, every subset $B$ of two or more parts can be split: the first step of the plan that separates parts of $B$ moves a set $S$, and $S \cap B$ can leave $B \setminus S$ along the same motion, since fewer parts are in its way. So the greedy method never meets a locked subassembly, and it makes $n - 1$ splits.
- **Search for a cheap plan.** Best-first and [A*](/a-star-search/) search over subassembly states, with a cost on each step, find a cheapest plan in the state graph. [Genetic algorithms](/genetic-algorithm/), [simulated annealing](/simulated-annealing/) and [ant colony optimization](/ant-colony-optimization/) are used on large products with no guarantee of optimality.

## Bounds

- **Search space.** There are $n!$ linear orders and $(2n-3)!!$ two-handed trees on $n$ labelled parts. The number of states, the connected sets of parts, is at most $2^n - 1$.
- **Boxes along axes.** For axis-aligned boxes, the graph of blocking along an axis direction has no cycle, so some part can always leave along any axis direction. Without a connection rule, a box product always has a linear plan, for example in the order of the left faces along $x$. The difficulty for boxes comes from the connection rule, the other conditions and the cost.
- **One translation in any direction.** Wilson and Latombe showed that a removable subassembly under one translation can be found in polynomial time. With the greedy argument above, a monotone two-handed plan with one translation per step and no connection rule is found in polynomial time.
- **Hardness.** Kavraki, Latombe and Wilson (1993) proved that deciding whether a planar assembly of polygons has a proper subassembly that can be removed is [NP-complete](/np-complete/) when the motion is not limited to one translation. Kavraki and Kolountzakis (1995) proved partitioning NP-complete in the plane when both sides must be connected. Natarajan (1988) proved that deciding whether a set of polyhedra can be assembled with general motions is [PSPACE](/pspace/)-hard.

These are proved results. Times of planners on real products are measured, not proved, and depend on the test product.

## Reductions

- **To disassembly.** When every motion of the model can be run backwards, a feasible assembly plan read backwards is a feasible disassembly plan, and the reverse. The [disassembly sequence planning](/disassembly-sequence-planning/) page proves this for one translation per step.
- **To a shortest path.** For linear plans, the states are the connected sets of placed parts, and a feasible step is an arc. A cheapest plan with costs on steps is a cheapest path from a single part to the full set, which [bitmask dynamic programming](/bitmask-dp/) solves in $O(2^n n)$ steps and tests.
- **To a partial order.** When the feasible orders are exactly those that respect a set of precedence pairs, a plan is a [topological sort](/topological-sort/) and the number of plans is a [count of linear extensions](/counting-linear-extensions/). Many products are not of this kind, since a part may be blocked only by a combination of other parts.
- **From partitioning.** A two-handed plan exists only if the product can be split once, so the hardness of [assembly partitioning](/assembly-partitioning/) carries over.

## Applications

- **Process planning for assembly.** The sequence decides the fixtures, the line layout and the robot programs.
- **Design review.** A product with no feasible sequence, or only bad ones, goes back to the designer. [Design for assembly](/design-for-assembly/) works on the same product before the sequence is planned.
- **Maintenance and recycling.** A disassembly plan that reaches one part tells a service team how much must come out first.
- **Robot assembly.** A robot cell needs the motions of each step, so the sequence planner feeds a [motion planner](/motion-planning/) for the final paths.

## References
