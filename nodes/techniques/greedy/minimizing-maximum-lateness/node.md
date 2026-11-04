---
tag: 5DHKKH
kind: problem
slug: minimizing-maximum-lateness
name: Minimizing maximum lateness
aliases:
- single-machine lateness scheduling
- minimize maximum lateness
area: techniques/greedy
level: core
summary: Schedule unit-or-variable jobs with deadlines on one machine to minimize the largest lateness.
prereqs: [scheduling-notation, exchange-argument]
see_also: [earliest-due-date-first, maximum-lateness-minimization, lawler-algorithm, minimizing-number-of-late-jobs, minimizing-weighted-completion-time, scheduling-with-release-dates, lateness-and-tardiness, earliest-deadline-first]
sources:
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 4.2, Scheduling to Minimize Lateness, An Exchange Argument
  - book: isbn:9783319265780
    title: Michael L. Pinedo, Scheduling, Theory, Algorithms, and Systems, fifth edition
    locator: Chapter 3, Single Machine Models (Deterministic), the maximum lateness and the EDD rule
  - book: isbn:9783540695158
    title: Peter Brucker, Scheduling Algorithms, fifth edition
    locator: Chapter 4, Single Machine Scheduling Problems
  - paper: doi:10.1287/mnsc.19.5.544
    title: Eugene L. Lawler, Optimal sequencing of a single machine subject to precedence constraints, Management Science 19(5), 1973
    locator: pages 544 to 546
  - paper: doi:10.1016/s0167-5060(08)70743-x
    title: J. K. Lenstra, A. H. G. Rinnooy Kan and P. Brucker, Complexity of machine scheduling problems, Annals of Discrete Mathematics 1, 1977
    locator: pages 343 to 362 (strong NP-hardness with release dates)
---

Minimizing maximum lateness is the problem of ordering $n$ jobs with processing times and due dates on one machine so that the largest lateness $L_{\max} = \max_j (C_j - d_j)$ is as small as possible. In [three-field notation](/scheduling-notation/) it is $1 \| L_{\max}$. The earliest due date rule, which runs the jobs in order of due date, is optimal and runs in $O(n \log n)$ time; scheduling texts call it Jackson's rule, after J. R. Jackson (1955). Its proof is the model [exchange argument](/exchange-argument/) of Kleinberg and Tardos.

## In plain words

You have a list of tasks. Each task takes some time, and each has a due date. You can work on one task at a time, and you finish a task once you start it. A task that ends after its due date is late by the difference. You want the worst delay to be as small as possible.

The answer is to do the tasks in order of due date, the most urgent first. The length of a task does not matter, and neither does how much slack it has. If two tasks are out of due-date order and next to each other, swapping them never makes the worst delay larger. So you can swap your way from any best plan to the due-date order without losing anything.

## Definition

**Input.** A set of $n$ jobs. Job $j$ has a processing time $p_j > 0$ and a due date $d_j$, a real number. All jobs are available at time 0.

**Schedules.** One machine, one job at a time, no preemption. Removing idle time never increases a completion time, so a schedule is an order $\pi$ of the jobs started at time 0 without gaps, and the job in position $i$ completes at $C_{\pi_i} = p_{\pi_1} + \cdots + p_{\pi_i}$.

**Objective.** The lateness of job $j$ is $L_j = C_j - d_j$, which is negative when the job is early. Find an order that minimizes
$$ L_{\max} = \max_{j} L_j. $$

**Related measures.** The tardiness is $T_j = \max(0, L_j)$, and $T_{\max} = \max(0, L_{\max})$, so an order that minimizes $L_{\max}$ also minimizes $T_{\max}$. All jobs meet their due dates if and only if the optimal $L_{\max}$ is at most 0. See [lateness and tardiness](/lateness-and-tardiness/).

**Theorem (earliest due date).** Every order with $d_{\pi_1} \le d_{\pi_2} \le \cdots \le d_{\pi_n}$ minimizes $L_{\max}$.

*Proof.* Call a pair of jobs $(a, b)$ an *inversion* of an order when $a$ comes before $b$ and $d_a > d_b$.

1. *All orders without inversions have the same $L_{\max}$.* Such orders differ only in the order of jobs with equal due dates, and these jobs are consecutive. Inside a block of jobs with the common due date $d$, the largest lateness is $C - d$, where $C$ is the completion time of the last job of the block, and $C$ is the same for every order of the block. Jobs outside the block keep their completion times.
2. *An order with an inversion has an adjacent inversion.* If $a$ comes before $b$ and $d_a > d_b$, then along the jobs from $a$ to $b$ the due date must drop somewhere, at two adjacent jobs.
3. *Swapping an adjacent inversion does not increase $L_{\max}$.* Let $a$ be followed directly by $b$, with $d_a > d_b$, and let $t$ be the completion time of the second of them, which is the same before and after the swap. Before the swap, $L_b = t - d_b$. After it, $b$ finishes earlier, so its lateness does not grow, and $a$ finishes at $t$, so $L'_a = t - d_a < t - d_b = L_b$. Other jobs are not affected. So the new maximum is at most the old one.
4. *Conclusion.* An optimal order $\pi^*$ exists, because there are finitely many orders. Each swap of step 3 removes exactly one inversion, the pair $(a, b)$, and keeps all others, so after at most $\binom{n}{2}$ swaps the order has no inversion and its $L_{\max}$ is at most that of $\pi^*$. By step 1, every order without inversions has this same value, so each one is optimal. $\square$

## Variants

- **Precedence constraints, $1 | prec | L_{\max}$.** Still easy. [Lawler's algorithm](/lawler-algorithm/) (1973) schedules backward: among the jobs with no unscheduled successor, it puts last the one with the smallest cost at the current end time. It solves $1 | prec | f_{\max}$ for any nondecreasing cost functions $f_j$ in $O(n^2)$ time.
- **Release dates, $1 | r_j | L_{\max}$.** Strongly NP-hard (Lenstra, Rinnooy Kan and Brucker, 1977). See [scheduling with release dates](/scheduling-with-release-dates/).
- **Release dates with preemption, $1 | r_j, pmtn | L_{\max}$.** Preemptive earliest due date, which at each moment runs the available job with the earliest due date, is optimal. This is the rule of [earliest deadline first](/earliest-deadline-first/) scheduling in real-time systems.
- **Feasibility with deadlines.** Decide whether all jobs can finish by their deadlines. The answer is yes if and only if the earliest due date order meets them all.
- **Number of late jobs, $1 \| \sum U_j$.** Count the late jobs instead of measuring the worst one. See [minimizing the number of late jobs](/minimizing-number-of-late-jobs/), which uses this rule as a subroutine.
- **Total tardiness, $1 \| \sum T_j$.** NP-hard in the ordinary sense, and not solved by the earliest due date rule.

## Examples

**Six jobs.** Let $(p_j, d_j)$ be $a = (4, 9)$, $b = (2, 4)$, $c = (3, 6)$, $d = (1, 13)$, $e = (3, 10)$, $f = (2, 8)$. The total processing time is 15.

| position | job | $p_j$ | $d_j$ | $C_j$ | $L_j$ |
| --- | --- | --- | --- | --- | --- |
| 1 | $b$ | 2 | 4 | 2 | $-2$ |
| 2 | $c$ | 3 | 6 | 5 | $-1$ |
| 3 | $f$ | 2 | 8 | 7 | $-1$ |
| 4 | $a$ | 4 | 9 | 11 | 2 |
| 5 | $e$ | 3 | 10 | 14 | 4 |
| 6 | $d$ | 1 | 13 | 15 | 2 |

The earliest due date order gives $L_{\max} = 4$, reached by job $e$. Over all $720$ orders the minimum is 4, reached by 10 orders, and the maximum is 11. Shortest processing time first ($d, b, f, c, e, a$) gives 6, and the input order $a, b, c, d, e, f$ gives 7.

**Shortest first fails.** Job 1 with $(p, d) = (1, 100)$ and job 2 with $(10, 10)$. Shortest first runs job 1 first, and job 2 is late by 1. Earliest due date runs job 2 first, and no job is late.

**Least slack first fails.** The slack of a job is $d_j - p_j$. Job 1 with $(1, 2)$ has slack 1, and job 2 with $(10, 10)$ has slack 0. Least slack first runs job 2 and then job 1, which completes at 11 and is late by 9. Earliest due date runs job 1 and then job 2, with $L_{\max} = 1$.

## Known algorithms

- **[Earliest due date first](/earliest-due-date-first/) (EDD, Jackson's rule).** Sort by due date. Exact for $1 \| L_{\max}$, $O(n \log n)$ time.
- **[Lawler's algorithm](/lawler-algorithm/).** Exact for $1 | prec | f_{\max}$, $O(n^2)$ time.
- **Preemptive EDD.** Exact for $1 | r_j, pmtn | L_{\max}$, $O(n \log n)$ time with a priority queue.
- **Branch and bound.** For the NP-hard $1 | r_j | L_{\max}$, branch and bound with the preemptive EDD value as the lower bound is the classic exact method.

## Bounds

- **Upper bound.** $O(n \log n)$ time in the comparison model for $1 \| L_{\max}$. If the jobs are given sorted by due date, $\Theta(n)$ time to compute the schedule and its $L_{\max}$.
- **The value.** With the jobs indexed by due date, $L_{\max} = \max_{k} \bigl( \sum_{i \le k} p_i - d_k \bigr)$. This is also a lower bound for every order, with its own proof: for each $k$, the last of the $k$ jobs with the earliest due dates finishes at time at least $\sum_{i \le k} p_i$, and its due date is at most $d_k$.

## Reductions

- **Deadlines as a special case.** Feasibility with deadlines is the question $L_{\max} \le 0$, so it reduces to this problem.
- **Inside other algorithms.** The algorithm of [Moore and Hodgson](/minimizing-number-of-late-jobs/) for the number of late jobs works on the earliest due date order and removes jobs from it.

## Applications

- **Meeting deadlines.** Ordering orders in a workshop or tasks in a project so that the worst delay is smallest.
- **Real-time systems.** The preemptive version is the earliest deadline first policy of [real-time scheduling](/real-time-scheduling/).
- **Teaching.** Kleinberg and Tardos use this problem to introduce the exchange argument, in contrast to the stays-ahead proof of interval scheduling.

## References
