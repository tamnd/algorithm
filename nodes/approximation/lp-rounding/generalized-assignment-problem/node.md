---
tag: C846S9
kind: problem
slug: generalized-assignment-problem
name: Generalized assignment problem
aliases:
- GAP
- minimum cost generalized assignment
area: approximation/lp-rounding
level: advanced
summary: Assign each job to a machine, where job j takes time p_ij and costs c_ij on machine i, so that loads stay within T at the least cost; LP rounding gives cost at most OPT with loads at most 2T.
model: word-ram
complexity:
  vars: {m: the number of machines, n: the number of jobs}
  time: {worst: O(m^n (n + m))}
prereqs: [assignment-problem, lp-relaxation, makespan, np-hard]
see_also: [shmoys-tardos-gap, unrelated-machine-scheduling-makespan, lenstra-shmoys-tardos, bicriteria-approximation, multiple-knapsack-problem, assignment-problem, iterative-relaxation, partition-problem]
sources:
  - paper: doi:10.1007/BF01585178
    title: David B. Shmoys and Éva Tardos, An approximation algorithm for the generalized assignment problem, Mathematical Programming 62(3), 1993
    locator: the problem, the LP, and the cost C and load 2T guarantee
  - paper: doi:10.1007/BF01585745
    title: Jan Karel Lenstra, David B. Shmoys and Éva Tardos, Approximation algorithms for scheduling unrelated parallel machines, Mathematical Programming 46, 1990
    locator: the 3/2 hardness for the load bound
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 11.1 (the generalized assignment problem)
  - book: isbn:9781107007512
    title: Lap Chi Lau, R. Ravi and Mohit Singh, Iterative Methods in Combinatorial Optimization, Cambridge University Press, 2011
    locator: Chapter 3 (matching and the generalized assignment problem)
---

The generalized assignment problem (GAP) asks to assign $n$ jobs to $m$ machines. Job $j$ takes time $p_{ij}$ and costs $c_{ij}$ if it goes to machine $i$, and each machine $i$ has a time limit $T_i$. The task is to find an assignment that keeps each machine within its limit and has the least total cost. Without the limits it is the easy choice of the cheapest machine for each job, and with one job per machine it is the [assignment problem](/assignment-problem/). With the limits, even deciding whether any feasible assignment exists is NP-hard, so no algorithm can approximate the cost alone. The standard result is the [bicriteria](/bicriteria-approximation/) guarantee of [Shmoys and Tardos](/shmoys-tardos-gap/) (1993): cost at most the optimum and loads at most $2T_i$. With all costs 0 and one limit $T$, GAP is [unrelated machine scheduling](/unrelated-machine-scheduling-makespan/).

## In plain words

You have a set of tasks and a set of workers. Each worker takes a different time for each task, and charges a different price. Each worker can work only a limited number of hours. Give every task to one worker, keep every worker within their hours, and pay as little as possible.

Fitting tasks into the hours is already a packing puzzle, as hard as splitting numbers into two equal halves. So the fast method allows a small overrun: it never pays more than the best plan, but a worker may work up to twice their hours.

## Definition

**Input.** Machines $i = 1, \ldots, m$ and jobs $j = 1, \ldots, n$. For each pair, a time $p_{ij} \ge 0$ and a cost $c_{ij}$. For each machine, a limit $T_i \ge 0$. Often all limits are the same $T$.

**Output.** A map $\sigma$ from jobs to machines with load $\sum_{j : \sigma(j) = i} p_{ij} \le T_i$ for each machine $i$, of least cost $\sum_j c_{\sigma(j) j}$. If no such map exists, the instance is infeasible.

**The LP.** With $x_{ij}$ the fraction of job $j$ on machine $i$,

$$\min \sum_{i, j} c_{ij} x_{ij} \ \text{ s.t. } \ \sum_i x_{ij} = 1 \text{ for each } j, \quad \sum_j p_{ij} x_{ij} \le T_i \text{ for each } i, \quad x \ge 0, \quad x_{ij} = 0 \text{ if } p_{ij} > T_i.$$

The last rule is needed. Without it, the LP could put a small part of a job that is too long for a machine there, and the rounding could not keep the load within $2T_i$.

**Bicriteria guarantee.** An algorithm is an $(\alpha, \beta)$ approximation if, for each feasible instance, it returns an assignment of cost at most $\alpha \cdot \text{OPT}$ with each load at most $\beta T_i$. Shmoys and Tardos give $(1, 2)$.

## Variants

- **Maximum profit GAP.** Each job may be left out, job $j$ gives profit $w_{ij}$ on machine $i$, and the loads must stay within $T_i$ exactly. The task is to maximize the profit. Here exact feasibility is easy (leave everything out), and constant ratios are known: $1/2$ from the Shmoys-Tardos rounding (Chekuri and Khanna 2000), and $1 - 1/e$ by Fleischer, Goemans, Mirrokni and Sviridenko (2006).
- **Multiple knapsack.** In the profit version, if $p_{ij} = s_j$ and $w_{ij} = w_j$ do not depend on the machine, the problem is the [multiple knapsack problem](/multiple-knapsack-problem/), which has a PTAS.
- **Makespan.** With all $c_{ij} = 0$ and one limit $T$, the question is the decision form of [unrelated machine scheduling](/unrelated-machine-scheduling-makespan/), $R \| C_{\max}$.
- **Restricted assignment.** If $p_{ij} \in \{p_j, \infty\}$, each job has a set of allowed machines and a fixed time. This is the [restricted assignment](/restricted-assignment-scheduling/) problem.
- **Cost and makespan together.** Minimize cost plus a weight times the makespan, or find the trade-off curve. Each point of the curve can be approximated with the same $(1, 2)$ guarantee.

## Examples

Take two machines, four jobs and $T = 4$.

| | $j_1$ | $j_2$ | $j_3$ | $j_4$ |
|---|---|---|---|---|
| $p_{1j}$ | 2 | 1 | 2 | 4 |
| $p_{2j}$ | 3 | 2 | 4 | 2 |
| $c_{1j}$ | 0 | 1 | 4 | 4 |
| $c_{2j}$ | 3 | 1 | 1 | 0 |

The optimum is $j_1, j_3 \to 1$ and $j_2, j_4 \to 2$, with loads $4$ and $4$ and cost $0 + 4 + 1 + 0 = 5$. The cheapest machine for each job would give $j_1 \to 1$, $j_3, j_4 \to 2$ and $j_2$ to either. That costs 2, but machine 2 has load $4 + 2 = 6 > 4$.

The LP optimum is $7/2$, with $j_3$ split half and half. The Shmoys-Tardos rounding returns the cheap assignment of cost 2 with loads 3 and 6. Its cost is at most the LP, and the load 6 is at most $T + \max_j p_{2j} = 8$. So the algorithm trades load for cost, as its guarantee allows.

## Known algorithms

| algorithm | type | guarantee |
|---|---|---|
| brute force over all maps | exact | time $O(m^n (n + m))$ |
| branch and price with column generation | exact | practical for moderate sizes |
| [Lenstra, Shmoys and Tardos](/lenstra-shmoys-tardos/) (1990) | LP rounding by a pseudo-forest, no costs | makespan at most $2T$ |
| [Shmoys and Tardos](/shmoys-tardos-gap/) (1993) | LP rounding by slots and a min-cost matching | cost at most the LP, load at most $T_i + \max_j p_{ij} \le 2T_i$ |
| [iterative relaxation](/iterative-relaxation/) (in Williamson and Shmoys, Section 11.1) | iterative rounding of the same LP | the same $(1, 2)$ bound |

For the exact methods, the column generation LP has one variable for each set of jobs that fits on a machine, as in the [configuration LP](/configuration-lp/), and its bound is much stronger than the assignment LP.

## Bounds

- **Lower bound used.** The LP value, which is at most OPT for each feasible instance.
- **No ratio on cost alone.** Deciding feasibility is NP-hard (see Reductions), so no polynomial algorithm returns a feasible assignment of cost within any factor of OPT, unless P = NP.
- **No load below $3/2$.** Lenstra, Shmoys and Tardos showed that, unless P = NP, no polynomial algorithm can find an assignment with loads less than $\frac{3}{2} T$ whenever one with loads at most $T$ exists. This holds even with no costs, so no $(\alpha, \beta)$ guarantee with $\beta < 3/2$ is possible.
- **The gap between $3/2$ and 2.** It is open whether $\beta$ can be below 2 with $\alpha$ finite, even with no costs.
- **The LP.** The factor 2 on loads is close to tight for this LP, even with no costs. Give each of the $m$ machines its own job of time $m - 1$ that can run only there, and add one job of time $m$ on every machine. The LP is feasible for $T = m$, by spreading the long job evenly, while every assignment has a machine with load $2m - 1 = (2 - 1/m) T$.

## Reductions

- **From partition.** Given numbers $a_1, \ldots, a_n$ with sum $2B$, take two machines, $p_{ij} = a_j$, $c_{ij} = 0$ and $T_1 = T_2 = B$. A feasible assignment is a split into two halves of equal sum, which is the NP-complete [partition problem](/partition-problem/).
- **To makespan.** Unrelated machine scheduling is GAP with zero costs and a guessed $T$. A search over $T$ with a $(1, 2)$ algorithm gives a 2-approximation for $R \| C_{\max}$.
- **To bipartite matching.** If each machine may take only one job and $T_i$ allows any single job, GAP is the [assignment problem](/assignment-problem/). The Shmoys-Tardos rounding turns the general case into a min-cost bipartite matching of jobs to slots.

## Applications

- **Workforce and task scheduling.** Tasks are given to staff with limited hours and different skills and costs.
- **Vehicle routing.** The classic cluster-first method of Fisher and Jaikumar assigns customers to vehicles by solving a GAP with vehicle capacities.
- **Cloud and computing.** Virtual machines or jobs are placed on servers with limited capacity, where each placement has a cost.
- **A subproblem.** GAP appears inside facility location with capacities, in lot sizing, and as the assignment step of many scheduling methods.

## References
