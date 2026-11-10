---
tag: 9Q08CA
kind: algorithm
slug: earliest-due-date-first
name: Earliest due date first (EDD)
aliases:
- EDD rule
- Jackson's rule
area: approximation/scheduling-approximation
level: intro
summary: Process jobs in order of due dates; optimal for the maximum lateness and the maximum tardiness on one machine, and an exact test of whether all deadlines can be met.
solves: [maximum-lateness-minimization]
model: word-ram
complexity:
  vars: {n: the number of jobs}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, online: false, recursive: false}
history:
  year: 1955
  people: [James R. Jackson]
  note: Jackson proved in a 1955 UCLA research report that the due date order minimizes the maximum lateness on one machine.
prereqs: [lateness-and-tardiness, scheduling-notation, sorting-problem]
see_also: [minimizing-maximum-lateness, maximum-lateness-minimization, lawler-algorithm, minimizing-tardy-jobs, scheduling-with-release-dates, shortest-processing-time-first, exchange-argument, earliest-deadline-first]
sources:
  - paper: "James R. Jackson, Scheduling a production line to minimize maximum tardiness, Research Report 43, Management Science Research Project, University of California, Los Angeles, 1955"
    locator: the whole report
  - book: isbn:9783319265780
    title: Michael L. Pinedo, Scheduling, Theory, Algorithms, and Systems, fifth edition
    locator: Chapter 3, Single Machine Models (Deterministic), the maximum lateness and the EDD rule
  - book: isbn:9783540695158
    title: Peter Brucker, Scheduling Algorithms, fifth edition
    locator: Chapter 4, Single Machine Scheduling Problems, minimax criteria
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Chapter 4, Section 4.2 (scheduling to minimize lateness, an exchange argument)
---

Earliest due date first (EDD), also called Jackson's rule, runs the jobs on one machine in order of their due dates. It solves $1 \| L_{\max}$ in the [three-field notation](/scheduling-notation/): it minimizes the largest [lateness](/lateness-and-tardiness/) $L_{\max} = \max_j (C_j - d_j)$. The same order minimizes the largest tardiness, and it meets all due dates whenever some order does, so it is also the standard test of whether a set of jobs fits before its deadlines. This page proves optimality with a lower bound that holds even for preemptive schedules. The [greedy page on the same problem](/minimizing-maximum-lateness/) gives the [exchange argument](/exchange-argument/) proof.

## In plain words

You have tasks with lengths and due dates, and one worker. A task that ends after its due date is late by the difference. You want the worst delay to be as small as possible.

Do the tasks in order of due date, the most urgent first. Look at the task that ends up worst. Every task before it has an earlier or equal due date, so all of them had to be done by about the same time anyway. No plan can finish that whole group before the total of their lengths, and the last task of the group, in any plan, is late by at least as much. So no plan does better.

The length of a task does not matter for the order, and neither does its slack.

## The problem

There are $n$ jobs and one machine. Job $j$ has a processing time $p_j \ge 0$ and a due date $d_j$, any real number. All jobs are available at time 0. A schedule runs one job at a time, and job $j$ completes at $C_j$. The lateness is $L_j = C_j - d_j$ and the goal is to minimize $L_{\max} = \max_j L_j$. This is the [maximum lateness](/maximum-lateness-minimization/) problem with no release dates and no precedence constraints. The algorithm is exact, so no approximation ratio appears on this page.

## The algorithm

```pseudo id=main
EDD(p[1 .. n], d[1 .. n])
L1  sort the jobs so that d[π1] ≤ d[π2] ≤ ... ≤ d[πn]
L2  t ← 0, Lmax ← −∞
L3  for k ← 1 to n do
L4      t ← t + p[πk], C[πk] ← t            ▷ no idle time
L5      Lmax ← max(Lmax, t − d[πk])
L6  return π, C, Lmax
```

Ties in line L1 may be broken in any way. The implementation breaks them by index and returns no value for $L_{\max}$ when there are no jobs.

## Example

Take $p = (3, 2, 1, 4, 2)$ and $d = (5, 4, 9, 10, 3)$ for jobs $0$ to $4$. The EDD order is $4, 1, 0, 2, 3$.

| position | job | $p_j$ | $d_j$ | $C_j$ | $L_j$ |
|---|---|---|---|---|---|
| 1 | 4 | 2 | 3 | 2 | $-1$ |
| 2 | 1 | 2 | 4 | 4 | $0$ |
| 3 | 0 | 3 | 5 | 7 | $2$ |
| 4 | 2 | 1 | 9 | 8 | $-1$ |
| 5 | 3 | 4 | 10 | 12 | $2$ |

So $L_{\max} = 2$, and no order of the $120$ does better. The proof below gives a witness: the first five jobs in the EDD order have total length $12$ and due dates at most $10$, so in every order the last of them is late by at least $2$. The shortest job first order $2, 1, 4, 0, 3$ gives $L_{\max} = 3$, and the minimum slack order (smallest $d_j - p_j$ first) also gives $3$.

## Correctness

Let $k$ be a position where EDD attains its maximum, and let $A = \{\pi_1, \ldots, \pi_k\}$ be the jobs up to that position. There is no idle time, so $L_{\max}(\text{EDD}) = p(A) - d_{\pi_k}$, and each job of $A$ has a due date at most $d_{\pi_k}$. In any schedule, preemptive or not, with idle time or not, the job of $A$ that completes last cannot complete before $p(A)$, and its due date is at most $d_{\pi_k}$. So its lateness is at least $L_{\max}(\text{EDD})$. The full proof is in `proofs/correctness.md`.

The lower bound $p(A) - \max_{j \in A} d_j$ holds for every set $A$ of jobs, so

$$\mathrm{OPT} = \max_{\emptyset \ne A} \Bigl( p(A) - \max_{j \in A} d_j \Bigr),$$

and the maximum is attained by a prefix of the EDD order. The tardiness $T_j = \max(0, L_j)$ gives $T_{\max} = \max(0, L_{\max})$, which is a nondecreasing function of $L_{\max}$, so EDD also minimizes $T_{\max}$.

## Complexity

- **Time.** Line L1 sorts $n$ due dates, $\Theta(n \log n)$ comparisons with a comparison sort. The loop of lines L3 to L5 takes $\Theta(n)$. So the time is $\Theta(n \log n)$, and $\Theta(n)$ if the jobs come sorted by due date.
- **Space.** $\Theta(n)$ for the order and the completion times.

## Properties

- **Exact and simple.** One sort gives an optimal schedule. The processing times are used only to compute $C_j$, not to choose the order.
- **Preemption does not help.** The lower bound of the proof holds for preemptive schedules, so $1 \mid pmtn \mid L_{\max}$ has the same optimum.
- **Deadline test.** Treat the due dates as hard deadlines $\bar d_j$. A schedule that meets all of them exists if and only if EDD gives $L_{\max} \le 0$. This test is a step of the [Moore-Hodgson algorithm](/minimizing-tardy-jobs/) and of many branch and bound methods.
- **Invariant under shifts.** Adding the same constant to all due dates shifts every $L_j$ by that constant and does not change the order. This is why the optimum can be negative or zero, and why a ratio guarantee for $L_{\max}$ makes no sense. See [maximum lateness minimization](/maximum-lateness-minimization/).

## Variants and improvements

- **Precedence constraints.** For $1 \mid prec \mid L_{\max}$, first replace each due date by $d'_j = \min(d_j, \min_{k \text{ succ. of } j} (d'_k - p_k))$, working back from the sinks, and then run EDD with ties broken in favor of predecessors. A cleaner exact method for any nondecreasing costs is [Lawler's algorithm](/lawler-algorithm/), which builds the schedule from the end.
- **Release dates.** $1 \mid r_j \mid L_{\max}$ is strongly NP-hard. With preemption, the rule "at each moment run the available job with the earliest due date" is optimal for $1 \mid r_j, pmtn \mid L_{\max}$. The non-preemptive version of the same rule is Schrage's heuristic, a 2-approximation in the delivery time form. Both are on the page on [maximum lateness minimization](/maximum-lateness-minimization/).
- **Unit jobs with integer release dates.** For $1 \mid r_j, p_j = 1 \mid L_{\max}$ with integer $r_j$, run at each integer time the released job with the earliest due date. This is the preemptive rule, and it never preempts, because every job ends at the next integer time.
- **Parallel machines.** $P \| L_{\max}$ is NP-hard, because with all $d_j = 0$ it is the [makespan](/makespan/) problem.
- **Real-time systems.** The preemptive rule for periodic tasks is [earliest deadline first](/earliest-deadline-first/).

## When to use it

Use EDD when the cost of a schedule is its worst delay, all jobs are present at the start, and there is one machine. Use it as a fast check that a set of jobs can meet its deadlines. Do not use it for the number of late jobs or for the total tardiness: see [minimizing tardy jobs](/minimizing-tardy-jobs/) and [total tardiness minimization](/total-tardiness-minimization/).

## Pitfalls

- **Minimum slack is not optimal.** With $p = (5, 2)$ and $d = (6, 4)$, job 0 has slack $1$ and job 1 has slack $2$. Running job 0 first gives $L_{\max} = 3$. EDD runs job 1 first and gets $1$.
- **EDD does not minimize the number of late jobs.** With $(p_j, d_j) = (4, 4), (1, 5), (1, 5), (1, 5)$, EDD has two late jobs, while dropping the long job to the end gives one.
- **Release dates without waiting.** Job A has $r = 0$, $p = 4$, $d = 10$ and job B has $r = 1$, $p = 1$, $d = 2$. Starting the available job with the earliest due date runs A first, and B ends at $5$ with lateness $3$. Waiting one unit for B gives $L_{\max} = 0$.
- **Lateness can be negative.** Code that starts $L_{\max}$ at $0$ computes $T_{\max}$, not $L_{\max}$. The implementation starts with no value.

## Implementations

## History

Jackson (1955) proved the rule in a research report of the Management Science Research Project at UCLA. It is one of the first exact results of scheduling theory, together with Smith's ratio rule (1956) for the weighted completion time. Kleinberg and Tardos use it as the main example of the exchange argument.

## References
