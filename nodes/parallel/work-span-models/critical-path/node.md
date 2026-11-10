---
tag: AF18VA
kind: concept
slug: critical-path
name: Critical path
aliases:
- critical path length
- longest path in a DAG
area: parallel/work-span-models
level: core
summary: A longest path in a computation DAG. Its number of strands is the span S, and no schedule on any number of processors can finish faster than it.
prereqs: [computation-dag, dag-longest-path]
see_also: [span-law, work-and-span, parallelism, greedy-scheduling, critical-path-lower-bound, pert-chart, longest-path-problem, parallel-merge-sort]
sources:
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Chapter 27, Section 27.1, the part on performance measures (the span as the number of vertices on a longest or critical path), and Section 24.2 (critical paths in PERT charts, found in Θ(V + E) time)
  - paper: doi:10.1145/324133.324234
    title: "Robert D. Blumofe and Charles E. Leiserson, Scheduling multithreaded computations by work stealing, Journal of the ACM 46(5), 1999"
    locator: the critical-path length T_infinity of a multithreaded computation and the lower bound it gives
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 26, Section 26.1 (span and critical paths of fork-join computations)
---

A critical path of a [computation DAG](/computation-dag/) is a longest directed path, and its number of strands is the span $S = T_\infty$ of the computation. The strands on it must run one after the other, so no schedule on any number of processors takes fewer than $S$ steps. The only way to finish faster than $S$ is to change the computation so that all its longest paths get shorter.

## In plain words

Some steps of a job must wait for others. Follow one chain of such steps from the start of the job to its end. The longest such chain is the critical path. It sets a floor on the time of the whole job: even with as many workers as you like, the steps of that chain must be done one after the other.

More workers help only while there is work to share. Once there are enough workers, the job takes as long as its longest chain. To go faster than that, you must change the job itself so that its longest chain gets shorter.

## The idea

The cost model is the [work-span model](/work-span-model/), with unit-time strands.

| Symbol | Meaning |
|---|---|
| $n$ | the input size of the program |
| $p$ | the number of processors |
| $W$, $T_1$ | the work, the number of strands |
| $S$, $D$, $T_\infty$ | the span, the number of strands on a critical path |
| $T_p$ | the time on $p$ processors |
| $W/S$ | the parallelism |

**Finding it.** Process the strands in [topological order](/topological-sort/) and let $d(v)$ be the number of strands on a longest path that ends at $v$, so $d(v) = 1 + \max d(u)$ over the predecessors $u$ of $v$. Keep for each $v$ the predecessor that gave the maximum. A strand $z$ with the largest $d(z)$ ends a critical path, and the stored predecessors lead back from $z$ to a source. This is the algorithm for the [longest path in a DAG](/dag-longest-path/), and it takes $\Theta(V + E)$ time (CLRS, third edition, Section 24.2). The page [computation DAG](/computation-dag/) gives it as pseudocode with a proof. In a general graph with cycles, the [longest path problem](/longest-path-problem/) is NP-hard, but a computation DAG has no cycles.

**Why it bounds every schedule.** Let $v_1 \to v_2 \to \cdots \to v_S$ be a critical path. Strand $v_{i+1}$ cannot start before $v_i$ has finished, and each strand takes one step, so $v_i$ finishes at step $i$ or later. So $v_S$ finishes at step $S$ or later, on any number of processors and under any scheduler. This is the [span law](/span-law/), $T_p \ge S$.

**Why only a shorter path helps.** The bound $T_p \ge S$ holds for each $p$, so more processors cannot bring the time below $S$. With unbounded processors, the schedule that runs each strand as soon as it is ready takes exactly $S$ steps, so $S$ is reached (see [work and span](/work-and-span/)). So the best time over all $p$ is exactly $S$, and to finish faster one must change the DAG so that its span drops. Two facts make this precise.

- Shortening or removing strands that are on no critical path does not change $S$. Each critical path keeps its $S$ strands, and no path gets longer.
- Shortening the strands of one critical path lowers $S$ only if no other path is as long. If two critical paths share no strand, shortening one leaves the other, and $S$ does not change. To lower $S$ one must cut every critical path.

**When it matters.** A [greedy scheduler](/greedy-scheduling/) gives $T_p \le W/p + S$. When $p$ is well below the [parallelism](/parallelism/) $W/S$, the term $W/p$ is the larger one, and the work decides the time. When $p$ is near or above $W/S$, the term $S$ is the larger one, and the critical path decides the time. So a critical path is the thing to shorten when there are many processors, and the work is the thing to cut when there are few.

## Examples

**Parallel sum of four numbers.** The DAG has 10 strands: a split, two half splits, four leaves, two half sums and a final sum. Each path from the first split through one half split, one leaf and one half sum to the final sum has 5 strands. So there are four critical paths, one for each leaf, and $S = 5$. A critical path need not be unique.

**Merge sort with a serial merge.** The top merge is a chain of $n$ strands, and it waits for both halves. A critical path goes down through the split strands and then up through one merge chain at each level, with $n/2^j$ strands at level $j$. So $S = \Theta(n + n/2 + n/4 + \cdots) = \Theta(n)$. A faster sort of the halves does not help, since the merges are on every critical path. Replacing the serial merge by a parallel merge shortens each of them to $\Theta(\log^2 n)$ and the span to $\Theta(\log^3 n)$ (see [parallel merge sort](/parallel-merge-sort/)).

**P-FIB.** In P-FIB$(n)$ of CLRS, a critical path goes through the spawned call P-FIB$(n-1)$ at each level, so $S = \Theta(n)$. The DAG of P-FIB$(4)$ has 17 strands and a critical path of 8 strands (CLRS, third edition, Figure 27.2).

**Work off the critical path.** Take a chain of $k$ strands and $pk$ more strands that are independent of everything. The chain is the only critical path, $S = k$, and $W = k + pk$. No schedule on $p$ processors takes fewer than $k$ steps. Making the independent strands cheaper lowers $W$ but leaves $S = k$, so the time stays at least $k$.

## Where it is used

- **Lower bounds on parallel time.** The [span law](/span-law/) and the critical path give the lower bound $T_p \ge S$, which with the [work law](/work-law/) gives $T_p \ge \max(W/p, S)$.
- **Scheduling.** In scheduling with precedence constraints, the length of a longest chain is a lower bound on the makespan (see [critical-path lower bound](/critical-path-lower-bound/)). Schedulers that give priority to strands with long paths below them follow the same idea.
- **Project planning.** In a [PERT chart](/pert-chart/), the critical path is the chain of tasks that sets the length of the project. A delay on it delays the whole project, and a delay elsewhere does not, up to the slack of that task.
- **Algorithm design.** A parallel algorithm with low span, for example a [parallel merge sort](/parallel-merge-sort/), is one whose critical paths are short. Designers find the serial chain that sets the span, such as a serial merge, and replace it.

## References
