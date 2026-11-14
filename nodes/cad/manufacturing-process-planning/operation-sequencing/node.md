---
tag: 3RDNRM
kind: problem
slug: operation-sequencing
name: Operation sequencing
aliases:
- machining operation sequencing
area: cad/manufacturing-process-planning
level: core
summary: Order the machining operations of a part under precedence from features, datums and tools, so tool changes and setup time are small.
prereqs: [traveling-salesman-problem]
see_also: [setup-planning, precedence-constrained-scheduling, computer-aided-process-planning, topological-sort, genetic-algorithm, cutting-sequence-planning, toolpath-planning, feature-recognition]
sources:
  - paper: doi:10.1080/002075499191409
    title: S. V. Bhaskara Reddy, M. S. Shunmugam and T. T. Narendran, Operation sequencing in CAPP using genetic algorithms, International Journal of Production Research 37(5), 1999, 1063 to 1074
    locator: operation sequencing under the precedence of form features, solved with a genetic algorithm whose coding and crossover keep the precedence
  - paper: doi:10.1080/00207540310001652897
    title: W. D. Li, S. K. Ong and A. Y. C. Nee, Optimization of process plans using a constraint-based tabu search approach, International Journal of Production Research 42(10), 2004, 1955 to 1985
    locator: the process plan model with a machine, a tool and a tool approach direction for each operation, the cost with machine, tool, setup and change terms, and the precedence constraints
  - paper: doi:10.1023/a:1008779125567
    title: Norbert Ascheuer, Michael Jünger and Gerhard Reinelt, A branch and cut algorithm for the asymmetric traveling salesman problem with precedence constraints, Computational Optimization and Applications 17(1), 2000, 61 to 84
    locator: exact solution of the sequencing problem with precedence constraints and asymmetric transition costs
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: Richard M. Karp, Reducibility among combinatorial problems, in Complexity of Computer Computations, Plenum, 1972, 85 to 103
    locator: the NP-completeness of the Hamiltonian circuit problem, which makes the traveling salesman problem NP-hard
  - paper: doi:10.1016/0304-3975(77)90012-3
    title: Christos H. Papadimitriou, The Euclidean travelling salesman problem is NP-complete, Theoretical Computer Science 4(3), 1977, 237 to 244
    locator: the NP-completeness of the TSP with Euclidean distances, used for the hole sequencing case
---

Operation sequencing puts the machining operations of a part in order. Each operation uses a tool, in a setup, at a place on the part. Some orders are not allowed: a datum face must be cut before the features measured from it, a hole is center drilled before it is drilled and drilled before it is reamed, and roughing comes before finishing. Among the allowed orders, the planner wants one with little time lost between operations: few tool changes, few setup changes and short moves of the tool. The precedence makes the allowed orders the linear extensions of a partial order, and the change costs make the problem a [traveling salesman problem](/traveling-salesman-problem/) with precedence constraints. This page states the problem, shows that it is NP-hard, and works a small example to its optimum.

## In plain words

A part may need twenty operations: face the top, rough a pocket, drill four holes, ream two of them, mill a slot on the side. Some must come before others, because a hole cannot be reamed before it is drilled. Many orders still remain.

The orders do not all take the same time. Each time the machine swaps a tool, it loses some seconds. Each time the part must be turned and clamped again, it loses minutes. So the planner wants an order that uses each tool in as few runs as it can, finishes one side of the part before the next, and moves the tool short distances. The task is to find, among the orders that respect the precedence, the one with the least lost time.

## Definition

There is no standard formal statement of operation sequencing. The following version covers the cited work, with the operations already chosen.

**Input.**
- A set $O = \{o_1, \dots, o_n\}$ of operations. Operation $o$ has a tool $\tau(o)$, a setup $\delta(o)$ (an orientation of the part, from [setup planning](/setup-planning/)), and a start and an end position of the tool.
- A precedence relation $\prec$ on $O$, a partial order: $o \prec o'$ means that $o$ must come before $o'$.
- A transition cost $c(o, o') \ge 0$ for each ordered pair. A common form is
$$c(o, o') = w_t\,[\tau(o) \ne \tau(o')] + w_s\,[\delta(o) \ne \delta(o')] + \operatorname{move}(o, o'),$$
with $w_t$ the time of a tool change, $w_s$ the time of a setup change, $[\cdot]$ equal to 1 when the condition holds and 0 otherwise, and $\operatorname{move}$ the time of the rapid move from the end of $o$ to the start of $o'$.

**Output.** An order $\pi = (\pi_1, \dots, \pi_n)$ of $O$ that is a linear extension of $\prec$: if $o \prec o'$, then $o$ comes before $o'$.

**Objective.** Minimize $\sum_{i=1}^{n-1} c(\pi_i, \pi_{i+1})$.

**Where the precedence comes from.** The usual sources are datums (a face before the features measured from it), the chain of a feature (center drill, drill, ream, chamfer), roughing before finishing, interacting features (a hole whose entry is in the floor of a pocket comes after the pocket), and good practice, such as a hole before a thread in it.

The problem differs from [precedence-constrained scheduling](/precedence-constrained-scheduling/): that problem assigns jobs to several machines to make the schedule short, while operation sequencing orders the operations on one machine and pays a cost that depends on which operation follows which.

## Variants

- **Tool changes only.** $w_s = 0$ and no move cost. With no precedence, the answer is trivial: group the operations by tool, with one change fewer than the number of tools.
- **Setups and tool changes.** The weighted cost above, with $w_s$ much larger than $w_t$, so the plan first keeps the setup changes few.
- **Alternatives.** Each operation may be done on one of several machines, with one of several tools, from one of several approach directions. Li, Ong and Nee (2004) choose the machine, the tool and the approach direction of each operation together with the order, with costs for each machine and tool and for each change of machine, tool and setup.
- **Hole sequencing.** Many holes are made with the same tool, and only the move cost matters. This is a traveling salesman path through the holes, and the [cutting sequence planning](/cutting-sequence-planning/) page treats the related problem for profile cutting.
- **Integrated planning.** Operation sequencing joined with [setup planning](/setup-planning/), machine choice and scheduling of the shop.

## Examples

**Nine operations on a block.** A block has a top face, two holes $A$ and $B$, a pocket and a side slot. Hole $B$ starts in the floor of the pocket. Tool change $w_t = 1$ and setup change $w_s = 10$, in minutes, with no move cost.

| operation | meaning | tool | setup |
|---|---|---|---|
| FM | face mill the top | T1 face mill | $+z$ |
| RP | rough the pocket | T4 end mill 10 mm | $+z$ |
| FP | finish the pocket | T5 end mill 6 mm | $+z$ |
| CDA, CDB | center drill holes $A$, $B$ | T2 spot drill | $+z$ |
| DRA, DRB | drill holes $A$, $B$ | T3 drill | $+z$ |
| CHA | chamfer hole $A$ | T2 spot drill | $+z$ |
| SL | mill the side slot | T4 end mill 10 mm | $+x$ |

Precedence: FM before every other $+z$ operation (the top is the datum), CDA before DRA before CHA, CDB before DRB, RP before FP, and RP before CDB (hole $B$ starts in the pocket floor).

- *Feature by feature.* FM, CDA, DRA, CHA, RP, FP, CDB, DRB, SL. The tools run T1, T2, T3, T2, T4, T5, T2, T3, T4: 8 tool changes and 1 setup change, cost 18.
- *Optimum.* FM, RP, CDA, CDB, DRA, DRB, FP, CHA, SL. The tools run T1, T4, T2, T3, T5, T2, T4: 6 tool changes and 1 setup change, cost 16.

A check of all 945 orders that respect the precedence finds 16 as the minimum, reached by 32 orders. A short argument gives the same bound. The plan has two setups, so at least one setup change. Five tools need at least 4 changes. Tool T2 must be loaded twice, because DRA with T3 comes between CDA and CHA. Tool T4 must also be loaded twice: SL is the only operation in its setup, and with one setup change it is first or last, while RP comes after FM and before FP, so RP is never first or last in setup $+z$ and cannot be next to SL. That gives at least 7 runs of one tool, so at least 6 tool changes.

## Known algorithms

- **Search over orders.** List the linear extensions of $\prec$, for example with an extension of [topological sort](/topological-sort/), and keep the cheapest. The number of linear extensions can be $n!$.
- **Dynamic programming over downsets.** A state is a downset $I$ of $\prec$ (the operations done so far, closed under predecessors) and the last operation. The best cost of a state is the minimum over its last step, as in the Held and Karp method for the TSP. If $\prec$ has width $w$, it splits into $w$ chains by Dilworth's theorem, and a downset is fixed by how many operations of each chain it holds, so there are at most $(n + 1)^w$ downsets. The time is $O((n + 1)^w\, n^2)$, polynomial for a fixed width.
- **Branch and cut.** The problem with a fixed first and last operation is the asymmetric TSP with precedence constraints. Ascheuer, Jünger and Reinelt (2000) solve it exactly with branch and cut.
- **Heuristics and metaheuristics.** Rules such as "finish the current setup and the current tool first", and search methods that keep the precedence: [genetic algorithms](/genetic-algorithm/) (Bhaskara Reddy, Shunmugam and Narendran 1999), tabu search (Li, Ong and Nee 2004) and [simulated annealing](/simulated-annealing/).

There are no standard benchmarks for operation sequencing. Papers test their methods on example parts of their own, so their results cannot be compared from paper to paper.

## Bounds

**NP-hardness.** The decision version with general transition costs is NP-hard by a reduction from the [traveling salesman problem](/traveling-salesman-problem/), which is NP-hard because the Hamiltonian circuit problem is NP-complete (Karp 1972). Given cities $1, \dots, n$ with distances $d$, make an operation per city, a start operation $s$ and an end operation $e$ at city 1, with $s$ before all and $e$ after all, and $c(o_i, o_j) = d(i, j)$, so an order costs exactly the length of the matching tour. With all tools and setups equal and the move cost a Euclidean distance, the same reduction from the Euclidean TSP, which is NP-complete (Papadimitriou 1977), shows that hole sequencing alone is NP-hard. Here $s$ and $e$ are at the place of city 1.

**Easy cases.** With no precedence and only the tool change cost, grouping by tool is optimal, since each tool must be loaded at least once. With precedence of fixed width, the dynamic program above is polynomial.

**Open in the cited sources.** The cited sources give no hardness result for the version whose only cost is the number of tool changes under precedence, so none is stated here.

## Reductions

- **From the TSP.** As above.
- **To the TSP with precedence.** An instance is an asymmetric TSP path with precedence constraints on its nodes, also called the sequential ordering problem. Add a dummy node with cost 0 to and from every operation, and put it before every operation in the precedence. A tour that starts at the dummy node is then a path through the operations with the same cost.

## Applications

- **Process planning.** After [setup planning](/setup-planning/), a [process planning](/computer-aided-process-planning/) system orders the operations of each setup and writes them to the operation sheet.
- **CAM.** The order fixes the tool list and the sequence of [toolpaths](/toolpath-planning/) in the NC program, and the rapid moves between them.
- **Machining centers with tool magazines.** The tool change time is the main cost between operations on one setup, so fewer runs per tool give a direct saving in cycle time.

## References
