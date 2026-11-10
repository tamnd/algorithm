---
tag: 6ZNFNM
kind: algorithm
slug: shmoys-tardos-gap
name: Shmoys-Tardos rounding for GAP
aliases:
- Shmoys-Tardos generalized assignment rounding
- slot rounding for GAP
area: approximation/lp-rounding
level: advanced
summary: Cut each machine's LP share into unit slots by decreasing job time and take a min-cost matching of jobs to slots; the cost is at most the LP and each load at most T plus one job.
solves: [generalized-assignment-problem]
model: real-ram
complexity:
  vars: {n: the number of jobs, m: the number of machines, L: the time to solve the LP with m n variables}
  time: {worst: O(L + n^2 (n + m) m)}
  space: {extra: O(n m)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1993
  people: [David B. Shmoys, Éva Tardos]
  note: Shmoys and Tardos showed that if some assignment has cost C and makespan T, then one with cost at most C and makespan at most 2T can be found in polynomial time; this extended the 2-approximation of Lenstra, Shmoys and Tardos (1990) for unrelated machines to costs.
prereqs: [generalized-assignment-problem, lp-relaxation, bipartite-matching, matching-polytope, min-cost-flow-problem]
see_also: [lenstra-shmoys-tardos, unrelated-machine-scheduling-makespan, bicriteria-approximation, iterative-rounding, successive-shortest-path, unrelated-machine-scheduling, dependent-rounding]
sources:
  - paper: doi:10.1007/BF01585178
    title: David B. Shmoys and Éva Tardos, An approximation algorithm for the generalized assignment problem, Mathematical Programming 62(3), 1993
    locator: pages 461 to 474 (the slot construction and Theorem 2.1)
  - paper: doi:10.1007/BF01585745
    title: Jan Karel Lenstra, David B. Shmoys and Éva Tardos, Approximation algorithms for scheduling unrelated parallel machines, Mathematical Programming 46, 1990
    locator: pages 259 to 271 (the 2-approximation and the 3/2 hardness)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 11.1 (the generalized assignment problem, with a proof by iterative rounding)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 17 (scheduling on unrelated parallel machines)
---

The Shmoys-Tardos algorithm rounds the LP relaxation of the [generalized assignment problem](/generalized-assignment-problem/): assign each job to a machine, where job $j$ takes time $p_{ij}$ and costs $c_{ij}$ on machine $i$, so that each machine finishes by a target time $T$ and the total cost is small. It solves the LP, cuts the fractional share of each machine into unit *slots* with the long jobs first, and finds a minimum cost matching of the jobs to the slots. The assignment costs at most the LP value, so at most the cost $C$ of the best schedule with makespan $T$, and each machine has load at most $T + \max_j p_{ij} \le 2T$. This is a [bicriteria](/bicriteria-approximation/) $(1, 2)$ guarantee, and it also gives the 2-approximation of [Lenstra, Shmoys and Tardos](/lenstra-shmoys-tardos/) for makespan alone.

## In plain words

Jobs must go to machines. Each machine takes its own time for each job, and each choice has a price. First solve an easier problem in which a job can be split across machines. Then, on each machine, line up the pieces it got, longest jobs first, and cut the line into seats that each hold one job's worth of pieces.

Now give each job one whole seat, at the least total price. Such a seating exists and costs no more than the split answer, because the split answer already fills the seats. A machine gets at most one job for each seat. The jobs in a seat are no longer than the jobs in the seat before it. So a machine runs at most one extra job beyond its time limit.

## The problem

The input is $m$ machines, $n$ jobs, times $p_{ij} \ge 0$, costs $c_{ij} \ge 0$ and a target $T > 0$. An assignment $\sigma$ maps each job to a machine; its cost is $\sum_j c_{\sigma(j) j}$, and the load of machine $i$ is $\sum_{j : \sigma(j) = i} p_{ij}$. Let $C$ be the least cost of an assignment with all loads at most $T$. The LP is

$$\min \sum_{i, j} c_{ij} x_{ij} \ \text{ s.t. } \sum_i x_{ij} = 1 \ (\text{each } j), \quad \sum_j p_{ij} x_{ij} \le T \ (\text{each } i), \quad x \ge 0, \quad x_{ij} = 0 \text{ if } p_{ij} > T.$$

The last condition is valid for each assignment with loads at most $T$, and it is what makes the bound $T + p_{ij} \le 2T$ possible. Each such assignment is feasible for the LP, so the LP value is at most $C$. The algorithm gets $T$ as input; a search over $T$ is on the [unrelated machines](/unrelated-machine-scheduling-makespan/) page.

## The algorithm

```pseudo id=main
SHMOYS-TARDOS-GAP(p, c, T)
L1  solve the LP with target T for an optimal x
L2  if the LP is infeasible then return "no assignment with loads at most T"
L3  for each machine i do
L4      k_i ← ⌈Σ_j x_ij⌉;  make slots (i, 1), ..., (i, k_i), each of capacity 1
L5      for each job j with x_ij > 0, in order of nonincreasing p_ij, do
L6          pour x_ij into the slots of i in order, filling each slot to 1 before the next; join j to each slot that gets a part of x_ij, with cost c_ij
L7  find a minimum cost matching of the jobs to the slots that covers all jobs
L8  σ(j) ← the machine of the slot of job j
L9  return σ
```

Line L6 splits the share of job $j$ over at most two consecutive slots when it crosses a slot boundary. The amounts that line L6 pours form a fractional matching: each job sends total 1, and each slot receives at most 1. All slots of machine $i$ except the last receive exactly 1. Line L7 runs [successive shortest paths](/successive-shortest-path/) on the bipartite graph of jobs and slots, with [Bellman-Ford](/bellman-ford/) because the residual costs can be negative. Any LP solution works in line L1; an optimal one gives the cost bound against $C$.

## Example

There are two machines and four jobs, and the target is $T = 4$.

| | $j_1$ | $j_2$ | $j_3$ | $j_4$ |
|---|---|---|---|---|
| $p_{1j}$ | 2 | 1 | 2 | 4 |
| $p_{2j}$ | 3 | 2 | 4 | 2 |
| $c_{1j}$ | 0 | 1 | 4 | 4 |
| $c_{2j}$ | 3 | 1 | 1 | 0 |

The LP optimum is $7/2$, at $x_{1,1} = x_{1,2} = 1$, $x_{1,3} = x_{2,3} = 1/2$ and $x_{2,4} = 1$. Both machines have fractional load exactly 4. The best assignment with loads at most 4 costs $C = 5$, so the LP is below $C$ here.

Machine 1 has $\sum_j x_{1j} = 5/2$, so it gets $k_1 = 3$ slots, and its jobs in order of time are $j_1, j_3, j_2$. Machine 2 has $\sum_j x_{2j} = 3/2$ and $k_2 = 2$, with the order $j_3, j_4$.

| slot | parts poured in | jobs joined | largest time | smallest time |
|---|---|---|---|---|
| $(1, 1)$ | $j_1$: 1 | $j_1$ | 2 | 2 |
| $(1, 2)$ | $j_3$: 1/2, $j_2$: 1/2 | $j_3, j_2$ | 2 | 1 |
| $(1, 3)$ | $j_2$: 1/2 | $j_2$ | 1 | 1 |
| $(2, 1)$ | $j_3$: 1/2, $j_4$: 1/2 | $j_3, j_4$ | 4 | 2 |
| $(2, 2)$ | $j_4$: 1/2 | $j_4$ | 2 | 2 |

A minimum cost matching is $j_1 \to (1, 1)$, $j_2 \to (1, 3)$, $j_3 \to (2, 1)$ and $j_4 \to (2, 2)$, of cost $0 + 1 + 1 + 0 = 2$. So $\sigma = (1, 1, 2, 2)$, with cost $2 \le 7/2$. The loads are $2 + 1 = 3$ and $4 + 2 = 6$. The load 6 is above $T = 4$ but within the bound $T + \max_j p_{2j} = 4 + 4 = 8 = 2T$. The cost 2 is the least cost of any assignment with loads at most 8, so the algorithm traded makespan for cost exactly as the theorem allows.

## Correctness

**Theorem (Shmoys and Tardos 1993).** If the LP with target $T$ is feasible, SHMOYS-TARDOS-GAP returns an assignment of cost at most the LP value, so at most $C$, in which each machine $i$ has load at most $T + \max \{ p_{ij} : x_{ij} > 0 \} \le 2T$.

The proof has two parts. The poured amounts are a fractional matching of cost $\sum_{i, j} c_{ij} x_{ij}$ that covers each job. The [bipartite matching polytope](/matching-polytope/) is integral, so there is an integral matching that covers all jobs with no larger cost, and line L7 finds one. For the load, list the slots of machine $i$ as $1, \ldots, k_i$, and let $p^{\max}_s$ and $p^{\min}_s$ be the largest and smallest time of a job joined to slot $s$. The jobs were poured in order of nonincreasing time, so $p^{\max}_{s+1} \le p^{\min}_s$. The matched job of slot $s$ has time at most $p^{\max}_s$, and the slots $1, \ldots, k_i - 1$ are full, so

$$\text{load}_i \le p^{\max}_1 + \sum_{s=1}^{k_i - 1} p^{\min}_s \le p^{\max}_1 + \sum_{s=1}^{k_i - 1} \sum_j p_{ij} \, (\text{part of } x_{ij} \text{ in slot } s) \le p^{\max}_1 + \sum_j p_{ij} x_{ij} \le p^{\max}_1 + T.$$

Finally $p^{\max}_1 \le T$ because $x_{ij} = 0$ when $p_{ij} > T$. The full proof is in the proof file below.

**The lower bound used.** The LP value with target $T$, which is at most the cost $C$ of each assignment with loads at most $T$.

**Tight example for the load.** Take $k$ machines, one long job of time $k$ on each machine, and on each machine $k - 1$ unit jobs that can run only there. With $T = k$, the LP puts $1/k$ of the long job on each machine, and each load is $k - 1 + 1 = k$. Each integral assignment puts the long job on one machine, with load $2k - 1$. So no rounding of this LP can give load less than $(2 - 1/k) T$.

**Hardness.** Deciding whether some assignment has all loads at most $T$ is NP-hard, even with two identical machines, by [partition](/partition-problem/). So a bound on the cost alone, with loads at most $T$, is not possible in polynomial time unless P = NP; some violation of the loads is needed. For makespan alone, ratio less than $3/2$ is NP-hard on unrelated machines ([Lenstra, Shmoys and Tardos 1990](/unrelated-makespan-inapproximability/)).

## Complexity

- **Time.** One LP with at most $mn$ variables and $n + m$ rows, in time $L$, which is polynomial by the [ellipsoid method](/ellipsoid-method/) or [interior point methods](/interior-point-method/). There are at most $n + m$ slots, because $\sum_i k_i \le \sum_i (\sum_j x_{ij} + 1) = n + m$. Each job is joined to at most two slots of each machine, so the bipartite graph has $O(nm)$ edges. Successive shortest paths does $n$ augmentations, each a Bellman-Ford run of $O((n + m) \cdot nm)$ time. The total is $O(L + n^2 (n + m) m)$ in the worst case. A faster matching, such as the [Hungarian algorithm](/hungarian-algorithm/), lowers the second term.
- **Space.** The LP solution, the slots and the edges take $O(nm)$ extra space, besides the LP solver.

## Properties

- **Bicriteria.** The output is within factor 1 on cost and factor 2 on makespan of the best schedule with makespan $T$; see [bicriteria approximation](/bicriteria-approximation/).
- **Per-machine targets.** The same proof works with a different target $T_i$ on each machine, giving load at most $T_i + \max_j p_{ij}$, where the maximum is over the jobs with $p_{ij} \le T_i$.
- **Deterministic.** With a fixed LP solver and a fixed matching rule, the output depends only on the input.
- **Any LP solution.** The rounding never uses that $x$ is a vertex; it works for every feasible $x$.

## Variants and improvements

- **Makespan alone.** With all costs zero, the theorem gives the [Lenstra-Shmoys-Tardos](/lenstra-shmoys-tardos/) 2-approximation for $R \| C_{\max}$, after a binary search over $T$. LST use a vertex of the LP and its pseudo-forest support instead of slots; see [unrelated machine scheduling](/unrelated-machine-scheduling-makespan/).
- **Iterative rounding.** The same bound has a proof by [iterative rounding](/iterative-rounding/): at a vertex of the LP, some job is integral, or some machine has at most two fractional jobs, or some machine can drop its load constraint. This is the proof of Williamson and Shmoys (Section 11.1).
- **Maximum profit.** In the profit version, each job may stay unassigned, and the aim is the largest total profit within the capacities. The slot rounding gives a $1/2$-approximation (Chekuri and Khanna 2000), and LP-based methods give $1 - 1/e$ and slightly more (Fleischer, Goemans, Mirrokni and Sviridenko 2006; Feige and Vondrák 2006).
- **Restricted assignment.** When $p_{ij} \in \{p_j, \infty\}$, better makespan bounds are known for the estimate of the optimum, by the configuration LP; see [restricted assignment](/restricted-assignment-scheduling/).

## When to use it

Use the algorithm when jobs must be placed on machines with different speeds or abilities, costs matter, and a bounded overrun of the time limit is acceptable. It needs one LP and one bipartite matching, and both are standard. It is also a clean way to round any fractional assignment with no loss in cost. When the time limits are hard, run it with a target $T/2$, if that LP is feasible, to get loads at most $T$ at a cost of at most $C(T/2)$, the best cost with loads at most $T/2$.

## Pitfalls

- **Dropping the filter $p_{ij} > T$.** Without $x_{ij} = 0$ for $p_{ij} > T$, the LP can put a tiny part of a huge job on a machine, the matching can give that job to the machine, and the load bound fails.
- **Sorting the wrong way.** The jobs must be poured in order of nonincreasing time. In the other order, the bound $p^{\max}_{s+1} \le p^{\min}_s$ fails, and the load of a machine can exceed $2T$.
- **Rounding up $k_i$ wrongly.** With $k_i = \lfloor \sum_j x_{ij} \rfloor$, the last part of the share of machine $i$ has no slot, and the fractional matching does not cover the jobs.
- **A matching that is not of minimum cost.** Any perfect matching gives the load bound, but only a minimum cost one gives the cost bound.

## Implementations

## History

Lenstra, Shmoys and Tardos (1990) gave the first 2-approximation for makespan on unrelated parallel machines, by rounding a vertex of the LP, and showed that ratio below $3/2$ is NP-hard. Shmoys and Tardos (1993) added costs: with the slot construction and a bipartite matching, they rounded any LP solution with no loss in cost and load at most $2T$, which solved the generalized assignment problem in the bicriteria sense. Their paper also treats the version where a job's time depends on the machine through a speed. Iterative rounding proofs of the same bound appear in the books of Williamson and Shmoys (2011) and of Lau, Ravi and Singh (2011).

## References
