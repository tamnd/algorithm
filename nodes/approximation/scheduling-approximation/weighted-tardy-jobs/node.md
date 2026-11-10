---
tag: 44W58E
kind: problem
slug: weighted-tardy-jobs
name: Minimizing the weighted number of tardy jobs
aliases:
- 1||sum wjUj
- weighted number of late jobs
- job sequencing with penalties
area: approximation/scheduling-approximation
level: advanced
summary: Choose which weighted jobs are late on one machine to minimize their total weight. NP-hard (Karp 1972), solved in O(n sum p_j) time by Lawler and Moore, with an FPTAS by rounding weights.
prereqs: [minimizing-tardy-jobs, knapsack-problem, pseudo-polynomial-time, fptas]
see_also: [minimizing-tardy-jobs, minimizing-number-of-late-jobs, knapsack-fptas, rounding-and-scaling, weak-np-hardness, karps-21-np-complete-problems, total-tardiness-minimization, scheduling-with-rejection]
sources:
  - paper: doi:10.1287/mnsc.16.1.77
    title: Eugene L. Lawler and J. Michael Moore, A functional equation and its application to resource allocation and sequencing problems, Management Science 16(1), 1969
    locator: pages 77 to 84 (the recursion for 1||sum wjUj)
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: Richard M. Karp, Reducibility among combinatorial problems, in Complexity of Computer Computations, 1972
    locator: pages 85 to 103 (JOB SEQUENCING, reduced from KNAPSACK)
  - paper: "Sartaj K. Sahni, Algorithms for scheduling independent tasks, Journal of the ACM 23(1), 1976"
    locator: pages 116 to 127 (approximation schemes for the weight of on-time jobs)
  - paper: "G. V. Gens and E. V. Levner, Fast approximation algorithm for job sequencing with deadlines, Discrete Applied Mathematics 3(4), 1981"
    locator: pages 313 to 318 (an FPTAS for the weight of late jobs)
  - paper: "Jan Karel Lenstra, Alexander H. G. Rinnooy Kan and Peter Brucker, Complexity of machine scheduling problems, Annals of Discrete Mathematics 1, 1977"
    locator: pages 343 to 362 (release dates make the problem strongly NP-hard)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability
    locator: Appendix A5.1, problem SS3 (sequencing to minimize tardy task weight)
  - book: isbn:9783319265780
    title: Michael L. Pinedo, Scheduling, Theory, Algorithms, and Systems, fifth edition
    locator: Chapter 3, Single Machine Models (Deterministic), the weighted number of tardy jobs
  - book: isbn:9783540695158
    title: Peter Brucker, Scheduling Algorithms, fifth edition
    locator: Chapter 4, Single Machine Scheduling Problems (the weighted number of late jobs, dynamic programming)
---

In $1 \| \sum_j w_j U_j$, each job has a processing time, a due date and a weight, and the goal is to order the jobs on one machine so that the total weight of the [late jobs](/lateness-and-tardiness/) is as small as possible. Without weights, [Moore-Hodgson](/minimizing-tardy-jobs/) solves it in $O(n \log n)$ time. With weights it is NP-hard, because it contains the [knapsack problem](/knapsack-problem/). It is NP-hard only in the weak sense: the Lawler-Moore dynamic program runs in $O(n \sum_j p_j)$ time, a similar program runs in $O(n \sum_j w_j)$ time, and rounding the weights of the second program gives an [FPTAS](/fptas/). An approximation for the weight of the on-time jobs does not give one for the weight of the late jobs. This page shows why.

## In plain words

Each order has a length, a due date and a value. If an order is late, you lose its value. You want to lose as little as possible.

Late orders can go to the end, so you choose a set of orders to finish on time. Those orders, done in due date order, must all meet their dates. This is like packing a knapsack, where the due dates set the sizes of the knapsack along the way. When the lengths are small numbers, you can try all possible amounts of busy time. When they are large, you round the values and try all rounded losses instead. That gives a loss at most a factor $1 + \varepsilon$ above the best.

## Definition

**Input.** Jobs $1, \ldots, n$ with processing times $p_j \ge 0$, due dates $d_j$ and weights $w_j \ge 0$, all integers, one machine, and all jobs available at time 0.

**Output.** An order of the jobs run back to back from time 0, with completion times $C_j$ and $U_j = 1$ when $C_j > d_j$.

**Goal.** Minimize $\sum_j w_j U_j$.

As in the unweighted problem, a set of jobs is *feasible* when it is on time in EDD order, and an optimal schedule runs a feasible set $S$ in EDD order and then the rest. The value is $w(J - S)$. So the problem is: find a feasible set of the largest weight, and the answer is the weight of its complement.

## Variants

- **Unweighted, $1 \| \sum U_j$.** Moore-Hodgson, $O(n \log n)$. See [minimizing tardy jobs](/minimizing-tardy-jobs/).
- **Common due date, $1 \mid d_j = d \mid \sum w_j U_j$.** Exactly the 0-1 knapsack problem with capacity $d$, sizes $p_j$ and values $w_j$.
- **Unit processing times, $1 \mid p_j = 1 \mid \sum w_j U_j$.** A greedy method by weight is optimal; see [job sequencing with deadlines](/job-sequencing-with-deadlines/).
- **Tardy processing time, $w_j = p_j$.** Minimize the total processing time of the late jobs. It is still NP-hard: with a common due date $d$ it asks for a subset of the $p_j$ with the largest sum at most $d$, which is [subset sum](/subset-sum-problem/).
- **Release dates.** $1 \mid r_j \mid \sum w_j U_j$ is strongly NP-hard, even without weights.
- **Maximization form.** Maximize the weight of the on-time jobs. The exact problem is the same, but the approximation results differ. Sahni (1976) gives an FPTAS for this form.

## Examples

**Six jobs.**

| job | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| $p_j$ | 3 | 2 | 4 | 1 | 3 | 2 |
| $d_j$ | 4 | 5 | 6 | 8 | 9 | 10 |
| $w_j$ | 5 | 4 | 7 | 2 | 6 | 3 |

The total weight is 27. The on-time set $\{0, 1, 4, 5\}$ completes at $3, 5, 8, 10$ in EDD order, all on time, so jobs 2 and 3 are late with weight $9$. The on-time set $\{2, 3, 4, 5\}$ completes at $4, 5, 8, 10$, also on time, and also gives weight $9$ for the late jobs 0 and 1. A search over all $2^6$ subsets and all $720$ orders confirms that 9 is optimal. Moore-Hodgson, which ignores the weights, makes jobs 2 and 0 late, with weight 12.

**The bounds of the FPTAS on this instance.** The jobs with $w_j \ge 6$ are $\{2, 4\}$, which are feasible. The jobs with $w_j \ge 5$ are $\{0, 2, 4\}$, which are not: in EDD order they complete at $3$, $7 > 6$ and $10 > 9$. So $t^* = 5$, and the bounds below give $5 \le \mathrm{OPT} \le 6 \cdot 5 = 30$. For $\varepsilon = 1/2$ the scale is $K = \varepsilon t^*/n = 5/12$, the rounded weights are $\lfloor 12 w_j / 5 \rfloor = (12, 9, 16, 4, 14, 7)$, and the table has $\lfloor n^2/\varepsilon \rfloor + 1 = 73$ columns. The scheme returns the late set $\{2, 3\}$ with weight 9.

**Approximating the on-time weight is not enough.** Take $p = (10, 1, 10)$, a common due date $11$ and $w = (900, 99, 1)$. The best on-time set is $\{0, 1\}$ with weight 999, so $\mathrm{OPT} = 1$. The set $\{0\}$ has on-time weight $900 \ge 0.9 \cdot 999$, so a $0.9$-approximation for the maximization form may return it. Its late weight is $100 = 100 \cdot \mathrm{OPT}$.

## Known algorithms

**Lawler and Moore (1969), $O(n \sum_j p_j)$.** Index the jobs in EDD order. Let $F_k(t)$ be the least weight of late jobs among $1, \ldots, k$ when the on-time jobs among them take exactly $t$ time units, with $F_0(0) = 0$ and $F_0(t) = \infty$ for $t > 0$. Then

$$F_k(t) = \min\big(F_{k-1}(t) + w_k,\; F_{k-1}(t - p_k) \text{ if } p_k \le t \le d_k\big),$$

and the optimum is $\min_t F_n(t)$. The second term puts job $k$ on time as the last on-time job so far, which ends at $t$. The table has $n \cdot (P + 1)$ entries with $P = \sum_j p_j$, each computed in $O(1)$ time.

**A dynamic program over the late weight, $O(n \sum_j w_j)$.** Let $g_k(W)$ be the least total processing time of an on-time set among $1, \ldots, k$ whose late jobs among $1, \ldots, k$ have weight exactly $W$. Then

$$g_k(W) = \min\big(g_{k-1}(W) + p_k \text{ if } g_{k-1}(W) + p_k \le d_k,\; g_{k-1}(W - w_k)\big).$$

Keeping only the least processing time for each $W$ is safe: the later jobs only need the total time of the on-time set, and a smaller total never hurts them. The optimum is the least $W$ with $g_n(W) < \infty$.

**An FPTAS by rounding the weights.** This is the scheme of [rounding and scaling](/rounding-and-scaling/) applied to the second program, in the style of Gens and Levner (1981), whose algorithm is faster.

```pseudo id=main
LATE-WEIGHT-FPTAS(p[1 .. n], d[1 .. n], w[1 .. n], ε)
L1  if all jobs are on time in EDD order then return no late jobs
L2  t* ← the largest weight x such that the jobs with w_j ≥ x are not feasible
L3  K ← ε t* / n, and w'_j ← ⌊w_j / K⌋ for each j
L4  B ← ⌊n t* / K⌋, which is ⌊n² / ε⌋
L5  for k in EDD order: fill g_k(W) for W = 0 .. B with the recursion above and the weights w'
L6  W* ← the least W ≤ B with g_n(W) < ∞
L7  return the late set of W*, found by walking back through the tables
```

*The bounds on OPT.* Let $H(x) = \{j : w_j \ge x\}$. Line L1 returns when $\mathrm{OPT} = 0$, so the full set $H(\min_j w_j)$ is not feasible, and $t^*$ exists. Every schedule has a late job in $H(t^*)$, since $H(t^*)$ is not feasible, so $\mathrm{OPT} \ge t^*$. Let $x^+$ be the next weight above $t^*$, if there is one. Then $H(x^+)$ is feasible, and the schedule that keeps it on time makes late only jobs of weight at most $t^*$, so $\mathrm{OPT} \le n t^*$. When $t^*$ is the largest weight, every job has weight at most $t^*$ and the same bound holds.

*The optimal late set fits in the table.* Let $S^*$ be the late set of an optimal schedule. Its rounded weight is $\sum_{j \in S^*} \lfloor w_j/K \rfloor \le \mathrm{OPT}/K \le n t^*/K$, and it is an integer, so it is at most $B$. So the table of line L5 contains a state for $S^*$, and $W^* \le w'(S^*)$.

*The ratio.* Let $S$ be the late set returned. Since $w_j < K(w'_j + 1)$,
$$w(S) \le K\, w'(S) + K |S| \le K\, w'(S^*) + K n \le w(S^*) + \varepsilon t^* \le (1 + \varepsilon)\,\mathrm{OPT}.$$

*The time.* Line L2 takes $O(n \log n)$ for each feasibility test, and a binary search over the sorted weights needs $O(\log n)$ tests, because feasibility of $H(x)$ only improves as $x$ grows. Line L5 has $n$ rounds of $B + 1 = O(n^2/\varepsilon)$ entries each. The total is $O(n^3/\varepsilon)$ time, which is polynomial in $n$ and $1/\varepsilon$.

The tests of this page check the Lawler-Moore program against a search over all subsets, and the scheme for $\varepsilon = 1, 1/2, 1/4, 1/10$ against the bound $(1 + \varepsilon)\,\mathrm{OPT}$.

## Bounds

- **Pseudo-polynomial upper bounds.** $O(n \min(\sum_j p_j, \max_j d_j))$, since the times above $\max_j d_j$ never hold an on-time set, and $O(n \sum_j w_j)$.
- **NP-hard in the weak sense.** NP-hard by the knapsack reduction, and not strongly NP-hard unless P = NP, by the pseudo-polynomial algorithms. See [weak NP-hardness](/weak-np-hardness/).
- **Approximation.** An FPTAS exists for the late weight and for the on-time weight. Release dates make even the unweighted problem strongly NP-hard, with no finite ratio for the late count, as shown on the [unweighted page](/minimizing-tardy-jobs/).

## Reductions

- **From knapsack.** Given items with sizes $s_i$, values $v_i$ and capacity $c$, make jobs with $p_i = s_i$, $w_i = v_i$ and $d_i = c$. The on-time sets are exactly the item sets that fit. Karp (1972) lists the problem as JOB SEQUENCING and reduces from knapsack. See [Karp's 21 problems](/karps-21-np-complete-problems/).
- **To knapsack, in a sense.** With a common due date the two problems are the same, so the [knapsack FPTAS](/knapsack-fptas/) gives the on-time form. With different due dates the constraint is a nested family of knapsack constraints, one for each prefix of the EDD order.
- **To scheduling with rejection.** A late job is like a rejected job with penalty $w_j$. See [scheduling with rejection](/scheduling-with-rejection/).

## Applications

- **Order acceptance with values.** A firm with more orders than capacity chooses which orders to deliver on time, to keep the most revenue.
- **Batch planning.** Jobs that miss a shipment date lose their value for that shipment.
- **Teaching.** It shows the difference between approximating a value and its complement, which also matters for vertex cover and independent set.

## References
