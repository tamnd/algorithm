---
tag: 7Y0GYX
kind: algorithm
slug: johnsons-rule
name: Johnson's rule
aliases:
- Johnson's algorithm for two-machine flow shop
- Johnson's two-list rule
area: systems/scheduling
level: advanced
summary: "For jobs that run on machine 1 then machine 2: jobs with a ≤ b first by increasing a, then the rest by decreasing b. This order minimizes the makespan of F2||Cmax."
solves: [two-machine-flow-shop]
model: word-ram
complexity:
  vars: {n: the number of jobs}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, online: false, recursive: false}
history:
  year: 1954
  people: [S. M. Johnson]
  note: Johnson gave the rule and its proof in the first volume of the Naval Research Logistics Quarterly, for two-stage production.
prereqs: [two-machine-flow-shop, exchange-argument]
see_also: [johnsons-rule-two-machine-flow-shop, three-machine-flow-shop, flow-shop-scheduling, makespan-lower-bounds, smiths-rule, job-shop-scheduling, sorting-problem, makespan]
sources:
  - paper: doi:10.1002/nav.3800010110
    title: S. M. Johnson, Optimal two- and three-stage production schedules with setup times included, Naval Research Logistics Quarterly 1(1), 1954
    locator: pages 61 to 68 (the rule, the condition min(a_i, b_j) ≤ min(a_j, b_i), and its proof)
  - book: isbn:9783319265780
    title: Michael L. Pinedo, Scheduling, Theory, Algorithms, and Systems, fifth edition
    locator: Chapter 6, Section 6.1, Flow Shops with Unlimited Intermediate Storage (the SPT(1)-LPT(2) form of the rule)
  - book: isbn:9783540695158
    title: Peter Brucker, Scheduling Algorithms, fifth edition
    locator: Chapter 6, Shop Scheduling Problems (the two-machine flow shop)
  - paper: doi:10.1002/nav.3800030307
    title: James R. Jackson, An extension of Johnson's results on job lot scheduling, Naval Research Logistics Quarterly 3(3), 1956
    locator: pages 201 to 203 (the rule for the two-machine job shop)
  - paper: doi:10.1287/moor.1.2.117
    title: M. R. Garey, D. S. Johnson and Ravi Sethi, The complexity of flowshop and jobshop scheduling, Mathematics of Operations Research 1(2), 1976
    locator: pages 117 to 129 (three machines are strongly NP-hard, so the rule does not extend)
---

Johnson's rule finds an optimal order for the [two-machine flow shop](/two-machine-flow-shop/) $F2 \| C_{\max}$, in which each job runs first on machine 1 for time $a_j$ and then on machine 2 for time $b_j$. It splits the jobs into those with $a_j \le b_j$ and those with $a_j > b_j$. The first group goes first, in increasing order of $a_j$; the second group goes last, in decreasing order of $b_j$. The cost is one sort, $\Theta(n \log n)$ time. This page is the two-list algorithm as one implements it, with a proof by adjacent swaps; the [theorem page](/johnsons-rule-two-machine-flow-shop/) has Johnson's original smallest-time procedure and the proof that one order on both machines is enough, and the [approximation-area flow shop page](/flow-shop-scheduling/) places the rule among the methods for $m$ machines.

## In plain words

Every job passes two stations, first station 1 and then station 2. The aim is to keep station 2 busy. At the start, station 2 can do nothing until the first job leaves station 1, so the first job should be quick at station 1. At the end, station 1 is done and only station 2 works, so the last job should be quick at station 2. Johnson's rule does this for the whole list. Jobs that are quicker at station 1 than at station 2 go first, quickest at station 1 first. The other jobs go after them, with the job that is slowest at station 2 first and the quickest at station 2 last.

## The problem

There are $n$ jobs. Job $j$ needs $a_j \ge 0$ on machine 1 and then $b_j \ge 0$ on machine 2. Each machine runs one job at a time, without preemption, and the buffer between them has no limit. The goal is a schedule with the least makespan. An optimal schedule exists that runs both machines in the same order; for such an order $\pi$, with each operation as early as possible, the makespan is

$$C_{\max}(\pi) = \max_{1 \le k \le n} \Big( \sum_{l \le k} a_{\pi(l)} + \sum_{l \ge k} b_{\pi(l)} \Big).$$

## The algorithm

```pseudo id=main
JOHNSONS-RULE(a[1 .. n], b[1 .. n])
L1  F ← the jobs j with a[j] ≤ b[j]
L2  G ← the jobs j with a[j] > b[j]
L3  sort F by a[j], increasing
L4  sort G by b[j], decreasing
L5  π ← F followed by G
L6  t1 ← 0; t2 ← 0
L7  for k ← 1 to n do
L8      t1 ← t1 + a[π(k)]               ▷ job π(k) leaves machine 1
L9      t2 ← max(t2, t1) + b[π(k)]      ▷ job π(k) leaves machine 2
L10 return π, t2
```

Lines L1 to L5 are the rule. Lines L6 to L10 run the order and compute the makespan $t_2$; machine 2 starts each job when both the job has left machine 1 and the previous job has left machine 2. A job with $a_j = b_j$ can go in either group; the proof works with both choices.

## Example

Six jobs.

| job | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| $a_j$ | 4 | 2 | 6 | 3 | 5 | 1 |
| $b_j$ | 3 | 5 | 2 | 6 | 5 | 2 |

Line L1 gives $F = \{2, 4, 5, 6\}$ (job 5 has $a_5 = b_5$), and line L2 gives $G = \{1, 3\}$. Line L3 sorts $F$ by $a_j$ to $6, 2, 4, 5$. Line L4 sorts $G$ by $b_j$, largest first, to $1, 3$. So $\pi = 6, 2, 4, 5, 1, 3$.

| job | machine 1 | machine 2 |
|---|---|---|
| 6 | 0 to 1 | 1 to 3 |
| 2 | 1 to 3 | 3 to 8 |
| 4 | 3 to 6 | 8 to 14 |
| 5 | 6 to 11 | 14 to 19 |
| 1 | 11 to 15 | 19 to 22 |
| 3 | 15 to 21 | 22 to 24 |

The makespan is $24$. Machine 2 is idle only from $0$ to $1$, so the makespan equals $\min_j a_j + \sum_j b_j = 1 + 23$, a lower bound for every schedule, and the order is optimal. The input order $1, 2, \ldots, 6$ takes $28$, and over all $720$ orders the makespan ranges from $24$ to $33$, with $7$ optimal orders.

## Correctness

Swap two adjacent jobs $i$ and $j$ in an order, with $A$ the machine 1 time before them and $B$ the machine 2 time after them. In the formula for $C_{\max}$ only the two terms of their positions change. With $i$ first these terms are $A + a_i + b_i + b_j + B$ and $A + a_i + a_j + b_j + B$, and their maximum is $A + B + a_i + b_i + a_j + b_j - \min(a_j, b_i)$. So $i$ before $j$ is no worse than $j$ before $i$ when $\min(a_i, b_j) \le \min(a_j, b_i)$. A short case check shows that the order of line L5 has this property for every pair $i$ before $j$, not only adjacent ones: two jobs of $F$ have $\min(a_i, b_j) \le a_i \le \min(a_j, b_i)$; two jobs of $G$ have $\min(a_i, b_j) \le b_j \le \min(a_j, b_i)$; and a job of $F$ before a job of $G$ is covered by $a_i \le b_i$ and $b_j < a_j$. Now take an optimal order and move it to $\pi$ by swapping adjacent pairs that are in the other order in $\pi$, as in bubble sort. Each swap puts a pair into its order in $\pi$, so it does not raise the makespan. So $\pi$ is optimal. The full proof is below.

## Complexity

- **Time.** Lines L1 and L2 take $\Theta(n)$. Lines L3 and L4 are two sorts, $\Theta(n \log n)$ in the worst case. Lines L6 to L10 take $\Theta(n)$.
- **Space.** $\Theta(n)$ for the two lists and the order.

## Properties

- **Exact** for $F2 \| C_{\max}$.
- **A check by lower bounds.** When the makespan meets $\min_j a_j + \sum_j b_j$ or $\sum_j a_j + \min_j b_j$, as in the example, the order is optimal for that reason alone. This does not always happen; the optimum can be above both bounds.
- **Ties.** Jobs with $a_j = b_j$ may go in either group, and ties inside a group may be broken in any way; every such order is optimal.
- **Mirror.** Swapping the machines and reversing the order gives an optimal order for the instance $(b, a)$, with the same makespan.

## Variants and improvements

- **One-list form.** Sort all jobs by the key $\min(a_j, b_j)$, and send a job to the front if its minimum is $a_j$ and to the back if it is $b_j$. This is Johnson's original procedure; the [theorem page](/johnsons-rule-two-machine-flow-shop/) implements it.
- **Three machines.** $F3 \| C_{\max}$ is strongly NP-hard (Garey, Johnson and Sethi 1976). If the middle machine is dominated, the rule applied to the times $(a_j + b_j, b_j + c_j)$ is optimal; see [three-machine flow shop](/three-machine-flow-shop/).
- **Many machines.** For $m$ machines, one can group the machines into two virtual machines, apply the rule to the summed times, and use the order as a start for a heuristic such as NEH or local search; see [flow shop scheduling](/flow-shop-scheduling/). No guarantee of optimality carries over.
- **Two-machine job shop.** Jackson 1956 extended the rule to two machines where each job has its own route of at most two operations; see [job shop scheduling](/job-shop-scheduling/).

## When to use it

Use it for a batch of jobs that pass two stages in the same order, with one server per stage and a buffer between them, when the goal is to finish the whole batch early: read then compute, compute then write, upload then process. All jobs must be known in advance. If the goal is the mean completion time rather than the batch time, the problem is strongly NP-hard and the rule is only a heuristic.

## Pitfalls

- **Sorting the second group the wrong way.** The jobs with $a_j > b_j$ go in decreasing order of $b_j$, not increasing.
- **Splitting on the wrong test.** The groups depend on comparing $a_j$ with $b_j$ for the same job, not on comparing jobs.
- **Using the pairwise test as a sort key.** The relation $\min(a_i, b_j) \le \min(a_j, b_i)$ is not transitive when there are ties, so a comparison sort with it as the comparator can return a wrong order. The [theorem page](/johnsons-rule-two-machine-flow-shop/) shows an instance. Use the two-list form or the one-list form, which sort by a real key.
- **Different orders on the two machines.** This never helps for two machines, so do not search over them.
- **Using it for the mean completion time.** It minimizes the makespan only.

## Implementations

## History

S. M. Johnson of the RAND Corporation published the rule in 1954, in the first issue of the Naval Research Logistics Quarterly. The paper treats two-stage production with setup times included in the processing times, proves the rule optimal for two stages, and gives a special case for three stages. It is one of the first exact results of scheduling theory. The two-list form is the usual textbook statement; Pinedo calls it SPT(1)-LPT(2).

## References
