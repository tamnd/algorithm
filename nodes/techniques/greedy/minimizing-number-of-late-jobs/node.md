---
tag: PAQY2H
kind: problem
slug: minimizing-number-of-late-jobs
name: Minimizing the number of late jobs
aliases:
- maximum number of on-time jobs
- unit-weight late jobs
area: techniques/greedy
level: core
summary: Choose the largest set of jobs that can all meet their deadlines on one machine.
prereqs: [minimizing-maximum-lateness, scheduling-notation]
see_also: [earliest-due-date-first, lateness-and-tardiness, job-sequencing-with-deadlines, minimizing-weighted-completion-time, priority-queue, knapsack-problem, pseudo-polynomial-time, exchange-argument]
sources:
  - paper: doi:10.1287/mnsc.15.1.102
    title: J. Michael Moore, An n job, one machine sequencing algorithm for minimizing the number of late jobs, Management Science 15(1), 1968
    locator: pages 102 to 109
  - paper: doi:10.1287/mnsc.16.1.77
    title: Eugene L. Lawler and J. Michael Moore, A functional equation and its application to resource allocation and sequencing problems, Management Science 16(1), 1969
    locator: pages 77 to 84
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: Richard M. Karp, Reducibility among combinatorial problems, in Complexity of Computer Computations, 1972
    locator: pages 85 to 103 (the sequencing problem with penalties)
  - book: isbn:9783319265780
    title: Michael L. Pinedo, Scheduling, Theory, Algorithms, and Systems, fifth edition
    locator: Chapter 3, Single Machine Models (Deterministic), the number of tardy jobs
  - book: isbn:9783540695158
    title: Peter Brucker, Scheduling Algorithms, fifth edition
    locator: Chapter 4, Single Machine Scheduling Problems
---

Minimizing the number of late jobs is the problem of ordering $n$ jobs with processing times and due dates on one machine so that as few jobs as possible finish after their due dates. In [three-field notation](/scheduling-notation/) it is $1 \| \sum U_j$, where $U_j = 1$ if job $j$ is late and $0$ otherwise. Equivalently, it asks for the largest set of jobs that can all finish on time. The Moore-Hodgson algorithm solves it in $O(n \log n)$ time: it scans the jobs by due date and, each time the current job would be late, drops the longest job kept so far. With weights, $1 \| \sum w_j U_j$ is NP-hard.

## In plain words

You have tasks with lengths and due dates, and one worker. Some tasks will be late no matter what. You want as many tasks as possible to be on time. The late ones can wait until the end, so the real question is which tasks to keep.

Go through the tasks by due date and keep each one. When the task you just added would finish late, throw out the longest task you have kept so far, which may be the new one. Throwing out the longest task frees the most time for the tasks still to come, and it costs only one task, which is the same cost as throwing out any other.

The kept tasks, done by due date, are all on time, and no other plan keeps more.

## Definition

**Input.** A set $J$ of $n$ jobs. Job $j$ has a processing time $p_j > 0$ and a due date $d_j$. All jobs are available at time 0, and one machine processes one job at a time without preemption.

**Objective.** For an order of the jobs without idle time, job $j$ completes at $C_j$ and is late when $C_j > d_j$. Find an order that minimizes the number of late jobs $\sum_j U_j$.

**Feasible sets.** A set $S \subseteq J$ is *feasible* if its jobs can be ordered so that all of them are on time. By the theorem on [minimizing maximum lateness](/minimizing-maximum-lateness/), $S$ is feasible if and only if its jobs in order of due date are all on time. An optimal schedule runs a feasible set of the largest size in due date order and the other jobs after it in any order, so the problem is the same as finding a largest feasible set.

**The Moore-Hodgson algorithm.** Index the jobs so that $d_1 \le d_2 \le \cdots \le d_n$. Start with $S_0 = \emptyset$. For $k = 1, \ldots, n$: let $S = S_{k-1} \cup \{k\}$. If $p(S) \le d_k$, set $S_k = S$. Otherwise remove from $S$ one job $l$ with the largest processing time, and set $S_k = S \setminus \{l\}$. Here $p(S) = \sum_{j \in S} p_j$. The answer is $S_n$.

**Theorem.** For each $k$, $S_k$ is a feasible subset of $\{1, \ldots, k\}$ of the largest size. Moreover, for each $j \le |S_k|$, the $j$ shortest jobs of $S_k$ have the least total processing time among all feasible subsets of $\{1, \ldots, k\}$ with $j$ jobs.

*Proof.* Write $m_k = |S_k|$, and $\sigma_j(X)$ for the sum of the $j$ smallest processing times in a set $X$. A subset of a feasible set is feasible, because removing jobs from the due date order only makes the other jobs finish earlier. Induction on $k$; the case $k = 0$ is trivial. Assume the claim for $k - 1$ and let $A = S_{k-1}$, $m = m_{k-1}$.

1. *Lower bound.* Let $T \subseteq \{1, \ldots, k\}$ be feasible with $|T| = j$. If $k \notin T$, then $T$ is a feasible subset of $\{1, \ldots, k-1\}$, so $j \le m$ and $p(T) \ge \sigma_j(A)$. If $k \in T$, then $T \setminus \{k\}$ is feasible with $j - 1$ jobs, so $j - 1 \le m$ and $p(T) \ge \sigma_{j-1}(A) + p_k$. In both cases $p(T) \ge \sigma_j(A \cup \{k\})$, because the $j$ smallest of $A \cup \{k\}$ either leave out $k$ or are $k$ and the $j - 1$ smallest of $A$.
2. *Case $p(A) + p_k \le d_k$.* The jobs of $A$ are on time in due date order, and $k$ has the largest due date so far, so it can go last and completes at $p(A) + p_k \le d_k$. So $S_k = A \cup \{k\}$ is feasible. No feasible subset of $\{1, \ldots, k\}$ has more than $m + 1$ jobs, because removing $k$ would give a feasible subset of $\{1, \ldots, k-1\}$ with more than $m$ jobs. The $j$ shortest jobs of $S_k$ form a feasible set with total $\sigma_j(A \cup \{k\})$, which meets the lower bound of step 1.
3. *Case $p(A) + p_k > d_k$: the largest size is $m$.* A feasible $T \subseteq \{1, \ldots, k\}$ with $m + 1$ jobs must contain $k$, and by step 1, $p(T) \ge \sigma_{m+1}(A \cup \{k\}) = p(A) + p_k > d_k$. In the due date order of $T$, job $k$ can go last, and it completes at $p(T) > d_k$. So $T$ is not feasible, a contradiction. The set $S_k$ has $m$ jobs.
4. *Case $p(A) + p_k > d_k$: $S_k$ is feasible.* If the removed job is $k$, then $S_k = A$. Otherwise $p_l \ge p_k$ and $l \in A$. The jobs of $A \setminus \{l\}$ finish no later than in $A$. Job $k$ completes at $p(A) - p_l + p_k \le p(A)$. Since $A$ is feasible, its last job completes at $p(A)$ by its due date, which is at most $d_k$. So $k$ is on time.
5. *Case $p(A) + p_k > d_k$: least totals.* The $j$ shortest jobs of $S_k$, for $j \le m$, are the $j$ shortest jobs of $A \cup \{k\}$, because only a longest job was removed. They form a feasible set, as a subset of $S_k$, and their total $\sigma_j(A \cup \{k\})$ meets the lower bound of step 1. $\square$

For $k = n$, the theorem says that $S_n$ is a largest feasible set, so the algorithm is optimal. The proof needs the second, stronger claim: the induction must know that the kept set is as short as possible, not only as large as possible.

## Variants

- **Weighted late jobs, $1 \| \sum w_j U_j$.** Each late job costs its weight. The problem is NP-hard: it is one of the problems in Karp's 1972 list, and the [knapsack problem](/knapsack-problem/) reduces to it when all due dates are equal. Lawler and Moore (1969) solve it by dynamic programming in $O(n \sum_j p_j)$ time, which is [pseudo-polynomial](/pseudo-polynomial-time/).
- **Unit processing times with weights, $1 | p_j = 1 | \sum w_j U_j$.** Easy again: the feasible sets form a matroid, and a greedy algorithm by weight is optimal. This is [job sequencing with deadlines](/job-sequencing-with-deadlines/).
- **Equal processing times.** If all $p_j$ are equal, every removed job is as long as any other, and the algorithm reduces to dropping any job when an overflow occurs.
- **Maximum lateness instead.** If the goal is the worst delay, not the count, the earliest due date order alone is optimal. See [minimizing maximum lateness](/minimizing-maximum-lateness/).
- **Total tardiness, $1 \| \sum T_j$.** Measures how late the jobs are, not how many. It is NP-hard, and the Moore-Hodgson rule does not solve it. See [lateness and tardiness](/lateness-and-tardiness/).

## Examples

**Seven jobs.** Let $(p_j, d_j)$ be $a = (2, 3)$, $b = (4, 5)$, $c = (3, 7)$, $d = (5, 9)$, $e = (1, 10)$, $f = (4, 12)$, $g = (2, 13)$, already in due date order.

| step | job | $(p, d)$ | $p(S)$ with the job | late? | removed | kept set after the step | $p$ of kept set |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | $a$ | $(2, 3)$ | 2 | no | | $a$ | 2 |
| 2 | $b$ | $(4, 5)$ | 6 | yes, $6 > 5$ | $b$ | $a$ | 2 |
| 3 | $c$ | $(3, 7)$ | 5 | no | | $a, c$ | 5 |
| 4 | $d$ | $(5, 9)$ | 10 | yes, $10 > 9$ | $d$ | $a, c$ | 5 |
| 5 | $e$ | $(1, 10)$ | 6 | no | | $a, c, e$ | 6 |
| 6 | $f$ | $(4, 12)$ | 10 | no | | $a, c, e, f$ | 10 |
| 7 | $g$ | $(2, 13)$ | 12 | no | | $a, c, e, f, g$ | 12 |

The schedule is $a, c, e, f, g$ (completing at 2, 5, 6, 10, 12), followed by the late jobs $b$ and $d$. Five jobs are on time. Over all subsets, 5 is the largest feasible size, and $\{a, c, e, f, g\}$ is the only feasible set of that size. The earliest due date order of all seven jobs, without removals, has 6 late jobs.

**Dropping the late job fails.** A tempting rule drops the job that would be late, not the longest one. Take $(p, d) = (4, 4)$, $(1, 5)$, $(1, 5)$, $(1, 5)$. Dropping the current late job keeps $(4, 4)$ and one short job: 2 on time. The Moore-Hodgson algorithm drops $(4, 4)$ when the second short job overflows and keeps the three short jobs: 3 on time.

## Known algorithms

- **Moore-Hodgson.** Sort by due date, then scan with a max-[priority queue](/priority-queue/) of the kept jobs keyed by processing time and a running total. Each job is inserted once and removed at most once, so the time is $O(n \log n)$ and the space $O(n)$.
- **Lawler and Moore dynamic programming.** For the weighted problem, with jobs in due date order, let $F_k(t)$ be the least weight of late jobs among the first $k$ jobs when the on-time jobs among them have total time $t$. Then $F_k(t) = \min(F_{k-1}(t) + w_k,\ F_{k-1}(t - p_k))$, where the second choice is allowed only when $t \le d_k$. This takes $O(n \sum_j p_j)$ time.
- **Brute force.** Check all $2^n$ subsets for feasibility in due date order. Useful only as a test oracle.

## Bounds

- **Upper bound.** $O(n \log n)$ time in the comparison model for $1 \| \sum U_j$. If the jobs are given in due date order, the scan still uses $O(n \log n)$ time for the priority queue.
- **Weighted case.** NP-hard in the ordinary sense, and solvable in pseudo-polynomial time $O(n \sum_j p_j)$.

## Reductions

- **Knapsack reduces to the weighted problem.** With a common due date $D$ for all jobs, a set is on time if and only if its total processing time is at most $D$. So minimizing the weight of late jobs is the same as maximizing the weight of a set of total size at most $D$, which is the 0-1 [knapsack problem](/knapsack-problem/) with capacity $D$. This shows that the weighted problem is NP-hard.
- **Uses earliest due date as a subroutine.** Feasibility of a set is tested by the [earliest due date](/earliest-due-date-first/) order, and the algorithm builds this order step by step.

## Applications

- **Order acceptance.** A workshop that cannot meet all due dates chooses the largest set of orders it can deliver on time, and declines or renegotiates the rest.
- **Overloaded real-time systems.** When not all tasks can meet their deadlines, keep the most tasks that can.
- **Teaching.** The algorithm shows a greedy rule whose proof needs a stronger invariant than the claim itself: the kept set must be both largest and shortest.

## References
