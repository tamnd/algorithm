---
tag: RMGX71
kind: data-structure
slug: non-directional-blocking-graph
name: Non-directional blocking graph
aliases:
- NDBG
- Wilson-Latombe blocking graph
area: cad/mechanism-and-assembly-design
level: advanced
summary: Wilson and Latombe's arrangement of directional blocking graphs over the sphere of translations, which finds a removable subassembly in polynomial time.
model: word-ram
complexity:
  vars: {n: the number of parts}
  time: {worst: O(n^2)}
  space: {extra: O(n^2)}
prereqs: [directed-graph, strongly-connected-components, tarjan-scc]
see_also: [assembly-partitioning, assembly-sequence-planning, motion-space-assembly-planning, and-or-graph-of-assembly-plans, de-fazio-whitney-precedence-method, condensation-graph, line-arrangement, configuration-space]
sources:
  - paper: doi:10.1016/0004-3702(94)90048-5
    title: Randall H. Wilson and Jean-Claude Latombe, Geometric reasoning about mechanical assembly, Artificial Intelligence 71(2), 371 to 396 (1994)
    locator: the directional blocking graph, the non-directional blocking graph over the arrangement of great circles on the sphere of directions, and the strong connectivity test for a removable subassembly
  - paper: doi:10.1177/027836499501400403
    title: Randall H. Wilson, Lydia E. Kavraki, Jean-Claude Latombe and Tomás Lozano-Pérez, Two-handed assembly sequencing, International Journal of Robotics Research 14(4) (1995)
    locator: blocking graphs for one translation to infinity and their use to generate partitionings
  - paper: doi:10.1007/s004539910025
    title: Dan Halperin, Jean-Claude Latombe and Randall H. Wilson, A general framework for assembly planning, the motion space approach, Algorithmica 26(3-4), 577 to 601 (2000)
    locator: the blocking graph of each cell of a motion space, of which the NDBG is the case of small translations
  - paper: doi:10.1016/0020-0190(93)90085-N
    title: Lydia E. Kavraki, Jean-Claude Latombe and Randall H. Wilson, On the complexity of assembly partitioning, Information Processing Letters 48(5), 229 to 235 (1993)
    locator: the NP-completeness of assembly partitioning when the motion is not restricted to one translation
  - paper: "Lydia E. Kavraki and Mihail N. Kolountzakis, Partitioning a planar assembly into two connected parts is NP-complete, Information Processing Letters 55(3), 159 to 165 (1995)"
    locator: the hardness of partitioning when both subassemblies must be connected
---

The non-directional blocking graph (NDBG) of an assembly, due to Wilson and Latombe, answers one question for every direction at once: which sets of parts can move by a small translation in that direction while the other parts stay? For one direction $d$, the *directional blocking graph* $\mathrm{DBG}(d)$ has a node for each part and an arc $i \to j$ when part $j$ stops part $i$ from moving along $d$. A set $S$ can move exactly when no arc leaves $S$, so a removable set exists exactly when the graph is not strongly connected, and a sink component of its condensation is one. The graph changes only when $d$ crosses a great circle of the sphere of directions that is perpendicular to a contact plane. So the sphere falls into finitely many cells, with one graph per cell, and the NDBG is that list. For axis-aligned boxes there are 26 cells, and the whole structure costs $O(n^2)$.

## In plain words

Push one part of a machine a tiny bit in some direction. Some other parts are in the way. Draw an arrow from the part you push to each part in the way. If you want to move a group of parts together, no arrow may go from the group to a part outside it.

Now look for parts that stop each other in a ring: A stops B, B stops C, C stops A. Such a ring can only move as one group. Squeeze each ring into one dot. The arrows between the dots never form a ring, so some dot has no arrow out. That group can move.

The arrows depend on the push direction. But they change only when the direction crosses a few special lines. So you only need to check one direction from each region between those lines.

## The abstract type

The input is an assembly of $n$ rigid parts with disjoint interiors, which may touch. The structure is built for a stated model:

- **Motion model: one infinitesimal translation.** A set $S$ moves by $\varepsilon d$ for all small $\varepsilon > 0$. Rotations are not allowed, and a set that can make a small move may still collide later on its way out.
- **Hand model: two-handed.** One hand moves $S$ as one rigid body, and the other hand holds the rest of the subassembly. The parts of $S$ do not move relative to each other, and $S$ does not need to be connected.

The operations are:

- BUILD: the graph $\mathrm{DBG}(c)$ for each cell $c$ of the sphere of directions,
- CAN-MOVE$(S, c)$: can $S$ move along a direction of cell $c$?
- REMOVABLE$(c, A)$: a nonempty proper subset of a subassembly $A$ that can move along cell $c$, or none,
- SEPARATE$(A)$: a cell and a set that can move along it, or none if $A$ is locked.

## Representation

For general polyhedra, a contact between two parts with a contact plane of normal $\nu$ blocks the directions in a closed half sphere, and the border of that half sphere is the great circle perpendicular to $\nu$. The great circles of all contact planes cut the sphere into an arrangement of open cells of dimension 2, 1 and 0, as a [line arrangement](/line-arrangement/) cuts the plane. Each cell keeps one graph. With $r$ different contact planes there are $O(r^2)$ cells.

For axis-aligned boxes, every contact plane is perpendicular to an axis, so the great circles are the three coordinate planes. They cut the sphere into 8 open triangles, 12 open arcs and 6 points, 26 cells in all. A cell is named by the sign vector $s \in \{-1, 0, 1\}^3 \setminus \{0\}$ of its directions. Each graph is a list of $n$ bit masks: bit $j$ of $out_c[i]$ is set when $j$ blocks $i$ along cell $c$.

The test BLOCKED$(a, b, s)$ for two boxes looks at one axis at a time. On axis $k$ it is true when the open intervals of $a$ and $b$ overlap, or when the right end of $a$ touches the left end of $b$ and $s_k > 0$, or when the left end of $a$ touches the right end of $b$ and $s_k < 0$. Box $b$ blocks box $a$ when the test is true on all three axes. This rule also covers boxes that touch only along an edge or at a corner.

## Operations

```pseudo id=main
BUILD(parts)                             ▷ 26 cells for boxes
L1  for each cell s ∈ {−1, 0, 1}³ \ {0} do
L2      for each ordered pair (i, j) of distinct parts do
L3          if BLOCKED(part i, part j, s) then
L4              add the arc i → j to DBG(s)

CAN-MOVE(S, s, A)                        ▷ S ⊆ A, the parts of the subassembly
L5  return no arc of DBG(s) goes from a part of S to a part of A \ S

REMOVABLE(s, A)
L6  run Tarjan's algorithm on DBG(s) restricted to A
L7  C ← the first strongly connected component that it completes
L8  if C = A then return none            ▷ A is strongly connected along s
L9  return C                             ▷ C has no arc out

SEPARATE(A)
L10 for each cell s: if REMOVABLE(s, A) is a set C, then return (s, C); return none
```

**The first component.** [Tarjan's algorithm](/tarjan-scc/) completes a component only after every component that it can reach. So the first completed one is a sink of the [condensation graph](/condensation-graph/), and it has no arc out. No second pass over the condensation is needed.

**Subassemblies.** The graph of a subassembly $A$ is the graph of the product restricted to $A$, because blocking is a relation between two parts. So BUILD runs once, and REMOVABLE works for every node of an [AND/OR graph](/and-or-graph-of-assembly-plans/).

**All removable sets.** A set can move along $s$ exactly when it is a union of components that is closed under the arcs of the condensation. All such sets can be listed from the condensation, which is how the [motion space approach](/motion-space-assembly-planning/) uses the graphs.

## Example

Take three boxes that fill six of the eight unit cells of a $2 \times 2 \times 2$ cube:

| part | corners | shape |
|---|---|---|
| a | $(1,1,0)$ to $(2,2,2)$ | a column along $z$ |
| b | $(0,0,0)$ to $(2,1,1)$ | a bar along $x$ |
| c | $(0,0,1)$ to $(1,2,2)$ | a bar along $y$ |

Move along a direction of the cell $s = (+, -, +)$, for example $(1, -1, 1)$. Part a moves toward $-y$ and its face $y = 1$ lies on the face $y = 1$ of b, so b blocks a. Part b moves toward $+z$ and its top face lies on the bottom face of c, so c blocks b. Part c moves toward $+x$ and its face $x = 1$ lies on the face $x = 1$ of a, so a blocks c. The graph is the cycle $a \to b \to c \to a$, it is strongly connected, and no part and no pair can move along this cell. By the reverse rule, the cell $(-, +, -)$ has the reverse cycle. In the other 24 cells the graph has no cycle and some part can move: for example, along $+x$ the only arc is $c \to a$, and Tarjan's algorithm completes $\{a\}$ first. The 26 cells give 26 different graphs.

The frame of the [liaison graph](/liaison-graph/) page shows the limit of the model. Its block sits on the base between two posts, with a gap of one unit below the top plate. Along $+z$ the block can make a small move, so its set is free in $\mathrm{DBG}(+z)$. A translation to infinity along $+z$ is still blocked by the top plate. The frame has only 9 different graphs, because all its parts have the same $y$ interval and so the sign of $s_y$ does not change any arc.

## Correctness

For two boxes and a direction $d$, the moved box $a + \varepsilon d$ meets the interior of $b$ for all small $\varepsilon$ exactly when BLOCKED$(a, b, \mathrm{sign}(d))$ holds, and for no small $\varepsilon$ otherwise. This follows from a check of one axis at a time. So the graph is constant on each cell. A rigid set $S$ collides only when one of its parts meets a part outside it, so $S$ can move exactly when no arc leaves it. If the graph restricted to $A$ is strongly connected, every proper subset has an arc out along a path to a part outside it. If it is not, the first component that Tarjan's algorithm completes has no arc out. Every direction lies in one of the 26 cells, so SEPARATE answers for all directions. The full proofs are in [the correctness proof](proofs/correctness.md), which also shows that the six axis cells of a box product never have a cycle.

## Complexity

For boxes, BUILD tests $26 \cdot n(n-1)$ ordered pairs in $O(1)$ time each, which is $O(n^2)$ time, and stores 26 graphs of $n$ masks of $n$ bits, which is $O(n^2)$ space. Tarjan's algorithm costs $O(n + e)$ for $e$ arcs, so SEPARATE costs $O(n^2)$ for one subassembly. For polyhedra with $r$ contact planes, the arrangement has $O(r^2)$ cells and each graph costs $O(n^2)$ pairs of parts plus the contact tests, so the structure is polynomial in the size of the input. This is the main result of Wilson and Latombe: with one translation, a removable subassembly is found in polynomial time, even though there are $2^n - 2$ candidate sets.

The hardness results mark the edge of that result. If the moving set may follow any collision free path and not only one translation, deciding whether a proper subassembly can be removed is NP-complete for polygons in the plane (Kavraki, Latombe and Wilson, 1993). If both sides of a partition must be connected, partitioning a planar assembly is NP-complete (Kavraki and Kolountzakis, 1995). The [assembly partitioning](/assembly-partitioning/) page gives the details.

## Variants

- **One translation to infinity.** A set that can leave along $d$ is the same test with a different arc rule: $j$ blocks $i$ when the swept volume of $i$ along $d$ meets $j$. For boxes and the six axis directions this is a test of one axis at a time, and the graph along an axis has no cycle. The [motion space approach](/motion-space-assembly-planning/) uses these graphs.
- **Small rigid motions.** Wilson and Latombe also built the graph for small motions with rotation. The space of motions is then 6-dimensional, and the cells come from an arrangement of hyperplanes in it.
- **The motion space.** Halperin, Latombe and Wilson put the NDBG into a general frame: cut a space of motions into cells where the blocking graph does not change, then run the strong connectivity test in each cell.
- **Connected sides.** A planner that wants connected subassemblies must search among the closed unions of components for one whose sides are connected. This is the step that the hardness result of Kavraki and Kolountzakis is about.

## When to use it

Use the NDBG to answer the question of one partition for a polyhedral product, or to fill the hyperarcs of an [AND/OR graph](/and-or-graph-of-assembly-plans/) or the answers of the [De Fazio and Whitney method](/de-fazio-whitney-precedence-method/) from geometry. It is the right tool when parts touch along faces and the main question is which way each part can start to move. Use extended blocking graphs, or a motion planner, when a part must travel far through a cluttered product.

## Pitfalls

- **Small motion is not removal.** A set that is free in a cell may still hit another part farther along. The frame block can move up a little but cannot leave along $+z$. Use the infinitesimal graph to find candidates and confirm each one with a test of the full path.
- **Edge and corner contacts.** Two boxes that touch only along an edge can block each other in the off-axis cells. A test that looks only at face contacts misses those arcs.
- **The 1-cells and 0-cells.** A direction such as $+x$ lies on the border of four triangle cells, and its graph has only arcs that each of them also has, often fewer. Checking only the open triangles can miss a set that moves along an axis.
- **Floating point.** The cell of a direction is decided by exact equalities between coordinates. Use exact numbers, or snap contacts with a stated tolerance.
- **A disconnected answer.** The removable set may not be connected, and its complement may not be connected either. If the plan needs connected subassemblies, check that after the SCC test.

## Implementations

The Python module builds the 26 graphs for boxes with integer or Fraction corners as bit masks, and gives CAN-MOVE, Tarjan's algorithm, REMOVABLE and SEPARATE. A shared helper holds the box predicates. The tests compare the test BLOCKED with a real small step, on random products with face, edge and corner contacts and on random directions of each cell. They compare CAN-MOVE and REMOVABLE with a step of every subset of up to 6 parts in every cell, and SEPARATE with every subassembly. They also check the reverse cell rule, the invariance under a scale of the coordinates, and the example.

## History

Wilson and Latombe introduced the non-directional blocking graph in 1994. Their result changed the view of assembly partitioning: before it, planners tested cuts of the liaison graph one by one, which takes exponential time in the worst case. Wilson, Kavraki, Latombe and Lozano-Pérez used blocking graphs to generate two-handed sequences in 1995. Halperin, Latombe and Wilson generalized the idea to the motion space approach in 2000.

## References
