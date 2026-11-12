---
tag: ZZVKP5
kind: algorithm
slug: yds-algorithm
name: Yao-Demers-Shenker algorithm
aliases:
- YDS
area: systems/scheduling
level: research
summary: The optimal offline algorithm for speed scaling with deadlines. It runs the densest interval of work at its density by EDF, removes that interval, compresses time and repeats.
solves: [speed-scaling]
model: real-ram
complexity:
  vars: {n: the number of jobs}
  time: {worst: O(n^3)}
  space: {extra: O(n)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1995
  people: [Frances Yao, Alan Demers, Scott Shenker]
  note: Yao, Demers and Shenker defined the speed scaling model and gave this algorithm, with its proof of optimality and the online algorithm AVR, at FOCS 1995.
prereqs: [speed-scaling, earliest-deadline-first]
see_also: [online-speed-scaling, avr, optimal-available, bkp-speed-scaling, edf-optimality, convex-function, kkt-conditions, deadline]
sources:
  - paper: "F. Frances Yao, Alan J. Demers and Scott Shenker, A Scheduling Model for Reduced CPU Energy, Proceedings of the 36th Annual Symposium on Foundations of Computer Science (FOCS), 1995"
    title: "A Scheduling Model for Reduced CPU Energy"
    locator: pages 374 to 382 (the model, critical intervals, the offline algorithm and its optimality, and the online algorithm AVR)
  - paper: "Nikhil Bansal, Tracy Kimbrel and Kirk Pruhs, Speed Scaling to Manage Energy and Temperature, Journal of the ACM 54(1), 2007"
    title: "Speed Scaling to Manage Energy and Temperature"
    locator: Article 3 (the KKT characterization of the YDS schedule, and the online algorithm BKP)
  - paper: "Susanne Albers, Energy-Efficient Algorithms, Communications of the ACM 53(5), 2010"
    title: "Energy-Efficient Algorithms"
    locator: pages 86 to 96 (the survey section on speed scaling with deadlines, with YDS and the online algorithms)
---

The Yao-Demers-Shenker algorithm (YDS) solves the offline [speed scaling](/speed-scaling/) problem with deadlines. Each job has a release time, a [deadline](/deadline/) and an amount of work, and one processor can run at any speed $s$, at power $s^\alpha$ with $\alpha > 1$. YDS finds a schedule that finishes every job in its window with the least energy. It looks for a *critical interval*, the time interval in which the work that must be done, divided by its length, is largest. The jobs whose windows lie inside it run at exactly that speed, in [earliest deadline first](/earliest-deadline-first/) order. Then YDS removes the interval, shrinks the time line so that the two sides meet, and repeats on the jobs that are left. Yao, Demers and Shenker (1995) proved that the result is optimal for every $\alpha > 1$. It is the benchmark against which online algorithms such as [AVR](/avr/) and [Optimal Available](/optimal-available/) are measured.

## In plain words

A processor can run slow and use little power, or fast and use much more. Running twice as fast takes more than twice the power, so it is best to run as slowly and as evenly as the deadlines allow.

Look at every stretch of time and add up the work of the jobs that must start and finish inside it. The stretch with the most work per unit of time is the busiest. Its jobs must run at least that fast, so run them at exactly that speed.

Then cut that stretch out of the time line and join the two ends. Do the same again with the jobs that are left. Each new stretch is less busy than the one before, so the speeds only go down.

## The problem

There are $n$ jobs. Job $j$ has a release time $r_j$, a deadline $d_j > r_j$ and a work $w_j > 0$. A schedule chooses at each time $t$ a speed $s(t) \ge 0$ and at most one job; if job $j$ runs during a set of times $T_j$, it gets $\int_{T_j} s(t)\,dt$ units of work. Preemption is free. The schedule is feasible if each job gets $w_j$ units of work within $[r_j, d_j]$. The energy is $\int s(t)^\alpha\,dt$ with a constant $\alpha > 1$. The goal is a feasible schedule of minimum energy.

For an interval $I = [z, z']$, let $J(I)$ be the set of jobs with $z \le r_j$ and $d_j \le z'$. The *intensity* of $I$ is

$$g(I) = \frac{\sum_{j \in J(I)} w_j}{z' - z}.$$

Every feasible schedule must do the work of $J(I)$ inside $I$, so it runs at an average speed of at least $g(I)$ there.

## The algorithm

```pseudo id=main
YDS(J)                                     ▷ jobs (r_j, d_j, w_j); times below are compressed times
L1  S ← the empty schedule; the used real time U ← ∅
L2  while J is not empty do
L3      [z, z′] ← an interval of maximum intensity g, with z a release time and z′ a deadline of a job in J
L4      A ← the jobs of J with z ≤ r_j and d_j ≤ z′
L5      T ← the real times outside U whose compressed time is in [z, z′]
L6      run the jobs of A by EDF at speed g during T; add this to S; U ← U ∪ T
L7      J ← J − A; for each job left, map each time t to t if t ≤ z, to z if z < t ≤ z′, and to t − (z′ − z) if t > z′
L8  return S
```

A critical interval can always be taken with its ends at a release time and a deadline, so line L3 tries only those $O(n^2)$ pairs. For a fixed start $z$, the jobs that are released at or after $z$, in order of deadline, give the work of every interval $[z, d]$ by a running sum, so one round takes $O(n^2)$ time after a sort.

Line L7 is the *compression*. A job that overlaps the removed interval loses that part of its window, because the processor is busy at speed $g$ there. Line L5 maps the compressed interval back to real time. It may be a union of pieces with gaps, where earlier rounds already run.

## Example

Three jobs, with $\alpha = 3$.

| job | release | deadline | work | density $w_j / (d_j - r_j)$ |
|---|---|---|---|---|
| 1 | 0 | 2 | 4 | 2 |
| 2 | 0 | 8 | 4 | 1/2 |
| 3 | 4 | 6 | 3 | 3/2 |

**Round 1.** The intensities include $g([0, 2]) = 4/2 = 2$, $g([4, 6]) = 3/2$, $g([0, 6]) = 7/6$ and $g([0, 8]) = 11/8$. The maximum is $[0, 2]$ with $g = 2$, so job 1 runs at speed 2 during $[0, 2]$. Compression removes 2 time units: job 2 gets the window $[0, 6]$ and job 3 the window $[2, 4]$.

**Round 2.** Now $g([2, 4]) = 3/2$ and $g([0, 6]) = 7/6$, so job 3 runs at speed $3/2$. In real time this is $[4, 6]$. After compression, job 2 has the window $[0, 4]$.

**Round 3.** Job 2 has intensity $4/4 = 1$. Its compressed window $[0, 4]$ is the real time $[2, 4] \cup [6, 8]$, so it runs at speed 1 in two pieces.

| time | $[0, 2]$ | $[2, 4]$ | $[4, 6]$ | $[6, 8]$ |
|---|---|---|---|---|
| job | 1 | 2 | 3 | 2 |
| speed | 2 | 1 | 3/2 | 1 |

The energy is $2 \cdot 2^3 + 2 \cdot 1^3 + 2 \cdot (3/2)^3 + 2 \cdot 1^3 = 16 + 2 + 27/4 + 2 = 107/4 = 26.75$. In the form $\sum_j w_j g_j^{\alpha - 1}$ it is $4 \cdot 4 + 4 \cdot 1 + 3 \cdot 9/4$, the same. For comparison, [AVR](/avr/) runs at the sum of the densities of the active jobs, and it uses $191/4 = 47.75$. The tests check every number here with exact fractions.

## Correctness

The proofs are in [proofs/correctness.md](proofs/correctness.md).

1. **Speeds go down.** The speed of each round is at most the speed of the round before. If an interval after compression had a higher intensity, the same interval with the removed one put back would have had a higher intensity than the critical one.
2. **Feasibility.** Inside a critical interval no subinterval has a higher intensity, so the jobs of the round fit at speed $g$, and EDF meets their deadlines, as in [EDF optimality](/edf-optimality/) for jobs with windows.
3. **Optimality.** Let $U_k$ be the real time used by the first $k$ rounds. Every job of these rounds has its window inside $U_k$, so any feasible schedule does at least their work inside $U_k$. Since $s^\alpha$ is a [convex function](/convex-function/), it lies above its tangent at the YDS speed. Summing the tangent bounds with weights $\alpha g_k^{\alpha-1}$ that do not grow with $k$ shows that any feasible schedule uses at least the energy of YDS.

The constant speed in each round is the convexity argument in its simplest form: for a fixed amount of work in a fixed time, a constant speed uses the least energy. The tests compare YDS with a brute force over all speed profiles on a grid of speeds in unit time slots, check the structure on random instances, and check that AVR never uses less energy.

## Complexity

There are at most $n$ rounds, since each round removes at least one job. A round sorts the jobs by deadline and tries $O(n)$ starts, each with a sweep of $O(n)$ jobs, so it takes $O(n^2)$ time; mapping back to real time and the EDF run in the round take $O(n^2)$ time as well. The total is $O(n^3)$ arithmetic operations and $O(n)$ space. Li, Yao and Yao later gave an $O(n^2 \log n)$ algorithm for the same schedule.

## Properties

- **Optimal for every $\alpha > 1$.** The schedule does not depend on $\alpha$. It is optimal for every strictly convex increasing power function of the speed.
- **Each job runs at one speed.** All of the work of job $j$ runs at the speed $g_j$ of its round, so the energy is $\sum_j w_j g_j^{\alpha - 1}$.
- **The peak speed is minimal.** The first speed $g_1$ is the largest intensity of any interval, which is the lowest maximum speed of any feasible schedule.
- **KKT characterization.** Bansal, Kimbrel and Pruhs showed that the YDS schedule is the solution of a convex program, and that YDS can be read as a way to meet its [KKT conditions](/kkt-conditions/).
- **Offline.** YDS needs all jobs in advance. Online, the best possible competitive ratio is above 1, and the analysis of online algorithms compares them with YDS.

## Variants and improvements

- **Online algorithms.** [Online speed scaling](/online-speed-scaling/) learns of each job at its release. AVR runs at the sum of the densities of the active jobs; [Optimal Available](/optimal-available/) runs YDS on the work that is left at each release; [BKP](/bkp-speed-scaling/) uses a different estimate of the needed speed.
- **Bounded speed.** If the speed is at most $s_{\max}$, the schedule is feasible exactly when $g_1 \le s_{\max}$, and then YDS is still optimal.
- **Discrete speeds.** If only some speeds are allowed, run each round at the two allowed speeds next to $g$, with the right split of time. This is optimal for the convex power function.
- **Faster algorithms.** Li, Yao and Yao found the critical intervals in $O(n^2 \log n)$ time in total.

## When to use it

Use YDS to compute the minimum energy for a known set of jobs with deadlines, for example a batch of frames to decode before display times, or as the lower bound when you test an online policy. Real processors have a few discrete speeds and a static power, so the YDS schedule is then a starting point to round, not the final answer.

## Pitfalls

- **Taking any interval.** An interval counts only the jobs whose whole windows lie inside it. Counting jobs that only overlap it gives a wrong, larger intensity.
- **Forgetting to compress.** After a round, the removed interval is busy. A job whose window overlaps it must lose that time, or the next rounds see too much room and pick speeds that are too low.
- **Real versus compressed time.** After a few rounds, one compressed interval can be several pieces in real time. Keep the used real time, and map each new interval back through it.
- **Floating point.** Ties between intervals of equal intensity are common, and rounding can break them in an order that splits a round in two. Use exact fractions or a tolerance.

## Implementations

## History

Yao, Demers and Shenker introduced the speed scaling model at FOCS 1995 to study how a processor that can change its voltage and clock rate should save energy. In the same paper they gave the offline algorithm, now called YDS, proved it optimal, and proposed the online algorithm AVR with a competitive ratio that depends on $\alpha$. Bansal, Kimbrel and Pruhs later gave a proof of optimality by convex programming, and introduced the online algorithm BKP. Li, Yao and Yao gave a faster algorithm for the same schedule. Speed scaling became a main topic of the algorithmic study of energy, surveyed by Albers in 2010.

## References
