---
tag: 7KTJSE
kind: algorithm
slug: cutmap
name: CutMap
aliases:
- Cong-Hwang CutMap
area: eda/fpga-analog-and-emerging-technologies
level: advanced
summary: Cong and Hwang's LUT mapper that keeps FlowMap's optimal depth and cuts area by choosing cuts that reuse already chosen LUT roots off the critical path.
solves: [lut-mapping]
model: word-ram
complexity:
  vars: {n: the number of gates, c: the largest number of K-feasible cuts of a gate, d: the largest fanin of a gate, K: the number of LUT inputs}
  time: {cut enumeration: O(n c^d K), labels and mapping: O(n c K)}
  space: {total: O(n c K)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 1995
  people: [Jason Cong, Yean-Yow Hwang]
  note: CutMap replaced the least-height cuts of FlowMap with least-cost cuts of bounded height, so that the depth stays optimal and the cuts reuse nodes that are already LUT outputs.
prereqs: [flowmap, k-feasible-cut, cut-enumeration, lut-mapping]
see_also: [daomap, chortle-crf, priority-cuts, static-timing-analysis, critical-path-method, max-flow-min-cut-theorem, technology-mapping, fpga-packing]
sources:
  - paper: doi:10.1145/201310.201322
    title: "Jason Cong and Yean-Yow Hwang, Simultaneous depth and area minimization in LUT-based FPGA mapping, Proceedings of the 3rd ACM International Symposium on Field-Programmable Gate Arrays (FPGA 1995), Monterey, pages 68 to 74"
    locator: the least-cost cut of bounded height, the required times from the optimal depth, the node costs that favor existing LUT roots, and the comparison with FlowMap on MCNC benchmarks, 15% fewer LUTs in the abstract (general locator for the body)
  - paper: doi:10.1145/233539.233540
    title: "Jason Cong and Yuzheng Ding, Combinational logic synthesis for LUT based field programmable gate arrays, ACM Transactions on Design Automation of Electronic Systems 1(2), 145 to 204, 1996"
    locator: Section 4.3.2 (the cost of a cut as the sum of node costs, low cost for nodes that are or will be LUT roots, the pruning theorem) and Section 5.4 (13% fewer LUTs than FlowMap)
  - paper: doi:10.1109/ICCAD.2004.1382677
    title: "Deming Chen and Jason Cong, DAOmap, a depth-optimal area optimization mapping algorithm for FPGA designs, Proceedings of the IEEE/ACM International Conference on Computer-Aided Design (ICCAD 2004), pages 752 to 759"
    locator: Section 1 (CutMap computes min-cost min-height cuts for critical nodes and min-cost cuts for non-critical nodes) and Table 1 (DAOmap against CutMap on the 20 largest MCNC benchmarks)
---

CutMap is an algorithm for [LUT mapping](/lut-mapping/), a step of FPGA CAD: it maps a network of gates into $K$-input lookup tables (LUTs) with the least possible depth, the same depth that [FlowMap](/flowmap/) gets, and tries to use fewer LUTs than FlowMap does. FlowMap gives each LUT root a cut of least height. CutMap only needs a cut whose height meets a required time, and among those cuts it takes the one of least cost, where a node that is already a LUT output costs nothing. Cong and Hwang gave it at FPGA 1995 and reported about 15% fewer LUTs than FlowMap at the same depth.

## In plain words

A LUT mapper picks, for each signal that must come out of a LUT, a set of at most $K$ signals to feed that LUT. FlowMap always picks the set that is as early as possible, so every LUT is as fast as it can be. That is more than needed: only the LUTs on the longest path must be that fast. CutMap first finds the best depth $D$, then works backward from the outputs and tells each LUT how late its inputs may arrive. Among the input sets that meet that deadline, it picks the one that makes the fewest new LUTs, which usually means it reuses signals that are already LUT outputs.

## The problem

**Input.** A $K$-bounded [Boolean network](/boolean-network/), a directed acyclic graph of gates with at most $K$ fanins each, a set of output gates, and an integer $K \ge 2$.

**Output.** A LUT mapping: a set of LUT roots, which includes every output gate, and for each root $v$ a [$K$-feasible cut](/k-feasible-cut/) $C_v$ of $v$ (a set of at most $K$ nodes, not containing $v$, that meets every path from a primary input to $v$). Every gate in a cut is a LUT root too. The LUT of $v$ computes $v$ as a function of $C_v$.

**Goal.** Under the unit delay model the depth of the mapping is the largest number of LUTs on a path from an input to an output. The goal is the fewest LUTs among mappings of least depth $D$. Finding that is NP-hard in general (Chen and Cong cite this for area mapping), so CutMap is a heuristic for the count. The depth part is exact.

## The algorithm

CutMap first computes the FlowMap label $\ell(v)$ of every node: $\ell(v) = 0$ for a primary input, and for a gate $\ell(v) = 1 + \min_C \max_{u \in C} \ell(u)$ over the $K$-feasible cuts $C$ of $v$. The *height* of a cut is $\max_{u \in C} \ell(u)$. The optimal depth is $D = \max_o \ell(o)$ over the outputs. Then the mapping phase below runs. The cost of a cut is the number of its gates that are not yet LUT roots, because each of them makes a new LUT.

```pseudo id=main
CUTMAP-MAP(N, outputs, K, D)
L1  r(o) ← D for each output o; roots ← outputs
L2  for each gate v in reverse topological order, skipping v if it is not in roots:
L3      b ← r(v) − 1
L4      F ← the K-feasible cuts C of v with max over u in C of ℓ(u) ≤ b
L5      C* ← the cut in F of least cost (ties: fewer nodes, then lower height)
L6      the LUT of v is C*
L7      for each node u in C*:
L8          if u is a gate then add u to roots
L9          r(u) ← min(r(u), r(v) − 1)   ▷ r(u) is D when not yet set
L10 return the LUTs
```

Line L4 is where CutMap differs from FlowMap. FlowMap keeps only cuts of height exactly $\ell(v) - 1$. CutMap keeps every cut of height up to $r(v) - 1$, and on a node off the critical path $r(v)$ is larger than $\ell(v)$, so there are more cuts to choose from. On the critical path $r(v) = \ell(v)$ and the choice is the same as in FlowMap, except that CutMap still picks the cheapest of the least-height cuts.

The implementation finds all $K$-feasible cuts by [cut enumeration](/cut-enumeration/) and computes the labels from them. The paper instead finds the least-cost cut of bounded height by a max-flow computation on a network with node costs, as FlowMap does for the labels, and uses a pruning theorem to make that fast. Both give a cut of least cost under the same height bound. The paper also starts with a guess of the nodes that will be LUT roots (for example the roots of large fanout-free cones) and gives them a low cost from the start; the implementation does not, so its costs come only from roots that are already chosen.

## Example

Take $K = 3$ and the network $g_0 = c \oplus b$, $g_1 = d \lor b$, $g_2 = g_1 \lor g_0$, $g_3 = g_2 \oplus a$, with output $g_3$.

The labels are $\ell(g_0) = \ell(g_1) = 1$, since their fanins are inputs. $\ell(g_2) = 1$, since the cut $\{b, c, d\}$ has height 0. The 3-feasible cuts of $g_3$ are $\{a, g_2\}$ and $\{a, g_0, g_1\}$, because every cut that reaches the inputs has the 4 inputs $a, b, c, d$. Both have height 1, so $\ell(g_3) = 2$ and $D = 2$.

| step | content |
|---|---|
| line L1 | $r(g_3) = 2$, roots $= \{g_3\}$ |
| $v = g_3$, L3 to L4 | $b = 1$; both cuts have height 1, so $F = \{\{a, g_2\}, \{a, g_0, g_1\}\}$ |
| L5 | $\{a, g_2\}$ makes one new root, $\{a, g_0, g_1\}$ makes two; $C^* = \{a, g_2\}$ |
| L7 to L9 | $g_2$ is a root with $r(g_2) = 1$ |
| $v = g_2$, L3 to L5 | $b = 0$; only $\{b, c, d\}$ has height 0, so it is the LUT of $g_2$ |
| L10 | 2 LUTs: $g_3$ over $\{a, g_2\}$ and $g_2$ over $\{b, c, d\}$; depth 2 |

FlowMap's mapping phase at $g_3$ takes a cut of height 1 that covers the most gates, which is $\{a, g_0, g_1\}$, because it puts both $g_2$ and $g_3$ in one LUT. Then $g_0$ and $g_1$ need their own LUTs, and the result has 3 LUTs. A brute force over all cut choices confirms that 2 is the least count at depth 2. The test file checks this example.

## Correctness

The [full proof](proofs/correctness.md) shows that the result is a valid mapping that computes the same outputs, and that its depth is exactly $D$. The key step is the invariant $\ell(u) \le r(u)$ for every root $u$. It holds at the outputs because $D$ is the largest output label. At a root $v$, the definition of $\ell(v)$ gives a cut of height $\ell(v) - 1 \le r(v) - 1$, so the set $F$ of line L4 is never empty. Every node of the chosen cut has label at most $r(v) - 1$, so line L9 keeps the invariant. Then by induction in topological order, the LUT of a root $u$ has depth at most $r(u)$, and every output has depth at most $D$. That no mapping has depth below $D$ is FlowMap's theorem that $\ell(v)$ is the least depth of $v$; this page cites it from [FlowMap](/flowmap/) and does not prove it again.

## Complexity

Let $c$ be the largest number of $K$-feasible cuts of a gate and $d \le K$ the largest fanin. Cut enumeration takes, at each gate, the product of the cut lists of its fanins, so it costs $O(c^d K)$ per gate and $O(n c^d K)$ in total, before the removal of dominated cuts. The labels cost $O(c K)$ per gate. The mapping phase visits each root once, filters its cuts at line L4 and computes their costs at line L5 in $O(c K)$ time, so it costs $O(n c K)$. The space is $O(n c K)$ for the cut lists. For a fixed $K$, $c$ is at most $O(n^K)$, but on real circuits it is much smaller. The flow-based version of the paper does not list cuts; Chen and Cong (2004) give its worst case as $O(2^K m n^{\lfloor K/2 \rfloor + 1})$ with $m$ edges, and the survey of Cong and Ding says the pruning theorem makes it much faster in practice.

## Properties

**What is proved.** The mapping is valid, computes the same outputs, and has depth $D$, the least possible depth (the last step by FlowMap's label theorem, cited by link). If a larger depth bound $D' \ge D$ is given, the same proof shows the depth is at most $D'$.

**What is cited.** Cong and Hwang (1995) reported fewer LUTs than FlowMap with the same depth on MCNC benchmarks. The abstract of the paper gives 15% fewer LUTs; the survey of Cong and Ding (1996, Section 5.4) states the average as a 13% area reduction. The two numbers may come from different benchmark sets or settings; this page does not decide between them. Chen and Cong (2004) report that DAOmap uses 16.02% fewer LUTs than CutMap with 5-input LUTs on the 20 largest MCNC benchmarks.

**What is measured.** The tests compare the LUT count with an exhaustive search over every cut choice at depth $D$, on 200 random networks of 3 to 7 two-input gates with $K = 3$ (seed 5). CutMap reaches the least count on all 200, and uses fewer LUTs than the FlowMap mapping phase on 1 of them. On another 400 networks (seed 0), it reaches the least count on 399, uses fewer LUTs than FlowMap on 3 and more on 1. These are tiny networks; they show that the greedy choice is often right, not that it is optimal.

**Not optimal for the count.** The choice at each root is greedy in reverse topological order. A cut that is cheap now can force more LUTs below, and the cost does not see that.

## Variants and improvements

- **Area recovery with relaxed depth.** If the depth bound is set above $D$, more cuts pass line L4 and the count can drop. The implementation takes the bound as a parameter.
- **FlowMap-r** (Cong and Ding) starts from the FlowMap mapping and improves it afterward by remapping and relaxing the depth of non-critical nodes, instead of choosing the cuts with costs from the start.
- **[DAOmap](/daomap/)** (Chen and Cong, 2004) enumerates cuts, gives them an area-flow cost that counts the duplication of nodes, and repeats the cut selection several times. It reports 16.02% fewer LUTs than CutMap and is 24.2 times faster.
- **[Priority cuts](/priority-cuts/)** keep only a few cuts per node, so that cut-based depth and area mapping scales to large networks.

## When to use it

Use CutMap when the depth of the LUT network must be the least possible and the LUT count should be small. Its idea, a required time from the optimal depth and a cheap cut under that bound, is the same as the slack used in [static timing analysis](/static-timing-analysis/) and the [critical path method](/critical-path-method/), and it is the base of most later depth-optimal area mappers. For new tools, DAOmap and priority cuts give better counts at the same depth.

## Pitfalls

- **Using the label as the bound.** If line L4 uses $\ell(v) - 1$ in place of $r(v) - 1$, the algorithm is FlowMap with a tie-break and loses most of the gain.
- **Order of the roots.** A root must be processed after every root that reads it, so that $r(u)$ is final. Reverse topological order does this. An order by label alone can fail, because a node and a node in its cut can have the same label.
- **The required time of a shared node.** A node read by several LUTs takes the least of their bounds at line L9. Overwriting it with the last bound can break the depth.
- **Dominated cuts.** Keep only cuts that are not strict supersets of another cut. A superset never has a smaller cost or height, and it makes the cut lists larger.
- **A cost without reuse.** A cost that counts only the size of the cut, without asking whether a node is already a root, gives no reuse and little gain over FlowMap.

## Implementations

## History

Cong and Ding gave FlowMap in 1992, and it found the least depth in polynomial time, but it used more LUTs than area mappers such as Chortle-crf. FlowMap-r improved the count by changes after the mapping. In 1995, Cong and Hwang presented CutMap at the FPGA symposium. It put the area cost into the cut computation itself and used the depth bound only where it is needed. It was part of the RASP synthesis system of UCLA and became the standard depth-optimal area mapper in academic work, until later cut-based mappers such as DAOmap (2004) and the priority cuts of ABC gave better counts.

## References
