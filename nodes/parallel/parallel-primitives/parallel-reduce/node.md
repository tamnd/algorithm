---
tag: 7TMWGJ
kind: algorithm
slug: parallel-reduce
name: Parallel reduction
aliases:
- tree reduction
- parallel reduce
area: parallel/parallel-primitives
level: intro
summary: Combines a sequence over a balanced binary tree in logarithmic depth.
solves: [parallel-reduction]
model: work-span-model
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n)}
  depth: {worst: Θ(log n)}
  space: {extra: Θ(log n)}
properties: {deterministic: true, recursive: true}
prereqs: [associative-operator, work-span-model, fork-join-model]
see_also: [parallel-reduction, all-prefix-sums, blelloch-scan, parallel-map, pairwise-summation, brent-theorem, warp-level-primitives, monoid]
sources:
  - url: https://www.cs.cmu.edu/~guyb/papers/Ble93.pdf
    title: Guy E. Blelloch, Prefix Sums and Their Applications, Technical Report CMU-CS-90-190, Carnegie Mellon University, 1990; also Chapter 1 of John H. Reif (editor), Synthesis of Parallel Algorithms, Morgan Kaufmann, 1993
    locator: Section 1.2, Implementation (the reduce operation on a balanced tree, Figure 1.2 for the up-sweep on a PRAM, Figure 1.3 and equation (1.1) for p processors)
  - book: isbn:9780201548563
    title: Joseph JaJa, An Introduction to Parallel Algorithms, Addison-Wesley, 1992
    locator: Chapter 1 (the sum of n elements on a balanced binary tree as the first example of the work-time framework) and Section 2.1, Balanced trees
  - book: isbn:9780124159938
    title: Michael McCool, Arch D. Robison and James Reinders, Structured Parallel Programming, Morgan Kaufmann, 2012
    locator: Chapter 5, Collectives (reduce, its tree shapes, and the effect of reordering on floating-point results)
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Chapter 27, Section 27.1 (spawn, sync, the work and span of a computation dag, and the greedy scheduler bound)
---

A parallel reduce combines the $n$ items of a sequence with an [associative operator](/associative-operator/) $\oplus$ into the single value $a_0 \oplus a_1 \oplus \cdots \oplus a_{n-1}$. It splits the sequence into two halves, reduces both halves at the same time, and combines the two results, so the combines form a balanced binary tree. In the [work-span model](/work-span-model/) it does exactly $n - 1$ combines, the same as a sequential loop, and its span is $\lceil \lg n \rceil$ combines, against $n - 1$ for the loop. It is the simplest useful parallel primitive, and it is the up-sweep half of the [Blelloch scan](/blelloch-scan/).

## In plain words

A teacher wants the total of a stack of exam scores. One person adding them one at a time needs one addition for each score after the first. Instead, the teacher gives half of the stack to each of two helpers. Each helper splits their part again and passes it on, until each person has one or two scores. Everyone adds at the same time, and the partial totals go back up, two at a time, until one total remains.

The number of additions is the same as for one person. But the time is only the number of times the stack can be halved, which is about twenty for a million scores. The method works for any operation where the grouping does not change the result, such as a maximum or joining strings, as long as each step keeps the left part on the left.

## The problem

The input is an array $A[0 \ldots n-1]$ over a set $S$, an associative operator $\oplus$ on $S$, and an identity $e$ of $\oplus$ for the case $n = 0$. The output is $A[0] \oplus A[1] \oplus \cdots \oplus A[n-1]$, which is the [reduction problem](/parallel-reduction/). The operator need not be commutative. Each application of $\oplus$ costs one unit of time.

## The algorithm

The range $[lo, hi)$ is half-open. The keyword spawn starts a call that may run in parallel with the code after it, and sync waits for it, as in the [fork-join model](/fork-join-model/).

```pseudo id=main
REDUCE(A, lo, hi)                            ▷ hi − lo ≥ 1
L1  if hi − lo = 1 then return A[lo]
L2  mid ← lo + ⌈(hi − lo) / 2⌉
L3  x ← spawn REDUCE(A, lo, mid)
L4  y ← REDUCE(A, mid, hi)
L5  sync
L6  return x ⊕ y                             ▷ left part on the left

PARALLEL-REDUCE(A, n, ⊕, e)
L7  if n = 0 then return e
L8  return REDUCE(A, 0, n)
```

The left part gets $\lceil m/2 \rceil$ of the $m$ items, so the tree is as balanced as possible. The two calls only read $A$, so they cannot race. Line L6 is the only line that applies the operator, and it keeps the order of the operands: $x$ is the result of the left part. The same tree can be computed level by level, which is the form for a PRAM or a GPU: in each round, item $2i$ and item $2i + 1$ of the current level are combined, and an odd last item moves up unchanged.

## Example

Reduce $A = [3, 1, 7, 0, 4, 1, 6, 3]$ with $+$. Each row is one level of the tree. The combines of one row are independent, so each row is one step of span.

| level | values | combines |
|---|---|---|
| 0 (input) | 3, 1, 7, 0, 4, 1, 6, 3 | 0 |
| 1 | 4, 7, 5, 9 | 4 |
| 2 | 11, 14 | 2 |
| 3 | 25 | 1 |

The result is 25 after $7 = n - 1$ combines in $3 = \lg 8$ levels. For $n = 5$ and string concatenation, $[a, b, c, d, e]$ splits into $[a, b, c]$ and $[d, e]$, then $[a, b, c]$ into $[a, b]$ and $[c]$. The combines are $ab$, $de$, $abc$ and $abcde$: 4 combines, on a longest chain of $3 = \lceil \lg 5 \rceil$ ($ab$, then $abc$, then $abcde$). The result is the left-to-right concatenation, because each combine keeps the left part on the left.

## Correctness

The call tree of REDUCE is one bracketing of $A[0] \oplus \cdots \oplus A[n-1]$ that keeps the order of the operands. By general associativity, every such bracketing has the same value as the left-to-right fold, so the result is correct. Formally, by strong induction on $hi - lo$: the two calls return the folds of the two parts, and the fold of the left part combined with the fold of the right part is the fold of the whole range. The full proof, with the exact counts below, is in [the proof of correctness](proofs/correctness.md).

## Complexity

All bounds are in the [work-span model](/work-span-model/). The field `time` of this page is the work $W$, and the field `depth` is the span $S$.

**Combines.** Let $W(m)$ be the number of combines on $m$ items. Then $W(1) = 0$ and $W(m) = W(\lceil m/2 \rceil) + W(\lfloor m/2 \rfloor) + 1$, which gives $W(n) = n - 1$ exactly. The longest chain of dependent combines satisfies $S(1) = 0$ and $S(m) = S(\lceil m/2 \rceil) + 1$, which gives $S(n) = \lceil \lg n \rceil$ exactly, by the identity $\lceil \lg \lceil m/2 \rceil \rceil = \lceil \lg m \rceil - 1$ for $m \ge 2$.

**Work and span.** The calls form a full binary tree with $2n - 1$ nodes. With unit cost for each call, spawn and sync, the work is $\Theta(n)$ and the span is $\Theta(\log n)$. The [parallelism](/parallelism/) is $W/S = \Theta(n / \log n)$.

**Time on $p$ processors.** By [Brent's theorem](/brent-theorem/), a greedy scheduler runs the reduce in time $T_p \le W/p + S = O(n/p + \log n)$. The blocked form gets the same bound directly: each of $p$ processors folds a block of $\lceil n/p \rceil$ items sequentially, and a tree reduces the $p$ block results. This takes $\lceil n/p \rceil - 1 + \lceil \lg p \rceil$ combine steps, the bound that Blelloch gives for the EREW PRAM (Section 1.2). It is $O(n/p)$ when $n/p \ge \lg p$.

**Space.** The serial execution of the fork-join program uses a stack of depth $\lceil \lg n \rceil + 1$ calls, each with $O(1)$ values, so the extra space is $\Theta(\log n)$. The level-by-level form uses an array of $\lceil n/2 \rceil$ items, or none if it works in place.

**Lower bounds.** Consider any algorithm that computes the result only by applying $\oplus$ to inputs and to earlier results, for an operator such as string concatenation, where the result depends on every item. Each application turns two partial values into one, and the result needs all $n$ items in one value, so at least $n - 1$ applications are needed. A value after $d$ levels of applications depends on at most $2^d$ items, so the span is at least $\lceil \lg n \rceil$. So the reduce is optimal in both measures, and it is [work-efficient](/work-efficiency/): its work matches the $n - 1$ combines of the sequential fold.

| measure | parallel reduce | sequential fold |
|---|---|---|
| combines (work) | $n - 1$ | $n - 1$ |
| span | $\lceil \lg n \rceil$ | $n - 1$ |
| work, with control | $\Theta(n)$ | $\Theta(n)$ |
| span, with control | $\Theta(\log n)$ | $\Theta(n)$ |

## Properties

- **Deterministic.** For a fixed $n$ the tree is fixed, so the result is the same on every run and for every number of processors, even for floating-point addition. This is not true for the blocked form, whose tree depends on $p$.
- **Order-keeping.** The operands stay in input order, so the operator need not be commutative.
- **Race-free.** The calls read shared input and return their results; no two calls write the same location.
- **Recursive.** The recursion depth is $\lceil \lg n \rceil + 1$.

## Variants and improvements

- **Level by level.** The rounds form above runs on an EREW PRAM with $\lfloor n/2 \rfloor$ processors in $\lceil \lg n \rceil$ steps. Blelloch writes it in place, storing each partial result at the right end of its range, so that the [Blelloch scan](/blelloch-scan/) can reuse the tree in its down-sweep.
- **Coarsening.** Below a grain size $g$, fold sequentially. The number of combines stays $n - 1$, the span becomes $g - 1 + \lceil \lg \lceil n/g \rceil \rceil$, and the number of spawns drops by a factor of about $g$.
- **Map and reduce together.** To reduce $f(a_0), \ldots, f(a_{n-1})$, apply $f$ at the leaves instead of in a separate [parallel map](/parallel-map/). This saves the array of mapped values.
- **Reducers.** In fork-join code that updates an accumulator inside a loop, a reducer hyperobject gives each strand its own view and combines the views in order. This is the subject of [reduction](/parallel-reduction/).
- **GPU reduction.** A GPU reduces a block of values in shared memory or with warp shuffles, then combines the block results in a second pass or with atomics. See [warp-level primitives](/warp-level-primitives/).
- **All prefixes.** Keeping every partial result, not only the last one, gives the [all-prefix-sums](/all-prefix-sums/) problem.

## When to use it

Use a parallel reduce for any total, maximum, minimum, count, logical test over all items, or other monoid summary of a large array. For small arrays, a sequential loop is faster, because each spawn costs much more than one combine. If the operator is commutative and the order of the results does not matter, an unordered combine (for example with atomic adds) can avoid the tree, but for floating-point data it gives a result that changes from run to run.

## Pitfalls

- **Swapped operands.** Returning $y \oplus x$ on line L6 still works for $+$ and $\max$, but gives the reversed string for concatenation and the wrong product for matrices. The tests with strings and $2 \times 2$ matrices catch it.
- **A non-associative operator.** With subtraction, the tree on $[8, 4, 2, 1]$ gives $(8 - 4) - (2 - 1) = 3$, but the loop gives $1$. The result depends on the tree, so it is not a reduction.
- **The wrong identity.** The identity of $\max$ is $-\infty$ (or the smallest value of the type), not $0$. The identity of $\times$ is $1$. A wrong identity changes the result only for some inputs, such as all-negative arrays, so it is easy to miss.
- **Floating-point sums.** On $[10^{16}, 1, 1, 1, 1, 1, 1, 1, 1]$ the loop gives $10^{16}$ and the tree gives $10^{16} + 6$. Neither is a bug, but a test that compares floating-point sums for exact equality fails.
- **A shared accumulator.** Writing `total ← total + A[i]` inside a parallel loop is a [determinacy race](/determinacy-race/): updates are lost. Use a reduce instead.
- **Too fine a grain.** One spawn for each item costs far more than one addition. Coarsen the leaves.

## Implementations

## History

The evaluation of an associative expression by a balanced tree is part of the basic toolkit of parallel algorithms. JaJa's textbook uses the sum of $n$ numbers on a balanced binary tree as its first example of the work-time framework for the PRAM. Blelloch calls the operation *reduce*, writes it as the up-sweep of a tree laid over the array, and gave its time $\lceil n/p \rceil + \lceil \lg p \rceil$ on the EREW PRAM with $p$ processors (1990).

## References
