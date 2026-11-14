---
tag: F2PE1Y
kind: problem
slug: assembly-partitioning
name: Assembly partitioning problem
aliases:
- subassembly separation problem
area: cad/mechanism-and-assembly-design
level: advanced
summary: Decide whether some subset of parts can be removed as one rigid body without collision. Kavraki, Latombe and Wilson showed it NP-complete in the plane.
prereqs: [liaison-graph, configuration-space, np-complete]
see_also: [non-directional-blocking-graph, motion-space-assembly-planning, assembly-sequence-planning, and-or-graph-of-assembly-plans, disassembly-sequence-planning, strongly-connected-components, motion-planning, piano-movers-problem]
sources:
  - paper: doi:10.1016/0020-0190(93)90085-N
    title: Lydia E. Kavraki, Jean-Claude Latombe and Randall H. Wilson, On the complexity of assembly partitioning, Information Processing Letters 48(5), 229 to 235 (1993)
    locator: the statement of the partitioning problem and its NP-completeness for planar assemblies
  - paper: "Lydia E. Kavraki and Mihail N. Kolountzakis, Partitioning a planar assembly into two connected parts is NP-complete, Information Processing Letters 55(3), 159 to 165 (1995)"
    locator: the hardness when both subassemblies must be connected
  - paper: doi:10.1016/0004-3702(94)90048-5
    title: Randall H. Wilson and Jean-Claude Latombe, Geometric reasoning about mechanical assembly, Artificial Intelligence 71(2), 371 to 396 (1994)
    locator: the polynomial-time partitioning for one translation by the non-directional blocking graph
  - paper: doi:10.1007/s004539910025
    title: Dan Halperin, Jean-Claude Latombe and Randall H. Wilson, A general framework for assembly planning, the motion space approach, Algorithmica 26(3-4), 577 to 601 (2000)
    locator: partitioning for several families of motions by cells of constant blocking graph
  - paper: "B. K. Natarajan, On planning assemblies, Proceedings of the Fourth Annual Symposium on Computational Geometry, 299 to 308 (1988)"
    locator: the complexity of assembly with general motions
---

The assembly partitioning problem asks whether an assembly can be split in two by one motion: is there a nonempty proper subset of the parts that can move away as one rigid body, while the other parts stay, without a collision? It is the question of one step of a two-handed plan, read as a step of disassembly. Its difficulty depends on the motions allowed. For one translation it is solved in polynomial time by the [non-directional blocking graph](/non-directional-blocking-graph/), although there are $2^n - 2$ candidate subsets. Kavraki, Latombe and Wilson proved it NP-complete for planar assemblies when the motion is more general, and Kavraki and Kolountzakis proved it NP-complete when both sides must be connected. This page states the problem for one subassembly, while [assembly sequence planning](/assembly-sequence-planning/) asks for a whole plan made of such splits.

## In plain words

You hold a finished product. Can you pull some of its parts out together, as one piece, without bending anything and without hitting the parts that stay? The piece you pull can be one part or many parts at the same time.

For one straight pull, there is a fast method. Draw an arrow from each part to every part in its way, and look for a group with no arrow out. For pulls that can turn or change direction, no fast method is known, and the problem is as hard as the hardest puzzles of its class. If both the piece you pull and the piece you keep must each hang together, the problem is hard even for straight pulls.

## Definition

**Input.**

- A subassembly $A$ of rigid parts with disjoint interiors, which may touch.
- A **motion model**: a class of motions for a rigid body. Common classes are one small translation, one translation to infinity in a fixed set $M$ of directions or in any direction, a path of $k$ translations, and any collision-free path.
- A **hand model**: two-handed. One hand holds the moving set $S$, the other holds $A \setminus S$, and the parts of each side keep their relative positions.
- Optionally, the rule that $S$, or both $S$ and $A \setminus S$, must be connected in the [liaison graph](/liaison-graph/).

**Output.** A nonempty proper subset $S \subset A$ and a motion of the class that takes $S$ from its place to infinity, or to a position far from $A \setminus S$, with no collision. Or the answer that no such $S$ exists, in which case $A$ is *locked* for that class.

**Objective.** This is a decision problem with a witness. A planner may also want a set $S$ that is small, connected, stable, or cheap to move.

Only the relative motion of the two sides matters, so moving $S$ out of $A \setminus S$ and moving $A \setminus S$ out of $S$ along the reverse motion are the same split.

## Variants

- **Small translations.** $S$ only needs to start moving. This is a local test, and it is the first filter of most planners.
- **One translation to infinity.** $S$ leaves along one straight line. For a fixed direction, a set can leave exactly when no arc of the blocking graph leaves it.
- **Several translations.** $S$ follows a path of $k$ straight pieces. Some products need two or more pieces, for example a part that must move up out of a slot and then sideways.
- **General motion.** $S$ follows any path with rotations. This is a [motion planning](/motion-planning/) problem in the [configuration space](/configuration-space/) of $S$, a case of the [piano movers problem](/piano-movers-problem/) with the other parts as obstacles.
- **Connected sides.** $S$, or both sides, must be connected in the liaison graph, so that each side holds together.
- **Removal of one part.** $|S| = 1$. This is the step of a linear plan and of most [disassembly](/disassembly-sequence-planning/) planners.

## Examples

**The frame, with axis translations.** Take the frame of the [liaison graph](/liaison-graph/) page: base plate 0, posts 1 and 2, block 3 on the base between the posts, top plate 4 on the posts. All five parts have the same depth along $y$. Let $S$ leave by one translation to infinity along an axis direction.

- With all six directions, every one of the $2^4 - 1 = 15$ splits is possible, because any set of parts can slide out along $y$.
- In the plane, with $\pm x$ and $\pm z$ only, 13 splits are possible. The two that are not are $\{3\}$ against the rest, because the closed frame holds the block on all four sides, and $\{1, 2\}$ against $\{0, 3, 4\}$, because the block between the posts and the plates above and below them stop the two posts.
- Of the 13 splits in the plane, 11 have two connected sides. The split $\{0, 4\}$ against $\{1, 2, 3\}$ is possible along $\pm x$, since the two plates are free to slide, but the base and the top plate do not touch.

The [motion space approach](/motion-space-assembly-planning/) page lists these splits and its tests check them against all subsets.

**Three bars and small motions.** Three boxes that fill six cells of a $2 \times 2 \times 2$ cube, a column and two bars, each block the next along the directions of the octant $(+, -, +)$. For a small translation along such a direction, no subset can move, but other directions free single parts. The [non-directional blocking graph](/non-directional-blocking-graph/) page works this example.

## Known algorithms

- **Test all subsets.** Try each of the $2^{n-1} - 1$ splits with a motion test. This is exact and exponential.
- **Non-directional blocking graph.** For one small translation in any direction, Wilson and Latombe cut the sphere of directions into cells of constant blocking graph. In each cell, a removable set exists exactly when the graph is not strongly connected, and a sink component of the condensation is one. The whole test takes polynomial time. For axis-aligned boxes there are 26 cells and the test takes $O(n^2)$ time.
- **Motion space approach.** Halperin, Latombe and Wilson apply the same idea to other families of motion: cut the motion space into cells of constant blocking graph and use strong connectivity in each cell. All removable sets of a cell are the unions of components that no arc leaves, and they can be listed in $O(n)$ time each.
- **Motion planning.** For general motions, a planner in the configuration space of $S$ tests one candidate set. Since the number of candidate sets is exponential, practical planners first use the blocking graphs to select candidates.

## Bounds

- **Candidates.** There are $2^{n-1} - 1$ splits of $n$ parts. For a fixed direction, the sets that can leave can be all of them, so listing them can take exponential time, while finding one takes polynomial time.
- **Polynomial cases.** One translation, either small or to infinity, with no connection rule: polynomial time by blocking graphs (Wilson and Latombe 1994). For boxes and the six axis directions, the blocking graph along an axis has no cycle, so a single part can always leave along each axis direction, and an assembly of boxes is never locked under this model.
- **Hardness.** Kavraki, Latombe and Wilson (1993) proved that deciding whether a planar assembly of polygons can be partitioned is [NP-complete](/np-complete/) when the moving set is not limited to one translation. Kavraki and Kolountzakis (1995) proved that partitioning a planar assembly into two connected parts is NP-complete. Natarajan (1988) showed that planning an assembly with general motions is [PSPACE](/pspace/)-hard.

The polynomial bounds and the hardness results are proved. The speed of partitioning planners on real products is measured, and it depends on the products tested.

## Reductions

- **One step of a plan.** A two-handed plan exists only if the product can be partitioned, and every node of an [AND/OR graph](/and-or-graph-of-assembly-plans/) needs the list of its splits. So partitioning is the inner test of two-handed sequence planning.
- **From a fixed direction to a graph problem.** For one translation along a fixed direction, the sets that can leave are the sets with no arc out in the blocking graph, which the [strongly connected components](/strongly-connected-components/) give.
- **Monotone in obstacles.** If $S$ can leave $A \setminus S$ along one translation, then $S \cap B$ can leave $B \setminus S$ along the same translation for any $B \subseteq A$ that meets both sides, because fewer parts are in the way. This is why a greedy split never leads into a dead end under one translation without a connection rule.

## Applications

- **Two-handed assembly sequences.** Planners take a product apart by repeated partitioning and read the result backwards.
- **Design checks.** A locked subassembly in a design means that it cannot be built in the planned way, which the designer must know early.
- **Maintenance.** The question whether a module can come out as one piece is a partitioning question with the module as $S$.

## References
