---
tag: R5X3KJ
kind: algorithm
slug: flowmap
name: FlowMap
aliases:
- Cong-Ding FlowMap
area: cad/logic-synthesis
level: core
summary: Cong and Ding's depth-optimal k-LUT mapping that labels nodes in topological order, finding a k-feasible cut of least height by a max-flow test.
solves: [lut-mapping]
model: word-ram
complexity:
  vars: {n: the number of nodes, m: the number of edges, K: the number of inputs of a LUT}
  time: {worst: O(K m n)}
  space: {extra: O(m)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1992
  people: [Jason Cong, Yuzheng Ding]
  note: Cong and Ding gave FlowMap at ICCAD 1992 and in IEEE TCAD in 1994, the first polynomial-time algorithm that maps a general K-bounded network into K-input LUTs with the least depth.
prereqs: [lut-mapping, k-feasible-cut, max-flow-min-cut-theorem, vertex-capacities-flow]
see_also: [cut-enumeration, priority-cuts, menger-theorem, edmonds-karp, ford-fulkerson, technology-mapping, tree-covering-technology-mapping, static-timing-analysis]
sources:
  - paper: "Jason Cong and Yuzheng Ding, FlowMap, an optimal technology mapping algorithm for delay optimization in lookup-table based FPGA designs, IEEE Transactions on Computer-Aided Design 13(1), 1 to 12, 1994"
    title: FlowMap, an optimal technology mapping algorithm for delay optimization in lookup-table based FPGA designs
    locator: the labeling phase, the network with t and the nodes of label p merged, the node-split flow network, the O(K m n) bound, and the proof of depth optimality for K-bounded networks
  - paper: "Jason Cong and Yuzheng Ding, An optimal technology mapping algorithm for delay optimization in lookup-table based FPGA designs, Proceedings of the IEEE/ACM International Conference on Computer-Aided Design (ICCAD 1992), pages 48 to 53"
    title: An optimal technology mapping algorithm for delay optimization in lookup-table based FPGA designs
    locator: the conference version of the algorithm (general locator)
  - paper: "Amir H. Farrahi and Majid Sarrafzadeh, Complexity of the lookup-table minimization problem for FPGA technology mapping, IEEE Transactions on Computer-Aided Design 13(11), 1319 to 1332, 1994"
    title: Complexity of the lookup-table minimization problem for FPGA technology mapping
    locator: the NP-completeness of LUT mapping with the fewest LUTs, the contrast with depth (general locator)
---

FlowMap maps a [Boolean network](/boolean-network/) into $K$-input lookup tables (LUTs) so that the longest chain of LUTs from an input to an output is as short as possible. It is the depth version of [LUT mapping](/lut-mapping/). The network must be $K$-bounded: every gate has at most $K$ fanins. FlowMap gives each node a label, the least depth of a LUT that computes the node, in topological order. The label of a gate $t$ is either $p$ or $p + 1$, where $p$ is the largest label of a fanin. It is $p$ exactly when a [$K$-feasible cut](/k-feasible-cut/) of $t$ separates $t$ and all nodes of label $p$ from the inputs, and a max-flow computation on a network with unit node capacities tests this. Cong and Ding (1992, 1994) proved that the labels are the least possible depths, so the mapping is depth-optimal, in $O(K m n)$ time. Before FlowMap, depth-optimal mapping was known only for trees.

## In plain words

An FPGA builds logic from small tables. Each table takes up to $K$ wires and can compute any function of them. You must cut a circuit of small gates into such tables. Each signal passes through a chain of tables, and you want the longest chain to be short, because each table adds delay.

Work from the inputs. For each gate, look at the gates that feed it and take the worst depth among them. The gate can reach that same depth only if one table can hold the gate together with every feeding gate at the worst depth, and that table needs at most $K$ wires in. A flow test on the graph answers this: it finds the fewest wires that separate the gate from the inputs. If the answer is too many, the gate gets one more level. At the end, build tables from the outputs back.

## The problem

The input is a $K$-bounded network $N$ with $n$ nodes and $m$ edges, a directed acyclic graph whose sources are the primary inputs (PIs), and a set of output nodes. A *mapping* gives each node $v$ that it needs a LUT whose inputs form a $K$-feasible cut $C_v$ of $v$, with $v \notin C_v$. The LUT computes $v$ from $C_v$, which is possible because a node is a function of each of its cuts. The LUT inputs that are gates need LUTs too. A gate can be covered by several LUTs, so logic may be duplicated. Under the unit delay model, the depth of a mapping is the largest number of LUTs on a path from a PI to an output. The task is a mapping of least depth.

Let $N_t$ be the cone of $t$, the nodes from which $t$ can be reached. Let $d(t)$ be the least depth of a LUT for $t$:
$$d(t) = 0 \text{ for a PI}, \qquad d(t) = \min_{C} \Big(1 + \max_{u \in C} d(u)\Big),$$
where $C$ ranges over the $K$-feasible cuts of $t$ that do not contain $t$. A mapping that uses at each node a cut that reaches this minimum has depth $\max_o d(o)$ over the outputs $o$, and no mapping has less, since the LUT inputs of $t$ in any mapping form such a cut. FlowMap computes $d$ without listing the cuts.

## The algorithm

```pseudo id=main
FLOWMAP(N, K, outputs)
L1  ℓ(v) ← 0 for each primary input v
L2  for each gate t in topological order do
L3      p ← the largest label ℓ(u) of a fanin u of t
L4      if p = 0 then ℓ(t) ← 1; C_t ← the fanins of t; continue
L5      N' ← the cone N_t with t and every node of label p merged into one sink t'
L6      F ← N' with each other node w split into w_in → w_out of capacity 1, the other edges of capacity ∞, and a source s with an edge of capacity ∞ into each PI
L7      if the max flow from s to t' in F is at most K then
L8          ℓ(t) ← p; C_t ← the nodes w with w_in reachable from s in the residual graph and w_out not reachable
L9      else
L10         ℓ(t) ← p + 1; C_t ← the fanins of t
L11 L ← the outputs that are gates; S ← ∅
L12 while L holds a gate t ∉ S do
L13     add a LUT for t with the inputs C_t to S; add the gates of C_t to L
L14 return ℓ and S
```

Lines L1 to L10 are the labeling phase and lines L11 to L14 the mapping phase. At line L4 all fanins are PIs, so the fanins form a cut of depth 1. Line L7 does not need the whole max flow: the code of this page stops after $K + 1$ augmenting paths of a breadth-first [augmenting path](/augmenting-path-flow/) search, as in [Edmonds-Karp](/edmonds-karp/). The split of line L6 turns a node cut into an edge cut, as on the [vertex capacities](/vertex-capacities-flow/) page. A merged node is not split, so it can never be in the cut.

## Example

Take $K = 3$, inputs $a, b, c, d, e$ and the gates $f = (a, b)$, $g = (b, c)$, $h = (c, d)$, $i = (f, g)$, $j = (g, h)$ and $o = (i, j, e)$, with $o$ the output. Node $g$ feeds both $i$ and $j$.

| gate | $p$ | merged into $t'$ | max flow | label | $C_t$ |
|---|---|---|---|---|---|
| $f, g, h$ | 0 | | | 1 | the fanins |
| $i$ | 1 | $i, f, g$ | 3: through $a$, $b$, $c$ | 1 | $\{a, b, c\}$ |
| $j$ | 1 | $j, g, h$ | 3: through $b$, $c$, $d$ | 1 | $\{b, c, d\}$ |
| $o$ | 1 | $o, f, g, h, i, j$ | 5: through $a$, $b$, $c$, $d$, $e$ | 2 | $\{i, j, e\}$ |

At $o$, each of the five inputs has its own edge into a merged node, so 5 node-disjoint paths reach $t'$, and the code stops after the fourth. The mapping phase starts at $o$ and makes three LUTs: $o$ over $\{e, i, j\}$, $i$ over $\{a, b, c\}$ and $j$ over $\{b, c, d\}$. The depth is 2. Gate $g$ is inside the LUTs of both $i$ and $j$, so it is duplicated. Without duplication, $g$ needs its own LUT, then $i$ or $j$ has depth 2 and $o$ has depth 3. The test file checks this example with a brute force over all $K$-feasible cuts of each node.

## Correctness

The [full proof](proofs/correctness.md) shows that $\ell(t) = d(t)$ for every node, by induction in topological order. Three facts carry it. First, $d$ is monotone along the cone: if $u$ is in the cone of $t$, then $d(u) \le d(t)$. With the fanin cut, this gives $p \le d(t) \le p + 1$. Second, $d(t) = p$ exactly when some cut of $t$ with at most $K$ nodes has only nodes of label below $p$, and by monotonicity such a set is a cut of $t$ exactly when it meets every path from a PI to a node of $N'$ that was merged into $t'$. Third, by the [max-flow min-cut theorem](/max-flow-min-cut-theorem/) with unit node capacities, that set exists exactly when the max flow at line L7 is at most $K$, and the residual reachability of line L8 gives one. The mapping phase then builds, for each LUT root $t$, a LUT of depth $\ell(t)$, so the depth is $\max_o d(o)$, the least possible.

## Complexity

At a gate $t$, the network $F$ has $O(|N_t|)$ nodes and $O(m)$ edges. One augmenting path costs $O(m)$ time by breadth-first search, and line L7 needs at most $K + 1$ of them, so a gate costs $O(K m)$ and the labeling phase $O(K m n)$. The mapping phase visits each LUT root once and costs $O(K n)$. The flow network of one gate takes $O(m)$ space. On circuits, the cones are much smaller than the whole network for most gates, so the run time is far below the bound.

## Properties

**What is proved.** For a $K$-bounded network under the unit delay model, with duplication allowed, the mapping has the least depth among all mappings into $K$-input LUTs of the given network structure. Each label is the least depth of a LUT for its node, and the labels never decrease along paths. The algorithm runs in polynomial time.

**What is not proved.** The number of LUTs is not optimized. Finding a mapping with the fewest LUTs is NP-hard (Farrahi and Sarrafzadeh 1994), and FlowMap often duplicates logic to save depth. The optimum is only over mappings of the given structure: a different decomposition of the same functions into $K$-bounded gates can allow a smaller depth. The result does not hold for a network that is not $K$-bounded without first splitting its large gates, and the depth then depends on the split.

**What is measured.** The test file compares the labels with the brute-force $d$ on 500 random networks with up to 6 inputs, 14 gates and $K$ from 2 to 4 (seed 5), and compares the mapping depth with an exhaustive search over every choice of one cut per gate on 40 networks with $K = 3$ (seed 9). These are checks of the code, not benchmark results. Cong and Ding report results on benchmark circuits in their paper.

## Variants and improvements

- **Area recovery.** After labeling, each node has a required time from the depth bound. A mapper can then choose, among the cuts that meet the required times, cuts that need fewer LUTs, for example cuts that do not duplicate logic. Later mappers do this with area flow and exact area, as in [priority cuts](/priority-cuts/).
- **Depth relaxation.** Relax the depth bound on paths that are not critical and use the slack to save LUTs. Cong and Ding studied this trade-off between depth and area after FlowMap.
- **Cut enumeration instead of flow.** With all cuts listed by [cut enumeration](/cut-enumeration/), a dynamic program over the cuts gives the same labels, and it can handle other costs. For $K = 6$ and large circuits, [priority cuts](/priority-cuts/) keep the dynamic program fast, at the cost of the proof.
- **Retiming.** Pan and Lin (1998) and others extend the labels to sequential circuits, so that mapping and [retiming](/retiming/) are done together.

## When to use it

Use FlowMap when the depth of a LUT network matters and a proof of optimality for the given structure is wanted, or as a reference for testing faster mappers. Modern tools use cut-based mapping with priority cuts, which computes depth labels in the same way over a limited set of cuts and then recovers area. FlowMap is not the tool for area, and it does not restructure logic.

## Pitfalls

- **Unbounded gates.** A gate with more than $K$ fanins has no $K$-feasible cut of its fanins. Split such gates first, for example into a tree of 2-input gates.
- **Merging only $t$.** The sink must include every node of label $p$ in the cone. If a node of label $p$ stays outside the sink, the cut can contain it, and the LUT would have depth $p + 1$.
- **Splitting the merged nodes.** The merged nodes must not get unit capacities, since they may not be cut. In the code of this page, edges out of a merged node are left out. Labels never decrease along a path, so such an edge goes to another merged node, and it does not change the flow.
- **Reading the cut.** The cut nodes are the split nodes whose input half is reachable from the source in the residual graph and whose output half is not. Taking all reachable nodes, or the unreachable ones, gives the wrong set.
- **Counting depth with PIs.** The PIs have label 0 and are not LUTs. A gate fed only by PIs has label 1.

## Implementations

## History

Early LUT mappers, such as Chortle and its depth version by Francis, Rose and their coauthors around 1990 and 1991, worked on trees, where dynamic programming is optimal, and handled general networks by splitting them into trees. Cong and Ding (1992, at ICCAD, and 1994, in IEEE TCAD) showed that depth-optimal mapping of a general $K$-bounded network takes polynomial time, with labels and a max-flow test, and called the method FlowMap. In the same year, Farrahi and Sarrafzadeh (1994) proved that minimizing the number of LUTs is NP-hard, which set the line between the two goals. FlowMap and its labels became the base of many later mappers, and the cut-based mappers of the late 1990s and 2000s compute the same labels by dynamic programming over enumerated cuts.

## References
