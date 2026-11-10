---
tag: Y1TYRR
kind: theorem
slug: span-law
name: Span law
aliases:
- span lower bound
- critical-path bound
area: parallel/work-span-models
level: core
summary: On any number p of processors, a computation of span T_infinity takes time T_p at least T_infinity, because the strands of a critical path run one after the other.
prereqs: [work-and-span, critical-path]
see_also: [work-law, parallelism, brent-theorem, greedy-scheduling, speedup, amdahls-law, critical-path-lower-bound]
sources:
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Chapter 27, Section 27.1, the span law, inequality (27.3), and the discussion of parallelism that follows it
  - paper: doi:10.1145/324133.324234
    title: "Robert D. Blumofe and Charles E. Leiserson, Scheduling multithreaded computations by work stealing, Journal of the ACM 46(5), 1999"
    locator: the lower bounds T_P >= T_1/P and T_P >= T_infinity on the execution time of a multithreaded computation
  - paper: doi:10.1002/j.1538-7305.1966.tb01709.x
    title: "R. L. Graham, Bounds for certain multiprocessing anomalies, Bell System Technical Journal 45(9), 1966"
    locator: the chain of tasks that covers the idle time, used in the proof of the bound 2 - 1/m with precedence constraints (pp. 1563-1581 for the paper)
---

The span law says that a computation with span $T_\infty$ takes time $T_p \ge T_\infty$ on $p$ processors, for every $p$ and every scheduler. It holds because the strands of a [critical path](/critical-path/) must run one after the other, one step each. With the [work law](/work-law/) it gives the lower bound $T_p \ge \max(T_1/p, T_\infty)$ of the [work-span model](/work-span-model/).

## Statement

The cost model is the work-span model: a [computation DAG](/computation-dag/) of unit-time strands, run on $p$ identical processors. A strand can start only after all its predecessors have finished, and it runs on one processor for one step.

| Symbol | Meaning |
|---|---|
| $n$ | the input size |
| $p$ | the number of processors, $p \ge 1$ |
| $W$, $T_1$ | the work |
| $S$, $D$, $T_\infty$ | the span, the number of strands on a longest path |
| $T_p$ | the number of steps of a given schedule on $p$ processors |
| $W/S$ | the parallelism |

**Theorem (span law).** Let $G$ be a computation DAG with span $S = T_\infty$. Each schedule of $G$ on any number $p$ of processors takes

$$T_p \ge T_\infty.$$

The bound does not depend on $p$, and it holds for every schedule. For strands of any lengths, with $T_\infty$ the largest total length along a path, the same bound holds, because a strand runs on one processor from start to end.

## In plain words

Some jobs must wait for others: you cannot paint a wall before it is built. Pick the longest chain of jobs where each one waits for the one before it. Those jobs must be done one at a time, in that order, however many workers you have. So the whole project takes at least as long as that chain. Extra workers can help with the other jobs, but not with this chain.

## Proof

Fix a schedule of $G$ on $p$ processors with $T_p$ steps, and let $f(v)$ be the step in which strand $v$ runs. A strand runs only after its predecessors have finished, so $f(u) < f(v)$, that is $f(u) + 1 \le f(v)$, for each edge $u \to v$.

Let $v_1 \to v_2 \to \cdots \to v_S$ be a critical path, a path with $S$ strands. We show $f(v_i) \ge i$ by [induction](/induction/) on $i$. For $i = 1$, $f(v_1) \ge 1$ since steps are numbered from 1. If $f(v_i) \ge i$, then $f(v_{i+1}) \ge f(v_i) + 1 \ge i + 1$ by the edge $v_i \to v_{i+1}$. So $f(v_S) \ge S$, and the schedule has at least $S$ steps: $T_p \ge f(v_S) \ge S = T_\infty$. $\blacksquare$

A second view, as in CLRS: a machine with unbounded processors can run any schedule of a machine with $p$ processors and leave the other processors idle, so $T_p \ge T_\infty$, where $T_\infty$ is the best time with unbounded processors. The page [work and span](/work-and-span/) proves that this best time is exactly the number of strands on a longest path, so the two views agree.

## Consequences

- **The parallelism bounds the speedup.** From $T_p \ge T_\infty$, the [speedup](/speedup/) is $T_1/T_p \le T_1/T_\infty$, the [parallelism](/parallelism/). So no number of processors can give a speedup above $T_1/T_\infty$.
- **No perfect linear speedup beyond the parallelism.** If $p > T_1/T_\infty$, then $T_1/T_p \le T_1/T_\infty < p$, so the speedup is below $p$.
- **More processors stop helping.** The time cannot drop below $T_\infty$ for any $p$. Past a point, the only way to go faster is to change the algorithm so that its span is smaller (see [critical path](/critical-path/)).
- **Amdahl's law as a special case.** If a computation must run a chain of $f T_1$ strands, for a fraction $0 < f \le 1$, then $T_\infty \ge f T_1$, so the speedup is at most $1/f$ on any number of processors. This is the limit in [Amdahl's law](/amdahls-law/).
- **Together with the work law.** Every schedule has $T_p \ge \max(T_1/p, T_\infty) \ge (T_1/p + T_\infty)/2$. A greedy schedule has $T_p \le T_1/p + T_\infty$ ([Brent's theorem](/brent-theorem/), [greedy scheduling](/greedy-scheduling/)), so it is within a factor 2 of the best schedule.

## Tightness

The bound is reached for each DAG when there are enough processors. Run every ready strand at each step. Then each strand $v$ runs at step $d(v)$, the number of strands on a longest path that ends at $v$, and the run takes exactly $T_\infty$ steps (proved on [work and span](/work-and-span/)). This needs at most as many processors as the largest number of strands with the same value $d(v)$, and $p \ge W$ is always enough. For a chain the bound is reached for each $p \ge 1$.

The bound can be far from the truth when $p$ is small. An antichain of $W$ strands has span 1, but it takes $\lceil W/p \rceil$ steps. The work law covers this case.

## History

The length of a longest chain of tasks is the classic lower bound for scheduling with precedence constraints. Graham (1966) used such a chain in the proof of his bound for list scheduling (see [critical-path lower bound](/critical-path-lower-bound/)). Blumofe and Leiserson (1999) state it for multithreaded computations as $T_P \ge T_\infty$. CLRS (third edition, 2009, Section 27.1) calls it the span law.

## References
