---
tag: AXAG57
kind: problem
slug: online-speed-scaling
name: Online speed scaling
aliases:
- dynamic speed scaling
- energy-efficient online scheduling
area: online-and-streaming/online-scheduling
level: advanced
summary: Choose processor speeds online to meet deadlines while minimizing energy under a convex power function.
prereqs: [speed-scaling, online-algorithm, competitive-ratio, deadline, release-time]
see_also: [yds-algorithm, avr, avr-competitive-ratio, optimal-available, bkp-speed-scaling, earliest-deadline-first, convex-function, online-throughput-maximization]
sources:
  - paper: "F. Frances Yao, Alan Demers and Scott Shenker, A scheduling model for reduced CPU energy, FOCS 1995"
    locator: pages 374 to 382 (the model with power s^alpha, the offline algorithm, AVR and OA, and the lower bound alpha^alpha for both)
  - paper: "Nikhil Bansal, Tracy Kimbrel and Kirk Pruhs, Speed scaling to manage energy and temperature, Journal of the ACM 54(1), 2007 (FOCS 2004)"
    locator: OA is exactly alpha^alpha competitive, BKP is 2 (alpha / (alpha - 1))^alpha e^alpha competitive and e competitive for the maximum speed, and the lower bound Omega((4/3)^alpha) for randomized algorithms
  - paper: "Nikhil Bansal, Ho-Leung Chan, Kirk Pruhs and Dmitriy Katz, Improved bounds for speed scaling in devices obeying the cube-root rule, ICALP 2009"
    locator: pages 144 to 155 (qOA with ratio 4^alpha / (2 sqrt(e alpha)), and the lower bound e^(alpha - 1) / alpha for deterministic algorithms)
  - paper: doi:10.1007/s00453-009-9379-z
    title: Nikhil Bansal, David P. Bunde, Ho-Leung Chan and Kirk Pruhs, Average rate speed scaling, Algorithmica 60(4), 2011 (LATIN 2008)
    locator: pages 877 to 889 (AVR is at least ((2 - delta) alpha)^alpha / 2 competitive, and a potential function proof of its upper bound)
  - paper: doi:10.4230/LIPIcs.STACS.2011.1
    title: Susanne Albers, Algorithms for dynamic speed scaling, STACS 2011
    locator: Section 2 (a survey of the deadline model, the online algorithms and their bounds) and Sections 3 and 4 (flow time plus energy, and sleep states)
---

Online speed scaling is the [speed scaling](/speed-scaling/) problem when the jobs arrive over time. A single processor can run at any speed, and at speed $s$ it uses power $s^{\alpha}$ for a constant $\alpha > 1$. Each job has a release time, an amount of work and a [deadline](/deadline/), and becomes known only at its release time. An [online algorithm](/online-algorithm/) chooses the speed and the job to run at each moment, must finish every job by its deadline, and aims to use little energy compared with the optimal offline schedule of the [YDS algorithm](/yds-algorithm/). The model is due to Yao, Demers and Shenker (1995). The best known deterministic ratios are $\alpha^{\alpha}$ ([Optimal Available](/optimal-available/)), $4^{\alpha} / (2 \sqrt{e \alpha})$ (qOA) and $2 (\alpha / (\alpha - 1))^{\alpha} e^{\alpha}$ ([BKP](/bkp-speed-scaling/)), and no deterministic algorithm is better than $e^{\alpha - 1} / \alpha$.

## In plain words

A processor that runs at half speed uses much less than half the power. With power $s^3$, half speed uses one eighth of the power, so doing the same work takes one quarter of the energy. So the processor should run as slowly as the deadlines allow.

If all jobs were known in advance, the best plan would be simple to compute. Online, the processor does not know what comes next. If it runs slowly and a lot of work then arrives, it must run very fast later, which costs much energy. If it runs fast and nothing more arrives, it has wasted energy. The question is how close an online rule can get to the best plan, measured as a ratio of energies that depends on $\alpha$.

## Definition

The input is a sequence $\sigma$ of $n$ jobs. Job $j$ has a release time $r_j$, a work $w_j > 0$ and a deadline $d_j > r_j$, and all three become known at time $r_j$. A schedule chooses a speed $s(t) \ge 0$ and a job to run at each time $t$; jobs may be preempted and resumed at no cost. It is feasible if each job gets $w_j$ units of work inside $[r_j, d_j]$. Its energy is

$$E = \int s(t)^{\alpha} \, dt.$$

There is no maximum speed, so a feasible schedule always exists, online as well as offline.

| symbol | meaning |
|---|---|
| $\sigma$ | the sequence of jobs, revealed at the release times |
| ALG$(\sigma)$ | the energy of the online algorithm, which must be feasible on every input |
| OPT$(\sigma)$ | the minimum energy of a feasible schedule, computed offline by the [YDS algorithm](/yds-algorithm/) |
| $c$ | the [competitive ratio](/competitive-ratio/): ALG$(\sigma) \le c \cdot$ OPT$(\sigma)$ for each $\sigma$, with additive constant $b = 0$ |
| $\alpha$ | the power exponent, $\alpha > 1$; for CMOS processors the cube-root rule gives $\alpha \approx 3$ |

Since the energy scales by a factor $\lambda^{\alpha}$ when all works scale by $\lambda$, an additive constant would not help, and the ratio is taken with $b = 0$. For a randomized algorithm, the ratio is taken against an oblivious adversary, which fixes $\sigma$ in advance: $\mathbb{E}[\text{ALG}(\sigma)] \le c \cdot$ OPT$(\sigma)$.

Two facts make the problem easier than it looks. First, once the speed $s(t)$ is fixed, [earliest deadline first](/earliest-deadline-first/) meets all deadlines whenever any order does, so an algorithm only needs to choose the speed. Second, by the [convexity](/convex-function/) of $s^{\alpha}$, a constant speed is the cheapest way to do a fixed amount of work in a fixed interval.

## Variants

- **General power functions.** Any convex power function $P(s)$. Many results extend, with ratios that depend on how fast $P$ grows.
- **Bounded speed.** If the speed is at most $T$, some inputs cannot be finished in time. The goal then combines throughput and energy, in the spirit of [online throughput maximization](/online-throughput-maximization/).
- **Flow time plus energy.** Without deadlines, the objective is the total [flow time](/flow-time/) plus the energy, studied by Albers and Fujiwara. Pruhs, Uthaisombut and Woeginger studied the flow time with a fixed energy budget.
- **Several processors.** Jobs must also be assigned to processors, with or without [migration](/job-migration/).
- **Sleep states.** The processor may also go to sleep and pay a cost to wake up.
- **Temperature.** The goal is to keep the maximum temperature low, under a cooling model (Bansal, Kimbrel and Pruhs).
- **Discrete speeds.** Only a few speeds are available. A wanted speed is replaced by the two nearest speeds in the right proportion.

## Examples

Take three jobs, written as (release, work, deadline): $A = (0, 4, 4)$, $B = (1, 3, 3)$ and $C = (2, 2, 6)$.

- **Offline optimum.** YDS runs $A$ and $B$ at speed $7/4$ on $[0, 4)$ and $C$ at speed 1 on $[4, 6)$.
- **AVR** runs at the sum of the densities of the open windows: 1, $5/2$, 3 and $3/2$ on the four unit intervals up to 4, then $1/2$ on $[4, 6)$.
- **OA** runs at 1 on $[0, 1)$, at 2 on $[1, 4)$ and at 1 on $[4, 6)$.
- **BKP** has a speed that changes all the time, with a largest value $7e/4 \approx 4.76$.

| algorithm | energy, $\alpha = 2$ | ratio | energy, $\alpha = 3$ | ratio |
|---|---|---|---|---|
| OPT (YDS) | $57/4$ | 1 | $375/16$ | 1 |
| OA | 15 | $20/19 \approx 1.05$ | 27 | about 1.15 |
| AVR | 19 | $4/3$ | $189/4$ | about 2.02 |
| BKP | about 30.4 | about 2.13 | about 113.3 | about 4.83 |

The exact values for YDS, AVR and OA are checked with fractions in the tests of the [AVR](/avr/) and [Optimal Available](/optimal-available/) pages, and the BKP values with a fine time step on the [BKP](/bkp-speed-scaling/) page. On this small input the cautious BKP rule is the worst, although its guarantee is the best for large $\alpha$.

## Known algorithms

| algorithm | idea | energy ratio | $\alpha = 2$ | $\alpha = 3$ | proof here |
|---|---|---|---|---|---|
| [AVR](/avr/) | sum of the job densities | $2^{\alpha - 1} \alpha^{\alpha}$ | 8 | 108 | full, on [AVR competitive ratio](/avr-competitive-ratio/) |
| [Optimal Available](/optimal-available/) | optimal plan for the known work | $\alpha^{\alpha}$, exact | 4 | 27 | lower bound only |
| qOA | $q$ times the OA speed, $q = 2 - 1/\alpha$ | $4^{\alpha} / (2 \sqrt{e \alpha})$ | about 3.43 | about 11.2 | cited |
| [BKP](/bkp-speed-scaling/) | $e$ times the densest recent window | $2 (\alpha / (\alpha - 1))^{\alpha} e^{\alpha}$ | about 59.1 | about 135.6 | feasibility only |

All four algorithms run the jobs by EDF, and each meets every deadline. BKP is also $e$-competitive for the maximum speed, which is proved on its page. For $\alpha$ above about 4.2, BKP has a better guarantee than OA, and for $\alpha$ above about 11 it is also better than qOA.

## Bounds

**A proved lower bound for every deterministic algorithm.** Every deterministic online algorithm has ratio at least

$$\frac{(4/3)^{\alpha} + (2/3)^{\alpha}}{2},$$

which is $10/9$ for $\alpha = 2$ and $4/3$ for $\alpha = 3$.

*Proof.* At time 0, job $(0, 1, 2)$ arrives. Let $x \in [0, 1]$ be the work that the algorithm does on $[0, 1)$; it does not depend on the future, since the algorithm is deterministic. By convexity, its energy on $[0, 1)$ is at least $x^{\alpha}$.

- If nothing else arrives, the algorithm has energy at least $x^{\alpha} + (1 - x)^{\alpha}$, and OPT runs at $1/2$ on $[0, 2)$ with energy $2^{1 - \alpha}$.
- If a second job $(1, 1, 2)$ arrives at time 1, the algorithm must do $2 - x$ units of work on $[1, 2)$, so its energy is at least $x^{\alpha} + (2 - x)^{\alpha}$. OPT runs at speed 1 on $[0, 2)$, doing the first job on $[0, 1)$ and the second on $[1, 2)$, with energy 2.

The first ratio $2^{\alpha - 1}(x^{\alpha} + (1 - x)^{\alpha})$ does not decrease for $x \ge 1/2$ and is symmetric about $1/2$, and the second ratio $(x^{\alpha} + (2 - x)^{\alpha})/2$ does not increase on $[0, 1]$. At $x = 2/3$ both equal $2^{\alpha - 1} (2^{\alpha} + 1) / 3^{\alpha}$, which is the value above. For $x \le 2/3$ the second ratio is at least this value, and for $x \ge 2/3$ the first one is. $\square$

**Cited bounds.**

- Every deterministic online algorithm has ratio at least $e^{\alpha - 1} / \alpha$, about 1.36 for $\alpha = 2$ and 2.46 for $\alpha = 3$ (Bansal, Chan, Katz and Pruhs 2009).
- Every randomized online algorithm has ratio $\Omega((4/3)^{\alpha})$ against an oblivious adversary (Bansal, Kimbrel and Pruhs).
- For AVR, the ratio is at least $((2 - \delta) \alpha)^{\alpha} / 2$ with $\delta \to 0$ as $\alpha$ grows (Bansal, Bunde, Chan and Pruhs).

**The $\alpha^{\alpha}$ family.** Let work arrive at rate $(1 - t)^{-1/\alpha}$ on $[0, 1 - \varepsilon]$, all with deadline 1. OPT runs at the arrival rate and uses energy at most $\ln(1/\varepsilon)$, while OA and AVR run at $\alpha((1 - t)^{-1/\alpha} - 1)$ and use $\alpha^{\alpha}(\ln(1/\varepsilon) - O(1))$. So both have ratio at least $\alpha^{\alpha}$, which shows that the analysis of OA is exact. The computation is on the [Optimal Available](/optimal-available/) page.

## Reductions

- **To the choice of a speed.** By the EDF fact in the definition, the problem reduces to choosing $s(t)$ online so that EDF at that speed is feasible. All the algorithms above are speed rules.
- **From the offline problem.** If all jobs are released at the same time, OA is optimal online, since it computes the YDS schedule at time 0 and nothing changes later. If all jobs have the same deadline, OA and AVR have the same speed.
- **From online deadline scheduling.** With a maximum speed and values for the jobs, the problem contains [online throughput maximization](/online-throughput-maximization/), where the speed is fixed and only the job choice is online.

## Applications

- **Dynamic voltage and frequency scaling.** Laptop, phone and server processors lower their clock rate and voltage when the load is light. Since dynamic power grows roughly with the cube of the frequency, slowing down saves energy, and online speed scaling is the model of how to do this with deadlines.
- **Real-time systems.** In [real-time scheduling](/real-time-scheduling/), tasks with hard deadlines run on processors whose speed can be set, and the speed rule must keep every deadline.
- **Data centers.** The same trade-off between speed and energy appears for servers and disks, together with the sleep states of the variants.

## References
