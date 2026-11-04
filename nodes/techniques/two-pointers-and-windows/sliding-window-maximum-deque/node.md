---
tag: N2ZTTV
kind: algorithm
slug: sliding-window-maximum-deque
name: Sliding window maximum with monotonic deque
aliases:
- monotonic queue maximum
area: techniques/two-pointers-and-windows
level: core
summary: Keep a deque of candidate indices in decreasing value order; solves the problem in O(n) total time.
solves: [sliding-window-maximum]
model: word-ram
complexity:
  vars: {n: the number of items in the array, k: the window length}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(k)}
properties: {stable: false, in_place: false, adaptive: false, online: true, deterministic: true, comparison: true, recursive: false}
prereqs: [sliding-window, deque, monotonic-deque, loop-invariant]
see_also: [sliding-window-maximum, monotonic-deque, monotonic-stack, two-stacks-queue, sliding-window-aggregation, sparse-table, range-minimum-query, shortest-subarray-sum-at-least-k]
sources:
  - url: https://cp-algorithms.com/data_structures/stack_queue_modification.html
    title: cp-algorithms, Minimum stack / Minimum queue
    locator: sections Queue modification (method 1) and Finding the minimum for all subarrays of fixed length
  - url: https://arxiv.org/abs/cs/0610046
    title: Daniel Lemire, Streaming maximum-minimum filter using no more than three comparisons per element, Nordic Journal of Computing 13(4), 2006
    locator: the online algorithm with a monotone double-ended queue and its worst-case comparison count
  - book: isbn:9783030542559
    title: Steven S. Skiena, The Algorithm Design Manual, third edition
    locator: Chapter 3, Data structures (stacks, queues and their uses)
---

The monotonic deque algorithm computes the maximum of every window of $k$ consecutive items of an array in $\Theta(n)$ total time, independent of $k$. It keeps a double-ended queue of indices whose values strictly decrease from the front to the back. When a new item arrives, every index at the back with a value at most the new value is removed for good, because the new item outlives it and is at least as large. The front of the deque is then the index of the window maximum. It solves the [sliding window maximum](/sliding-window-maximum/) problem and is the standard example of a [monotonic deque](/monotonic-deque/).

## In plain words

Picture a queue of people where each person has a height, and you want to know the tallest person among the last $k$ who joined. When a new person joins, everyone at the back who is not taller than the new person can leave at once: they will leave the window before the new person does, and they are never taller, so they can never be the answer again.

After this cleanup, the people who remain stand in order of height, tallest at the front. The person at the front is the tallest in the window. If that person is now too old for the window, they leave from the front. Every person joins once and leaves once, so the total work is small.

## The problem

**Input.** An array $A[0 \ldots n-1]$ of items with a total order, and a window length $k$ with $1 \le k \le n$.

**Output.** The array $M[0 \ldots n-k]$ with $M[l] = \max(A[l], \ldots, A[l + k - 1])$.

Write $W_r$ for the set of indices of the window that ends at $r$: $W_r = \{\max(0, r - k + 1), \ldots, r\}$. The algorithm reports $\max_{i \in W_r} A[i]$ for $r = k - 1, \ldots, n - 1$, which is $M[r - k + 1]$.

## The algorithm

```pseudo id=main
SLIDING-WINDOW-MAXIMUM(A[0 .. n − 1], k)
L1  D ← empty deque of indices; M ← empty list
L2  for r ← 0 to n − 1 do
L3      while D is not empty and A[back(D)] ≤ A[r] do pop the back of D
L4      push r at the back of D
L5      if front(D) ≤ r − k then pop the front of D
L6      if r ≥ k − 1 then append A[front(D)] to M
L7  return M
```

Line L3 removes the indices that can no longer be a maximum. Line L5 removes the index that has just left the window; at most one index leaves at each step, so one test is enough. Line L6 reads the answer from the front.

For the sliding window *minimum*, reverse the comparison in line L3 to $A[back(D)] \ge A[r]$.

## Example

$A = [1, 3, -1, -3, 5, 3, 6, 7]$ and $k = 3$. The deque is shown as pairs (index, value), after line L5.

| $r$ | $A[r]$ | popped at the back | deque after the step | window | output |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | none | (0, 1) | $[0, 0]$ | |
| 1 | 3 | (0, 1) | (1, 3) | $[0, 1]$ | |
| 2 | $-1$ | none | (1, 3), (2, $-1$) | $[0, 2]$ | 3 |
| 3 | $-3$ | none | (1, 3), (2, $-1$), (3, $-3$) | $[1, 3]$ | 3 |
| 4 | 5 | (3, $-3$), (2, $-1$), (1, 3) | (4, 5) | $[2, 4]$ | 5 |
| 5 | 3 | none | (4, 5), (5, 3) | $[3, 5]$ | 5 |
| 6 | 6 | (5, 3), (4, 5) | (6, 6) | $[4, 6]$ | 6 |
| 7 | 7 | (6, 6) | (7, 7) | $[5, 7]$ | 7 |

The output is $M = [3, 3, 5, 5, 6, 7]$. The loop of line L3 makes 10 comparisons of values in total, below the bound $2n - 2 = 14$. In this run line L5 never pops: each index left the deque at the back before it left the window.

## Correctness

Call an index $i \in W_r$ a *leader* of $W_r$ if $A[i] > A[j]$ for every $j$ with $i < j \le r$. The last index $r$ is always a leader. The leaders, read from left to right, have strictly decreasing values, and the first leader is the last index in $W_r$ where the window maximum occurs.

The loop keeps this invariant, after line L5 of step $r$:

> **(Q)** $D$ holds, from front to back, exactly the leaders of $W_r$, in increasing order of index.

*Why no maximum is skipped.* Line L3 pops an index $j < r$ with $A[j] \le A[r]$. Each later window that contains $j$ ends at some $r' \ge r$ and starts at most at $j$, so it also contains $r$, and $A[r] \ge A[j]$. So $j$ is not a leader of any window from now on, and dropping it loses no answer. The indices that line L3 keeps have values greater than $A[r]$, so they are still leaders. Line L4 adds $r$, which is a leader. Line L5 removes the index $r - k$ if it is in $D$; this is the only index of $W_{r-1}$ that is not in $W_r$. So (Q) holds for $W_r$.

*Result.* By (Q) the front of $D$ is the first leader, whose value is the maximum of $W_r$. Line L6 reports it for each full window. The [proof page](proofs/correctness.md) gives the full induction.

## Complexity

- **Deque operations.** Each index is pushed once at line L4 and popped at most once, at the back or at the front. So there are at most $2n$ deque operations in total, and each costs $O(1)$.
- **Value comparisons.** In line L3, each comparison that returns true pops an index, and at most one comparison per step returns false. The index $n - 1$ is never popped at the back, and step 0 makes no comparison, so there are at most $(n - 1) + (n - 1) = 2n - 2$ comparisons. A strictly increasing array makes exactly $n - 1$.
- **Index comparisons.** One per step in line L5.
- **Space.** The deque holds at most $k$ indices, since all are in the current window: $\Theta(k)$ extra space in the worst case, for a strictly decreasing array. The output takes $n - k + 1$ cells.
- **Per step.** One step can pop up to $k$ indices, so the worst case for one step is $\Theta(k)$; the cost is $O(1)$ amortized per step by the [aggregate method](/aggregate-method/).

## Properties

- **Online.** Step $r$ uses only $A[0 \ldots r]$, so the algorithm works on a stream and outputs each maximum as soon as its window is complete.
- **Independent of $k$.** The total time is $\Theta(n)$ for every $k$.
- **Comparison-based.** It needs only the order of the items.
- **Ties.** With the test $\le$ in line L3, the deque values are strictly decreasing, and the front is the last position of the maximum in the window. With $<$, equal values stay, and the front is the first position of the maximum.

## Variants and improvements

- **Minimum, or both.** Reverse the test for the minimum; run two deques for both.
- **Variable windows.** The same deque works when the left end moves by any rule that never goes back: pop the front while its index is less than the left end. This is how the deque serves [sliding window](/sliding-window/) problems such as [shortest subarray with sum at least $k$](/shortest-subarray-sum-at-least-k/) and windows with a bound on max minus min.
- **Queue with a maximum.** A queue that answers "maximum" in $O(1)$ amortized time, built from this deque or from [two stacks](/two-stacks-queue/). The two-stack queue works for any associative operation, not only max; see [sliding window aggregation](/sliding-window-aggregation/).
- **Block method.** Cut the array into blocks of $k$ items. For each block compute the prefix maxima and the suffix maxima. Each window covers the end of one block and the start of the next, so its maximum is the larger of one suffix maximum and one prefix maximum. This takes about 3 comparisons per item for every $k$, and it has no data-dependent branches, which helps on vector hardware. It is not online.
- **Fewer comparisons.** Lemire (2006) gave a streaming max-min filter with at most 3 comparisons per item in the worst case for the maximum and minimum together.
- **Static queries.** For arbitrary ranges instead of a sliding window, use a [sparse table](/sparse-table/) or another [range minimum query](/range-minimum-query/) structure.

## When to use it

Use it for the maximum or minimum of every window of a stream or array, and inside dynamic programs of the form $f(r) = \max_{r - k \le j < r} f(j) + c(r)$, where the window of candidates moves right. When the operation is not max or min, use a two-stack queue or a prefix-based method instead.

## Pitfalls

- **Storing values instead of indices.** The deque must hold indices, or pairs of index and value, so that line L5 can tell when the front has left the window.
- **Strict versus non-strict pop.** Both are correct for the maximum value. With $<$ the deque can hold equal values, and line L5 must still remove exactly the index $r - k$, not every index with the front value.
- **Expiry by the size of the deque.** A test such as "pop the front when $D$ holds more than $k$ indices" is wrong: the deque usually holds fewer than $k$ indices, and an index that has left the window can stay at the front. On $A = [5, 1, 1]$ with $k = 2$ this test reports 5 for the window $[1, 1]$. Compare the index of the front with $r - k$.
- **Reading the answer too early.** Line L6 must wait for $r \ge k - 1$, the first full window.
- **Window larger than the array.** For $k > n$ there is no full window; return an empty output, or treat the whole array as one window, by the convention of the caller.

## Implementations

## History

The deque method is folklore in programming practice and competitive programming, and it is the standard solution taught for the problem. In image processing the same task is the running max filter, or grayscale dilation with a flat line element. There the block method was the standard fast method, and Lemire (2006) gave an online deque algorithm with at most 3 comparisons per item for the max and min filters together.

## References
