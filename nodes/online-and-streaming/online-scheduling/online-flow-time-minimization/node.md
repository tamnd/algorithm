---
tag: 0HW8KH
kind: problem
slug: online-flow-time-minimization
name: Online flow time minimization
aliases:
- online total flow time
- online weighted flow time
- online response time minimization
area: online-and-streaming/online-scheduling
level: advanced
summary: Jobs are released online and the total (weighted) flow time must be minimized.
prereqs: [flow-time, online-algorithm, competitive-ratio, release-time]
see_also: [srpt, srpt-optimality, non-clairvoyant-flow-time-minimization, online-max-stretch, flow-time-minimization, stretch, identical-machines, job-migration]
sources:
  - book: isbn:9781584883975
    title: Joseph Y-T. Leung (ed.), Handbook of Scheduling, Algorithms, Models, and Performance Analysis, Chapman and Hall/CRC, 2004
    locator: Chapter 15, Kirk Pruhs, Jiří Sgall and Eric Torng, Online Scheduling (the sections on flow time objectives)
  - paper: "Stefano Leonardi and Danny Raz, Approximating total flow time on parallel machines, Journal of Computer and System Sciences 73(6), 2007 (STOC 1997)"
    locator: pages 875 to 891 (SRPT on m machines is O(log min(n/m, P))-competitive, and the Omega(log(n/m)) and Omega(log P) lower bounds for randomized online algorithms)
  - paper: doi:10.1016/j.ipl.2004.02.013
    title: David P. Bunde, SPT is optimally competitive for uniprocessor flow, Information Processing Letters 90(5), 2004
    locator: pages 233 to 238, Theorem 1 (SPT is (Delta + 1)/2-competitive without preemption) and Theorem 12 (no deterministic algorithm does better)
  - paper: "Nikhil Bansal and Ho-Leung Chan, Weighted flow time does not admit O(1)-competitive algorithms, SODA 2009"
    locator: pages 1238 to 1244 (no deterministic online algorithm has a constant ratio for the weighted flow time on one machine)
  - paper: "Baruch Awerbuch, Yossi Azar, Stefano Leonardi and Oded Regev, Minimizing the flow time without migration, SIAM Journal on Computing 31(5), 2002 (STOC 1999)"
    locator: pages 1370 to 1382 (an O(min(log P, log n))-competitive algorithm on m machines without migration)
  - paper: "Michael A. Bender, Soumen Chakrabarti and S. Muthukrishnan, Flow and stretch metrics for scheduling continuous job streams, SODA 1998"
    locator: pages 270 to 279 (FIFO is (3 - 2/m)-competitive for the maximum flow time on m machines)
  - paper: "Luca Becchetti, Stefano Leonardi, Alberto Marchetti-Spaccamela and Kirk Pruhs, Online weighted flow time and deadline scheduling, Journal of Discrete Algorithms 4(3), 2006 (APPROX 2001)"
    locator: pages 339 to 352 (highest density first with speed 1 + eps is (1 + 1/eps)-competitive for the weighted flow time)
---

Online flow time minimization is the problem of scheduling jobs that arrive over time, so that the total (or weighted) [flow time](/flow-time/) is small, when each job becomes known only at its [release time](/release-time/). An [online algorithm](/online-algorithm/) is judged by its [competitive ratio](/competitive-ratio/) against the best offline schedule. On one machine with [preemption](/preemptive-scheduling/), [SRPT](/srpt/) is optimal. Each change of the model (more machines, weights, no preemption, unknown sizes) makes the best ratio grow, often to a logarithm or a polynomial of the input.

## In plain words

A server gets requests over time. It does not know what requests come later. Each request says how much work it needs. The server decides at each moment which request to work on. The goal is that, on average, requests leave the system soon after they arrive.

If the server can pause a request and continue it later, the best rule is to always work on the request with the least work left. No other rule, even one that knows the future, does better on one server. With several servers, or with requests of different importance, or without the right to pause, no rule is always close to the best one. The theory then asks how far from the best a rule must be in the worst case.

## Definition

**Input.** A sequence $\sigma$ of $n$ jobs. Job $j$ has a release time $r_j \ge 0$, a processing time $p_j > 0$ and, in the weighted version, a weight $w_j > 0$. The job and its data become known at time $r_j$ (the [clairvoyant](/clairvoyant-scheduling/) model). There are $m \ge 1$ [identical machines](/identical-machines/) of speed 1.

**Output.** A schedule, built online: the decision at time $t$ uses only the jobs with $r_j \le t$. Each machine runs at most one job at a time, and a job runs on at most one machine at a time. With preemption, a job can be stopped and resumed later. With [migration](/job-migration/), it can resume on another machine.

**Objective.** Minimize the total flow time $\sum_j F_j = \sum_j (C_j - r_j)$, or the weighted flow time $\sum_j w_j F_j$.

**Notation.**

| symbol | meaning |
|---|---|
| $\sigma$ | the job sequence |
| ALG$(\sigma)$, OPT$(\sigma)$ | the objective value of the online schedule and of the best offline schedule in the same model |
| $c$ | the competitive ratio: ALG$(\sigma) \le c \cdot$ OPT$(\sigma)$ for each $\sigma$; all ratios below have additive constant $b = 0$ |
| $P$ | the ratio of the largest to the smallest processing time (also written $\Delta$) |
| $W$ | the ratio of the largest to the smallest weight |

For a randomized algorithm, the ratio is in expectation against an [oblivious adversary](/oblivious-adversary/), which fixes $\sigma$ in advance. In three-field notation the basic problem is $P \mid r_j, \text{pmtn} \mid \sum F_j$, with the jobs revealed online.

## Variants

- **One machine or $m$ machines.** On one machine with preemption the problem is solved by SRPT. On $m \ge 2$ machines no online algorithm has a constant ratio.
- **With or without migration.** Without migration, a job stays on the machine where it first runs. Awerbuch, Azar, Leonardi and Regev gave an $O(\min(\log P, \log n))$-competitive algorithm for this model.
- **Without preemption.** Each job runs to completion once it starts.
- **Weighted flow time.** The objective $\sum w_j F_j$. The total [stretch](/stretch/) is the case $w_j = 1/p_j$.
- **Maximum flow time.** The objective $\max_j F_j$. FIFO is optimal on one machine and $(3 - 2/m)$-competitive on $m$ machines (Bender, Chakrabarti and Muthukrishnan 1998). See also [online max stretch](/online-max-stretch/).
- **Unknown sizes.** If $p_j$ is learned only when job $j$ completes, the problem is [non-clairvoyant flow time minimization](/non-clairvoyant-flow-time-minimization/).
- **Extra speed.** In the resource augmentation model, the online algorithm has machines of speed $1 + \varepsilon$ and OPT has speed 1. Many problems with no constant ratio get an $O(1/\varepsilon)$ or $O(1/\varepsilon^2)$ ratio in this model.
- **Flow time plus energy.** With speed scaling, the objective is the flow time plus the energy; see [online speed scaling](/online-speed-scaling/).

## Examples

Take one machine and four jobs, written as (release, size): $A = (0, 5)$, $B = (1, 2)$, $C = (2, 4)$ and $D = (3, 1)$.

| rule | model | flow times of $A, B, C, D$ | total |
|---|---|---|---|
| [SRPT](/srpt/) | preemptive, online | 8, 2, 10, 1 | 21 |
| best schedule without preemption | offline | 13, 2, 6, 1 | 22 |
| SPT, start the shortest waiting job when the machine is free | no preemption, online | 5, 7, 10, 3 | 25 |
| FIFO | no preemption, online | 5, 6, 9, 9 | 29 |
| processor sharing, each waiting job gets an equal share | preemptive, non-clairvoyant | 23/2, 13/2, 10, 4 | 32 |

The offline schedule without preemption keeps the machine idle on $[0, 1)$, then runs $B$, $D$, $C$ and $A$ in this order. An online rule cannot do this, because at time 0 it does not know that $B$ comes at time 1. Online SPT starts $A$ at time 0, and then $B$, $C$ and $D$ wait behind it. The non-clairvoyant rule pays because it does not know which job is short.

**Two machines.** With jobs $(0, 1)$, $(0, 1)$, $(0, 3)$, $(3, 1)$ and $(3, 1)$ on 2 machines, SRPT gets total flow time 9 and the optimum is 8 (the computation is on the [SRPT optimality](/srpt-optimality/) page). So SRPT is not optimal on $m \ge 2$ machines.

## Known algorithms

| algorithm | model | ratio | proved here or cited |
|---|---|---|---|
| [SRPT](/srpt/) | 1 machine, preemptive | 1 (optimal) | proved on [SRPT optimality](/srpt-optimality/) |
| SRPT | $m$ machines, preemptive, with migration | $O(\log \min(n/m, P))$ | cited, Leonardi and Raz 1997 |
| AALR algorithm | $m$ machines, preemptive, no migration | $O(\min(\log P, \log n))$ | cited, Awerbuch, Azar, Leonardi and Regev 1999 |
| SPT | 1 machine, no preemption | $(P + 1)/2$ | cited, Bunde 2004 |
| FIFO | $m$ machines, maximum flow time | $3 - 2/m$ | cited, Bender, Chakrabarti and Muthukrishnan 1998 |
| highest density first | 1 machine, weighted, speed $1 + \varepsilon$ | $1 + 1/\varepsilon$ | cited, Becchetti, Leonardi, Marchetti-Spaccamela and Pruhs |

Highest density first runs the waiting job with the largest $w_j / p_j$. With weights and no extra speed, the best known deterministic ratios on one machine are logarithmic in $W$ or in $P$, and no constant ratio is possible (Bansal and Chan 2009).

## Bounds

- **One machine, preemptive.** The ratio 1 is reached, so the problem has no gap.
- **$m$ machines, preemptive.** Each online algorithm, deterministic or randomized against an oblivious adversary, has ratio $\Omega(\log(n/m))$ on some inputs and $\Omega(\log P)$ on others (Leonardi and Raz 1997). The SRPT upper bound matches this up to a constant factor.
- **One machine, no preemption.** No deterministic online algorithm has a ratio below $(P + 1)/2$, so SPT is optimal (Bunde 2004). As a function of $n$ alone, the deterministic ratio is $\Omega(n)$.
- **Weighted, one machine.** No deterministic online algorithm is $O(1)$-competitive for $\sum w_j F_j$ (Bansal and Chan 2009).
- **Offline.** The offline preemptive problem on one machine is solved by SRPT. Without preemption, it has no $O(n^{1/2 - \varepsilon})$ approximation unless P = NP; see [flow time minimization](/flow-time-minimization/).

## Reductions

- **To total completion time.** Since $\sum F_j = \sum C_j - \sum r_j$, the optimal schedules are the same, but a ratio for $\sum C_j$ gives no ratio for $\sum F_j$. See [flow time](/flow-time/) and [online total completion time](/online-total-completion-time/).
- **Stretch.** Total stretch is weighted flow time with $w_j = 1/p_j$, so each result for weighted flow time applies to it.
- **Preemptive to non-preemptive.** An online schedule without preemption can follow a preemptive one: start each job in the order of its preemptive completion. This loses a factor 2 for $\sum C_j$, but no constant factor for $\sum F_j$.
- **Non-clairvoyant.** Each non-clairvoyant algorithm is also clairvoyant, so the lower bounds of this page also hold for [non-clairvoyant flow time minimization](/non-clairvoyant-flow-time-minimization/), and its upper bounds hold here.

## Applications

Web servers, database servers and operating system schedulers minimize the mean response time, which is the mean flow time. Size-based schedulers in the style of SRPT are used where the sizes are known, for example static files on a web server. Data center schedulers with many machines meet the $m$-machine models, and the gap between the online and the offline optimum there explains why such systems often use extra capacity.

## References
