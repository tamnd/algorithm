---
tag: YTYZ4Q
kind: definition
slug: work-and-span
name: Work and span
aliases:
- work
- span
- depth
area: parallel/work-span-models
level: core
summary: The two cost measures of a parallel computation DAG. The work W = T_1 is the number of strands, and the span S = T_infinity is the number of strands on a longest path.
prereqs: [work-span-model, computation-dag]
see_also: [work-span-analysis, critical-path, parallelism, work-law, span-law, work-efficiency, parallel-reduce, parallel-merge-sort]
sources:
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Chapter 27, Section 27.1, the part on performance measures (work, span, Figure 27.2 for P-FIB(4)), and Section 27.3 for MERGE-SORT' with a serial merge
  - paper: doi:10.1145/227234.227246
    title: "Guy E. Blelloch, Programming parallel algorithms, Communications of the ACM 39(3), 1996"
    locator: the definitions of work and depth
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 26, Section 26.1 (work and span of fork-join computations)
---

Work and span are the two cost measures of the [work-span model](/work-span-model/). The work $W = T_1$ of a computation is the number of its unit-time strands, and the span $S = T_\infty$ is the number of strands on a longest path of its [computation DAG](/computation-dag/). The work is the time on one processor, and the span is the time on an unbounded number of processors.

## Definition

Let $G = (V, E)$ be the computation DAG of one run of a program, with unit-time strands as vertices. The cost model is the work-span model.

| Symbol | Meaning |
|---|---|
| $n$ | the input size |
| $p$ | the number of processors |
| $W$, $T_1$ | the work |
| $S$, $D$, $T_\infty$ | the span, also called the depth |
| $T_p$ | the time on $p$ processors under a given scheduler |
| $W/S$ | the [parallelism](/parallelism/) |

- The **work** is $W = |V|$, the number of strands.
- The **span** is the largest number of vertices on a directed path of $G$. A path with this many vertices is a [critical path](/critical-path/).

If strand $v$ takes time $t(v)$ instead of one unit, the work is $\sum_{v} t(v)$ and the span is the largest sum of $t(v)$ along a path. A strand of time $k$ is the same as a chain of $k$ unit strands, so the unit case covers the weighted one.

The names $T_1$ and $T_\infty$ are exact, and the two facts below are proved here.

- **$T_1 = W$.** One processor runs one strand per step. It can run the strands in a [topological order](/topological-sort/) with no idle step, and it needs at least $|V|$ steps.
- **$T_\infty = S$.** With unbounded processors, run every ready strand at each step. Let $d(v)$ be the number of vertices on a longest path that ends at $v$. By [induction](/induction/) along a topological order, strand $v$ runs at step $d(v)$: it becomes ready one step after its last predecessor $u$ runs, and $1 + \max_u d(u) = d(v)$. So the run takes $\max_v d(v) = S$ steps. No schedule takes fewer, because the strands of a critical path must run one per step. This is the [span law](/span-law/).

There are three ways to compute the two numbers. For a DAG that is given as a graph, one pass in topological order finds both in linear time (see [computation DAG](/computation-dag/)). For a fork-join program, the composition rules of the [work-span model](/work-span-model/) add the work in each case and add the span in series and take its maximum in parallel. For a recursive algorithm, the rules give recurrences, and the page [work-span analysis](/work-span-analysis/) solves them.

## Examples and non-examples

**Parallel sum.** The sum of $n$ numbers by divide and conquer spawns the two halves and adds the two results after the sync. With one strand to split, one strand to add, and one strand for each leaf,

$$W(n) = W(\lceil n/2 \rceil) + W(\lfloor n/2 \rfloor) + 2, \qquad S(n) = S(\lceil n/2 \rceil) + 2, \qquad W(1) = S(1) = 1.$$

So $W(n) = 3n - 2 = \Theta(n)$ and $S(n) = 2\lceil \lg n \rceil + 1 = \Theta(\log n)$. For $n = 4$ the DAG has 10 strands and a longest path of 5 strands: split, split a half, a leaf, add the half, add the whole. A serial loop over the same numbers is a chain of $n$ strands, so it has $W = S = n$. The two programs have the same work up to a constant factor, but the span drops from $n$ to $\Theta(\log n)$. The general version is [parallel reduce](/parallel-reduce/).

**Merge sort with a serial merge.** Run the two recursive calls of [merge sort](/merge-sort/) in parallel, but merge with the serial merge, a chain of $m$ strands for $m$ items. Each call on $m > 1$ items is one split strand, then the two calls in parallel, then the merge chain:

$$W(n) = W(\lceil n/2 \rceil) + W(\lfloor n/2 \rfloor) + n + 1, \qquad S(n) = S(\lceil n/2 \rceil) + n + 1.$$

For $n = 2^k$, the span is $S(n) = 1 + \sum_{j=1}^{k} (2^j + 1) = 2n + \lg n - 1 = \Theta(n)$, and the work is $W(n) = n \lg n + 2n - 1 = \Theta(n \lg n)$ (by induction on $k$). The span is linear because the top merge alone is a chain of $n$ strands. CLRS (third edition, Section 27.3) finds the same $\Theta(n \lg n)$ work and $\Theta(n)$ span for its MERGE-SORT$'$.

| $n$ | $W$ | $S$ | $W/S$ |
|---|---|---|---|
| 8 | 39 | 18 | 2.2 |
| 16 | 95 | 35 | 2.7 |
| 1024 | 12,287 | 2,057 | 6.0 |
| $2^{20}$ | 23,068,671 | 2,097,171 | 11.0 |

The parallelism $W/S$ grows only like $\lg n$, so this version cannot use many processors. A parallel merge lowers the span to $\Theta(\log^3 n)$ (see [parallel merge sort](/parallel-merge-sort/) and [work-span analysis](/work-span-analysis/)).

**Fibonacci.** The procedure P-FIB of CLRS spawns P-FIB$(n-1)$ and calls P-FIB$(n-2)$. Its DAG for $n = 4$ has $W = 17$ strands and span $S = 8$ (CLRS, third edition, Figure 27.2). In general $W = \Theta(\phi^n)$ with $\phi = (1 + \sqrt{5})/2$, and $S = \Theta(n)$. See [parallel Fibonacci](/parallel-fibonacci/).

**Non-examples.**

- The time $T_p$ on $p$ processors is not a measure of the DAG alone. It depends on the scheduler, and two greedy schedules of one DAG can differ by a factor close to 2 (see [greedy scheduling](/greedy-scheduling/)).
- The depth of the recursion is not the span. Merge sort with a serial merge has recursion depth $\lceil \lg n \rceil$, but its span is $\Theta(n)$.
- The span of a parallel loop is not the span of its slowest iteration. A [parallel for](/parallel-for/) over $n$ iterations spawns them through a tree of depth $\Theta(\log n)$, so its span is $\Theta(\log n)$ plus the largest span of one iteration.
- The work is not the number of useful operations only. The strands that spawn and sync count too, and they change the constant factor.

## Related definitions

- The [parallelism](/parallelism/) is $W/S$, the largest speedup that any number of processors can give.
- A [critical path](/critical-path/) is a path with $S$ strands.
- The [work law](/work-law/) and the [span law](/span-law/) give $T_p \ge \max(W/p, S)$.
- The [speedup](/speedup/) is $T_1/T_p$ and the [parallel efficiency](/parallel-efficiency/) is $T_1/(p T_p)$.
- An algorithm is [work-efficient](/work-efficiency/) when $W = O(T_{seq})$ for the best sequential time $T_{seq}$.
- Blelloch calls the span the *depth*. The size and the depth of a [Boolean circuit](/boolean-circuit/) are the circuit analogues of the work and the span.

## References
