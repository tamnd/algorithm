---
tag: W9Q826
kind: algorithm
slug: kadane-algorithm
name: Kadane's algorithm
aliases:
- Kadane's maximum subarray algorithm
area: sequences/subarray-problems
level: intro
summary: Linear-time dynamic program that scans once, tracking the best sum of a subarray ending at each position.
solves: [maximum-subarray-problem]
model: word-ram
complexity:
  vars: {n: the number of items in the array}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {stable: false, in_place: true, adaptive: false, online: true, deterministic: true, comparison: false, recursive: false}
history:
  year: 1977
  people: [Joseph B. Kadane, Jon Bentley]
  note: Kadane designed the linear scan in 1977 after Michael Shamos described the problem at a seminar at Carnegie Mellon University; Bentley published it with the slower algorithms in his Programming Pearls column of 1984.
prereqs: [maximum-subarray-problem, loop-invariant, optimal-substructure]
see_also: [maximum-subarray-divide-and-conquer, circular-kadane-algorithm, kadane-max-product, bentley-column-sweep, prefix-sums, segment-tree-maximum-subsegment-sum, k-maximum-subarray-problem, online-algorithm]
sources:
  - paper: doi:10.1145/358234.381162
    title: "Jon Bentley, Programming pearls: algorithm design techniques, Communications of the ACM 27(9) (1984), 865-873"
    locator: the scanning algorithm and the account of its origin
  - book: isbn:9780201657883
    title: Jon Bentley, Programming Pearls, second edition
    locator: Column 8, Section 8.4, A Scanning Algorithm
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 4.1, Exercise 4.1-5 (the linear-time nonrecursive algorithm)
  - paper: doi:10.1016/0167-6423(83)90015-1
    title: "David Gries, A note on a standard strategy for developing loop invariants and loops, Science of Computer Programming 2(3) (1982), 207-214"
    locator: the derivation of the linear algorithm from a loop invariant
  - paper: doi:10.3390/a16110519
    title: "Joseph B. Kadane, Two Kadane Algorithms for the Maximum Sum Subarray Problem, Algorithms 16(11) (2023), 519"
    locator: the algorithm known as Kadane's and the one he intended, and where they differ
---

Kadane's algorithm solves the [maximum subarray problem](/maximum-subarray-problem/) in one left-to-right pass, in $\Theta(n)$ time and $O(1)$ extra space. At each position $j$ it keeps the largest sum of a subarray that *ends* at $j$. That value obeys a one-line recurrence: either extend the best subarray that ends at $j - 1$, or start again at $j$, whichever gives more. The answer is the largest of these values. It is the classic first example of [optimal substructure](/optimal-substructure/) in a dynamic program, and the linear time is optimal, since every item must be read.

## In plain words

Walk along the list once and carry a running total. Before you add the next number, look at the total you carry. If it is negative, it can only pull the next stretch down, so drop it and start a new stretch at the next number. If it is zero or more, keep it and add the next number.

At every step, the running total is the best total of a stretch that ends at the current number. Keep a note of the largest running total you have seen and where its stretch started and ended. When the walk is over, that note is the answer.

## The problem

**Input.** An array $A[1..n]$ of numbers with $n \ge 1$.

**Output.** A value $S^*$ and indices $i \le j$ with $A[i] + \dots + A[j] = S^*$, where $S^*$ is the largest sum of a non-empty [subarray](/subarray/).

For the convention that allows the empty subarray, return $\max(S^*, 0)$, with an empty range when $S^* < 0$.

## The algorithm

```pseudo id=main
KADANE(A[1 .. n])
L1  cur ← A[1]; c ← 1; best ← A[1]; (bi, bj) ← (1, 1)
L2  for j ← 2 to n do
L3      if cur < 0 then cur ← A[j]; c ← j
L4      else cur ← cur + A[j]
L5      if cur > best then best ← cur; (bi, bj) ← (c, j)
L6  return (best, bi, bj)
```

The variable $cur$ is the best sum of a subarray that ends at $j$, and $c$ is where that subarray starts. Line L3 starts again when the carried sum is negative, and line L4 extends it otherwise. Line L5 records a new best.

The recurrence behind the loop is, with $E(j)$ the largest sum of a subarray ending at $j$,

$$E(1) = A[1], \qquad E(j) = A[j] + \max(E(j - 1), 0), \qquad S^* = \max_{1 \le j \le n} E(j).$$

## Example

$A = [-2, 1, -3, 4, -1, 2, 1, -5, 4]$. The table shows the values after line L5 of each step.

| $j$ | $A[j]$ | action | $cur$ | $c$ | $best$ | $(bi, bj)$ |
|---|---|---|---|---|---|---|
| 1 | $-2$ | start | $-2$ | 1 | $-2$ | $(1, 1)$ |
| 2 | $1$ | restart, $cur < 0$ | $1$ | 2 | $1$ | $(2, 2)$ |
| 3 | $-3$ | extend | $-2$ | 2 | $1$ | $(2, 2)$ |
| 4 | $4$ | restart, $cur < 0$ | $4$ | 4 | $4$ | $(4, 4)$ |
| 5 | $-1$ | extend | $3$ | 4 | $4$ | $(4, 4)$ |
| 6 | $2$ | extend | $5$ | 4 | $5$ | $(4, 6)$ |
| 7 | $1$ | extend | $6$ | 4 | $6$ | $(4, 7)$ |
| 8 | $-5$ | extend | $1$ | 4 | $6$ | $(4, 7)$ |
| 9 | $4$ | extend | $5$ | 4 | $6$ | $(4, 7)$ |

The answer is $6$, from $A[4..7] = [4, -1, 2, 1]$. At step 8 the carried sum falls to $1$ but stays non-negative, so it is kept, and step 9 reaches $5$, which does not beat $6$.

## Correctness

The loop keeps this invariant at the end of each step $j$:

> **(K)** $cur = E(j)$ is the largest sum of a subarray that ends at $j$, and $A[c..j]$ is such a subarray. $best$ is the largest sum of a subarray of $A[1..j]$, and $A[bi..bj]$ is such a subarray.

*Base.* After line L1, the only subarray of $A[1..1]$ is $A[1..1]$.

*Step.* Every subarray that ends at $j \ge 2$ is either $A[j..j]$, or $A[i..j]$ with $i < j$, which is a subarray ending at $j - 1$ followed by $A[j]$. The best of the second kind is $E(j - 1) + A[j]$. So $E(j) = A[j] + \max(E(j-1), 0)$. Lines L3 and L4 compute exactly this, and they keep the start $c$ of a subarray that reaches it. A subarray of $A[1..j]$ either ends at $j$ or lies in $A[1..j-1]$, so line L5 keeps the second part of (K).

At the end, $j = n$ and (K) gives the answer. The [proof page](proofs/correctness.md) writes out the induction.

## Complexity

- **Time.** The loop runs $n - 1$ times, with one comparison and one addition in lines L3 and L4 and one comparison in line L5. So the time is $\Theta(n)$ on every input, with at most $n - 1$ additions and $2(n - 1)$ comparisons.
- **Space.** Six scalars, $\Theta(1)$ extra space. The array is only read.
- **Lower bound.** Every algorithm for the problem must read every item, so $\Theta(n)$ is optimal; see the [maximum subarray problem](/maximum-subarray-problem/).

## Properties

- **Online.** Step $j$ uses only $A[1..j]$. After each step, $best$ is the answer for the prefix read so far, so the algorithm works on a stream with $O(1)$ memory.
- **A dynamic program in $O(1)$ space.** The table $E(1..n)$ is never stored, since each entry depends only on the one before.
- **Ties.** With the strict test $cur > best$ in line L5, the reported subarray is the one with the earliest end among those with the best sum. With the test $cur < 0$ in line L3, a carried sum of $0$ is kept, so the reported subarray starts as early as possible for its end.
- **Exact on integers.** With integer items, the only risk is overflow: every value of $cur$ and $best$ is a subarray sum, so it lies between $-n \max |A|$ and $n \max |A|$.

## Variants and improvements

- **Empty subarray allowed.** Start with $cur = best = 0$ and use $cur \leftarrow \max(cur, 0) + A[j]$ for all $j$, then report $\max(best, 0)$. This is the form in Bentley's column, `maxendinghere = max(maxendinghere + x[i], 0)`.
- **Prefix sum form.** Keep the running prefix sum $P$ and its smallest earlier value $m$; the best subarray ending at $j$ has sum $P_j - m$. This is the same algorithm in other words, see [prefix sums](/prefix-sums/).
- **Kadane's intended algorithm.** Kadane (2023) reports that the algorithm he gave in 1977 differs from the one that carries his name only on inputs with no positive item, where it is more informative.
- **Minimum subarray.** Swap max and min. Together with the total, this gives the [circular Kadane algorithm](/circular-kadane-algorithm/).
- **Products.** Carry both the largest and the smallest product ending at $j$, because a negative item swaps them; see [Kadane for maximum product](/kadane-max-product/).
- **Two dimensions.** Run it on column sums for each pair of rows; see the [Bentley column sweep](/bentley-column-sweep/).
- **Range queries.** For the best subarray inside any range of a changing array, keep the total, best prefix, best suffix and best subarray of each node of a segment tree; see the [segment tree for maximum subsegment sum](/segment-tree-maximum-subsegment-sum/).

## When to use it

Use it for the largest sum of a contiguous run in one pass, on an array or a stream. It is the standard answer whenever the question is about contiguous runs and the item values may be negative. When the run must have a length between two bounds, use the prefix sums with a [monotonic deque](/monotonic-deque-prefix-sums/) instead. For many ranges of one array, use a segment tree.

## Pitfalls

- **All negative items.** An implementation that starts with $best = 0$ returns $0$ for $[-3, -1, -2]$. That is right only if the empty subarray is allowed. For the non-empty answer $-1$, start from $A[1]$ as in line L1.
- **Resetting to zero after the update.** The form `cur = cur + A[j]; if cur < 0: cur = 0` gives the right value only under the empty convention, and it loses the start index unless the reset also moves $c$ to $j + 1$.
- **Updating the start at the wrong time.** The start $c$ must change only when the carried sum is dropped, in line L3. Setting $bi \leftarrow c$ outside line L5 can pair the start of one subarray with the end of another.
- **Overflow.** Sums of $n$ items can exceed the item type, for example $32$-bit sums of $10^5$ items of size $10^5$.

## Implementations

## History

Ulf Grenander at Brown University posed the two-dimensional problem in pattern recognition. He and others found the cubic and quadratic algorithms for one dimension, and Michael Shamos found the $n \log n$ divide-and-conquer algorithm. In 1977 Shamos described the problem at a seminar at Carnegie Mellon University, where the statistician Joseph Kadane designed the linear algorithm almost at once. Jon Bentley told the story and gave all four algorithms in his Programming Pearls column of September 1984, and the scan has carried Kadane's name since. Gries (1982) derived the same loop from its invariant as an example of program derivation. In 2023 Kadane published his own account, with the version he had intended.

## References
