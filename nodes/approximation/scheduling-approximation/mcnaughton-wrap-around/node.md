---
tag: FQ9V3K
kind: algorithm
slug: mcnaughton-wrap-around
name: McNaughton's wrap-around rule
aliases:
- wrap-around rule
- McNaughton's algorithm
area: approximation/scheduling-approximation
level: core
summary: Fills machines in sequence, splitting jobs, to get an optimal preemptive schedule on identical machines.
solves: [preemptive-makespan-scheduling]
model: real-ram
complexity:
  vars: {n: the number of jobs, m: the number of machines}
  time: {worst: Θ(n + m), average: Θ(n + m), best: Θ(n + m)}
  space: {extra: Θ(1)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1959
  people: [Robert McNaughton]
  note: McNaughton gave the rule and the optimal value max(sum p_j / m, max p_j) in 1959.
prereqs: [preemptive-makespan-scheduling, makespan-lower-bounds]
see_also: [preemptive-makespan-scheduling, makespan-lower-bounds, preemption, makespan-minimization, list-scheduling, uniform-machine-scheduling, preemptive-scheduling, open-shop-scheduling]
sources:
  - paper: doi:10.1287/mnsc.6.1.1
    title: "R. McNaughton, Scheduling with deadlines and loss functions, Management Science 6(1), 1959"
    locator: the wrap-around construction for identical machines with preemption and its optimal value (pp. 1-12 for the paper)
  - paper: doi:10.1016/S0167-5060(08)70356-X
    title: "R. L. Graham, E. L. Lawler, J. K. Lenstra and A. H. G. Rinnooy Kan, Optimization and approximation in deterministic sequencing and scheduling: a survey, Annals of Discrete Mathematics 5, 1979"
    locator: the section on identical parallel machines with preemption, P|pmtn|Cmax
  - book: isbn:9783319265780
    title: Michael L. Pinedo, Scheduling, Theory, Algorithms, and Systems, fifth edition
    locator: Chapter 5 (parallel machine models, the makespan with preemptions and the wrap-around rule)
  - book: isbn:9783540695158
    title: Peter Brucker, Scheduling Algorithms, fifth edition
    locator: Chapter 5 (parallel machines, the problem P|pmtn|Cmax)
---

McNaughton's wrap-around rule is the exact algorithm for [preemptive makespan scheduling](/preemptive-makespan-scheduling/) on identical machines, $P \mid \mathrm{pmtn} \mid C_{\max}$. It computes $C^* = \max(\frac1m \sum_j p_j, \max_j p_j)$, then fills machine 1 with the jobs in any order up to time $C^*$, wraps the rest of the job that crosses $C^*$ to time $0$ of machine 2, and goes on in the same way. The schedule has makespan $C^*$, which equals the [lower bound](/makespan-lower-bounds/), so it is optimal, and it splits at most $m - 1$ jobs. McNaughton published it in 1959, and it runs in $O(n + m)$ time.

## In plain words

Think of each machine as a strip of paper, all of the same length, and of each job as a piece of tape of its own length. First choose the strip length: long enough for the longest piece of tape, and long enough that all the tape fits on all strips together. Then lay the pieces end to end on the first strip. When a piece reaches the end of the strip, cut it and put the rest at the start of the next strip.

A cut job has its end on one machine and its start on the next. The two parts never run at the same time, because the job is not longer than the strip. Since the strip length is a bound that no schedule can beat, the result is the best possible.

## The problem

The input is a number $m \ge 1$ of identical machines and $n$ jobs with times $p_1, \ldots, p_n \ge 0$. A preemptive schedule can stop a job and go on with it later, on the same or on another machine, at no cost. A machine runs one job at a time, and a job runs on at most one machine at a time. The goal is the smallest [makespan](/makespan/). Here $n$ is the number of jobs and $m$ is the number of machines.

*Ratio convention.* This is a minimization problem, and the rule is exact: $\mathrm{ALG} = \mathrm{OPT}$, so its ratio is $\rho = 1$. The proof compares with the two [lower bounds](/makespan-lower-bounds/) $\mathrm{OPT} \ge \frac1m \sum_j p_j$ and $\mathrm{OPT} \ge \max_j p_j$, which hold for preemptive schedules too.

| symbol | meaning |
|---|---|
| $n$, $m$ | the number of jobs and the number of machines |
| $p_j$ | the processing time of job $j$ |
| $C^*$ | the value $\max(\frac1m \sum_j p_j, \max_j p_j)$ |
| $i$, $t$ | the current machine and the current time on it |
| $r$, $d$ | the rest of the current job and the length of the next piece |

## The algorithm

```pseudo id=main
MCNAUGHTON(p[1 .. n], m)
L1  C* ← max(max_j p[j], (p[1] + ... + p[n]) / m)
L2  i ← 1, t ← 0
L3  for j ← 1 to n do
L4      r ← p[j]
L5      while r > 0 do
L6          d ← min(r, C* − t)
L7          run job j on machine i in the interval [t, t + d)
L8          t ← t + d, r ← r − d
L9          if t = C* then i ← i + 1, t ← 0
L10 return C* and the pieces
```

Each round of the inner loop places one piece. Line L9 moves to the next machine when the current one is full up to $C^*$.

## Example

Take $m = 3$ and $p = (5, 4, 4, 3, 2, 2)$, with total $20$. Line L1 gives $C^* = \max(5, \frac{20}{3}) = \frac{20}{3}$.

| job | $p_j$ | pieces | machine time used after the job |
|---|---|---|---|
| 1 | 5 | $M_1$: $[0, 5)$ | $M_1$ up to $5$ |
| 2 | 4 | $M_1$: $[5, \frac{20}{3})$, $M_2$: $[0, \frac73)$ | $M_1$ full, $M_2$ up to $\frac73$ |
| 3 | 4 | $M_2$: $[\frac73, \frac{19}{3})$ | $M_2$ up to $\frac{19}{3}$ |
| 4 | 3 | $M_2$: $[\frac{19}{3}, \frac{20}{3})$, $M_3$: $[0, \frac83)$ | $M_2$ full, $M_3$ up to $\frac83$ |
| 5 | 2 | $M_3$: $[\frac83, \frac{14}{3})$ | $M_3$ up to $\frac{14}{3}$ |
| 6 | 2 | $M_3$: $[\frac{14}{3}, \frac{20}{3})$ | $M_3$ full |

Jobs 2 and 4 are split. Job 2 runs on $M_2$ in $[0, \frac73)$ and on $M_1$ in $[5, \frac{20}{3})$, and these intervals do not meet. The makespan is $\frac{20}{3}$. Without preemption the best makespan is $7$, for example with $\{5, 2\}$, $\{4, 3\}$ and $\{4, 2\}$.

## Correctness

Line L1 sets $C^*$ to the lower bound, so it is enough to show that the pieces form a feasible preemptive schedule that ends by $C^*$. The loop fills the machines in order, each one from $0$ up to $C^*$ with no gap, and the total time $\sum_j p_j \le m C^*$ fits into $m$ machines. A job crosses the end of a machine at most once, because $p_j \le C^*$. If it is split, its second piece runs on the next machine in $[0, d_2)$ and its first piece in $[t, C^*)$ on the earlier machine, with $d_2 = p_j - (C^* - t) \le t$. So the two pieces do not overlap in time. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

- **Time.** Each round of the inner loop L5 to L9 either ends a job (when $d = r$) or fills a machine (when $d = C^* - t$). There are at most $n$ of the first kind and $m$ of the second, so the loop runs at most $n + m$ times. Line L1 takes $\Theta(n)$. The total is $\Theta(n + m)$ in the [real RAM](/real-ram/) model.
- **Space.** $\Theta(1)$ beyond the output. The output has at most $n + m - 1$ pieces.

## Properties

| claim | statement | status |
|---|---|---|
| optimal | the makespan is $C^* = \max(\frac1m \sum_j p_j, \max_j p_j) = \mathrm{OPT}$ | proved in the correctness proof |
| few preemptions | at most $m - 1$ jobs are split, each into exactly two pieces | proved in the correctness proof |
| any order | the job order at line L3 can be arbitrary | by the proof |
| gap to the nonpreemptive optimum | if $C^* > 0$, the nonpreemptive optimum is less than $2C^*$ | proved in the correctness proof |
| online | no; line L1 needs the total time of all jobs | by the pseudocode |

## Variants and improvements

- **Uniform machines, $Q \mid \mathrm{pmtn} \mid C_{\max}$.** The optimum is the largest of the ratios of the $k$ longest jobs to the $k$ fastest speeds, for $k < m$, and of all jobs to all speeds. Horvath, Lam and Sethi (1977) gave the level algorithm, and Gonzalez and Sahni (1978) a faster method with at most $2(m - 1)$ preemptions. See [preemptive makespan scheduling](/preemptive-makespan-scheduling/).
- **Unrelated machines, $R \mid \mathrm{pmtn} \mid C_{\max}$.** The optimum is the value of a linear program, and the schedule comes from a decomposition of its solution (Lawler and Labetoulle 1978).
- **Deadlines and release dates.** McNaughton's paper also treats deadlines. With release dates and due dates, $P \mid \mathrm{pmtn}, r_j \mid L_{\max}$ is solved through a [maximum flow](/max-flow-problem/) problem.
- **Online preemptive scheduling.** If jobs arrive one by one, an exact answer is impossible. Chen, van Vliet and Woeginger (1995) gave the best deterministic ratio, $1/(1 - (1 - \frac1m)^m)$, which tends to $\frac{e}{e - 1}$.
- **Nonpreemptive rounding.** Moving each split job entirely to one of its two machines gives a nonpreemptive schedule of makespan less than $2C^*$, which is a simple 2-approximation for $P \mid\mid C_{\max}$.

## When to use it

Use the wrap-around rule whenever jobs can be split across machines at no cost, for example for divisible computing work, time sharing, or production that can move between equal lines. It is exact, linear in time, and easy to check by hand. Use its value $C^*$ as the lower bound in the analysis of nonpreemptive algorithms such as [list scheduling](/list-scheduling/). If machines differ in speed, use the methods for $Q$ and $R$ on [preemptive makespan scheduling](/preemptive-makespan-scheduling/).

## Pitfalls

- **Leaving out the largest job at line L1.** With $C^* = \frac1m \sum_j p_j$ only, a job longer than $C^*$ wraps onto itself. For $m = 2$ and $p = (3, 1)$, this gives $C^* = 2$, and job 1 would run on $M_1$ in $[0, 2)$ and on $M_2$ in $[0, 1)$ at the same time.
- **Inexact comparison at line L9.** With floating-point times, $t$ may stop just below $C^*$, and the rule then opens one machine too many or places a piece of length almost $0$. Use exact fractions or integers scaled by $m$.
- **Putting the rest at the end of the next machine at lines L7 and L9.** The rule depends on the rest starting at time $0$ of the next machine. If the rest goes to the end of the next machine instead, its interval can overlap the first piece.
- **Reading the pieces as a nonpreemptive schedule.** The output is feasible only if preemption is allowed. Its value can be much smaller than the nonpreemptive optimum: three unit jobs on two machines give $\frac32$, against $2$.

## Implementations

## History

McNaughton (1959) studied scheduling with deadlines and loss functions and gave the wrap-around construction for identical machines with preemption. The survey of Graham, Lawler, Lenstra and Rinnooy Kan (1979) lists $P \mid \mathrm{pmtn} \mid C_{\max}$ as solved by this rule in $O(n)$ time. Horvath, Lam and Sethi (1977) and Gonzalez and Sahni (1978) extended it to uniform machines, and Lawler and Labetoulle (1978) to unrelated machines by linear programming.

## References
