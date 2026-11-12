---
tag: X20JQV
kind: problem
slug: scheduling-problem
name: Scheduling problem
area: systems/scheduling
level: intro
summary: "Assign jobs to machines over time, so that no machine runs two jobs at once and each job gets its processing time, and optimize an objective such as makespan or total completion time."
see_also: [cpu-scheduling, scheduling-metrics, scheduling-notation, graham-three-field-notation, single-machine-scheduling, machine-environments, real-time-scheduling, flow-time-minimization]
sources:
  - book: isbn:9783319265780
    title: Michael L. Pinedo, Scheduling, Theory, Algorithms, and Systems, fifth edition, Springer, 2016
    locator: Chapter 1 (the role of scheduling) and Chapter 2 (deterministic models, the framework and the notation)
  - book: isbn:9783540695158
    title: Peter Brucker, Scheduling Algorithms, fifth edition, Springer, 2007
    locator: Chapter 1 (classification of scheduling problems) and Chapter 4 (single machine problems)
  - paper: doi:10.1016/S0167-5060(08)70356-X
    title: R. L. Graham, E. L. Lawler, J. K. Lenstra and A. H. G. Rinnooy Kan, Optimization and approximation in deterministic sequencing and scheduling, a survey, Annals of Discrete Mathematics 5, 1979
    locator: Section 2 (the classification) and the sections on single machine and parallel machine problems
  - paper: "Jan Karel Lenstra, Alexander H. G. Rinnooy Kan and Peter Brucker, Complexity of machine scheduling problems, Annals of Discrete Mathematics 1, 1977"
    locator: pages 343 to 362 (strong NP-hardness of 1|r_j|Lmax and 1|r_j|sum C_j, among others)
  - book: isbn:9781119320913
    title: Abraham Silberschatz, Peter B. Galvin and Greg Gagne, Operating System Concepts, tenth edition, Wiley, 2018
    locator: Chapter 5 (CPU scheduling) and Chapter 11, Section 11.2 (HDD scheduling)
---

The scheduling problem asks how to run a set of jobs on a set of machines over time: each machine runs at most one job at a time, each job gets its processing time after its release, and a chosen objective, such as the time when the last job ends or the sum of the completion times, is as small as possible. It is the common frame of [CPU scheduling](/cpu-scheduling/), [disk scheduling](/disk-scheduling/), [real-time scheduling](/real-time-scheduling/) and the machine scheduling of operations research. This page states the problem and its main cases; the notation that names each case is on [three-field notation](/scheduling-notation/), and the online forms are on [Graham's three-field notation](/graham-three-field-notation/) in online scheduling.

## In plain words

You have some jobs and some machines. Each job needs a machine for some time. A job may have to wait until a start time, and it may have a due time. A machine can do only one job at a time.

A schedule says which machine does which job, and when. Many schedules are possible, and you want a good one. What "good" means depends on what you care about. You may want all the work done as early as possible. You may want the jobs, on average, to finish soon after they arrive. You may want no job to be late.

These goals often disagree. The order that finishes all the work first can make the average job wait longer. So each scheduling problem names its jobs, its machines, its rules, and the one quantity to make small.

## Definition

**Input.** A set of $n$ jobs $J = \{1, \ldots, n\}$ and $m$ machines $M = \{1, \ldots, m\}$. Job $j$ has a processing time $p_j > 0$, and may have a release time $r_j \ge 0$, a due date $d_j$, a weight $w_j > 0$, and a set of predecessors. On machines of different speeds or kinds, the processing time depends on the machine, $p_{ij}$; see [machine environments](/machine-environments/).

**Schedule.** A schedule $S$ gives each job a finite set of pieces $(i, [s, e))$, each one a machine $i$ and a time interval. It is *feasible* when

1. no two pieces on the same machine overlap;
2. no two pieces of the same job overlap (a job is on one machine at a time);
3. each piece of job $j$ starts at or after $r_j$, and after all predecessors of $j$ end;
4. the pieces of job $j$ do the work $p_j$ in total (on identical machines, their lengths sum to $p_j$);
5. without preemption, each job has exactly one piece.

The completion time $C_j(S)$ is the end of the last piece of job $j$.

**Objective.** A function $f(C_1, \ldots, C_n)$ to minimize. The usual ones are the [makespan](/makespan/) $C_{\max} = \max_j C_j$, the total completion time $\sum_j C_j$, the weighted total $\sum_j w_j C_j$, the total [flow time](/flow-time/) $\sum_j (C_j - r_j)$, the maximum lateness $L_{\max} = \max_j (C_j - d_j)$, and the number of late jobs $\sum_j U_j$ with $U_j = [C_j > d_j]$. Each of these is *regular*: it does not decrease when some $C_j$ grows.

**Output.** A feasible schedule $S$ with the least value $f(C_1(S), \ldots, C_n(S))$.

The three-field notation $\alpha \mid \beta \mid \gamma$ names a case by its machines, its job rules and its objective, for example $1 \mid r_j \mid \sum C_j$. It is defined on [three-field notation](/scheduling-notation/), and this page uses it without repeating the definition.

## Variants

- **Offline or online.** Offline, all jobs are known at the start. Online, a job becomes known at its release, and the scheduler must act without the future; see [online algorithm](/online-algorithm/).
- **Clairvoyant or not.** A [clairvoyant](/clairvoyant-scheduling/) scheduler learns $p_j$ when job $j$ arrives. An operating system usually does not, and predicts it from the past, as in [shortest-job-first](/shortest-job-first/).
- **With or without preemption.** See [preemption](/preemption/) for the systems view and [preemptive scheduling](/preemptive-scheduling/) for the theory.
- **Real time.** Jobs come from tasks that repeat, with deadlines, and the question is whether every deadline can be met; see [real-time scheduling](/real-time-scheduling/) and [schedulability analysis](/schedulability-analysis/).
- **Shops.** Each job is a chain of operations on different machines: [flow shop](/flow-shop-scheduling/), [job shop](/job-shop-scheduling/) and [open shop](/open-shop-scheduling/).
- **Decision form.** Given a bound $K$, is there a feasible schedule with $f \le K$? The decision form is the one used in NP-hardness proofs.

## Examples

One machine, no preemption, four jobs:

| job | $r_j$ | $p_j$ | $d_j$ | $w_j$ |
|---|---|---|---|---|
| 1 | 0 | 4 | 6 | 1 |
| 2 | 1 | 2 | 4 | 3 |
| 3 | 2 | 1 | 5 | 1 |
| 4 | 3 | 3 | 12 | 2 |

Running the jobs in the order of release, each as early as possible, gives completion times 4, 6, 7 and 10. So $C_{\max} = 10$, $\sum C_j = 27$, $\sum w_j C_j = 49$, $L_{\max} = 2$ and $\sum U_j = 2$ (jobs 2 and 3 are late). An exhaustive search over all 24 orders gives the optimum of each objective:

| objective | optimal value | an optimal order |
|---|---|---|
| $C_{\max}$ | 10 | 1, 2, 3, 4 |
| $\sum C_j$ | 25 | 2, 3, 4, 1 |
| $\sum w_j C_j$ | 38 | 2, 3, 4, 1 |
| $\sum (C_j - r_j)$ | 19 | 2, 3, 4, 1 |
| $L_{\max}$ | 2 | 1, 2, 3, 4 |
| $\sum U_j$ | 1 | 1, 3, 2, 4 |

The best order for $\sum C_j$ keeps the machine idle from 0 to 1 to wait for job 2, and ends at 11, later than the release order. So the objectives disagree, and the best schedule for $\sum C_j$ is not work-conserving. With preemption allowed, the schedule 1, 2, 3, 1, 4 on the intervals $[0,1), [1,3), [3,4), [4,7), [7,10)$ has $\sum C_j = 24$, less than any nonpreemptive schedule.

## Known algorithms

One machine:

- $1 \mid\mid \sum C_j$: [shortest processing time first](/shortest-processing-time-first/), $O(n \log n)$. The operating-system form, with predicted bursts, is [shortest-job-first](/shortest-job-first/).
- $1 \mid\mid \sum w_j C_j$: [Smith's rule](/smith-rule/), $O(n \log n)$; see also [weighted completion time](/weighted-completion-time/).
- $1 \mid\mid L_{\max}$: [earliest due date first](/earliest-due-date-first/), $O(n \log n)$.
- $1 \mid\mid \sum U_j$: the [Moore-Hodgson algorithm](/moore-hodgson-algorithm/), $O(n \log n)$.
- $1 \mid r_j, \mathrm{pmtn} \mid \sum C_j$: [SRPT](/srpt/), optimal by [Schrage's theorem](/srpt-optimality/).

Several machines:

- $P \mid\mid C_{\max}$: [list scheduling](/list-scheduling/) and [longest processing time first](/longest-processing-time-first/), approximation algorithms; see [makespan minimization](/makespan-minimization/).
- $F2 \mid\mid C_{\max}$: [Johnson's rule](/johnsons-rule/), $O(n \log n)$.

Operating systems use online rules that are judged by the [scheduling metrics](/scheduling-metrics/): [FCFS](/fcfs-scheduling/), [round robin](/round-robin/), [priority scheduling](/priority-scheduling/) and the [multilevel feedback queue](/multilevel-feedback-queue/).

## Bounds

- The cases above with an $O(n \log n)$ rule are in P. Each rule sorts the jobs by one key, and the sort dominates the time.
- $1 \mid r_j \mid L_{\max}$ and $1 \mid r_j \mid \sum C_j$ are [strongly NP-hard](/strong-np-hardness/) (Lenstra, Rinnooy Kan and Brucker 1977). So a release date alone, without preemption, makes the one-machine problem hard; see [scheduling with release dates](/scheduling-with-release-dates/).
- $P2 \mid\mid C_{\max}$ is NP-hard, and $P \mid\mid C_{\max}$ with $m$ in the input is strongly NP-hard; see [makespan minimization](/makespan-minimization/).
- Each nonpreemptive one-machine instance has an optimal schedule among the $n!$ orders, each job started as early as its order allows, because the objectives are regular. So exhaustive search takes $O(n! \cdot n)$ time and is exact; it is the oracle of the tests of this area.

## Reductions

- **From [partition](/partition-problem/) to $P2 \mid\mid C_{\max}$.** Given positive integers $a_1, \ldots, a_n$ with sum $2B$, make job $j$ with $p_j = a_j$. Two machines finish by time $B$ if and only if the numbers split into two sets of sum $B$. The reduction takes $O(n)$ time.
- **From [3-partition](/three-partition/) to $P \mid\mid C_{\max}$**, which gives strong NP-hardness.
- **CPU scheduling to machine scheduling.** With one CPU burst per process and no I/O, [CPU scheduling](/cpu-scheduling/) is $1 \mid r_j \mid \gamma$ or $1 \mid r_j, \mathrm{pmtn} \mid \gamma$.

## Applications

Operating systems schedule processes on CPUs and requests on disks. Real-time systems schedule periodic control tasks against deadlines. Factories schedule operations on machines, which is where the theory began. Compilers schedule instructions on functional units, and clusters schedule jobs on servers ([cluster scheduling](/cluster-scheduling/)). Networks schedule packets on links ([packet scheduling](/packet-scheduling/)).

## References
