---
tag: HNSXTR
kind: theorem
slug: work-law
name: Work law
aliases:
- work lower bound
area: parallel/work-span-models
level: core
summary: On p processors, a computation of work T_1 takes time T_p at least T_1/p, because p processors do at most p units of work per step.
prereqs: [work-and-span]
see_also: [span-law, brent-theorem, greedy-scheduling, speedup, parallel-efficiency, work-efficiency, makespan-lower-bounds]
sources:
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Chapter 27, Section 27.1, the work law, inequality (27.2), and the definitions of speedup and linear speedup that follow it
  - paper: doi:10.1145/324133.324234
    title: "Robert D. Blumofe and Charles E. Leiserson, Scheduling multithreaded computations by work stealing, Journal of the ACM 46(5), 1999"
    locator: the lower bounds T_P >= T_1/P and T_P >= T_infinity on the execution time of a multithreaded computation
  - paper: doi:10.1002/j.1538-7305.1966.tb01709.x
    title: "R. L. Graham, Bounds for certain multiprocessing anomalies, Bell System Technical Journal 45(9), 1966"
    locator: the lower bound of the total processing time divided by the number of processors, used in the proof of the bound 2 - 1/m (pp. 1563-1581 for the paper)
---

The work law says that a computation with work $T_1$ takes time $T_p \ge T_1/p$ on $p$ processors, under any scheduler. It holds because $p$ processors can do at most $p$ units of work in one step, and the whole work must be done. With the [span law](/span-law/) it gives the lower bound $T_p \ge \max(T_1/p, T_\infty)$ of the [work-span model](/work-span-model/).

## Statement

The cost model is the work-span model: a [computation DAG](/computation-dag/) of unit-time strands, run on $p$ identical processors, where each processor runs at most one strand in each time step.

| Symbol | Meaning |
|---|---|
| $n$ | the input size |
| $p$ | the number of processors, $p \ge 1$ |
| $W$, $T_1$ | the work, the number of strands |
| $S$, $D$, $T_\infty$ | the span |
| $T_p$ | the number of steps of a given schedule on $p$ processors |
| $W/S$ | the parallelism |

**Theorem (work law).** Let $G$ be a computation DAG with work $W = T_1$. Each schedule of $G$ on $p$ processors takes

$$T_p \ge \frac{T_1}{p}, \qquad \text{and so} \qquad T_p \ge \left\lceil \frac{T_1}{p} \right\rceil.$$

The bound holds for every schedule, greedy or not, and for every DAG. It uses no property of the edges. The same proof gives the bound for strands of any lengths, with $T_1$ the sum of the lengths, if a processor does at most one unit of work in each unit of time.

## In plain words

Think of a pile of jobs and a team of workers, where each worker can do one job at a time. However the team shares the jobs, in each hour it can finish at most as many jobs as it has workers. So the time it needs is at least the number of jobs divided by the number of workers. The order between the jobs can only make things slower, never faster.

## Proof

Fix a schedule of $G$ on $p$ processors with $T_p$ steps. Let $a_t$ be the number of strands that run in step $t$. Each processor runs at most one strand per step, so $a_t \le p$ for each $t$. Each strand of $G$ runs in exactly one step, so

$$T_1 = W = \sum_{t=1}^{T_p} a_t \le \sum_{t=1}^{T_p} p = p\,T_p.$$

Divide by $p$ to get $T_p \ge T_1/p$. Since $T_p$ is an integer, $T_p \ge \lceil T_1/p \rceil$. $\blacksquare$

For strands of any lengths, let $a_t$ be the units of work done in unit $t$ of time. Again $a_t \le p$, and the sum of all $a_t$ is $T_1$, so the same two lines apply.

## Consequences

- **No superlinear speedup in the model.** The [speedup](/speedup/) is $T_1/T_p$, and the work law gives $T_1/T_p \le p$. So $p$ processors give at most a factor $p$. Speedups above $p$ that are seen on real machines come from effects that the model leaves out, such as more cache in total.
- **Efficiency and cost.** The [parallel efficiency](/parallel-efficiency/) $T_1/(p T_p)$ is at most 1, and the cost $p \cdot T_p$ is at least $T_1$.
- **Work efficiency matters for few processors.** Let $T_{seq}$ be the time of the best sequential algorithm. A parallel algorithm with work $W$ takes at least $W/p$ steps, so it can beat the sequential one only if $W/p < T_{seq}$, that is $p > W/T_{seq}$. An algorithm that does $\lg n$ times too much work needs more than $\lg n$ processors to break even. This is why [work efficiency](/work-efficiency/) comes first when $p$ is small.
- **Together with the span law.** With $T_p \ge T_\infty$, every schedule has $T_p \ge \max(T_1/p, T_\infty)$. The greedy bound $T_p \le T_1/p + T_\infty$ of [Brent's theorem](/brent-theorem/) and of [greedy scheduling](/greedy-scheduling/) is at most twice this lower bound.

## Tightness

The bound is reached for many DAGs, so it cannot be improved in general.

- An antichain of $W$ strands with no edges, with $p$ dividing $W$, runs in exactly $W/p$ steps by running $p$ strands in each step.
- For $p = 1$ each DAG takes exactly $T_1$ steps, since one processor runs the strands in a [topological order](/topological-sort/) with no idle step.
- For a DAG with span $S$ much smaller than $W/p$, a greedy schedule takes at most $W/p + S$ steps, so the work law is tight up to the lower-order term $S$.

The bound can be far from the truth when the span is large. A chain of $W$ strands takes $W$ steps on any number of processors, while the work law gives only $W/p$. The span law covers this case.

## History

The bound is the simplest lower bound in multiprocessor scheduling: the total processing time divided by the number of processors. Graham (1966) used it, with the length of the longest chain, in the proof of his bound for list scheduling (see [makespan lower bounds](/makespan-lower-bounds/)). Blumofe and Leiserson (1999) state it for multithreaded computations as $T_P \ge T_1/P$. CLRS (third edition, 2009, Section 27.1) calls it the work law.

## References
