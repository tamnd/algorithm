---
tag: 7HB9EH
kind: problem
slug: parallel-reduction
name: Reduction
aliases:
- accumulate
- fold
area: parallel/parallel-primitives
level: intro
summary: Combine all elements of a sequence with an associative operator.
prereqs: [parallel-reduce, associative-operator]
see_also: [monoid, all-prefix-sums, determinacy-race, pairwise-summation, histogram-computation, mapreduce-model, combining-tree, crcw-pram]
sources:
  - paper: doi:10.1145/1583991.1584017
    title: Matteo Frigo, Pablo Halpern, Charles E. Leiserson and Stephen Lewin-Berlin, Reducers and other Cilk++ hyperobjects, Proceedings of the 21st ACM Symposium on Parallelism in Algorithms and Architectures (SPAA), 79 to 90, 2009
    locator: the definition of reducer hyperobjects by a monoid, the views of the strands, and the guarantee that the result equals the serial execution
  - book: isbn:9780124159938
    title: Michael McCool, Arch D. Robison and James Reinders, Structured Parallel Programming, Morgan Kaufmann, 2012
    locator: Chapter 5, Collectives (reduce, the conditions on the combiner, and the effect of reordering on floating-point results)
  - url: https://www.cs.cmu.edu/~guyb/papers/Ble93.pdf
    title: Guy E. Blelloch, Prefix Sums and Their Applications, Technical Report CMU-CS-90-190, Carnegie Mellon University, 1990
    locator: Section 1.2, Implementation (reduce as the up-sweep of a balanced tree)
  - paper: doi:10.1145/65950.65958
    title: Paul Beame and Johan Håstad, Optimal bounds for decision problems on the CRCW PRAM, Journal of the ACM 36(3), 643 to 670, 1989
    locator: the Ω(log n / log log n) time lower bound for parity with a polynomial number of processors
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 4, Summation (the error bounds of recursive and pairwise summation)
---

The reduction problem asks for the value $a_0 \oplus a_1 \oplus \cdots \oplus a_{n-1}$ of a whole sequence under an [associative operator](/associative-operator/) $\oplus$, such as a total, a maximum or a count. In parallel code it also names a technique: a loop that updates an accumulator, such as `sum ← sum + f(i)`, is rewritten as a reduction so that its iterations can run in parallel. This page is about the problem and that technique. The basic algorithm that solves it, a balanced tree of combines, is the [parallel reduce](/parallel-reduce/).

## In plain words

Many loops build one answer from many items: they add up costs, count matches, or keep the largest value seen. Written in the usual way, each step needs the result of the step before, so the loop seems to be strictly one step at a time.

But if the order of grouping does not change the answer, the items can be split into groups, each group can be done by a different worker, and the group answers can be put together at the end. Reduction is the name for this kind of job. The skill is to see that a loop has this shape, and to make sure that the workers do not write to the same total at the same time.

## Definition

**The problem.** The input is a sequence $a_0, \ldots, a_{n-1}$ over a set $S$ and a [monoid](/monoid/) $(S, \oplus, e)$: an associative operator $\oplus$ with an identity $e$. The output is $a_0 \oplus \cdots \oplus a_{n-1}$, which is $e$ for $n = 0$. Associativity makes the output well defined without brackets; commutativity is not assumed, so the order of the items matters. Often the items are $f(0), \ldots, f(n-1)$ for a function $f$, and the problem is then a map followed by a reduction.

**The technique.** A loop has a reduction in a variable $acc$ when

1. $acc$ is set to $e$ before the loop,
2. each iteration $i$ changes $acc$ only by the update $acc \leftarrow acc \oplus x_i$, where $x_i$ does not depend on $acc$, and
3. no iteration reads $acc$ in any other way.

Then the value of $acc$ after the loop is $x_0 \oplus x_1 \oplus \cdots \oplus x_{n-1}$, by induction on the number of iterations, and the loop can be replaced by a computation of the $x_i$ in parallel followed by a reduction. The variable $acc$ is the only dependence between iterations, so with it removed the iterations are independent.

**How this differs from parallel reduce.** Reduction is *what* is computed, and the technique of finding it in a loop. [Parallel reduce](/parallel-reduce/) is one *way* to compute it: split the sequence in two, reduce both halves at the same time, and combine. Reducers, atomic updates and per-thread totals are other ways.

## Variants

- **Map-reduce.** The items are $f(a_i)$, and the map is done at the leaves of the reduction, so the mapped values are never stored.
- **Reduce by key.** Each item has a key, and the output is one reduction per key, as in a [histogram](/histogram-computation/) or the word count of the [MapReduce model](/mapreduce-model/). It is a reduction in the monoid of maps from keys to values, combined key by key.
- **Commutative reduction.** When $\oplus$ is also commutative, the items may be combined in any order, for example with atomic adds as they arrive, or in a [combining tree](/combining-tree/) inside the memory network.
- **All-reduce.** In distributed memory, every process ends with the result, as in MPI_Allreduce.
- **All prefixes.** If every partial result is needed, the problem is [all-prefix-sums](/all-prefix-sums/).
- **Non-associative updates.** A loop such as $acc \leftarrow 2 \cdot acc + x_i$ is not a reduction in $+$. It is a reduction in the composition of the affine maps $y \mapsto 2y + x_i$, which is associative. When no associative operator fits, the loop cannot be reduced in this way.

## Examples

| task | monoid $(S, \oplus, e)$ |
|---|---|
| total | numbers, $+$, $0$ |
| count of items with a property | integers, $+$, $0$, with $x_i \in \{0, 1\}$ |
| largest value | numbers, $\max$, $-\infty$ |
| "does any item match?" | booleans, $\lor$, false |
| "do all items match?" | booleans, $\land$, true |
| index of the first maximum | pairs (value, index); keep the larger value, and on a tie the smaller index |
| mean | pairs (sum, count), added component by component |
| concatenation of lists | lists, append, the empty list (not commutative) |
| dot product $\sum u_i v_i$ | numbers, $+$, $0$, with $x_i = u_i v_i$ |

The loop $acc \leftarrow 0$; for $i$ in $0..n-1$: if $a_i > 0$ then $acc \leftarrow acc + 1$ is a reduction: set $x_i = 1$ if $a_i > 0$ and $x_i = 0$ otherwise. The loop that sets $acc \leftarrow a_i - acc$ is not a reduction in $-$, because subtraction is not associative.

## Known algorithms

- **[Parallel reduce](/parallel-reduce/).** A balanced tree of combines: exactly $n - 1$ combines and span $\lceil \lg n \rceil$, deterministic for a fixed $n$.
- **Per-thread totals.** Each of $p$ threads folds a block of about $n/p$ items, and the $p$ totals are combined in order at the end. This takes $n - 1$ combines and time $O(n/p + \log p)$. It is the usual implementation of the reduction clause of OpenMP.
- **Reducers.** Frigo, Halpern, Leiserson and Lewin-Berlin (2009) defined the reducer, a kind of *hyperobject* in Cilk++. The programmer gives a monoid and writes the loop with the usual update. The runtime gives each parallel strand its own *view* of the variable, starts new views at the identity, and when parallel strands join, it combines their views in the order of the serial program. So for an associative operator the result is the same as in the serial execution, even when the operator is not commutative, such as list append. The paper also defines holders and splitters, other hyperobjects for variables that are not reductions.
- **Atomic updates.** For a commutative operator with hardware support, such as integer addition, each iteration updates one shared total with an atomic instruction such as [fetch-and-add](/fetch-and-add/). This is simple but serializes the updates, so it is slow when there are many.
- **GPU reduction.** Each thread block reduces its part in shared memory or with warp shuffles, and a second pass or an atomic combines the block results. See [warp-level primitives](/warp-level-primitives/).

## Bounds

**Work and span.** For an operator whose result depends on every item, such as string concatenation, at least $n - 1$ applications of $\oplus$ are needed, because each one merges two partial values into one. The span is at least $\lceil \lg n \rceil$, because a value made by $d$ levels of a binary operator depends on at most $2^d$ items. The parallel reduce meets both bounds exactly, so it is optimal and [work-efficient](/work-efficiency/).

**PRAM time.** On an EREW PRAM, $n / \lg n$ processors reduce $n$ items in $O(\log n)$ time, an optimal time-processor product. On a [CRCW PRAM](/crcw-pram/), some reductions are faster: the logical OR of $n$ bits takes $O(1)$ time with $n$ processors, since every processor with a 1 writes 1 to the same cell, and the maximum takes $O(1)$ time with $n^2$ processors. But not every reduction is: the sum of $n$ bits modulo 2 is the parity function, and Beame and Håstad (1989) proved that it needs $\Omega(\log n / \log\log n)$ time with a polynomial number of processors.

**Accuracy.** For floating-point addition, the bracketing changes the result. A loop has an error bound that grows like $(n - 1) u$ times the sum of the absolute values, where $u$ is the unit roundoff, while a balanced tree, which is [pairwise summation](/pairwise-summation/), has a bound that grows like $\lceil \lg n \rceil u$. So the parallel order is usually more accurate, but not the same.

## Reductions

- **To parallel reduce.** Every instance is solved by a [parallel reduce](/parallel-reduce/) with the given monoid. If the operator has no identity, add one, or treat $n = 0$ separately.
- **From a loop.** A loop with an accumulator that satisfies the three conditions above reduces to a parallel map of the $x_i$ followed by a reduction.
- **To all-prefix-sums.** The reduction is the last entry of the inclusive scan, so any scan algorithm solves it. The converse is not true at the same cost: a reduction gives only one value.
- **Histograms.** Computing a histogram with $k$ bins is a reduction in the monoid of vectors of length $k$ under addition by entries, or a reduce by key.

## Applications

Reductions appear in almost every parallel program: totals and averages in data analysis, norms and dot products in numerical code, the global test for convergence in an iterative solver, counts in database queries, and the reduce phase of MapReduce. In fork-join languages, the reduction technique and reducers remove the most common [determinacy race](/determinacy-race/): many strands updating one shared total. In compilers, recognizing reductions is a standard step of automatic parallelization of loops.

## References
