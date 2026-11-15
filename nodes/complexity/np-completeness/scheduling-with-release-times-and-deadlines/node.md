---
tag: T16ZNM
kind: problem
slug: scheduling-with-release-times-and-deadlines
name: Scheduling with release times and deadlines
aliases:
- sequencing within intervals
- sequencing with release times and deadlines
area: complexity/np-completeness
level: core
summary: Decide whether jobs with lengths, release times and deadlines can run on one machine without preemption. Strongly NP-complete, but easy with preemption or equal lengths.
prereqs: [three-partition, partition-problem, strong-np-hardness, release-time, deadline]
see_also: [single-machine-scheduling, maximum-lateness-minimization, scheduling-with-release-dates, earliest-deadline-first, earliest-due-date-first, preemptive-scheduling, three-partition, scheduling-notation]
sources:
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Theorem 3.8 (SEQUENCING WITHIN INTERVALS is NP-complete, by a reduction from PARTITION), Theorem 4.5 (it is NP-complete in the strong sense, by a reduction from 3-PARTITION) and the appendix, problem SS1
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Section 8.8, Numerical Problems (the reduction from subset sum to scheduling with release times and deadlines)
  - paper: doi:10.1016/S0167-5060(08)70743-X
    title: J. K. Lenstra, A. H. G. Rinnooy Kan and P. Brucker, Complexity of machine scheduling problems, Annals of Discrete Mathematics 1, 343 to 362 (1977)
    locator: the single-machine results, including the NP-hardness of 1|r_j|L_max
  - paper: W. A. Horn, Some simple scheduling algorithms, Naval Research Logistics Quarterly 21(1), 1974
    title: Horn, preemptive scheduling with release times by earliest deadline first
    locator: the preemptive one-machine algorithm
  - paper: M. R. Garey, D. S. Johnson, B. B. Simons and R. E. Tarjan, Scheduling unit-time tasks with arbitrary release times and deadlines, SIAM Journal on Computing 10(2), 1981
    title: Garey, Johnson, Simons and Tarjan, equal-length jobs with arbitrary release times and deadlines in polynomial time
    locator: the main algorithm
---

Scheduling with release times and deadlines asks whether a set of jobs can be run on a single machine so that each job starts no earlier than its [release time](/release-time/), ends no later than its [deadline](/deadline/), and runs without interruption, one job at a time. Garey and Johnson call it SEQUENCING WITHIN INTERVALS. It is [NP-complete](/np-complete/) in the [strong sense](/strong-np-hardness/), by a reduction from [3-partition](/three-partition/), so it has no [pseudo-polynomial](/pseudo-polynomial-time/) algorithm unless P = NP. Small changes make it easy: with preemption, or with all release times equal, an earliest-deadline rule decides it, and equal job lengths also give a polynomial-time algorithm. In the three-field notation it is the question whether $1 \mid r_j \mid L_{\max} \le 0$.

## In plain words

One machine has a list of jobs. Each job takes a fixed time, cannot start before a given moment, and must be done by a given moment. Once a job starts, it runs to the end. Is there an order that meets every limit?

If all jobs are ready at the start, run them in order of their deadlines; this is always right. If jobs may be paused and resumed, always run the job with the nearest deadline among the ready ones. But when jobs arrive at different times and cannot be paused, the machine sometimes must stay idle and wait for a job that has not arrived yet. Choosing when to wait is the hard part. No fast method is known, even when all times are small numbers.

## Definition

**Instance.** A finite set of jobs. Each job $j$ has a length $p_j \in \mathbb{Z}^+$, a release time $r_j \in \mathbb{Z}_{\ge 0}$ and a deadline $d_j \in \mathbb{Z}^+$, all in binary.

**Question.** Is there a start time $s_j$ for each job $j$ such that $r_j \le s_j$ and $s_j + p_j \le d_j$ for all $j$, and the intervals $[s_j, s_j + p_j)$ of different jobs are disjoint?

**Encoding and certificate.** All data are integers, so if a feasible schedule exists, one with integer start times exists. The order of the jobs is a certificate: start each job as early as its release time and the end of the previous job allow, and check the deadlines in $O(n)$ arithmetic operations. So the problem is in NP.

**Complexity.** The problem is NP-complete in the strong sense, by a pseudo-polynomial transformation from 3-partition (Garey and Johnson, Theorem 4.5). An earlier proof by a Karp reduction from [partition](/partition-problem/) (Garey and Johnson, Theorem 3.8) shows ordinary NP-completeness. Because the problem is strongly NP-complete, it stays NP-complete when all numbers are bounded by a polynomial in the number of jobs, and it has no pseudo-polynomial algorithm unless P = NP.

## Variants

- **Preemption allowed.** If a job may be interrupted and resumed later, the rule that always runs the released job with the earliest deadline is optimal (Horn 1974), so the problem is in P. See [earliest deadline first](/earliest-deadline-first/) and [preemptive scheduling](/preemptive-scheduling/).
- **Equal release times.** If all $r_j = 0$, running the jobs in order of deadlines with no idle time is optimal (Jackson's rule), so the problem takes $O(n \log n)$ time. See [earliest due date first](/earliest-due-date-first/).
- **Equal deadlines.** If all deadlines are equal, run the jobs in order of release times with no unnecessary idle time. This minimizes the completion time of the last job, so the problem is in P.
- **Equal lengths.** If all jobs have the same length, the problem is in P for arbitrary release times and deadlines (Garey, Johnson, Simons and Tarjan 1981). With unit lengths and integer times, earliest deadline first at each integer time is enough.
- **Few distinct values.** The reduction from partition uses only two release times and two deadlines, so the problem stays NP-complete in that case.
- **Lateness.** With due dates instead of hard deadlines, minimizing the maximum lateness on one machine with release times is $1 \mid r_j \mid L_{\max}$; see [maximum lateness minimization](/maximum-lateness-minimization/) and [scheduling with release dates](/scheduling-with-release-dates/). The question "is $L_{\max} \le 0$?" is this problem, so that version is strongly NP-hard too.

## Examples

**Preemption changes the answer.** Job A has $p = 4$, $r = 0$, $d = 6$, and job B has $p = 2$, $r = 1$, $d = 3$. Without preemption there is no feasible schedule: if A runs first it ends at 4, after the deadline of B; if B runs first it occupies $[1, 3)$ and A then ends at 7. With preemption, earliest deadline first runs A in $[0, 1)$, B in $[1, 3)$ and A again in $[3, 6)$, which meets both deadlines.

**The reduction from 3-partition on a yes-instance.** Take $m = 2$, $B = 20$ and $a = (6, 7, 7, 6, 6, 8)$, with $B/4 < a_i < B/2$ and $\sum a_i = mB = 40$. Each $a_i$ becomes a job with release time 0 and deadline $m(B + 1) - 1 = 41$. One extra job of length 1 has release time 20 and deadline 21, so it must run in $[20, 21)$. The total length is 41, so the machine is never idle, and the other jobs fill two gaps $[0, 20)$ and $[21, 41)$ of length exactly $B$:

| interval | $[0, 6)$ | $[6, 13)$ | $[13, 20)$ | $[20, 21)$ | $[21, 27)$ | $[27, 33)$ | $[33, 41)$ |
|---|---|---|---|---|---|---|---|
| job | 6 | 7 | 7 | extra | 6 | 6 | 8 |

The gaps hold the triples $\{6, 7, 7\}$ and $\{6, 6, 8\}$.

**The reduction on a no-instance.** For $a = (6, 6, 6, 6, 7, 9)$ with $B = 20$, no triple containing 9 sums to 20, so there is no 3-partition. The same construction gives a set of jobs with no feasible schedule.

**The reduction from partition.** For $a = (8, 7, 6, 5, 4)$, with total $A = 30$, make jobs of lengths $a_i$ with release time 0 and deadline $A + 1 = 31$, and one job of length 1 with release time 15 and deadline 16. The extra job splits the time line into $[0, 15)$ and $[16, 31)$, and a feasible schedule exists because $\{4, 5, 6\}$ and $\{7, 8\}$ both sum to 15. For $a = (1, 2, 7)$, with total 10, no subset sums to 5, and the jobs with the extra job in $[5, 6)$ have no feasible schedule.

## Known algorithms

- **Dynamic programming over subsets.** For each set $S$ of jobs, keep the earliest time at which all of $S$ can be finished first, in a feasible order. This takes $O(2^n n)$ time, for example about $2.1 \times 10^7$ steps for $n = 20$ jobs, on a [word RAM](/word-ram/).
- **Branch and bound.** Practical solvers for $1 \mid r_j \mid L_{\max}$ use bounds from the preemptive relaxation, which earliest deadline first solves exactly. They have no polynomial bound on the time. See [maximum lateness minimization](/maximum-lateness-minimization/).
- **Polynomial special cases.** Preemption, equal release times and equal deadlines take $O(n \log n)$ time by sorting rules, and equal lengths take polynomial time (Garey, Johnson, Simons and Tarjan 1981).

## Bounds

- **Strong NP-completeness.** NP-complete in the strong sense (Garey and Johnson, Theorem 4.5). There is no pseudo-polynomial algorithm unless P = NP.
- **Ordinary NP-completeness with two release values.** NP-complete with only two distinct release times and two distinct deadlines (the reduction from partition, Garey and Johnson Theorem 3.8).
- **Optimization.** $1 \mid r_j \mid L_{\max}$ is NP-hard (Lenstra, Rinnooy Kan and Brucker 1977), and the reduction above shows that it is strongly NP-hard.

## Reductions

- **From 3-partition (pseudo-polynomial transformation, Garey and Johnson Theorem 4.5).** For an instance $a_1, \ldots, a_{3m}$ with bound $B$, make a job of length $a_i$, release time 0 and deadline $m(B + 1) - 1$ for each $i$. For $k = 1, \ldots, m - 1$, add a job of length 1 with release time $kB + k - 1$ and deadline $kB + k$. These $m - 1$ jobs cut the time line into $m$ gaps of length $B$, and the total length equals the horizon, so each gap is filled exactly. The bounds $B/4 < a_i < B/2$ force exactly three jobs into each gap. All numbers are at most $m(B + 1)$, so the transformation keeps the numbers polynomially bounded.
- **From partition (Karp reduction, Garey and Johnson Theorem 3.8).** For numbers with an even total $A$, make jobs of lengths $a_i$ with release time 0 and deadline $A + 1$, and one job of length 1 with release time $A/2$ and deadline $A/2 + 1$. A feasible schedule exists if and only if a subset sums to $A/2$. For an odd total, output a fixed no-instance.
- **From subset sum (Karp reduction, Kleinberg and Tardos Section 8.8).** For numbers $w_i$ and target $W$, the same idea with one job of length 1 that must run in $[W, W + 1)$, and deadline $1 + \sum_i w_i$ for the others. See [subset sum](/subset-sum-problem/).
- **To maximum lateness.** Set due dates equal to deadlines and ask whether $L_{\max} \le 0$.

## Applications

- **Single-resource planning.** A machine, a runway, an operating room or a test bench that serves one job at a time, where jobs arrive at known times and have hard due times, gives this problem when jobs cannot be interrupted.
- **Real-time systems.** Non-preemptive tasks with release times and deadlines on one processor are this problem, which is why real-time schedulers prefer preemption, where [earliest deadline first](/earliest-deadline-first/) is exact.
- **Hardness of scheduling.** Many single-machine problems with release times are shown strongly NP-hard through this problem or its reduction from 3-partition; see [single-machine scheduling](/single-machine-scheduling/).

## References
