---
tag: HAXQH6
kind: algorithm
slug: daomap
name: DAOmap
aliases:
- depth-optimal area-optimized mapping
area: eda/fpga-analog-and-emerging-technologies
level: research
summary: Chen and Cong's depth-optimal LUT mapper that cuts area by cost functions for logic duplication and reconvergence and by iterative cut selection.
solves: [lut-mapping]
model: word-ram
complexity:
  vars: {n: the number of gates, c: the largest number of K-feasible cuts of a gate, d: the largest fanin of a gate, K: the number of LUT inputs, T: the number of cut selection passes}
  time: {cut enumeration and costs: O(n c^d K + n c d n), cut selection: O(T n c K)}
  space: {total: O(n c K)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 2004
  people: [Deming Chen, Jason Cong]
  note: DAOmap moved depth-optimal area mapping from the flow-based cuts of CutMap to cut enumeration, with an area cost that counts node duplication and a cut selection that uses slack, shared inputs and earlier passes.
prereqs: [cut-enumeration, flowmap, k-feasible-cut, lut-mapping]
see_also: [cutmap, priority-cuts, chortle-crf, static-timing-analysis, critical-path-method, technology-mapping, and-inverter-graph, fpga-packing]
sources:
  - paper: doi:10.1109/ICCAD.2004.1382677
    title: "Deming Chen and Jason Cong, DAOmap, a depth-optimal area optimization mapping algorithm for FPGA designs, Proceedings of the IEEE/ACM International Conference on Computer-Aided Design (ICCAD 2004), San Jose, pages 752 to 759"
    locator: Section 3 (cut enumeration with arrival time and area, Formulas 1 to 4), Section 4.1 to 4.3 (area flow, the cost U_C of a cut with alpha 0.8 and beta 0.4, the duplication cost of Formulas 6 and 7), Section 4.4 (Figure 4 ICS, Figure 5 pick_cut, share 1.15, slack weight 0.3, cut probing), Section 5 (Tables 1 to 3, three ICS passes)
  - paper: doi:10.1145/201310.201322
    title: "Jason Cong and Yean-Yow Hwang, Simultaneous depth and area minimization in LUT-based FPGA mapping, Proceedings of the 3rd ACM International Symposium on Field-Programmable Gate Arrays (FPGA 1995), pages 68 to 74"
    locator: CutMap, the mapper that DAOmap is compared against (general locator)
  - paper: "J. Cong, C. Wu and E. Ding, Cut ranking and pruning, enabling a general and efficient FPGA mapping solution, Proceedings of the ACM International Symposium on Field-Programmable Gate Arrays (FPGA 1999)"
    title: Cut ranking and pruning, enabling a general and efficient FPGA mapping solution
    locator: cut enumeration with the area estimate that divides the area of a signal by its fanout, and cut pruning for large K; cited by DAOmap as reference 6 (general locator)
---

DAOmap is an algorithm for [LUT mapping](/lut-mapping/), a step of FPGA CAD: it maps a network of gates into $K$-input lookup tables (LUTs) with the least possible depth and as few LUTs as it can. It lists all $K$-feasible cuts of each node by [cut enumeration](/cut-enumeration/), and while it does so it computes for each node the least arrival time and an area estimate that shares the area of a signal among its readers and adds a cost for logic that a cut would duplicate. Then it maps from the outputs back with required times. A node on the critical path takes its cheapest cut of least height. A node with slack takes the cut that is cheapest after a bonus for inputs that are already LUT outputs and for slack that it leaves to the nodes below. The selection runs three times, and each pass learns from the last. Chen and Cong gave it at ICCAD 2004 and reported 16.02% fewer LUTs than [CutMap](/cutmap/) at the same depth with 5-input LUTs.

## In plain words

Every signal that leaves a LUT costs a LUT, so a good mapping makes as few signals into LUT outputs as it can without making any path longer than the best possible depth. DAOmap first gives each node an estimate of how many LUTs its logic needs. A signal that feeds three gates splits its cost three ways, and a cut that copies logic which other gates also use pays extra. Then it walks back from the outputs. Where a node has no time to spare, it picks the cheapest fastest cut. Where it has time, it prefers cuts that read signals that are already LUT outputs, and cuts that leave time for the logic below. It repeats the walk a few times, and each walk knows which signals the last walk made into LUT outputs.

## The problem

**Input.** A $K$-bounded [Boolean network](/boolean-network/) (a directed acyclic graph of gates with at most $K$ fanins each; the paper uses 2-input networks), a set of output gates, and an integer $K$ (the paper uses 4, 5 and 6).

**Output.** A LUT mapping: a set of LUT roots that includes every output gate, and for each root $v$ a [$K$-feasible cut](/k-feasible-cut/) $C_v$ of $v$. Every gate in a cut is a root too.

**Goal.** The fewest LUTs among mappings whose depth, under the unit delay model, is the least possible depth $D$. The paper notes that area mapping is NP-hard, so DAOmap is a heuristic for the count. The depth part is exact.

## The algorithm

For a cut $C$ of a gate $v$, the arrival time is $1 + \max_{u \in C} \mathrm{arr}(u)$, and $\mathrm{arr}(v)$ is the least arrival time over the cuts of $v$, with $\mathrm{arr} = 0$ at a primary input. These are the [FlowMap](/flowmap/) labels. The area of a cut is

$$A_C = \sum_{i \in C} \frac{A_i}{f(i)} + U_C + \sum_{f} P_f,$$

where $f(i)$ is the number of readers of signal $i$ and $A_i$ is the area of node $i$ ($A = 0$ at an input). The last sum runs over the fanins $f$ of $v$ that are gates with more than one reader and are not in $C$: for each one, the cut covers the cone of $f$ and so copies it, and it pays $P_f = N_f / |C|$, where $N_f$ is the number of gates of that cone. The area of a node is $A_v = \min A_C$ over the cuts of $v$ that reach $\mathrm{arr}(v)$. With required time $r(v)$, the slack of a cut is $s(C) = r(v) - 1 - \max_{u \in C} \mathrm{arr}(u)$, and the cut keeps the depth only if $s(C) \ge 0$.

```pseudo id=main
DAOMAP(N, outputs, K, T)
L1  enumerate the K-feasible cuts of every gate, and compute arr and the areas A_C and A_v in topological order
L2  D ← max arr(o) over the outputs; tentative ← the gates with more than 3 readers
L3  repeat T times:
L4      r(o) ← D for each output o; roots ← outputs
L5      for each gate v in reverse topological order, skipping v if it is not in roots:
L6          if r(v) = arr(v) then C* ← the cut with s(C) = 0 of least A_C
L7          else C* ← the cut with s(C) ≥ 0 of least A_C / share(C) − 0.3 s(C)
L8          the LUT of v is C*; for each gate u in C*: add u to roots and set r(u) ← min(r(u), r(v) − 1)
L9      keep this mapping if it has the fewest LUTs so far; tentative ← its roots with more than one reader
L10 return the kept mapping
```

At line L7, let $m$ be the number of nodes of $C$ that are roots of this pass or tentative roots from the last pass. Then $\mathrm{share}(C)$ is 1 when $m = 0$, 1.15 when $m = 1$, and $m$ otherwise; these values and the weight 0.3 are from the paper. Dividing by the share makes a cut cheaper when it reads signals that are already LUT outputs, so the LUTs share inputs and fewer nodes are copied. The term $0.3\, s(C)$ favors cuts that use little of the slack, so the nodes below have room to pick cheap cuts too.

The implementation leaves out two parts of the paper, and changes one. First, the paper computes $U_C$ from the cut size $I_C$, the number of covered nodes $N_C$, the fanout of the root and the number of reconvergent paths that the cut covers, with constants $\alpha = 0.8$ and $\beta = 0.4$; the implementation uses $U_C = 1$, one LUT per cut. Second, the paper adjusts the cost by *cut probing*, which rewards a cut that lowers the fanout of a covered gate or that makes nodes into roots that the last pass had copied; the implementation does not. Third, the paper outputs the mapping of the last pass and keeps all earlier roots of strong fanout as tentative roots; the implementation keeps the best pass, and uses only the roots of the last pass. None of these changes affects the depth.

## Example

Take $K = 3$ and the network $g_0 = c \lor d$, $g_1 = b \land d$, $g_2 = g_1 \land g_0$, $g_3 = g_1 \lor a$, $g_4 = a \oplus g_2$, with outputs $g_3$ and $g_4$. Gate $g_1$ has two readers; the others have one.

Line L1 gives $\mathrm{arr} = 1$ for $g_0, g_1, g_2, g_3$ ($g_2$ and $g_3$ have cuts of inputs only, $\{b, c, d\}$ and $\{a, b, d\}$) and $\mathrm{arr}(g_4) = 2$, so $D = 2$. Some of the areas:

| cut | arrival | $A_C$ |
|---|---|---|
| $g_2$ over $\{b, c, d\}$ | 1 | $0 + 1 + 1/3 = 1.333$ (it copies $g_1$) |
| $g_2$ over $\{g_1, c, d\}$ | 2 | $1/2 + 1 = 1.5$ |
| $g_4$ over $\{a, g_2\}$ | 2 | $A_{g_2}/1 + 1 = 2.333$ |
| $g_4$ over $\{a, g_0, g_1\}$ | 2 | $1 + 1/2 + 1 = 2.5$ |
| $g_3$ over $\{a, g_1\}$ | 2 | $1/2 + 1 = 1.5$ |
| $g_3$ over $\{a, b, d\}$ | 1 | $1 + 1/3 = 1.333$ |

The selection, in reverse topological order:

| root | $r$ | $\mathrm{arr}$ | choice |
|---|---|---|---|
| $g_4$ | 2 | 2 | critical (line L6): both cuts have slack 0, and $\{a, g_2\}$ has less area; $r(g_2) = 1$ |
| $g_3$ | 2 | 1 | slack (line L7): $\{a, g_1\}$ costs $1.5 - 0 = 1.5$, $\{a, b, d\}$ costs $1.333 - 0.3 \cdot 1 = 1.033$; take $\{a, b, d\}$ |
| $g_2$ | 1 | 1 | critical: only $\{b, c, d\}$ has slack 0 |

The result has 3 LUTs and depth 2: $g_4$ over $\{a, g_2\}$, $g_3$ over $\{a, b, d\}$ and $g_2$ over $\{b, c, d\}$. Gate $g_1$ is copied into two LUTs, but it never becomes a LUT of its own. The two later passes give the same mapping. A brute force over all cut choices shows that 3 is the least count at depth 2. The FlowMap mapping phase takes the cut of $g_4$ that covers the most gates, $\{a, g_0, g_1\}$, so both $g_0$ and $g_1$ need their own LUTs and the result has 4. The test file checks every number in the two tables.

## Correctness

The [full proof](proofs/correctness.md) shows that the result is a valid mapping with the same outputs and depth exactly $D$. The argument is the same as for CutMap. The invariant is $\mathrm{arr}(u) \le r(u)$ for every root. At a critical root the cut that gives $\mathrm{arr}(v)$ has slack 0, and at a root with slack that same cut has slack at least 0, so lines L6 and L7 always have a cut to choose. Every chosen cut has $s(C) \ge 0$, so each node of it has $\mathrm{arr}(u) \le r(v) - 1$, and the invariant holds after line L8. Then by induction the LUT depth of each root is at most $r$. That no mapping has depth below $D$ is FlowMap's label theorem, cited from [FlowMap](/flowmap/). Nothing in the costs, the shares or the passes can break the depth, because all of them only rank cuts that already meet the bound.

## Complexity

Let $c$ be the largest number of cuts of a gate. Cut enumeration costs $O(c^d K)$ per gate. The duplication cost walks the cone of each multi-reader fanin for each cut, which is $O(d n)$ per cut in the worst case and much less on real circuits, where the cones of $K$-feasible cuts are small. Each selection pass visits each root once and scores its cuts in $O(c K)$, so $T$ passes cost $O(T n c K)$. The space is $O(n c K)$ for the cut lists and their areas. Chen and Cong show (Figure 2, the 20 largest MCNC benchmarks) that the average number of cuts per node is a small constant for small $K$, so enumeration is close to linear in $n$, and that it grows fast for $K \ge 7$, where cut pruning is needed. They give CutMap's worst case as $O(2^K m n^{\lfloor K/2 \rfloor + 1})$ for comparison.

## Properties

**What is proved.** The mapping is valid, computes the same outputs, and has the least possible depth $D$ (the last step by FlowMap's label theorem, cited by link). This holds for any costs, shares, slack weight or number of passes.

**What is cited.** On the 20 largest MCNC benchmarks, Chen and Cong (2004, Table 1 and Section 5.1) report that DAOmap uses 16.02% fewer LUTs than CutMap and runs 24.2 times faster with 5-input LUTs, at the same depth for every benchmark. With 4-input LUTs the numbers are 13.98% and 13.2 times, and with 6-input LUTs 12.44% and 4.7 times. Against CutMap with its depth relaxation switch, DAOmap uses 11.62%, 14.76% and 11.13% fewer LUTs for $K = 4, 5, 6$. On six industrial benchmarks, CutMap did not finish two of them in 10 hours. In the study of the passes, 3 passes gave the best average and more passes made it slightly worse. The paper also notes that the area estimate $A_v$ is not a lower bound on the mapped area once the depth is constrained.

**What is measured.** The tests compare the LUT count with an exhaustive search over every cut choice at depth $D$, on 200 random networks of 3 to 7 two-input gates with $K = 3$ (seed 5). DAOmap reaches the least count on all 200, and uses fewer LUTs than the FlowMap mapping phase on 1. On 400 other networks (seed 0) it reaches the least count on 395, uses fewer LUTs than FlowMap on 1 and more on 3, and the second and third passes never improve on the first. Such small networks have little room for the passes to help; the measurements show that the implementation is sound, not that it matches the results of the paper.

## Variants and improvements

- **CutMap** ([CutMap](/cutmap/), 1995) is the flow-based mapper that DAOmap replaced. It also maps from required times, with a cut cost that favors existing roots, but it computes one cut at a time by max-flow.
- **Area flow and exact area.** The area flow of DAOmap, where a signal's area is divided by its fanout, became standard. Later mappers add a second pass of *exact area*, which counts the LUTs that a cut would really add or free given the current mapping.
- **[Priority cuts](/priority-cuts/)** (Mishchenko, Cho, Chatterjee and Brayton, 2007) keep only a few best cuts per node, so that the same depth and area recovery scales to large networks and to $K = 6$ and above.
- **[And-inverter graphs](/and-inverter-graph/).** Mapping from an and-inverter graph with choices, as in ABC, gives the mapper several structures of the same logic to choose from, which DAOmap cannot do on a fixed network.

## When to use it

Use DAOmap when the LUT depth must be the least possible and the count matters, and $K$ is at most 6 so that all cuts can be listed. It is a good model of a depth-optimal mapper with area recovery, and its parts (area flow, duplication cost, slack, shared inputs, repeated passes) are the parts of most later mappers. For large designs or $K$ above 6, use a mapper with priority cuts.

## Pitfalls

- **Picking the cheapest cut everywhere.** If every node takes its least $A_C$ at line L1, the result keeps the depth only on paths where it happens to; required times are needed to know which cuts are allowed.
- **Area flow as a bound.** $A_v$ is an estimate. It can be below the real area, because it assumes that a node with several readers is not copied, and under the depth bound it is not a lower bound either.
- **Tuned constants.** The share 1.15 for one shared input, the slack weight 0.3 and the constants of $U_C$ come from experiments on MCNC benchmarks. They are not derived, and other benchmark sets can need other values.
- **Too many passes.** The paper found that more than 3 passes made the result slightly worse, because the tentative roots from old passes no longer fit the current one.
- **Large K.** The number of cuts grows fast with $K$. Without pruning, $K = 7$ and above is slow.

## Implementations

## History

Cong and Ding gave FlowMap in 1992 for least depth, and CutMap (Cong and Hwang, 1995) added area by computing cuts of least cost with max-flow. Cut enumeration, which lists all cuts of a node by combining the cuts of its fanins, and the area estimate that divides the area of a signal by its fanout, came from the cut ranking and pruning work of Cong, Wu and Ding (FPGA 1999), which was area-oriented and did not keep the depth optimal. In 2004 Chen and Cong showed in DAOmap that enumeration with good costs beats the flow-based cuts on both area and run time, and it was part of the RASP system of UCLA. The ideas moved into the priority cut mappers of ABC (2007) and the mappers that followed.

## References
