---
tag: 8VZBMV
kind: technique
slug: two-pointers
name: Two pointers
aliases:
- two-pointer technique
- opposite-ends pointers
area: techniques/two-pointers-and-windows
level: intro
summary: Scan an array or list with two indices that move monotonically, giving linear time for pair and range problems.
prereqs: [loop-invariant, binary-search]
see_also: [sliding-window, monotone-window-property, two-pointer-pair-search, fast-and-slow-pointers, dutch-national-flag-algorithm, sorted-array-intersection, container-with-most-water, three-sum-two-pointer-scan]
sources:
  - book: isbn:9780132158718
    title: Edsger W. Dijkstra, A Discipline of Programming, Prentice-Hall, 1976
    locator: Chapter 14, The problem of the Dutch national flag
  - book: isbn:9780201657883
    title: Jon Bentley, Programming Pearls, second edition
    locator: Column 8 (Algorithm design techniques, the scanning algorithm) and Column 11 (Sorting, the partition loops of quicksort)
  - book: isbn:9783030542559
    title: Steven S. Skiena, The Algorithm Design Manual, third edition
    locator: Chapter 4, Sorting (applications of sorting)
  - url: https://cp-algorithms.com/others/tortoise_and_hare.html
    title: cp-algorithms, Floyd's linked list cycle finding algorithm
    locator: sections Proposed algorithm and Why does it work
---

The two-pointer technique scans a sequence with two indices that only move in one direction each, and uses an argument about the order of the data to decide which index to move at each step. Since each index crosses the sequence at most once, the scan does $O(n)$ steps where a search over all pairs does $\Theta(n^2)$. The technique has three main shapes: two indices that move toward each other from the ends (the [pair search](/two-pointer-pair-search/)), two indices that move in the same direction at different rates (read and write pointers, merges, [fast and slow pointers](/fast-and-slow-pointers/)), and the [sliding window](/sliding-window/), whose two ends bound a range. Its correctness always rests on one [loop invariant](/loop-invariant/): each move drops only candidates that cannot be part of an optimal answer.

## In plain words

Many problems ask for the best pair of positions in a list: two numbers with a given sum, two walls that hold the most water, the longest stretch with some property. Trying every pair takes time that grows with the square of the list length.

Two pointers do better when the list has an order that lets you rule out a whole group of pairs with one look. You keep two markers. At each step you look at the two items under them, and you move one marker forward. The move is safe when you can prove that the item you leave behind cannot be part of any better answer with the items that are still ahead. Since the markers never move back, each one crosses the list once, and the total work is about the length of the list.

## When it applies

- **The input is sorted, or can be sorted.** Then the sum or the difference of two items grows when one index moves right and falls when the other moves left. Pair search, [3SUM](/three-sum-two-pointer-scan/) and [sorted intersection](/sorted-array-intersection/) use this.
- **The answer is a pair $(i, j)$ and a test at $(i, j)$ rules out a full row or column.** A test that says "every pair $(i, j')$ with $j' \le j$ is no better" lets you drop $i$. This is the case of the [container with most water](/container-with-most-water/).
- **The answer is a contiguous range, and the property of a range is monotone.** If a range is good, every range inside it is good (or every range around it). Then the valid starts for each end form an interval that moves right. This is the [monotone window property](/monotone-window-property/), and the technique becomes a [sliding window](/sliding-window/).
- **An in-place rewrite of an array.** One index reads, another writes, and the write index never passes the read index. [Remove duplicates](/remove-duplicates-from-sorted-array/), partition and compaction use this.
- **A sequence defined by a function $x_{i+1} = f(x_i)$.** Two pointers at different speeds meet inside a cycle. This is [fast and slow pointers](/fast-and-slow-pointers/).
- **Signals that it does not apply.** Negative numbers in a sum window, an unsorted input with no cheap sort, or a property that is not monotone. Then a pointer move can drop the optimum, and you need [prefix sums](/prefix-sums/) with a hash table, a deque, or a full search.

## The template

The opposite-ends form, with the holes to fill named in capitals:

```pseudo id=main
TWO-POINTERS(A[0 .. n − 1])
L1  i ← 0, j ← n − 1, best ← NONE
L2  while i < j do
L3      best ← BETTER(best, VALUE(i, j))          ▷ hole: what a pair is worth
L4      if DONE(i, j) then return best             ▷ hole: early exit, if any
L5      if DROP-LEFT(i, j) then i ← i + 1          ▷ hole: i cannot pair with any j' in (i, j]
L6      else j ← j − 1                             ▷ then j cannot pair with any i' in [i, j)
L7  return best
```

**The invariant to prove.** For the pairs $(i, j)$ with $0 \le i < j \le n-1$, let $\mathrm{OPT}$ be the best value. The loop must keep:

> **(T)** Either $best$ already equals $\mathrm{OPT}$, or some optimal pair $(p, q)$ has $i \le p < q \le j$.

**What the holes must satisfy.** Line L5 keeps (T) if DROP-LEFT$(i, j)$ is true only when no pair $(i, q)$ with $i < q \le j$ is better than $best$ after line L3. Line L6 keeps (T) if, when DROP-LEFT is false, no pair $(p, j)$ with $i \le p < j$ is better than $best$. In the table of all pairs, the open pairs are the triangle above the diagonal with rows $i$ to $j$ and columns $i$ to $j$; the pair $(i, j)$ is its top right corner. Line L5 removes row $i$ of the triangle, and line L6 removes column $j$. So each step must show that the corner decides the whole row or the whole column. For a sum on a sorted array, the corner is the largest entry of its row and the smallest entry of its column, and this is exactly the test $A[i] + A[j] < t$.

**Termination and cost.** Each iteration decreases $j - i$ by exactly 1, from $n - 1$ to 0. So there are at most $n - 1$ iterations, and the time is $O(n)$ times the cost of the holes. When the loop stops, the triangle is empty, so by (T) $best = \mathrm{OPT}$.

**The same-direction form.** Both indices start at the left. A *read* index $r$ visits each item, and a *write* or *slow* index $w \le r$ marks the end of the output or the start of a window. The invariant describes the prefix $A[0 \ldots w-1]$ in terms of $A[0 \ldots r-1]$, for example "the distinct values of $A[0 \ldots r-1]$, in order". The cost is $O(n)$ because $r$ moves $n$ times and $w$ moves at most $n$ times. The [sliding window](/sliding-window/) page gives the window form of this template.

## Classic examples

From simple to hard:

- **[Two sum on a sorted array](/two-sum-sorted/)** by [two-pointer pair search](/two-pointer-pair-search/). VALUE is the test $A[i] + A[j] = t$ and DROP-LEFT is $A[i] + A[j] < t$. It needs $n - 1$ steps, and every algorithm must read all $n$ items.
- **[Remove duplicates from a sorted array](/remove-duplicates-from-sorted-array/).** Same direction: the write index $w$ keeps the distinct values seen so far, and the read index adds $A[r]$ when it differs from $A[w - 1]$.
- **[Intersection of sorted arrays](/sorted-array-intersection/).** One index in each array; move the one at the smaller value, since that value has no partner left in the other array.
- **[Container with most water](/container-with-most-water/).** VALUE is $(j - i) \min(h_i, h_j)$ and DROP-LEFT is $h_i \le h_j$: a pair $(i, q)$ with $q < j$ is narrower and no taller than $h_i$.
- **[Trapping rain water](/trapping-rain-water/).** Move the side with the lower running maximum; the water above that bar is then known exactly.
- **[Dutch national flag](/dutch-national-flag-algorithm/).** Three indices split the array into four regions; Dijkstra's invariant is the model for all in-place partition loops, such as [Hoare partition](/hoare-partition/).
- **[3SUM](/three-sum-two-pointer-scan/).** Fix one item, and run the pair search on the rest: $\Theta(n^2)$ in total.
- **[Fast and slow pointers](/fast-and-slow-pointers/).** One index moves one step and the other two steps along $x_{i+1} = f(x_i)$; they meet inside the cycle.
- **[Sliding window](/sliding-window/) problems.** [Minimum size subarray sum](/minimum-size-subarray-sum/), [longest substring without repeating characters](/longest-substring-without-repeating-characters/) and [minimum window substring](/minimum-window-substring/) move a left and a right end of a window.

## Variations

- **Opposite ends.** The indices start at $0$ and $n - 1$ and meet. Pair problems on sorted data and problems where the width of a pair matters.
- **Same direction, reader and writer.** In-place filters, compaction and partition. The writer never passes the reader, so no item is overwritten before it is read.
- **Two sequences.** One index in each of two sorted sequences, as in the merge of [merge sort](/merge-sort/), [merging sorted lists](/merging-sorted-lists/) and [interval list intersection](/interval-list-intersection-two-pointers/).
- **Window.** Both indices move right, and the range between them is the object; see the [sliding window](/sliding-window/) and the [monotone window property](/monotone-window-property/).
- **Different speeds.** Fast and slow pointers on a linked list or a functional graph find a cycle, its start and its length, or the middle of a list.
- **More than two pointers.** Three or four indices, as in the Dutch national flag, or $k - 2$ fixed indices and a pair search for [k-sum](/k-sum/).
- **Pointers plus binary search.** When only one index has a monotone rule, binary search for the other one costs $O(\log n)$ per step. Two pointers replace the search when the other index is also monotone.

## Pitfalls

- **A move without a proof.** The common bug is a move that looks natural but can drop the optimum. For each move, write the sentence "no pair that uses the index I drop is better than what I have", and check it against the order of the data.
- **Moving both pointers on a mismatch.** In the pair search, moving $i$ and $j$ together skips the pairs $(i, j - 1)$ and $(i + 1, j)$. On $[1, 4, 6, 9]$ with target 5 it loses the pair $(0, 1)$.
- **Off-by-one at the meeting point.** The test $i < j$ forbids a pair of one index with itself; $i \le j$ allows it. Choose by the problem.
- **No order to use.** On unsorted data or with negative values in a sum window, the monotone argument fails and the scan can give a wrong answer without any error.
- **Null checks in pointer chasing.** With fast and slow pointers on a list without a cycle, the fast pointer must test its next node before it moves two steps.

## Exercises

1. Given a sorted array $A$ and a value $t \ge 0$, decide in $O(n)$ time if there are indices $i < j$ with $A[j] - A[i] = t$. State the invariant and prove that no answer is skipped.
2. Given a sorted array of integers, return the sorted array of their squares in $O(n)$ time. (Hint: the largest square is at one of the two ends.)
3. Count the pairs $i < j$ of a sorted array with $A[i] + A[j] < t$ in $O(n)$ time.
4. Given a string, decide in $O(n)$ time if it reads the same from both ends when only letters are compared and case is ignored.
5. Give an input on which the container scan that moves the *taller* side returns a wrong answer.
6. Prove that the merge-like intersection scan does at most $m + n - 1$ comparisons, and give inputs on which it does exactly that many.

## References
