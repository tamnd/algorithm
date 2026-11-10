---
tag: 6ZZRPV
kind: definition
slug: identical-machines
name: Identical machines
aliases:
- parallel identical machines
- P environment
area: online-and-streaming/online-scheduling
level: intro
summary: Machine environment where every job has the same processing time on every machine; online, the state of a schedule is only the multiset of machine loads.
prereqs: [graham-three-field-notation, machine-environments, makespan]
see_also: [uniform-machines, unrelated-machines, restricted-assignment, list-scheduling-competitive-ratio, online-makespan-minimization, online-makespan-lower-bound, machine-environments, makespan-minimization]
sources:
  - paper: doi:10.1002/j.1538-7305.1966.tb01709.x
    title: "R. L. Graham, Bounds for certain multiprocessing anomalies, Bell System Technical Journal 45(9), 1966"
    locator: the model of m identical processors and the bound 2 - 1/m for list schedules
  - book: isbn:9781584883975
    title: "Kirk Pruhs, Jiri Sgall and Eric Torng, Online scheduling, in Joseph Y.-T. Leung (editor), Handbook of Scheduling, Chapman and Hall/CRC, 2004"
    locator: the chapter on online scheduling (Chapter 15), the sections on makespan for jobs one by one and over time
  - paper: "Jiri Sgall, On-line scheduling, in A. Fiat and G. J. Woeginger (eds.), Online Algorithms, The State of the Art, LNCS 1442, Springer, 1998"
    title: Sgall 1998, survey chapter
    locator: the section on scheduling jobs one by one on identical machines, deterministic, randomized and preemptive
  - paper: "Bo Chen, Andre van Vliet and Gerhard J. Woeginger, An optimal algorithm for preemptive on-line scheduling, Operations Research Letters 18(3), 1995"
    title: Chen, van Vliet and Woeginger 1995
    locator: the preemptive online-list algorithm with ratio m^m / (m^m - (m - 1)^m)
  - paper: "Bo Chen and Arjen P. A. Vestjens, Scheduling on identical machines: how good is LPT in an on-line setting?, Operations Research Letters 21(4), 1997"
    title: Chen and Vestjens 1997
    locator: the online-over-time LPT rule, its ratio 3/2, and the lower bound for all online algorithms over time
---

Identical machines are the machine environment $P$ of the [three-field notation](/graham-three-field-notation/): there are $m$ machines, and job $j$ takes the same time $p_j$ on each of them. The [offline page on machine environments](/machine-environments/) places $P$ between one machine and [uniform machines](/uniform-machines/). This page is about what the environment means for an [online algorithm](/online-algorithm/): because all machines are equal, the only thing that matters about a partial schedule is the multiset of machine loads, and the classical online problem on it is [online makespan minimization](/online-makespan-minimization/).

## Definition

There are $m \ge 1$ machines $M_1, \ldots, M_m$. Each job $j$ has a processing time $p_j \ge 0$. If job $j$ runs on machine $M_i$, it occupies $M_i$ for $p_j$ time units, for every $i$. A machine runs at most one job at a time, and, without preemption, a job runs on one machine without a break. The class is written $P \mid \beta \mid \gamma$, or $Pm \mid \beta \mid \gamma$ when the number of machines is a fixed constant.

For a set of jobs on machine $M_i$, the *load* of $M_i$ is $\ell_i = \sum_{j \text{ on } M_i} p_j$. Without release times and without idle time, the [makespan](/makespan/) of a schedule is $\max_i \ell_i$.

**Symmetry.** A permutation of the machines maps each schedule to a schedule with the same cost for every objective. So in the $\mathrm{online\text{-}list}$ paradigm the state of a schedule that matters for the makespan is the sorted load vector $\ell_{(1)} \ge \ell_{(2)} \ge \cdots \ge \ell_{(m)}$, and an online rule only chooses which position of this vector gets the next job. Adversary proofs and exhaustive searches for lower bounds use this: the [lower bounds for $m = 2$ and $m = 3$](/online-makespan-lower-bound/) are game trees over sorted load vectors.

**Two lower bounds on the optimum.** For every instance, $\mathrm{OPT} \ge \frac1m \sum_j p_j$ and $\mathrm{OPT} \ge \max_j p_j$; see [makespan lower bounds](/makespan-lower-bounds/). An online algorithm knows both values for the jobs seen so far, so it can compare its own load with them at each step. Most online algorithms for this environment do so.

**What the environment changes online.** The offline problem $P \mid\mid C_{\max}$ has a PTAS, so offline the environment is easy to approximate. Online, the ratio is a constant strictly between 1 and 2, for each paradigm:

| class | best known deterministic ratio | lower bound | source |
|---|---|---|---|
| $P \mid \mathrm{online\text{-}list} \mid C_{\max}$ | $2 - \frac1m$ for $m \le 3$; about $1.9201$ for large $m$ | $2 - \frac1m$ for $m = 2, 3$; about $1.88$ for large $m$ | [Graham](/list-scheduling-competitive-ratio/), [the lower bounds](/online-makespan-lower-bound/), [the problem page](/online-makespan-minimization/) |
| $P \mid \mathrm{online\text{-}list}, \mathrm{pmtn} \mid C_{\max}$ | $\frac{m^m}{m^m - (m-1)^m}$, optimal | the same | Chen, van Vliet and Woeginger 1995 |
| $P \mid \mathrm{online\text{-}time} \mid C_{\max}$ | $\frac32$ | about $1.3473$ | Chen and Vestjens 1997 |

The preemptive ratio is $\frac43$ for $m = 2$, about $1.4211$ for $m = 3$, and it tends to $\frac{e}{e-1} \approx 1.5820$ as $m \to \infty$. The last two rows are cited, not proved here; the [preemptive scheduling](/preemptive-scheduling/) page proves the case $m = 2$.

## Examples and non-examples

**Example: list scheduling on three machines.** Take $m = 3$ and the list $\sigma = (2, 3, 4, 6, 2, 2)$. [List scheduling](/list-scheduling/) puts each job on a machine of least load (ties to the lowest index).

| job | loads before | machine | loads after |
|---|---|---|---|
| 2 | (0, 0, 0) | $M_1$ | (2, 0, 0) |
| 3 | (2, 0, 0) | $M_2$ | (2, 3, 0) |
| 4 | (2, 3, 0) | $M_3$ | (2, 3, 4) |
| 6 | (2, 3, 4) | $M_1$ | (8, 3, 4) |
| 2 | (8, 3, 4) | $M_2$ | (8, 5, 4) |
| 2 | (8, 5, 4) | $M_3$ | (8, 5, 6) |

The online makespan is $8$. The optimum is $7$: the sets $\{6\}$, $\{4, 3\}$ and $\{2, 2, 2\}$ give loads $6, 7, 6$, and $7$ is the least possible, because the total is $19 > 3 \cdot 6$ and the loads are integers. The ratio $\frac87$ is below Graham's bound $2 - \frac13 = \frac53$. The trouble is the job of size 6: when it came, the least load was 2, and an algorithm that kept one machine empty for a large job would have done better on this list, but worse on others.

**Example: the tight list.** For $m = 3$, the list of six jobs of size 1 followed by one job of size 3 gives list scheduling the loads $(2, 2, 2)$ and then a makespan of $5$, while the optimum is $3$. The ratio is $\frac53 = 2 - \frac13$, so Graham's bound is reached; the [theorem page](/list-scheduling-competitive-ratio/) gives the list for each $m$.

**Non-examples.**

- Machines with speeds, where job $j$ takes $p_j / s_i$ on $M_i$, are [uniform machines](/uniform-machines/), not identical ones. The least loaded machine is then not the machine where a job ends first.
- Times $p_{ij}$ that depend on the pair are [unrelated machines](/unrelated-machines/). A job that may run only on some machines is [restricted assignment](/restricted-assignment/), the case $p_{ij} \in \{p_j, \infty\}$.
- A job that needs several machines at the same time is a parallel or [moldable task](/moldable-task-scheduling/), outside the model.
- Identical machines with preemption are still identical machines: $\mathrm{pmtn}$ is an entry of $\beta$, not of $\alpha$.

## Related definitions

- [Machine environments](/machine-environments/): the offline view of $1$, $P$, $Q$ and $R$, and the shop environments.
- [Uniform machines](/uniform-machines/), [unrelated machines](/unrelated-machines/) and [restricted assignment](/restricted-assignment/): the more general environments, where the online ratios grow with $m$.
- [List scheduling is $(2 - 1/m)$-competitive](/list-scheduling-competitive-ratio/), [online makespan minimization](/online-makespan-minimization/) and its [lower bounds](/online-makespan-lower-bound/).
- [Makespan minimization](/makespan-minimization/): the offline problem $P \mid\mid C_{\max}$.

## References
