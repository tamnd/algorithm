---
tag: 62Y3C2
kind: algorithm
slug: response-time-analysis
name: Response-time analysis
aliases:
- worst-case response time analysis
- RTA
area: systems/scheduling
level: advanced
summary: "Compute the worst-case response time of each task under fixed priorities as the least solution of R = C + sum of ceil(R/T_j) C_j, by iteration from R = C. Exact for D at most T."
solves: [real-time-scheduling]
model: word-ram
complexity:
  vars: {n: the number of tasks, r: the largest ratio of a deadline to a period}
  time: {worst: O(n^3 r)}
  space: {extra: O(1)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1986
  people: [Mathai Joseph, Paritosh Pandya]
  note: Joseph and Pandya gave the response time of a task under fixed priorities as the least solution of a recurrence; Audsley, Burns, Richardson, Tindell and Wellings (1993) made the iteration the standard test and added blocking and jitter.
prereqs: [rate-monotonic-scheduling, rate-monotonic-optimality]
see_also: [rate-monotonic-optimality, deadline-monotonic-scheduling, liu-layland-utilization-bound, schedulability-analysis, priority-ceiling-protocol, priority-inheritance-protocol, fixed-priority-scheduling, fixed-point-iteration]
sources:
  - paper: "Mathai Joseph and Paritosh Pandya, Finding response times in a real-time system, The Computer Journal 29(5) (1986), 390-395"
    locator: the response time of a task under preemptive fixed priorities as the least solution of a recurrence
  - paper: "Neil C. Audsley, Alan Burns, Mike F. Richardson, Ken Tindell and Andy J. Wellings, Applying new scheduling theory to static priority pre-emptive scheduling, Software Engineering Journal 8(5) (1993), 284-292"
    locator: the iterative computation of the worst-case response time, with blocking and release jitter
  - paper: doi:10.1145/321738.321743
    title: "C. L. Liu and James W. Layland, Scheduling algorithms for multiprogramming in a hard-real-time environment, Journal of the ACM 20(1) (1973), 46-61"
    locator: the critical instant theorem, which makes the synchronous release the worst case
  - paper: "John P. Lehoczky, Fixed priority scheduling of periodic task sets with arbitrary deadlines, Proceedings of the 11th IEEE Real-Time Systems Symposium, 1990"
    locator: the analysis of a level-i busy period with several jobs of a task, for deadlines after the periods
  - book: isbn:9781461406754
    title: "Giorgio C. Buttazzo, Hard Real-Time Computing Systems: Predictable Scheduling Algorithms and Applications, third edition, Springer, 2011"
    locator: Chapter 4 (response time analysis) and Chapter 7 (blocking terms from resource access protocols)
---

Response-time analysis (RTA) is the exact schedulability test for [fixed-priority](/fixed-priority-scheduling/) scheduling of periodic or sporadic tasks on one processor. For each task it computes the worst-case response time $R_i$, the longest time from a release of a job to its end, as the least solution of $R = C_i + \sum_{j \in \operatorname{hp}(i)} \lceil R / T_j \rceil C_j$, by iteration from $R = C_i$; the task set is schedulable if and only if $R_i \le D_i$ for each task. The test is due to Joseph and Pandya (1986) and to Audsley, Burns, Richardson, Tindell and Wellings (1993). It is exact for deadlines at most the periods, with no release jitter and no blocking; with a blocking term $B_i$ for shared resources it gives a safe upper bound.

## In plain words

Pick one task and imagine its worst day: its job arrives at the same moment as a job of every more important task. Start a guess for when it ends: just its own run time. In that much time, the more important tasks also arrive and take turns, so add their work to the guess. The new guess is longer, so maybe more important jobs arrive in it; add them too. Repeat.

The guess grows until it stops changing, and then it is the true worst wait for this task. If it passes the deadline first, the task can miss. Do this for each task. The answer does not depend on how long the full schedule is, and it is exact: it says "yes" exactly when every deadline is always met.

## The problem

The input is a list of $n$ independent tasks $\tau_i = (C_i, T_i, D_i)$, periodic and synchronous or [sporadic](/sporadic-task-model/), with $D_i \le T_i$, in priority order: $\tau_1$ has the highest priority. Scheduling is preemptive, on one processor, with no overheads. The output is, for each task, its worst-case response time, or the answer that it can miss its deadline. Optionally each task has a blocking term $B_i$: the longest time a job of $\tau_i$ can wait for a job of lower priority, for example for a lock under the [priority ceiling protocol](/priority-ceiling-protocol/).

## The algorithm

Let $\operatorname{hp}(i) = \{1, \ldots, i - 1\}$ and

$$F_i(t) = C_i + B_i + \sum_{j < i} \left\lceil \frac{t}{T_j} \right\rceil C_j .$$

The term $\lceil t / T_j \rceil C_j$ is the work that $\tau_j$ releases in a window of length $t$ that starts with one of its releases. The worst-case response time is the least $t > 0$ with $F_i(t) = t$.

```pseudo id=main
RESPONSE-TIME(τ, i, B)                     ▷ τ in priority order; B: the blocking term
L1  R ← C_i + B
L2  loop
L3      R' ← C_i + B + Σ_{j < i} ⌈R / T_j⌉ C_j
L4      if R' > D_i then return MISS
L5      if R' = R then return R
L6      R ← R'
```

Run it for each $i$; the set is schedulable if no call returns MISS. The iteration only adds work, so the values of $R$ never decrease, and it stops at the least fixed point or above the deadline. With integers or fractions the arithmetic is exact; the ceiling is computed as $-\lfloor -R / T_j \rfloor$, not with floating point.

## Example

Take $\tau_1 = (1, 4, 4)$, $\tau_2 = (2, 6, 6)$ and $\tau_3 = (3, 12, 12)$ in rate-monotonic order, with $U = 5/6$.

- $\tau_1$: $R = 1$, and $F_1(1) = 1$. So $R_1 = 1$.
- $\tau_2$: $R = 2$, then $2 + \lceil 2/4 \rceil \cdot 1 = 3$, then $2 + \lceil 3/4 \rceil = 3$. So $R_2 = 3$.
- $\tau_3$:

| step | $R$ | $\lceil R/4 \rceil \cdot 1$ | $\lceil R/6 \rceil \cdot 2$ | $R' = 3 + \ldots$ |
|---|---|---|---|---|
| 1 | 3 | 1 | 2 | 6 |
| 2 | 6 | 2 | 2 | 7 |
| 3 | 7 | 2 | 4 | 9 |
| 4 | 9 | 3 | 4 | 10 |
| 5 | 10 | 3 | 4 | 10 |

So $R_3 = 10 \le 12$, and the set is schedulable, although $U = 0.833$ is above the [Liu-Layland bound](/liu-layland-utilization-bound/) $0.780$. A simulation of the synchronous release shows the first job of $\tau_3$ ending at time 10.

**A miss.** For $\tau_1 = (2, 5, 5)$ and $\tau_2 = (4, 7, 7)$: $R = 4$, then $4 + 2 = 6$, then $4 + 2 \cdot 2 = 8 > 7$. So $\tau_2$ can miss its deadline; indeed the synchronous release makes it end at 8.

**Blocking.** For $\tau_1 = (1, 4, 4)$ and $\tau_2 = (2, 6, 6)$ with $B_2 = 1$: $R = 3$, then $2 + 1 + \lceil 3/4 \rceil = 4$, then $4$ again, so $R_2 \le 4$. With $B_2 = 3$: $R = 5$, then $2 + 3 + \lceil 5/4 \rceil = 7 > 6$, a possible miss.

## Correctness

The [critical instant theorem](/rate-monotonic-optimality/) shows that, for $D_i \le T_i$ and $B_i = 0$, the worst response time of $\tau_i$ over all legal release patterns is the least $t > 0$ with $F_i(t) \le t$, and the synchronous release reaches it. The iteration starts below this value, never passes it, and increases by at least the smallest $C_j$ in each step, so it reaches it or passes $D_i$. The full proof is below. With $B_i > 0$, the term $B_i$ only adds a delay that the protocol guarantees as an upper bound, so the result is an upper bound.

## Complexity

- **Per task.** Each step that changes $R$ increases at least one count $\lceil R / T_j \rceil$, and each count stays at most $\lceil D_i / T_j \rceil$ while $R \le D_i$. So the loop runs at most $1 + \sum_{j < i} \lceil D_i / T_j \rceil \le 1 + (i - 1)(r + 1)$ times, where $r = \max_{i, j} D_i / T_j$. Each step costs $O(n)$, so a task costs $O(n^2 r)$, and the whole test $O(n^3 r)$.
- **Pseudo-polynomial.** The bound depends on the ratio of the periods, not on the hyperperiod, but it is not polynomial in the size of the input. No polynomial algorithm is expected: computing the worst-case response time is NP-hard (Eisenbrand and Rothvoß 2008; see [schedulability analysis](/schedulability-analysis/)).
- **In practice.** The number of steps is usually small, and the test is much faster than a simulation of the [hyperperiod](/hyperperiod/).

## Properties

- **Exact** for constrained deadlines, no jitter and no blocking: it accepts a task set if and only if the priority order meets all deadlines for each legal release pattern.
- **Monotone.** Larger $C_j$ or smaller $T_j$ never decrease $R_i$. So the test is safe when $C_j$ is an upper bound on the run time.
- **One task at a time.** $R_i$ depends only on the tasks of higher priority as a set, not on their order. Audsley's optimal priority assignment uses this.
- **Any fixed priority order.** It works for [rate-monotonic](/rate-monotonic-scheduling/), [deadline-monotonic](/deadline-monotonic-scheduling/) or any other order.
- **Values, not only yes or no.** The response times give the slack of each task, for example for a sensitivity analysis of the $C_i$.

## Variants and improvements

- **Blocking.** With a resource access protocol such as the [priority inheritance protocol](/priority-inheritance-protocol/) or the [priority ceiling protocol](/priority-ceiling-protocol/), $B_i$ is the protocol's bound on the time that a job of $\tau_i$ waits for jobs of lower priority. The result is then an upper bound.
- **Release jitter.** If the job of $\tau_j$ can be released up to $J_j$ after its arrival, the interference term becomes $\lceil (R + J_j) / T_j \rceil C_j$, and the response time is $R_i + J_i$ (Audsley et al. 1993).
- **Arbitrary deadlines.** If $D_i > T_i$, several jobs of $\tau_i$ can be pending at once, and the first job is not always the worst. The analysis then looks at each job $q = 0, 1, \ldots$ of the busy period that starts at the synchronous release, until a job ends before the next release of $\tau_i$ (Lehoczky 1990). The page on [deadline-monotonic scheduling](/deadline-monotonic-scheduling/) has an implementation.
- **Time demand at fixed points.** Lehoczky, Sha and Ding (1989) test whether $W_i(t) \le t$ for some $t$ among the points $k T_j \le D_i$ and $D_i$, where $W_i(t) = C_i + \sum_{j<i} \lceil t / T_j \rceil C_j$; this is equivalent to RTA and gives the yes or no answer without the values.
- **Faster bounds.** Linear upper bounds on the response time give a polynomial sufficient test that is often close to exact.

## When to use it

Use RTA for each fixed-priority system that has to be certified, and whenever the [Liu-Layland bound](/liu-layland-utilization-bound/) rejects a set. It handles constrained deadlines, any priority order, blocking and jitter in one framework, and it is fast enough to run inside an optimizer that searches over priority orders or task parameters.

## Pitfalls

- **Starting too high.** The iteration must start from a value at most the least fixed point, for example $C_i + B_i$, or $R_{i-1} + C_i$ when $\tau_{i-1}$ has the next higher priority and the same blocking. From a larger start it can stop at a larger fixed point, which is safe but not exact.
- **Floating point.** With floating point, $\lceil R / T_j \rceil$ can be one too large or too small when $R$ is a multiple of $T_j$. Use integers, fractions or exact ceiling division.
- **Deadlines after the periods.** The simple recurrence is not exact if $R_i > T_i$, because an earlier job of the same task can delay the job; use the busy period version.
- **Offsets.** With fixed offsets the synchronous release may never happen, and the test is only sufficient.
- **Blocking is not exact.** A result with $B_i > 0$ that exceeds $D_i$ does not prove that a deadline is missed.

## Implementations

## History

Joseph and Pandya (1986) gave the response time of a task under fixed priorities as the least solution of a recurrence. Lehoczky, Sha and Ding (1989) gave an equivalent exact test at a finite set of points, and Lehoczky (1990) treated deadlines after the periods. Audsley, Burns, Richardson, Tindell and Wellings (1993) presented the iterative form with blocking and release jitter, which became the standard test for fixed-priority systems.

## References
