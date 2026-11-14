---
tag: JR7CA6
kind: problem
slug: hardware-software-partitioning
name: Hardware-software partitioning
aliases:
- hardware/software codesign partitioning
- HW/SW partitioning
area: eda/high-level-synthesis-and-scheduling
level: advanced
summary: Split the tasks of a system between software on a processor and custom hardware to meet timing at the least cost, as in the Vulcan and COSYMA codesign systems.
prereqs: [knapsack-problem, control-data-flow-graph]
see_also: [module-selection, interface-synthesis, min-cut-problem, fractional-knapsack, simulated-annealing, kernighan-lin, binary-integer-programming, amdahls-law]
sources:
  - paper: doi:10.1109/54.232470
    title: Rajesh K. Gupta and Giovanni De Micheli, Hardware-software cosynthesis for digital systems, IEEE Design and Test of Computers 10(3), 29 to 41, 1993
    locator: whole paper (the Vulcan system, which starts from an all-hardware design and moves operations to software under timing constraints)
  - paper: "Rolf Ernst, Jörg Henkel and Thomas Benner, Hardware-software cosynthesis for microcontrollers, IEEE Design and Test of Computers 10(4), 64 to 75, 1993"
    locator: whole paper (the COSYMA system, which starts from an all-software design and moves basic blocks to hardware by simulated annealing)
  - paper: "Harold S. Stone, Multiprocessor scheduling with the aid of network flow algorithms, IEEE Transactions on Software Engineering SE-3(1), 1977"
    locator: whole paper (the assignment of program modules to two processors with communication costs as a minimum cut)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Appendix A6, problem MP9, Knapsack
---

Hardware-software partitioning decides, for each task of a system, whether it runs as software on a processor or as a custom hardware block, such as a coprocessor made by [high-level synthesis](/high-level-synthesis/). Hardware is faster but costs area, and moving data between the two sides costs time. The goal is the least running time within an area budget, or the least area that meets a deadline. With an area budget, the problem contains the [knapsack problem](/knapsack-problem/) and is NP-hard. With communication costs but no budget, it is a [minimum cut](/min-cut-problem/) and takes polynomial time. The codesign systems Vulcan (Gupta and De Micheli, 1993) and COSYMA (Ernst, Henkel and Benner, 1993) attacked it from opposite ends.

## In plain words

A gadget has many jobs to do. Each job can run as a program on a cheap general processor, or as a special circuit that is much faster but takes chip area. The chip area is limited. If two jobs that talk a lot sit on different sides, the data must cross between processor and circuit, which costs time too. The task is to choose which jobs become circuits so that the whole gadget is as fast as possible without going over the area limit. It is like packing a bag: each job that becomes a circuit takes room and saves time, and the bag has a fixed size.

## Definition

**Input.**

- A set of $n$ tasks. Task $i$ takes time $s_i \ge 0$ in software and $h_i \ge 0$ in hardware, and its hardware version has area $a_i \ge 0$.
- A communication cost $c_{ij} \ge 0$ for each pair of tasks, paid when $i$ and $j$ are on different sides. It is 0 for tasks that do not exchange data.
- An area budget $A$.

**Feasible solutions.** A set $H$ of tasks to put in hardware, with $\sum_{i \in H} a_i \le A$. The other tasks run in software.

**Objective.** The processor and the hardware run one task at a time, so the time is
$$t(H) = \sum_{i \notin H} s_i + \sum_{i \in H} h_i + \sum_{\{i, j\} :\ |\{i, j\} \cap H| = 1} c_{ij}.$$
Minimize $t(H)$.

**Decision form.** Given the input and a time $K$, is there a feasible $H$ with $t(H) \le K$?

The *gain* of task $i$ is $g_i = s_i - h_i$, the time saved by moving it to hardware. With no communication costs, $t(H) = \sum_i s_i - \sum_{i \in H} g_i$, so the problem is to choose tasks of largest total gain within the area budget.

## Variants

- **Least area for a deadline.** Fix the time bound $K$ and minimize $\sum_{i \in H} a_i$. Vulcan works in this form.
- **Concurrent execution.** The processor and the hardware run at the same time, so the time is the length of a schedule of the task graph, as in [resource-constrained scheduling](/resource-constrained-scheduling/), not a sum.
- **Several processors and accelerators.** Each task picks one of several targets, which is a form of [module selection](/module-selection/) at the system level.
- **Granularity.** The tasks can be processes, functions, loops or basic blocks. COSYMA partitions basic blocks, and finer grains give more choices and more communication.
- **Shared hardware.** Two tasks in hardware may share units, so the area of $H$ is less than the sum of the $a_i$. Then the cost depends on a later [resource binding](/resource-binding/).
- **Energy.** The objective is the energy, with a deadline, for battery-powered devices.

## Examples

**Four tasks.** The tasks, with software time, hardware time and area, are $P = (9, 2, 5)$, $Q = (6, 1, 4)$, $R = (4, 1, 2)$ and $S = (7, 3, 3)$, with no communication costs. All in software takes $9 + 6 + 4 + 7 = 26$. The gains are $7, 5, 3, 4$. The best time for each budget:

| budget $A$ | best $H$ | time |
|---|---|---|
| 5 | $\{P\}$ or $\{R, S\}$ | 19 |
| 6 | $\{Q, R\}$ | 18 |
| 7 | $\{P, R\}$ | 16 |
| 9 | $\{Q, R, S\}$ or $\{P, Q\}$ | 14 |
| 14 | all four | 7 |

The task with the best gain per unit of area is $R$ (3 per 2), then $P$ (7 per 5), $S$ (4 per 3) and $Q$ (5 per 4). Taking tasks in this order while they fit gives $\{R, S\}$ with time 19 for budget 6, while $\{Q, R\}$ gives 18. So the order by gain per area is not optimal.

**Communication.** Add a cost $c_{QR} = 4$ to the example. With budget 6, $\{Q, R\}$ still takes 18, since both are in hardware and pay nothing. With budget 4, $\{Q\}$ takes $26 - 5 + 4 = 25$ and $\{R\}$ takes $26 - 3 + 4 = 27$, and $\{S\}$ takes $26 - 4 = 22$, the best. Communication makes tasks that talk prefer the same side.

## Known algorithms

- **Dynamic programming.** With no communication costs, the knapsack recurrence over the budget is exact in $O(nA)$ time for integer areas, which is pseudo-polynomial. See the [knapsack problem](/knapsack-problem/).
- **Greedy by gain per area.** Fast, and exact for the fractional relaxation, see [fractional knapsack](/fractional-knapsack/). The example shows it is not exact for whole tasks.
- **Integer programming.** A 0-1 variable per task, and one per communicating pair, gives exact solutions for moderate sizes, see [0-1 integer programming](/binary-integer-programming/).
- **Minimum cut.** With no area budget, exact in polynomial time, as shown below.
- **Moves from all hardware.** Vulcan (Gupta and De Micheli, 1993) starts with everything in hardware and moves operations to software while the timing constraints hold. Heuristic.
- **Moves from all software.** COSYMA (Ernst, Henkel and Benner, 1993) starts with everything in software and moves basic blocks to hardware by [simulated annealing](/simulated-annealing/) until the time constraint holds. Heuristic.
- **Local search.** Moves in the style of [Kernighan-Lin](/kernighan-lin/) swap tasks between the sides to reduce the communication. Heuristic.

## Bounds

**Lower bound.** Every partition takes at least $\sum_i \min(s_i, h_i)$, which is reached when the budget allows every task its faster side and there are no communication costs.

**Fractional bound.** With no communication costs, the best gain is at most the gain of the fractional relaxation, in which a task may be split. Taking tasks by gain per area and a fraction of the first that does not fit gives that relaxation. In the example with budget 6, it takes $R$ and $4/5$ of $P$, for a gain of $3 + 5.6 = 8.6$, so no partition beats a time of $26 - 8.6 = 17.4$. The best is 18.

**Approximation.** With no communication costs, the better of the greedy set and the single task of largest gain that fits has at least half of the best gain, as for the knapsack problem, and the knapsack approximation schemes apply to the gain.

## Reductions

**From knapsack, so NP-hard.** Take a knapsack instance with values $v_i$, weights $w_i$, capacity $W$ and target $T$. Make task $i$ with $s_i = v_i$, $h_i = 0$ and $a_i = w_i$, no communication costs, and budget $A = W$. Then $t(H) = \sum_i v_i - \sum_{i \in H} v_i$, and $H$ fits the budget exactly when its weight is at most $W$. So some $H$ has $t(H) \le \sum_i v_i - T$ exactly when some set of weight at most $W$ has value at least $T$. The construction takes linear time, and a partition is checked in polynomial time, so the decision form is NP-complete. The areas carry the numbers of the knapsack instance, so this shows NP-hardness in the weak sense, matching the pseudo-polynomial dynamic program.

**To minimum cut, with no budget.** Take $A = \sum_i a_i$, so every $H$ fits. Build a network with a source $\sigma$ for software and a sink $\tau$ for hardware, an arc $\sigma \to i$ of capacity $h_i$ and an arc $i \to \tau$ of capacity $s_i$ for each task, and arcs $i \to j$ and $j \to i$ of capacity $c_{ij}$ for each pair. For a cut with the side $X \ni \sigma$, put the tasks of $X$ in software and the others in $H$. The cut contains $i \to \tau$ for each software task, $\sigma \to i$ for each hardware task, and one arc of capacity $c_{ij}$ for each pair split by the cut. So the cut capacity is exactly $t(H)$, and a [minimum cut](/min-cut-problem/) gives an optimal partition. This is Stone's construction (1977) for assigning modules to two processors.

## Applications

- **Embedded systems.** Codesign tools choose which functions of a controller, a codec or a signal chain become accelerators.
- **FPGA systems on chip.** Chips with a processor and programmable logic let the designer move functions between the two, and the partition is redone as the design evolves.
- **Accelerator offload.** The choice of which kernels go to a GPU or an accelerator, with the data transfer cost, is the same problem with the bus as the communication cost. The speedup is limited by the software part, as in [Amdahl's law](/amdahls-law/).

## References
