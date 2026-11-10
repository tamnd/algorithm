---
tag: GV2GDX
kind: problem
slug: online-makespan-minimization
name: Online makespan minimization
aliases:
- online load balancing on identical machines
- online parallel machine scheduling
- P|online-list|Cmax
area: online-and-streaming/online-scheduling
level: core
summary: "Jobs arrive one by one and must be assigned to identical machines to minimize the makespan. List scheduling is 2 - 1/m competitive; the best known ratio for large m is about 1.9201."
prereqs: [list-scheduling-competitive-ratio, makespan, identical-machines]
see_also: [list-scheduling-competitive-ratio, online-makespan-lower-bound, identical-machines, preemptive-scheduling, makespan-minimization, list-scheduling, online-restricted-assignment-load-balancing, uniform-machines]
sources:
  - paper: "Gabor Galambos and Gerhard J. Woeginger, An on-line scheduling heuristic with better worst case ratio than Graham's list scheduling, SIAM Journal on Computing 22(2), 1993"
    title: Galambos and Woeginger 1993
    locator: the first deterministic algorithm with ratio below 2 - 1/m for every m at least 4
  - paper: "Yair Bartal, Amos Fiat, Howard Karloff and Rakesh Vohra, New algorithms for an ancient scheduling problem, Journal of Computer and System Sciences 51(3), 1995"
    title: Bartal, Fiat, Karloff and Vohra 1995
    locator: the algorithm with ratio 2 - 1/70 (about 1.986) for m at least 70, the first ratio bounded below 2 for all m
  - paper: "David R. Karger, Steven J. Phillips and Eric Torng, A better algorithm for an ancient scheduling problem, Journal of Algorithms 20(2), 1996"
    title: Karger, Phillips and Torng 1996
    locator: the algorithm with ratio 1.945
  - paper: "Susanne Albers, Better bounds for online scheduling, SIAM Journal on Computing 29(2), 1999"
    title: Albers 1999
    locator: the algorithm with ratio 1.923 and the lower bound 1.852 for m at least 80
  - paper: "Rudolf Fleischer and Michaela Wahl, Online scheduling revisited, Journal of Scheduling 3(6), 2000"
    title: Fleischer and Wahl 2000
    locator: the algorithm with ratio 1 + sqrt((1 + ln 2)/2), about 1.9201, the best known for large m
  - paper: "Susanne Albers, On randomized online scheduling, STOC 2002"
    title: Albers 2002
    locator: the randomized algorithm with ratio 1.916 for all m
  - paper: "Jiri Sgall, On-line scheduling, in A. Fiat and G. J. Woeginger (eds.), Online Algorithms, The State of the Art, LNCS 1442, Springer, 1998"
    title: Sgall 1998, survey chapter
    locator: the section on scheduling jobs one by one on identical machines, deterministic and randomized
---

Online makespan minimization is the problem $P \mid \mathrm{online\text{-}list} \mid C_{\max}$: jobs come one by one, each must go to one of $m$ [identical machines](/identical-machines/) at once and for good, and the goal is a small maximum load. The offline problem is [makespan minimization](/makespan-minimization/), which has a PTAS. Online, [list scheduling](/list-scheduling/) is $(2 - \frac1m)$-competitive and optimal for $m \le 3$, and for large $m$ the best known deterministic ratio is about $1.9201$, against a lower bound near $1.88$. The gap between these two numbers is one of the oldest open questions of online algorithms.

## In plain words

Tasks arrive one at a time, and you must hand each one to a worker before you see the next. All workers are equally fast. At the end, you are judged by the time when the last worker is done. Giving each task to the least busy worker is never worse than about twice the best plan. The danger of that rule is a huge task at the end, after the work has been spread evenly. Better rules keep a few workers less busy, so that a huge task has somewhere to go, but not so many that the plan looks bad if no huge task ever comes.

## Definition

**Input.** A number $m \ge 1$ of machines, and a request sequence $\sigma = (p_1, p_2, \ldots, p_n)$ of job sizes $p_t \ge 0$. The number $n$ is not known in advance.

**Online rule.** When $p_t$ is shown, the algorithm assigns job $t$ to a machine $a_t \in \{1, \ldots, m\}$, using only $p_1, \ldots, p_t$ and its earlier choices. The choice is final.

**Cost.** The load of machine $i$ is $\ell_i = \sum_{t :\, a_t = i} p_t$, and $\mathrm{ALG}(\sigma) = \max_i \ell_i$. $\mathrm{OPT}(\sigma)$ is the least makespan of any assignment of the same jobs.

**Measure.** An algorithm is $c$-competitive if $\mathrm{ALG}(\sigma) \le c \cdot \mathrm{OPT}(\sigma) + b$ for all $\sigma$, and strictly $c$-competitive if $b = 0$. Since the adversary can multiply all sizes by a large number, every lower bound below holds for any constant $b$, so the strict and the non-strict ratios are equal. For randomized algorithms, $\mathrm{ALG}$ is the expected makespan against an [oblivious adversary](/oblivious-adversary/).

## Variants

- **Preemptive**, $P \mid \mathrm{online\text{-}list}, \mathrm{pmtn} \mid C_{\max}$: the optimal ratio is known exactly, $\frac{m^m}{m^m - (m - 1)^m}$; see [preemptive scheduling](/preemptive-scheduling/).
- **Over time**, $P \mid \mathrm{online\text{-}time} \mid C_{\max}$: jobs arrive at [release times](/release-time/), and the algorithm may wait. The longest-job-first rule is $\frac32$-competitive.
- **Randomized**: the algorithm may flip coins. On two machines the optimal ratio is $\frac43$.
- **Semi-online**: the algorithm gets extra information, for example that the list is sorted by non-increasing size (then LS is LPT, ratio $\frac43 - \frac1{3m}$, [LPT bound](/lpt-bound/)), or the total size, or the value of $\mathrm{OPT}$.
- **Other machine models**: [uniform](/uniform-machines/) or [unrelated](/unrelated-machines/) machines, and [restricted assignment](/online-restricted-assignment-load-balancing/), where the ratios grow with $m$ or need other ideas.
- **With reassignment**: the algorithm may move a bounded amount of earlier work, which allows ratios close to $1$.

## Examples

**The tight list for list scheduling.** For $m = 4$, take $12$ jobs of size $1$ and then one job of size $4$. LS reaches loads $(3, 3, 3, 3)$ and then a makespan of $7$; the optimum is $4$, so the ratio is $\frac74 = 2 - \frac14$. Graham's theorem says that no list does worse ([proof](/list-scheduling-competitive-ratio/)).

**Why an imbalanced schedule can be better.** On the same unit jobs, a rule that aims at the loads $(4, 4, 2, 2)$ has ratio $\frac43$ if the list stops after the unit jobs, since $\mathrm{OPT} = 3$. If the job of size $4$ then comes, it goes to a machine of load $2$, and the makespan is $6$ against $\mathrm{OPT} = 4$: a ratio of $\frac32$. Both values are below $\frac74$. The algorithms of Galambos and Woeginger, Bartal et al., Karger, Phillips and Torng, Albers, and Fleischer and Wahl turn this idea into a rule for all lists: keep a fixed fraction of the machines at a load well below the others, and use list scheduling otherwise. The adversary answers with other lists, which is why the best ratio stays near $1.9$.

## Known algorithms

| algorithm | ratio | machines | source |
|---|---|---|---|
| [list scheduling](/list-scheduling/) | $2 - \frac1m$ | all $m$; optimal for $m \le 3$ | Graham 1966, [proved here](/list-scheduling-competitive-ratio/) |
| Galambos and Woeginger | $2 - \frac1m - \varepsilon_m$ with $\varepsilon_m > 0$ | $m \ge 4$; tends to $2$ | Galambos and Woeginger 1993 |
| Bartal, Fiat, Karloff and Vohra | $2 - \frac1{70} \approx 1.986$ | $m \ge 70$ | Bartal et al. 1995 |
| Karger, Phillips and Torng | $1.945$ | all $m$ | Karger, Phillips and Torng 1996 |
| Albers | $1.923$ | all $m$ | Albers 1999 |
| Fleischer and Wahl | $1 + \sqrt{\frac{1 + \ln 2}{2}} \approx 1.9201$ | all $m$; the best for large $m$ | Fleischer and Wahl 2000 |
| randomized, two machines | $\frac43$, optimal | $m = 2$ | Bartal et al. 1995 |
| randomized, Albers | $1.916$ | all $m$ | Albers 2002 |

All rows except the first are cited, not proved here.

## Bounds

**Deterministic lower bounds.** No deterministic online algorithm has ratio below:

| value | machines | status on this site |
|---|---|---|
| $\frac32$ | $m = 2$, and every $m \ge 2$ | proved on the [lower bound page](/online-makespan-lower-bound/) |
| $\frac53$ | $m = 3$ | proved on the [lower bound page](/online-makespan-lower-bound/) |
| $\sqrt3 \approx 1.732$ | $m = 4$ | cited (Rudin and Chandrasekaran 2003) |
| $1 + \frac1{\sqrt2} \approx 1.707$ | $m \ge 4$ | cited (Faigle, Kern and Turán 1989) |
| $1.837$ | $m \ge 3454$ | cited (Bartal, Karloff and Rabani 1994) |
| $1.852$ | $m \ge 80$ | cited (Albers 1999) |
| $1.854$ | $m \ge 80$ | cited (Gormley, Reingold, Torng and Westbrook 2000) |
| $1.88$ | $m$ large | cited (Rudin 2001) |

So the optimal deterministic ratio for large $m$ lies between about $1.88$ and $1.9201$. For $m = 2$ and $m = 3$ it is $2 - \frac1m$, reached by LS.

**Randomized lower bound.** No randomized online algorithm has ratio below $\frac{e}{e - 1} \approx 1.582$ against an oblivious adversary as $m \to \infty$ (Chen, van Vliet and Woeginger 1994; Sgall 1997; cited). The best known randomized ratio, $1.916$, is far above it.

## Reductions

- **Special case of load balancing.** The problem is the case $p_{ij} = p_j$ of online [unrelated machines](/unrelated-machines/) and the case $M_j = \{1, \ldots, m\}$ of [online restricted assignment](/online-restricted-assignment-load-balancing/). Lower bounds on this page therefore hold there, and the $\Theta(\log m)$ bounds there show how much the extra structure costs.
- **From a list to time.** Shmoys, Wein and Williamson (1995) turn an offline $\rho$-approximation for makespan with release dates into a $2\rho$-competitive algorithm over time; see [release time](/release-time/).
- **Scaling.** Since $\mathrm{OPT}$ is homogeneous in the sizes, a lower bound list can be scaled, and an algorithm that needs the value of $\mathrm{OPT}$ can guess it and double the guess when it is too small ([doubling trick](/doubling-trick/)), at the price of a constant factor.

## Applications

- Dispatching tasks to identical servers when each task must be placed on arrival, as in a front-end load balancer.
- Assigning jobs to the processors of a parallel computer, with no later migration.
- A test bed for adversary methods: the small-$m$ lower bounds are game trees over sorted load vectors, and the large-$m$ bounds come from computer-aided searches.

## References
