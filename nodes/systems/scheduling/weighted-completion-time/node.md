---
tag: 09K18D
kind: problem
slug: weighted-completion-time
name: "Weighted completion time scheduling"
aliases:
- sum of weighted completion times
- weighted mean response time of a batch
area: systems/scheduling
level: advanced
summary: "Order jobs that are all present on one machine to minimize the sum of weight times completion time, 1||ΣwjCj. Smith's rule solves it in O(n log n) time."
prereqs: [single-machine-scheduling, scheduling-metrics]
see_also: [smiths-rule, weighted-completion-time-scheduling, minimizing-weighted-completion-time, shortest-job-first, sjf-optimality, sidney-decomposition, srpt, scheduling-with-release-dates]
sources:
  - paper: doi:10.1002/nav.3800030106
    title: Wayne E. Smith, Various optimizers for single-stage production, Naval Research Logistics Quarterly 3(1-2), 1956
    locator: pages 59 to 66 (the problem and the ratio rule)
  - book: isbn:9783319265780
    title: Michael L. Pinedo, Scheduling, Theory, Algorithms, and Systems, fifth edition
    locator: Chapter 3, Section 3.1, The Total Weighted Completion Time
  - book: isbn:9783540695158
    title: Peter Brucker, Scheduling Algorithms, fifth edition
    locator: Chapter 4, Single Machine Scheduling Problems (the total weighted completion time, with and without precedence)
  - paper: "doi:10.1016/S0167-5060(08)70743-X"
    title: Jan Karel Lenstra, Alexander H. G. Rinnooy Kan and Peter Brucker, Complexity of machine scheduling problems, Annals of Discrete Mathematics 1, 1977
    locator: pages 343 to 362 (strong NP-hardness of 1|rj|ΣCj)
  - paper: "doi:10.1016/S0167-5060(08)70323-6"
    title: Eugene L. Lawler, Sequencing jobs to minimize total weighted completion time subject to precedence constraints, Annals of Discrete Mathematics 2, 1978
    locator: pages 75 to 90 (series-parallel precedence in polynomial time, and NP-hardness for general precedence)
---

Minimizing weighted completion time is the problem of ordering $n$ jobs on one machine, all present at time $0$, so that $\sum_j w_j C_j$ is as small as possible, where $C_j$ is the [completion time](/scheduling-metrics/) of job $j$ and $w_j > 0$ its weight. In [Graham's notation](/scheduling-notation/) it is $1 \| \sum w_j C_j$. [Smith's rule](/smiths-rule/) solves it exactly in $\Theta(n \log n)$ time. This page is the one-machine problem as a systems scheduler sees it; [the general problem page](/weighted-completion-time-scheduling/) covers release dates, precedence and parallel machines with their approximation algorithms, and [the greedy-technique page](/minimizing-weighted-completion-time/) treats it as an exercise in exchange arguments.

## In plain words

One server has a queue of jobs, and all of them are already there. Each job takes some time. Each job also has a weight, for example the number of users who wait for it, or the money lost for each second that it is not done. A job costs its weight times the time at which it finishes. The task is to choose the order of the jobs so that the total cost is as small as possible. The server never stops between jobs, and a job, once started, runs to its end.

## Definition

**Input.** $n$ jobs. Job $j$ has a processing time $p_j \ge 0$ and a weight $w_j > 0$, both rational.

**Schedule.** An order $\pi$ of the jobs. The machine runs them back to back from time $0$, so $C_{\pi(k)} = \sum_{i \le k} p_{\pi(i)}$.

**Goal.** Minimize $F(\pi) = \sum_{j=1}^{n} w_j C_j$.

Idle time, and preemption when all jobs are present, cannot help: idle time delays every later job, and a preempted job can be moved to the end of its last piece without delaying it while the jobs that ran between its pieces finish earlier. So the order is the whole decision.

**Equivalent objectives.** With all jobs present at time $0$, the flow time $F_j = C_j - r_j$ equals $C_j$. The weighted waiting time is $\sum_j w_j (C_j - p_j) = \sum_j w_j C_j - \sum_j w_j p_j$, and the second sum does not depend on the order. The weighted mean response time is $\sum_j w_j C_j / \sum_j w_j$. All three have the same optimal orders.

## Variants

| problem | status | method or source |
|---|---|---|
| $1 \| \sum C_j$ | $O(n \log n)$ | [shortest processing time first](/shortest-processing-time-first/) |
| $1 \| \sum w_j C_j$ | $O(n \log n)$ | [Smith's rule](/smiths-rule/), Smith 1956 |
| $1 \mid chains \mid \sum w_j C_j$ | polynomial | the ratio rule on chain prefixes, Pinedo Section 3.1 |
| $1 \mid \text{series-parallel prec} \mid \sum w_j C_j$ | polynomial | Lawler 1978 |
| $1 \mid prec \mid \sum w_j C_j$ | NP-hard (Lawler 1978) | 2-approximation by [Sidney decomposition](/sidney-decomposition/) |
| $1 \mid r_j \mid \sum C_j$ | strongly NP-hard (Lenstra, Rinnooy Kan and Brucker 1977) | see [release dates](/scheduling-with-release-dates/) |
| $1 \mid r_j, pmtn \mid \sum C_j$ | polynomial | [SRPT](/srpt/) |
| $P \| \sum C_j$ | polynomial | SPT dealt to the machine that is free first |

With weights and parallel machines, or with weights, release dates and preemption, the problem becomes NP-hard; [the general problem page](/weighted-completion-time-scheduling/) lists these cases with their approximation ratios.

## Examples

**Three jobs, all six orders.** Take $a$ with $(p, w) = (3, 1)$, $b$ with $(1, 2)$ and $c$ with $(4, 3)$. The ratios $p/w$ are $3$, $1/2$ and $4/3$.

| order | $\sum w_j C_j$ | weighted waiting time |
|---|---|---|
| $a, b, c$ | 35 | 18 |
| $a, c, b$ | 40 | 23 |
| $b, a, c$ | 30 | 13 |
| $b, c, a$ | 25 | 8 |
| $c, a, b$ | 35 | 18 |
| $c, b, a$ | 30 | 13 |

The ratio order $b, c, a$ is the unique optimum, with cost $25$. Each waiting time is the cost minus $\sum_j w_j p_j = 3 + 2 + 12 = 17$, so the two columns rank the orders in the same way.

**Five jobs.** The [Smith's rule page](/smiths-rule/) works a batch of five jobs with ties, where the optimum is $158$ and four orders reach it.

**A non-example.** If job $b$ of the first example is released only at time $4$, the problem is $1 \mid r_j \mid \sum w_j C_j$ and the definition above does not apply. The ratio order $b, c, a$ must idle until time $4$ and costs $2 \cdot 5 + 3 \cdot 9 + 1 \cdot 12 = 49$, while $c, b, a$ costs $3 \cdot 4 + 2 \cdot 5 + 1 \cdot 8 = 30$.

## Known algorithms

- **[Smith's rule](/smiths-rule/).** Sort by $p_j / w_j$, smallest first. Optimal, $\Theta(n \log n)$ time and $\Theta(n)$ space. The proof swaps adjacent jobs: a swap of $i$ then $j$ changes the cost by $w_i p_j - w_j p_i$.
- **Brute force.** Try all $n!$ orders. Useful only as a test oracle for $n \le 8$ or so.
- **Dynamic programming over subsets.** The best order of a set $S$ ends with some job $j$ that completes at $p(S)$, so $\mathrm{OPT}(S) = \min_{j \in S} (\mathrm{OPT}(S - \{j\}) + w_j\, p(S))$. This takes $O(2^n n)$ time. It is not needed here, but it is the standard exact method for the NP-hard variants with precedence.

## Bounds

- **Upper bound.** $O(n \log n)$ time by Smith's rule.
- **Lower bound.** With unit weights and distinct processing times, the optimal order is the sorted order of the $p_j$, and it is unique. So in the comparison model any algorithm that outputs an optimal order needs $\Omega(n \log n)$ comparisons in the worst case. Smith's rule is optimal in this model.
- **The value of the optimum.** In ratio order, $\mathrm{OPT} = \sum_{i \le j} w_j p_i$ over pairs with $i$ at or before $j$, a sum that can be computed in $O(n)$ after the sort.

## Reductions

- **From sorting.** Sorting $n$ distinct numbers reduces to $1 \| \sum C_j$: use the numbers as processing times, which gives the lower bound above.
- **To the general problem.** $1 \| \sum w_j C_j$ is the case $m = 1$, no release dates and no precedence of [the general weighted completion time problem](/weighted-completion-time-scheduling/), and the case of one machine of the [scheduling problem](/scheduling-problem/).
- **A pair cost view.** $\sum_j w_j C_j = \sum_j w_j p_j + \sum_{i \ne j,\ i \text{ before } j} w_j p_i$. For each unordered pair, the order adds either $w_j p_i$ or $w_i p_j$. Choosing the smaller one for each pair separately gives a lower bound, and the ratio order meets it for every pair at the same time, which is a second proof of optimality.

## Applications

- **Batch queues.** A batch scheduler that wants to minimize the weighted mean response time of the jobs in a queue sorts them by Smith's rule. With equal weights this is [shortest job first](/shortest-job-first/), whose optimality is [this proof](/sjf-optimality/) with unit weights.
- **Request ordering in one worker.** A worker that holds several requests, each blocking $w_j$ clients, serves them in ratio order to minimize total client waiting.
- **A subproblem.** The ratio rule is the building block of Sidney decomposition for precedence constraints and of list schedules on parallel machines.

## References
