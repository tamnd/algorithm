---
tag: 192FEE
kind: problem
slug: minimizing-tardy-jobs
name: Minimizing the number of tardy jobs
aliases:
- 1||sum Uj
- Moore's problem
- maximizing the number of on-time jobs
area: approximation/scheduling-approximation
level: core
summary: Order jobs with due dates on one machine so that the fewest finish late. Moore-Hodgson solves 1||sum Uj in O(n log n); release dates or two machines make it NP-hard and not approximable in ratio.
prereqs: [lateness-and-tardiness, earliest-due-date-first, priority-queue]
see_also: [minimizing-number-of-late-jobs, moore-hodgson-algorithm, weighted-tardy-jobs, maximum-lateness-minimization, total-tardiness-minimization, job-sequencing-with-deadlines, scheduling-with-release-times-and-deadlines, scheduling-with-rejection]
sources:
  - paper: doi:10.1287/mnsc.15.1.102
    title: J. Michael Moore, An n job, one machine sequencing algorithm for minimizing the number of late jobs, Management Science 15(1), 1968
    locator: pages 102 to 109 (the algorithm, with the shorter form due to Hodgson)
  - paper: doi:10.1287/mnsc.16.1.77
    title: Eugene L. Lawler and J. Michael Moore, A functional equation and its application to resource allocation and sequencing problems, Management Science 16(1), 1969
    locator: pages 77 to 84 (the weighted case by dynamic programming)
  - paper: "Jan Karel Lenstra, Alexander H. G. Rinnooy Kan and Peter Brucker, Complexity of machine scheduling problems, Annals of Discrete Mathematics 1, 1977"
    locator: pages 343 to 362 (strong NP-hardness of 1|r_j|sum Uj)
  - paper: "Hiroshi Kise, Toshihide Ibaraki and Hisashi Mine, A solvable case of the one-machine scheduling problem with ready and due times, Operations Research 26(1), 1978"
    locator: pages 121 to 126 (release dates and due dates in the same order)
  - book: isbn:9783319265780
    title: Michael L. Pinedo, Scheduling, Theory, Algorithms, and Systems, fifth edition
    locator: Chapter 3, Single Machine Models (Deterministic), the number of tardy jobs
  - book: isbn:9783540695158
    title: Peter Brucker, Scheduling Algorithms, fifth edition
    locator: Chapter 4, Single Machine Scheduling Problems (the number of late jobs)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability
    locator: Appendix A5.1, problems SS1 to SS3
---

Minimizing the number of tardy jobs asks for an order of $n$ jobs on one machine with the fewest jobs that complete after their due dates. In the [three-field notation](/scheduling-notation/) it is $1 \| \sum_j U_j$, where $U_j = 1$ for a [late job](/lateness-and-tardiness/). Late jobs may as well go last, so the problem is to choose the largest set of jobs that can all be on time. The Moore-Hodgson algorithm (1968) solves it exactly in $O(n \log n)$ time. Small changes make it hard: weights, release dates or a second machine. In the hard versions the optimum can be 0, so the count of late jobs has no approximation algorithm with a finite ratio, and approximation results are stated for the number of on-time jobs instead. The [greedy page on this problem](/minimizing-number-of-late-jobs/) proves Moore-Hodgson by an invariant. This page gives a different proof, by deletion of one job, and the complexity of the variants.

## In plain words

You have jobs with lengths and due dates, and one worker. You want as many jobs as possible to be done on time. Jobs that are late anyway can wait until the end, so the question is which jobs to keep.

Go through the jobs by due date and keep each one. When the job you just added would finish late, throw out the longest job you have kept, which may be the new one. Throwing out the longest job costs one job, like any other choice, and frees the most time for the jobs that follow.

## Definition

**Input.** Jobs $1, \ldots, n$ with processing times $p_j \ge 0$ and due dates $d_j$, all available at time 0, and one machine.

**Output.** An order $\sigma$ of the jobs, run back to back from time 0. Job $j$ completes at $C_j$, and $U_j = 1$ if $C_j > d_j$.

**Goal.** Minimize $\sum_j U_j$.

A set $S$ of jobs is **feasible** if some order runs all of $S$ on time. By the [EDD theorem](/earliest-due-date-first/), $S$ is feasible if and only if its jobs in order of due date are all on time, which means $p(\{i \in S : i \preceq j\}) \le d_j$ for each $j \in S$, where $\preceq$ is the EDD order. An optimal schedule runs a largest feasible set in EDD order, followed by the other jobs. A subset of a feasible set is feasible.

## Variants

| problem | status |
|---|---|
| $1 \| \sum U_j$ | $O(n \log n)$, Moore-Hodgson |
| $1 \| \sum w_j U_j$ | NP-hard, pseudo-polynomial; see [weighted tardy jobs](/weighted-tardy-jobs/) |
| $1 \mid p_j = 1 \mid \sum w_j U_j$ | greedy by weight; [job sequencing with deadlines](/job-sequencing-with-deadlines/) |
| $1 \mid r_j \mid \sum U_j$ | strongly NP-hard (Lenstra, Rinnooy Kan and Brucker 1977) |
| $1 \mid r_j \mid \sum U_j$, $r_i < r_j \Rightarrow d_i \le d_j$ | $O(n^2)$ (Kise, Ibaraki and Mine 1978) |
| $1 \mid r_j, pmtn \mid \sum U_j$ | polynomial, by dynamic programming (Lawler 1990) |
| $1 \mid prec, p_j = 1 \mid \sum U_j$ | NP-hard (Garey and Johnson, SS2) |
| $P2 \| \sum U_j$ | NP-hard, from [partition](/partition-problem/) |
| $P \| \sum U_j$ | strongly NP-hard, from [3-partition](/three-partition/) |

**Minimization and maximization.** The two forms "fewest late jobs" and "most on-time jobs" have the same optimal schedules, but not the same approximation behavior. See the section Bounds.

## Examples

**Seven jobs.** Take the jobs below, already in EDD order.

| step $k$ | $p_k$ | $d_k$ | total with $k$ | late? | removed | kept set |
|---|---|---|---|---|---|---|
| 0 | 4 | 5 | 4 | no | | 0 |
| 1 | 3 | 6 | 7 | yes | 0 ($p = 4$) | 1 |
| 2 | 2 | 7 | 5 | no | | 1, 2 |
| 3 | 6 | 10 | 11 | yes | 3 ($p = 6$) | 1, 2 |
| 4 | 1 | 12 | 6 | no | | 1, 2, 4 |
| 5 | 5 | 14 | 11 | no | | 1, 2, 4, 5 |
| 6 | 2 | 15 | 13 | no | | 1, 2, 4, 5, 6 |

The schedule is $1, 2, 4, 5, 6$, completing at $3, 5, 6, 11, 13$, and then the late jobs $0$ and $3$. So $\sum U_j = 2$. A search over all $5040$ orders confirms that 2 is optimal.

**Dropping the new job is wrong.** Take $p = (6, 3, 4)$ and $d = (6, 7, 8)$. A rule that keeps the jobs it has and drops each new job that would be late keeps job 0 and drops jobs 1 and 2: two late jobs. Moore-Hodgson drops job 0, the longest, when job 1 overflows. Then jobs 1 and 2 complete at 3 and 7, both on time, and only one job is late.

**A hard instance with optimum 0.** Two machines and a common due date $D = 5$, with $p = (3, 2, 2, 3)$. All jobs are on time exactly when the jobs split into two sets of sum 5, here $\{3, 2\}$ and $\{2, 3\}$. With $p = (4, 3, 3)$ and $D = 5$, no split exists and the optimum is 1.

## Known algorithms

**Moore-Hodgson.** Moore (1968) gave the algorithm, and the short form below is due to Hodgson.

```pseudo id=main
MOORE-HODGSON(p[1 .. n], d[1 .. n])
L1  sort the jobs so that d[1] ≤ d[2] ≤ ... ≤ d[n]
L2  E ← empty max-heap keyed by p, t ← 0
L3  for k ← 1 to n do
L4      insert k into E, t ← t + p[k]
L5      if t > d[k] then remove the job ℓ with the largest p from E, t ← t − p[ℓ]
L6  return the jobs of E in EDD order, then the other jobs
```

The value $t$ is always $p(E)$. Each job enters and leaves the heap at most once, so the time is $O(n \log n)$ and the space is $O(n)$.

**Proof of optimality, by deletion of one job.** We use induction on $n$. Index the jobs in EDD order. If line L5 never removes a job, then all jobs are on time and the schedule is optimal. Otherwise let $k$ be the first step where line L5 removes a job. Before step $k$ nothing was removed, so $E = \{1, \ldots, k\}$ at line L5, $p(\{1, \ldots, j\}) \le d_j$ for all $j < k$, and $p(\{1, \ldots, k\}) > d_k$. Let $\ell$ be the job removed, the longest of $1, \ldots, k$.

1. *Some largest feasible set does not contain $\ell$.* Let $S$ be a largest feasible set with $\ell \in S$. The set $\{1, \ldots, k\}$ is not feasible, since in EDD order job $k$ completes at $p(\{1, \ldots, k\}) > d_k$. So some $i \le k$ is not in $S$. Let $S' = S - \{\ell\} + \{i\}$, and note $p_i \le p_\ell$. Run $S'$ in EDD order and check each $j \in S'$. If $j < k$, then $j$ completes by $p(\{1, \ldots, j\}) \le d_j$. If $j > k$, then $j \in S$ and $j$ comes after both $i$ and $\ell$, so its completion time changes by $p_i - p_\ell \le 0$. If $j = k \in S$, the same holds. If $j = k = i$, then $\ell < k$, and $k$ completes at $p(S \cap \{1, \ldots, k-1\}) - p_\ell + p_k \le p(S \cap \{1, \ldots, k-1\})$, which is the completion time in $S$ of the last job of $S$ before $k$, so it is at most that job's due date and at most $d_k$. So $S'$ is feasible and as large as $S$.
2. *The algorithm on $J - \{\ell\}$ is the same run.* Run the algorithm on the jobs other than $\ell$. For $j < k$, $j \ne \ell$, the totals are at most $p(\{1, \ldots, j\}) \le d_j$, so nothing is removed. If $\ell = k$, the run has no step $k$. If $\ell \ne k$, then $k \ge 2$, and at step $k$ the total is $p(\{1, \ldots, k-1\}) + p_k - p_\ell \le p(\{1, \ldots, k-1\}) \le d_{k-1} \le d_k$, so again nothing is removed. After step $k$ both runs hold the same set $\{1, \ldots, k\} - \{\ell\}$ and the same $t$, so from then on they make the same choices, given the same tie rule. The run on $J$ returns $\ell$ as late and otherwise the output of the run on $J - \{\ell\}$.
3. *Conclusion.* By the induction hypothesis, the run on $J - \{\ell\}$ returns a largest feasible subset of $J - \{\ell\}$. By step 1, a largest feasible subset of $J$ avoids $\ell$, so it has the same size. So the run on $J$ returns a largest feasible set of $J$. ∎

The tests of this page compare the algorithm with a search over all orders for $n \le 6$, and with a search over all $2^n$ subsets with the EDD test for $n \le 10$.

**Other algorithms.**

- The [Lawler-Moore dynamic program](/weighted-tardy-jobs/) for $1 \| \sum w_j U_j$ in $O(n \sum_j p_j)$ time, and an FPTAS for it.
- For $1 \mid r_j \mid \sum U_j$, branch and bound and integer programming. Kise, Ibaraki and Mine (1978) give an $O(n^2)$ algorithm when release dates and due dates are in the same order.

## Bounds

- **Upper bound.** $O(n \log n)$ time for $1 \| \sum U_j$. Deciding whether $\sum U_j = 0$ takes one EDD pass after the sort.
- **No ratio for the hard minimization variants.** For $1 \mid r_j \mid \sum U_j$, the question "is $\sum U_j = 0$?" is [sequencing with release times and deadlines](/scheduling-with-release-times-and-deadlines/), which is strongly NP-complete. For $P2 \| \sum U_j$ with a common due date, it is [partition](/partition-problem/). An algorithm with a finite [approximation ratio](/approximation-ratio/) $\alpha$ must return 0 when the optimum is 0, so it would decide these questions. Hence no such algorithm runs in polynomial time unless P = NP.
- **The maximization form.** Maximizing the number of on-time jobs, also called throughput, has no such barrier, since its optimum is positive whenever any single job can be on time. Constant-factor approximations are known for it with release dates and on several machines, for example by Bar-Noy, Guha, Naor and Schieber (2001).

## Reductions

- **To the maximum lateness test.** A set is feasible if and only if EDD has $L_{\max} \le 0$ on it. See [maximum lateness](/maximum-lateness-minimization/).
- **From partition to $P2 \| \sum U_j$.** Numbers $a_1, \ldots, a_n$ with sum $2B$ become jobs with $p_j = a_j$ and $d_j = B$ on two machines. All jobs are on time if and only if the numbers split into two halves of sum $B$. The same idea with 3-partition and $m$ machines gives strong NP-hardness of $P \| \sum U_j$.
- **From knapsack to the weighted version.** With a common due date, the on-time jobs are a knapsack of capacity $d$. See [weighted tardy jobs](/weighted-tardy-jobs/).
- **To scheduling with rejection.** Declaring a job late is like rejecting it at the cost $w_j$. See [scheduling with rejection](/scheduling-with-rejection/).

## Applications

- **Order acceptance.** A shop that cannot meet all due dates picks the most orders it can deliver on time and renegotiates the others.
- **Overload in real-time systems.** When not all tasks can meet their deadlines, keep the most tasks that can.
- **A subroutine.** The algorithm gives a lower bound on the number of late jobs in branch and bound methods for harder variants.

## References
