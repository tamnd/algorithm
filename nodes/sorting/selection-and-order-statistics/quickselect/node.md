---
tag: TTGB6K
kind: algorithm
slug: quickselect
name: Quickselect
aliases:
- Hoare's FIND
- nth_element
- randomized selection
area: sorting/selection-and-order-statistics
level: intro
summary: Partition around a pivot and recurse only into the side containing the target rank; expected O(n) time.
solves: [selection-problem]
model: comparison-model
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n²), expected: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {stable: false, in_place: true, adaptive: false, online: false, deterministic: false, comparison: true, recursive: false}
history:
  year: 1961
  people: [C. A. R. Hoare]
  note: Hoare published the procedure FIND as Algorithm 65 in the Communications of the ACM in July 1961, next to Partition and Quicksort.
prereqs: [selection-problem, partition-around-pivot, lomuto-partition, randomized-algorithm]
see_also: [quickselect-expected-linear, randomized-quickselect, median-of-medians, introselect, floyd-rivest-select, quicksort, pivot-selection, hoare-partition]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 9, Section 9.2, Selection in expected linear time (RANDOMIZED-SELECT)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.5, Applications, the part on selection (partitioning-based selection takes linear time on average)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.3, Minimum-comparison selection, and Section 5.2.2, Sorting by exchanging (partitioning)
  - paper: doi:10.1145/366622.366647
    title: C. A. R. Hoare, Algorithm 65, Find, Communications of the ACM 4(7) (1961)
    locator: pages 321 to 322
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Section 13.5, Randomized divide and conquer, median-finding and quicksort
---

Quickselect finds the item of rank $k$ in an unsorted array: it [partitions](/partition-around-pivot/) the array around a pivot, as [quicksort](/quicksort/) does, and then continues only in the side that holds rank $k$. It solves the [selection problem](/selection-problem/) with a random pivot in expected $\Theta(n)$ time on every input, with fewer than $4n$ comparisons in expectation, but in $\Theta(n^2)$ time in the worst case. It works in place with $O(1)$ extra space. It is the usual library selection routine, for example the core of `std::nth_element` in C++.

## In plain words

You want the fifth smallest exam score in a pile of papers, and you do not want to sort the whole pile. Take one paper at random as the pivot. Put the papers with a lower or equal score to its left, and the papers with a higher score to its right. Now count the left pile. If it has exactly four papers, the pivot is the answer. If it has more, the answer is in the left pile, and you can throw the right pile away. If it has fewer, the answer is in the right pile.

Do the same again in the pile that is left. Each step throws away a part of the papers, and a random pivot throws away a large part most of the time. So the total work is only a few times the size of the pile.

## The problem

The input is an array $A[0 \ldots n-1]$ of $n \ge 1$ items with a [total order](/total-order/), and a rank $k$ with $1 \le k \le n$. The output is the $k$-th smallest item, the [order statistic](/order-statistic/) of rank $k$: the item at index $k - 1$ of the sorted array. This is the [selection problem](/selection-problem/). The algorithm also rearranges $A$, so that at the end $A[k-1]$ is the answer, the items before it are at most the answer, and the items after it are at least the answer.

## The algorithm

The range $[lo, hi)$ is half-open. The target index $t = k - 1$ is the index of the answer in the sorted array. PARTITION is the [Lomuto partition](/lomuto-partition/) with the last item as the pivot, as in [quicksort](/quicksort/).

```pseudo id=main
QUICKSELECT(A, k)                          ▷ 1 ≤ k ≤ n; return the k-th smallest item
L1  lo ← 0, hi ← n, t ← k − 1
L2  while hi − lo > 1 do                   ▷ the answer is in A[lo .. hi − 1]
L3      r ← a uniform random index in [lo, hi)
L4      swap A[r] and A[hi − 1]            ▷ the random item becomes the pivot
L5      p ← PARTITION(A, lo, hi)
L6      if t = p then return A[p]
L7      else if t < p then hi ← p
L8      else lo ← p + 1
L9  return A[lo]

PARTITION(A, lo, hi)                       ▷ the pivot is x = A[hi − 1]
L10 x ← A[hi − 1]
L11 i ← lo                                 ▷ A[lo .. i − 1] holds the items ≤ x
L12 for j ← lo to hi − 2 do
L13     if A[j] ≤ x then
L14         swap A[i] and A[j]
L15         i ← i + 1
L16 swap A[i] and A[hi − 1]
L17 return i
```

Lines L3 and L4 move a random item to the end, where PARTITION expects its pivot. After line L5, the pivot is at its final index $p$: the items of $A[lo \ldots p-1]$ are at most $A[p]$, and the items of $A[p+1 \ldots hi-1]$ are larger. If $t = p$, the pivot is the answer. If $t < p$, the answer is among the items left of $p$, so line L7 drops the pivot and the right side. Line L8 is the mirror case. Quicksort would recurse into both sides; quickselect keeps one side, so it needs no recursion and no stack. When the range has one item, it is the answer.

## Example

Find the median, $k = 5$, of $A = [7, 2, 9, 4, 1, 8, 3, 6, 5]$, so $t = 4$. Assume that line L3 picks the items 8, 3, 6 and 4 as the pivots, in this order. A partition of a range of $m$ items makes $m - 1$ comparisons.

| step | range $[lo, hi)$ | pivot | array after PARTITION | $p$ | comparisons | next range |
|---|---|---|---|---|---|---|
| 1 | $[0, 9)$ | 8 | [7 2 4 1 5 3 6 **8** 9] | 7 | 8 | $t < p$: $[0, 7)$ |
| 2 | $[0, 7)$ | 3 | [2 1 **3** 7 5 6 4 8 9] | 2 | 6 | $t > p$: $[3, 7)$ |
| 3 | $[3, 7)$ | 6 | [2 1 3 5 4 **6** 7 8 9] | 5 | 3 | $t < p$: $[3, 5)$ |
| 4 | $[3, 5)$ | 4 | [2 1 3 **4** 5 6 7 8 9] | 3 | 1 | $t > p$: $[4, 5)$ |

The last range has one item, so line L9 returns $A[4] = 5$. The run made $8 + 6 + 3 + 1 = 18$ comparisons. A sort of 9 items needs at least $\lceil \lg 9! \rceil = 19$ comparisons in the worst case. With pivots chosen at random, the expected number of comparisons for $n = 9$ and $k = 5$ is $10487/630 \approx 16.6$, and for large $n$ it is about $3.39n$ for the median.

## Correctness

The loop of line L2 keeps this [loop invariant](/loop-invariant/): $lo \le t < hi$; each item of $A[0 \ldots lo-1]$ is at most each item of $A[lo \ldots hi-1]$; each item of $A[lo \ldots hi-1]$ is at most each item of $A[hi \ldots n-1]$; and $A$ is a permutation of the input. Under this invariant, the item of sorted index $t$ of the whole array is the item of sorted index $t - lo$ of the block $A[lo \ldots hi-1]$. PARTITION keeps the invariant, and each pass removes at least the pivot from the range, so the loop ends. At the end, either $t = p$ and the pivot is in its sorted place, or the range is the single index $t$. The full proof, with the proof of PARTITION, is in the proof file below.

## Complexity

Let $C$ be the number of comparisons. Each pass of the loop with a range of $m$ items makes $m - 1$ comparisons in line L13 and $O(m)$ other work, so the time is $\Theta(C + 1)$ plus $\Theta(1)$ per pass.

- **Worst case, $\Theta(n^2)$.** If each pivot is the largest item of the range and $k = 1$, the range shrinks by one item per pass. The comparisons are $(n-1) + (n-2) + \cdots + 1 = n(n-1)/2$. Since each pass makes at most $n - 1$ comparisons and there are at most $n - 1$ passes, the worst case is also $O(n^2)$.
- **Expected case, $\Theta(n)$.** The expectation is over the random choices of line L3, for each fixed input of distinct items. The page [Expected linear time of randomized selection](/quickselect-expected-linear/) proves the exact value
$$ \mathbb{E}[C] = 2\bigl((n+1)H_n - (n+3-k)H_{n+1-k} - (k+2)H_k + n + 3\bigr) < 4n, $$
where $H_m$ is the $m$-th [harmonic number](/harmonic-series/). For $k = 1$ it is about $2n$, and for the median it is about $2(1 + \ln 2)n \approx 3.386n$. For example, $n = 1000$ gives $1985.0$ for $k = 1$ and $3336.3$ for $k = 500$.
- **Best case, $\Theta(n)$.** The first pass already makes $n - 1$ comparisons, and if its pivot has index $t$ the loop stops. Every correct selection algorithm must read each item, so no run takes $o(n)$ time.
- **Space, $\Theta(1)$.** The loop uses $lo$, $hi$, $t$ and the partition indices. It has no recursion.

## Properties

- **In place.** It moves items only by swaps inside $A$.
- **Not stable.** PARTITION moves equal items past each other.
- **Randomized, Las Vegas.** The answer is always correct; only the running time depends on the random choices, as in a [Las Vegas algorithm](/las-vegas-algorithm/).
- **Partial order as a by-product.** At the end, $A[k-1]$ is the answer, the items before it are at most the answer, and the items after it are at least the answer. So the $k$ smallest items are in $A[0 \ldots k-1]$, which solves [top-k selection](/top-k-selection/) at no extra cost.

## Variants and improvements

- **Recursive form.** CLRS writes the same method as the recursive RANDOMIZED-SELECT; see [randomized quickselect](/randomized-quickselect/). The recursion is a tail call, so the loop above is equivalent.
- **Three-way partition.** Split the range into the items less than, equal to, and greater than the pivot, as in the [Dutch national flag](/dutch-national-flag/) problem. Then many equal keys do not slow the method down, and the loop can stop as soon as $t$ falls in the middle block.
- **Better pivots.** A median of three, or the median of a small random sample, gives a pivot nearer the middle. The [Floyd-Rivest algorithm](/floyd-rivest-select/) takes this to its limit and makes $n + \min(k, n-k) + o(n)$ comparisons in expectation.
- **A guaranteed pivot.** [Median of medians](/median-of-medians/) picks a pivot that is never in the outer 30 percent, which gives $O(n)$ time in the worst case, but with a larger constant. [Introselect](/introselect/) starts as quickselect and switches to median of medians only when the ranges do not shrink fast enough.
- **Hoare partition.** The [Hoare partition](/hoare-partition/) scans from both ends and makes fewer swaps. Hoare's original FIND used this kind of scan.

## When to use it

Use quickselect when you need one order statistic, or the $k$ smallest items in any order, from data in memory, and an expected linear time is enough. It is simple, in place and fast in practice. If an adversary can choose the input and the random choices are predictable, or you need a guaranteed bound, use [introselect](/introselect/) or [median of medians](/median-of-medians/). If you need many order statistics of the same data, sort once, or use [multiple selection](/multiple-selection/). For the $k$ smallest of a stream, use [heap-based selection](/heap-select/).

## Pitfalls

- **A fixed pivot.** The deterministic pivot $A[hi-1]$, without lines L3 and L4, takes $\Theta(n^2)$ time on a sorted input with $k = 1$, and sorted inputs are frequent. Keep the random swap of lines L3 and L4.
- **Many equal keys.** With the test $A[j] \le x$ of line L13, an array of $n$ equal items puts each pivot at the right end, and the run takes $\Theta(n^2)$ time even with random pivots. Use a three-way partition when the keys can repeat a lot.
- **Rank against index.** The rank $k$ starts at 1, the index $t$ at 0. Comparing $k$ with $p$ in line L6 instead of $t$ returns the wrong item. The test with $k = 1$ and $k = n$ catches this.
- **An empty range.** Line L7 sets $hi \leftarrow p$, not $p - 1$, because the range is half-open. With $hi \leftarrow p - 1$, the item at $p - 1$ is lost and the result can be wrong.

## Implementations

## History

C. A. R. Hoare published FIND as Algorithm 65 in the Communications of the ACM in July 1961, in the same issue as his Partition (Algorithm 63) and Quicksort (Algorithm 64). Blum, Floyd, Pratt, Rivest and Tarjan gave a pivot rule with a linear worst case in 1973, and Floyd and Rivest gave a sampling method with a near-optimal expected number of comparisons in 1975.

## References
