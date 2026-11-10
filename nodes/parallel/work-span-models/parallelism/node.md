---
tag: Y4BWC5
kind: definition
slug: parallelism
name: Parallelism
aliases:
- average parallelism
area: parallel/work-span-models
level: core
summary: The ratio T_1/T_infinity of the work to the span of a computation; the largest speedup that any number of processors can give it.
prereqs: [work-and-span, span-law]
see_also: [speedup, parallel-slackness, critical-path, brent-theorem, amdahls-law, work-efficiency, hillis-steele-scan, blelloch-scan]
sources:
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Chapter 27, Section 27.1, the part on parallelism (the ratio T_1/T_infinity, its three readings, and the limit on perfect linear speedup), and the analysis of P-FIB
  - paper: doi:10.1109/12.21127
    title: "Derek L. Eager, John Zahorjan and Edward D. Lazowska, Speedup versus efficiency in parallel systems, IEEE Transactions on Computers 38(3), 1989"
    locator: the average parallelism of a computation and the bounds on speedup in terms of it
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 26, Section 26.1 (work, span and parallelism)
---

The parallelism of a computation is the ratio $T_1/T_\infty = W/S$ of its work to its span. It is the largest [speedup](/speedup/) that the computation can get on any number of processors, and it is the average number of strands per step when every strand runs as soon as it is ready. When the number of processors $p$ is larger than the parallelism, perfect linear speedup is not possible.

## Definition

The cost model is the [work-span model](/work-span-model/), with a [computation DAG](/computation-dag/) of unit-time strands.

| Symbol | Meaning |
|---|---|
| $n$ | the input size |
| $p$ | the number of processors |
| $W$, $T_1$ | the work |
| $S$, $D$, $T_\infty$ | the span |
| $T_p$ | the time on $p$ processors |
| $W/S$ | the parallelism |

The **parallelism** of a computation with work $T_1$ and span $T_\infty$ is

$$\frac{T_1}{T_\infty} = \frac{W}{S}.$$

It has three readings, and each one is a fact proved here.

- **Average work per step.** With unbounded processors, run each strand at the first step where it is ready. This takes exactly $S$ steps (see [work and span](/work-and-span/)) and runs all $W$ strands, so on average $W/S$ strands run in each step. This is why Eager, Zahorjan and Lazowska (1989) call it the average parallelism.
- **The largest speedup.** For every $p$ and every schedule, the [span law](/span-law/) gives $T_p \ge T_\infty$, so the speedup is $T_1/T_p \le T_1/T_\infty$. With unbounded processors, the schedule above reaches $T_p = T_\infty$, so the bound is reached. So the parallelism is exactly the largest speedup over all $p$ and all schedules.
- **The limit for perfect linear speedup.** If $p > T_1/T_\infty$, then $T_1/T_p \le T_1/T_\infty < p$, so the speedup is less than $p$. Perfect linear speedup $T_1/T_p = p$ needs $p \le T_1/T_\infty$.

The ratio of the parallelism to $p$ is the [parallel slackness](/parallel-slackness/). By [Brent's theorem](/brent-theorem/), a greedy scheduler gets near perfect linear speedup when the slackness is well above 1.

## Examples and non-examples

The table gives the work, span and parallelism of some fork-join computations, with the counts of the pages [work and span](/work-and-span/) and [work-span analysis](/work-span-analysis/) (one strand to split, one to join, and one for each leaf). The asymptotic forms are proved on those pages or in CLRS, third edition, Chapter 27.

| computation | $W$ | $S$ | $W/S$ | asymptotic parallelism |
|---|---|---|---|---|
| parallel sum, $n = 2^{20}$ | 3,145,726 | 41 | about 76,725 | $\Theta(n / \log n)$ |
| parallel Fibonacci of 30 | 4,038,805 | 59 | about 68,454 | $\Theta(\phi^n / n)$ |
| merge sort with a serial merge, $n = 2^{20}$ | 23,068,671 | 2,097,171 | about 11.0 | $\Theta(\log n)$ |
| Hillis-Steele scan, $n = 2^{20}$ (additions, rounds) | 19,922,945 | 20 | about 996,147 | $\Theta(n)$ |
| Blelloch scan, $n = 2^{20}$ (additions, levels) | 2,097,150 | 40 | about 52,429 | $\Theta(n / \log n)$ |

- **Merge sort.** With a serial merge, merge sort has parallelism only $\Theta(\log n)$, about 11 for a million items: more than about 11 processors cannot help. With the parallel merge of [parallel merge sort](/parallel-merge-sort/), the parallelism is $\Theta(n / \log^2 n)$ (CLRS, third edition, Section 27.3).
- **High parallelism is not speed.** The [Hillis-Steele scan](/hillis-steele-scan/) has about 19 times the parallelism of the [Blelloch scan](/blelloch-scan/) for $n = 2^{20}$, but it does about 9.5 times as much work. On $p = 8$ processors, the [work law](/work-law/) gives it at least 2,490,369 steps, more than the 1,048,575 additions of a serial loop. The parallelism says how many processors a computation can use, not how fast it runs on few of them (see [work efficiency](/work-efficiency/)).
- **Non-example: the width of the DAG.** The largest number of strands that could run at one time is not the parallelism. A chain of $k$ strands followed by $k$ strands that all depend on the end of the chain has $k$ strands side by side, but $W = 2k$ and $S = k + 1$, so the parallelism is below 2. No number of processors gives a speedup of 2 or more.
- **Non-example: the number of processors.** The parallelism is a property of the computation alone. It does not depend on $p$ or on the scheduler.

## Related definitions

- The [speedup](/speedup/) $T_1/T_p$ on $p$ processors is at most $\min(p, T_1/T_\infty)$, by the work law and the span law.
- The [parallel slackness](/parallel-slackness/) is $(T_1/T_\infty)/p$.
- A [critical path](/critical-path/) has $T_\infty$ strands, so the parallelism is the work per strand of a critical path.
- In [Amdahl's law](/amdahls-law/), a serial fraction $f$ of the work gives $T_\infty \ge f T_1$, so the parallelism is at most $1/f$.
- In terms of the parallelism $A$, a greedy schedule has speedup at least $pA/(A + p - 1)$ (see [greedy scheduling](/greedy-scheduling/)).

## References
