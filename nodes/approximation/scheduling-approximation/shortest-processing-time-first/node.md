---
tag: VXZQYC
kind: algorithm
slug: shortest-processing-time-first
name: Shortest processing time first (SPT)
aliases:
- SPT rule
- shortest job first for total completion time
area: approximation/scheduling-approximation
level: intro
summary: Sort jobs by processing time and deal them to the machines in turn; optimal for the total completion time on one machine and on identical parallel machines.
solves: [weighted-completion-time-scheduling]
model: word-ram
complexity:
  vars: {n: the number of jobs, m: the number of machines}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, online: false, recursive: false}
history:
  year: 1956
  people: [Wayne E. Smith]
  note: Smith proved the ratio rule for one machine in 1956; SPT is its case with equal weights.
prereqs: [scheduling-notation, exchange-argument, sorting-problem]
see_also: [smith-rule, weighted-completion-time-scheduling, optimal-tape-storage, list-scheduling, longest-processing-time-first, flow-time-minimization, scheduling-with-release-dates, srpt]
sources:
  - paper: doi:10.1002/nav.3800030106
    title: Wayne E. Smith, Various optimizers for single-stage production, Naval Research Logistics Quarterly 3(1-2), 1956
    locator: pages 59 to 66
  - book: isbn:9783319265780
    title: Michael L. Pinedo, Scheduling, Theory, Algorithms, and Systems, fifth edition
    locator: Chapter 3 (the SPT and WSPT rules on one machine) and Chapter 5 (SPT for the total completion time on parallel machines)
  - book: isbn:9783540695158
    title: Peter Brucker, Scheduling Algorithms, fifth edition
    locator: Chapter 4 (single machine) and Chapter 5 (parallel machines, total completion time)
  - paper: "John Bruno, Edward G. Coffman Jr. and Ravi Sethi, Scheduling independent tasks to reduce mean finishing time, Communications of the ACM 17(7), 1974"
    locator: pages 382 to 387
---

Shortest processing time first (SPT) is the rule that runs the shortest jobs first. On one machine it solves $1 \| \sum C_j$ in the [three-field notation](/scheduling-notation/): it minimizes the sum of the completion times. On $m$ identical machines it sorts the jobs the same way and deals them to the machines in turn, and this solves $P \| \sum C_j$. Both results follow from one counting argument: each job delays itself and every job after it on its machine, so the short jobs must go where they delay the most jobs. With weights, the rule becomes [Smith's rule](/smith-rule/).

## In plain words

You have a pile of tasks and one worker. Each task has a length. Every finished task is a happy customer, and you want the customers to wait as little as possible in total.

A task that runs early makes every later task wait for it. So a long task at the front makes many people wait a long time, while a short task at the front costs them only a little. The best plan is to do the short tasks first and the long tasks last.

With several workers, give the shortest task to the first worker, the next one to the second worker, and so on in turn. Each worker then has short tasks early and long tasks late, and the few tasks that make the most people wait are the shortest ones.

## The problem

There are $n$ jobs and $m \ge 1$ identical machines. Job $j$ has a processing time $p_j \ge 0$, and all jobs are available at time 0. A schedule puts each job on one machine, without preemption, and each machine runs one job at a time. The completion time of job $j$ is $C_j$. The goal is to minimize $\sum_j C_j$. Dividing by $n$ gives the mean completion time, so the same schedule minimizes both. With all release dates equal to 0, the completion time is also the [flow time](/flow-time/) of the job.

Idle time only delays jobs, so we look only at schedules in which each machine runs its jobs back to back from time 0. Such a schedule is a list of jobs for each machine.

This page uses $n$ for the number of jobs and $m$ for the number of machines. The algorithm is exact, so no ratio appears here; the approximation pages for the harder variants are listed below.

## The algorithm

```pseudo id=main
SPT(p[1 .. n], m)
L1  sort the jobs so that p[π1] ≤ p[π2] ≤ ... ≤ p[πn]
L2  load[1 .. m] ← 0, total ← 0, each machine list empty
L3  for k ← 1 to n do
L4      i ← ((k − 1) mod m) + 1                ▷ deal the jobs in turn
L5      load[i] ← load[i] + p[πk], C[πk] ← load[i], append πk to machine i
L6      total ← total + C[πk]
L7  return the machine lists, C and total
```

For $m = 1$, line L4 always picks machine 1, and the algorithm is the plain SPT order. Ties in line L1 may be broken in any way; the implementation breaks them by index.

## Example

Take five jobs with $p = (4, 1, 3, 6, 2)$ for jobs $0$ to $4$.

**One machine.** The SPT order is jobs $1, 4, 2, 0, 3$ with lengths $1, 2, 3, 4, 6$.

| position | job | $p_j$ | $C_j$ | jobs it delays (itself included) |
|---|---|---|---|---|
| 1 | 1 | 1 | 1 | 5 |
| 2 | 4 | 2 | 3 | 4 |
| 3 | 2 | 3 | 6 | 3 |
| 4 | 0 | 4 | 10 | 2 |
| 5 | 3 | 6 | 16 | 1 |

The total is $1 + 3 + 6 + 10 + 16 = 36$. The last column gives the same total as $5 \cdot 1 + 4 \cdot 2 + 3 \cdot 3 + 2 \cdot 4 + 1 \cdot 6 = 36$. The longest first order $3, 0, 2, 4, 1$ gives $6 + 10 + 13 + 15 + 16 = 60$, the worst of all $120$ orders.

**Two machines.** The dealt order puts jobs $1, 2, 3$ on machine 1, with completion times $1, 4, 10$, and jobs $4, 0$ on machine 2, with completion times $2, 6$. The total is $23$, which is the least over all $2^5$ assignments and all orders.

## Correctness

The proof in `proofs/correctness.md` counts how often each processing time is paid. On a machine with the list $j_1, \ldots, j_r$, the job $j_s$ is part of the completion times of $j_s, \ldots, j_r$, so

$$\sum_{s=1}^{r} C_{j_s} = \sum_{s=1}^{r} (r - s + 1)\, p_{j_s}.$$

Call $r - s + 1$ the *coefficient* of job $j_s$. Each machine offers the coefficients $1, 2, 3, \ldots$, so in any schedule at most $m$ jobs have coefficient $1$, at most $m$ have coefficient $2$, and so on. Hence the $i$-th smallest coefficient is at least $\lceil i/m \rceil$. By the [rearrangement](/exchange-argument/) of a sum of products, the total is at least $\sum_{i=1}^n \lceil i/m \rceil\, q_i$, where $q_1 \ge q_2 \ge \cdots \ge q_n$ are the processing times from the longest down. SPT gives the $i$-th longest job exactly the coefficient $\lceil i/m \rceil$, so it meets this lower bound:

$$\mathrm{OPT} = \sum_{i=1}^{n} \left\lceil \frac{i}{m} \right\rceil q_i .$$

For $m = 1$ this is $\sum_i i\, q_i$: the longest job is paid once and the shortest $n$ times.

## Complexity

- **Time.** The sort of line L1 takes $\Theta(n \log n)$ comparisons in the worst case. The loop of lines L3 to L6 takes $\Theta(n)$ time. So the time is $\Theta(n \log n)$ in every case for a comparison sort, and $O(n + m)$ after the sort if the jobs come sorted.
- **Space.** $\Theta(n + m)$ for the order, the loads and the lists.
- **Lower bound.** On one machine, the order that SPT outputs is the sorted order, so a comparison-based algorithm that outputs an optimal order needs $\Omega(n \log n)$ comparisons in the worst case when the processing times are distinct, by the sorting lower bound of the [comparison model](/comparison-model/).

## Properties

- **Exact.** The schedule is optimal, not only approximate. On one machine, the same order also minimizes the mean waiting time $\sum_j (C_j - p_j)/n$, because $\sum_j p_j$ is fixed.
- **Not unique.** Jobs of equal length can be swapped. On $m$ machines, any schedule that gives the $i$-th longest job a coefficient of $\lceil i/m \rceil$ is optimal, for example the list version below.
- **Independent of the processing times beyond their order.** Only the sorted order is used, so the schedule stays optimal if all lengths are changed in a way that keeps their order.
- **Greedy list version.** Running SPT as a [list schedule](/list-scheduling/), where the next shortest job starts on the machine that is free first, also gives an optimal schedule for $P \| \sum C_j$ (Pinedo, Chapter 5).

## Variants and improvements

- **Weights.** For $1 \| \sum w_j C_j$, sort by $p_j / w_j$, which is [Smith's rule](/smith-rule/). On parallel machines, $P2 \| \sum w_j C_j$ is already NP-hard. See [weighted completion time scheduling](/weighted-completion-time-scheduling/) for the approximation results.
- **Uniform and unrelated machines.** For $Q \| \sum C_j$ the same coefficient argument works with coefficients $k / s_i$ on a machine of speed $s_i$. For $R \| \sum C_j$, Bruno, Coffman and Sethi (1974) build a bipartite graph between jobs and the slots "position $k$ from the end on machine $i$", with cost $k\, p_{ij}$, and solve a minimum cost assignment. See [unrelated machine scheduling](/unrelated-machine-scheduling/).
- **Release dates.** With release dates, $1 \mid r_j \mid \sum C_j$ is strongly NP-hard. If preemption is allowed, the rule "run the job with the shortest remaining processing time" ([SRPT](/srpt/)) is optimal, and turning that schedule into a non-preemptive one gives a 2-approximation. See [scheduling with release dates](/scheduling-with-release-dates/) and [flow time minimization](/flow-time-minimization/).
- **Precedence constraints.** With chains or a general order, SPT is no longer optimal. See [Sidney decomposition](/sidney-decomposition/).

## When to use it

Use SPT when all jobs are known at the start, the goal is the total or the mean completion time, and the machines are identical. It is the standard example of a greedy rule proved by an [exchange argument](/exchange-argument/), and the base of the ratio rules for weighted and precedence constrained problems. When the goal is the [makespan](/makespan/), use [longest processing time first](/longest-processing-time-first/) instead.

## Pitfalls

- **SPT is bad for the makespan.** With $m = 2$ and $p = (1, 1, 1, 1, 4)$, SPT puts the jobs of length $1, 1, 4$ on one machine, with a makespan of $6$ and $\sum C_j = 12$. The schedule that puts the long job alone has a makespan of $4$ but $\sum C_j = 14$. The two goals pull in different directions.
- **Release dates break the rule.** Job A has $r = 0$, $p = 10$ and job B has $r = 1$, $p = 1$. Starting the shortest available job runs A first and gives $10 + 11 = 21$. Waiting one unit and running B first gives $2 + 12 = 14$. A greedy rule that never waits is not optimal here.
- **Weights are ignored.** With $p = (1, 2)$ and $w = (1, 10)$, SPT gives $1 \cdot 1 + 10 \cdot 3 = 31$, but the other order gives $10 \cdot 2 + 1 \cdot 3 = 23$.
- **Unbalanced dealing.** On $m$ machines it is not enough to sort each machine's list. Putting all short jobs on one machine wastes the small coefficients of the others. The jobs must be dealt in turn, or by the list rule.

## Implementations

## History

Smith (1956) proved that the ratio rule minimizes the weighted sum of completion times on one machine. SPT is its special case with equal weights. The positional argument for parallel machines is a classical result of scheduling theory, presented in Pinedo, Chapter 5, and Bruno, Coffman and Sethi (1974) extended it to unrelated machines with an assignment problem.

## References
