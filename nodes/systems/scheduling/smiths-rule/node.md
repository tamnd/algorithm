---
tag: 51P9W7
kind: algorithm
slug: smiths-rule
name: "Smith's rule for weighted completion time"
aliases:
- weighted shortest processing time
- Smith's ratio rule for 1||sum wjCj
area: systems/scheduling
level: advanced
summary: "Sort the jobs on one machine by processing time divided by weight, smallest first. This order minimizes the weighted sum of completion times, 1||ΣwjCj (Smith 1956)."
solves: [weighted-completion-time]
model: word-ram
complexity:
  vars: {n: the number of jobs}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, online: false, recursive: false, stable: true}
history:
  year: 1956
  people: [Wayne E. Smith]
  note: Smith proved in 1956 that the ratio order is optimal for the weighted sum of completion times on one machine.
prereqs: [weighted-completion-time, exchange-argument, sorting-problem]
see_also: [smith-rule, weighted-completion-time-scheduling, shortest-job-first, shortest-processing-time-first, sidney-decomposition, single-machine-scheduling, srpt, scheduling-metrics]
sources:
  - paper: doi:10.1002/nav.3800030106
    title: Wayne E. Smith, Various optimizers for single-stage production, Naval Research Logistics Quarterly 3(1-2), 1956
    locator: pages 59 to 66 (the ratio rule and its proof by an exchange of adjacent jobs)
  - book: isbn:9783319265780
    title: Michael L. Pinedo, Scheduling, Theory, Algorithms, and Systems, fifth edition
    locator: Chapter 3, Section 3.1, The Total Weighted Completion Time (the WSPT rule and the chain version)
  - book: isbn:9783540695158
    title: Peter Brucker, Scheduling Algorithms, fifth edition
    locator: Chapter 4, Single Machine Scheduling Problems (the total weighted completion time)
  - paper: "Tsuyoshi Kawaguchi and Seiki Kyan, Worst case bound of an LRF schedule for the mean weighted flow-time problem, SIAM Journal on Computing 15(4), 1986"
    locator: pages 1119 to 1129 (the ratio rule as a list schedule on parallel machines)
---

Smith's rule, also called WSPT (weighted shortest processing time first), runs the jobs on one machine in nondecreasing order of the ratio $p_j / w_j$ of [processing time](/scheduling-metrics/) to weight. It solves the [weighted completion time problem](/weighted-completion-time/) $1 \| \sum w_j C_j$ exactly, with one sort, in $\Theta(n \log n)$ time. With all weights equal it becomes [shortest job first](/shortest-job-first/). This page is the systems view with a tested implementation; the greedy-technique page [Smith's rule](/smith-rule/) has the same rule with a longer exchange proof, and [the general weighted completion time problem](/weighted-completion-time-scheduling/) covers the hard variants and their approximations.

## In plain words

A machine has a queue of jobs. Each job takes some time and has an importance, for example the number of users who wait for it. Each user is unhappy for as long as the job of that user is not done. To make the total unhappiness small, look at how much work each job needs for each unit of importance. Run the job with the least work per unit of importance first, then the next one, and so on. A short job that many people wait for goes early. A long job that only one person waits for goes last.

## The problem

There are $n$ jobs, all present at time $0$, on one machine that runs one job at a time without preemption. Job $j$ has a processing time $p_j \ge 0$ and a weight $w_j > 0$. An order $\pi$ runs the jobs back to back, so the completion time of the job in position $k$ is $C_{\pi(k)} = \sum_{i \le k} p_{\pi(i)}$. The goal is an order with the least cost $\sum_j w_j C_j$. In [Graham's notation](/scheduling-notation/) this is $1 \| \sum w_j C_j$. Idle time only makes each $C_j$ larger, so an optimal schedule has none.

## The algorithm

```pseudo id=main
SMITHS-RULE(p[1 .. n], w[1 .. n])
L1  π ← the jobs 1 .. n, sorted stably by p[j] / w[j], smallest first
L2  t ← 0, cost ← 0
L3  for k ← 1 to n do
L4      t ← t + p[π(k)]                      ▷ completion time of job π(k)
L5      cost ← cost + w[π(k)] · t
L6  return π, cost
```

Line L1 is the whole rule. Compare two ratios exactly, with $p_i w_j \le p_j w_i$ in integers or with fractions; a floating point key can order two equal ratios the wrong way, which here does no harm to the cost, and an integer division $\lfloor p_j / w_j \rfloor$ can order two different ratios the wrong way, which does harm. Lines L2 to L5 only compute the cost.

## Example

A batch server has five jobs in its queue. The weight $w_j$ is the number of users who wait for job $j$, so $\sum_j w_j C_j$ is the total waiting time of the users.

| job | $p_j$ | $w_j$ | $p_j / w_j$ |
|---|---|---|---|
| 0 | 8 | 4 | 2 |
| 1 | 2 | 1 | 2 |
| 2 | 5 | 5 | 1 |
| 3 | 3 | 1 | 3 |
| 4 | 6 | 2 | 3 |

Line L1 gives the order $2, 0, 1, 3, 4$. Jobs 0 and 1 have equal ratios, and so do jobs 3 and 4; the stable sort keeps their input order.

| position | job | $C_j$ | $w_j C_j$ | cost so far |
|---|---|---|---|---|
| 1 | 2 | 5 | 25 | 25 |
| 2 | 0 | 13 | 52 | 77 |
| 3 | 1 | 15 | 15 | 92 |
| 4 | 3 | 18 | 18 | 110 |
| 5 | 4 | 24 | 48 | 158 |

The cost is 158, the least over all $120$ orders. Four orders reach it: the two orders of each tied pair. Shortest job first ($1, 3, 2, 4, 0$) costs 185, heaviest job first ($2, 0, 4, 1, 3$) costs 160, the input order costs 183, and the worst order costs 228. Heaviest first comes close here only because the heaviest job is also the one with the best ratio.

## Correctness

Swap two adjacent jobs $i$ and $j$, with $i$ first, that start at time $t$. All other jobs keep their completion times. Before the swap the two jobs add $w_i(t + p_i) + w_j(t + p_i + p_j)$; after it they add $w_j(t + p_j) + w_i(t + p_i + p_j)$. The difference, after minus before, is $w_i p_j - w_j p_i$. So the swap lowers the cost exactly when $p_j / w_j < p_i / w_i$, that is, when the pair was out of ratio order. Any order can be turned into the order of line L1 by swaps of adjacent out-of-order pairs, as in bubble sort, and no such swap raises the cost. So the order of line L1 is optimal. When all weights are positive, every optimal order is in ratio order, because an order with an adjacent out-of-order pair can be improved. The full proof is below, and the [technique page](/smith-rule/) gives the same argument in a longer form.

## Complexity

- **Time.** Line L1 is a comparison sort of $n$ keys, $\Theta(n \log n)$ in each case. Lines L3 to L5 take $\Theta(n)$.
- **Space.** $\Theta(n)$ for the order.
- **Lower bound.** With unit weights the rule must output the jobs sorted by $p_j$, so in the comparison model no exact method for $1 \| \sum w_j C_j$ that outputs the order is faster than $\Omega(n \log n)$.

## Properties

- **Exact.** It is optimal for $1 \| \sum w_j C_j$ by the exchange argument above, not only a heuristic.
- **Only the ratio matters.** Scaling all weights by one positive number, or all times by one positive number, does not change the order.
- **Equal ratios are free.** Jobs with the same ratio can go in any order; the cost is the same.
- **Weight zero goes last.** A job with $w_j = 0$ has an infinite ratio. It adds nothing to the cost, so it goes at the end. The implementation treats it this way.
- **Not online.** The rule needs all jobs at time $0$.

## Variants and improvements

- **Unit weights.** $1 \| \sum C_j$ is solved by [shortest processing time first](/shortest-processing-time-first/), which is the same rule with $w_j = 1$. In an operating system this order is [shortest job first](/shortest-job-first/), and [its optimality](/sjf-optimality/) is the special case of the proof here.
- **Chains.** If the jobs form chains that must run in order, Smith's rule applies to the best prefix of each chain, the one with the least ratio of total time to total weight. Pinedo, Section 3.1, gives this rule.
- **Series-parallel and general precedence.** [Sidney decomposition](/sidney-decomposition/) extends the ratio idea. With general precedence constraints, $1 \mid prec \mid \sum w_j C_j$ is NP-hard, and every order consistent with a Sidney decomposition is a 2-approximation.
- **Release dates.** With release dates the problem $1 \mid r_j \mid \sum C_j$ is already strongly NP-hard (Lenstra, Rinnooy Kan and Brucker 1977). For unit weights with preemption, [SRPT](/srpt/) is optimal. See [weighted completion time scheduling](/weighted-completion-time-scheduling/).
- **Parallel machines.** On identical machines, assign the jobs in Smith's order, each to the machine that becomes free first. This is optimal for unit weights and has ratio $(1 + \sqrt 2)/2$ for general weights (Kawaguchi and Kyan 1986).

## When to use it

Use Smith's rule when one server runs a batch of jobs that are all present, and the cost of a job is its weight times its completion time: the weighted mean response time of a batch queue, the order of requests in one disk or network batch when each request has a priority, or the order of queries in a single worker when some queries block more clients. If jobs arrive over time, the rule is a heuristic; use it at each decision point among the jobs present, and expect no guarantee of optimality.

## Pitfalls

- **The ratio upside down.** Sorting by $w_j / p_j$ in increasing order runs the worst jobs first. The rule is $p_j / w_j$ increasing, or $w_j / p_j$ decreasing.
- **Integer division.** In integer code, $p_j / w_j$ with floor division makes $5/3$ and $4/3$ equal. Compare $p_i w_j$ with $p_j w_i$, or use exact fractions.
- **Weight zero.** A division by $w_j = 0$ fails. Put such jobs at the end.
- **Release dates.** The rule is not optimal when jobs arrive over time. Job A has $r = 0$, $p = 10$, $w = 1$, and job B has $r = 1$, $p = 1$, $w = 10$. Running the only job present, A, at time 0 gives $C_A = 10$ and $C_B = 11$, a cost of $120$. Waiting for B gives $C_B = 2$ and $C_A = 12$, a cost of $32$.
- **Mixing up objectives.** Smith's rule minimizes the weighted sum, not the weighted maximum and not the number of late jobs. For those, see the [overview of one-machine problems](/single-machine-scheduling/).

## Implementations

## History

Wayne E. Smith published the rule in 1956 in the Naval Research Logistics Quarterly, in a paper on several sequencing rules for one production stage. The proof by an exchange of two adjacent jobs comes from that paper. The rule for chains and the extensions to precedence constraints came later; Pinedo, Section 3.1, gives the chain rule.

## References
