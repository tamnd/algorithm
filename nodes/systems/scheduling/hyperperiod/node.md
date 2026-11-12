---
tag: A9XCXA
kind: definition
slug: hyperperiod
name: Hyperperiod
aliases:
- least common multiple of periods
area: systems/scheduling
level: intro
summary: "The least common multiple H of the task periods. The release pattern of a periodic task system repeats every H time units, so one hyperperiod is enough to simulate."
prereqs: [periodic-task-model, least-common-multiple]
see_also: [cyclic-executive, schedulability-analysis, earliest-deadline-first, rate-monotonic-scheduling, utilization, sporadic-task-model]
sources:
  - book: isbn:9780130996510
    title: Jane W. S. Liu, Real-Time Systems, Prentice Hall, 2000
    locator: Chapter 3 (the hyperperiod of a periodic task system) and Chapter 5 (clock-driven scheduling, where the major cycle is the hyperperiod)
  - paper: "Joseph Y.-T. Leung and M. L. Merrill, A note on preemptive scheduling of periodic, real-time tasks, Information Processing Letters 11(3) (1980), 115-118"
    locator: the feasibility interval [0, s + 2H] for periodic tasks with offsets
  - book: isbn:9781461406754
    title: "Giorgio C. Buttazzo, Hard Real-Time Computing Systems: Predictable Scheduling Algorithms and Applications, third edition, Springer, 2011"
    locator: Chapter 4, Periodic Task Scheduling (the hyperperiod and the timeline scheduling approach)
---

The hyperperiod of a [periodic task system](/periodic-task-model/) is the [least common multiple](/least-common-multiple/) $H = \operatorname{lcm}(T_1, \ldots, T_n)$ of its periods. All tasks release a job together at time 0 in a synchronous system, and again at each multiple of $H$, so the release pattern repeats every $H$ time units. For this reason a simulation of one hyperperiod (or, with offsets, of a slightly longer window) decides whether a schedule meets all deadlines, and a static table for one hyperperiod can run forever.

## Definition

Let $\tau = \{\tau_1, \ldots, \tau_n\}$ be a periodic task system with positive integer periods $T_1, \ldots, T_n$. Its **hyperperiod** is

$$H = \operatorname{lcm}(T_1, \ldots, T_n),$$

the least positive integer that each $T_i$ divides. If the periods are rational, write them as integers in a common unit of time (for example, in microseconds) and take the lcm there.

In one hyperperiod, task $\tau_i$ releases exactly $H / T_i$ jobs, so the window $[0, H)$ holds

$$\sum_{i=1}^n \frac{H}{T_i}$$

jobs, with total work $\sum_i (H / T_i) C_i = HU$, where $U$ is the [utilization](/utilization/).

**Repetition.** Let the system be synchronous, with constrained deadlines $D_i \le T_i$, and let a scheduling rule decide only from the pending jobs, their release times and their deadlines, in a way that does not change when all times shift by $H$. Fixed priorities and [earliest deadline first](/earliest-deadline-first/) are such rules. If this rule meets each deadline in $(0, H]$, then its schedule on $[H, 2H)$ is the schedule on $[0, H)$ shifted by $H$, and so on for each later hyperperiod.

*Proof.* A job released in $[0, H)$ has its deadline at most $H - T_i + D_i \le H$. All these deadlines are met, so no work is pending at time $H$. At time $H$ the system is in the same state as at time 0: no pending work, and the same future releases, shifted by $H$. The rule makes the same choices, shifted by $H$. $\square$

So the check of the deadlines in $(0, H]$ decides whether the rule meets all deadlines. If a deadline is missed, the system fails at that point; if none is missed, the schedule repeats and no deadline is ever missed.

**Offsets.** If the task $\tau_i$ has an offset $O_i$, let $s = \max_i O_i$. The release pattern repeats with period $H$ from time $s$ on, but the pending work at time $s + H$ may not be 0. Leung and Merrill (1980) showed that, for constrained deadlines, the system is feasible if and only if [EDF](/earliest-deadline-first/) meets each deadline in $[0, s + 2H]$. The window $[0, s + H]$ is not always enough (see the second example).

## Examples and non-examples

**Two periods.** With periods 5 and 7, $H = 35$. The window $[0, 35)$ holds $7 + 5 = 12$ jobs.

**A small hyperperiod.** With periods 10, 20 and 40, each period divides the next one (the periods are *harmonic*), so $H = 40$, the largest period. The window holds $4 + 2 + 1 = 7$ jobs. Harmonic periods are popular in practice for this reason.

**Common factors.** With periods 4, 6 and 10, $H = 60$, and the window holds $15 + 10 + 6 = 31$ jobs.

**A large hyperperiod.** With the periods 3, 5, 7, 11 and 13, which are distinct primes, $H$ is their product, $15015$. The window holds $5005 + 3003 + 2145 + 1365 + 1155 = 12673$ jobs, for 5 tasks. In general $H$ can grow exponentially in the number of tasks, so a simulation over one hyperperiod is not a polynomial-time test.

**An offset that needs the longer window.** Write tasks as $(O, C, T, D)$. Take $\tau_1 = (2, 1, 2, 2)$ and $\tau_2 = (0, 3, 6, 4)$, so $H = 6$, $s = 2$ and $U = 1$. Under EDF:

| interval | job | note |
|---|---|---|
| $[0, 2)$ | $\tau_2$, released 0, deadline 4 | |
| $[2, 3)$ | $\tau_2$, released 0, deadline 4 | the deadline 4 ties with $\tau_1$; the earlier release wins |
| $[3, 4)$ | $\tau_1$, released 2, deadline 4 | |
| $[4, 5)$ | $\tau_1$, released 4, deadline 6 | |
| $[5, 6)$ | idle | |
| $[6, 7)$ | $\tau_1$, released 6, deadline 8 | |
| $[7, 10)$ | $\tau_2$, released 6, deadline 10 | at 8 the deadline 10 ties; the earlier release wins |
| $[10, 11)$ | $\tau_1$, released 8, deadline 10 | it misses its deadline |

Each deadline up to $s + H = 8$ is met, but the job of $\tau_1$ released at 8 misses its deadline 10, which is inside $[0, s + 2H] = [0, 14]$. No schedule can do better: the jobs with release and deadline in $[6, 10]$ need $1 + 1 + 3 = 5$ units of work in 4 units of time.

**Non-examples.**

- Periods 1 and $\sqrt 2$ have no common multiple, because their ratio is irrational. The release pattern never repeats, and the system has no hyperperiod.
- A [sporadic task](/sporadic-task-model/) has no fixed release times, so a sporadic system has no repeating pattern. For the analysis on one processor, the synchronous periodic pattern with the same parameters is the worst case, and its hyperperiod then bounds the interval to check.
- With a deadline after the period ($D_i > T_i$), a job released just before $H$ can still run after $H$, so the processor may have pending work at $H$ and the schedule may not repeat from $H$. Then the analysis uses the length of the busy period that starts at time 0.

## Related definitions

- [Least common multiple](/least-common-multiple/): the number-theoretic operation behind $H$; it can be computed from $\operatorname{lcm}(a, b) = ab / \gcd(a, b)$, one period at a time.
- [Cyclic executive](/cyclic-executive/): a static schedule table whose *major cycle* is the hyperperiod, cut into equal *frames*.
- [Utilization](/utilization/): $HU$ is the busy time in each hyperperiod of a schedule that meets all deadlines, and $H(1 - U)$ is the idle time.
- *Feasibility interval*: a finite window such that a check of the deadlines in it decides schedulability. For synchronous tasks with $D_i \le T_i$ it is $[0, H]$; with offsets, $[0, s + 2H]$.
- [Schedulability analysis](/schedulability-analysis/): the tests that avoid a simulation of a long hyperperiod.

## References
