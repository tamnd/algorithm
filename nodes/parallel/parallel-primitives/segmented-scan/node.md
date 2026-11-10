---
tag: KQTVZW
kind: algorithm
slug: segmented-scan
name: Segmented scan
aliases:
- segmented prefix sum
area: parallel/parallel-primitives
level: advanced
summary: Scan over (flag, value) pairs that resets at segment starts, using a single scan.
solves: [segmented-prefix-sums]
model: work-span-model
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n)}
  depth: {worst: Θ(log n)}
  space: {extra: Θ(n)}
properties: {deterministic: true}
prereqs: [segmented-prefix-sums, blelloch-scan]
see_also: [all-prefix-sums, associative-operator, monoid, sparse-matrix-vector-multiplication, parallel-quicksort, compressed-sparse-row, data-parallelism, parallel-prefix]
sources:
  - url: https://www.cs.cmu.edu/~guyb/papers/Ble93.pdf
    title: Guy E. Blelloch, Prefix Sums and Their Applications, Technical Report CMU-CS-90-190, Carnegie Mellon University, 1990; also Chapter 1 of John H. Reif (editor), Synthesis of Parallel Algorithms, Morgan Kaufmann, 1993
    locator: Section 1.5, Segmented Scans (the segmented operator and its use in quicksort, Section 1.5.1), and the Notes (Schwartz 1980 and Mago 1979)
  - paper: doi:10.1109/12.42122
    title: Guy E. Blelloch, Scans as primitive parallel operations, IEEE Transactions on Computers 38(11), 1526 to 1538, 1989
    locator: Section II-C, Segments and Segmented Scans
  - paper: doi:10.1145/357114.357116
    title: Jacob T. Schwartz, Ultracomputers, ACM Transactions on Programming Languages and Systems 2(4), 484 to 521, 1980
    locator: the segmented forms of the parallel prefix operations
  - paper: "Shubhabrata Sengupta, Mark Harris and Michael Garland, Efficient Parallel Scan Algorithms for GPUs, NVIDIA Technical Report NVR-2008-003, 2008"
    title: Efficient Parallel Scan Algorithms for GPUs
    locator: Section 2.1 (segmented scan by a transformation of the operator, and the care that the exclusive form needs)
  - paper: "Shubhabrata Sengupta, Mark Harris, Yao Zhang and John D. Owens, Scan Primitives for GPU Computing, Graphics Hardware 2007, pages 97 to 106"
    title: Scan Primitives for GPU Computing
    locator: the segmented scan on the GPU and its use in quicksort and sparse matrix-vector products
---

A segmented scan computes the [prefix sums](/all-prefix-sums/) of each segment of an array, where the segments are marked by flags, in one pass that does not depend on the number or the sizes of the segments. It runs one ordinary scan on the pairs (flag, value) with the operator $(f, x) \oplus_s (g, y) = (f \lor g,\ g\ ?\ y : x \oplus y)$. This operator is associative whenever $\oplus$ is (Schwartz 1980), so any scan algorithm works, and with the [Blelloch scan](/blelloch-scan/) the cost is $\Theta(n)$ work and $\Theta(\log n)$ span. Segmented scans let a flat array hold many independent sequences, which is the basis of nested [data parallelism](/data-parallelism/).

## In plain words

Several shops share one long list of hourly takings, one shop after another, and each shop wants its own running total. One could make a separate list for each shop, but if there are thousands of tiny shops, starting one job per shop is slow.

Instead, put a mark at the first hour of each shop and run one running total over the whole list, with one rule: when you reach a mark, forget the total so far and start again from that number. The rule can be written as a way of combining two pieces of the list, and the grouping of the pieces does not change the result. So the fast parallel running-total methods still work, unchanged, on the whole list at once.

## The problem

The input is an array $A[0 \ldots n-1]$ over a [monoid](/monoid/) $(S, \oplus, e)$ and an array of flags $F[0 \ldots n-1]$, with $F[i] = 1$ when a new segment starts at $i$; position 0 always starts a segment. For each $i$, let $s(i)$ be the start of the segment of $i$. The output is the inclusive segmented scan $I[i] = A[s(i)] \oplus \cdots \oplus A[i]$, the exclusive one $X[i] = A[s(i)] \oplus \cdots \oplus A[i-1]$, or both. This is the [segmented prefix sums](/segmented-prefix-sums/) problem.

## The algorithm

Here $\oplus_s$ is the segmented operator above, and EXCLUSIVE-SCAN is any scan for an associative operator with an identity, such as the Blelloch scan.

```pseudo id=main
SEGMENTED-SCAN(A, F, n, ⊕, e)
L1  for i ← 0 to n − 1 in parallel do P[i] ← (F[i] or i = 0, A[i])
L2  Q ← EXCLUSIVE-SCAN(P, ⊕s, (0, e))
L3  for i ← 0 to n − 1 in parallel do
L4    I[i] ← value of (Q[i] ⊕s P[i])                  ▷ inclusive
L5    X[i] ← e if flag of P[i] = 1, else value of Q[i]   ▷ exclusive
L6  return (I, X)
```

The flag of a combined pair says whether a segment starts anywhere in that piece. When the right piece contains a start, everything to its left belongs to earlier segments, so the combine keeps only the right value. Line L5 needs its test: at a segment start, $Q[i]$ holds the total of the previous segment, not $e$.

## Example

Let $A = [3, 1, 7, 0, 4, 1, 6, 3]$ with $+$ and flags $F = [1, 0, 1, 0, 0, 1, 0, 0]$, so the segments are $[3, 1]$, $[7, 0, 4]$ and $[1, 6, 3]$.

| $i$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| $P[i]$ | (1,3) | (0,1) | (1,7) | (0,0) | (0,4) | (1,1) | (0,6) | (0,3) |
| $Q[i]$ | (0,0) | (1,3) | (1,4) | (1,7) | (1,7) | (1,11) | (1,1) | (1,7) |
| $I[i]$ | 3 | 4 | 7 | 7 | 11 | 1 | 7 | 10 |
| $X[i]$ | 0 | 3 | 0 | 7 | 7 | 0 | 1 | 7 |

At $i = 5$, the pair scan $Q[5] = (1, 11)$ holds the total of the second segment. The inclusive value is $(1, 11) \oplus_s (1, 1) = (1, 1)$, and the exclusive value is $0$ because a segment starts at 5. Taking the value of $Q[5]$ as is would give 11, which is the pitfall that line L5 avoids.

## Correctness

The proof has two parts. First, $\oplus_s$ is associative with identity $(0, e)$: the flags combine with $\lor$, and for the values a case split on the flags of the second and the third operand reduces every case to the associativity of $\oplus$. So the scan on line L2 computes the true prefixes $P[0] \oplus_s \cdots \oplus_s P[i-1]$. Second, by induction on $i$, the prefix of the pairs up to $i$ has value $A[s(i)] \oplus \cdots \oplus A[i]$, since a combine with a flagged pair drops everything before it. The full proof, with the brute-force check in the tests as a second check, is in [the proof of correctness](proofs/correctness.md).

## Complexity

The field `time` of this page is the work, and the field `depth` is the span.

**Work and span.** Lines L1 and L3 to L5 are maps with $O(1)$ work per item. Each $\oplus_s$ costs one $\oplus$ and one $\lor$. With the Blelloch scan on line L2, the scan does $2(m - 1)$ combines in $2 \lceil \lg n \rceil$ rounds, where $m = 2^{\lceil \lg n \rceil}$, and line L4 adds $n$ more in one round. The tests check these exact counts. So the work is $\Theta(n)$ and the span is $\Theta(\log n)$, whatever the segments are.

**Compared with one scan per segment.** Running a separate scan on each segment in parallel has the same total work, but a span of $\Theta(\log \ell)$ for the longest segment $\ell$ plus the cost of starting one task per segment. With many short segments, the per-task cost dominates; with a few long ones, the load is uneven. The segmented scan avoids both, which is why it suits SIMD and GPU hardware.

**Space.** The pairs take one extra flag per item.

## Properties

- **Associative, not commutative.** The segmented operator is associative but not commutative, even when $\oplus$ is: $(1, 1) \oplus_s (0, 2) = (1, 3)$ but $(0, 2) \oplus_s (1, 1) = (1, 1)$. So the scan must keep the order of the operands.
- **Any scan works.** Because $\oplus_s$ is an associative operator with an identity, every scan algorithm, circuit and library function can compute a segmented scan without change: [Hillis-Steele](/hillis-steele-scan/), Blelloch, the [prefix circuits](/parallel-prefix/), and blocked scans.
- **Independent of the segments.** The cost does not depend on the number or the sizes of the segments, including empty segments when the segments are given by lengths.
- **Deterministic.** The bracketing is fixed by $n$.

## Variants and improvements

- **Direct implementation.** Instead of pairs, a segmented up-sweep and down-sweep can keep the flags in a separate array and test them inside the scan. Blelloch gives such a version; it does the same work but avoids building pairs.
- **Backward segmented scan.** Scanning from the right gives each item the sum to the end of its segment, for example to copy the last value of a segment to all its items.
- **Segmented copy and distribute.** A segmented scan with the operator "keep the left value" copies the first item of each segment to all items of the segment. Blelloch's quicksort uses this to give each item the pivot of its segment.
- **Segmented reduce.** The inclusive value at the last item of each segment is the total of the segment. With a [pack](/parallel-pack/) of those positions, this gives one total per segment, the operation used in [sparse matrix-vector multiplication](/sparse-matrix-vector-multiplication/).
- **Head flags from lengths.** When segments are given by their lengths, an exclusive $+$-scan of the lengths gives the starts, and a [scatter](/scatter-and-gather/) writes the flags.
- **GPU versions.** Sengupta, Harris, Zhang and Owens (2007) and Sengupta, Harris and Garland (2008) give segmented scans for GPUs, with warp-level and block-level steps.

## When to use it

Use a segmented scan when many independent scans have to run at once, especially when the segments are many, short or uneven. Typical cases are rows of a sparse matrix in [compressed sparse row](/compressed-sparse-row/) format, the subproblems of a [quicksort](/parallel-quicksort/) or of a radix sort without recursion, the adjacency lists of a graph, and the inner sequences of a nested data-parallel program. When there are only a few long segments, separate scans are simpler and just as fast.

## Pitfalls

- **The exclusive form.** Taking the value of the exclusive pair scan as is gives the total of the previous segment at each segment start. Line L5 must return $e$ there. The tests check this case.
- **Swapped operands.** Because $\oplus_s$ is not commutative, a scan that swaps the operands is wrong for every input with more than one segment, even for $+$.
- **Position 0.** If $F[0] = 0$, the first items form a segment anyway. Code that ORs the flags must treat position 0 as a start, or the identity must be the right start value.
- **The wrong identity.** The identity of $\oplus_s$ is $(0, e)$, with the identity of $\oplus$ as its value. With $\max$ as the base operator, the value must be $-\infty$. With 0, the exclusive output at each segment start is 0, and a padded scan can mix the 0 into its partial results.
- **Flags or lengths.** Some libraries mark segment ends, or take segment lengths, or take segment keys. Mixing the conventions shifts every segment by one.

## Implementations

## History

Blelloch's notes credit Schwartz (1980), in his paper on ultracomputers, and independently Mago (1979) with the first suggestion of segmented scans. Blelloch made the segmented scan a primitive of the scan vector model in "Scans as primitive parallel operations" (1989) and in "Prefix Sums and Their Applications" (1990), where he used it for quicksort and for operations on segmented vectors. It became the basis of the flattening of nested data parallelism in NESL. On GPUs, Sengupta, Harris, Zhang and Owens (2007) showed how to use segmented scans for quicksort and sparse matrix-vector products.

## References
