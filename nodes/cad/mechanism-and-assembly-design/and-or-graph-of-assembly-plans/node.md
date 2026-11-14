---
tag: XTSFWX
kind: data-structure
slug: and-or-graph-of-assembly-plans
name: AND/OR graph of assembly plans
aliases:
- Homem de Mello-Sanderson AND/OR graph
area: cad/mechanism-and-assembly-design
level: core
summary: Homem de Mello and Sanderson's graph whose nodes are subassemblies and whose hyperarcs are feasible splits, which holds all assembly sequences compactly.
model: word-ram
complexity:
  vars:
    n: the number of parts
    N: the number of connected sets of parts
    C: the number of candidate splits tested (over all nodes)
  time:
    worst: O(C n^2)
  space:
    extra: O(N + C)
prereqs: [liaison-graph, hypergraph, directed-acyclic-graph]
see_also: [assembly-sequence-planning, de-fazio-whitney-precedence-method, non-directional-blocking-graph, motion-space-assembly-planning, disassembly-sequence-planning, assembly-partitioning, catalan-numbers, memoization]
sources:
  - paper: doi:10.1109/70.54734
    title: Luiz S. Homem de Mello and Arthur C. Sanderson, AND/OR graph representation of assembly plans, IEEE Transactions on Robotics and Automation 6(2), 188 to 199 (1990)
    locator: the AND/OR graph of an assembly, its solution trees as assembly plans, and the decomposition by cut-sets of the graph of connections
  - paper: "Luiz S. Homem de Mello and Arthur C. Sanderson, A correct and complete algorithm for the generation of mechanical assembly sequences, IEEE Transactions on Robotics and Automation 7(2), 228 to 240 (1991)"
    locator: the decomposition algorithm and its proof of correctness and completeness
  - paper: doi:10.1177/027836499501400403
    title: Randall H. Wilson, Lydia E. Kavraki, Jean-Claude Latombe and Tomás Lozano-Pérez, Two-handed assembly sequencing, International Journal of Robotics Research 14(4) (1995)
    locator: the monotone two-handed model and the generation of partitionings by translations
  - paper: doi:10.1109/JRA.1987.1087132
    title: Thomas L. De Fazio and Daniel E. Whitney, Simplified generation of all mechanical assembly sequences, IEEE Journal of Robotics and Automation 3(6), 640 to 658 (1987)
    locator: the diagram of assembly states, an equivalent representation of the same sequences
---

The AND/OR graph of an assembly, due to Homem de Mello and Sanderson, stores every way to build a product in a structure much smaller than the list of those ways. Its nodes are subassemblies, and a hyperarc goes from a subassembly to the two smaller subassemblies of each feasible way to split it. An assembly plan is a solution tree of the graph: take the whole product, choose one hyperarc, and continue in the same way in both children. The number of plans can grow like $n!$, but the graph has at most one node for each connected set of parts, and it gives the plan count, the best plan for a cost, and all plans by a recursion over its nodes.

## In plain words

Think about building a product backwards. Take the finished product and ask: in how many ways can I pull it into two pieces, each still in one piece itself, with one simple motion? Each answer is a fork in the road. Then ask the same question of each piece, and so on down to single parts.

Many different build orders share the same pieces. A plan that first makes the left half and a plan that first makes the right half both use the same "left half" piece. The AND/OR graph stores each piece once and keeps for it the list of its good splits. "OR" means you choose one split of a piece. "AND" means that after you choose it, you must build both halves.

To count all plans, count the plans of each piece once, from the small pieces up, and multiply along each split.

## The abstract type

A product has parts $P = \{1, \ldots, n\}$ and a [liaison graph](/liaison-graph/) $L$. The graph is built for a stated model:

- **Hand model: two-handed and monotone.** Each step takes two finished subassemblies and joins them with one motion. A part never moves again relative to the other parts of its subassembly. Each subassembly, except perhaps the whole product, must be connected in $L$. Linear sequences, which add one part at a time, are the special case where one side of every step is a single part.
- **Motion model on this page: one step translations.** A split $\{S_1, S_2\}$ is feasible if one side can leave the other by one translation to infinity along a direction of a fixed set $M$, here a subset of the six axis directions $\pm x, \pm y, \pm z$. The parts are axis-aligned boxes. Other motion models change only the test FEASIBLE, not the structure.

The structure is a directed [hypergraph](/hypergraph/) $G = (V, A)$:

- the nodes $V$ are the product $P$ and the connected subassemblies that can appear in a plan,
- a hyperarc $S \to \{S_1, S_2\}$ is an admissible split of $S$: $S_1$ and $S_2$ are connected and FEASIBLE($S_1$, $S_2$) holds,
- a *plan* (solution tree) below $S$ is $S$ itself if $|S| = 1$, and otherwise one hyperarc of $S$ with a plan below each side.

The operations are BUILD($P$), the hyperarcs of a node, PLANS($S$), the number of plans below $S$, the plans themselves one by one, and the best plan for a cost on the hyperarcs. Every hyperarc goes to strictly smaller sets, so the graph is a [directed acyclic graph](/directed-acyclic-graph/) of hyperarcs, and every recursion over it stops.

This page is the representation. The task of finding a sequence is the [assembly sequence planning](/assembly-sequence-planning/) problem, and the question of one split is [assembly partitioning](/assembly-partitioning/).

## Representation

A set of parts is a bit mask. The graph is a dictionary from a node to its list of hyperarcs, each a pair of masks $(S_1, S_2)$ where $S_1$ holds the lowest part of $S$. For the motion test, each direction $d \in M$ and each part $i$ has a mask $stop_d[i]$ of the parts that block $i$ when it moves along $d$. Then $S_1$ can leave $S_2$ along $d$ exactly when $stop_d[i] \cap S_2 = \emptyset$ for all $i \in S_1$. For boxes and an axis direction, $j$ blocks $i$ along $+x$ when their open $y$ and $z$ intervals overlap and $b_j$ lies at or beyond the right face of $b_i$.

## Operations

```pseudo id=main
BUILD(P)                                 ▷ P: all parts; M: the motion set
L1  arcs ← empty map; push P on a stack; until the stack is empty, pop S and DECOMPOSE(S)

DECOMPOSE(S)
L2  if S is a node already then return
L3  make S a node with no hyperarcs
L4  if |S| = 1 then return
L5  v ← the lowest part of S
L6  for each connected S1 with v ∈ S1 ⊊ S do      ▷ GROW of the liaison graph, inside S
L7      S2 ← S \ S1
L8      if S2 is connected and FEASIBLE(S1, S2) then
L9          add the hyperarc S → {S1, S2}; push S1 and S2

FEASIBLE(S1, S2)
L10 for each d in M: if no part of S1 is blocked along d by a part of S2, or no part of S2 is blocked along d by a part of S1, then return true
L11 return false

PLANS(S)                                 ▷ memoized
L12 if |S| = 1 then return 1
L13 return the sum over the hyperarcs S → {S1, S2} of PLANS(S1) · PLANS(S2)
```

**Splits once.** Every split has exactly one side that holds the lowest part $v$ of $S$, so line L6 meets each split exactly once. The enumeration is the GROW scheme of the liaison graph, restricted to $S$.

**Memoization.** Line L2 makes the graph share subassemblies. A set such as $\{0, 1, 3\}$ can come from many larger sets, but it is expanded once. PLANS uses the same idea, as in [memoization](/memoization/).

**Best plan.** Replace sum by minimum and product by sum in line L13, add a cost $c(S \to \{S_1, S_2\})$ for each hyperarc, and the recursion returns the cost of the cheapest plan: $\mathrm{BEST}(S) = \min (c + \mathrm{BEST}(S_1) + \mathrm{BEST}(S_2))$.

## Example

Take the frame of the [liaison graph](/liaison-graph/) page: base plate 0, left post 1, right post 2, block 3 between the posts on the base, top plate 4 on the posts, with liaisons $\{0,1\}, \{0,2\}, \{0,3\}, \{1,3\}, \{2,3\}, \{1,4\}, \{2,4\}$. The frame is a planar product, so let the parts move in its plane only: $M = \{+x, -x, +z, -z\}$.

The blocking relation along $+z$ is: the top plate blocks every part below it (1, 2, 3, and also 0), and the base plate blocks nothing. Along $+x$ the right post blocks the left post and the block, and the block blocks the left post. So the block is caught in the closed frame: the posts stop it along $\pm x$, the top plate along $+z$ and the base plate along $-z$. The split $\{\{0, 1, 2, 4\}, \{3\}\}$ is not feasible, and the frame without its block, $\{0, 1, 2, 4\}$, is not a node. The block must be in place before the top plate closes the frame.

The root has 12 splits into two connected sets, and 11 of them are feasible. The table gives each hyperarc with the plan counts of its two sides:

| hyperarc of the root | plans of the sides | product |
|---|---|---|
| $\{0\}$, $\{1,2,3,4\}$ | 1, 10 | 10 |
| $\{0,1\}$, $\{2,3,4\}$ | 1, 2 | 2 |
| $\{0,1,2,3\}$, $\{4\}$ | 12, 1 | 12 |
| $\{0,1,3\}$, $\{2,4\}$ | 3, 1 | 3 |
| $\{0,1,3,4\}$, $\{2\}$ | 8, 1 | 8 |
| $\{0,1,4\}$, $\{2,3\}$ | 2, 1 | 2 |
| $\{0,2\}$, $\{1,3,4\}$ | 1, 2 | 2 |
| $\{0,2,3\}$, $\{1,4\}$ | 3, 1 | 3 |
| $\{0,2,3,4\}$, $\{1\}$ | 8, 1 | 8 |
| $\{0,2,4\}$, $\{1,3\}$ | 2, 1 | 2 |
| $\{0,3\}$, $\{1,2,4\}$ | 1, 2 | 2 |

So PLANS(root) $= 54$. Inside $\{1, 2, 3, 4\}$, without the base plate, the block can drop out along $-z$, so the split $\{\{1,2,4\}, \{3\}\}$ is feasible there. The graph has 26 nodes (all 27 connected sets but $\{0,1,2,4\}$) and 58 hyperarcs. Of the 54 plans, 32 are linear, and each linear plan gives two part orders, because the first two parts can come in either order. So 64 of the 120 orders of the five parts are feasible linear sequences.

If all six directions are allowed, every connected set of the frame can slide out along $+y$, because all parts have the same $y$ interval. Then all 27 connected sets are nodes, all 65 splits into two connected sets are hyperarcs, and there are 64 plans.

## Correctness

Each split of a node has exactly one side that holds its lowest part, and the GROW scheme lists each connected set with that part once. So each node gets exactly one hyperarc for each admissible split. By induction on the size of a node, the solution trees below it are in one to one correspondence with the plans for it: the root hyperarc of a plan is a hyperarc of the graph, and the two subtrees are plans for its two sides. So the graph holds every monotone two-handed plan under the model once and nothing else, and the recursion of line L13 counts them. Every node other than the product is a side of an admissible split, so it is connected, and the graph has at most $N$ nodes when the product is connected. The full proofs are in [the correctness proof](proofs/correctness.md).

## Complexity

Let $c(S)$ be the number of connected sets inside $S$ that hold the lowest part of $S$. BUILD lists $c(S)$ candidates for each node and tests each one in $O(n^2)$ word operations with bit masks, so it costs $O(C\, n^2)$ for $n$ parts and a fixed motion set, where $C = \sum_S c(S)$ is the number of candidate splits. The graph has at most $N$ nodes and at most $\sum_S (c(S) - 1)$ hyperarcs. PLANS visits each node and hyperarc once.

| product | nodes | hyperarcs | plans |
|---|---|---|---|
| chain of $n$ parts, all splits feasible | $n(n+1)/2$ | $\binom{n+1}{3}$ | Catalan $C_{n-1}$ |
| all pairs in contact, all splits feasible | $2^n - 1$ | $(3^n - 2^{n+1} + 1)/2$ | $(2n-3)!!$ |
| the frame, $M = \{\pm x, \pm z\}$ | 26 | 58 | 54 |

For $n = 10$ parts that all touch, there are $(2n-3)!! = 34{,}459{,}425$ plans but only 1023 nodes and 28,501 hyperarcs. The [Catalan numbers](/catalan-numbers/) of the chain grow like $4^n$, and the chain has only $O(n^3)$ hyperarcs. The graph is still exponential in the worst case, because the number of connected sets is. It can also hold nodes with no plan below them, when a subassembly can be reached but not built, so a product with no plan at all can still have a large graph.

## Variants

- **Directed graph of assembly states.** For linear plans, a node can be a set of placed parts and an arc can add one part. De Fazio and Whitney draw the same states as sets of made liaisons in the [diagram of liaison sequences](/de-fazio-whitney-precedence-method/). The AND/OR graph holds the two-handed plans as well.
- **Other motion models.** FEASIBLE can test a single translation in any direction (with the [non-directional blocking graph](/non-directional-blocking-graph/)), a sequence of translations, or a general motion found by a [motion planner](/motion-planning/). The structure does not change. The [motion space approach](/motion-space-assembly-planning/) gives the feasible splits for a whole family of motions.
- **Stability and tools.** Real planners add tests to line L8: is each subassembly stable under gravity, can a gripper hold it, can a tool reach the joint. Each test removes hyperarcs.
- **Lazy search.** Instead of building the whole graph, a best first search from the root expands only the nodes that the cheapest partial plans reach. This is the AO* idea for AND/OR graphs.
- **Disassembly.** Read from the root down, a solution tree is a [disassembly](/disassembly-sequence-planning/) plan. A plan that takes out only one part uses only the path of nodes that hold that part.

## When to use it

Use the AND/OR graph when the planner needs all plans of a product with up to a few tens of parts: to count them, to pick the cheapest one under a cost such as the number of tool changes or reorientations, or to keep alternatives for a line balancing step. If one plan is enough, a direct [assembly partitioning](/assembly-partitioning/) search down one branch is cheaper. If only linear sequences are allowed, the precedence relations of [De Fazio and Whitney](/de-fazio-whitney-precedence-method/) are a more compact description when they exist.

## Pitfalls

- **Connected sets are an assumption.** Requiring each subassembly to be connected in the liaison graph is a model choice for stability. It removes plans in which a robot holds two loose parts together. State it.
- **Exponential size.** The number of connected sets grows exponentially for products with a central part, such as a base plate that touches all others. The graph is compact compared with the list of plans, not small.
- **Same node from many parents.** Without line L2, the same subassembly is expanded once for each parent, and the work grows like the number of plans.
- **Counting orders versus plans.** A linear plan matches two part orders, because the first two parts are joined in one step. A two-handed plan matches several orders of its steps. State which one a count means.
- **Planar products and the third axis.** A product drawn in a plane, with all parts of the same depth, can come apart along the depth axis in any order. The frame example has 64 plans with all six directions and 54 when motion is kept in the plane.

## Implementations

The Python module builds the graph from a list of boxes with integer or Fraction corners and a set of axis directions, or from an abstract liaison graph and any feasibility test. It counts plans and linear plans by memoized recursion and lists the plans. A shared helper holds the box predicates. The tests compare the set of plans with all full binary trees on the parts, each checked on the geometry with a sampled sweep test, for up to 5 parts and a few products of 6 parts; compare twice the number of linear plans with a check of all $n!$ orders; check that every node is a connected set; and check the chain and complete graph counts.

## History

Homem de Mello and Sanderson presented the AND/OR graph of assembly plans at AAAI in 1986 and in the IEEE Transactions on Robotics and Automation in 1990. In 1991 they gave the decomposition algorithm with a proof that it is correct and complete. De Fazio and Whitney (1987) gave the diagram of liaison states for linear sequences at the same time. Wilson, Kavraki, Latombe and Lozano-Pérez (1995) studied the two-handed monotone model for translations and showed how to generate the feasible partitions directly from the geometry, instead of testing each cut of the liaison graph.

## References
