---
tag: SPB6JF
kind: concept
slug: parallel-for
name: Parallel for loop
aliases:
- parallel loop
- forall
area: parallel/parallel-primitives
level: intro
summary: A loop whose independent iterations execute concurrently.
prereqs: [fork-join-model, work-span-model]
see_also: [parallel-map, parallel-reduction, data-parallelism, task-parallelism, fork-join-parallelism, determinacy-race, work-stealing, greedy-scheduling]
sources:
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Chapter 27, Section 27.1, the subsection Parallel loops (the parallel for keyword, its implementation by divide-and-conquer spawning in MAT-VEC-MAIN-LOOP, and the span Θ(lg n) + max iter∞(i)), and the subsection Race conditions (MAT-VEC-WRONG)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 26, Section 26.1 (parallel loops in the fork-join model)
  - book: isbn:9780124159938
    title: Michael McCool, Arch D. Robison and James Reinders, Structured Parallel Programming, Morgan Kaufmann, 2012
    locator: Chapter 4, Map (parallel loops as the map pattern, and the grain of the work), and Chapter 8, Fork-Join (recursive splitting of loops)
---

A parallel for loop is a loop whose iterations may run at the same time, because no iteration depends on another. It is a control construct: it says *which* iterations may overlap, and the runtime decides how they run. In the [fork-join model](/fork-join-model/), a parallel loop over $n$ iterations is compiled into a balanced tree of spawns, so it adds $\Theta(\log n)$ to the span and $\Theta(n)$ to the work. The data operation that a parallel loop most often performs, applying one function to every item, is the [parallel map](/parallel-map/).

## In plain words

A teacher has a pile of 100 tests to mark, and each test can be marked without looking at the others. The teacher can hand the tests out to several helpers and let them work at the same time. A parallel for loop is a way for a program to say the same thing: "these steps do not depend on each other, so do them in any order, or all at once".

The program does not say who does which step. A scheduler hands out the work. To start many helpers quickly, it does not hand out the tests one by one; it splits the pile in half, gives each half to someone who splits it again, and so on.

## The idea

**Meaning.** The loop "for $i \leftarrow 0$ to $n - 1$ in parallel do $B(i)$" means that the $n$ bodies $B(0), \ldots, B(n-1)$ are logically parallel: the program is correct only if every order of running them, and every overlap, gives the same result. This holds when no two iterations access the same memory location with at least one write. If two iterations do, the loop has a [determinacy race](/determinacy-race/) and its result can change from run to run. For example, the loop body $y \leftarrow y + a_i$ races on $y$; the fix is a [reduction](/parallel-reduction/).

**Implementation by divide and conquer.** A fork-join runtime does not spawn $n$ tasks from one loop, because the spawns would then form a chain of length $n$. Instead, it runs the loop as a recursion, as in the procedure MAT-VEC-MAIN-LOOP of CLRS (third edition, Section 27.1):

- if the range $[lo, hi)$ has one iteration, run it;
- otherwise, let $mid = \lfloor (lo + hi)/2 \rfloor$, spawn the loop on $[lo, mid)$, run the loop on $[mid, hi)$, and sync.

The spawns form a balanced binary tree with $n$ leaves, $n - 1$ inner nodes and height $\lceil \lg n \rceil$.

**Cost.** Let $W_i$ and $S_i$ be the work and the span of iteration $i$. Then a parallel loop has

$$
W = \Theta(n) + \sum_{i=0}^{n-1} W_i, \qquad S = \Theta(\log n) + \max_{0 \le i < n} S_i.
$$

The $\Theta(n)$ term is the cost of the spawn tree, which is dominated by the bodies whenever each body does at least constant work. The $\Theta(\log n)$ term is the height of the tree: each path from the root to an iteration passes through $\lceil \lg n \rceil$ spawns. A serial loop has span $\sum_i S_i$ instead of the maximum. CLRS gives this span as $\Theta(\lg n) + \max_i \mathit{iter}_\infty(i)$.

**Nesting.** Parallel loops can be nested. For a doubly nested loop over $n \times m$ iterations with constant-time bodies, the span is $\Theta(\log n + \log m)$, because the two spawn trees are on top of each other. If the inner loop is serial, the span is $\Theta(\log n + m)$.

**Grain size.** One spawn costs far more than one addition. So a runtime, or the programmer, coarsens the loop: below a *grain size* $g$, the range runs as a serial loop. With constant-time bodies, the spawn tree then has about $n/g$ leaves, the span becomes $\Theta(g + \log(n/g))$, and the overhead drops by a factor of about $g$. A good grain keeps the leaf work much larger than a spawn, and keeps $n/g$ much larger than the number of processors so that [work stealing](/work-stealing/) can balance the load.

**Other implementations.** OpenMP divides the iterations of a parallel loop into chunks for a fixed team of threads, either statically, in equal blocks decided before the loop starts, or dynamically, with threads taking the next chunk from a shared counter. GPU programs launch one thread for each iteration, grouped into thread blocks. These change the constant factors and the load balance, but not the meaning of the loop.

## Examples

- **Vector addition.** The loop "for $i$ in parallel: $c_i \leftarrow a_i + b_i$" has work $\Theta(n)$ and span $\Theta(\log n)$.
- **Matrix-vector product.** CLRS computes $y = Ax$ for an $n \times n$ matrix with a parallel loop over the rows and a serial inner loop: $y_i \leftarrow \sum_j a_{ij} x_j$. The work is $\Theta(n^2)$ and the span is $\Theta(\log n) + \Theta(n) = \Theta(n)$, so the parallelism is $\Theta(n)$. Making the inner loop a [parallel reduce](/parallel-reduce/) reduces the span to $\Theta(\log n)$.
- **A race.** CLRS's MAT-VEC-WRONG makes the inner loop parallel with the update $y_i \leftarrow y_i + a_{ij} x_j$. Two iterations of the inner loop then update $y_i$ at the same time, and some updates are lost.
- **Uneven iterations.** If iteration $i$ takes time $i$, the work is $\Theta(n^2)$ and the span is $\Theta(n)$, set by the longest iteration. A static split into $p$ equal blocks gives the last block about $2/p$ of the work instead of $1/p$; dynamic chunks or work stealing fix this.

## Where it is used

Parallel loops are the most common way to write parallel code. OpenMP (`parallel for`), Cilk (`cilk_for`), Threading Building Blocks (`parallel_for`), the parallel algorithms of C++17, Chapel (`forall`) and many other systems provide them. In the analysis of algorithms, CLRS uses `parallel for` as a keyword next to spawn and sync, and most fork-join algorithms in that style, such as parallel merge sort and matrix multiplication, are written with it. A parallel loop that writes $f(i)$ into position $i$ of a new array is a [parallel map](/parallel-map/); a parallel loop whose iterations write to arbitrary positions is a scatter. [Data parallelism](/data-parallelism/) is built on loops of this kind, while [task parallelism](/task-parallelism/) uses spawn and sync on different code.

## References
