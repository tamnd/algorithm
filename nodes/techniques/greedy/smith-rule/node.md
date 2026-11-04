---
tag: 5N4EPA
kind: algorithm
slug: smith-rule
name: Smith's rule
aliases:
- weighted shortest processing time first
- WSPT
- ratio rule
area: techniques/greedy
level: core
summary: Sort jobs by nonincreasing weight divided by processing time; optimal for weighted completion time.
solves: [minimizing-weighted-completion-time]
model: comparison-model
complexity:
  vars: {n: the number of jobs}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {stable: true, in_place: false, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
history:
  year: 1956
  people: [Wayne E. Smith]
  note: Smith proved the ratio rule for one machine in Naval Research Logistics Quarterly in 1956.
prereqs: [minimizing-weighted-completion-time, exchange-argument, sorting-problem]
see_also: [optimal-tape-storage, shortest-job-first, minimizing-maximum-lateness, greedy-algorithm, weighted-completion-time-scheduling, scheduling-notation]
sources:
  - paper: doi:10.1002/nav.3800030106
    title: Wayne E. Smith, Various optimizers for single-stage production, Naval Research Logistics Quarterly 3(1-2), 1956
    locator: pages 59 to 66
  - book: isbn:9783319265780
    title: Michael L. Pinedo, Scheduling, Theory, Algorithms, and Systems, fifth edition
    locator: Chapter 3, Single Machine Models (Deterministic), the WSPT rule for the total weighted completion time
  - book: isbn:9783540695158
    title: Peter Brucker, Scheduling Algorithms, fifth edition
    locator: Chapter 4, Single Machine Scheduling Problems
  - paper: doi:10.1287/opre.23.2.283
    title: Jeffrey B. Sidney, Decomposition algorithms for single-machine sequencing with precedence relations and deferral costs, Operations Research 23(2), 1975
    locator: pages 283 to 298
  - paper: doi:10.1016/s0167-5060(08)70323-6
    title: Eugene L. Lawler, Sequencing jobs to minimize total weighted completion time subject to precedence constraints, Annals of Discrete Mathematics 2, 1978
    locator: pages 75 to 90
  - paper: doi:10.1016/s0167-5060(08)70743-x
    title: J. K. Lenstra, A. H. G. Rinnooy Kan and P. Brucker, Complexity of machine scheduling problems, Annals of Discrete Mathematics 1, 1977
    locator: pages 343 to 362 (NP-hardness of the problem with release dates)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Chapter 4, exercises (scheduling jobs to minimize the weighted sum of completion times)
---

Smith's rule orders jobs on one machine by nonincreasing ratio $w_j / p_j$ of weight to processing time, and this order minimizes the weighted sum of completion times $\sum_j w_j C_j$. It is also called weighted shortest processing time first (WSPT). It solves the problem $1 \| \sum w_j C_j$ of [minimizing weighted completion time](/minimizing-weighted-completion-time/) in $\Theta(n \log n)$ time, the cost of one sort. Its proof is the textbook [exchange argument](/exchange-argument/): swapping two adjacent jobs that break the rule always lowers the cost.

## In plain words

One machine must do several jobs, one after another. Each job takes some time, and each job has an importance. Every job pays its importance for every unit of time it waits until it is done, so the cost of a job is its importance times its finish time. You want the smallest total cost.

Look at two jobs that run one right after the other. Swapping them does not change when the pair is done or what the other jobs pay. It only changes which of the two waits for the other. The first job makes the second wait its own length, and the second would make the first wait its length. So the job that should go first is the one with more importance per unit of length.

The rule follows: sort the jobs by importance divided by length, from high to low.

## The problem

The input is a set of $n$ jobs. Job $j$ has a processing time $p_j > 0$ and a weight $w_j$, a real number, usually $w_j \ge 0$. A schedule is an order $\pi = (\pi_1, \ldots, \pi_n)$ of the jobs on one machine, with no idle time and no preemption. The completion time of the job in position $i$ is $C_{\pi_i} = p_{\pi_1} + \cdots + p_{\pi_i}$. The goal is an order that minimizes
$$ \sum_{j} w_j C_j. $$
In [three-field notation](/scheduling-notation/) this is $1 \| \sum w_j C_j$. With all $w_j = 1$ it is $1 \| \sum C_j$, which [shortest job first](/shortest-job-first/) solves.

## The algorithm

```pseudo id=main
SMITH-RULE(J)                       ▷ J: n jobs with p(j) > 0
L1  sort J into j1, ..., jn with w(ja)·p(jb) ≥ w(jb)·p(ja) for a < b
                                     ▷ the ratios w/p are nonincreasing; ties in input order
L2  t ← 0, total ← 0
L3  for i ← 1 to n do
L4      t ← t + p(ji)                 ▷ t is the completion time of ji
L5      total ← total + w(ji)·t
L6  return (j1, ..., jn), total
```

Line L1 is the rule. It compares two jobs by the cross products $w_a p_b$ and $w_b p_a$, which gives the same order as the ratios $w_a / p_a$ and $w_b / p_b$ because $p_a, p_b > 0$, and it avoids division and rounding for integer data. Lines L2 to L5 compute the completion times and the cost of the order. A job with weight 0 has ratio 0 and goes after all jobs with positive weight.

## Example

Six jobs, with $(p_j, w_j)$: $A = (3, 1)$, $B = (1, 2)$, $C = (4, 4)$, $D = (2, 5)$, $E = (5, 3)$, $F = (2, 2)$. The ratios $w_j / p_j$ are $1/3$, $2$, $1$, $5/2$, $3/5$ and $1$. Line L1 gives the order $D, B, C, F, E, A$, with $C$ before $F$ because of their input order.

| $i$ | job | $p$ | $w$ | $w/p$ | $t = C_j$ after L4 | $w_j C_j$ | total after L5 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | $D$ | 2 | 5 | 2.5 | 2 | 10 | 10 |
| 2 | $B$ | 1 | 2 | 2 | 3 | 6 | 16 |
| 3 | $C$ | 4 | 4 | 1 | 7 | 28 | 44 |
| 4 | $F$ | 2 | 2 | 1 | 9 | 18 | 62 |
| 5 | $E$ | 5 | 3 | 0.6 | 14 | 42 | 104 |
| 6 | $A$ | 3 | 1 | 0.333 | 17 | 17 | 121 |

The cost is 121, the minimum over all $720$ orders. Exactly two orders reach it, this one and the one with $F$ before $C$, which have equal ratios. For comparison, shortest processing time first ($B, D, F, A, C, E$) costs 134, largest weight first ($D, C, E, B, F, A$) costs 136, the input order costs 172, and the worst order costs 218.

## Correctness

The key fact is the effect of one adjacent swap. Let $a$ and $b$ be adjacent in an order, with $a$ first, and let $s$ be the time when $a$ starts. Before the swap they pay $w_a(s + p_a) + w_b(s + p_a + p_b)$. After the swap they pay $w_b(s + p_b) + w_a(s + p_a + p_b)$. All other jobs keep their completion times. So

$$ \text{cost after} - \text{cost before} = w_a p_b - w_b p_a. $$

If $w_a / p_a < w_b / p_b$, the difference is negative and the swap helps. So no optimal order has an adjacent pair with an increasing ratio, which means every optimal order is sorted by nonincreasing ratio. If two adjacent jobs have equal ratios, the difference is 0. Any two orders sorted by nonincreasing ratio differ only inside blocks of equal ratio, and adjacent swaps inside a block turn one into the other without changing the cost. So all such orders have the same cost, and the order of line L1 is optimal. The full proof is below. The proof does not use the sign of the weights.

## Complexity

- **Time.** Line L1 is a comparison sort with $O(n \log n)$ comparisons in the worst case, for example with [merge sort](/merge-sort/). Lines L3 to L5 take $\Theta(n)$ time. The total is $\Theta(n \log n)$ for a comparison sort.
- **Lower bound.** In the comparison model, where the algorithm compares ratios, $\Omega(n \log n)$ comparisons are necessary in the worst case: for distinct weights and $p_j = 1$, the ratios are distinct and the unique optimal order is the sorted order of the weights, so any algorithm that outputs an optimal order sorts the weights.
- **Space.** $\Theta(n)$ for the sorted order. The loop uses $O(1)$ extra space.
- **Arithmetic.** With integer data, the products in line L1 have about twice the bits of the input, and the total in line L5 is at most $n \cdot \max_j w_j \cdot \sum_j p_j$.

## Properties

- **Stable.** With a stable sort, jobs with equal ratios stay in input order. This does not change the cost.
- **Every optimal order is a Smith order.** By the swap identity, an order is optimal if and only if its ratios are nonincreasing. So the rule describes all optimal solutions, not only one.
- **Exact for any real weights.** The proof holds for negative weights too. Only $p_j > 0$ is needed.
- **Not online.** The rule needs all jobs at time 0. With release dates the problem changes (see Variants).

## Variants and improvements

- **Shortest processing time first.** With equal weights the rule sorts by $p_j$ alone. This is [shortest job first](/shortest-job-first/), and it minimizes the mean completion time. Storing files on a tape is the same problem; see [optimal tape storage](/optimal-tape-storage/).
- **Chains and series-parallel precedence.** If the jobs form chains that must run in order, Smith's ratio extends to a chain prefix: the ratio of a prefix is its total weight over its total processing time. Sidney (1975) gave a decomposition method for precedence constraints, and Lawler (1978) gave an $O(n \log n)$ algorithm for series-parallel precedence and proved the general precedence case NP-hard. See [minimizing weighted completion time](/minimizing-weighted-completion-time/).
- **Release dates.** With release dates $r_j$ and no preemption, even $1 | r_j | \sum C_j$ is NP-hard, and Smith's rule is only a heuristic. With preemption and equal weights, shortest remaining processing time first is optimal.
- **Parallel machines.** On identical parallel machines, Smith's rule used as a list rule is an approximation, not an exact algorithm. See [weighted completion time scheduling](/weighted-completion-time-scheduling/).

## When to use it

Use it whenever one machine must order jobs that are all ready at the start, with no deadlines and no precedence, and the cost is a weighted sum of completion times. It is exact and it costs one sort. If there are deadlines, the objective is different: use [earliest due date first](/minimizing-maximum-lateness/) for the maximum lateness or [Moore and Hodgson](/minimizing-number-of-late-jobs/) for the number of late jobs. If there are precedence constraints or release dates, the rule is no longer exact.

## Pitfalls

- **Sorting by the wrong key.** Sorting by $p_j$ alone (shortest first) or by $w_j$ alone (heaviest first) in line L1 is wrong when the weights differ: on the example they cost 134 and 136 against 121. Sort by $w_j / p_j$.
- **Sorting in the wrong direction.** The ratio $w_j / p_j$ must be nonincreasing. If the rule is written with the inverse ratio $p_j / w_j$, the order is nondecreasing. Mixing the two gives the worst order of the pair at each step.
- **Division by zero and rounding.** Computing $p_j / w_j$ fails for $w_j = 0$, and floating-point ratios can order two equal ratios wrongly. Compare the cross products $w_a p_b$ and $w_b p_a$, as line L1 does.
- **Overflow.** In 64-bit integers, $w_a p_b$ can overflow when both factors are near $2^{32}$, and the total in line L5 can overflow much earlier. Use wider integers or check the ranges.
- **Idle time.** The proof assumes the machine never waits. With release dates, a job may not be ready, and the swap identity no longer holds.

## Implementations

## History

Wayne E. Smith published the ratio rule in 1956, in "Various optimizers for single-stage production" in Naval Research Logistics Quarterly, with the adjacent-swap proof. Scheduling texts such as Pinedo and Brucker now give it as the WSPT rule. Sidney in 1975 and Lawler in 1978 extended it to precedence constraints.

## References
