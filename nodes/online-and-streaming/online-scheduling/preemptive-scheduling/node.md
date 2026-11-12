---
tag: ZK155Z
kind: definition
slug: preemptive-scheduling
name: Preemptive scheduling
aliases:
- pmtn
area: online-and-streaming/online-scheduling
level: intro
summary: "Scheduling where a running job may be interrupted and resumed later without penalty. Online, preemption lowers the makespan ratio on two machines from 3/2 to 4/3 and makes SRPT optimal for flow time."
prereqs: [graham-three-field-notation, preemption]
see_also: [preemption, job-migration, preemptive-makespan-scheduling, mcnaughton-wrap-around, srpt, srpt-optimality, identical-machines, online-makespan-minimization]
sources:
  - paper: "Bo Chen, Andre van Vliet and Gerhard J. Woeginger, An optimal algorithm for preemptive on-line scheduling, Operations Research Letters 18(3), 1995"
    title: Chen, van Vliet and Woeginger 1995
    locator: the preemptive online-list algorithm on m identical machines with ratio m^m / (m^m - (m - 1)^m) and the matching lower bound
  - paper: "Jiri Sgall, On-line scheduling, in A. Fiat and G. J. Woeginger (eds.), Online Algorithms, The State of the Art, LNCS 1442, Springer, 1998"
    title: Sgall 1998, survey chapter
    locator: the sections on preemptive scheduling of jobs one by one and over time
  - book: isbn:9781584883975
    title: "Kirk Pruhs, Jiri Sgall and Eric Torng, Online scheduling, in Joseph Y.-T. Leung (editor), Handbook of Scheduling, Chapman and Hall/CRC, 2004"
    locator: the chapter on online scheduling (Chapter 15), the preemptive results for makespan and flow time
---

A schedule is preemptive if a job may stop and continue later, with no loss of the work done and no extra cost. In the [three-field notation](/graham-three-field-notation/) this is the entry $\mathrm{pmtn}$ of $\beta$, and the offline makespan case is solved by [McNaughton's wrap-around rule](/mcnaughton-wrap-around/); see [preemptive makespan scheduling](/preemptive-makespan-scheduling/). Online, preemption has a different use in each paradigm. Over a list, it lets the algorithm spread a job over gaps of the schedule; over time, it lets the algorithm stop a long job when a short one arrives. This page defines the entry and proves on two machines that preemption lowers the best online makespan ratio to $\frac43$.

## Definition

In a *preemptive* schedule, each job $j$ runs during a finite union of time intervals, on one or more machines, such that:

1. the total length of the intervals of job $j$, weighted by machine speed if there is one, is $p_j$;
2. at each time, job $j$ runs on at most one machine;
3. at each time, each machine runs at most one job.

Whether the pieces of a job may be on different machines is a separate choice, [job migration](/job-migration/). In the classical notation $\mathrm{pmtn}$ allows migration. A *nonpreemptive* schedule runs each job in one interval on one machine. The general concept in operating systems is [preemption](/preemption/).

**Preemption in the online paradigms.**

| paradigm | what the algorithm fixes on arrival of job $j$ |
|---|---|
| $\mathrm{online\text{-}list}, \mathrm{pmtn}$ | all pieces of job $j$: the machines and the time intervals, which may be anywhere in the schedule, also before pieces of earlier jobs, as long as rules 1 to 3 hold |
| $\mathrm{online\text{-}time}, \mathrm{pmtn}$ | nothing in advance; at each time $t$ it chooses which released jobs run, and it may stop a job at any time and continue it later |

In both cases the [offline optimum](/offline-optimum/) is the preemptive optimum. For makespan on identical machines it has the closed form $\max\{\max_j p_j, \frac1m \sum_j p_j\}$ (McNaughton).

**Claim.** For $P2 \mid \mathrm{online\text{-}list}, \mathrm{pmtn} \mid C_{\max}$, every deterministic online algorithm has ratio at least $\frac43$.

*Proof.* Give two jobs of size $1$. Let $c$ be the makespan of the online schedule of these two jobs. If the list ends, $\mathrm{OPT} = 1$, so the ratio is at least $c$. Let $d$ be the total length of the times in $[0, c]$ at which both machines are busy. The two jobs have total size $2 \le 2d + (c - d)$, so $d \ge 2 - c$. Now give a third job of size $2$. Then $\mathrm{OPT} = \max\{2, \frac{4}{2}\} = 2$. The new job cannot run at a time when both machines are busy, and by rule 2 it gets at most one unit of work per time unit, so it ends at time at least $d + 2 \ge 4 - c$. The ratio is then at least $\frac{4 - c}{2}$. So the ratio is at least $\max\{c, \frac{4 - c}{2}\}$, which is smallest at $c = \frac43$, where both terms are $\frac43$. $\square$

## Examples and non-examples

**Makespan over a list.** Without preemption, the best ratio on two machines is $\frac32$, reached by list scheduling ([lower bound](/online-makespan-lower-bound/)). With preemption, it is $\frac43$: the claim above gives the lower bound, and Chen, van Vliet and Woeginger (1995) give an algorithm with ratio $\frac{m^m}{m^m - (m - 1)^m}$ for each $m$, which is $\frac43$ for $m = 2$ and also optimal for each $m$ (cited). The values are about $1.4211$ for $m = 3$ and tend to $\frac{e}{e - 1} \approx 1.5820$, below the nonpreemptive bounds near $1.9$.

**Flow time over time.** On one machine with $\mathrm{online\text{-}time}$, the rule [SRPT](/srpt/), "run the job with the least remaining work", is optimal for $\sum_j F_j$ ([SRPT optimality](/srpt-optimality/)). It needs preemption: when a short job arrives during a long one, SRPT stops the long one. Without preemption, a long job that has started blocks every short job behind it, and no online rule is close to the optimum.

**Non-examples.**

- A schedule in which a stopped job must start again from zero is *preemption with restart*, not $\mathrm{pmtn}$: the work done is lost.
- A job that runs on two machines at the same time is a parallel job, not a preempted job; rule 2 forbids it.
- Splitting a job into parts that are then scheduled as separate jobs without rule 2 is the *divisible load* model, where the bound $\max_j p_j$ does not hold.

## Related definitions

- [Preemption](/preemption/): the systems view.
- [Job migration](/job-migration/): whether the pieces may use different machines.
- [Preemptive makespan scheduling](/preemptive-makespan-scheduling/) and [McNaughton's wrap-around rule](/mcnaughton-wrap-around/): the offline problem.
- [SRPT](/srpt/) and [SRPT optimality](/srpt-optimality/): preemption over time.
- [Online makespan minimization](/online-makespan-minimization/): the nonpreemptive problem.

## References
