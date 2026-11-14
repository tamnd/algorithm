---
tag: AZSXZM
kind: problem
slug: disassembly-sequence-planning
name: Disassembly sequence planning
aliases:
- disassembly planning
- selective disassembly
area: cad/mechanism-and-assembly-design
level: core
summary: Find an order to remove all parts, or only a chosen part, from an assembly for maintenance and recycling, often by wave propagation or graph search.
prereqs: [assembly-sequence-planning, liaison-graph, breadth-first-search]
see_also: [assembly-partitioning, and-or-graph-of-assembly-plans, non-directional-blocking-graph, motion-space-assembly-planning, de-fazio-whitney-precedence-method, design-for-assembly, state-space-search, motion-planning]
sources:
  - paper: doi:10.1016/S0010-4485(98)00009-8
    title: Hari Srinivasan and Rajit Gadh, A geometric algorithm for single selective disassembly using the wave propagation abstraction, Computer-Aided Design 30(8), 603 to 613 (1998)
    locator: the removal of one target part, the waves of parts around it, and the order of removal
  - paper: doi:10.1109/70.54734
    title: Luiz S. Homem de Mello and Arthur C. Sanderson, AND/OR graph representation of assembly plans, IEEE Transactions on Robotics and Automation 6(2), 188 to 199 (1990)
    locator: assembly plans found by decomposition of the product, that is, by disassembly read in reverse
  - paper: doi:10.1177/027836499501400403
    title: Randall H. Wilson, Lydia E. Kavraki, Jean-Claude Latombe and Tomás Lozano-Pérez, Two-handed assembly sequencing, International Journal of Robotics Research 14(4) (1995)
    locator: assembly sequencing by disassembly under the monotone two-handed model
  - paper: doi:10.1016/0004-3702(94)90048-5
    title: Randall H. Wilson and Jean-Claude Latombe, Geometric reasoning about mechanical assembly, Artificial Intelligence 71(2), 371 to 396 (1994)
    locator: removable subassemblies from blocking graphs, the step of a disassembly
---

Disassembly sequence planning asks how to take a product apart: which parts or subassemblies come out first, along which motion, and in what order. The goal can be to take out every part, for recycling or a full overhaul, or to reach one part, for a repair, while removing as few other parts as possible. Each step must be possible: the piece that moves must leave without a collision. Under a motion model whose motions can be run backwards, disassembly is assembly in reverse: a feasible disassembly plan read backwards is a feasible assembly plan, and so most assembly planners work by disassembly. The two problems still differ in their goals and in joints that cannot be undone. This page states the problem, and the [assembly sequence planning](/assembly-sequence-planning/) page states the forward one.

## In plain words

To change a battery inside a device, you do not take every part out. You remove the cover, perhaps a board, and then the battery. A good plan removes few parts and uses easy motions.

A planner looks at each part and asks: can it come out now, or is something in the way? It removes the parts that are free, looks again, and stops when the part it wants is free. To take everything apart, it goes on until no part is left.

If every step of taking apart can be done backwards, then the same steps in the opposite order put the product together. So a plan to take a product apart is also a plan to build it.

## Definition

**Input.**

- An assembly $P$ of $n$ rigid parts in their final positions, with disjoint interiors, and its [liaison graph](/liaison-graph/).
- A **motion model**: the motions that a piece may make to leave. On this page the main model is one translation to infinity along a direction of a fixed set $M$.
- A **hand model**: *linear*, where each step removes one part from the rest, or *two-handed*, where each step splits a subassembly into two. Plans are *monotone*: a piece that is taken out is not put back, and a subassembly is not changed while it moves.
- Optionally, a target part $p^\ast$ or a set of targets, the rule that what remains must stay connected or stable, and a cost for each step.
- For recycling, a value for each part and a cost for each removal, and the set of joints that can only be broken, such as welds and glue.

**Output.** A plan. For full disassembly, a linear plan is an order in which all parts are removed, and a two-handed plan is a binary tree read from the root down. For a target, a sequence of removals that ends with $p^\ast$.

**Constraints.** At each step, the moving piece $S$ can leave the rest $R$ of its subassembly: for some allowed motion, no position along it puts a part of $S$ into the interior of a part of $R$.

**Objective.** Full disassembly: any feasible plan, or a cheapest one. A target: as few removals as possible, or least total cost. Recycling: the most value for the cost, where the plan may stop early.

## Variants

- **Full or partial.** Full disassembly takes out all parts. Partial disassembly stops when the targets are out, or when the value of the next part is less than its cost.
- **One target or many.** Taking out one target is the most common case in maintenance. Several targets share removals, so they should be planned together.
- **Nondestructive or destructive.** If a joint can be cut or broken, the cut part may be removed without a free motion. This changes the problem and breaks its link to assembly.
- **Linear or two-handed.** Removing a whole module in one step is often cheaper than taking it apart in place.
- **Motion model.** One translation along a few axes, as on this page, any one translation, as with the [non-directional blocking graph](/non-directional-blocking-graph/), or general motions found by a [motion planner](/motion-planning/).

## Examples

**The frame, with motion in its plane.** Take the frame of the [liaison graph](/liaison-graph/) page: base plate 0, posts 1 and 2, block 3 on the base between the posts, top plate 4 on the posts, all of the same depth. The motion model is one translation along $\pm x$ or $\pm z$, the hand model is linear, and what remains must stay connected.

- **Full disassembly.** Of the 120 removal orders, 64 are feasible. These are exactly the 64 feasible assembly orders read backwards, which the [De Fazio and Whitney](/de-fazio-whitney-precedence-method/) page counts.
- **Reaching the block.** In the full frame the block cannot move. The posts stop it along $\pm x$, the top plate along $+z$ and the base along $-z$. Each of the four other parts can come out first: the base along $-z$, the top plate along $+z$, the left post along $-x$ and the right post along $+x$. After that, the block leaves along the same direction. So the target needs one removal before it, and there are four such plans.
- **A third axis.** If the parts may also move along $\pm y$, the block slides out at once, with no other removal.

## Known algorithms

- **Assembly planners in reverse.** The [AND/OR graph](/and-or-graph-of-assembly-plans/) is built by splitting the product from the top, which is two-handed disassembly. The diagram of liaison states of De Fazio and Whitney, read backwards, gives the linear disassembly orders. Both are exact under their models.
- **Partitioning.** Repeated [assembly partitioning](/assembly-partitioning/) with the non-directional blocking graph or the [motion space approach](/motion-space-assembly-planning/) takes a product apart one split at a time. With one translation and no connection rule, a greedy choice of splits never gets stuck if any plan exists, because a set that can leave can still leave when fewer parts are in its way.
- **Search for a target.** A [breadth-first search](/breadth-first-search/) over the sets of removed parts, with an arc for each part that is free, finds a plan with the fewest removals before the target. It is exact and can visit $2^{n-1}$ states.
- **Wave propagation.** Srinivasan and Gadh (1998) order the parts around the target in waves, by which parts must come out before which, and remove them from the outside in. It is a geometric method designed for a short removal sequence in practice.
- **Metaheuristics.** For recycling with values and costs on large products, planners use [genetic algorithms](/genetic-algorithm/) and similar methods with no guarantee of optimality.

## Bounds

- **Search space.** There are $n!$ removal orders and $2^n$ sets of removed parts.
- **Polynomial cases.** One translation and no connection rule: a full plan is found in polynomial time by repeated partitioning, by the argument in the list above. For axis-aligned boxes and the axis directions, one part can always leave along any axis direction, so a full linear plan always exists without a connection rule.
- **Hardness.** Since a full two-handed disassembly starts with one split, the hardness results of [assembly partitioning](/assembly-partitioning/) apply: NP-completeness for planar assemblies when the motion is more than one translation (Kavraki, Latombe and Wilson 1993) and when both sides must be connected (Kavraki and Kolountzakis 1995). No hardness result for the fewest removals before one target is cited on this page.

The counts in the examples are computed and checked against all orders. The quality of wave propagation and of metaheuristics on real products is measured, not proved.

## Reductions

**Disassembly and assembly are reverses.** Take the monotone model in which each step moves one piece $S$, a single part or a subassembly, by one translation, and let $-M = \{-d : d \in M\}$.

*Claim.* A sequence of steps is a feasible disassembly plan with motions in $M$ if and only if the same steps in reverse order, each moving the same piece along $-d$ from far away into its place, form a feasible assembly plan with motions in $-M$. The sets present before and after each step are the same in both plans.

*Proof.* Let a disassembly step move $S$ out of the rest $R$ along $d$. It is feasible when $S + t d$ does not meet the interior of $R$ for any $t > 0$. The reverse step brings $S$ in along $-d$: it starts at $S + T d$ for a large $T$ and moves to $S$, through the positions $S + t d$ for $t$ from $T$ down to $0$. These are the same positions, so this motion is collision free exactly when the disassembly step is, and beyond $T$ the piece is far from $R$. In the reversed plan, the state before the assembly step is the state after the disassembly step, and the reverse. So each condition on states, such as connected or stable subassemblies, holds in one plan exactly when it holds in the other. Monotone plans move a piece only as one rigid body in both directions, so the steps match one to one. $\square$

The same proof works for any motion model whose motions can be run backwards, such as paths of several translations or general rigid motions, because a path and its reverse pass through the same positions. It does not hold for joints that can be made but not undone, for destructive steps, or when the stability of a part during its motion depends on its direction. The costs of the two plans can also differ, because tools and grips differ.

**To a shortest path.** For a target with the fewest removals, the states are the sets of removed parts and the arcs are free removals, so the problem is a shortest path in a [state space](/state-space-search/).

## Applications

- **Maintenance and repair.** A service manual lists which parts come out before a worn part, and a planner checks that the list is feasible and short.
- **Recycling and remanufacturing.** A disassembly plan decides which modules to take out for reuse and where to stop.
- **Design review.** A part that is hard to reach for service is a design problem, which [design for assembly](/design-for-assembly/) and similar reviews look for.
- **Assembly sequences.** Most assembly planners take the product apart in reverse, by the reduction above.

## References
