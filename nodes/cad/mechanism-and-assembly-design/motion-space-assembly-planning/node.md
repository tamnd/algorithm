---
tag: TCQ1T4
kind: algorithm
slug: motion-space-assembly-planning
name: Motion space approach to assembly planning
aliases:
- motion space assembly framework
area: cad/mechanism-and-assembly-design
level: research
summary: Halperin, Latombe and Wilson's framework that splits the space of subassembly motions into cells of constant blocking relations and searches it for separations.
solves: [assembly-partitioning]
model: word-ram
complexity:
  vars: {n: the number of parts of the subassembly, R: the number of removable sets in the output over the six directions}
  time: {worst: O(n^2 + n R)}
  space: {extra: O(n^2 + R)}
properties: {deterministic: true, recursive: true, exact: true}
history:
  year: 2000
  people: [Dan Halperin, Jean-Claude Latombe, Randall H. Wilson]
  note: They put the blocking graph methods for different kinds of motion into one frame, a space of motions cut into cells with one blocking graph each.
prereqs: [non-directional-blocking-graph, configuration-space, strongly-connected-components]
see_also: [assembly-sequence-planning, assembly-partitioning, and-or-graph-of-assembly-plans, disassembly-sequence-planning, tarjan-scc, condensation-graph, motion-planning, minkowski-sum]
sources:
  - paper: doi:10.1007/s004539910025
    title: Dan Halperin, Jean-Claude Latombe and Randall H. Wilson, A general framework for assembly planning, the motion space approach, Algorithmica 26(3-4), 577 to 601 (2000)
    locator: the motion space, the partition into regions of constant blocking graph, and the computation of removable subassemblies from the strongly connected components in each region
  - paper: doi:10.1016/0004-3702(94)90048-5
    title: Randall H. Wilson and Jean-Claude Latombe, Geometric reasoning about mechanical assembly, Artificial Intelligence 71(2), 371 to 396 (1994)
    locator: the non-directional blocking graph, the first case of the approach
  - paper: doi:10.1177/027836499501400403
    title: Randall H. Wilson, Lydia E. Kavraki, Jean-Claude Latombe and Tomás Lozano-Pérez, Two-handed assembly sequencing, International Journal of Robotics Research 14(4) (1995)
    locator: the generation of two-handed sequences from blocking graphs of translations
  - book: doi:10.1007/978-1-4615-4022-9
    title: Jean-Claude Latombe, Robot Motion Planning, Kluwer Academic Publishers (1991)
    locator: configuration space and the decomposition of a space into cells of constant behavior
---

The motion space approach of Halperin, Latombe and Wilson is a general method to find the subassemblies that can be taken out of an assembly. First choose a family of motions, such as all translations to infinity or all small rigid motions, and treat the family as a space. For each pair of parts, find the motions of that space along which one part hits the other. These sets cut the space into cells, and inside one cell the *blocking graph*, with an arc $i \to j$ when $j$ is in the way of $i$, does not change. In each cell, a set of parts can move exactly when no arc leaves it, so the removable sets are the closed unions of the strongly connected components of the cell's graph. The [non-directional blocking graph](/non-directional-blocking-graph/) is the case of small translations. This page implements one core step: the removable subassemblies along the six axis directions, where each direction is its own cell.

## In plain words

To take a machine apart, you must choose what to pull out and which way to pull it. There are many ways to pull. But two ways that are close together often hit the same parts. So group the ways to pull into regions where the same parts are in the way.

In one region, draw an arrow from each part to each part that stops it. A group of parts can come out when no arrow goes from the group to a part outside it. Parts that stop each other in a ring must come out together, so squeeze each ring into one dot. Then list every group of dots that no arrow leaves.

Do this for every region, and you know every group that can come out with that kind of pull.

## The problem

The input is a subassembly $A$ of rigid parts and a motion space $\mathcal{M}$. The output is every pair $(m, S)$ of a motion $m \in \mathcal{M}$, given by its cell, and a nonempty proper subset $S \subset A$ that can move along $m$ while $A \setminus S$ stays. The partitions of $A$ are the question of [assembly partitioning](/assembly-partitioning/). This page finds the separations of one subassembly, and the [assembly sequence planning](/assembly-sequence-planning/) problem chains such separations into a whole plan, for example in an [AND/OR graph](/and-or-graph-of-assembly-plans/).

The model of the implemented step is:

- **Motion model: one translation to infinity along an axis.** The motion space is the finite set $\{+x, -x, +y, -y, +z, -z\}$. Each direction is one cell.
- **Hand model: two-handed.** $S$ moves as one rigid body and $A \setminus S$ stays. Neither side needs to be connected.
- **Parts:** axis-aligned boxes with disjoint interiors, which may touch.

## The algorithm

The approach has five steps. The implemented one is step 4.

1. Choose the motion space $\mathcal{M}$.
2. For each ordered pair of parts $(i, j)$, compute the set $B_{ij} \subseteq \mathcal{M}$ of motions along which part $i$ meets part $j$. For translations to infinity, these are the directions $d$ for which the ray from the origin along $d$ meets the [Minkowski difference](/minkowski-sum/) of $j$ and $i$.
3. Compute the arrangement of the borders of all $B_{ij}$. In each cell, the blocking graph is constant.
4. For each cell, build the blocking graph, compute its strongly connected components, and list the closed sets.
5. Use the closed sets to answer a partitioning query, or to fill the hyperarcs of an AND/OR graph.

For the six axis directions, steps 1 to 3 are trivial, and step 4 is:

```pseudo id=main
REMOVABLE-SETS(A)                        ▷ A: a subassembly; M: the six axis directions
L1  for each direction d ∈ M do          ▷ each direction is one cell
L2      for each ordered pair (i, j) of distinct parts of A do
L3          if j blocks i along d then add the arc i → j to G_d
L4      C_0, …, C_{k−1} ← the components of G_d in the order Tarjan's algorithm completes them
L5      succ[t] ← the parts outside C_t that an arc from C_t reaches, for each t
        EXTEND(0, ∅)

EXTEND(t, chosen)                        ▷ chosen: a union of C_0, …, C_{t−1}
L6  if t < k then go to L8
L7  output chosen as a set that leaves along d, if chosen ≠ ∅ and chosen ≠ A; return
L8  EXTEND(t + 1, chosen)                ▷ C_t stays
L9  if succ[t] ⊆ chosen then EXTEND(t + 1, chosen ∪ C_t)      ▷ C_t moves
```

**The blocking test.** Box $j$ blocks box $i$ along $+x$ when their open $y$ intervals overlap, their open $z$ intervals overlap, and $j$ lies at or beyond the right face of $i$. The other directions are the same with other axes and signs.

**Why the order of Tarjan's algorithm.** [Tarjan's algorithm](/tarjan-scc/) completes a component only after every component that it reaches. So when EXTEND decides on $C_t$, it has already decided on every component that $C_t$ points to, and the test of line L9 is final. Every path of calls ends in a valid set, and no call is wasted.

## Example

Take the frame of the [liaison graph](/liaison-graph/) page: base plate 0, left post 1, right post 2, block 3 on the base between the posts, top plate 4 on the posts. All parts have the same $y$ interval. The blocking graphs are:

| direction | arcs | removable sets |
|---|---|---|
| $+x$ | $1 \to 2$, $1 \to 3$, $3 \to 2$ | 14 |
| $-x$ | $2 \to 1$, $2 \to 3$, $3 \to 1$ | 14 |
| $+y$, $-y$ | none | 30 each |
| $+z$ | $0 \to 1, 2, 3, 4$; $1 \to 4$; $2 \to 4$; $3 \to 4$ | 8 |
| $-z$ | $4 \to 0, 1, 2, 3$; $1 \to 0$; $2 \to 0$; $3 \to 0$ | 8 |

Along $+z$, a set that holds the base must hold all parts above it, so it is all of $A$. A set without the base can leave exactly when it holds the top plate. Any subset of $\{1, 2, 3\}$ can go with it, which gives $2^3 = 8$ sets. Along $+x$, the parts 0 and 4 have no arcs and are free to join any set, and the closed subsets of $\{1, 2, 3\}$ are $\emptyset$, $\{2\}$, $\{2, 3\}$ and $\{1, 2, 3\}$. That gives $4 \cdot 4 = 16$ closed sets, and 14 without $\emptyset$ and $A$. Along $\pm y$ every one of the $2^5 - 2 = 30$ sets can leave.

Read as splits, the four directions in the plane of the frame give 13 of the 15 splits of the frame into two sets. The two splits that are missing are $\{0, 1, 2, 4\}$ against $\{3\}$, because the closed frame holds the block, and $\{0, 3, 4\}$ against $\{1, 2\}$. In the second one, the two posts cannot move together along $\pm x$ because the block is between them, and the base and the top plate stop them along $\pm z$. Of the 13 splits, 11 have two connected sides, and these are the 11 hyperarcs of the root in the AND/OR graph example. With the $\pm y$ directions, all 15 splits are possible.

## Correctness

Box $j$ blocks box $i$ along an axis direction exactly when $i$ hits $j$ for some distance of travel, which follows from a test on one axis. A rigid set $S$ collides only when one of its parts hits a part outside it, so $S$ can leave exactly when no arc of $G_d$ leaves $S$. Such a closed set is a union of components. Because the components come in the order of Tarjan's algorithm, the test of line L9 is final when it is made, so the recursion outputs every closed set except $\emptyset$ and $A$ once, and nothing else. For boxes and an axis direction, an arc always goes to a part with a larger lower coordinate on that axis, so $G_d$ has no cycle and each component is one part. The full proofs are in [the correctness proof](proofs/correctness.md).

## Complexity

For a subassembly of $n$ parts, lines L2 and L3 test $n(n-1)$ pairs in $O(1)$ time each, and Tarjan's algorithm and line L5 take $O(n^2)$ time. Each call of EXTEND has a child at line L8, so the recursion tree has at most $n (R_d + 2) + 1$ calls for $R_d$ output sets. Over the six directions the step costs $O(n^2 + n R)$ time, which is $O(n)$ for each output set after the graphs are built. The output can be exponential: along $\pm y$ the frame has $2^n - 2$ removable sets.

For general motion spaces, the cost of the whole approach is the cost of the arrangement of step 3 times the cost of step 4 per cell. The number of cells depends on the motion space and the shapes. For small translations of polyhedra it is quadratic in the number of contact planes, as on the NDBG page. For larger motion spaces the arrangement grows much faster, and [assembly partitioning](/assembly-partitioning/) with general motions is NP-complete.

## Properties

- **Exact for its motion space.** The lists hold every removable set for the chosen motions, and only those. A set that needs a motion outside the space, such as a turn or two steps of translation, is not found.
- **Not connected by default.** A removable set or its complement can be disconnected. A planner that needs connected subassemblies filters the output.
- **Output sensitive.** After the graphs are built, each removable set costs $O(n)$.
- **Shared work.** The pair tests of step 2 depend only on the two parts, so the graphs of a subassembly are the graphs of the product restricted to it.

## Variants and improvements

- **Small translations.** The motion space is the sphere of directions with small motions. Step 3 gives the arrangement of great circles of the [non-directional blocking graph](/non-directional-blocking-graph/).
- **Translations to infinity in any direction.** The blocking sets are the directions that meet the Minkowski differences of pairs of parts, and step 3 is an arrangement of curves on the sphere. The axis directions of this page are 6 of its points.
- **Small rigid motions.** Translations and rotations together give a 6-dimensional motion space. The blocking sets come from linear constraints at each contact.
- **One part at a time.** A linear planner keeps only the sets of one part, which are the sinks of the condensation, as the [De Fazio and Whitney method](/de-fazio-whitney-precedence-method/) needs.
- **Disassembly.** For [disassembly sequence planning](/disassembly-sequence-planning/), the same lists give the first step of each plan, and the rest follows by recursion on both sides.

## When to use it

Use the approach when the motions of a product fit a family with a clear geometry: translations along a few fixed axes, as for many boxed or machined products, or small motions to test for local locks. The axis case of this page is cheap and exact, and it fills an AND/OR graph without a test of every split. When parts need long paths with turns, use a [motion planner](/motion-planning/) on the few candidates that the approach leaves.

## Pitfalls

- **The motion space must be stated.** The same product can be separable under one space and locked under another. In the frame, the block is free along $\pm y$ and caught in the plane.
- **Infinitesimal is not extended.** A set that can make a small move may still hit a part on its way out. Do not mix the graphs of the two spaces.
- **Lists can be huge.** For a product whose parts are free along one direction, every subset is removable. Ask for the sinks only, or for one set, when the full list is not needed.
- **Touching at the end.** A part that ends exactly at the face of another part along the direction of motion is blocked by it. A test with a strict inequality there misses contacts.
- **Cells of lower dimension.** In a continuous motion space, the borders of the cells are cells too, and their graphs can have fewer arcs. A method that samples only open cells misses them.

## Implementations

The Python module computes the blocking graphs along the six axis directions for boxes with integer or Fraction corners, lists the removable sets of a subassembly for each direction, and turns them into splits. A shared helper holds the box predicates. The tests compare the lists with a test of every subset of every subassembly of up to 5 parts, and of the whole product for 6 parts, each subset swept out along the direction at small steps. They also compare the enumeration of closed sets with all subsets on random directed graphs with cycles, and check the splits, the absence of cycles along an axis, a scale of the coordinates, and the frame.

## History

Wilson and Latombe introduced the non-directional blocking graph for small translations in 1994. Wilson, Kavraki, Latombe and Lozano-Pérez used blocking graphs of translations to generate two-handed sequences in 1995. Halperin, Latombe and Wilson published the motion space approach in Algorithmica in 2000. It showed that these methods, and others for richer motions, follow one scheme: cut the motion space into cells of constant blocking graph and use strong connectivity in each cell.

## References
