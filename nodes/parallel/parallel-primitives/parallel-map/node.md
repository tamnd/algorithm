---
tag: S8QNJR
kind: algorithm
slug: parallel-map
name: Parallel map
aliases:
- elementwise map
- apply-to-each
area: parallel/parallel-primitives
level: intro
summary: Applies a function to every element of a sequence in parallel.
model: work-span-model
complexity:
  vars: {n: "the number of items, with f taking constant time"}
  time: {worst: Θ(n)}
  depth: {worst: Θ(log n)}
  space: {extra: Θ(log n)}
properties: {deterministic: true, recursive: true}
prereqs: [parallel-for, work-span-model]
see_also: [parallel-reduce, scatter-and-gather, parallel-pack, data-parallelism, determinacy-race, mapreduce-model, simt-model, fork-join-parallelism]
sources:
  - book: isbn:9780124159938
    title: Michael McCool, Arch D. Robison and James Reinders, Structured Parallel Programming, Morgan Kaufmann, 2012
    locator: Chapter 4, Map (the map pattern, elemental functions, and the fusion of maps)
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Chapter 27, Section 27.1, the subsection Parallel loops (the divide-and-conquer implementation of a parallel loop and its span Θ(lg n) + max iter∞(i))
  - paper: doi:10.1145/227234.227246
    title: Guy E. Blelloch, Programming parallel algorithms, Communications of the ACM 39(3), 85 to 97, 1996
    locator: the apply-to-each construct of NESL and its work and depth
  - paper: doi:10.1145/7902.7903
    title: W. Daniel Hillis and Guy L. Steele Jr., Data parallel algorithms, Communications of the ACM 29(12), 1170 to 1183, 1986
    locator: the opening sections on the data-parallel style, with one processor for each data element
---

A parallel map applies a function $f$ to every item of an array $A$ and returns the array $B$ with $B[i] = f(A[i])$. The calls of $f$ are independent, so they can all run at the same time. In the [work-span model](/work-span-model/), with a fork-join split of the index range, the work is $(n - 1) + \sum_i W_f(A[i])$ and the span is at most $\lceil \lg n \rceil + \max_i S_f(A[i])$. For a constant-time $f$, this is $\Theta(n)$ work and $\Theta(\log n)$ span, so a map is the simplest data-parallel operation, and the one that most others are combined with.

## In plain words

A map does the same thing to every item of a list: double every price, convert every temperature from Fahrenheit to Celsius, or make every name upper case. The result for one item never depends on another item.

So many workers can share the job. The only work besides the job itself is handing it out. Handing out one item at a time from one desk would be slow, so the list is split in half, each half is split again, and so on, until each worker has a small piece. This takes only as many rounds as the number of times the list can be halved.

## The problem

The input is an array $A[0 \ldots n-1]$ and a function $f$ whose calls do not write shared memory. The output is the array $B[0 \ldots n-1]$ with $B[i] = f(A[i])$. The call of $f$ on item $i$ has work $W_i$ and span $S_i$; often $f$ takes constant time. This is the data operation; the control construct that runs independent iterations is the [parallel for loop](/parallel-for/).

## The algorithm

The range $[lo, hi)$ is half-open. The keyword spawn starts a call that may run in parallel with the code after it, and sync waits for it.

```pseudo id=main
MAP(f, A, B, lo, hi)                       ▷ hi − lo ≥ 1
L1  if hi − lo = 1 then B[lo] ← f(A[lo]); return
L2  mid ← lo + ⌈(hi − lo) / 2⌉
L3  spawn MAP(f, A, B, lo, mid)
L4  MAP(f, A, B, mid, hi)
L5  sync

PARALLEL-MAP(f, A, n)
L6  B ← a new array of length n
L7  if n > 0 then MAP(f, A, B, 0, n)
L8  return B
```

The two calls write disjoint parts of $B$ and only read $A$, so they cannot race. This is the parallel for loop "for $i \leftarrow 0$ to $n - 1$ in parallel do $B[i] \leftarrow f(A[i])$" with its spawn tree written out. On a PRAM or a GPU, the map is a single step: processor $i$ computes $f(A[i])$, with no tree at all.

## Example

Map $f(x) = x^2$ over $A = [3, 1, 7, 0, 4]$. The range $[0, 5)$ splits into $[0, 3)$ and $[3, 5)$; then $[0, 3)$ splits into $[0, 2)$ and $[2, 3)$, $[0, 2)$ into $[0, 1)$ and $[1, 2)$, and $[3, 5)$ into $[3, 4)$ and $[4, 5)$.

| leaf | depth | $B[i]$ |
|---|---|---|
| $[0, 1)$ | 3 | 9 |
| $[1, 2)$ | 3 | 1 |
| $[2, 3)$ | 2 | 49 |
| $[3, 4)$ | 2 | 0 |
| $[4, 5)$ | 2 | 16 |

The output is $[9, 1, 49, 0, 16]$. There are $4 = n - 1$ split nodes and 5 calls of $f$, so the work is 9 units, and the deepest leaf is at depth $3 = \lceil \lg 5 \rceil$, so the span is $3 + 1 = 4$ units.

## Correctness

The split nodes form a full binary tree whose leaves are the single indices $0, \ldots, n-1$, each once. Leaf $i$ is the only code that writes $B[i]$, and nothing reads $B$ before the end, so there is no [determinacy race](/determinacy-race/) and every schedule gives the same $B$. The sync on line L5 makes sure that every leaf has written before the result is used. The full proof, with the exact work and span, is in [the proof of correctness](proofs/correctness.md).

## Complexity

The field `time` of this page is the work and the field `depth` is the span, for a constant-time $f$.

**Work.** The tree has $n - 1$ split nodes, so $W = (n - 1) + \sum_i W_i$. With $W_i = 1$, this is $2n - 1$, which is $\Theta(n)$.

**Span.** Every leaf is at depth $\lfloor \lg n \rfloor$ or $\lceil \lg n \rceil$, so
$$
\lfloor \lg n \rfloor + \max_i S_i \le S \le \lceil \lg n \rceil + \max_i S_i,
$$
which is $\lceil \lg n \rceil + 1$ for unit-cost calls. The span is set by the slowest call, not by the sum of the calls.

**Parallelism.** For a constant-time $f$, the parallelism is $W/S = \Theta(n / \log n)$. By [Brent's theorem](/brent-theorem/), $p$ processors run the map in time $O(n/p + \log n)$.

**Space.** The output takes $n$ cells. The serial execution of the recursion uses a stack of $\lceil \lg n \rceil + 1$ frames.

## Properties

- **Deterministic.** The result does not depend on the schedule, as long as $f$ does not write shared memory.
- **Order-free.** The calls may run in any order, so $f$ needs no algebraic property. Compare a [reduce](/parallel-reduce/), which needs an associative operator.
- **Composable.** Two maps in a row equal one map of the composed function, $\mathrm{map}(g) \circ \mathrm{map}(f) = \mathrm{map}(g \circ f)$. A map followed by a reduce can do $f$ at the leaves of the reduce.
- **Embarrassingly parallel.** There is no communication between items. The only parallel overhead is the spawn tree.

## Variants and improvements

- **Grain size.** Ranges of at most $g$ items run as a serial loop. This divides the number of spawns by about $g$ and changes the span to $\Theta(g + \log(n/g))$ for unit-cost calls. The tests check that the number of splits is between $n/g - 1$ and $2n/g$.
- **Map with an index.** $B[i] = f(i, A[i])$, or a map over several arrays of the same length, such as $C[i] = A[i] + B[i]$. NESL calls this apply-to-each.
- **In-place map.** $A[i] \leftarrow f(A[i])$ needs no output array and is still race-free.
- **Fusion.** Compilers fuse maps with each other and with reductions and scans, so that the intermediate arrays are never stored. McCool, Robison and Reinders describe this for the map pattern.
- **Nested maps.** If $f$ itself contains a map, the span adds up: a map over $n$ rows of a map over $m$ items has span $\Theta(\log n + \log m)$. This is nested [data parallelism](/data-parallelism/).
- **SIMD and GPU.** On vector hardware, consecutive items go into the lanes of one instruction. On a GPU, each thread computes one or a few items, as in the [SIMT model](/simt-model/).

## When to use it

Use a parallel map whenever the result for each item depends only on that item, for example to transform every pixel, every record or every particle in a time step. When $f$ is very cheap, such as one addition, the speed is set by memory bandwidth, not by processors, so fuse the map with the next operation if possible. When the work per item varies a lot, keep the grain small enough for [work stealing](/work-stealing/) to balance the load. When item $i$ writes to a position computed from the data, the operation is a [scatter](/scatter-and-gather/), not a map, and it can race.

## Pitfalls

- **A function with side effects.** If $f$ updates a shared counter or appends to a shared list, the map has a race. Use a [reduction](/parallel-reduction/) or a [pack](/parallel-pack/) instead.
- **Too fine a grain.** One spawn for each item costs much more than a cheap $f$. A parallel map can then be slower than a loop.
- **Uneven work.** If a few calls are slow, the span is the slowest call, and a static split into $p$ blocks can leave most processors idle.
- **Reading the output.** Code that reads $B[j]$ inside the map, for $j \ne i$, reads a value that may not be written yet.

## Implementations

## History

The map is one of the oldest ideas of parallel programming and of functional programming, where `map` applies a function to every element of a list. Hillis and Steele (1986) made the data-parallel style popular, with one processor of the Connection Machine for each data element, so that a map is a single step. Blelloch's language NESL (1990s) made apply-to-each the basic parallel construct and gave it a cost in work and depth. CLRS introduced the `parallel for` keyword, with its divide-and-conquer implementation and span bound, in the third edition (2009).

## References
