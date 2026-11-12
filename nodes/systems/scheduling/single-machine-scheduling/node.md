---
tag: WGMPRW
kind: problem
slug: single-machine-scheduling
name: Scheduling jobs on one machine
aliases:
- one-machine scheduling
- single-machine sequencing
area: systems/scheduling
level: core
summary: "The family of problems 1|β|γ: order jobs on one machine for an objective such as total weighted completion time, maximum lateness or late jobs. Some are greedy, some NP-hard."
prereqs: [scheduling-notation, scheduling-problem]
see_also: [smiths-rule, weighted-completion-time, minimizing-late-jobs, moore-hodgson-algorithm, earliest-due-date-first, lawler-algorithm, total-tardiness-minimization, exchange-argument]
sources:
  - book: isbn:9783319265780
    title: Michael L. Pinedo, Scheduling, Theory, Algorithms, and Systems, fifth edition
    locator: Chapter 3, Single Machine Models (Deterministic), Sections 3.1 to 3.6, and Chapter 4
  - book: isbn:9783540695158
    title: Peter Brucker, Scheduling Algorithms, fifth edition
    locator: Chapter 4, Single Machine Scheduling Problems
  - paper: doi:10.1002/nav.3800030106
    title: Wayne E. Smith, Various optimizers for single-stage production, Naval Research Logistics Quarterly 3(1-2), 1956
    locator: pages 59 to 66 (the ratio rule for the weighted sum of completion times)
  - paper: "James R. Jackson, Scheduling a production line to minimize maximum tardiness, Research Report 43, Management Science Research Project, University of California, Los Angeles, 1955"
    locator: the whole report (the due date order for the maximum lateness)
  - paper: doi:10.1287/mnsc.15.1.102
    title: J. Michael Moore, An n job, one machine sequencing algorithm for minimizing the number of late jobs, Management Science 15(1), 1968
    locator: pages 102 to 109
  - paper: doi:10.1287/mnsc.19.5.544
    title: Eugene L. Lawler, Optimal sequencing of a single machine subject to precedence constraints, Management Science 19(5), 1973
    locator: pages 544 to 546 (the least cost last rule for 1|prec|fmax)
  - paper: doi:10.1287/mnsc.16.1.77
    title: Eugene L. Lawler and J. Michael Moore, A functional equation and its application to resource allocation and sequencing problems, Management Science 16(1), 1969
    locator: pages 77 to 84 (the pseudo-polynomial dynamic program for the weighted number of late jobs)
  - paper: doi:10.1287/moor.15.3.483
    title: Jianzhong Du and Joseph Y.-T. Leung, Minimizing total tardiness on one machine is NP-hard, Mathematics of Operations Research 15(3), 1990
    locator: pages 483 to 495
  - paper: "doi:10.1016/S0167-5060(08)70743-X"
    title: Jan Karel Lenstra, Alexander H. G. Rinnooy Kan and Peter Brucker, Complexity of machine scheduling problems, Annals of Discrete Mathematics 1, 1977
    locator: pages 343 to 362 (strong NP-hardness of 1|rj|Lmax, 1|rj|ΣCj and 1||ΣwjTj)
  - paper: "doi:10.1016/S0167-5060(08)70742-8"
    title: Eugene L. Lawler, A pseudopolynomial algorithm for sequencing jobs to minimize total tardiness, Annals of Discrete Mathematics 1, 1977
    locator: pages 331 to 342
  - paper: "doi:10.1016/S0167-5060(08)70323-6"
    title: Eugene L. Lawler, Sequencing jobs to minimize total weighted completion time subject to precedence constraints, Annals of Discrete Mathematics 2, 1978
    locator: pages 75 to 90 (NP-hardness of 1|prec|ΣwjCj)
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: Richard M. Karp, Reducibility among combinatorial problems, in Complexity of Computer Computations, 1972
    locator: pages 85 to 103 (sequencing with deadlines and penalties, NP-complete)
---

Single-machine scheduling is the family of problems in which $n$ jobs share one machine that runs one job at a time, and an order of the jobs must make some cost as small as possible. In [Graham's notation](/scheduling-notation/) these are the problems $1 \mid \beta \mid \gamma$. They are the simplest case of the [scheduling problem](/scheduling-problem/), yet they already show the full range: some are solved by one sort justified by an [exchange argument](/exchange-argument/), some by a greedy method with a heap, and some are NP-hard. This page is a map of that range for systems readers, with a status table and links to the pages that solve each case.

## In plain words

One worker has a list of tasks. Each task takes some time. A task can also have a due time, an importance, a time before which it cannot start, or tasks that must come before it. The worker does one task at a time and must pick an order. What the best order is depends on what you want. If you want people to wait as little as possible, short and important tasks go first. If you want no task to be very late, the most urgent go first. If you want as many tasks as possible to be on time, you give up some tasks on purpose. Some of these goals have a quick and exact answer. Others are so hard that no quick exact method is known.

## Definition

**Input.** $n$ jobs. Job $j$ has a processing time $p_j \ge 0$ and, depending on the problem, some of: a weight $w_j > 0$, a due date $d_j$, a release date $r_j$, and a precedence relation among the jobs.

**Schedule.** Each job $j$ gets a start time $S_j \ge r_j$, so that no two jobs overlap, and $j$ starts only after each of its predecessors completes. The completion time is $C_j = S_j + p_j$. With preemption ($pmtn$), a job may be split into pieces of total length $p_j$.

**Objective $\gamma$.** A cost of the completion times. The common ones are the makespan $C_{\max}$, the total completion time $\sum C_j$, the weighted sum $\sum w_j C_j$, the maximum lateness $L_{\max} = \max_j (C_j - d_j)$, the number of late jobs $\sum U_j$ with $U_j = [C_j > d_j]$, the total tardiness $\sum T_j$ with $T_j = \max(0, C_j - d_j)$, and their weighted forms. See [lateness and tardiness](/lateness-and-tardiness/) and [scheduling metrics](/scheduling-metrics/).

When all $r_j = 0$ and the objective does not decrease when a job finishes earlier, no idle time and no preemption is needed, and a schedule is just an order of the $n$ jobs. That is why most of the problems below are problems of choosing a permutation.

## Variants

| problem | status | method | page |
|---|---|---|---|
| $1 \| C_{\max}$ | trivial | any order without idle time, $C_{\max} = \sum p_j$ | [makespan](/makespan/) |
| $1 \| L_{\max}$ | $O(n \log n)$ | earliest due date first (Jackson 1955) | [EDD](/earliest-due-date-first/) |
| $1 \mid prec \mid L_{\max}$ | $O(n^2)$ | least cost last (Lawler 1973) | [Lawler's algorithm](/lawler-algorithm/) |
| $1 \mid r_j \mid L_{\max}$ | strongly NP-hard (Lenstra, Rinnooy Kan and Brucker 1977) | branch and bound in practice | [release dates](/scheduling-with-release-dates/) |
| $1 \mid r_j, pmtn \mid L_{\max}$ | $O(n \log n)$ | preemptive EDD among the released jobs | [release dates](/scheduling-with-release-dates/) |
| $1 \| \sum C_j$ | $O(n \log n)$ | shortest processing time first | [SPT](/shortest-processing-time-first/) |
| $1 \| \sum w_j C_j$ | $O(n \log n)$ | ratio $p_j / w_j$ order (Smith 1956) | [Smith's rule](/smiths-rule/) |
| $1 \mid prec \mid \sum w_j C_j$ | NP-hard (Lawler 1978) | 2-approximation | [Sidney decomposition](/sidney-decomposition/) |
| $1 \mid r_j \mid \sum C_j$ | strongly NP-hard (Lenstra, Rinnooy Kan and Brucker 1977) | approximation | [release dates](/scheduling-with-release-dates/) |
| $1 \mid r_j, pmtn \mid \sum C_j$ | $O(n \log n)$ | shortest remaining processing time | [SRPT](/srpt/) |
| $1 \| \sum U_j$ | $O(n \log n)$ | Moore 1968 | [Moore-Hodgson](/moore-hodgson-algorithm/) |
| $1 \| \sum w_j U_j$ | NP-hard (Karp 1972), $O(n \sum p_j)$ (Lawler and Moore 1969) | dynamic program | [weighted tardy jobs](/weighted-tardy-jobs/) |
| $1 \| \sum T_j$ | NP-hard in the ordinary sense (Du and Leung 1990), pseudo-polynomial (Lawler 1977) | dynamic program | [total tardiness](/total-tardiness-minimization/) |
| $1 \| \sum w_j T_j$ | strongly NP-hard (Lenstra, Rinnooy Kan and Brucker 1977) | branch and bound | [total tardiness](/total-tardiness-minimization/) |

The polynomial rows have short greedy algorithms: one sort, or a sort and a heap. The NP-hard rows split into two groups. $\sum w_j U_j$ and $\sum T_j$ have pseudo-polynomial algorithms, so they are easy when the times are small integers. The rows marked strongly NP-hard have no pseudo-polynomial algorithm unless P = NP; see [strong NP-hardness](/strong-np-hardness/).

## Examples

**Four jobs, five objectives.** All jobs are present at time $0$.

| job | $p_j$ | $d_j$ | $w_j$ |
|---|---|---|---|
| $a$ | 4 | 4 | 1 |
| $b$ | 1 | 7 | 3 |
| $c$ | 3 | 6 | 2 |
| $d$ | 2 | 3 | 1 |

Every order has $C_{\max} = 10$. The other objectives disagree. Over all $24$ orders:

| order | rule that gives it | $\sum C_j$ | $\sum w_j C_j$ | $L_{\max}$ | $\sum U_j$ | $\sum T_j$ |
|---|---|---|---|---|---|---|
| $b, d, c, a$ | SPT | **20** | 28 | 6 | **1** | **6** |
| $b, c, d, a$ | Smith's rule | 21 | **27** | 6 | 2 | 9 |
| $d, a, c, b$ | EDD | 27 | 56 | **3** | 3 | 8 |
| $d, c, b, a$ | Moore-Hodgson | 23 | 40 | 6 | **1** | **6** |

The bold values are the optima. SPT is the only optimum for $\sum C_j$, Smith's rule the only optimum for $\sum w_j C_j$, and the optima for $L_{\max}$ are EDD and $a, d, c, b$. The EDD order is the worst of the four for the number of late jobs: it keeps every job only a little late. Moore-Hodgson starts from EDD, sees that $a$ is late at time $6$, and drops $a$, the longest job so far, to the end. Here SPT also happens to reach one late job, which is not true in general.

## Known algorithms

- **One sort.** [SPT](/shortest-processing-time-first/), [Smith's rule](/smiths-rule/) and [EDD](/earliest-due-date-first/) each sort the jobs by one key and are proved optimal by swapping two adjacent jobs.
- **Sort and a heap.** The [Moore-Hodgson algorithm](/moore-hodgson-algorithm/) for $1 \| \sum U_j$ scans in EDD order and keeps the on-time set in a max-heap of processing times. With release dates and preemption, a heap of released jobs gives preemptive EDD and [SRPT](/srpt/).
- **Backward greedy.** [Lawler's algorithm](/lawler-algorithm/) builds the order from the end. At each step it puts last the job, among those without unscheduled successors, whose cost at the current end time is least. It works for any nondecreasing $f_j$ in $1 \mid prec \mid f_{\max}$.
- **Dynamic programming.** Lawler and Moore 1969 solve $1 \| \sum w_j U_j$ in $O(n \sum p_j)$ time over EDD prefixes and total on-time length. Lawler 1977 solves $1 \| \sum T_j$ in pseudo-polynomial time by a decomposition at the longest job.
- **Exact search.** Branch and bound and integer programs are used for the strongly NP-hard rows. For tests, a dynamic program over subsets runs in $O(2^n n)$ time for any objective that is a sum or a maximum of per-job costs.

## Bounds

- **Comparison lower bound.** The sort-based rows need $\Omega(n \log n)$ comparisons in the worst case, since with suitable data they must output a sorted order. So SPT, Smith's rule and EDD are optimal in the comparison model.
- **No idle time.** For a regular objective (one that does not decrease when any $C_j$ decreases) and no release dates, an optimal schedule without idle time exists, so the search space is the $n!$ orders.
- **Preemption.** Without release dates, preemption never helps a regular objective on one machine. With release dates it can: $1 \mid r_j, pmtn \mid \sum C_j$ is polynomial while $1 \mid r_j \mid \sum C_j$ is strongly NP-hard.

## Reductions

- **Down to one machine.** Each problem here is the case $m = 1$ of the parallel-machine problem with the same $\beta$ and $\gamma$ (see [machine environments](/machine-environments/)), so each hardness result here carries over to parallel machines.
- **Between objectives.** $1 \| \sum C_j$ is $1 \| \sum w_j C_j$ with unit weights. $1 \| \sum U_j$ is $1 \| \sum w_j U_j$ with unit weights. A schedule with $L_{\max} \le 0$ exists if and only if the optimum of $1 \| \sum U_j$ is $0$.
- **From partition and knapsack.** $1 \| \sum w_j U_j$ with $d_j = d$ for all $j$ is the [knapsack problem](/knapsack-problem/) in the form: choose the on-time jobs of total length at most $d$ with the largest weight. This gives its NP-hardness by a reduction from [partition](/partition-problem/).
- **From 3-partition.** $1 \mid r_j \mid L_{\max}$ is strongly NP-hard by a reduction from [3-partition](/three-partition/): release dates and due dates cut the time line into windows that each must hold three jobs.

## Applications

- **Batch servers.** A server that drains a queue of requests, each with a priority, uses Smith's rule for the weighted mean response time and SPT for the mean response time. This is [shortest job first](/shortest-job-first/) in an operating system.
- **Deadline systems.** A controller with tasks that have due times uses EDD to keep the worst lateness small. If it may refuse tasks, Moore-Hodgson tells it which ones to refuse so that the most tasks finish on time; see [minimizing late jobs](/minimizing-late-jobs/).
- **Bottleneck machines.** In a factory, the busiest machine often decides the throughput. The one-machine problem with release dates and delivery times is the core step of the shifting bottleneck heuristic for [job shops](/job-shop-scheduling/).

## References
