---
tag: JAYC4Q
kind: definition
slug: release-time
name: Release time
aliases:
- arrival time
- release date
- r_j
area: online-and-streaming/online-scheduling
level: intro
summary: "The earliest time at which a job may start; in online scheduling over time it is also the time when the job becomes known, so the algorithm must decide without knowing later arrivals."
prereqs: [graham-three-field-notation, online-algorithm]
see_also: [deadline, graham-three-field-notation, clairvoyant-scheduling, scheduling-with-release-dates, scheduling-with-release-times-and-deadlines, flow-time, online-total-completion-time, online-flow-time-minimization]
sources:
  - book: isbn:9781584883975
    title: "Kirk Pruhs, Jiri Sgall and Eric Torng, Online scheduling, in Joseph Y.-T. Leung (editor), Handbook of Scheduling, Chapman and Hall/CRC, 2004"
    locator: the chapter on online scheduling (Chapter 15), the paradigm of jobs arriving over time and the section on makespan over time
  - paper: "David B. Shmoys, Joel Wein and David P. Williamson, Scheduling parallel machines on-line, SIAM Journal on Computing 24(6), 1995"
    title: Shmoys, Wein and Williamson 1995
    locator: the reduction that turns an offline rho-approximation for makespan with release dates into a 2 rho-competitive algorithm over time
  - paper: "Bo Chen and Arjen P. A. Vestjens, Scheduling on identical machines: how good is LPT in an on-line setting?, Operations Research Letters 21(4), 1997"
    title: Chen and Vestjens 1997
    locator: the online LPT rule over time and its ratio 3/2
  - paper: "J. A. Hoogeveen and A. P. A. Vestjens, Optimal on-line algorithms for single-machine scheduling, IPCO 1996, LNCS 1084, Springer, 1996"
    title: Hoogeveen and Vestjens 1996
    locator: the lower bound 2 for nonpreemptive total completion time on one machine over time, and the delayed SPT rule that reaches it
---

The release time $r_j$ of job $j$ is the earliest time at which the job may start. Offline it is a constraint in the field $\beta$, written $r_j$; see [scheduling with release dates](/scheduling-with-release-dates/). In the online paradigm $\mathrm{online\text{-}time}$ of the [three-field notation](/graham-three-field-notation/), the release time is also the moment when the job becomes known, so at time $t$ the algorithm knows only the jobs with $r_j \le t$. This page defines the release time and shows how the online meaning changes which rules are good, for example why it can pay to leave a machine idle.

## Definition

Each job $j$ has a *release time* (or *release date*) $r_j \ge 0$. A schedule is feasible for the release times if every job starts at a time $S_j \ge r_j$; with preemption, no part of job $j$ runs before $r_j$. The completion time of job $j$ is $C_j$, and its [flow time](/flow-time/) is $F_j = C_j - r_j$, the time that the job spends in the system.

**Offline and online meaning.** The same number has two roles.

| setting | what $r_j$ means | what the algorithm knows at time $t$ |
|---|---|---|
| offline, $\alpha \mid r_j \mid \gamma$ | a constraint: $S_j \ge r_j$ | all jobs, with all their data |
| $\mathrm{online\text{-}list}$ with $r_j$ | a constraint, given with the job when the job is shown in the list | the jobs shown so far; the time of the schedule is not the time of the list |
| $\mathrm{online\text{-}time}$ | a constraint, and the arrival time of the job | only the jobs with $r_j \le t$, and their data |
| $\mathrm{online\text{-}time\text{-}nclv}$ | as $\mathrm{online\text{-}time}$ | the jobs with $r_j \le t$, but not their sizes until they end |

In $\mathrm{online\text{-}time}$ the decisions are made in time order. At each time $t$ the algorithm chooses which released jobs run at $t$, and it may let a machine idle while a job waits. The [offline optimum](/offline-optimum/) knows all release times in advance and obeys the same constraint $S_j \ge r_j$.

**Never-idle rules.** A rule is *greedy* or *busy* if it never lets a machine idle while a released job waits to start. For makespan, greedy rules are good:

- On one machine, $1 \mid \mathrm{online\text{-}time} \mid C_{\max}$, every greedy rule is optimal. Let $t_0$ be the last time at which the machine is idle and a job is released. All jobs that run after $t_0$ have $r_j \ge t_0$, and the machine has no gap after $t_0$, so $\mathrm{ALG} = t_0 + \sum_{j :\, r_j \ge t_0} p_j$. No schedule can start these jobs before $t_0$, so $\mathrm{OPT} \ge \mathrm{ALG}$.
- On $m$ identical machines, every greedy rule is strictly 2-competitive for makespan, even without the sizes. Let job $l$ end last, at $C_l = S_l + p_l$. During $[r_l, S_l)$ job $l$ waits, so all $m$ machines are busy with other jobs, and $m (S_l - r_l) \le \sum_{j \ne l} p_j$. Then $\mathrm{ALG} \le (r_l + p_l) + \frac1m \sum_j p_j \le \mathrm{OPT} + \mathrm{OPT}$.

The best known deterministic ratio for $P \mid \mathrm{online\text{-}time} \mid C_{\max}$ is $\frac32$, reached by the greedy rule that starts the longest waiting job (Chen and Vestjens 1997, cited). Shmoys, Wein and Williamson (1995) give a general method: run an offline $\rho$-approximation on the jobs released so far, wait until the batch ends, and repeat; this gives ratio $2\rho$ (cited).

## Examples and non-examples

**Idle time can pay.** Take one machine without preemption and the objective $\sum_j C_j$. At time $0$ one job of size $1$ is released. A greedy rule starts it at once, and it ends at $1$. At time $\varepsilon$, the adversary releases $k$ jobs of size $0$. They must wait until $1$, so the greedy cost is $1 + k \cdot 1 = 1 + k$. The optimum waits until $\varepsilon$, runs the $k$ jobs at once, then the long job: its cost is $k\varepsilon + (1 + \varepsilon)$. As $\varepsilon \to 0$ the ratio tends to $1 + k$, which grows without bound. An online rule must sometimes wait. For this class every deterministic rule has ratio at least $2$, and a rule that delays long jobs reaches $2$ (Hoogeveen and Vestjens 1996, cited); see [online total completion time](/online-total-completion-time/).

**Release time and the list.** In $P \mid \mathrm{online\text{-}list}, r_j \mid C_{\max}$, the list may show a job with $r_j = 100$ before a job with $r_j = 0$. The algorithm assigns each job a machine and a start time $S_j \ge r_j$ when it sees it. The release time is data, not the clock.

**Non-examples.**

- A release time is not a [deadline](/deadline/): $r_j$ bounds the start from below, while a deadline $\bar d_j$ bounds the completion from above.
- The time when a job becomes known need not equal its release time. In models with lookahead, or in the $\mathrm{online\text{-}list}$ example above, the job is known before it may start. The definition of $\mathrm{online\text{-}time}$ makes the two times equal.
- Flow time is not a release time: $F_j = C_j - r_j$ is measured from the release time, and objectives based on it are on the [flow time](/flow-time/) and [online flow time minimization](/online-flow-time-minimization/) pages.

## Related definitions

- [Scheduling with release dates](/scheduling-with-release-dates/) and [scheduling with release times and deadlines](/scheduling-with-release-times-and-deadlines/): the offline problems.
- [Deadline](/deadline/): the upper end of the time window of a job.
- [Clairvoyant scheduling](/clairvoyant-scheduling/): whether $p_j$ is known at $r_j$.
- [Graham's three-field notation](/graham-three-field-notation/): the entries $\mathrm{online\text{-}list}$ and $\mathrm{online\text{-}time}$.
- [Flow time](/flow-time/) and [online total completion time](/online-total-completion-time/): objectives measured from the release times.

## References
