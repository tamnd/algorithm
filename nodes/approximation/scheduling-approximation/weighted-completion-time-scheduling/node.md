---
tag: Y1GCMZ
kind: problem
slug: weighted-completion-time-scheduling
name: Minimizing the weighted sum of completion times
aliases:
- total completion time
- 1||sum wjCj
- sum of completion times
- min-sum scheduling
area: approximation/scheduling-approximation
level: core
summary: Minimize the weighted sum of job completion times. Easy on one machine by Smith's rule; release dates, precedence or machines make it NP-hard, with 2-approximations and PTASs.
prereqs: [scheduling-notation, smith-rule, srpt]
see_also: [shortest-processing-time-first, minimizing-weighted-completion-time, sidney-decomposition, srpt-optimality, scheduling-with-release-dates, flow-time-minimization, precedence-constrained-scheduling, unrelated-machine-scheduling]
sources:
  - paper: doi:10.1002/nav.3800030106
    title: Wayne E. Smith, Various optimizers for single-stage production, Naval Research Logistics Quarterly 3(1-2), 1956
    locator: pages 59 to 66 (the ratio rule for one machine)
  - paper: "Cynthia Phillips, Clifford Stein and Joel Wein, Minimizing average completion time in the presence of release dates, Mathematical Programming 82, 1998"
    locator: pages 199 to 223 (the conversion of a preemptive schedule, factor 2)
  - paper: "Jan Karel Lenstra, Alexander H. G. Rinnooy Kan and Peter Brucker, Complexity of machine scheduling problems, Annals of Discrete Mathematics 1, 1977"
    locator: pages 343 to 362 (strong NP-hardness of 1|r_j|sum C_j)
  - paper: "Tsuyoshi Kawaguchi and Seiki Kyan, Worst case bound of an LRF schedule for the mean weighted flow-time problem, SIAM Journal on Computing 15(4), 1986"
    locator: pages 1119 to 1129 (the bound (1 + sqrt 2)/2 for WSPT list scheduling)
  - paper: "Leslie A. Hall, Andreas S. Schulz, David B. Shmoys and Joel Wein, Scheduling to minimize average completion time: off-line and on-line approximation algorithms, Mathematics of Operations Research 22(3), 1997"
    locator: pages 513 to 544 (LP relaxations and constant factors, with precedence and release dates)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 4.1 (the SRPT conversion) and Section 4.2 (an LP for the weighted case with release dates)
  - book: isbn:9783319265780
    title: Michael L. Pinedo, Scheduling, Theory, Algorithms, and Systems, fifth edition
    locator: Chapter 3, Single Machine Models (Deterministic), the total weighted completion time
---

Minimizing the weighted sum of completion times asks for a schedule of $n$ jobs with weights $w_j$ that makes $\sum_j w_j C_j$ as small as possible, where $C_j$ is the time job $j$ completes. With all weights 1 the objective is the total completion time $\sum_j C_j$, which is $n$ times the average completion time. In the [three-field notation](/scheduling-notation/) the basic form is $1 \| \sum w_j C_j$, and [Smith's rule](/smith-rule/) solves it exactly by sorting. The problem becomes NP-hard when jobs have release dates, when jobs have precedence constraints, or when there are weights on two or more machines. This page collects these versions, gives the factor 2 conversion of Phillips, Stein and Wein for $1 \mid r_j \mid \sum C_j$ with a full proof, and lists the approximation ratios and hardness results.

## In plain words

Jobs wait in a queue, and each minute a job waits costs its weight. You want the total cost of the waiting to be small. On one machine with all jobs ready, run first the jobs that are short compared to their weight. Trouble starts when jobs arrive over time. A job that comes later may be so short that you should have kept the machine idle for it. One way out is to solve the easier problem where jobs may be interrupted, and then run the jobs whole, in the order they finished there. That costs at most twice the best.

## Definition

**Input.** Jobs $1, \ldots, n$ with processing times $p_j \ge 0$ and weights $w_j \ge 0$. Some versions also have release dates $r_j \ge 0$, a precedence order on the jobs, or $m$ machines.

**Output.** A schedule: each job runs for $p_j$ time units on one machine, not before $r_j$, after all its predecessors are complete, and no machine runs two jobs at once. Without preemption, each job runs in one piece.

**Goal.** Minimize $\sum_j w_j C_j$.

The objective is regular: it does not decrease when a completion time increases. So without release dates no optimal schedule has idle time. The objective $\sum_j w_j (C_j - r_j)$, the weighted [flow time](/flow-time/), differs from $\sum_j w_j C_j$ by the constant $\sum_j w_j r_j$. So the two have the same optimal schedules, but not the same approximation ratios. See [flow time minimization](/flow-time-minimization/).

## Variants

| problem | status |
|---|---|
| $1 \| \sum C_j$ | $O(n \log n)$, [SPT](/shortest-processing-time-first/) |
| $1 \| \sum w_j C_j$ | $O(n \log n)$, [Smith's rule](/smith-rule/) (1956) |
| $1 \mid r_j, pmtn \mid \sum C_j$ | $O(n \log n)$, [SRPT](/srpt/) (Schrage 1968) |
| $1 \mid r_j, pmtn \mid \sum w_j C_j$ | strongly NP-hard (Labetoulle, Lawler, Lenstra and Rinnooy Kan 1984) |
| $1 \mid r_j \mid \sum C_j$ | strongly NP-hard (Lenstra, Rinnooy Kan and Brucker 1977); factor 2 below, PTAS |
| $1 \mid prec \mid \sum w_j C_j$ | strongly NP-hard; factor 2, see [Sidney decomposition](/sidney-decomposition/) |
| $1 \mid prec \mid \sum w_j C_j$, series-parallel order | $O(n \log n)$ (Lawler 1978) |
| $P \| \sum C_j$ | $O(n \log n)$, SPT dealt to the machines in turn |
| $P2 \| \sum w_j C_j$ | NP-hard; $P \| \sum w_j C_j$ is strongly NP-hard; PTAS |
| $R \| \sum C_j$ | polynomial, by bipartite matching (Horn 1973; Bruno, Coffman and Sethi 1974) |
| $R \| \sum w_j C_j$ | APX-hard; factor $3/2$, then $3/2 - \varepsilon$ |

## Examples

**One machine, no release dates.** Jobs with $(p, w) = (3, 1), (1, 2), (2, 2)$ have ratios $p_j / w_j = 3, 1/2, 1$. Smith's rule runs them in the order $2, 3, 1$ (using 1-based names) with completion times $1, 3, 6$ and cost $2 \cdot 1 + 2 \cdot 3 + 1 \cdot 6 = 14$. The [Smith's rule page](/smith-rule/) has the exchange proof.

**Release dates.** Take five jobs, numbered from 0, with unit weights:

| job | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| $p_j$ | 5 | 1 | 2 | 4 | 1 |
| $r_j$ | 0 | 1 | 2 | 3 | 8 |

- *First come, first served.* The order $0, 1, 2, 3, 4$ gives completion times $5, 6, 8, 12, 13$, total 44.
- *SRPT, with preemption.* Job 0 starts at 0. Job 1 arrives at 1 and is shorter than the 4 units left of job 0, so it runs from 1 to 2. Job 2 runs from 2 to 4. At time 4, job 0 and job 3 both have 4 units left, and the tie goes to job 0, which runs from 4 to 8. Job 4 runs from 8 to 9 and job 3 from 9 to 13. The completion times are $C^P = (8, 2, 4, 13, 9)$, total 36. This is the optimum with preemption, and so a lower bound for the problem without it.
- *The conversion.* Order the jobs by $C^P_j$: $1, 2, 0, 4, 3$. Run them whole in this order, each as early as possible: job 1 in $[1, 2]$, job 2 in $[2, 4]$, job 0 in $[4, 9]$, job 4 in $[9, 10]$, job 3 in $[10, 14]$. The total is $2 + 4 + 9 + 10 + 14 = 39$. Each job completes at most twice as late as in $C^P$.
- *The optimum.* A search over all 120 orders gives 37, for the order $1, 2, 3, 4, 0$, with completion times $2, 4, 8, 9, 14$. The long job 0 goes last, though it is the only job ready at time 0. The conversion is within $39 / 37 \approx 1.05$ of it here.

**Two machines.** For $P2 \| \sum C_j$ with $p = (3, 3, 2, 2, 2, 6)$, SPT deals the jobs in the order $2, 3, 4, 0, 1, 5$ to the machine that is free first. Machine 1 runs jobs $2, 4, 1$ and completes them at $2, 4, 7$. Machine 2 runs jobs $3, 0, 5$ and completes them at $2, 5, 11$. The total 31 is optimal.

## Known algorithms

**The SRPT conversion for $1 \mid r_j \mid \sum C_j$** (Phillips, Stein and Wein 1998). Solve the preemptive problem exactly, then run the jobs whole in the order of their preemptive completion times.

```pseudo id=main
SRPT-CONVERSION(p[1 .. n], r[1 .. n])
L1  C^P ← completion times of the preemptive SRPT schedule
L2  sort the jobs so that C^P[j1] ≤ C^P[j2] ≤ ... ≤ C^P[jn]
L3  t ← 0
L4  for k ← 1 to n do
L5      start jk at max(t, r[jk]), t ← max(t, r[jk]) + p[jk], C[jk] ← t
L6  return the order j1, ..., jn and the times C
```

SRPT runs, at each moment, the released job with the least remaining work. It changes jobs only at release dates and completions, so it has at most $2n$ pieces and a heap makes it run in $O(n \log n)$ time. The sort and the final pass take $O(n \log n)$ and $O(n)$. So the whole algorithm takes $O(n \log n)$ time and $O(n)$ space.

**Theorem.** The schedule of SRPT-CONVERSION is feasible and has $C_j \le 2 C^P_j$ for each job $j$. So its total is at most $2 \sum_j C^P_j \le 2\,\mathrm{OPT}$.

*Proof.* Each job starts at or after its release date, by line L5, and the jobs run one after another, so the schedule is feasible. Fix $k$. Line L5 makes $C_{j_k} = \max_{1 \le i \le k} \bigl( r_{j_i} + p_{j_i} + p_{j_{i+1}} + \cdots + p_{j_k} \bigr)$, because the last idle time before $j_k$ ends at the release date of some $j_i$, and from then on the machine is busy. Each term is at most $\max_{i \le k} r_{j_i} + \sum_{i \le k} p_{j_i}$. Now look at the preemptive schedule. The jobs $j_1, \ldots, j_k$ all complete by $C^P_{j_k}$, by the sort in line L2, so all their work is done by then: $\sum_{i \le k} p_{j_i} \le C^P_{j_k}$. Also each $j_i$ with $i \le k$ is released before it completes, so $r_{j_i} \le C^P_{j_i} \le C^P_{j_k}$. Together, $C_{j_k} \le 2 C^P_{j_k}$. Summing over $k$ gives $\sum_j C_j \le 2 \sum_j C^P_j$. SRPT is optimal for $1 \mid r_j, pmtn \mid \sum C_j$ ([proof](/srpt-optimality/)), and every non-preemptive schedule is also a preemptive one, so $\sum_j C^P_j \le \mathrm{OPT}$. ∎

The same proof works for any preemptive schedule in place of SRPT. With weights, it turns an $\alpha$-approximate preemptive schedule into a $2\alpha$-approximate non-preemptive one, but $1 \mid r_j, pmtn \mid \sum w_j C_j$ is itself NP-hard.

The tests of this page check $C_j \le 2 C^P_j$ for each job, and compare the total with the optimum found by a search over all orders, on seeded random instances with up to 7 jobs. They also check SRPT against a dynamic program over unit time slots.

**Other algorithms.**

- **Smith's rule and SPT.** For $1 \| \sum w_j C_j$ sort by $p_j / w_j$; see [Smith's rule](/smith-rule/) and [minimizing weighted completion time](/minimizing-weighted-completion-time/). For $P \| \sum C_j$, SPT dealt to the machines is optimal; see [SPT](/shortest-processing-time-first/).
- **WSPT list scheduling.** For $P \| \sum w_j C_j$, take the jobs in Smith order and put each on the machine that is free first. Kawaguchi and Kyan (1986) prove the ratio $(1 + \sqrt 2)/2 \approx 1.207$, and show that it is tight. The page's implementation includes this rule and its tests check the bound against a search over all assignments for $m = 2, 3$.
- **Randomized $\alpha$-points.** For $1 \mid r_j \mid \sum C_j$, run the jobs in the order in which they reach a random fraction $\alpha$ of their work in the preemptive schedule. Chekuri, Motwani, Natarajan and Stein (2001) choose $\alpha$ from a suitable distribution and get the expected ratio $e/(e-1) \approx 1.58$.
- **LP relaxations.** Linear programs in the completion time variables, with the constraints $\sum_{j \in S} p_j C_j \ge \frac12 \bigl( p(S)^2 + \sum_{j \in S} p_j^2 \bigr)$ for every set $S$, give constant factors with release dates and precedence constraints (Hall, Schulz, Shmoys and Wein 1997). Williamson and Shmoys, Section 4.2, give a 3-approximation for $1 \mid r_j \mid \sum w_j C_j$ this way. See [LP relaxation](/lp-relaxation/).
- **Precedence constraints.** For $1 \mid prec \mid \sum w_j C_j$, several different methods give the factor 2: LP rounding (Hall, Schulz, Shmoys and Wein 1997), Chudak and Hochbaum (1999), Chekuri and Motwani (1999), and Margot, Queyranne and Wang (2003). The last two use the [Sidney decomposition](/sidney-decomposition/).
- **Approximation schemes.** Afrati and others (1999) give a PTAS for $1 \mid r_j \mid \sum w_j C_j$ and for several machine models with release dates. Skutella and Woeginger (2000) give a PTAS for $P \| \sum w_j C_j$. See [PTAS](/ptas/).
- **Unrelated machines.** $R \| \sum C_j$ is a bipartite matching problem: a job that is $k$-th from last on machine $i$ adds $k\,p_{ij}$ to the total, so assign jobs to (machine, position) pairs at minimum cost (Horn 1973; Bruno, Coffman and Sethi 1974). For $R \| \sum w_j C_j$, Skutella (2001) gives $3/2$ by a convex quadratic program, and Bansal, Srinivasan and Svensson (2016) give $3/2 - \varepsilon$ for a small constant $\varepsilon > 0$. See [unrelated machine scheduling](/unrelated-machine-scheduling/).

## Bounds

- **Exact cases.** $O(n \log n)$ time for $1 \| \sum w_j C_j$, $P \| \sum C_j$ and $1 \mid r_j, pmtn \mid \sum C_j$.
- **Approximation.** Factor 2 for $1 \mid r_j \mid \sum C_j$ by the conversion on this page, $e/(e-1)$ in expectation by $\alpha$-points, and a PTAS. Factor 2 for $1 \mid prec \mid \sum w_j C_j$.
- **Strong NP-hardness.** $1 \mid r_j \mid \sum C_j$ and $1 \mid prec \mid \sum C_j$ are strongly NP-hard, so they have no [FPTAS](/fptas/) unless P = NP; see [strong NP-hardness](/strong-np-hardness/).
- **Precedence constraints.** For $1 \mid prec \mid \sum w_j C_j$, Bansal and Khot (2009) show that no polynomial algorithm has ratio $2 - \varepsilon$, under a variant of the unique games conjecture. Ambühl, Mastrolilli and Svensson show that it has no PTAS under another complexity assumption.
- **Unrelated machines.** $R \| \sum w_j C_j$ is APX-hard, so it has no PTAS unless P = NP.

## Reductions

- **Weighted completion time and weighted flow time.** They differ by the constant $\sum_j w_j r_j$, so exact algorithms transfer, but ratios do not. See [flow time minimization](/flow-time-minimization/).
- **From 3-partition to $P \| \sum w_j C_j$.** With $w_j = p_j$, the cost depends only on the machine loads, and is smallest when all loads are equal; this makes the problem as hard as [3-partition](/three-partition/).
- **From $1 \mid prec \mid \sum w_j C_j$ to vertex cover.** Correa and Schulz (2005) and Ambühl and Mastrolilli (2009) show that the scheduling problem is a special case of vertex cover in a graph built from the precedence order. This links the factor 2 for the scheduling problem to the factor 2 for vertex cover.
- **$R \| \sum C_j$ to assignment.** As above, a minimum-cost bipartite matching between jobs and (machine, position) pairs.

## Applications

- **Average response time.** In a server or an operating system, $\sum_j C_j$ is $n$ times the mean time a job spends in the system when all jobs are present at time 0.
- **Work in progress.** In a factory, $\sum_j w_j C_j$ measures the inventory cost of unfinished orders, with $w_j$ the holding cost per unit of time.
- **A building block.** The completion time LP and the conversion of preemptive schedules appear in online scheduling and in many approximation algorithms for shop problems. See [online total completion time](/online-total-completion-time/).

## References
