---
tag: BXSS6G
kind: problem
slug: module-selection
name: Module selection
aliases:
- resource type selection
area: eda/high-level-synthesis-and-scheduling
level: advanced
summary: Choose for each operation one of several library units of different speed and area, for example a ripple or carry-lookahead adder, together with the schedule.
prereqs: [latency-constrained-scheduling, knapsack-problem]
see_also: [resource-constrained-scheduling, ilp-scheduling-formulation, resource-binding, operation-chaining, sdc-scheduling, critical-path-method, hardware-software-partitioning, interconnect-binding]
sources:
  - paper: doi:10.1109/ISCAS.1991.176748
    title: Masayoshi Ishikawa and Giovanni De Micheli, A module selection algorithm for high-level synthesis, IEEE International Symposium on Circuits and Systems, 1991
    locator: whole paper (module selection under a latency bound, starting from the fastest modules)
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: Chapters 5 and 6 (scheduling and binding when one operation type has several implementations)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Appendix A6, problem MP9, Knapsack
---

Module selection is the problem of [high-level synthesis](/high-level-synthesis/) in which each operation may run on one of several library modules that do the same job at different speed and area, for example a ripple-carry adder that is small and slow or a carry-lookahead adder that is large and fast. The choice of modules and the schedule must be made together, since a slow module lengthens the schedule and a fast one costs area. It contains [latency-constrained scheduling](/latency-constrained-scheduling/), where each operation has one module, and it is [NP-hard](/np-hard/) even for a chain of operations, where scheduling alone would be trivial, by a reduction from the [knapsack problem](/knapsack-problem/).

## In plain words

A chip library often has several circuits for the same job. One multiplier is fast but big, another is slow but small. For each multiplication in the design, we pick one of these circuits and a time slot. Picking the small, slow circuit saves area but makes the whole computation take longer. With a deadline to meet, the task is to pick the circuits and slots so that the deadline holds and the total area of the circuits we build is least. Fast circuits belong where time is short, and slow ones where there is time to spare.

## Definition

The model is that of [latency-constrained scheduling](/latency-constrained-scheduling/), with types replaced by a choice of modules.

**Input.**

- A sequencing graph $G = (V, E)$ with no cycle, and for each operation $v$ an operation kind $o(v)$, such as multiply or add.
- A library of modules. Each module $m$ implements one kind, has an integer delay $d_m \ge 1$ and an area $c_m > 0$. Let $M(v)$ be the modules of kind $o(v)$.
- A latency bound $L$, an integer.

**Feasible solutions.** A module choice $\mu(v) \in M(v)$ for each $v$, and a schedule $s : V \to \{0, 1, \ldots\}$ with $s(v) \ge s(u) + d_{\mu(u)}$ for each edge $(u, v)$ and $s(v) + d_{\mu(v)} \le L$ for each $v$. Units are not pipelined and there is no chaining.

**Objective.** The design needs
$$a_m(\mu, s) = \max_{0 \le j < L} \left|\{ v : \mu(v) = m,\ s(v) \le j < s(v) + d_m \}\right|$$
instances of module $m$. Minimize the area $\sum_m c_m\, a_m(\mu, s)$.

**Decision form.** Given the input and an area $A$, is there a feasible choice and schedule with area at most $A$?

A feasible choice exists exactly when $L$ is at least the critical path computed with the fastest module of each kind, see the [critical path method](/critical-path-method/).

## Variants

- **Least latency under an area bound.** Swap the roles: the area is bounded and the latency is minimized, as in [resource-constrained scheduling](/resource-constrained-scheduling/).
- **Pipelined modules.** A pipelined module of latency $d_m$ accepts a new operation every step, so it is busy only in step $s(v)$.
- **Shared multi-function units.** An ALU implements several kinds at once. Then a module serves operations of different kinds, and the area count mixes kinds.
- **Chaining and clock period.** With [operation chaining](/operation-chaining/), modules have delays in nanoseconds, and the choice also decides which operations fit together in one clock period.
- **Power and energy.** The cost adds the energy per operation of each module, or the problem bounds the power per step.

## Examples

**Three multiplies and an add.** Multiplies $m_1$ and $m_2$ feed an add $s$, which feeds a multiply $m_3$. The library has a fast multiplier $F$ with delay 1 and area 8, a slow multiplier $S$ with delay 2 and area 3, and an adder with delay 1 and area 1. The least area for each latency bound:

| $L$ | least area | a best design |
|---|---|---|
| 3 | 17 | two $F$ and one adder: $m_1, m_2$ in step 0, $s$ in step 1, $m_3$ in step 2 |
| 4 | 9 | one $F$ and one adder: $m_1$ in step 0, $m_2$ in step 1, $s$ in step 2, $m_3$ in step 3 |
| 5 | 7 | two $S$ and one adder: $m_1, m_2$ in steps 0 and 1, $s$ in step 2, $m_3$ in steps 3 and 4 |
| 6 | 7 | the same |
| 7 | 4 | one $S$ and one adder: $m_1$, then $m_2$, then $s$, then $m_3$ |

Below $L = 3$ nothing is feasible, since the path $m_1, s, m_3$ takes 3 steps even with $F$. At $L = 4$, mixing $S$ and $F$ costs at least $8 + 3 + 1 = 12$, more than reusing one $F$. The cheapest design jumps from 9 to 7 at $L = 5$, where two slow multipliers fit, and to 4 at $L = 7$, where one slow multiplier does all three.

## Known algorithms

- **Integer programming.** The [ILP scheduling formulation](/ilp-scheduling-formulation/) extends to module choice with a 0-1 variable for each operation, module and start step. Exact, for small graphs.
- **Start fast, then slow down.** Ishikawa and De Micheli (1991) start from the fastest modules and replace them by slower, cheaper ones on operations with slack, as long as the latency bound holds. Heuristic.
- **Scheduling with module choice.** List and force-directed schedulers can try each module of an operation and keep the one that adds the least area. Heuristic. Schedulers based on [system of difference constraints](/sdc-scheduling/) take a fixed choice and are run for several choices.
- **Dynamic programming for chains.** For a chain of operations of distinct kinds, the problem is a knapsack with integer delays, solved in $O(nL)$ time by the knapsack recurrence.

## Bounds

**Monotone in the latency.** Any design feasible for $L$ is feasible for $L + 1$, so the least area does not increase as $L$ grows. The table above shows that it falls in jumps, from 17 to 9 in one step of $L$, and not at every step.

**Lower bound.** Each kind used in $G$ needs at least one module, so the area is at least the sum, over the kinds, of the area of the smallest module of that kind. The example reaches this bound at $L = 7$.

**Upper bound on useful latency.** With $n$ operations and the slowest delay $D$, running all operations one after another on the smallest module of each kind takes at most $nD$ steps, so for $L \ge nD$ the lower bound is reached.

## Reductions

**From latency-constrained scheduling.** If each kind has exactly one module, module selection is latency-constrained scheduling, which is NP-hard. So module selection is NP-hard as well.

**From knapsack, for a chain.** Take a knapsack instance: items with values $v_i \ge 1$ and weights $w_i \ge 1$, $i = 1, \ldots, n$, a capacity $W$ and a target $T$. Build a chain $u_1 \to u_2 \to \cdots \to u_n$, where $u_i$ has its own kind with two modules: a fast one with delay 1 and area $1 + v_i$, and a slow one with delay $1 + w_i$ and area 1. Set $L = n + W$. Since each kind occurs once, every chosen module has one instance. Let $Q$ be the set of operations that get the slow module. The chain fits in $L$ steps exactly when $n + \sum_{i \in Q} w_i \le n + W$, and the area is $n + \sum_{i \notin Q} v_i$. So the area is at most $n + \sum_i v_i - T$ exactly when some set $Q$ of weight at most $W$ has value at least $T$. The instance has size polynomial in the input. The chain needs no scheduling decision, so the hardness comes from the module choice alone. The numbers $w_i$ appear as delays, and the dynamic program above is polynomial in $L$, so this reduction shows NP-hardness in the weak sense only.

## Applications

- **Datapath synthesis.** Every library offers several adders and multipliers, and synthesis tools choose among them per operation.
- **FPGA flows.** A multiply can go to a DSP block or to lookup table logic, which differ in delay and in the scarce resource they use.
- **Codesign.** At a coarser level, choosing between a hardware and a software version of a task is the same trade-off, see [hardware-software partitioning](/hardware-software-partitioning/).

## References
