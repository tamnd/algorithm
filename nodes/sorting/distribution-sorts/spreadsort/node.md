---
tag: ER6NF4
kind: algorithm
slug: spreadsort
name: Spreadsort
area: sorting/distribution-sorts
level: advanced
summary: Hybrid of MSD radix distribution and comparison sort that adapts bucket counts to the input distribution.
solves: [sorting-problem]
model: word-ram
complexity:
  vars: {n: the number of keys, K: the number of bits of a key, S: the most bits that one pass uses, M: the size below which a range is sorted by insertion sort}
  time: {worst: O(n K + n M), average: "O(n (1 + log n / S))", best: Θ(n)}
  space: {extra: "O(2^S · K)"}
properties: {stable: false, in_place: true, adaptive: true, online: false, deterministic: true, comparison: false, recursive: true}
prereqs: [msd-radix-sort, bucket-sort]
see_also: [msd-radix-sort, american-flag-sort, flashsort, bucket-sort, radix-sort, insertion-sort, integer-sorting, distribution-sort]
sources:
  - paper: Steven J. Ross, The Spreadsort High-performance General-case Sorting Algorithm, Proceedings of the International Conference on Parallel and Distributed Processing Techniques and Applications (PDPTA 2002), Volume 3, Las Vegas, 2002, pages 1100 to 1106
    locator: the description of the algorithm (minimum and maximum, bins of a power-of-two width, the cap on bins per pass, recursion and the comparison-sort fallback)
  - url: https://www.boost.org/doc/libs/1_85_0/libs/sort/doc/html/sort/single_thread/spreadsort.html
    title: Steven Ross, Boost.Sort library documentation, Spreadsort
    locator: the overview of the hybrid radix and comparison sort, the tuning constants max_splits and log_mean_bin_size, and the worst-case performance section
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Chapter 5, Section 5.1, String Sorts, subsection MSD string sort, the in-place key-indexed counting and the cut-off to insertion sort
---

Spreadsort is a hybrid sort that splits keys into bins by their leading bits, as [MSD radix sort](/msd-radix-sort/) does, but it chooses the number of bins from the size of the range and from the spread between its smallest and largest key. It sends small ranges to a comparison sort. The bins start at the minimum key, so the first pass uses only the bits that actually differ, and a range of equal keys stops at once. Steven J. Ross published it in 2002, and it is the spreadsort of the Boost.Sort library.

## In plain words

You must put a pile of numbered cards in order. First you look for the smallest and the largest number. You make a row of boxes that covers exactly the numbers from the smallest to the largest, with one box for each block of equal width. You put each card into its box. A box with many cards is done the same way again, with new boxes that cover only the numbers in that box. A box with few cards is sorted by hand, one card at a time.

The number of boxes depends on the number of cards. Many cards get many boxes, but never more than a fixed limit, so the boxes fit in fast memory. If the numbers are close together, the first row of boxes already uses the bits that differ, so little work is wasted.

## The problem

The input is an array $A[0 \ldots n-1]$ of keys from a totally ordered set, and the output is the same keys in non-decreasing order. This is the [sorting problem](/sorting-problem/). Spreadsort needs a map $f$ from keys to non-negative integers with $x < y \Leftrightarrow f(x) < f(y)$, so $f$ is one-to-one and preserves the order. For integers, $f$ is the identity. For IEEE floats, $f$ is the bit pattern with the sign handled so that the order of the integers is the order of the floats. For strings, $f$ reads the characters as the digits of a number. Write $K$ for the number of bits of $f(x)$.

## The algorithm

A task $(lo, hi)$ is a range of $A$ that must be sorted. $M$ is the cut-off for insertion sort, $S$ is the cap on the bits of one pass, and $L$ is the log of the mean number of keys per bin.

```pseudo id=main
SPREADSORT(A, n, M, S, L)
L1  stack ← the task (0, n)
L2  while stack is not empty do
L3      (lo, hi) ← pop stack; m ← hi − lo
L4      if m < M then insertion sort A[lo .. hi − 1]; continue
L5      mn ← min f(A[i]), mx ← max f(A[i]) for lo ≤ i < hi
L6      if mn = mx then continue                       ▷ all keys equal
L7      r ← the number of bits of mx − mn
L8      b ← max(1, min(S, ⌊log₂ m⌋ − L, r))
L9      shift ← r − b                                  ▷ bin of x: (f(x) − mn) >> shift
L10     count the keys of each of the 2^b bins; start[j] ← the first index of bin j
L11     permute A[lo .. hi − 1] in place so that bin j is at start[j] .. start[j + 1] − 1
L12     if shift = 0 then continue                     ▷ each bin holds equal keys
L13     push (start[j], start[j + 1]) for each bin j with at least 2 keys
L14 return A
```

Line L8 is the adaptive part. A range of $m$ keys gets about $m / 2^L$ bins, rounded down to a power of two, but at most $2^S$, and never more bins than the spread $mx - mn$ needs. Line L11 is the in-place cycle permutation of [American flag sort](/american-flag-sort/): take the key at the next free place of bin $j$, and swap it to the next free place of its own bin until a key of bin $j$ comes back.

## Example

Sort $A = [37, 12, 58, 3, 45, 21, 60, 9, 33, 50]$ with $M = 4$ and $L = 0$, so $f$ is the identity. Line L5 gives $mn = 3$ and $mx = 60$. The spread is $57$, which has $r = 6$ bits. Line L8 gives $b = \min(S, \lfloor \log_2 10 \rfloor, 6) = 3$, so there are 8 bins and $shift = 3$. The bin of $x$ is $(x - 3) \gg 3$.

| key | 37 | 12 | 58 | 3 | 45 | 21 | 60 | 9 | 33 | 50 |
|---|---|---|---|---|---|---|---|---|---|---|
| $x - 3$ | 34 | 9 | 55 | 0 | 42 | 18 | 57 | 6 | 30 | 47 |
| bin | 4 | 1 | 6 | 0 | 5 | 2 | 7 | 0 | 3 | 5 |

The counts are $[2, 1, 1, 1, 1, 2, 1, 1]$, and after line L11 the array is $[3, 9 \mid 12 \mid 21 \mid 33 \mid 37 \mid 45, 50 \mid 58 \mid 60]$ (the order inside a bin can differ). Line L13 pushes the two bins with two keys. Each has fewer than $M = 4$ keys, so line L4 sorts it by insertion sort, and the result is $[3, 9, 12, 21, 33, 37, 45, 50, 58, 60]$. One pass did all the work, because the 10 keys are spread evenly over the range from 3 to 60.

## Correctness

The invariant is the same as for MSD radix sort. The ranges on the stack are disjoint, and each key outside them is in order with all other keys. When a range is split, each key of bin $j$ is less than each key of bin $j + 1$, because the bin number $(f(x) - mn) \gg shift$ does not decrease when $f(x)$ grows, and $f$ preserves the order. When $shift = 0$, each bin has one value of $f$, so its keys are equal. The loop ends because each split leaves bins whose spread is less than $2^{shift} \le 2^{r - 1}$, so the bit count $r$ of each new task is at least one less. The full proof is below.

## Complexity

- **One pass.** Lines L5 to L13 on a range of $m$ keys cost $O(m + 2^b)$. Line L8 gives $2^b \le m / 2^L$, so a pass costs $\Theta(m)$.
- **Depth.** A key goes through at most $K$ passes, because each pass removes at least one bit of the spread (line L8 has $b \ge 1$). In the end it is in a range sorted by insertion sort, which costs $O(M)$ for each key. So the worst case is $O(n K + n M)$.
- **Uniform keys.** The average bound is for keys spread evenly. For such keys, a pass on $m$ keys with $b$ bits leaves bins of about $m / 2^b$ keys. While $m$ is large, $b = S$ and the size drops by a factor $2^S$. So after about $\log_2 n / S$ passes the bins are small, and the cost is $O(n (1 + \log n / S))$ in expectation. With $S = 11$ this is two or three passes for a million keys.
- **Best case.** If all keys are equal, or if the first pass gives bins of at most one key, the cost is $\Theta(n)$.
- **Space.** The pass uses $2^b \le 2^S$ counters, which are freed at the end of the pass. The stack holds at most $2^S$ tasks for each open level, and there are at most $K$ levels. So the extra space is $O(2^S K)$, and it does not depend on $n$.

The Boost documentation states a worst case of the better of $O(n \log n)$ comparisons and $O(n (K/S + S))$ operations for its version, which also switches to a comparison sort when a range is large but its spread needs too many passes.

## Properties

- **Not stable.** The cycle permutation of line L11 moves equal keys past each other.
- **In place.** The keys move inside $A$. The extra memory is the counters and the stack.
- **Adaptive to the distribution.** The bins start at the minimum of each range, and their number follows the size of the range. A range with a small spread needs few passes, and a range of equal keys costs one scan.
- **Hybrid.** It uses the bits of the keys as indices, and it uses comparisons only inside small ranges.

## Variants and improvements

- **Comparison fallback for large ranges.** The Boost version compares the number of passes that the spread needs with the cost of a comparison sort, and use the comparison sort (for example [introsort](/introsort/)) when it is cheaper. This bounds the worst case by $O(n \log n)$.
- **Float and string keys.** Boost has `float_sort`, which sorts IEEE floats by their bits after the sign is handled, and `string_sort`, which reads one character for each pass and skips the common prefix of the range.
- **Tuning constants.** Boost names $S$ `max_splits` (11 by default) and $L$ `log_mean_bin_size`. A smaller $S$ keeps the counters in the L1 cache.
- **Related sorts.** [Flashsort](/flashsort/) also places keys by a linear map from the minimum to the maximum, but in one pass with a fixed number of classes and insertion sort at the end. [MSD radix sort](/msd-radix-sort/) uses a fixed digit and does not look at the minimum.

## When to use it

Use spreadsort for large arrays of integers, floats or strings when an in-place sort is wanted that is faster than a comparison sort. For a few thousand keys or fewer, the passes cost more than they save, and a good comparison sort is better. If the sort must be stable, use [LSD radix sort](/radix-sort/) or [merge sort](/merge-sort/).

## Pitfalls

- **A wrong key map.** The map $f$ must preserve the order. The raw bits of a negative float or of a two's complement integer do not. Flip the sign bit of integers, and flip all bits of negative floats.
- **Bins from zero, not from the minimum.** If the bins start at 0, keys in a narrow range far from 0 all fall into one bin, and the pass is wasted. Line L9 subtracts $mn$.
- **Too many bins.** Without the cap $S$ and the factor $2^L$, a pass on a small range can allocate more counters than there are keys, and the counters leave the cache.
- **A map that is not one-to-one.** If two different keys can have the same $f$ value, as for floats and large integers mixed, line L6 and line L12 must sort the range by comparison and not stop.

## Implementations

## History

Steven J. Ross presented spreadsort at the PDPTA conference in 2002 as a general-case sort that combines radix distribution and comparison sorting. He later wrote the integer, float and string versions of the Boost.Sort library. The idea of bins scaled from the minimum to the maximum of the data goes back to [distribution sorts](/distribution-sort/) such as [bucket sort](/bucket-sort/) and flashsort, and the in-place permutation follows American flag sort.

## References
