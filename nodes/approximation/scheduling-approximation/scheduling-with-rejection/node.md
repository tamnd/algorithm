---
tag: NKR10R
kind: problem
slug: scheduling-with-rejection
name: Scheduling with rejection
aliases:
- prize-collecting scheduling
- multiprocessor scheduling with rejection
- order acceptance and scheduling
area: approximation/scheduling-approximation
level: research
summary: Each job is scheduled or rejected at a penalty; minimize the makespan plus the penalties. A simple threshold rule gives 2 - 1/m, with a PTAS, an FPTAS for fixed m, and 1 + phi online.
prereqs: [makespan-minimization, list-scheduling, approximation-ratio]
see_also: [prize-collecting-steiner-tree, minimizing-tardy-jobs, weighted-tardy-jobs, knapsack-problem, hochbaum-shmoys-ptas, bicriteria-approximation, competitive-ratio, fptas]
sources:
  - paper: "Yair Bartal, Stefano Leonardi, Alberto Marchetti-Spaccamela, Jiří Sgall and Leen Stougie, Multiprocessor scheduling with rejection, SIAM Journal on Discrete Mathematics 13(1), 2000"
    locator: pages 64 to 78 (the problem, the online ratio 1 + phi, the PTAS, and the FPTAS for fixed m)
  - paper: "Daniel W. Engels, David R. Karger, Stavros G. Kolliopoulos, Sudipta Sengupta, R. N. Uma and Joel Wein, Techniques for scheduling with rejection, Journal of Algorithms 49(1), 2003"
    locator: pages 175 to 191 (rejection with the weighted sum of completion times)
  - paper: "Han Hoogeveen, Martin Skutella and Gerhard J. Woeginger, Preemptive scheduling with rejection, Mathematical Programming 94, 2003"
    locator: pages 361 to 374 (preemptive makespan with rejection)
  - paper: "Dvir Shabtay, Nufar Gaspar and Moshe Kaspi, A survey on offline scheduling with rejection, Journal of Scheduling 16(1), 2013"
    locator: pages 3 to 28 (a survey of the offline results by objective)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability
    locator: Section 4.2 (3-partition and strong NP-completeness) and Appendix A5.1, problem SS8 (multiprocessor scheduling)
---

Scheduling with rejection gives the scheduler a choice for each job: run it, or reject it and pay a penalty $e_j$. In the version of Bartal, Leonardi, Marchetti-Spaccamela, Sgall and Stougie (2000), there are $m$ identical machines and the goal is to minimize the [makespan](/makespan/) of the accepted jobs plus the total penalty of the rejected jobs. With very large penalties nothing is rejected and the problem is [makespan minimization](/makespan-minimization/), so it is strongly NP-hard when $m$ is part of the input. A simple threshold rule, proved below, gives the ratio $2 - 1/m$ and is exact on one machine. Bartal and others give a PTAS, an FPTAS for each fixed $m$, and an online algorithm with competitive ratio $1 + \varphi \approx 2.618$, where $\varphi$ is the golden ratio. The same idea of paying for what you do not serve appears in [prize-collecting](/prize-collecting-steiner-tree/) problems on graphs.

## In plain words

A shop with several identical machines gets a list of orders. It can make an order, which takes machine time, or turn it down and pay a fee. The shop pays for the time until the last machine is done, plus all the fees. An order is worth taking only if its fee is larger than its share of the time, its length divided by the number of machines. Very long orders are a problem of their own, because one long order alone can set the end time. So try each possible length of the longest order you take, take the orders that are worth it up to that length, and keep the best result.

## Definition

**Input.** Jobs $1, \ldots, n$ with processing times $p_j \ge 0$ and rejection penalties $e_j \ge 0$, and $m$ identical machines.

**Output.** A set $A$ of accepted jobs, and an assignment of the jobs of $A$ to the machines. The jobs not in $A$ are rejected.

**Goal.** Minimize $C_{\max}(A) + e(N - A)$, where $C_{\max}(A)$ is the largest machine load and $e(X) = \sum_{j \in X} e_j$.

In the [three-field notation](/scheduling-notation/) this is often written $P \mid rej \mid C_{\max} + \sum_{j \in R} e_j$, where $R$ is the set of rejected jobs. Other objectives for the accepted jobs give other problems of the same family, for example $\sum_{j \in A} w_j C_j + e(R)$.

## Variants

| problem | status |
|---|---|
| $1 \mid rej \mid C_{\max} + e(R)$ | trivial: accept $j$ if and only if $p_j \le e_j$ |
| $P2 \mid rej \mid C_{\max} + e(R)$ | NP-hard, from [partition](/partition-problem/); FPTAS for each fixed $m$ |
| $P \mid rej \mid C_{\max} + e(R)$ | strongly NP-hard, from [3-partition](/three-partition/); PTAS; factor $2 - 1/m$ below |
| online, $P \mid rej \mid C_{\max} + e(R)$ | competitive ratio $1 + \varphi$ (Bartal and others 2000) |
| $P \mid pmtn, rej \mid C_{\max} + e(R)$ | studied by Hoogeveen, Skutella and Woeginger (2003) |
| $1 \mid rej \mid \sum_{A} w_j C_j + e(R)$ | NP-hard (Engels and others 2003) |
| a bound on the total penalty, or on the makespan | a [bicriteria](/bicriteria-approximation/) problem; with $m = 1$ and a bound on the makespan it is [knapsack](/knapsack-problem/) |

When the accepted jobs must meet due dates and the rejected jobs pay $w_j$, the problem is [weighted tardy jobs](/weighted-tardy-jobs/): rejected jobs are the late ones, which can go at the end. The survey of Shabtay, Gaspar and Kaspi (2013) lists the results for many objectives.

## Examples

**Six jobs, two machines.** Take the jobs below, numbered from 0.

| job | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| $p_j$ | 6 | 4 | 3 | 3 | 2 | 2 |
| $e_j$ | 2 | 5 | 4 | 1 | 3 | 1 |
| $p_j / m$ | 3 | 2 | 1.5 | 1.5 | 1 | 1 |

Jobs 0 and 3 have $e_j < p_j / 2$, so the rule never accepts them. For each guess $T$ of the longest accepted job, the rule accepts the other jobs with $p_j \le T$ and schedules them by longest job first:

| guess $T$ | accepted | loads | makespan | penalty | total |
|---|---|---|---|---|---|
| 0 | none | 0, 0 | 0 | 16 | 16 |
| 2 | 4, 5 | 2, 2 | 2 | 12 | 14 |
| 3 | 2, 4, 5 | 3, 4 | 4 | 8 | 12 |
| 4 or 6 | 1, 2, 4, 5 | 6, 5 | 6 | 3 | 9 |

The best total is 9: jobs 1 and 5 on one machine, jobs 2 and 4 on the other, and jobs 0 and 3 rejected. A search over all $3^6$ choices confirms that 9 is optimal.

**A loss.** Take $m = 2$, $p = (4, 4)$ and $e = (1, 4)$. Job 0 has $e_0 = 1 < p_0/2 = 2$, so the rule rejects it, and the best guess costs 5. The optimum accepts both jobs, one on each machine, for a total of 4. Rejecting job 0 saves nothing here, because the second machine would be idle anyway.

**A tight family.** Take $m$ jobs of length $mK$. Job 0 has a huge penalty and the others have penalty $K - 1 < mK/m$. The rule accepts only job 0 and pays $mK + (m-1)(K-1)$. The optimum accepts all jobs, one per machine, for $mK$. The ratio tends to $2 - 1/m$ as $K$ grows, so the bound below is tight for this rule.

## Known algorithms

**The threshold rule.** Guess the longest accepted job, accept the jobs that are worth their share of machine time, and list-schedule them.

```pseudo id=main
THRESHOLD-REJECTION(p[1 .. n], e[1 .. n], m)
L1  for each T in {0} ∪ {p[1], ..., p[n]} do
L2      A ← { j : p[j] ≤ T and p[j] ≤ m · e[j] }
L3      list-schedule the jobs of A on m machines, longest job first
L4      value ← makespan of A + total penalty of the jobs not in A
L5      remember the schedule if value is the smallest so far
L6  return the best schedule
```

There are at most $n + 1$ guesses, and each takes $O(n \log n)$ time for the sort and the heap of machine loads. So the time is $O(n^2 \log n)$. The space is $O(n + m)$.

**Theorem.** THRESHOLD-REJECTION returns a schedule of cost at most $(2 - 1/m)\,\mathrm{OPT}$. For $m = 1$ it is optimal.

*Proof.* Fix an optimal solution with accepted set $A^*$. Let $T^*$ be the largest $p_j$ in $A^*$, or 0 if $A^*$ is empty. Two lower bounds hold: $\mathrm{OPT} \ge p(A^*)/m + e(N - A^*)$, because some machine has load at least the average, and $\mathrm{OPT} \ge T^*$, because the job of length $T^*$ runs somewhere.

Look at the iteration with $T = T^*$. Line L2 chooses, among the subsets of $\{j : p_j \le T^*\}$, a set $A$ with the smallest value of $p(A)/m + e(N - A)$: each job counts on its own, and a job is accepted exactly when $p_j / m \le e_j$. The set $A^*$ is one of these subsets, so

$$\frac{p(A)}{m} + e(N - A) \le \frac{p(A^*)}{m} + e(N - A^*) \le \mathrm{OPT}.$$

By Graham's bound for [list scheduling](/list-scheduling/), the makespan at line L3 is at most $p(A)/m + (1 - 1/m) \max_{j \in A} p_j \le p(A)/m + (1 - 1/m)\,T^*$. So the value at line L4 is at most $\mathrm{OPT} + (1 - 1/m)\,T^* \le (2 - 1/m)\,\mathrm{OPT}$. The best guess is at least as good. For $m = 1$ the factor is 1. ∎

The tests of this page compare the rule with a search over all ways to reject a job or put it on a machine, on seeded random instances with up to 6 jobs and 2 or 3 machines, and check the tight family.

Bartal and others (2000) also give a $(2 - 1/m)$-approximation that runs in $O(n \log n)$ time. We have not checked whether it is the same rule as the one above.

**Approximation schemes.** Bartal and others (2000) give a PTAS for $P \mid rej \mid C_{\max} + e(R)$, built on the [Hochbaum-Shmoys](/hochbaum-shmoys-ptas/) approach for the makespan, and an FPTAS for each fixed $m$, by a dynamic program over rounded machine loads in the style of the [knapsack FPTAS](/knapsack-fptas/).

**Online.** Jobs arrive one by one, and each must be accepted and assigned, or rejected, at once. Bartal and others (2000) give a deterministic online algorithm with [competitive ratio](/competitive-ratio/) $1 + \varphi \approx 2.618$ for every $m$, and show that no deterministic online algorithm does better when $m$ is large.

## Bounds

- **Upper bounds.** Factor $2 - 1/m$ in polynomial time by the rule above, a PTAS, and an FPTAS for each fixed $m$.
- **Lower bounds.** Strongly NP-hard when $m$ is part of the input, since large penalties give $P \| C_{\max}$, so there is no FPTAS unless P = NP. NP-hard already for $m = 2$, from [partition](/partition-problem/).
- **Online.** Competitive ratio $1 + \varphi$ for deterministic algorithms, and this is the best possible for large $m$.

## Reductions

- **From makespan minimization.** Set $e_j > \sum_k p_k$ for all $j$. Then no optimal solution rejects a job, and the problem is $P \| C_{\max}$.
- **One machine with a makespan bound to knapsack.** Accepting a set of total length at most $D$ with the smallest total penalty of the rest is the same as choosing a set of largest penalty with total length at most $D$, which is the [knapsack problem](/knapsack-problem/).
- **Due dates and late jobs.** For $1 \| \sum w_j U_j$, a late job can go after all on-time jobs, so declaring a job late is rejecting it at the cost $w_j$. See [minimizing tardy jobs](/minimizing-tardy-jobs/).
- **Prize-collecting problems.** In the [prize-collecting Steiner tree](/prize-collecting-steiner-tree/), a vertex is either connected or its penalty is paid. Scheduling with rejection is the same trade-off for jobs.

## Applications

- **Order acceptance.** A firm that cannot make all orders in time accepts some and turns the others down or gives them to a subcontractor at a cost.
- **Admission control.** An overloaded server or network rejects some requests, which costs a penalty in service quality, to keep the response time of the rest short.
- **Outsourcing.** Rejected jobs are often jobs given to an outside supplier, and the penalty is its price.

## References
