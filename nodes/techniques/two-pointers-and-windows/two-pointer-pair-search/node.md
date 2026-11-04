---
tag: XYYCS4
kind: algorithm
slug: two-pointer-pair-search
name: Two-pointer pair search
aliases:
- two-sum two-pointer scan
area: techniques/two-pointers-and-windows
level: intro
summary: Start pointers at both ends and move the one that makes the sum too small or too large; runs in O(n).
solves: [two-sum-sorted]
model: word-ram
complexity:
  vars: {n: the number of items in the array}
  time: {worst: Θ(n), average: Θ(n), best: Θ(1)}
  space: {extra: Θ(1)}
properties: {stable: false, in_place: true, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
prereqs: [two-pointers, loop-invariant, binary-search]
see_also: [two-sum-sorted, three-sum-two-pointer-scan, 3sum, k-sum, container-with-most-water, hash-table, monotone-window-property]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 2, exercises of Section 2.3 (decide in Θ(n lg n) time if two items of a set sum to x)
  - book: isbn:9783030542559
    title: Steven S. Skiena, The Algorithm Design Manual, third edition
    locator: Chapter 4, Sorting (applications of sorting)
  - book: isbn:9780201657883
    title: Jon Bentley, Programming Pearls, second edition
    locator: Column 8, Algorithm design techniques (scanning algorithms)
---

Two-pointer pair search decides if a sorted array holds two items, at different positions, whose sum is a target $t$. It puts one pointer at each end of the array, and at each step it moves the pointer whose item makes the sum too small or too large. It solves the [two sum problem on a sorted array](/two-sum-sorted/) in $\Theta(n)$ time and $\Theta(1)$ extra space, and it is the inner loop of the quadratic [3SUM](/3sum/) algorithm. It is the first example of the [two-pointer technique](/two-pointers/).

## In plain words

The numbers are in order, from small to large. Put your left hand on the smallest number and your right hand on the largest. Add the two numbers.

If the sum is too small, the left number cannot be part of any answer: even the largest partner that is left does not make it big enough. So move the left hand one step to the right. If the sum is too large, the right number cannot be part of any answer, for the same reason with the smallest partner. So move the right hand one step to the left. If the sum is right, stop.

Each step throws away one number for good. So the search ends after fewer steps than there are numbers.

## The problem

The input is an array $A[0 \ldots n-1]$ of numbers in non-decreasing order, $A[0] \le A[1] \le \cdots \le A[n-1]$, and a target $t$. The output is a pair of indices $(i, j)$ with $0 \le i < j \le n-1$ and $A[i] + A[j] = t$, or NIL if no such pair exists. This is the [two sum problem on a sorted array](/two-sum-sorted/), which also gives the variants and the lower bound.

## The algorithm

```pseudo id=main
PAIR-SEARCH(A, t)                       ▷ A[0 .. n − 1] sorted, non-decreasing
L1  lo ← 0, hi ← n − 1
L2  while lo < hi do
L3      s ← A[lo] + A[hi]
L4      if s = t then return (lo, hi)
L5      if s < t then lo ← lo + 1          ▷ A[lo] is too small for every partner left
L6      else hi ← hi − 1                   ▷ A[hi] is too large for every partner left
L7  return NIL
```

The pair $(lo, hi)$ is the only pair that the loop looks at in one step. Think of the $n \times n$ table of sums $A[i] + A[j]$ with $i < j$. Rows grow to the right and columns grow downward, because $A$ is sorted. The pair $(lo, hi)$ is the top right corner of the part of the table that is still open. If the corner is too small, the whole row $lo$ in the open part is too small, because the corner is the largest entry of the row. If the corner is too large, the whole column $hi$ in the open part is too large, because the corner is the smallest entry of the column. So each step closes one row or one column.

## Example

Search $A = [1, 3, 4, 6, 8, 11, 14, 17]$ for $t = 22$.

| step | $lo$ | $hi$ | $A[lo]$ | $A[hi]$ | $s$ | action |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 7 | 1 | 17 | 18 | $s < t$, so $lo \leftarrow 1$ |
| 2 | 1 | 7 | 3 | 17 | 20 | $s < t$, so $lo \leftarrow 2$ |
| 3 | 2 | 7 | 4 | 17 | 21 | $s < t$, so $lo \leftarrow 3$ |
| 4 | 3 | 7 | 6 | 17 | 23 | $s > t$, so $hi \leftarrow 6$ |
| 5 | 3 | 6 | 6 | 14 | 20 | $s < t$, so $lo \leftarrow 4$ |
| 6 | 4 | 6 | 8 | 14 | 22 | found $(4, 6)$ |

The pair $(4, 6)$ gives $8 + 14 = 22$. In step 4 the item 17 leaves for good: its smallest partner that is left is 6, and $6 + 17 = 23$ is already too large. On the same array, the target $t = 24$ has no pair, and the loop stops after 7 steps with $lo = hi = 5$.

## Correctness

The loop keeps this [loop invariant](/loop-invariant/):

> **(P)** $0 \le lo \le hi + 1 \le n$, and for each pair $(i, j)$ with $i < j$ and $A[i] + A[j] = t$, there is a pair $(i', j')$ with $lo \le i' < j' \le hi$ and $A[i'] + A[j'] = t$.

In words: if a solution exists, one still lies inside the open range. The key step is line L5. If $A[lo] + A[hi] < t$, then each $j$ with $lo < j \le hi$ has $A[lo] + A[j] \le A[lo] + A[hi] < t$, so no solution in the range uses $lo$, and removing $lo$ loses nothing. Line L6 is the mirror case. When the loop stops with $lo \ge hi$, the range holds no pair, so by (P) no solution exists, and NIL is right. Each pair that line L4 returns is a solution with $lo < hi$. The full proof, with the bound on the number of steps, is in the proof below.

## Complexity

- **Steps.** Each iteration that does not return decreases $hi - lo$ by exactly 1. The value starts at $n - 1$ and the loop runs only while it is at least 1. So the loop runs at most $n - 1$ times, and exactly $n - 1$ times when no pair exists.
- **Time.** Each iteration does one addition and at most two comparisons. The worst case is $\Theta(n)$. The best case is $\Theta(1)$, when $A[0] + A[n-1] = t$. On an input with no pair the time is $\Theta(n)$ whatever the values are.
- **Space.** Two indices and one sum: $\Theta(1)$ extra words.
- **Sorting first.** On an unsorted input, sort first in $O(n \log n)$ time. In the [comparison model](/comparison-model/) the sort then dominates. A [hash table](/hash-table/) of the items seen so far solves the unsorted version in $O(n)$ expected time instead.

The bound is optimal for a sorted input: the [two sum problem on a sorted array](/two-sum-sorted/) page shows that each correct algorithm must read $\Omega(n)$ items in the worst case.

## Properties

- **In place and read only.** The algorithm reads $A$ and does not write to it.
- **Deterministic.** Its path depends only on the signs of $A[lo] + A[hi] - t$.
- **Which pair it finds.** With several solutions, it does not always return the one with the smallest $i$. On $A = [1, 2, 3, 4]$ and $t = 5$ it returns $(0, 3)$ at once, and $(1, 2)$ is a second solution.
- **Duplicates.** Equal items at different positions are allowed. For $A = [5, 5]$ and $t = 10$ the answer is $(0, 1)$. The test $lo < hi$ forbids the use of one position twice.

## Variants and improvements

- **All pairs, or the number of pairs.** After a match, the items equal to $A[lo]$ and the items equal to $A[hi]$ form two blocks. If $A[lo] \ne A[hi]$ and the blocks have sizes $a$ and $b$, they give $ab$ pairs. If $A[lo] = A[hi]$, every pair inside the block $A[lo \ldots hi]$ is a match, which gives $\binom{hi - lo + 1}{2}$ pairs, and the scan stops. Skip both blocks and go on. The time stays $\Theta(n)$ for the count, and is $\Theta(n + k)$ to list $k$ pairs.
- **Pairs with sum less than $t$.** If $A[lo] + A[hi] < t$, then $lo$ forms a pair with each of $lo + 1, \ldots, hi$: add $hi - lo$ to the count and move $lo$. Else move $hi$. This counts all such pairs in $\Theta(n)$ time.
- **Closest sum.** Record $|A[lo] + A[hi] - t|$ at each step and move the pointers as in lines L5 and L6. The same invariant, with "a pair at distance at most the best so far", shows that the closest pair is seen.
- **Difference instead of sum.** For $A[j] - A[i] = t$ with $t \ge 0$, both pointers start at the left and move to the right. This is the same-direction form of the [technique](/two-pointers/).
- **Binary search.** For each $i$, [binary search](/binary-search/) for $t - A[i]$ in $A[i+1 \ldots n-1]$. This takes $\Theta(n \log n)$ time. It is slower, but it adapts to a range of targets and to a short first array.
- **Three and more items.** Fix the smallest item and run this search on the rest: [3SUM by two-pointer scan](/three-sum-two-pointer-scan/) in $\Theta(n^2)$ time, and the [k-sum](/k-sum/) generalization in $O(n^{k-1})$ time.

## When to use it

Use it when the array is already sorted, or when you must sort it for another reason, and when you want $O(1)$ extra space. If the input is unsorted and you need only one pass, use a [hash table](/hash-table/) of the items seen so far: $O(n)$ expected time, but $\Theta(n)$ extra space and no worst-case guarantee. If you need the original indices of an unsorted input, sort pairs (value, index) and run the scan on them.

## Pitfalls

- **The loop test.** Writing $lo \le hi$ in line L2 allows $lo = hi$, and then the algorithm reports a single item used twice, for example $(2, 2)$ for $A = [1, 3, 5]$ and $t = 10$. The right test is $lo < hi$.
- **Moving both pointers.** After a mismatch, moving both $lo$ and $hi$ can skip the answer. On $A = [1, 4, 6, 9]$ and $t = 5$, the first sum is $10 > 5$; moving both gives the range $[1, 2]$, and the pair $(0, 1)$ is lost. Move exactly one pointer, as in lines L5 and L6.
- **The wrong pointer.** If $s < t$, move $lo$ up, not $hi$ down. Moving $hi$ down makes the sum smaller, and the proof of (P) no longer applies.
- **Overflow.** In a language with fixed-size integers, $A[lo] + A[hi]$ can overflow. Compare $A[lo]$ with $t - A[hi]$ when the range of the values allows it, or use a wider type.
- **Unsorted input.** On an unsorted array the scan can miss a pair. On $[3, 1, 2]$ with $t = 3$ it first sees $3 + 2 = 5 > 3$, then $3 + 1 = 4 > 3$, and stops without the pair $(1, 2)$.

## Implementations

## History

The problem of testing if two items of a set sum to a given value appears as an exercise in CLRS Chapter 2, with a $\Theta(n \lg n)$ bound that comes from sorting first. Skiena lists the scan among the applications of sorting. The scan from both ends has no single known inventor; it is part of the folklore of the two-pointer technique.

## References
