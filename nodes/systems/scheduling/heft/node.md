---
tag: PKPCT3
kind: algorithm
slug: heft
name: Heterogeneous earliest finish time
aliases:
- HEFT
- HEFT list scheduling
area: systems/scheduling
level: research
summary: A list-scheduling heuristic for task graphs on processors of different speeds. It orders tasks by upward rank and puts each one on the processor where it finishes first.
solves: [precedence-constrained-scheduling]
model: word-ram
complexity:
  vars: {n: the number of tasks, e: the number of edges, q: the number of processors}
  time: {worst: O(n^2 q + e q), average: O(n^2 q + e q), best: Θ(n q + e q)}
  space: {extra: Θ(n q + e)}
properties: {deterministic: true, online: false, recursive: false}
history:
  year: 2002
  people: [Haluk Topcuoglu, Salim Hariri, Min-You Wu]
  note: Topcuoglu, Hariri and Wu gave HEFT and the related CPOP heuristic for task graphs on heterogeneous processors.
prereqs: [list-scheduling, critical-path-method, directed-acyclic-graph]
see_also: [precedence-constrained-scheduling, unrelated-machine-scheduling-makespan, critical-path, critical-path-lower-bound, resource-constrained-project-scheduling, graham-anomalies, work-stealing, topological-sort]
sources:
  - paper: doi:10.1109/71.993206
    title: Haluk Topcuoglu, Salim Hariri and Min-You Wu, Performance-effective and low-complexity task scheduling for heterogeneous computing, IEEE Transactions on Parallel and Distributed Systems 13(3), 2002
    locator: pages 260 to 274 (the HEFT algorithm with the upward rank and the insertion-based policy, its time bound, the ten-task example on three processors, and CPOP)
  - paper: doi:10.1145/344588.344618
    title: Yu-Kwong Kwok and Ishfaq Ahmad, Static scheduling algorithms for allocating directed task graphs to multiprocessors, ACM Computing Surveys 31(4), 1999
    locator: pages 406 to 471 (the model of task graphs with communication costs, and list-scheduling heuristics with priorities from path lengths)
  - paper: "doi:10.1016/S0022-0000(75)80008-0"
    title: J. D. Ullman, NP-complete scheduling problems, Journal of Computer and System Sciences 10(3), 1975
    locator: pages 384 to 393 (scheduling a precedence graph of unit-time tasks on identical processors is NP-complete)
---

Heterogeneous earliest finish time (HEFT) is a heuristic of Topcuoglu, Hariri and Wu (2002) that schedules a task graph on processors of different speeds, with a cost for data that moves between processors. It is a [list scheduling](/list-scheduling/) method in two phases. First it gives each task an *upward rank*, the length of the longest path from the task to the end of the graph with mean costs, and sorts the tasks by decreasing rank. Then it takes the tasks in this order and puts each one on the processor where it finishes earliest, counting the data transfers and allowing the task to fill an idle gap left between tasks already there. Even the case of identical processors and no transfers is NP-hard, so HEFT has no optimality guarantee; it is a fast and widely used baseline. The [precedence-constrained scheduling page](/precedence-constrained-scheduling/) of the approximation area covers algorithms with proved ratios on identical machines; this page is the systems heuristic for heterogeneous machines.

## In plain words

A program is split into tasks, and some tasks need the results of others. There are several processors, and each task runs faster on some of them than on others. Moving a result from one processor to another takes time, but on the same processor it is free. First, give each task a score: roughly how long the work that still depends on it will take, from this task down to the end. Tasks with more work behind them are more urgent. Then go through the tasks from most urgent to least. For each task, try every processor: see when its inputs can arrive there, find the first free time that is long enough, and see when the task would end. Put the task where it ends first. This is quick and usually good, but it does not always find the best schedule.

## The algorithm

**Model.** A directed acyclic graph of $n$ tasks and $e$ edges, and $q$ processors. Task $i$ takes $w_{i,p}$ on processor $p$. An edge $(i, j)$ means that $j$ needs the output of $i$; the transfer takes $c_{i,j}$ if the two tasks run on different processors and $0$ on the same one. A processor runs one task at a time, without preemption, and transfers overlap with computation. Let $\bar w_i$ be the mean of $w_{i,p}$ over the processors. In the paper the transfer time also depends on the pair of processors, and the rank uses its mean; the code here uses one value per edge.

**Upward rank.** $\operatorname{rank}_u(i) = \bar w_i + \max_{(i, j)} \big(c_{i,j} + \operatorname{rank}_u(j)\big)$, and $\operatorname{rank}_u(i) = \bar w_i$ for an exit task.

```pseudo id=main
HEFT(w[1 .. n][1 .. q], c, edges)
L1  for each task i in reverse topological order do rank[i] ← mean of w[i][·] + max over edges (i, j) of c[i, j] + rank[j]   (0 if none)
L2  λ ← the tasks in decreasing rank, ties in topological order
L3  for each task i in λ do
L4      for each processor p do
L5          ready ← max over edges (j, i) of AFT[j] + (0 if proc[j] = p else c[j, i])   (0 if none)
L6          EST[p] ← the start of the first idle gap on p, at or after ready, that is at least w[i][p] long
L7          EFT[p] ← EST[p] + w[i][p]
L8      p* ← the first p with the least EFT[p]; proc[i] ← p*; AST[i] ← EST[p*]; AFT[i] ← EFT[p*]
L9  return proc, AST, AFT
```

Line L1 is phase 1, the prioritizing; lines L3 to L8 are phase 2, the processor selection. AST and AFT are the actual start and finish times. Line L6 is the insertion-based policy: a task may go into a gap between two tasks that are already on $p$, if it fits there after its inputs arrive. The last gap, after the last task on $p$, has no end, so line L6 always finds a start.

## Example

The example of Topcuoglu, Hariri and Wu: ten tasks $n_1, \ldots, n_{10}$ on three processors $P_1, P_2, P_3$.

| task | $w$ on $P_1$ | $w$ on $P_2$ | $w$ on $P_3$ | $\bar w$ | successors with $c$ |
|---|---|---|---|---|---|
| $n_1$ | 14 | 16 | 9 | 13 | $n_2$: 18, $n_3$: 12, $n_4$: 9, $n_5$: 11, $n_6$: 14 |
| $n_2$ | 13 | 19 | 18 | 16.67 | $n_8$: 19, $n_9$: 16 |
| $n_3$ | 11 | 13 | 19 | 14.33 | $n_7$: 23 |
| $n_4$ | 13 | 8 | 17 | 12.67 | $n_8$: 27, $n_9$: 23 |
| $n_5$ | 12 | 13 | 10 | 11.67 | $n_9$: 13 |
| $n_6$ | 13 | 16 | 9 | 12.67 | $n_8$: 15 |
| $n_7$ | 7 | 15 | 11 | 11 | $n_{10}$: 17 |
| $n_8$ | 5 | 11 | 14 | 10 | $n_{10}$: 11 |
| $n_9$ | 18 | 12 | 20 | 16.67 | $n_{10}$: 13 |
| $n_{10}$ | 21 | 7 | 16 | 14.67 | |

**Phase 1.** From the exit task up: $\operatorname{rank}_u(n_{10}) = 14.67$, $\operatorname{rank}_u(n_8) = 10 + 11 + 14.67 = 35.67$, $\operatorname{rank}_u(n_9) = 44.33$, $\operatorname{rank}_u(n_7) = 42.67$, $\operatorname{rank}_u(n_2) = 16.67 + \max(19 + 35.67,\ 16 + 44.33) = 77$, and so on up to $\operatorname{rank}_u(n_1) = 13 + \max(18 + 77,\ 12 + 80,\ 9 + 80,\ 11 + 69,\ 14 + 63.33) = 108$. The ranks of $n_3, n_4, n_5, n_6$ are $80, 80, 69, 63.33$. Line L2 gives the order $n_1, n_3, n_4, n_2, n_5, n_6, n_9, n_7, n_8, n_{10}$; the tie between $n_3$ and $n_4$ goes to $n_3$, which comes first in the topological order.

**Phase 2.** The finish time that line L7 computes on each processor, and the choice of line L8:

| step | task | EFT on $P_1$ | EFT on $P_2$ | EFT on $P_3$ | chosen | runs |
|---|---|---|---|---|---|---|
| 1 | $n_1$ | 14 | 16 | 9 | $P_3$ | 0 to 9 |
| 2 | $n_3$ | 32 | 34 | 28 | $P_3$ | 9 to 28 |
| 3 | $n_4$ | 31 | 26 | 45 | $P_2$ | 18 to 26 |
| 4 | $n_2$ | 40 | 46 | 46 | $P_1$ | 27 to 40 |
| 5 | $n_5$ | 52 | 39 | 38 | $P_3$ | 28 to 38 |
| 6 | $n_6$ | 53 | 42 | 47 | $P_2$ | 26 to 42 |
| 7 | $n_9$ | 69 | 68 | 76 | $P_2$ | 56 to 68 |
| 8 | $n_7$ | 58 | 83 | 49 | $P_3$ | 38 to 49 |
| 9 | $n_8$ | 62 | 79 | 73 | $P_1$ | 57 to 62 |
| 10 | $n_{10}$ | 102 | 80 | 97 | $P_2$ | 73 to 80 |

At step 3, $n_4$ on $P_2$ waits for the output of $n_1$ from $P_3$, ready at $9 + 9 = 18$, and ends at $18 + 8 = 26$. On $P_3$ there is no transfer, but $P_3$ is busy with $n_3$ until $28$, so $n_4$ would end at $28 + 17 = 45$. At step 7, $n_9$ needs data from $n_2$ on $P_1$ (ready at $40 + 16 = 56$ on $P_2$), from $n_4$ and from $n_5$; on $P_2$ it starts at $56$. The makespan is $80$, as in the paper. In this example no task goes into an earlier gap.

**HEFT is not optimal.** Three tasks on two processors: $t_1$ takes $4$ on $P_1$ and $3$ on $P_2$, $t_2$ takes $2$ and $6$, $t_3$ takes $1$ and $7$, with edges $t_1 \to t_2$ of cost $2$ and $t_1 \to t_3$ of cost $6$. The ranks are $13.5, 4, 4$. Line L8 puts $t_1$ on $P_2$, since $3 < 4$. Then $t_2$ ends at $3 + 2 + 2 = 7$ on $P_1$, and $t_3$ ends at $10$ on both processors and goes to $P_1$, from $9$ to $10$. The makespan is $10$. All three tasks on $P_1$ take $4 + 2 + 1 = 7$ with no transfer, and $7$ is optimal. The greedy choice for $t_1$ ignores the transfers it causes later.

## Correctness

HEFT is a heuristic, so correctness here means that it always returns a valid schedule, and that line L1 computes the longest-path ranks it claims. For each edge $(i, j)$, $\operatorname{rank}_u(i) \ge c_{i,j} + \operatorname{rank}_u(j) \ge \operatorname{rank}_u(j)$, and an equal rank is broken by the topological order, so the order of line L2 is a topological order. So when line L5 handles task $i$, all its predecessors are placed, and the start that line L6 chooses is at least the arrival time of every input. Line L6 picks a start in a gap that holds the whole task, so the tasks on one processor never overlap. The full proof, with the gap search, is on the proof page.

## Complexity

- **Time.** Line L1 handles each task and edge once, $O(n q + e)$, and line L2 sorts, $O(n \log n)$. In phase 2, line L5 looks at each edge once for each processor, $O(e q)$ in total. Line L6 scans the busy list of $p$, which has at most $n$ entries, so it costs $O(n)$ for each task and processor, $O(n^2 q)$ in total. Topcuoglu, Hariri and Wu state $O(e \cdot q)$ for a dense graph, where $e$ is of order $n^2$.
- **Space.** $\Theta(n q + e)$ for the costs, the graph and the busy lists.

## Properties

- **Not optimal.** The small example above gives $10$ where $7$ is optimal. With identical processors and no transfers the problem is already NP-hard (Ullman 1975).
- **No approximation guarantee.** Change the small example so that $t_1$ takes $1 + \varepsilon$ on $P_1$ and $1$ on $P_2$, and has $k$ children that each take $1$ on $P_1$, a very large time on $P_2$, and a transfer cost $C$. HEFT puts $t_1$ on $P_2$ and ends at $1 + C + k$, while all tasks on $P_1$ end at $1 + \varepsilon + k$. As $C$ grows, the ratio grows without bound.
- **Static.** It needs the whole graph and all costs before it starts.
- **Deterministic.** The ties in lines L2 and L8 must be fixed for the result to be reproducible; this page uses the topological order and the lowest processor index.
- **Ranks.** The rank of an entry task with the largest rank is the mean-cost length of a longest path, a rough estimate of the critical path, not a lower bound on the makespan.
- **Same machines.** With identical processors and no transfer costs, HEFT is list scheduling with the longest-path priority and gap filling.

## Variants and improvements

- **CPOP.** In the same paper, Critical-Path-on-a-Processor uses the sum of upward and downward rank as priority, and puts every task of the critical path on the one processor that runs that whole path fastest.
- **Without insertion.** Line L6 can append the task after the last one on $p$. This costs $O(1)$ per processor and gives the $O(e q)$ bound, but loses the gaps.
- **Other rank weights.** The mean $\bar w_i$ can be replaced by the median, the best or the worst time, or a weighted mean by processor speed.
- **Lookahead.** Choose the processor by the effect on the successors, not by the task's own finish time alone. This targets the failure in the small example.
- **Task duplication.** Run a parent task again on the processor of its child to avoid a transfer.

## When to use it

Use HEFT for static schedules of a workflow or task graph on a set of different processors, such as CPUs and GPUs on one node or machines of different kinds in a cluster, when the run times and transfer sizes can be estimated in advance. It is a simple, strong baseline for new heuristics. If the costs are not known in advance or change at run time, a dynamic method such as [work stealing](/work-stealing/) on the ready tasks is often better. If the processors are identical and there are no transfers, plain list scheduling with the longest-path priority is the same algorithm with less code.

## Pitfalls

- **Wrong rank direction.** The rank goes from the task down to the exit. Using the downward rank with a decreasing sort gives an order that is not topological.
- **Ties.** Tasks with equal rank must be ordered so that a predecessor comes first; with zero costs a parent and its child can have the same rank.
- **Forgetting that same-processor transfers are free.** Line L5 adds $c_{j,i}$ only for a predecessor on another processor.
- **Gap search.** A gap must hold the whole task after its inputs arrive, not only start inside it.
- **Contention.** The model lets any number of transfers run at once. On a shared network, the real schedule can be much longer.
- **Estimates.** HEFT trusts its cost table. Bad estimates give a bad schedule, and the static schedule does not adapt.

## Implementations

## History

Topcuoglu, Hariri and Wu published HEFT and CPOP in IEEE Transactions on Parallel and Distributed Systems in 2002, and compared them with earlier heuristics for heterogeneous processors on random graphs and on graphs from applications. HEFT builds on list scheduling with priorities from path lengths, a family of heuristics that the survey of Kwok and Ahmad (1999) reviews.

## References
