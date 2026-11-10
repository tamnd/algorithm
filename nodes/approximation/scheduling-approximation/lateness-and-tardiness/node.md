---
tag: PSVFWJ
kind: definition
slug: lateness-and-tardiness
name: Lateness and tardiness
aliases:
- due date
- tardiness
- lateness
- earliness
- unit penalty
area: approximation/scheduling-approximation
level: intro
summary: With due date d_j and completion time C_j, the lateness is L_j = C_j - d_j, the tardiness is max(0, L_j), the earliness is max(0, -L_j), and the job is late (U_j = 1) when C_j > d_j.
prereqs: [scheduling-notation, makespan]
see_also: [earliest-due-date-first, maximum-lateness-minimization, minimizing-tardy-jobs, weighted-tardy-jobs, total-tardiness-minimization, lawler-algorithm, deadline, scheduling-with-release-dates]
sources:
  - paper: doi:10.1016/S0167-5060(08)70356-X
    title: Ronald L. Graham, Eugene L. Lawler, Jan Karel Lenstra and Alexander H. G. Rinnooy Kan, Optimization and approximation in deterministic sequencing and scheduling, a survey, Annals of Discrete Mathematics 5, 1979
    locator: Section 2 (the job data, the completion time, the lateness, the tardiness and the unit penalty, and the optimality criteria)
  - book: isbn:9783319265780
    title: Michael L. Pinedo, Scheduling, Theory, Algorithms, and Systems, fifth edition
    locator: Chapter 2, Deterministic Models, Preliminaries, Section 2.1 (framework and notation, the objective functions)
  - book: isbn:9783540695158
    title: Peter Brucker, Scheduling Algorithms, fifth edition
    locator: Chapter 1, Classification of Scheduling Problems (job data and optimality criteria)
---

In deterministic scheduling, each job $j$ can have a due date $d_j$, the time by which it should complete. When a schedule makes job $j$ complete at time $C_j$, four numbers measure how well the job meets its due date: the lateness $L_j$, the tardiness $T_j$, the earliness $E_j$ and the unit penalty $U_j$. The objectives $L_{\max}$, $T_{\max}$, $\sum_j U_j$, $\sum_j w_j U_j$, $\sum_j T_j$ and $\sum_j w_j T_j$ in the [three-field notation](/scheduling-notation/) are built from them.

## Definition

Let job $j$ have the due date $d_j \in \mathbb{R}$ and the completion time $C_j$ in a given schedule. Then

$$L_j = C_j - d_j, \qquad T_j = \max(0, L_j), \qquad E_j = \max(0, -L_j), \qquad U_j = \begin{cases} 1 & \text{if } C_j > d_j, \\ 0 & \text{if } C_j \le d_j. \end{cases}$$

- The **lateness** $L_j$ can be negative, zero or positive. A negative value means that the job completes early.
- The **tardiness** $T_j \ge 0$ is the positive part of the lateness. It is zero for every job that is on time.
- The **earliness** $E_j \ge 0$ is the negative part of the lateness.
- The **unit penalty** $U_j$ is 1 when the job is **late** (also called tardy) and 0 when it is **on time**. A job that completes exactly at $d_j$ is on time.

These satisfy $L_j = T_j - E_j$, $|L_j| = T_j + E_j$, $T_j \cdot E_j = 0$, and $U_j = 1$ if and only if $T_j > 0$.

The standard objectives over $n$ jobs, with weights $w_j \ge 0$ where they appear, are

$$L_{\max} = \max_j L_j, \quad T_{\max} = \max_j T_j, \quad \sum_j U_j, \quad \sum_j w_j U_j, \quad \sum_j T_j, \quad \sum_j w_j T_j .$$

A function of the completion times is **regular** if it is nondecreasing in each $C_j$. All six objectives are regular. A regular objective never gains from idle time or from delaying a job, which is why the single-machine algorithms on this site run the jobs back to back from time 0 when all jobs are available at time 0.

## Examples and non-examples

**A worked example.** Five jobs with $p = (3, 2, 1, 4, 2)$ and $d = (5, 4, 9, 10, 3)$ run in the order $0, 1, 2, 3, 4$ from time 0.

| job $j$ | $p_j$ | $d_j$ | $C_j$ | $L_j$ | $T_j$ | $E_j$ | $U_j$ |
|---|---|---|---|---|---|---|---|
| 0 | 3 | 5 | 3 | $-2$ | 0 | 2 | 0 |
| 1 | 2 | 4 | 5 | 1 | 1 | 0 | 1 |
| 2 | 1 | 9 | 6 | $-3$ | 0 | 3 | 0 |
| 3 | 4 | 10 | 10 | 0 | 0 | 0 | 0 |
| 4 | 2 | 3 | 12 | 9 | 9 | 0 | 1 |

So $L_{\max} = T_{\max} = 9$, $\sum_j U_j = 2$, $\sum_j T_j = 10$ and $\sum_j E_j = 5$. Job 3 completes exactly at its due date, so it is on time. The [EDD](/earliest-due-date-first/) order $4, 1, 0, 2, 3$ of the same jobs has $L_{\max} = 2$, which is the optimum.

**$L_{\max}$ and $T_{\max}$ can differ.** If every job is on time, $T_{\max} = 0$ for all such schedules, but $L_{\max}$ is negative and still tells them apart. In general $T_{\max} = \max(0, L_{\max})$, so a schedule that minimizes $L_{\max}$ also minimizes $T_{\max}$, but not the other way round.

**The sum of lateness is not a due date objective.** $\sum_j L_j = \sum_j C_j - \sum_j d_j$, and the second sum does not depend on the schedule. So minimizing $\sum_j L_j$ is the same as minimizing $\sum_j C_j$, which the [SPT rule](/shortest-processing-time-first/) solves. Only the positive part, $\sum_j T_j$, makes the due dates matter, and [it is NP-hard](/total-tardiness-minimization/) on one machine.

**Earliness is not regular.** $E_j$ decreases when $C_j$ grows, so objectives such as $\sum_j (E_j + T_j)$ (just-in-time scheduling) can gain from idle time. The rules for regular objectives, such as running the jobs without gaps, do not apply to them.

**A due date is not a deadline.** A due date may be missed at a cost. A [deadline](/deadline/) $\bar d_j$ is a hard constraint: a schedule with $C_j > \bar d_j$ is not feasible. The question "can all due dates be met?" is the same as "is $T_{\max} = 0$?" and also the same as "is $L_{\max} \le 0$?".

**Lateness is not a ratio measure.** $L_{\max}$ can be zero or negative, so the statement "$L_{\max}$ is within a factor 2 of the optimum" has no meaning in general. Approximation results for $L_{\max}$ use the delivery time form, where all values are positive. See [minimizing maximum lateness](/maximum-lateness-minimization/).

## Related definitions

- **Completion time and flow time.** $C_j$ is the time when job $j$ completes. With a release date $r_j$, the flow time is $F_j = C_j - r_j$. See [flow time minimization](/flow-time-minimization/) and [scheduling with release dates](/scheduling-with-release-dates/).
- **Makespan.** The [makespan](/makespan/) $C_{\max} = \max_j C_j$ is the lateness objective $L_{\max}$ with all $d_j = 0$.
- **Delivery time.** In the delivery form, job $j$ has a delivery time $q_j \ge 0$ after it completes, and the goal is to minimize $\max_j (C_j + q_j)$. With $q_j = K - d_j$ for a constant $K \ge \max_j d_j$, this equals $L_{\max} + K$.
- **Problems built on these measures.** [Maximum lateness](/maximum-lateness-minimization/) and [Lawler's algorithm](/lawler-algorithm/) for $f_{\max}$; [the number of tardy jobs](/minimizing-tardy-jobs/) and [its weighted form](/weighted-tardy-jobs/); [total tardiness](/total-tardiness-minimization/).

## References
