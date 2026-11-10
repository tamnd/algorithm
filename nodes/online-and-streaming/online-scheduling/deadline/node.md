---
tag: AHTFR4
kind: definition
slug: deadline
name: Deadline
aliases:
- due date (hard)
- hard deadline
area: online-and-streaming/online-scheduling
level: intro
summary: "The latest time by which a job must complete. Online, EDF keeps all deadlines on one machine, but on two or more machines no online rule finds every feasible schedule."
prereqs: [release-time]
see_also: [release-time, earliest-deadline-first, edf-optimality, least-laxity-first, online-machine-minimization, online-throughput-maximization, online-admission-control, scheduling-with-release-times-and-deadlines]
sources:
  - paper: "Michael L. Dertouzos and Aloysius K. Mok, Multiprocessor on-line scheduling of hard-real-time tasks, IEEE Transactions on Software Engineering 15(12), 1989"
    title: Dertouzos and Mok 1989
    locator: the result that no online algorithm is optimal for scheduling jobs with deadlines on two or more processors
  - paper: "Cynthia A. Phillips, Clifford Stein, Eric Torng and Joel Wein, Optimal time-critical scheduling via resource augmentation, Algorithmica 32(2), 2002"
    title: Phillips, Stein, Torng and Wein 2002
    locator: the speed and machine augmentation results for EDF and LLF with deadlines (STOC 1997 version)
  - book: isbn:9781584883975
    title: "Kirk Pruhs, Jiri Sgall and Eric Torng, Online scheduling, in Joseph Y.-T. Leung (editor), Handbook of Scheduling, Chapman and Hall/CRC, 2004"
    locator: the chapter on online scheduling (Chapter 15), the parts on jobs with deadlines and real-time scheduling
---

A deadline $\bar d_j$ is the latest time by which job $j$ must complete. Together with the [release time](/release-time/) $r_j$ it gives the job a time window $[r_j, \bar d_j]$. Offline, deadlines appear in [scheduling with release times and deadlines](/scheduling-with-release-times-and-deadlines/). Online, a job with a deadline arrives at its release time, and the algorithm must keep a promise for a job that it saw only now. On one machine with preemption, [EDF](/earliest-deadline-first/) keeps every promise that any schedule can keep; on two or more machines no online rule can do that, and the online questions become how many extra machines, how much extra speed, or how many rejected jobs are needed.

## Definition

Job $j$ has a release time $r_j$, a size $p_j > 0$ and a *deadline* $\bar d_j \ge r_j + p_j$. A schedule *meets* the deadline of job $j$ if $C_j \le \bar d_j$. An instance is *feasible* on $m$ machines if one schedule meets all deadlines. The *laxity* of job $j$ at time $t$ is $\bar d_j - t - q_j(t)$, where $q_j(t)$ is the work of $j$ not yet done: the time that the job can still wait.

**Hard and soft.** The bar marks a hard deadline. A due date $d_j$ without the bar is soft: a schedule may miss it and then pays in the objective, through the lateness $L_j = C_j - d_j$, the tardiness $\max(0, C_j - d_j)$ or the indicator $U_j$ of a late job. This page is about hard deadlines.

**What a deadline means online.** In $\mathrm{online\text{-}time}$, job $j$ and its deadline become known at $r_j$. Since a missed hard deadline is a failure and not a cost, the online question is not a ratio of two costs of the same schedule type. Common forms are:

| question | online objective | page |
|---|---|---|
| keep all deadlines, with as few machines as possible | number of machines | [online machine minimization](/online-machine-minimization/) |
| keep all deadlines, with as little extra speed as possible | the speed factor of the online machines | this page, below |
| keep as many jobs (or as much weight) as possible | throughput | [online throughput maximization](/online-throughput-maximization/), [admission control](/online-admission-control/) |

**One machine.** With preemption on one machine, the rule "run the released job with the earliest deadline" ([EDF](/earliest-deadline-first/)) uses only the released jobs, and it meets all deadlines whenever some schedule does; see [EDF optimality](/edf-optimality/). So $1 \mid \mathrm{online\text{-}time}, \mathrm{pmtn}, r_j, \bar d_j$ needs no more than the offline optimum.

## Examples and non-examples

**Two machines: no online rule is optimal.** Take $m = 2$ with preemption and migration. At time $0$ three jobs arrive:

| job | $r_j$ | $p_j$ | $\bar d_j$ |
|---|---|---|---|
| $x$ | 0 | 1 | 2 |
| $y$ | 0 | 1 | 2 |
| $z$ | 0 | 2 | 4 |

At time $1$ the adversary looks at the work done so far. It is at most $2$, because two machines ran for one time unit.

- If $z$ has had less than one unit of work, the adversary releases two jobs with $r = 2$, $p = 2$, $\bar d = 4$. They fill both machines during $[2, 4]$, so $z$ must end by $2$. It still needs more than one unit of work, but a job runs on one machine at a time, so it gets at most one unit during $[1, 2]$.
- If $z$ has had at least one unit, then $x$ and $y$ together have had at most one unit, and the adversary releases two jobs with $r = 1$, $p = 1$, $\bar d = 2$. During $[1, 2]$ both machines are needed for them, so $x$ and $y$ must be done by $1$, which they are not.

Both instances are feasible offline. With the two jobs of size $2$: $z$ runs on one machine during $[0, 2]$, $x$ then $y$ run on the other, and the new jobs run during $[2, 4]$. With the two jobs of size $1$: $x$ and $y$ run during $[0, 1]$, the new jobs during $[1, 2]$, and $z$ during $[2, 4]$. So every online algorithm misses a deadline on a feasible instance on two machines. This is the idea behind the result of Dertouzos and Mok (1989), cited.

**What extra resources buy.** Phillips, Stein, Torng and Wein (2002) show that EDF on $m$ machines of speed $2 - \frac1m$ meets all deadlines of every instance that is feasible on $m$ machines of speed $1$ (cited). With extra machines instead of speed, the question is [online machine minimization](/online-machine-minimization/).

**Non-examples.**

- A due date in the objective $\sum_j U_j$ or $L_{\max}$ is not a hard deadline: a late job is allowed and costs something.
- A deadline is not a release time: it bounds the completion, not the start.
- The relative deadline of a periodic task in [real-time scheduling](/real-time-scheduling/) is measured from each release of the task; each release then gives one job with an absolute deadline as above.

## Related definitions

- [Release time](/release-time/): the other end of the window.
- [Earliest deadline first](/earliest-deadline-first/), [EDF optimality](/edf-optimality/) and [least laxity first](/least-laxity-first/): the classical rules.
- [Online machine minimization](/online-machine-minimization/): how many machines an online algorithm needs.
- [Online throughput maximization](/online-throughput-maximization/) and [online admission control](/online-admission-control/): when jobs may be dropped.
- [Scheduling with release times and deadlines](/scheduling-with-release-times-and-deadlines/): the offline view.

## References
