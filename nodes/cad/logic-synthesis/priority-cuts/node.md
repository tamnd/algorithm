---
tag: TMZ6X8
kind: algorithm
slug: priority-cuts
name: Priority cuts mapping
aliases:
- priority cuts
area: cad/logic-synthesis
level: advanced
summary: Mishchenko and coauthors' LUT mapper that keeps only a few best cuts per node, ranked by depth, area flow and exact area, so that cut-based mapping stays fast for large k.
solves: [lut-mapping]
model: word-ram
complexity:
  vars: {N: the number of nodes, C: the number of cuts kept per node, k: the number of inputs of a LUT}
  time: {worst: O(N k C^4 + N^2 C^2)}
  space: {extra: O(N k C)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2007
  people: [Alan Mishchenko, Sungmin Cho, Satrajit Chatterjee, Robert Brayton]
  note: Mishchenko, Cho, Chatterjee and Brayton kept a small number of priority cuts per node, computed again in each mapping pass, instead of all K-feasible cuts, and used it for combinational and sequential mapping in ABC.
prereqs: [lut-mapping, cut-enumeration]
see_also: [flowmap, k-feasible-cut, and-inverter-graph, technology-mapping, sat-sweeping, aig-rewriting, static-timing-analysis, beam-search]
sources:
  - paper: "Alan Mishchenko, Sungmin Cho, Satrajit Chatterjee and Robert Brayton, Combinational and sequential mapping with priority cuts, Proceedings of the IEEE/ACM International Conference on Computer-Aided Design (ICCAD 2007), pages 354 to 361"
    title: Combinational and sequential mapping with priority cuts
    locator: the priority cuts, the order of the mapping passes for depth, area flow and exact area, and the experiments (general locator; the default number of cuts and the exact sort keys are not checked)
  - paper: "Alan Mishchenko, Satrajit Chatterjee and Robert Brayton, Improvements to technology mapping for LUT-based FPGAs, IEEE Transactions on Computer-Aided Design 26(2), 2007"
    title: Improvements to technology mapping for LUT-based FPGAs
    locator: area flow, exact local area with reference counting, and mapping with structural choices (general locator)
  - paper: "Jason Cong, Chang Wu and Yuzheng Ding, Cut ranking and pruning, enabling a general and efficient FPGA mapping solution, Proceedings of the 1999 ACM/SIGDA Seventh International Symposium on Field Programmable Gate Arrays (FPGA 99), pages 29 to 35"
    title: Cut ranking and pruning, enabling a general and efficient FPGA mapping solution
    locator: the earlier idea of ranking cuts and keeping part of them (general locator)
---

Priority cuts mapping is a method for [LUT mapping](/lut-mapping/) that does not list all [$k$-feasible cuts](/k-feasible-cut/) of each node. Each node keeps at most $C$ cuts, its priority cuts, and the cuts of a node are made by merging only the priority cuts of its fanins. A mapping pass visits the nodes in topological order, makes the candidate cuts of a node, sorts them by the cost of the pass and keeps the first $C$, with the first as the best cut. The first pass sorts by depth. Later passes sort by area flow and by exact area, and they keep every node within the required time from the first pass, so the depth found in the first pass does not grow. Mishchenko, Cho, Chatterjee and Brayton (2007) used a small $C$ and reported that, on their benchmarks, this costs little depth or area while making mapping with 6-input cuts much faster. It is the base of the `if` LUT mapper of ABC. With $C$ unlimited the first pass is the exact depth dynamic program. With a small $C$ it is a heuristic and has no proved bound on the loss.

## In plain words

To map a circuit into lookup tables, a mapper must choose, for each gate, a small group of wires that decides the gate. There are many such groups, and listing all of them takes too long when each table has six inputs.

So keep only a few good groups for each gate, say eight. Build the groups of a gate only from the kept groups of the gates that feed it. Rank them, keep the best few, and move on. First rank them by how deep the result is, to find the shortest chain of tables. Then go over the circuit again and rank by how many tables they need, but never let a gate get later than the first pass allows. The kept groups change from pass to pass.

## The problem

The input is a $k$-bounded network, for example an [and-inverter graph](/and-inverter-graph/), with $N$ nodes in topological order and a set of outputs, and the LUT size $k$. The output is a mapping: for each needed gate a $k$-feasible cut, whose LUT computes the gate. The goal is the least depth, then the fewest LUTs at that depth. Least depth alone is solved exactly by [FlowMap](/flowmap/), and the fewest LUTs is NP-hard, so the second goal is only approached.

The pass costs use these terms. The *arrival time* of a node is the depth of its best cut, $1$ plus the largest arrival time of a leaf, with 0 for the inputs. The *area flow* of a node $v$ with best cut $B$ is
$$AF(v) = \frac{1 + \sum_{u \in B} AF(u)}{\max(1, \mathrm{fanout}(v))},$$
with 0 for the inputs, an estimate of the LUTs that $v$ needs, with shared logic split among its fanouts. The *exact area* of a cut of $v$, in the current mapping, is the number of LUTs that using the cut adds: the LUT of $v$ and the LUTs of its leaves that no other LUT uses yet, found with reference counts. The *required time* of a node in the mapping is the latest arrival time that keeps every output within the depth $D$ of the first pass.

## The algorithm

```pseudo id=main
PRIORITY-CUTS(G, k, C)
L1  for each gate v: P(v) ← ∅; best(v) ← none
L2  for each pass in (depth, area flow, exact area) do
L3      if the pass is not the depth pass then find the reference counts and the required times of the mapping from best, with D at the outputs
L4      for each gate v in topological order do
L5          A ← the unions of one set from P(u) ∪ {{u}} for each fanin u, with at most k leaves and without dominated sets
L6          if best(v) ≠ none then add best(v) to A
L7          if the pass is exact area and v is in the mapping then dereference best(v)
L8          sort A by the key of the pass, with every cut whose arrival time is later than the required time of v at the end
L9          P(v) ← the first C cuts of A; best(v) ← the first cut of A
L10         set the arrival time and the area flow of v from best(v)
L11         if the pass is exact area and v is in the mapping then reference best(v)
L12     if the pass is the depth pass then D ← the largest arrival time of an output
L13 return the LUTs reached from the outputs through best
```

The keys of line L8 are (arrival time, number of leaves, area flow) in the depth pass, (area flow, arrival time, number of leaves) in the area flow pass and (exact area, area flow, arrival time, number of leaves) in the exact area pass. Ties go to the smaller sorted list of leaves, so the code of this page is deterministic. Line L5 is the merge of [cut enumeration](/cut-enumeration/), applied to the short lists. Line L6 keeps the best cut of the last pass, which may no longer be a merge of the new priority cuts of the fanins. That cut is what keeps the depth from growing. Dereferencing at line L7 and referencing at line L11 keep the reference counts equal to the number of uses of each node in the current mapping, so that the exact area of line L8 is computed against the mapping without the old cut of $v$.

## Example

Take $k = 3$, the inputs $a, b, c, d$ and the gates $p = (a, c)$, $q = (b, p)$, $r = (d, q)$, $s = (b, r)$ and $o = (p, s)$, with $o$ the output. The least depth is 2.

With $C = 1$, the depth pass keeps one cut per node:

| node | kept cut | arrival |
|---|---|---|
| $p$ | $\{a, c\}$ | 1 |
| $q$ | $\{a, b, c\}$ | 1 |
| $r$ | $\{d, q\}$ | 2 |
| $s$ | $\{b, d, q\}$ | 2 |
| $o$ | $\{p, s\}$ | 3 |

At $q$, the cut $\{a, b, c\}$ has depth 1 and beats $\{b, p\}$, which has depth 2, so $\{b, p\}$ is dropped. At $r$, the merge of $\{d\}$ with $\{a, b, c\}$ has 4 leaves, so $r$ must use $q$ as a leaf. The pass ends with depth 3 and 4 LUTs, for $o$, $p$, $s$ and $q$. The area passes keep depth 3 and lower the count to 3 LUTs.

With $C = 2$, $q$ keeps $\{a, b, c\}$ and $\{b, p\}$. Then $r$ keeps $\{d, q\}$ and $\{b, d, p\}$, and $s$ keeps $\{b, d, p\}$ and $\{b, d, q\}$, both of depth 2, with $\{b, d, p\}$ first because its area flow is lower, 1.5 against 2. At $o$, the union of $\{p\}$ and $\{b, d, p\}$ is $\{b, d, p\}$, of depth 2. The mapping has depth 2 and 2 LUTs: $o$ over $\{b, d, p\}$ and $p$ over $\{a, c\}$. The cut that is best at $q$ alone is not the one that helps at $o$, and one more priority cut keeps the useful one.

## Correctness

The [full proof](proofs/correctness.md) shows four facts. Every cut that a node keeps is a $k$-feasible cut of the node, because it is a union of cuts of the fanins, so every LUT computes its node and the mapping keeps the functions. With $C$ at least the number of cuts of every node, the depth pass keeps all minimal $k$-feasible cuts, by the theorem of cut enumeration, and computes the least depth exactly. The area passes never raise the depth above the depth $D$ of the first pass: the old best cut of each node in the mapping meets its required time, and it is always a candidate at line L6. The exact area pass never raises the number of LUTs, since the old best cut is a candidate and line L8 prefers a cut with an exact area that is not larger.

## Complexity

With 2-input gates, line L5 makes at most $(C + 1)^2$ unions of $O(k)$ cost each, and the dominance test of the code of this page compares pairs, $O(k C^4)$ in the worst case. Line L8 sorts $O(C^2)$ cuts. The exact area of a cut costs $O(N)$ in the worst case, since referencing can walk a large cone, but on circuits the walk is short, and implementations bound its depth. A pass is $O(N k C^4)$ without the exact area walks, and the walks add $O(N^2 C^2)$ in the worst case. Without the walks, for a fixed $C$ and $k$, a pass is linear in $N$, the main gain over full enumeration, whose lists have no fixed bound. The priority cuts take $O(N k C)$ space, and only the best cut of each node must survive between passes.

## Properties

**What is proved.** The mapping computes the same functions as the network. The depth after the area passes is at most the depth of the first pass. The exact area pass never increases the number of LUTs of the mapping. With $C$ unlimited, the first pass gives the least depth. With any $C$, the depth is at least the least depth, since every mapping is.

**What is not proved.** With a small $C$ there is no bound on the gap to the least depth or to the fewest LUTs, and the example above loses one level with $C = 1$. The area passes are heuristics, and nothing is proved about the LUT count after the area flow pass.

**What is measured.** The code of this page was run on 20 random networks of 2-input gates, each with 16 inputs, 150 gates whose fanins come from the 12 nodes before them, and 8 outputs (seed 77). For $k = 4$, the sum of the depths over the 20 networks was 241 with $C = 1$, 223 with $C = 2$, 214 with $C = 4$, 179 with $C = 8$ and 178 with no limit, the least depth. The LUT counts after the area passes were 1449, 1280, 1161, 1023 and 1020. For $k = 6$ the depth sums were 58, 49, 44 and 40 for $C = 1, 2, 4, 8$, with 412, 326, 283 and 252 LUTs. These are toy measurements to show the trend, not benchmark results. The paper reports its own measurements on benchmark circuits, against mapping with all cuts.

## Variants and improvements

- **Structural choices.** Run the mapper on a network that keeps several equivalent structures of the same logic, found by [SAT sweeping](/sat-sweeping/). The cuts of a node then come from all its choices, and the mapper can pick the better structure for each cut. The paper of Mishchenko, Chatterjee and Brayton on improvements to LUT mapping maps with such choices.
- **Sequential mapping.** The same cut lists work across registers, so that mapping and [retiming](/retiming/) are done together, the second topic of the 2007 paper.
- **Standard cells.** With the truth table of each cut and [Boolean matching](/boolean-matching/), the same passes can map into a cell library instead of LUTs.
- **Other costs.** The keys of line L8 can count wire length, edge count or power instead of LUTs.
- **More cuts for critical nodes.** A mapper can keep more cuts at nodes on critical paths and fewer elsewhere.

## When to use it

Use priority cuts for LUT mapping of large circuits with $k = 6$ or more, where full [cut enumeration](/cut-enumeration/) is too slow or too large, and when both depth and LUT count matter. For a proof of depth optimality on small designs, use [FlowMap](/flowmap/) or full enumeration. Run AIG optimization such as [rewriting](/aig-rewriting/) first, since the mapper does not restructure logic.

## Pitfalls

- **Dropping the old best cut.** If the best cut of the last pass is not a candidate, an area pass can be forced to a later cut, and the depth can grow.
- **Stale required times.** The required times must come from the current mapping, not from the network, since a node that the mapping does not use has no required time.
- **Reference counts out of step.** In the exact area pass, the old cut of a node in the mapping must be dereferenced before the candidates are costed and the new one referenced after, or the exact area counts the node's own LUTs as shared.
- **Fanout counts in area flow.** Count an output as a fanout, and divide by 1 for a node with no fanout. If outputs are not counted, an output node that also feeds one gate looks fully owned by that gate.
- **Trusting a small C.** A small $C$ can lose depth, as the example shows. Check the depth against a pass with more cuts when it matters.

## Implementations

## History

Cut-based LUT mapping lists the $k$-feasible cuts of each node and picks one by dynamic programming, as in the mappers of Pan and Lin (1998) and of Cong, Wu and Ding (1999), who already ranked cuts and kept only part of them. Mishchenko, Chatterjee and Brayton improved the area passes of such mappers with area flow, exact local area and structural choices, in a paper that appeared in IEEE TCAD in 2007. In the same year, Mishchenko, Cho, Chatterjee and Brayton replaced full enumeration by a few priority cuts per node, computed again in each pass, and applied it to both combinational and sequential mapping. The method is the base of the `if` LUT mapper of ABC.

## References
