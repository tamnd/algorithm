---
tag: R0SSCD
kind: problem
slug: minimizing-weighted-completion-time
name: Minimizing weighted completion time
aliases:
- weighted sum of completion times
- single-machine weighted completion
area: techniques/greedy
level: core
summary: Order jobs on one machine to minimize the sum of weighted completion times.
prereqs: [scheduling-notation, single-machine-scheduling]
see_also: [smith-rule, shortest-job-first, optimal-tape-storage, weighted-completion-time-scheduling, exchange-argument, minimizing-maximum-lateness, minimizing-number-of-late-jobs]
sources:
  - paper: doi:10.1002/nav.3800030106
    title: Wayne E. Smith, Various optimizers for single-stage production, Naval Research Logistics Quarterly 3(1-2), 1956
    locator: pages 59 to 66
  - book: isbn:9783319265780
    title: Michael L. Pinedo, Scheduling, Theory, Algorithms, and Systems, fifth edition
    locator: Chapter 3, Single Machine Models (Deterministic), the total weighted completion time
  - book: isbn:9783540695158
    title: Peter Brucker, Scheduling Algorithms, fifth edition
    locator: Chapter 4, Single Machine Scheduling Problems
  - paper: doi:10.1016/s0167-5060(08)70323-6
    title: Eugene L. Lawler, Sequencing jobs to minimize total weighted completion time subject to precedence constraints, Annals of Discrete Mathematics 2, 1978
    locator: pages 75 to 90
  - paper: doi:10.1016/s0167-5060(08)70743-x
    title: J. K. Lenstra, A. H. G. Rinnooy Kan and P. Brucker, Complexity of machine scheduling problems, Annals of Discrete Mathematics 1, 1977
    locator: pages 343 to 362
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Problem 16-2, Scheduling to minimize average completion time
---

Minimizing weighted completion time is the problem of ordering $n$ jobs on one machine so that the sum $\sum_j w_j C_j$ of weight times completion time is as small as possible. In [three-field notation](/scheduling-notation/) it is $1 \| \sum w_j C_j$. [Smith's rule](/smith-rule/), which sorts the jobs by nonincreasing ratio $w_j / p_j$, solves it exactly in $O(n \log n)$ time. Small additions to the model, such as release dates or precedence constraints, make it NP-hard.

## In plain words

A machine has a queue of jobs, all ready now. It does one job at a time and never stops in the middle of a job. Each job has a length and an importance. A job costs its importance times the time at which it is done, and the total cost is the sum over all jobs. The question is the best order for the queue.

When all jobs are equally important, the answer is to do the short jobs first, so that the many short jobs do not wait behind a long one. When the importances differ, a long but very important job can deserve to go early. The right measure is importance per unit of length. This page is about the problem and its versions; the rule that solves it has its own page.

## Definition

**Input.** A set of $n$ jobs. Job $j$ has a processing time $p_j > 0$ and a weight $w_j \ge 0$. All jobs are available at time 0.

**Schedules.** One machine processes one job at a time, without preemption. Idle time never helps, because removing it makes every job finish no later. So a schedule is an order $\pi = (\pi_1, \ldots, \pi_n)$ of the jobs, and the job in position $i$ completes at
$$ C_{\pi_i} = \sum_{l=1}^{i} p_{\pi_l}. $$

**Objective.** Find an order that minimizes $\sum_{j} w_j C_j$.

**Equivalent forms.** Because $\sum_j w_j p_j$ does not depend on the order, minimizing $\sum_j w_j C_j$ is the same as minimizing the weighted waiting time $\sum_j w_j (C_j - p_j)$. With $W = \sum_j w_j > 0$, it is also the same as minimizing the weighted mean completion time $\frac{1}{W}\sum_j w_j C_j$.

**The key identity.** If two adjacent jobs $a$ (first) and $b$ are swapped, no other completion time changes, and the cost changes by exactly $w_a p_b - w_b p_a$. The page on [Smith's rule](/smith-rule/) derives this identity and the full proof of optimality from it.

## Variants

- **Unit weights, $1 \| \sum C_j$.** Minimize the total, or mean, completion time. [Shortest job first](/shortest-job-first/) is optimal. This is also the problem of [optimal tape storage](/optimal-tape-storage/).
- **Precedence constraints, $1 | prec | \sum w_j C_j$.** NP-hard in general (Lawler, 1978). Lawler solved series-parallel precedence in $O(n \log n)$ time, and for chains the ratio of Smith extends to the ratio of a chain prefix. Sidney's decomposition (1975) reduces the general problem to smaller pieces.
- **Release dates, $1 | r_j | \sum C_j$.** Even with unit weights, the problem is strongly NP-hard (Lenstra, Rinnooy Kan and Brucker, 1977). With preemption allowed, $1 | r_j, pmtn | \sum C_j$ is solved by shortest remaining processing time first.
- **Deadlines.** If each job must finish by a deadline, the problem $1 | \bar d_j | \sum C_j$ asks for the least total completion time among schedules that meet all deadlines. It is a different problem; see [minimizing maximum lateness](/minimizing-maximum-lateness/) for the feasibility side.
- **Parallel machines.** On $m$ identical machines, $P \| \sum C_j$ is solved by shortest job first in round-robin, but $P2 \| \sum w_j C_j$ is NP-hard (Lenstra, Rinnooy Kan and Brucker, 1977). See [weighted completion time scheduling](/weighted-completion-time-scheduling/) for the approximation results.

## Examples

**All orders of three jobs.** Let $a = (p, w) = (3, 2)$, $b = (1, 1)$, $c = (2, 4)$. The ratios $w/p$ are $2/3$, $1$ and $2$.

| order | completion times | $\sum w_j C_j$ |
| --- | --- | --- |
| $a, b, c$ | 3, 4, 6 | 34 |
| $a, c, b$ | 3, 5, 6 | 32 |
| $b, a, c$ | 1, 4, 6 | 33 |
| $b, c, a$ | 1, 3, 6 | 25 |
| $c, a, b$ | 2, 5, 6 | 24 |
| $c, b, a$ | 2, 3, 6 | 23 |

The best order is $c, b, a$, the order of decreasing ratio, with cost 23. Shortest job first ($b, c, a$) costs 25, and heaviest job first ($c, a, b$) costs 24. Both are worse here.

**Unit weights.** For $p = (4, 1, 3, 2)$ and all $w_j = 1$, shortest first gives the order with times $1, 2, 3, 4$, the completion times $1, 3, 6, 10$ and the total $20$, so the mean completion time is $5$. The reverse order gives $4, 7, 9, 10$ and the total $30$.

**A larger instance.** The [Smith's rule](/smith-rule/) page traces six jobs whose optimum is 121, against 134 for shortest first and 136 for heaviest first.

## Known algorithms

- **[Smith's rule](/smith-rule/) (WSPT).** Sort by nonincreasing $w_j / p_j$. Exact, $O(n \log n)$ time.
- **[Shortest job first](/shortest-job-first/) (SPT).** Exact for unit weights. $O(n \log n)$ time.
- **Lawler's algorithm for series-parallel precedence.** Exact, $O(n \log n)$ time, by repeated merging of the series-parallel decomposition with ratio comparisons (Lawler, 1978).
- **Dynamic programming over subsets.** For $1 | prec | \sum w_j C_j$, let $F(S)$ be the least cost of a set $S$ of jobs that is closed under predecessors and runs first. The last job $j$ of $S$ completes at $p(S) = \sum_{i \in S} p_i$, so $F(S) = \min_j \bigl(F(S \setminus \{j\}) + w_j\, p(S)\bigr)$ over the jobs $j \in S$ with no successor in $S$. This takes $O(2^n n)$ time and is only useful for small $n$.

## Bounds

- **Upper bound.** $O(n \log n)$ time for $1 \| \sum w_j C_j$, by one sort.
- **Lower bound.** In the comparison model, $\Omega(n \log n)$ comparisons are necessary to output an optimal order, because with $p_j = 1$ and distinct weights the only optimal order sorts the weights.
- **Value.** With unit weights and the jobs indexed so that $p_1 \le \cdots \le p_n$, the optimum is $\sum_{j=1}^{n} (n - j + 1)\, p_j$, because the $j$-th shortest job delays itself and the $n - j$ jobs after it.

## Reductions

- **Tape storage is the unit-weight case, and the frequency-weighted case is this problem.** Reading a file from a tape costs the sum of the lengths of the files before it and its own length. With access frequencies as weights, the expected cost of a read is $\sum_j w_j C_j / \sum_j w_j$, so [optimal tape storage](/optimal-tape-storage/) with frequencies is $1 \| \sum w_j C_j$.
- **Partition reduces to the two-machine case.** The NP-hardness of $P2 \| \sum w_j C_j$ uses the partition problem: with $w_j = p_j$, the cost depends only on how the total processing time is split between the two machines, and it is smallest when the split is even.
- **To linear programming.** The problem has linear programming formulations in completion-time variables, whose constraints describe the set of feasible completion vectors on one machine. These formulations are the base of the approximation algorithms for the NP-hard variants.

## Applications

- **Job queues.** Batch queues and print queues where a job's cost grows with its waiting time and jobs have priorities.
- **Storage layout.** Ordering files on a tape, or records in a list that is read from the front, by access frequency per unit of length.
- **Mean response time.** With unit weights the objective is the mean response time of the jobs, and shortest first is the classic rule to reduce it.

## References
