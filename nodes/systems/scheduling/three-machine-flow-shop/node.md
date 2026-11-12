---
tag: F4DF7W
kind: problem
slug: three-machine-flow-shop
name: Scheduling jobs on three machines
aliases:
- F3||Cmax
- three-stage flow shop
area: systems/scheduling
level: advanced
summary: "Jobs run on machines 1, 2 and 3 in this order; minimize the makespan, F3||Cmax. Strongly NP-hard, but Johnson's rule is optimal when the middle machine is dominated."
prereqs: [two-machine-flow-shop, johnsons-rule, strong-np-hardness]
see_also: [johnsons-rule-two-machine-flow-shop, flow-shop-scheduling, three-partition, job-shop-scheduling, makespan-lower-bounds, np-hard, local-search, open-shop-scheduling]
sources:
  - paper: doi:10.1002/nav.3800010110
    title: S. M. Johnson, Optimal two- and three-stage production schedules with setup times included, Naval Research Logistics Quarterly 1(1), 1954
    locator: pages 61 to 68 (the three-stage special case with a dominated middle stage)
  - paper: doi:10.1287/moor.1.2.117
    title: M. R. Garey, D. S. Johnson and Ravi Sethi, The complexity of flowshop and jobshop scheduling, Mathematics of Operations Research 1(2), 1976
    locator: pages 117 to 129 (F3||Cmax is strongly NP-hard, by a reduction from 3-partition)
  - book: isbn:9783319265780
    title: Michael L. Pinedo, Scheduling, Theory, Algorithms, and Systems, fifth edition
    locator: Chapter 6, Section 6.1, Flow Shops with Unlimited Intermediate Storage (permutation schedules for m ≤ 3, and the NP-hardness of F3||Cmax)
  - book: isbn:9783540695158
    title: Peter Brucker, Scheduling Algorithms, fifth edition
    locator: Chapter 6, Shop Scheduling Problems (flow shop problems)
---

The three-machine flow shop is the problem of scheduling $n$ jobs that each run on machine 1, then on machine 2, then on machine 3, so that the last job finishes as early as possible. In [Graham's notation](/scheduling-notation/) it is $F3 \| C_{\max}$. It looks like a small step from the [two-machine flow shop](/two-machine-flow-shop/), which [Johnson's rule](/johnsons-rule/) solves with one sort, but it is strongly NP-hard (Garey, Johnson and Sethi 1976). One order on all three machines is still enough, so the problem is a search over $n!$ orders. Johnson's 1954 paper gives a special case that is easy: when the middle machine is dominated by the first or the last one, Johnson's rule on the summed times $(a_j + b_j,\ b_j + c_j)$ is optimal. This page gives that reduction and an instance outside the case where it fails. The [approximation-area flow shop page](/flow-shop-scheduling/) covers $m$ machines and their approximation algorithms.

## In plain words

Every job passes three stations in the same order. Each station handles one job at a time, and there is room for waiting jobs between the stations. For two stations there is a quick rule that gives the best order. For three stations no quick rule is known that always works, and most likely none exists, since the problem is as hard as the hardest search problems. There is one useful exception. If the middle station is always quick compared with the first station, or always quick compared with the last one, it never really holds things up. Then you can think of the first two stations as one, and of the last two as one, and use the two-station rule.

## Definition

**Input.** $n$ jobs. Job $j$ needs $a_j \ge 0$ on machine 1, then $b_j \ge 0$ on machine 2, then $c_j \ge 0$ on machine 3.

**Schedule.** Start times such that each machine runs at most one operation at a time, no operation is preempted, and each job starts on machine $i + 1$ only after it ends on machine $i$. Buffers have no limit.

**Goal.** Minimize the makespan $C_{\max}$.

**One order is enough.** For three machines there is always an optimal schedule that runs the jobs in the same order on all machines: an adjacent swap on machine 1 makes it agree with machine 2, and an adjacent swap on machine 3 makes it agree with machine 2, and neither swap delays anything. The [optimality page of Johnson's rule](/johnsons-rule-two-machine-flow-shop/) proves this and shows that it fails for four machines. For an order $\pi$, with each operation as early as possible,

$$C_{\max}(\pi) = \max_{1 \le k \le l \le n} \Big( \sum_{q \le k} a_{\pi(q)} + \sum_{k \le q \le l} b_{\pi(q)} + \sum_{q \ge l} c_{\pi(q)} \Big),$$

the longest path that leaves machine 1 at position $k$ and machine 2 at position $l$.

## Variants

- **Dominated middle machine.** If $\min_j a_j \ge \max_j b_j$ or $\min_j c_j \ge \max_j b_j$, the problem is solved in $O(n \log n)$ time by Johnson's rule on $(a_j + b_j,\ b_j + c_j)$ (Johnson 1954). See Known algorithms.
- **Two machines.** $F2 \| C_{\max}$ is solved by [Johnson's rule](/johnsons-rule/).
- **Preemption.** $F3 \mid pmtn \mid C_{\max}$ is also NP-hard; see [flow shop scheduling](/flow-shop-scheduling/).
- **More machines.** For $m \ge 4$ even the best permutation schedule may not be optimal, and the problem stays strongly NP-hard. For each fixed $m$ there is a polynomial-time approximation scheme; see [flow shop scheduling](/flow-shop-scheduling/).
- **Other shops.** In a [job shop](/job-shop-scheduling/) each job has its own route, and in an [open shop](/open-shop-scheduling/) the route is free. With three machines both are NP-hard for the makespan.

## Examples

**A dominated middle machine.** Five jobs:

| job | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| $a_j$ | 7 | 2 | 5 | 3 | 6 |
| $b_j$ | 4 | 1 | 3 | 2 | 4 |
| $c_j$ | 4 | 6 | 5 | 7 | 4 |
| $a_j + b_j$ | 11 | 3 | 8 | 5 | 10 |
| $b_j + c_j$ | 8 | 7 | 8 | 9 | 8 |

Here $\min_j c_j = 4 \ge 4 = \max_j b_j$, so the case applies, although $\min_j a_j = 2$ is less than $\max_j b_j$. Johnson's rule on the last two rows puts jobs 2, 4 and 3 first (their first time is at most their second), in increasing first time, then jobs 1 and 5 in decreasing second time. The order $2, 4, 3, 1, 5$ runs as follows.

| job | machine 1 | machine 2 | machine 3 |
|---|---|---|---|
| 2 | 0 to 2 | 2 to 3 | 3 to 9 |
| 4 | 2 to 5 | 5 to 7 | 9 to 16 |
| 3 | 5 to 10 | 10 to 13 | 16 to 21 |
| 1 | 10 to 17 | 17 to 21 | 21 to 25 |
| 5 | 17 to 23 | 23 to 27 | 27 to 31 |

The makespan is $31$, the optimum over all $120$ orders. The input order takes $37$ and the worst order $39$.

**Outside the case.** Two jobs: job 1 has $(a, b, c) = (1, 5, 5)$ and job 2 has $(1, 4, 2)$. The middle machine is not dominated, since $\max_j b_j = 5$ exceeds both $\min_j a_j = 1$ and $\min_j c_j = 2$. The summed times are $(6, 10)$ and $(5, 6)$, and Johnson's rule picks the order $2, 1$, with makespan $15$. The order $1, 2$ takes $13$:

| order | job | machine 1 | machine 2 | machine 3 |
|---|---|---|---|---|
| $2, 1$ | 2 | 0 to 1 | 1 to 5 | 5 to 7 |
| | 1 | 1 to 2 | 5 to 10 | 10 to 15 |
| $1, 2$ | 1 | 0 to 1 | 1 to 6 | 6 to 11 |
| | 2 | 1 to 2 | 6 to 10 | 11 to 13 |

The two-machine problem on the summed times ranks the orders the other way: $21$ for $2, 1$ and $22$ for $1, 2$. Its makespan stops matching the real one when the longest path leaves machine 1 and machine 2 at different jobs, which the condition on the middle machine rules out.

## Known algorithms

**The reduction for a dominated middle machine** (Johnson 1954).

```pseudo id=main
JOHNSON-THREE-MACHINE(a[1 .. n], b[1 .. n], c[1 .. n])
L1  if not (min a ≥ max b or min c ≥ max b) then the order below is only a heuristic
L2  for j ← 1 to n do a′[j] ← a[j] + b[j]; c′[j] ← b[j] + c[j]
L3  π ← JOHNSONS-RULE(a′, c′)
L4  t1 ← 0; t2 ← 0; t3 ← 0
L5  for k ← 1 to n do
L6      t1 ← t1 + a[π(k)]
L7      t2 ← max(t2, t1) + b[π(k)]
L8      t3 ← max(t3, t2) + c[π(k)]
L9  return π, t3
```

*Why it is optimal in the case.* Write $T(k, l)$ for the term of the makespan formula with $k \le l$. If $\min a \ge \max b$, then $T(l, l) - T(k, l) = \sum_{k < q \le l} a_{\pi(q)} - \sum_{k \le q < l} b_{\pi(q)} \ge 0$, since both sums have $l - k$ terms and each $a$ is at least each $b$. If $\min c \ge \max b$, then in the same way $T(k, k) \ge T(k, l)$. In both cases the maximum is reached with $k = l$, so $C_{\max}(\pi) = \max_k \big(\sum_{q \le k} a_{\pi(q)} + b_{\pi(k)} + \sum_{q \ge k} c_{\pi(q)}\big)$. Adding the constant $\sum_j b_j$ turns this into $\max_k \big(\sum_{q \le k} a'_{\pi(q)} + \sum_{q \ge k} c'_{\pi(q)}\big)$, the two-machine makespan of $\pi$ for the times $(a', c')$. So the order that is optimal for the two-machine instance, which line L3 finds, is optimal for the three-machine one, over all orders and so over all schedules.

**General instances.**

- **Exact search.** Branch and bound over orders, with bounds from the machine loads below, or an integer program. The search space is $n!$ orders.
- **Brute force.** All $n!$ orders with lines L4 to L9, practical for $n \le 8$.
- **Heuristics.** The reduction above, used outside its case, is a fast heuristic. Insertion heuristics and [local search](/local-search/) on orders are the usual tools for larger $n$; see [flow shop scheduling](/flow-shop-scheduling/).

## Bounds

- **Hardness.** Strongly NP-hard (Garey, Johnson and Sethi 1976). So there is no pseudo-polynomial algorithm and no fully polynomial approximation scheme unless P = NP.
- **Lower bounds on the makespan.** $C_{\max} \ge \max\big(\sum_j a_j + \min_j (b_j + c_j),\ \min_j a_j + \sum_j b_j + \min_j c_j,\ \min_j (a_j + b_j) + \sum_j c_j,\ \max_j (a_j + b_j + c_j)\big)$. Each machine load needs a head before it and a tail after it.
- **The special case.** $O(n \log n)$ time.

## Reductions

- **From 3-partition.** Garey, Johnson and Sethi reduce [3-partition](/three-partition/) to $F3 \| C_{\max}$. The instance is built so that a schedule meets the makespan target only if some jobs leave gaps of fixed length and the other jobs fill these gaps exactly, three at a time, which happens only if the numbers split into triples of equal sum. The numbers in the instance are bounded by a polynomial, so $F3 \| C_{\max}$ is strongly NP-hard. Since the dominated case is polynomial, hard instances must have a middle machine that is not dominated, unless P = NP.
- **To two machines, in the dominated case.** As in Known algorithms, the map $(a_j, b_j, c_j) \mapsto (a_j + b_j,\ b_j + c_j)$ reduces the case to $F2 \| C_{\max}$ and changes every makespan by the same constant $\sum_j b_j$.
- **To the general flow shop.** $F3 \| C_{\max}$ is the case $m = 3$ of [flow shop scheduling](/flow-shop-scheduling/).

## Applications

- **Three-stage pipelines.** Fetch, process and store; or upload, compute and download. When the middle stage is fast compared with one of its neighbours, as with a short transform between a slow read and a slow write, the reduction gives an optimal batch order at the cost of one sort.
- **Production lines.** Johnson's own setting, three production stages with one machine each.
- **Start orders for heuristics.** In general instances the reduction gives a good first order for local search or branch and bound.

## References
