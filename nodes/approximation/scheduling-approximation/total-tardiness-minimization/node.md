---
tag: 0G2W28
kind: problem
slug: total-tardiness-minimization
name: Total tardiness minimization
aliases:
- 1||sum Tj
- weighted total tardiness
- 1||sum wjTj
- total tardiness problem
area: approximation/scheduling-approximation
level: advanced
summary: Order jobs on one machine to minimize total tardiness. NP-hard (Du and Leung 1990), pseudo-polynomial by Lawler's decomposition, with an FPTAS; the weighted form is strongly NP-hard.
prereqs: [lateness-and-tardiness, earliest-due-date-first, pseudo-polynomial-time, fptas]
see_also: [weighted-tardy-jobs, maximum-lateness-minimization, shortest-processing-time-first, rounding-and-scaling, weak-np-hardness, strong-np-hardness, exchange-argument, weighted-completion-time-scheduling]
sources:
  - paper: "Eugene L. Lawler, A pseudopolynomial algorithm for sequencing jobs to minimize total tardiness, Annals of Discrete Mathematics 1, 1977"
    locator: pages 331 to 342 (the decomposition theorem and the O(n^4 sum p) algorithm; strong NP-hardness of the weighted case)
  - paper: "Jianzhong Du and Joseph Y.-T. Leung, Minimizing total tardiness on one machine is NP-hard, Mathematics of Operations Research 15(3), 1990"
    locator: pages 483 to 495
  - paper: "Eugene L. Lawler, A fully polynomial approximation scheme for the total tardiness problem, Operations Research Letters 1(6), 1982"
    locator: pages 207 to 208
  - paper: "John Emmons, One-machine sequencing to minimize certain functions of job tardiness, Operations Research 17(4), 1969"
    locator: pages 701 to 715 (the dominance rules)
  - paper: "Jan Karel Lenstra, Alexander H. G. Rinnooy Kan and Peter Brucker, Complexity of machine scheduling problems, Annals of Discrete Mathematics 1, 1977"
    locator: pages 343 to 362 (1||sum wjTj is strongly NP-hard)
  - paper: "Maurice Cheung, Julián Mestre, David B. Shmoys and José Verschae, A primal-dual approximation algorithm for min-sum single-machine scheduling problems, SIAM Journal on Discrete Mathematics 31(2), 2017"
    locator: the whole paper (constant-factor approximation for 1||sum fj, which contains 1||sum wjTj)
  - book: isbn:9783319265780
    title: Michael L. Pinedo, Scheduling, Theory, Algorithms, and Systems, fifth edition
    locator: Chapter 3, Single Machine Models (Deterministic), the total tardiness, dynamic programming and the FPTAS
---

The total tardiness problem $1 \| \sum_j T_j$ asks for an order of $n$ jobs on one machine that minimizes the sum of the [tardiness](/lateness-and-tardiness/) values $T_j = \max(0, C_j - d_j)$. It looks like a mix of two easy problems, since [EDD](/earliest-due-date-first/) is optimal when all jobs can be late and [SPT](/shortest-processing-time-first/) is optimal when all due dates are 0. But it is NP-hard (Du and Leung 1990). It is NP-hard only in the weak sense: Lawler's decomposition algorithm (1977) runs in $O(n^4 \sum_j p_j)$ time, and scaling the processing times gives an FPTAS (Lawler 1982). The weighted form $1 \| \sum_j w_j T_j$ is strongly NP-hard.

## In plain words

Each job has a length and a due date. When a job ends after its date, you pay one unit for each unit of time it is late. You want to pay as little as possible in total.

Doing the jobs by due date is good when everything is late anyway, and doing short jobs first is good when the dates are all very early. In between, neither rule is right, and the problem is hard. Still, the longest job can only go in a few places. Trying each place splits the problem into two smaller ones, and a table over start times solves it when the numbers are small. When they are large, round them down to small numbers first. The result is then at most a factor $1 + \varepsilon$ above the best.

## Definition

**Input.** Jobs $1, \ldots, n$ with integer processing times $p_j \ge 0$, due dates $d_j$ and, for the weighted form, weights $w_j \ge 0$. One machine, and all jobs available at time 0.

**Output.** An order of the jobs, run back to back from time 0, with completion times $C_j$.

**Goal.**

$$\min \sum_{j=1}^n T_j, \qquad T_j = \max(0, C_j - d_j), \qquad \text{or } \min \sum_{j=1}^n w_j T_j \text{ for the weighted form}.$$

Idle time never helps, because $T_j$ is nondecreasing in $C_j$.

## Variants

- **All due dates equal to 0.** Then $T_j = C_j$, and SPT is optimal. With weights, [Smith's rule](/smith-rule/) is optimal.
- **Every job late in every order.** If every job is late in every schedule, $\sum_j T_j = \sum_j C_j - \sum_j d_j$, and SPT is optimal again. If no job needs to be late, EDD gives $\sum_j T_j = 0$.
- **Agreeable data.** If $p_i < p_j$ implies $d_i \le d_j$, the order that is both EDD and SPT is optimal. This follows from repeated use of the dominance rule below: each swap of an inverted pair lowers the number of inversions.
- **Weighted, $1 \| \sum w_j T_j$.** Strongly NP-hard (Lawler 1977; Lenstra, Rinnooy Kan and Brucker 1977). So it has no FPTAS unless P = NP.
- **Maximum tardiness, $1 \| T_{\max}$.** Easy: EDD. See [maximum lateness](/maximum-lateness-minimization/).
- **Release dates.** $1 \mid r_j \mid \sum T_j$ is strongly NP-hard, as it contains $1 \mid r_j \mid L_{\max}$ feasibility.

## Examples

Take five jobs in EDD order.

| job | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| $p_j$ | 7 | 8 | 3 | 1 | 6 |
| $d_j$ | 4 | 7 | 11 | 14 | 20 |

- EDD, the order $0, 1, 2, 3, 4$, completes at $7, 15, 18, 19, 25$, with tardiness $3, 8, 7, 5, 5$, so $\sum T_j = 28$.
- SPT, the order $3, 2, 4, 0, 1$, completes at $1, 4, 10, 17, 25$, with tardiness $0, 0, 0, 13, 18$, so $\sum T_j = 31$.
- The order $0, 2, 3, 1, 4$ completes at $7, 10, 11, 19, 25$, with tardiness $3, 0, 0, 12, 5$, so $\sum T_j = 20$. A search over all 120 orders confirms that 20 is optimal. Only one other order, $0, 3, 2, 1, 4$, reaches it.

**The decomposition on this example.** The longest job is job 1, with $p_1 = 8$, at position 1 of the EDD order. Job 0 comes before it in EDD order and is not longer, so it goes before job 1. The algorithm tries to put job 1 after the jobs of EDD positions up to $b$, for $b = 1, 2, 3, 4$, and solves the two sides.

| $b$ | before job 1 | $C_1$ | $T_1$ | best before | best after | total |
|---|---|---|---|---|---|---|
| 1 | $\{0\}$ | 15 | 8 | 3 | 15 | 26 |
| 2 | $\{0, 2\}$ | 18 | 11 | 3 | 10 | 24 |
| 3 | $\{0, 2, 3\}$ | 19 | 12 | 3 | 5 | 20 |
| 4 | $\{0, 2, 3, 4\}$ | 25 | 18 | 3 | 0 | 21 |

The best choice is $b = 3$, with total 20.

**The FPTAS on a scaled copy.** Multiply all numbers by 10: $p = (70, 80, 30, 10, 60)$ and $d = (40, 70, 110, 140, 200)$. EDD has $T_{\max} = 80$. For $\varepsilon = 1$, $K = 2 \varepsilon T_{\max} / (n(n+1)) = 160/30 = 16/3$, so the rounded times are $\lfloor 3 p_j / 16 \rfloor = (13, 15, 5, 1, 11)$ and the due dates become $3 d_j / 16$. The exact algorithm on the rounded instance returns $0, 2, 3, 1, 4$, which has total tardiness 200 for the original jobs, the optimum.

## Known algorithms

**Lawler's decomposition (1977).** Index the jobs in EDD order, with ties by index, and let $k$ be a longest job; this implementation takes the last one in EDD order among the longest.

**Decomposition theorem.** There is an optimal order and a position $b$ at or after the position of $k$ such that the jobs before $k$ are exactly the other jobs of EDD positions up to $b$, and the jobs after $k$ are those after $b$.

```pseudo id=main
LAWLER-TARDINESS(J, t)                     ▷ J in EDD order, start time t
L1  index the jobs in EDD order (once, at the top level)
L2  if J is empty then return 0
L3  k ← a longest job of J, at position a of J
L4  for b ← a to |J| − 1 do
L5      B ← the jobs of J at positions up to b, except k;  A ← the jobs after b;  C ← t + p(B) + p[k]
L6      value(b) ← LAWLER-TARDINESS(B, t) + max(0, C − d[k]) + LAWLER-TARDINESS(A, C)
L7  return the least value(b), with its order
```

With memoization on $(J, t)$ the sets $J$ that occur are of the form "the jobs of EDD positions $i$ to $j$ that are shorter than a given job", so there are $O(n^3)$ of them. Each is solved for at most $\sum_j p_j + 1$ start times, with $O(n)$ choices of $b$. The time is $O(n^4 \sum_j p_j)$, which is pseudo-polynomial.

**Proof of the decomposition theorem (a sketch).**

1. *Dominance (Emmons 1969), with a full proof.* If $p_j \le p_k$ and $d_j \le d_k$, some optimal order has $j$ before $k$. Take an optimal order with $k$ before $j$ and swap the two jobs. The jobs between them end no later, since $p_j \le p_k$, and so do $j$ and the jobs outside. Write $a = C_k < b = C_j$ for the old completion times. Then $j$ now ends by $a$ and $k$ ends at $b$. With $g(x) = \max(0, x)$, the change in cost is at most $g(a - d_j) + g(b - d_k) - g(a - d_k) - g(b - d_j)$. The pairs $(a - d_j, b - d_k)$ and $(a - d_k, b - d_j)$ have the same sum, and since $a < b$ and $d_j \le d_k$, both numbers of the first pair lie between $a - d_k$ and $b - d_j$. Since $g$ is convex, $g(x) + g(y) \le g(x') + g(y')$ whenever $x + y = x' + y'$ and $x, y$ lie between $x'$ and $y'$. So the change is at most 0.
2. *All jobs before $k$ in EDD order go before $k$.* Such a job $j$ has $d_j \le d_k$ and, as $k$ is a longest job, $p_j \le p_k$. Apply step 1.
3. *The jobs after $k$ in EDD order that go before $k$ form a prefix.* This step is only sketched here. Lawler fixes an optimal order, replaces $d_k$ by $\max(d_k, C_k)$, where $C_k$ is the completion time of $k$ in that order, and shows that this does not change the set of optimal orders that matter. With the new due date, any job after $k$ in EDD order and with an earlier due date than the new $d_k$ can be moved before $k$ by the same kind of exchange, and one with a later due date after it. Since the jobs are in EDD order, the jobs moved before $k$ are those of positions up to some $b$. See Lawler (1977) for the details.

The tests of this page compare the implementation with a search over all orders for $n \le 7$ on 400 random instances, with many equal processing times, so the tie rule is also tested.

**Lawler's FPTAS (1982).** Let $T_{\max}$ be the maximum tardiness of the EDD order. If $T_{\max} = 0$, EDD has $\sum_j T_j = 0$ and is optimal. Otherwise let

$$K = \frac{2 \varepsilon\, T_{\max}}{n(n+1)}, \qquad p'_j = \lfloor p_j / K \rfloor, \qquad d'_j = d_j / K,$$

solve the instance $(p', d')$ exactly with the decomposition algorithm, and use its order $\sigma'$ for the original jobs. If $K \le 1$, solve the original instance exactly instead.

*The bounds.* EDD minimizes $T_{\max}$, and $\sum_j T_j \ge \max_j T_j$ for every order, so $\mathrm{OPT} \ge T_{\max}$. EDD itself has $\sum_j T_j \le n T_{\max}$, so $\mathrm{OPT} \le n T_{\max}$.

*The ratio, with a full proof.* For an order $\sigma$, let $C'_j(\sigma)$ and $T'_j(\sigma)$ be the values in the rounded instance. Since $K p'_j \le p_j < K(p'_j + 1)$, the job in position $i$ of $\sigma$ has $K C'_j(\sigma) \le C_j(\sigma) < K C'_j(\sigma) + K i$. So
$$T_j(\sigma) \le \max(0, K C'_j(\sigma) - d_j) + K i = K T'_j(\sigma) + K i, \qquad K T'_j(\sigma) \le T_j(\sigma).$$
Let $\sigma^*$ be an optimal order for the original jobs. Then
$$\sum_j T_j(\sigma') \le K \sum_j T'_j(\sigma') + K \frac{n(n+1)}{2} \le K \sum_j T'_j(\sigma^*) + \varepsilon T_{\max} \le \mathrm{OPT} + \varepsilon\, \mathrm{OPT}.$$
The middle step uses that $\sigma'$ is optimal for the rounded instance.

*The time, only cited.* The decomposition algorithm on the rounded instance takes $O(n^4 \sum_j p'_j)$ time, and $\sum_j p'_j \le \sum_j p_j / K = n(n+1) \sum_j p_j / (2 \varepsilon T_{\max})$. This alone is not polynomial, because $\sum_j p_j$ can be much larger than $T_{\max}$: two jobs with $p = (10^9, 1)$ and $d = (10^9, 0)$ have $T_{\max} = 1$. Lawler (1982) proves a running time of $O(n^7/\varepsilon)$ for his scheme. This page does not reproduce that part of the analysis, so it states the polynomial time bound only by citation.

The tests check the scheme for $\varepsilon = 1, 1/2, 1/4, 1/10$ against the bound $(1 + \varepsilon)\,\mathrm{OPT}$, with processing times up to 400 so that the rounding is active.

**Other methods.** Branch and bound with the dominance rules of Emmons and the decomposition solves large instances in practice. For the weighted form, which has no FPTAS, Cheung, Mestre, Shmoys and Verschae (2017) give a constant-factor approximation for the more general problem $1 \| \sum_j f_j(C_j)$ with nondecreasing $f_j$.

## Bounds

- **Upper bound.** $O(n^4 \sum_j p_j)$ time (Lawler 1977), and an FPTAS (Lawler 1982).
- **Lower bound.** NP-hard (Du and Leung 1990), so no polynomial algorithm unless P = NP. Because of the pseudo-polynomial algorithm, it is not strongly NP-hard unless P = NP. See [weak NP-hardness](/weak-np-hardness/).
- **The weighted form.** Strongly NP-hard, so no pseudo-polynomial algorithm and no FPTAS unless P = NP. See [strong NP-hardness](/strong-np-hardness/).
- **Testing $\mathrm{OPT} = 0$.** Easy in both forms: run EDD. So, unlike $1 \mid r_j \mid L_{\max}$, the zero optimum does not block a finite approximation ratio.

## Reductions

- **From even-odd partition.** Du and Leung (1990) reduce a restricted form of [partition](/partition-problem/) to the decision version of $1 \| \sum T_j$. The reduction is long and is not given here.
- **From 3-partition, weighted form.** The strong NP-hardness of $1 \| \sum w_j T_j$ comes from a reduction from [3-partition](/three-partition/) (Lawler 1977; Lenstra, Rinnooy Kan and Brucker 1977).
- **Special cases.** With all $d_j = 0$ the problem is $1 \| \sum C_j$, and with all $d_j$ very large it is trivial. The sum of lateness $\sum_j L_j$ is $\sum_j C_j - \sum_j d_j$ and so is easy.

## Applications

- **Due date penalties.** Contracts that charge for each day of delay give a total tardiness cost.
- **Dispatching rules.** Rules such as apparent tardiness cost, which mix EDD and SPT, are heuristics for this problem in shop scheduling.
- **Benchmark.** The problem is a standard test case for exact methods, local search and approximation schemes.

## References
