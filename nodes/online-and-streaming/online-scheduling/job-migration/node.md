---
tag: JR8S17
kind: concept
slug: job-migration
name: Job migration
aliases:
- migratory scheduling
- migration
- non-migratory scheduling
area: online-and-streaming/online-scheduling
level: advanced
summary: "A preempted job may resume on a different machine. Migration changes the offline optimum, the online bounds for flow time, and the number of machines needed for deadlines."
prereqs: [preemptive-scheduling, identical-machines]
see_also: [preemptive-scheduling, mcnaughton-wrap-around, preemptive-makespan-scheduling, online-machine-minimization, online-flow-time-minimization, srpt, real-time-scheduling, deadline]
sources:
  - paper: "Stefano Leonardi and Danny Raz, Approximating total flow time on parallel machines, Journal of Computer and System Sciences 73(6), 2007"
    title: Leonardi and Raz 2007
    locator: the analysis of SRPT with migration on m machines, O(log min(n/m, P)), and the matching lower bound (STOC 1997 version)
  - paper: "Baruch Awerbuch, Yossi Azar, Stefano Leonardi and Oded Regev, Minimizing the flow time without migration, SIAM Journal on Computing 31(5), 2002"
    title: Awerbuch, Azar, Leonardi and Regev 2002
    locator: the non-migratory online algorithm for total flow time and its O(log min(n, P)) bound (STOC 1999 version)
  - paper: "W. A. Horn, Some simple scheduling algorithms, Naval Research Logistics Quarterly 21(1), 1974"
    title: Horn 1974
    locator: the flow formulation for preemptive scheduling with release times and deadlines on identical machines, with migration
---

Migration is the right of a preempted job to continue on another machine. It only matters with [preemption](/preemptive-scheduling/): a job that never stops never changes machine. The classical entry $\mathrm{pmtn}$ allows migration, and a *non-migratory* schedule fixes one machine per job but may still stop and continue jobs there. Online, the two models have different optima and different competitive ratios, so each result must say which model it uses.

## In plain words

Think of a job as a task that a worker can put down and pick up later. With migration, a different worker may pick it up. Without migration, the same worker must finish it. Migration lets the machines share the load of one long job, so the work spreads more evenly. It costs something in a real system, because the state of the job must move, and many systems forbid it. The question is how much the schedule loses when the jobs must stay where they first ran.

## The idea

**Definitions.** In a preemptive schedule on $m$ machines, job $j$ runs during a set of time intervals. The schedule is *migratory* if the intervals of a job may be on different machines, and *non-migratory* (or *partitioned*) if all intervals of each job are on one machine. Both keep the rule that a job runs on at most one machine at a time.

**Without release times, non-migratory preemption is useless for makespan.** If each job stays on one machine, the machine must do the total size $\ell_i$ of its jobs, and it can do so in one block from time $0$. So the non-migratory preemptive optimum equals the nonpreemptive optimum on identical machines. The migratory optimum is $\max\{\max_j p_j, \frac1m \sum_j p_j\}$, reached by [McNaughton's rule](/mcnaughton-wrap-around/), which moves at most $m - 1$ jobs from one machine to the next.

**With time windows, migration decides feasibility.** For jobs with [release times](/release-time/) and [deadlines](/deadline/), Horn (1974) decides migratory feasibility on $m$ machines by a flow: one node per job, one node per elementary interval between consecutive release times and deadlines, capacity $p_j$ out of the source, the interval length from a job to each interval in its window, and $m$ times the interval length into the sink. Without migration, the jobs must first be split among the machines, which is a packing problem and NP-hard in general.

**Online.** The online models differ in what the algorithm may do when a job waits. With migration, a job can move to any machine that becomes free; without it, a job may wait while another machine is idle.

| problem | with migration | without migration |
|---|---|---|
| total [flow time](/online-flow-time-minimization/), $m$ machines | SRPT is $O(\log \min\{\frac nm, P\})$, and this is optimal for deterministic algorithms (Leonardi and Raz) | $O(\log \min\{n, P\})$ (Awerbuch, Azar, Leonardi and Regev) |
| keep all deadlines with few machines | [online machine minimization](/online-machine-minimization/), $O(\log m)$ machines per optimal machine and better | non-migratory versions are studied separately |
| makespan, over a list | ratio $\frac{m^m}{m^m - (m-1)^m}$ ([preemptive scheduling](/preemptive-scheduling/)) | the same as nonpreemptive, by the argument above |

Here $P$ is the ratio of the largest to the smallest job size. The flow time rows are cited.

## Examples

**Three unit jobs on two machines.** The migratory optimum is $\max\{1, \frac32\} = \frac32$. McNaughton's rule fills machine 1 up to time $\frac32$ with job 1 during $[0, 1]$ and job 3 during $[1, \frac32]$, and then wraps the rest of job 3 to machine 2 during $[0, \frac12]$, followed by job 2 during $[\frac12, \frac32]$. The two pieces of job 3 do not overlap in time, so the schedule is valid. Without migration, one machine gets two of the three jobs, and the makespan is $2$. The ratio between the two models is $\frac43$ here.

**Deadlines.** The [deadline page](/deadline/) shows three jobs on two machines for which no online algorithm keeps all deadlines, even with migration. Without migration the offline problem is already harder: three jobs with $r_j = 0$, $p_j = 2$ and $\bar d_j = 3$ fit on two machines with migration (total work $6 = 2 \cdot 3$, and McNaughton's rule gives makespan $3$), but not without, because one machine would need $4 > 3$ time units.

## Where it is used

- Multiprocessor [real-time scheduling](/real-time-scheduling/): global scheduling (with migration) against partitioned scheduling (without).
- The analysis of [SRPT](/srpt/) on parallel machines and of other [flow time](/online-flow-time-minimization/) algorithms.
- [Online machine minimization](/online-machine-minimization/), where the main results assume migration.
- Offline [preemptive makespan scheduling](/preemptive-makespan-scheduling/), where McNaughton's rule needs at most $m - 1$ migrations.

## References
