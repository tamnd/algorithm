---
tag: FGZ81Z
kind: problem
slug: flow-time-minimization
name: Minimizing flow time
aliases:
- weighted flow time
- response time
- total flow time
- 1|r_j,pmtn|sum Fj
area: approximation/scheduling-approximation
level: advanced
summary: Minimize the total or weighted time that jobs spend between release and completion. SRPT is optimal with preemption; without it the ratio sqrt n is the best possible.
prereqs: [flow-time, scheduling-with-release-dates, srpt]
see_also: [srpt-optimality, weighted-completion-time-scheduling, online-flow-time-minimization, stretch, maximum-lateness-minimization, competitive-ratio, preemptive-scheduling, approximation-ratio]
sources:
  - paper: "Linus Schrage, A proof of the optimality of the shortest remaining processing time discipline, Operations Research 16(3), 1968"
    locator: pages 687 to 690 (SRPT is optimal for the total flow time with preemption)
  - paper: "Hans Kellerer, Thomas Tautenhahn and Gerhard J. Woeginger, Approximability and nonapproximability results for minimizing total flow time on a single machine, SIAM Journal on Computing 28(4), 1999"
    locator: pages 1155 to 1166 (an O(sqrt n) approximation without preemption, and no O(n^(1/2 - eps)) unless P = NP)
  - paper: "Stefano Leonardi and Danny Raz, Approximating total flow time on parallel machines, Journal of Computer and System Sciences 73(6), 2007"
    locator: pages 875 to 891 (SRPT on m machines, ratio O(log min(n/m, P)), and a matching lower bound for online algorithms)
  - paper: "Nikhil Bansal and Ho-Leung Chan, Weighted flow time does not admit O(1)-competitive algorithms, SODA 2009"
    locator: pages 1238 to 1244 (no constant competitive ratio online with weights)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 4.1 (SRPT and the conversion for the total completion time)
  - book: isbn:9783319265780
    title: Michael L. Pinedo, Scheduling, Theory, Algorithms, and Systems, fifth edition
    locator: Chapter 3, Single Machine Models (Deterministic), preemption and release dates
---

Minimizing flow time asks for a schedule of jobs that arrive over time, so that the jobs spend little time in the system. The [flow time](/flow-time/) of job $j$ is $F_j = C_j - r_j$, the time from its release date $r_j$ to its completion $C_j$. The usual objectives are the total flow time $\sum_j F_j$, the weighted flow time $\sum_j w_j F_j$, and the maximum flow time $F_{\max}$. The total flow time differs from the total completion time by the constant $\sum_j r_j$, so both have the same optimal schedules. Their approximation behavior is very different, because the optimal flow time can be much smaller than the optimal completion time. With preemption on one machine, [SRPT](/srpt/) is optimal for $\sum_j F_j$. Without preemption, Kellerer, Tautenhahn and Woeginger (1999) give an $O(\sqrt n)$-approximation and prove that no polynomial algorithm does better than $n^{1/2 - \varepsilon}$ unless P = NP.

## In plain words

Each job waits from the moment it arrives until it is done, and you want the total wait to be small. If you may pause a job, always work on the job that is closest to done. Then as few jobs as possible are waiting at each moment, and the total wait is the smallest possible. If you may not pause jobs, a long job can block many short ones, and no fast method gets close to the best in general. If you care only about the longest wait, serve the jobs in the order they arrive.

## Definition

**Input.** Jobs $1, \ldots, n$ with processing times $p_j \ge 0$, release dates $r_j \ge 0$, and in the weighted version weights $w_j \ge 0$. One machine, or $m$ identical machines.

**Output.** A schedule in which job $j$ runs for $p_j$ time units in total, not before $r_j$. With preemption the job may be cut into pieces. Without preemption it runs in one piece.

**Goal.** Minimize $\sum_j F_j$, or $\sum_j w_j F_j$, or $F_{\max} = \max_j F_j$, where $F_j = C_j - r_j$.

**Why the ratio changes.** For any schedule, $\sum_j C_j = \sum_j F_j + \sum_j r_j$. If the release dates are large and the jobs are short, $\sum_j r_j$ dominates both sides. A schedule with $\sum_j C_j$ at most $(1 + \delta)$ times the optimum can then have $\sum_j F_j$ many times the optimum. So a factor for completion time does not give a factor for flow time.

## Variants

| problem | status |
|---|---|
| $1 \mid r_j, pmtn \mid \sum F_j$ | $O(n \log n)$, SRPT (Schrage 1968) |
| $1 \mid r_j \mid \sum F_j$ | strongly NP-hard; $O(\sqrt n)$-approximation; no $O(n^{1/2 - \varepsilon})$ unless P = NP |
| $1 \mid r_j, pmtn \mid \sum w_j F_j$ | strongly NP-hard; constant factors, and a PTAS |
| $1 \mid r_j \mid F_{\max}$ | $O(n \log n)$, FIFO; preemption does not help |
| $P \mid r_j, pmtn \mid \sum F_j$ | NP-hard for $m \ge 2$; SRPT is an $O(\log \min(n/m, P))$-approximation |
| online, one machine, $\sum F_j$ | SRPT is optimal, so its competitive ratio is 1 |
| online, one machine, $\sum w_j F_j$ | no constant competitive ratio (Bansal and Chan 2009) |

Here $P$ is the ratio of the largest to the smallest processing time. For the online versions see [online flow time minimization](/online-flow-time-minimization/). The [stretch](/stretch/) $F_j / p_j$ is the flow time with $w_j = 1/p_j$.

## Examples

**Five jobs.** Take the jobs of the [weighted completion time page](/weighted-completion-time-scheduling/), numbered from 0:

| job | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| $p_j$ | 5 | 1 | 2 | 4 | 1 |
| $r_j$ | 0 | 1 | 2 | 3 | 8 |

Here $\sum_j r_j = 14$.

| schedule | completion times | $\sum C_j$ | $\sum F_j$ |
|---|---|---|---|
| SRPT, with preemption | 8, 2, 4, 13, 9 | 36 | 22 |
| best without preemption, order $1, 2, 3, 4, 0$ | 14, 2, 4, 8, 9 | 37 | 23 |
| SRPT order run whole, $1, 2, 0, 4, 3$ | 9, 2, 4, 14, 10 | 39 | 25 |
| FIFO, order $0, 1, 2, 3, 4$ | 5, 6, 8, 12, 13 | 44 | 30 |

The SRPT order run without preemption is within $39/37 \approx 1.05$ of the optimum for completion time, but within $25/23 \approx 1.09$ for flow time. The gap grows when all release dates are shifted by a large constant: $\sum C_j$ ratios tend to 1, but $\sum F_j$ ratios do not change.

FIFO is the worst of the four for the total, but it is the best for the maximum. Its flow times are $5, 5, 6, 9, 5$, so $F_{\max} = 9$. Jobs 0 to 3 are released by time 3 and need 12 units of work in total, so in any schedule one of them completes at 12 or later and has flow time at least $12 - 3 = 9$.

**Weights.** Take $p = (2, 1)$, $r = (0, 0)$ and $w = (10, 1)$. SRPT runs job 1 first, with $\sum w_j F_j = 10 \cdot 3 + 1 \cdot 1 = 31$. Running job 0 first gives $10 \cdot 2 + 1 \cdot 3 = 23$. So SRPT is not optimal with weights.

## Known algorithms

**SRPT for $1 \mid r_j, pmtn \mid \sum F_j$.** At each moment, run the released job with the least remaining processing time.

```pseudo id=main
SRPT(p[1 .. n], r[1 .. n])
L1  sort the jobs by release date
L2  t ← 0, H ← empty min-heap keyed by remaining time
L3  while some job is not complete do
L4      insert into H every job with r[j] ≤ t; if H is empty then t ← next release date
L5      remove from H the job j with the least remaining time q
L6      run j until t + q or the next release date, whichever is first; if it ends at t + q then C[j] ← t + q, else put j back with the work left
L7  return C and the total flow time, the sum over j of C[j] − r[j]
```

A job is put back only at a release date, so lines L5 and L6 run at most $2n$ times, and the time is $O(n \log n)$ with $O(n)$ space.

*Why SRPT is optimal.* At time $t$, let $N(t)$ be the number of released jobs that are not complete. Then $\sum_j F_j = \int_0^\infty N(t)\,dt$. For each $k$, the $k$ smallest remaining times at $t$ in SRPT sum to at most those in any other schedule at $t$, by an exchange argument over time. Hence SRPT has at least as many completed jobs as any other schedule at each time, and so the smallest $N(t)$ at each $t$. The full proof is on the page [SRPT optimality](/srpt-optimality/).

**FIFO for $1 \mid r_j \mid F_{\max}$.** Run the jobs whole in order of release date, as early as possible.

**Theorem.** FIFO minimizes $F_{\max}$, also among preemptive schedules.

*Proof.* Let job $k$ have the largest flow time in FIFO. Let $i$ be the first job of the busy period of FIFO that contains $k$. Then $k$ completes at $r_i + p(B)$, where $B$ is the set of jobs from $i$ to $k$ in FIFO order, and each job of $B$ has its release date in $[r_i, r_k]$. In any schedule, no job of $B$ runs before $r_i$, so the last job of $B$ to complete does so at $r_i + p(B)$ or later. Its release date is at most $r_k$, so its flow time is at least $r_i + p(B) - r_k$, which is the flow time of $k$ in FIFO. ∎

The problem $1 \mid r_j \mid F_{\max}$ is $1 \mid r_j \mid L_{\max}$ with due dates $d_j = r_j$. Release dates and due dates are then in the same order, which is why the [maximum lateness](/maximum-lateness-minimization/) problem, strongly NP-hard in general, is easy here.

The tests of this page compare SRPT and FIFO with a dynamic program over unit time slots that allows preemption, and with a search over all orders without preemption, on seeded random instances.

**Other algorithms.**

- **Without preemption.** Kellerer, Tautenhahn and Woeginger (1999) turn an optimal preemptive schedule into a non-preemptive one and get the ratio $O(\sqrt n)$. They also prove that no polynomial algorithm has ratio $O(n^{1/2 - \varepsilon})$ for any $\varepsilon > 0$ unless P = NP. *Sketch of the hardness idea:* add many short jobs that arrive at fixed times, so that a schedule that does not fit the long jobs into the right gaps makes many short jobs wait. We do not reproduce the proof here.
- **Weighted flow time with preemption.** Chekuri, Khanna and Zhu (2001) give $O(\log^2 P)$, and Bansal and Pruhs (2010) $O(\log \log P)$. Batra, Garg and Kumar (2018) give the first constant factor, in pseudo-polynomial time, and Feige, Kulkarni and Li (2019) make it polynomial. Rohwedder and Wiese (2021) give $2 + \varepsilon$, and Armbruster, Rohwedder and Wiese (2023) a PTAS.
- **Parallel machines.** SRPT on $m$ machines runs the $m$ jobs with the least remaining time. Leonardi and Raz (2007) prove the ratio $O(\log \min(n/m, P))$, and show that no online algorithm does better by more than a constant factor.
- **Highest density first.** Running the job with the largest $w_j / p_j$ is optimal for $\sum w_j F_j$ when all jobs are released together, by [Smith's rule](/smith-rule/). With release dates and some extra speed it does well in the online setting.

## Bounds

- **Exact.** $O(n \log n)$ for $1 \mid r_j, pmtn \mid \sum F_j$ and for $1 \mid r_j \mid F_{\max}$.
- **Approximation without preemption.** $\Theta(\sqrt n)$ up to the factor $n^{\varepsilon}$ for $1 \mid r_j \mid \sum F_j$: an $O(\sqrt n)$-approximation exists, and $O(n^{1/2 - \varepsilon})$ is NP-hard.
- **Weights.** $1 \mid r_j, pmtn \mid \sum w_j F_j$ is strongly NP-hard, so it has no [FPTAS](/fptas/) unless P = NP, but it has a [PTAS](/ptas/).
- **Online.** With weights, no online algorithm has a constant [competitive ratio](/competitive-ratio/) (Bansal and Chan 2009).

## Reductions

- **Flow time and completion time.** $\sum_j F_j = \sum_j C_j - \sum_j r_j$, so exact algorithms for one give exact algorithms for the other. Approximation ratios do not carry over, because the constant can dominate.
- **Maximum flow time and maximum lateness.** $F_{\max}$ is $L_{\max}$ with $d_j = r_j$.
- **Stretch.** The total stretch $\sum_j F_j / p_j$ is the weighted flow time with $w_j = 1/p_j$. See [stretch](/stretch/).

## Applications

- **Response time of servers.** A web server or a database answers requests that arrive over time. The mean flow time is the mean response time, and SRPT-like rules are used in practice for static content, where the size of a request is known.
- **Operating systems.** "Shortest remaining time next" is SRPT for processes whose lengths can be estimated.
- **Fairness.** The maximum flow time and the stretch measure how long the worst-off job waits, which the total flow time ignores.

## References
