---
tag: 8E37B4
kind: problem
slug: remove-duplicates-from-sorted-array
name: Remove duplicates from a sorted array
aliases:
- in-place deduplication
area: techniques/two-pointers-and-windows
level: intro
summary: Compact a sorted array in place so each distinct value appears once, using a read pointer and a write pointer.
prereqs: [two-pointers, loop-invariant]
see_also: [two-finger-compaction, dedup, element-distinctness, duplicate-detection, hash-table, sorted-array-intersection, in-place-algorithm, adversary-argument]
sources:
  - url: https://leetcode.com/problems/remove-duplicates-from-sorted-array/
    title: LeetCode, problem 26, Remove Duplicates from Sorted Array
    locator: problem statement
  - url: https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/
    title: LeetCode, problem 80, Remove Duplicates from Sorted Array II
    locator: problem statement (keep at most two copies)
  - book: isbn:9783030542559
    title: Steven S. Skiena, The Algorithm Design Manual, third edition
    locator: Chapter 4, Sorting (applications of sorting, uniqueness testing and removing duplicates)
---

The problem of removing duplicates from a sorted array asks to rewrite the array in place so that its first $k$ cells hold the $k$ distinct values in sorted order, and to return $k$. A read pointer and a write pointer solve it with $n - 1$ comparisons, $\Theta(n)$ time and $O(1)$ extra space, and every comparison-based algorithm needs $n - 1$ comparisons on some input. It is the simplest example of the same-direction form of the [two-pointer technique](/two-pointers/), and the model for [two-finger compaction](/two-finger-compaction/).

## In plain words

You have a sorted row of numbers, and equal numbers stand next to each other. You want to keep one copy of each number at the front of the row, in order, without a second row.

Use two fingers. The reading finger walks over every number. The writing finger marks where the next kept number goes. When the reading finger finds a number that differs from the last kept number, it is a new number, so copy it to the writing finger and move the writing finger by one. When it is the same as the last kept number, it is a copy, so skip it. Because the row is sorted, a number that equals none of the kept numbers must differ from the last one, so this one check is enough.

## Definition

**Input.** An array $A[0 \ldots n-1]$ sorted in non-decreasing order.

**Output.** The number $k$ of distinct values in $A$. On return, $A[0 \ldots k-1]$ holds these values in increasing order. The cells $A[k \ldots n-1]$ may hold any values.

**Model.** The algorithm may compare two items for equality or order, copy items between cells, and use $O(1)$ extra cells. The cost is the number of comparisons; the time is $\Theta$ of the number of steps.

## Variants

- **Keep at most $c$ copies.** Each value stays $\min(\text{count}, c)$ times. The write test becomes $w < c$ or $A[r] \ne A[w - c]$. For $c = 2$ this is LeetCode problem 80.
- **Remove all values that repeat.** Keep only the values that appear exactly once. Compare $A[r]$ with both neighbors $A[r-1]$ and $A[r+1]$ in the original array, or process each run of equal items as a block.
- **Unsorted input.** Sort first, in $O(n \log n)$ time, or use a [hash table](/hash-table/) of seen values in $O(n)$ expected time; the hash method keeps the first copy of each value in input order. See [dedup](/dedup/).
- **Sorted linked list.** Same idea with one pointer: if a node has the same value as its next node, unlink the next node.
- **Count only.** Return $k$ without moving items. This is the number of $r \ge 1$ with $A[r] \ne A[r-1]$, plus 1 for $n \ge 1$.

## Examples

**Keep one copy.** $A = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]$, so $n = 10$ and $k = 5$. The write pointer starts at $w = 1$, since $A[0]$ is always kept.

| $r$ | $A[r]$ | $A[w-1]$ | action | $w$ after | $A[0 \ldots w-1]$ |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | skip | 1 | $[0]$ |
| 2 | 1 | 0 | write | 2 | $[0, 1]$ |
| 3 | 1 | 1 | skip | 2 | $[0, 1]$ |
| 4 | 1 | 1 | skip | 2 | $[0, 1]$ |
| 5 | 2 | 1 | write | 3 | $[0, 1, 2]$ |
| 6 | 2 | 2 | skip | 3 | $[0, 1, 2]$ |
| 7 | 3 | 2 | write | 4 | $[0, 1, 2, 3]$ |
| 8 | 3 | 3 | skip | 4 | $[0, 1, 2, 3]$ |
| 9 | 4 | 3 | write | 5 | $[0, 1, 2, 3, 4]$ |

The scan does 9 comparisons and 4 writes.

**Keep at most two copies.** $A = [0, 0, 1, 1, 1, 1, 2, 3, 3]$ gives $k = 7$ and $A[0 \ldots 6] = [0, 0, 1, 1, 2, 3, 3]$. $A = [1, 1, 1, 2, 2, 3]$ gives $k = 5$ and $[1, 1, 2, 2, 3]$.

**Edge cases.** The empty array gives $k = 0$. An array with all items equal gives $k = 1$. An array with all items different gives $k = n$ and is not changed.

## Known algorithms

**Read and write pointers.** If $n = 0$, return 0. Set $w \leftarrow 1$. For $r = 1, \ldots, n - 1$: if $A[r] \ne A[w - 1]$, set $A[w] \leftarrow A[r]$ and $w \leftarrow w + 1$. Return $w$.

Write $A_0$ for the input array, before any write. At each test of the loop, with $1 \le r \le n$:

> **(D)** $1 \le w \le r$; $A[0 \ldots w-1]$ is the list of the distinct values of $A_0[0 \ldots r-1]$ in increasing order; $A[w-1] = A_0[r-1]$; and $A[r \ldots n-1] = A_0[r \ldots n-1]$.

*Initialization.* With $r = w = 1$, the prefix $A_0[0 \ldots 0]$ has the single distinct value $A_0[0] = A[0]$.

*Why no distinct value is skipped.* Let $x = A[r] = A_0[r]$, which is not yet changed by (D). All values of $A_0[0 \ldots r-1]$ are at most $A_0[r-1] = A[w-1]$, because $A_0$ is sorted. If $x = A[w-1]$, then $x$ is already in the output, and skipping it keeps (D) with $r + 1$. If $x \ne A[w-1]$, then $x > A_0[r-1]$, so $x$ is larger than every value of the prefix. It is a new distinct value, and it belongs at the end of the sorted output. The write puts it at position $w$, and the new last item $A[w] = x = A_0[r]$. The write is safe because $w \le r$: it changes cell $w$, which is either cell $r$ itself or a cell before $r$ that the read pointer has passed, so no unread item is lost.

*End.* The loop stops with $r = n$, and (D) says that $A[0 \ldots w-1]$ is the sorted list of all distinct values. The loop does exactly $n - 1$ comparisons for $n \ge 1$, and at most $n - 1$ writes. A check $w \ne r$ before the write saves the writes on an input with no duplicates, but it does not change the order of the cost.

**Keep at most $c$ copies.** Replace the test by "$w < c$ or $A[r] \ne A[w - c]$". The invariant becomes: $A[0 \ldots w-1]$ is the sorted list in which each value $v$ of $A_0[0 \ldots r-1]$ appears $\min(\text{count of } v, c)$ times. The output is sorted, so $A[w - c] = A[r]$ holds if and only if the last $c$ output items all equal $A[r]$, which means that $A[r]$ already has $c$ copies.

**Hash set.** On unsorted input, keep a hash set of seen values and the same two pointers. This takes $O(n)$ expected time and $O(k)$ extra space.

## Bounds

**Comparisons.** The scan uses $n - 1$ comparisons, and this is optimal. Take an input with $n$ different values. Suppose that an algorithm stops without comparing some pair of neighbors $A[i] < A[i+1]$. Change $A[i+1]$ to the value of $A[i]$. The array is still sorted, and each comparison that the algorithm made has the same result, because only the order of this one pair changed. So the algorithm returns $k = n$ on an input with $n - 1$ distinct values. This [adversary argument](/adversary-argument/) shows that all $n - 1$ neighbor pairs must be compared directly.

**Time and space.** $\Theta(n)$ time and $O(1)$ extra space. For unsorted input in the comparison model, the problem is at least as hard as [element distinctness](/element-distinctness/), which needs $\Omega(n \log n)$ comparisons.

## Reductions

- **Element distinctness.** The array has duplicates if and only if the returned $k$ is less than $n$. With a sort first, this is the standard $O(n \log n)$ method for [duplicate detection](/duplicate-detection/).
- **Compaction.** Removing duplicates is compaction with the filter "differs from the last kept item". The same read and write pointers remove any items that fail a test, as in [two-finger compaction](/two-finger-compaction/), and as in the partition step of quicksort.
- **Run-length encoding.** Store the position $r$ at each write. These are the starts of the runs, and the differences of consecutive starts are the counts of the values.

## Applications

- **Set operations on sorted lists.** Sorting and then removing duplicates turns a list into a set, before a [sorted intersection](/sorted-array-intersection/) or a union.
- **Database `DISTINCT`.** A sort-based plan for `SELECT DISTINCT` sorts the rows and then runs this scan.
- **Unix `sort | uniq`.** The `uniq` program removes adjacent duplicate lines, which are all duplicates once the input is sorted.

## References
