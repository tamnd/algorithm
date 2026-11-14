---
tag: 3GVCMN
kind: problem
slug: resource-binding
name: Resource binding
aliases:
- functional unit binding
- resource sharing
area: eda/high-level-synthesis-and-scheduling
level: core
summary: Assign the operations of a scheduled graph to functional unit instances so that operations in the same step never share a unit and the total cost is least.
prereqs: [resource-compatibility-graph, resource-constrained-scheduling, clique-cover]
see_also: [register-binding, interconnect-binding, module-selection, tseng-siewiorek-clique-partitioning, weighted-bipartite-matching-binding, graph-coloring, interval-partitioning, chromatic-number]
sources:
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: Chapter 6, Resource Sharing and Binding (sharing and binding of functional resources, compatibility and conflict graphs, and binding with control flow)
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: Richard M. Karp, Reducibility among combinatorial problems, in Complexity of Computer Computations, Plenum (1972), 85 to 103
    locator: the list of 21 problems (Chromatic number and Clique cover)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Appendix A1.1, problems GT4, Graph k-colorability, and GT15, Partition into cliques
  - paper: doi:10.1109/TCAD.1986.1270207
    title: Chia-Jeng Tseng and Daniel P. Siewiorek, Automated synthesis of data paths in digital systems, IEEE Transactions on Computer-Aided Design 5(3), 379 to 395, 1986
    locator: functional unit allocation as clique partitioning of the operation compatibility graph
---

Resource binding is the step of [high-level synthesis](/high-level-synthesis/) that maps each operation of a scheduled design to one instance of a functional unit, such as multiplier 2 or ALU 1. Two operations may use one instance only if they are never busy in the same step. With the schedule fixed, the least number of instances of a unit type is the least number of cliques that partition the [resource compatibility graph](/resource-compatibility-graph/) of that type. For straight-line code this is easy, but with conditional code it is [NP-hard](/np-hard/).

## In plain words

After scheduling, each calculation has a time slot. Now each one needs a piece of hardware to run on. Two multiplies in different slots can use the same multiplier, but two multiplies in the same slot cannot, unless they sit on the two sides of an if and so never both happen. The task is to give each calculation a unit so that no unit is double booked, and to buy as few units as possible. When the code has no branches, count the busiest slot: that many units of the type are enough. When branches let calculations share a slot without a clash, the puzzle becomes as hard as coloring a map. A second goal is to keep the wiring small, since each extra source on a unit input costs a multiplexer input.

## Definition

**Input.**

- A scheduled sequencing graph $G = (V, E)$, part of a [control data flow graph](/control-data-flow-graph/), with a delay $d(v)$ and a start step $s(v)$ for each operation, as in [resource-constrained scheduling](/resource-constrained-scheduling/). There is no chaining, and units are not pipelined unless the variant says so.
- A relation of *mutual exclusion*: $u$ and $v$ are mutually exclusive when no execution of the design runs both.
- A set $K$ of unit types with an area $c_k > 0$ for each $k \in K$, and for each operation the type $t(v) \in K$ that runs it.

Let $B(v) = \{s(v), \ldots, s(v) + d(v) - 1\}$ be the busy set of $v$. Two operations of the same type are *compatible* when $B(u) \cap B(v) = \emptyset$ or they are mutually exclusive.

**Feasible solutions.** A binding $\beta$ maps each $v$ to an instance $\beta(v) = (t(v), i)$ with $i \in \{1, 2, \ldots\}$, such that $\beta(u) = \beta(v)$ implies that $u$ and $v$ are compatible.

**Objective.** Minimize $\sum_{k \in K} c_k\, n_k(\beta)$, where $n_k(\beta)$ is the number of instances of type $k$ that $\beta$ uses.

**Decision form.** Given the input and integers $(N_k)_{k \in K}$, is there a binding with $n_k(\beta) \le N_k$ for each $k$?

Since each operation has one type, the objective splits into one problem per type: minimize $n_k$ over the operations of type $k$. By the clique argument on the [resource compatibility graph](/resource-compatibility-graph/) page, the least $n_k$ is the clique partition number of the compatibility graph $G_k$, which is the [chromatic number](/chromatic-number/) $\chi(\overline{G_k})$ of the conflict graph.

This page is about functional units. [Register binding](/register-binding/) is the same kind of problem for values and their lifetimes, and [interconnect binding](/interconnect-binding/) chooses the multiplexers and ports once units and registers are bound.

## Variants

- **Interconnect cost.** The objective adds the multiplexer inputs in front of the units. Then two bindings with the same unit count can differ in cost, and the problem no longer splits by type. See [interconnect binding](/interconnect-binding/).
- **Several types per operation.** An add may run on an adder or on an ALU. The binding then also chooses the type, which is the problem of [module selection](/module-selection/) when the types differ in delay.
- **Pipelined units.** A pipelined unit takes a new operation in each step, so $B(v) = \{s(v)\}$.
- **Loops.** In a loop that starts a new iteration every $II$ steps, an operation is busy in the steps $B(v) \bmod II$. Busy sets become arcs of a circle with $II$ points, and the conflict graph is a circular-arc graph, see [circular-arc coloring](/circular-arc-coloring/).
- **Binding before scheduling.** Some flows bind first and then schedule with the binding as a constraint, or solve both together in one [0-1 program](/binary-integer-programming/). The definition above fixes the schedule.

## Examples

**Straight-line code.** Take the schedule of the [compatibility graph](/resource-compatibility-graph/) page with the branch removed: multiplies $m_1, m_2$ in step 1, $m_3$ in step 2, and $m_4$ in steps 3 and 4. At most 2 multiplies are busy in one step, and the binding $\{m_1, m_3, m_4\}$, $\{m_2\}$ uses 2 multipliers.

**Conditional code where the busiest step is not enough.** Let a variable $\kappa$ select one of the cases $1, \ldots, 10$, and put five multiplies $m_1, \ldots, m_5$ in step 1, all guarded:

| operation | runs when $\kappa$ is in |
|---|---|
| $m_1$ | $\{1, 5, 6\}$ |
| $m_2$ | $\{1, 2, 7\}$ |
| $m_3$ | $\{2, 3, 8\}$ |
| $m_4$ | $\{3, 4, 9\}$ |
| $m_5$ | $\{4, 5, 10\}$ |

Each value of $\kappa$ runs at most 2 multiplies, so no execution ever has more than 2 busy in step 1. But $m_i$ and $m_{i+1}$ (and $m_5$ and $m_1$) run together for one value of $\kappa$, and no other pair does. The conflict graph is the 5-cycle, which needs 3 colors, so the least binding has 3 multipliers, for example $\{m_1, m_3\}$, $\{m_2, m_4\}$ and $\{m_5\}$.

## Known algorithms

- **Interval partitioning and the left-edge algorithm.** Exact for straight-line code with one type per operation: they reach the number of operations in the busiest step. See [interval partitioning](/interval-partitioning/) and the [left-edge algorithm](/left-edge-algorithm/).
- **Coloring of chordal conflict graphs.** Exact when the conflict graph is [chordal](/chordal-graph/), in linear time. See [chordal graph coloring](/chordal-graph-coloring/).
- **Tseng-Siewiorek clique partitioning.** A greedy merge on the compatibility graph. Heuristic: it can use more units than needed, even on straight-line code. See [Tseng-Siewiorek clique partitioning](/tseng-siewiorek-clique-partitioning/).
- **Weighted bipartite matching.** Binds step by step with an [assignment problem](/assignment-problem/) per step to save interconnect. Heuristic for interconnect. See [weighted bipartite matching binding](/weighted-bipartite-matching-binding/).
- **Coloring heuristics.** For general conflict graphs, [greedy coloring](/greedy-coloring/) and [DSatur](/dsatur/) are fast with no guarantee.
- **Integer programming.** A 0-1 variable for each operation and instance gives the optimum for small designs, also with interconnect costs. See [0-1 integer programming](/binary-integer-programming/).

## Bounds

**Lower bound.** In every binding, $n_k \ge \omega(\overline{G_k})$, the size of the largest set of pairwise conflicting operations of type $k$, since they need distinct instances. This is at least the largest number of type-$k$ operations busy in one step of one execution.

**Straight-line code.** With no mutually exclusive pairs, the busy sets are intervals of steps, the conflict graph is an interval graph, and the least $n_k$ equals the largest number of type-$k$ operations busy in one step. Proof: pairwise intersecting intervals share a point, so a largest clique of the conflict graph is a set of operations busy in one common step, which gives the lower bound. The [interval coloring depth theorem](/interval-coloring-depth-theorem/) gives a coloring with that many colors. So for straight-line code, the scheduler already fixes the unit count, and binding only decides the interconnect.

**Gap with branches.** The 5-cycle example has $\omega = 2$ and needs 3. Since the construction in the next section realizes every graph as a conflict graph, the ratio $\chi / \omega$ is unbounded: there are triangle-free graphs of any chromatic number.

**Upper bound.** Any greedy coloring of the conflict graph uses at most $\Delta + 1$ instances, with $\Delta$ the largest number of operations that conflict with one operation.

## Reductions

**To clique cover and coloring.** For one type per operation, resource binding of type $k$ is the [clique cover problem](/clique-cover/) on $G_k$, and [graph coloring](/graph-coloring/) on its complement. The proof is on the [resource compatibility graph](/resource-compatibility-graph/) page.

**NP-hard with conditional code.** The decision form is NP-complete. It is in NP, since a binding is checked pair by pair. For hardness, take any graph $H = (U, F)$ and an integer $q$. Number the edges and the vertices of $H$, so that a variable $\kappa$ ranges over $F \cup U$. For each vertex $u$, build a multiply $m_u$ in step 1, guarded by the test $\kappa \in S_u$ with
$$S_u = \{ e \in F : u \in e \} \cup \{ u \}.$$
Two multiplies $m_u$ and $m_v$ both run exactly when $\kappa \in S_u \cap S_v$. The private elements $u$ and $v$ differ, so $S_u \cap S_v = \{uv\}$ when $uv \in F$ and $S_u \cap S_v = \emptyset$ otherwise. So $m_u$ and $m_v$ conflict exactly when $uv$ is an edge of $H$, the conflict graph of the multiplies is $H$, and $q$ multipliers suffice exactly when $\chi(H) \le q$. The construction has $|U|$ operations and tests of total size $O(|U| + |F|)$. Chromatic number is NP-complete (Karp 1972), so resource binding is NP-hard. The 5-cycle example above is this construction for $H = C_5$.

The proof needs a mutual exclusion relation that is exact for these tests. A tool that detects fewer exclusions sees more conflicts, which can only raise the count.

**Polynomial case.** For straight-line code, the bound above is reached by interval partitioning in $O(n \log n)$ time for $n$ operations.

## Applications

- **Datapath synthesis.** Every high-level synthesis tool binds operations to units after or during scheduling, as in the flows of De Micheli and of Tseng and Siewiorek.
- **Sharing of large units.** Dividers, floating point units and memory ports are costly, so sharing them across exclusive branches saves the most area.
- **FPGA DSP blocks.** On an FPGA with few DSP blocks, binding decides how many multiplies share one block and how many multiplexer inputs they need.

## References
