---
tag: 5TYMK3
kind: algorithm
slug: quicksort
name: Quicksort
aliases:
- partition-exchange sort
- Hoare's sort
area: sorting/comparison-sorts
level: core
summary: Partitions around a pivot and recurses on both sides; Theta(n log n) expected and Theta(n^2) worst case.
solves: [sorting-problem]
model: comparison-model
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n²), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {stable: false, in_place: true, adaptive: false, online: false, deterministic: true, comparison: true, recursive: true}
history:
  year: 1961
  people: [C. A. R. Hoare]
  note: Hoare found quicksort in 1959 and 1960 and published it as Algorithm 64 in the Communications of the ACM in 1961, with the full paper in The Computer Journal in 1962.
prereqs: [lomuto-partition, divide-and-conquer-paradigm, loop-invariant]
see_also: [randomized-quicksort, hoare-partition, pivot-selection, three-way-quicksort, quicksort-stack-depth, quicksort-expected-running-time, introsort, merge-sort]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 7, Quicksort (Section 7.1 for the algorithm and PARTITION, Section 7.2 for the worst and best cases, Section 7.4 for the analysis)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.2, Sorting by exchanging (Algorithm Q and the analysis of its mean comparison count)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.3, Quicksort
  - paper: doi:10.1093/comjnl/5.1.10
    title: C. A. R. Hoare, Quicksort, The Computer Journal 5(1), 1962
    locator: pages 10 to 16, the whole paper
  - book: isbn:9780201657883
    title: Jon Bentley, Programming Pearls, second edition
    locator: Column 11, Sorting (the one-way partition of Nico Lomuto)
---

Quicksort sorts an array by divide and conquer: it picks one item as the *pivot*, moves the smaller items before it and the larger items after it, and then sorts the two sides. It solves the [sorting problem](/sorting-problem/) in $\Theta(n \log n)$ time on average and in the best case, but in $\Theta(n^2)$ time in the worst case. It sorts in place and is not stable. With a random pivot ([randomized quicksort](/randomized-quicksort/)) and a careful partition, it is the fastest general sort on arrays in practice, and it is the core of most library sorts of numbers.

## In plain words

You have a pile of exam papers to put in order of score. You take one paper, the pivot. You make two piles: the papers with a score not more than the pivot, and the papers with a higher score. Now the pivot goes between the two piles, and it is in its final place. It never moves again.

Then you do the same with each pile. A pile of one paper is already in order, so you stop there.

The method is fast when each pivot cuts its pile near the middle. It is slow when each pivot is the smallest or the largest paper, because then one pile is empty and the other is only one paper smaller.

## The problem

The input is an array $A[0 \ldots n-1]$ of items with a total order. The output is the same array, with its items in non-decreasing order. This is the [sorting problem](/sorting-problem/). The algorithm changes the array in place.

## The algorithm

The call QUICKSORT$(A, 0, n)$ sorts the full array. The range $[lo, hi)$ is half-open. This version uses the last item as the pivot and the [Lomuto partition](/lomuto-partition/), as in CLRS.

```pseudo id=main
QUICKSORT(A, lo, hi)                       ▷ sort A[lo .. hi − 1]
L1  if hi − lo ≤ 1 then return
L2  p ← PARTITION(A, lo, hi)
L3  QUICKSORT(A, lo, p)
L4  QUICKSORT(A, p + 1, hi)

PARTITION(A, lo, hi)                       ▷ the pivot is x = A[hi − 1]
L5  x ← A[hi − 1]
L6  i ← lo                                 ▷ A[lo .. i − 1] holds the items ≤ x
L7  for j ← lo to hi − 2 do
L8      if A[j] ≤ x then
L9          swap A[i] and A[j]
L10         i ← i + 1
L11 swap A[i] and A[hi − 1]                ▷ put the pivot between the two parts
L12 return i
```

PARTITION scans the range once from the left. It keeps the items that are at most $x$ in a growing block at the left end. When it finds such an item at $j$, it swaps it to the end of that block. At the end, line L11 puts the pivot right after the block. Then $A[lo \ldots p-1] \le x = A[p] < A[p+1 \ldots hi-1]$, and the pivot is at its final index $p$. The two calls sort the two sides. The pivot is in neither call, so each call has fewer items than the range.

QUICKSORT does no work after the calls. All the work is in PARTITION, before the calls. Merge sort is the opposite: it splits for free and does its work in the merge.

## Example

Sort $A = [6, 3, 9, 1, 7, 2, 8, 5]$. Each row is one call of PARTITION. The pivot is the last item of the range.

| range | the range before | pivot | the range after | $p$ |
|---|---|---|---|---|
| $[0, 8)$ | 6 3 9 1 7 2 8 5 | 5 | 3 1 2 **5** 7 9 8 6 | 3 |
| $[0, 3)$ | 3 1 2 | 2 | 1 **2** 3 | 1 |
| $[4, 8)$ | 7 9 8 6 | 6 | **6** 9 8 7 | 4 |
| $[5, 8)$ | 9 8 7 | 7 | **7** 8 9 | 5 |
| $[6, 8)$ | 8 9 | 9 | 8 **9** | 7 |

The result is $[1, 2, 3, 5, 6, 7, 8, 9]$. The first partition is a good split, 3 items against 4. The calls on $[4, 8)$ and $[5, 8)$ are bad splits: the pivot is the smallest item, so the left side is empty. The run makes $7 + 2 + 3 + 2 + 1 = 15$ comparisons.

## Correctness

PARTITION is correct by a [loop invariant](/loop-invariant/) of line L7: before the step for $j$, each item of $A[lo \ldots i-1]$ is at most $x$, each item of $A[i \ldots j-1]$ is larger than $x$, and $A[hi-1] = x$. The [Lomuto partition](/lomuto-partition/) page proves it. At the end, $j = hi - 1$, and line L11 gives

$$A[lo \ldots p-1] \le A[p] = x < A[p+1 \ldots hi-1].$$

QUICKSORT is then correct by strong induction on the length $hi - lo$. A range of length 0 or 1 is sorted. For a longer range, both calls get a shorter range and sort it. Each item on the left is at most $x$, and each item on the right is larger, so the full range is sorted. The full proof is below.

## Complexity

Let $C(m)$ count the comparisons on a range of $m$ items. PARTITION on $m \ge 2$ items makes exactly $m - 1$ comparisons, one for each item other than the pivot, and does $O(m)$ other work. If the pivot has rank $k + 1$ in its range (so $k$ items go left), then

$$C(m) = (m - 1) + C(k) + C(m - 1 - k), \qquad C(0) = C(1) = 0.$$

The running time is $\Theta(n + C(n))$, so it is enough to count comparisons.

**Each comparison is with a pivot.** Draw the *pivot tree*: the pivot of a call is a node, and the pivots of its two calls are its children. Each item is a pivot of one call or is alone in a range of one item, so each item is one node. An item $y$ is compared with the pivot of each call whose range holds $y$ and whose pivot is not $y$, and these pivots are the proper ancestors of $y$ in the tree. So $C(n)$ is the sum of the depths of all nodes of the pivot tree, which is its *internal path length*.

**Worst case $\Theta(n^2)$.** List the nodes of the pivot tree in order of depth. Each proper ancestor of the $k$-th node has a smaller depth, so it comes before it in the list. So the $k$-th node has depth at most $k - 1$, and $C(n) \le \sum_{k=1}^{n} (k - 1) = n(n-1)/2$. A sorted input reaches this bound: the pivot $A[hi - 1]$ is the largest item, the right side is empty, and $C(n) = (n - 1) + C(n - 1) = n(n-1)/2$. A reversed input or an input of equal items also reaches it.

**Best case $\Theta(n \log n)$.** A binary tree with $n$ nodes has at most $2^d$ nodes at depth $d$. So the $k$-th node in order of depth has depth at least $\lfloor \lg k \rfloor$, and

$$C(n) \ge \sum_{k=1}^{n} \lfloor \lg k \rfloor \ge n \lg n - 3n \quad \text{for } n \ge 1.$$

The second step follows from $\lfloor \lg k \rfloor \ge \lg k - 1$ and $\sum_{k=1}^n \lg k = \lg n! \ge n \lg n - n \lg e$, with $1 + \lg e < 3$. A pivot that is the median of its range at each step gives $C(n) \le n \lg n$, so the best case is $\Theta(n \log n)$.

**Average case $\Theta(n \log n)$.** On a uniformly random permutation of $n$ distinct keys, the mean number of comparisons is

$$\bar C(n) = 2(n+1)H_n - 4n = 2n \ln n - (4 - 2\gamma)n + O(\log n) \approx 1.386\, n \lg n,$$

where $H_n$ is the $n$-th [harmonic number](/harmonic-series/). For $n = 10$ this is $24.44$, against $n(n-1)/2 = 45$ in the worst case. For $n = 1000$ it is $10{,}986$, against $499{,}500$. The proof is on the page [expected running time of randomized quicksort](/quicksort-expected-running-time/): the same pair argument applies, because on a random input the pivot of each call is a uniform item of its range. This holds because the Lomuto partition keeps each side in a uniformly random order, given the set of its items. Knuth (Section 5.2.2) and CLRS (Section 7.4) give the derivation by the recurrence.

**Space.** PARTITION uses $O(1)$ extra space. The recursion stack has one frame for each node on a root path of the pivot tree, so its depth is $\Theta(n)$ in the worst case and $\Theta(\log n)$ in the best case. If the algorithm recurses on the smaller side and loops on the larger side, the depth is at most $\lg n$ in every case. The page [quicksort stack depth](/quicksort-stack-depth/) gives this change.

| claim | model and case | bound |
|---|---|---|
| time | comparison model, worst | $\Theta(n^2)$ |
| time | comparison model, average over uniform permutations | $\Theta(n \log n)$ |
| time | comparison model, best | $\Theta(n \log n)$ |
| extra space | the stack, worst | $\Theta(n)$ |

## Properties

- **Not stable.** The swap of line L9 can move an item past an equal item. On the input $(1, a), (1, b), (0, c)$, the pivot $(0, c)$ is swapped to the front, and $(1, a)$ goes to the end: the output is $(0, c), (1, b), (1, a)$.
- **In place.** The array is the only large memory. The stack holds $O(1)$ values for each level of the recursion.
- **Not adaptive.** A sorted input is the worst case of this version, not the best.
- **Cache friendly.** PARTITION reads and writes the range from left to right, so it uses the cache well.

## Variants and improvements

- **[Randomized quicksort](/randomized-quicksort/).** Pick the pivot uniformly at random. Then the expected time is $O(n \log n)$ on each input.
- **[Hoare partition](/hoare-partition/).** Scan from both ends and swap pairs that are on the wrong sides. It does about three times fewer swaps than Lomuto on average and splits a range of equal items in the middle.
- **[Pivot selection](/pivot-selection/).** Use the [median of three](/median-of-three-pivot/) items or [Tukey's ninther](/tukeys-ninther/) to get a pivot near the median.
- **[Three-way quicksort](/three-way-quicksort/).** Partition into the items less than, equal to and greater than the pivot. This makes the time $O(n)$ on an input of equal items.
- **[Dual-pivot quicksort](/dual-pivot-quicksort/).** Partition around two pivots into three parts. Java uses it for arrays of primitive types.
- **A cut-off to [insertion sort](/insertion-sort/).** Sort the ranges of fewer than about 10 to 20 items with insertion sort.
- **[Introsort](/introsort/).** Switch to heapsort when the depth passes $2 \lg n$. This bounds the worst case by $O(n \log n)$.
- **[Quickselect](/quickselect/).** Recurse on one side only to find the item of rank $k$, in $O(n)$ expected time.

## When to use it

Use quicksort, in its randomized or introsort form, to sort a large array in memory when stability is not necessary. Its inner loop is short and scans memory in order, so on arrays it is usually faster than [heapsort](/heapsort/) and [merge sort](/merge-sort/).

Do not use this deterministic version on input that can be sorted or chosen by an adversary. Use [merge sort](/merge-sort/) when you need a stable sort or a guaranteed $O(n \log n)$ bound, and on linked lists.

## Pitfalls

- **Sorted input is the worst case.** With the first or the last item as pivot, a sorted or a reversed input takes $n(n-1)/2$ comparisons. The fix is a random pivot or the median of three.
- **The stack overflows.** The recursion is $n - 1$ calls deep in the worst case. On a sorted array of a million items, a language with a fixed stack crashes. Recurse on the smaller side first and loop on the larger side.
- **Many equal items.** With Lomuto, an array of equal items is a worst case, because each item goes to the left side. Use the Hoare partition or the three-way partition.
- **The pivot in a call.** The calls of lines L3 and L4 must leave out the index $p$. A call on $A[lo \ldots p]$ with the Lomuto partition can repeat forever when the pivot is the largest item.
- **Comparing with <.** If line L8 tests $A[j] < x$, the sort is still correct, but now an array of equal items gives $p = lo$ in each call, and the time is still quadratic.

## Implementations

The Python version raises the recursion limit of the interpreter, because the recursion is $n - 1$ calls deep on a sorted input.

## History

C. A. R. Hoare found quicksort in 1959 and 1960, when he worked on the machine translation of Russian and needed to sort words. He published the algorithm as Algorithm 64 in the Communications of the ACM in 1961, and the full paper with the analysis of the average case in The Computer Journal in 1962. His partition scans from both ends. The one-way partition of this page is due to Nico Lomuto, as Bentley reports in Programming Pearls, and CLRS made it the standard form in textbooks. Knuth gives the exact mean $2(n+1)H_n - 4n$ and the variance in Section 5.2.2.

## References
