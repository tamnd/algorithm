---
tag: 3GT4MC
kind: technique
slug: sliding-window
name: Sliding window
aliases:
- moving window
- sliding window technique
- window
- window technique
area: techniques/two-pointers-and-windows
level: intro
summary: Maintain a contiguous window [l, r) whose endpoints only advance, updating an aggregate incrementally.
prereqs: [two-pointers, subarray, loop-invariant]
see_also: [two-pointers, monotone-window-property, sliding-window-maximum-deque, minimum-window-substring-algorithm, sliding-window-longest-substring, sliding-window-model, sliding-window-aggregation, prefix-sums]
sources:
  - url: https://cp-algorithms.com/data_structures/stack_queue_modification.html
    title: cp-algorithms, Minimum stack / Minimum queue
    locator: section Finding the minimum for all subarrays of fixed length
  - book: isbn:9780201657883
    title: Jon Bentley, Programming Pearls, second edition
    locator: Column 8, Algorithm design techniques (scanning algorithms and cumulative arrays)
  - book: isbn:9783030542559
    title: Steven S. Skiena, The Algorithm Design Manual, third edition
    locator: Chapter 3, Data structures (queues and hashing)
---

The sliding window technique solves problems about contiguous subarrays or substrings by keeping one window $A[l \ldots r]$ and a summary of its contents, such as a sum, a table of counts or a deque, and by moving the two ends only to the right. Each item enters the window once and leaves it at most once, so a scan over all useful windows costs $O(n)$ updates instead of the $\Theta(n^2)$ windows of a full search. It is the window form of the [two-pointer technique](/two-pointers/). The scan is correct when the window predicate has the [monotone window property](/monotone-window-property/): a good window stays good when it shrinks, or stays good when it grows.

## In plain words

Many questions ask about a stretch of neighbors in a list: the best sum of $k$ neighbors, the longest stretch with no repeated letter, the shortest stretch that adds up to a target. Checking every stretch is slow, because a list of length $n$ has about $n^2 / 2$ stretches.

A sliding window looks at the stretches in a smart order. It keeps one stretch, with a left and a right edge, and a short summary of what is inside. Moving the right edge adds one item to the summary; moving the left edge removes one. Neither edge ever moves back. With the right kind of question, the window still meets every stretch that could be the answer, and the total work is about two steps per item.

## When it applies

- **The answer is a contiguous range.** Subarrays and substrings, not subsequences or subsets.
- **The window summary can be updated.** Adding the item at the right and removing the item at the left each take $O(1)$ or $O(\log n)$: a sum, a count table, a number of distinct values, a [monotonic deque](/monotonic-deque/) for a maximum.
- **Fixed length.** For windows of a given length $k$ (moving averages, [window maxima](/sliding-window-maximum-deque/), anagram search), both ends move together and every window is visited. No monotone property is needed.
- **Variable length, down-closed predicate.** If every sub-window of a good window is good ("at most $k$ distinct", "no repeats", "sum at most $s$ with non-negative items"), the longest good window is found by growing on the right and shrinking on the left until the window is good again.
- **Variable length, up-closed predicate.** If every super-window of a good window is good ("contains all of $t$", "sum at least $s$ with non-negative items"), the shortest good window is found by growing until good and shrinking while good.
- **Signals that it does not apply.** Negative items in a sum condition, conditions on order inside the window, or answers that are not contiguous. Then use [prefix sums](/prefix-sums/) with a hash table or a deque, dynamic programming, or a full search.

## The template

For the longest window that satisfies a down-closed predicate VALID, with the holes in capitals:

```pseudo id=main
LONGEST-WINDOW(A[0 .. n − 1])
L1  l ← 0; S ← EMPTY-SUMMARY; best ← 0
L2  for r ← 0 to n − 1 do
L3      ADD(S, A[r])                          ▷ hole: put A[r] into the summary
L4      while not VALID(S) do                 ▷ hole: test the window A[l .. r]
L5          REMOVE(S, A[l]); l ← l + 1        ▷ hole: take A[l] out of the summary
L6      best ← max(best, r − l + 1)
L7  return best
```

**The invariant to prove.** For an end $r$, let $L(r)$ be the smallest $i$ such that $A[i \ldots r]$ is valid (the empty window $A[r+1 \ldots r]$ counts as valid). After line L5 of step $r$:

> **(V)** $l = L(r)$, $S$ is the summary of $A[l \ldots r]$, and $best = \max_{r' \le r} (r' - L(r') + 1)$.

**Why no window is skipped.** If VALID is down-closed, then $L(r - 1) \le L(r)$: the window $A[L(r) \ldots r - 1]$ is a part of the valid $A[L(r) \ldots r]$, so it is valid, and the smallest valid start for $r - 1$ is at most $L(r)$. So at the start of step $r$ the left end $l = L(r - 1)$ is not past $L(r)$. The loop of line L4 moves $l$ only while $A[l \ldots r]$ is not valid, so it stops exactly at $L(r)$. A start that it passes is not valid for end $r$, and not for any later end either, since a later window with this start contains $A[l \ldots r]$. So every end meets its longest valid window, and line L6 sees the answer.

**For the shortest window** with an up-closed predicate, the loop body becomes "while VALID: record $r - l + 1$; REMOVE$(S, A[l])$; $l \leftarrow l + 1$". The invariant is that every start $i < l$ has had its shortest valid window $A[i \ldots e(i)]$ recorded, where $e(i)$ is non-decreasing. See [minimum size subarray sum](/minimum-size-subarray-sum/) and the [minimum window algorithm](/minimum-window-substring-algorithm/).

**Cost.** Line L3 runs $n$ times and line L5 at most $n$ times in total, because $l$ never passes $r + 1$. So the scan makes at most $2n$ summary updates and at most $2n$ calls to VALID, an $O(n)$ total when each costs $O(1)$. This [aggregate count](/aggregate-method/) holds even though a single step can run line L5 many times.

## Classic examples

From simple to hard:

- **Fixed length $k$, sum or average.** Add $A[r]$, subtract $A[r - k]$. This is the [maximum sum subarray of fixed length](/maximum-sum-subarray-of-fixed-length/) and the moving average.
- **[Minimum size subarray sum](/minimum-size-subarray-sum/).** Shortest window with sum at least $s$, for non-negative items. Up-closed.
- **[Longest substring without repeating characters](/longest-substring-without-repeating-characters/).** Down-closed; the [algorithm](/sliding-window-longest-substring/) jumps the left end with the last position of each character.
- **[Longest substring with at most $k$ distinct characters](/longest-substring-with-k-distinct/).** Down-closed, with a count table and a distinct counter.
- **[Sliding window maximum](/sliding-window-maximum-deque/).** Fixed length, with a monotonic deque as the summary.
- **[Minimum window substring](/minimum-window-substring/).** Up-closed, with a count table and a counter of missing characters.
- **Count the good windows.** With a down-closed predicate, the number of good nonempty windows is $\sum_r (r - L(r) + 1)$. With "exactly $k$" $=$ "at most $k$" $-$ "at most $k - 1$", it counts subarrays with exactly $k$ distinct values.

## Variations

- **Fixed versus variable length.** A fixed window moves both ends together; a variable window moves the left end by the predicate.
- **Jumping left end.** When the summary knows where the next good start is, the left end jumps there, as with the last positions in the longest distinct substring.
- **Summaries that cannot remove.** Max, min, gcd and other operations without an inverse need a [monotonic deque](/monotonic-deque/) (for max and min) or a [two-stack queue](/two-stacks-queue/) (for any associative operation); see [sliding window aggregation](/sliding-window-aggregation/).
- **Streams.** In the [sliding window model](/sliding-window-model/) of data streams, the window is the last $W$ items or the last $T$ time units, and the summary must fit in small memory.
- **Window over a sorted array.** For "the largest set of values within a range of width $d$", sort and slide a window over the sorted values. The window is a range of values, not of positions.
- **Two windows or nested windows.** "Exactly $k$" by the difference of two "at most" windows; or a window inside a binary search over its length.

## Pitfalls

- **Non-monotone predicate.** With negative numbers, a window with sum at least $s$ can become invalid when it grows, and the scan misses answers. On $[1, -3, 4]$ with $s = 4$, the shortest answer is $[4]$, but the window sum never reaches 4.
- **Wrong loop at the left end.** For the longest window, shrink while *not* valid and record after the loop; for the shortest window, record and shrink while valid. Mixing the two records invalid windows or misses the shortest ones.
- **The left end passing the right end.** If the predicate can fail on a window of one item, the loop of line L4 must allow $l = r + 1$, an empty window, and the length $r - l + 1$ is then 0.
- **Stale summary.** Every change of $l$ or $r$ must update the summary in the same step. Forgetting to remove $A[l]$ before $l \leftarrow l + 1$ is the usual bug.
- **Removing by value from a deque.** For a window maximum, compare indices with the window bound, not values, or equal values leave too early.

## Exercises

1. Given an array of non-negative integers and $s$, count the subarrays with sum at most $s$ in $O(n)$ time. State the invariant.
2. Given a binary array and $k$, find the longest subarray with at most $k$ zeros. Prove that the left end never needs to move back.
3. Given a string and a pattern $t$, report every start of a substring of length $|t|$ that is an anagram of $t$, in $O(n + |t| + \sigma)$ time.
4. Show that the template for the longest window is wrong for the predicate "sum at most $s$" when items can be negative, by a small input.
5. Given an array and $d$, find the longest subarray whose maximum and minimum differ by at most $d$, in $O(n)$ time. (Hint: two monotonic deques.)
6. Prove that for a down-closed predicate the number of valid nonempty windows is $\sum_{r} (r - L(r) + 1)$, and compute it for "no repeated character" on $\texttt{abcabcbb}$.

## References
