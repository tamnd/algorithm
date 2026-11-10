---
tag: Y52VJG
kind: problem
slug: sliding-window-maximum
name: Sliding window maximum
aliases:
- maximum of every window of size k
- range maximum over a moving window
- sliding window minimum
- window extremum
- running max filter
area: online-and-streaming/sliding-windows
level: core
summary: Report the maximum of the most recent W items, or of the items of the last T time units, after each step of a stream; a monotone deque does it in O(1) amortized time per item.
prereqs: [sliding-window-model, deque, amortized-cost]
see_also: [sliding-window-maximum-deque, monotonic-deque, min-queue, sliding-window-aggregation, daba-queue, sparse-table, time-based-window, mathematical-morphology]
sources:
  - url: https://arxiv.org/abs/cs/0610046
    title: Daniel Lemire, Streaming maximum-minimum filter using no more than three comparisons per element, Nordic Journal of Computing 13(4), 2006
    locator: Section 2 (the van Herk and Gil-Werman block method), Section 3 (the online deque algorithm with at most 3 comparisons per item for max and min together)
  - paper: "Marcel van Herk, A fast algorithm for local minimum and maximum filters on rectangular and octagonal kernels, Pattern Recognition Letters 13(7), 1992"
    locator: pages 517 to 521, the block method with prefix and suffix maxima
  - paper: "Joseph Gil and Michael Werman, Computing 2-D min, median, and max filters, IEEE Transactions on Pattern Analysis and Machine Intelligence 15(5), 1993"
    locator: pages 504 to 507, the block method found independently
  - url: https://arxiv.org/abs/2009.13768
    title: Kanat Tangwongsan, Martin Hirzel and Scott Schneider, In-order sliding-window aggregation in worst-case constant time, extended version
    locator: Section 8.1, max as a selective operator and the worst-case bounds of DABA for it
---

The sliding window maximum problem asks, at each step of a stream, for the largest of the items that are still in the window: the last $W$ items in a count-based window, or the items of the last $T$ time units in a time-based window. Recomputing the maximum costs $W - 1$ comparisons per step, and a running maximum fails because the maximum can leave the window. A deque of the items that can still become the maximum solves both window kinds in $O(1)$ amortized time per item and $O(W)$ space; the [monotonic deque algorithm](/sliding-window-maximum-deque/) gives that method for arrays in full, and this page gives the problem, the time-based version and the bounds.

## In plain words

A sensor sends a reading every second, and a display must always show the highest reading of the last minute. Keeping the highest value seen so far is not enough: after a minute the peak is too old and must go, and then you need the second highest, which you did not keep. The fix is to keep a short list of readings that could still become the peak. A reading drops out of that list as soon as a newer reading is at least as high, because the newer one will stay longer and is never lower. The list is then sorted from high to low, the oldest entry is the answer, and old entries leave from the front.

## Definition

**Count-based window.** The input is a stream $x_1, x_2, \ldots$ of items from a totally ordered set and a window size $W \ge 1$. After item $t$ arrives, output

$$m_t = \max\{x_i : \max(1, t - W + 1) \le i \le t\}.$$

**Time-based window.** Each item $x_i$ comes with a timestamp $\tau_i$, with $\tau_1 \le \tau_2 \le \cdots$, and the window length is $T > 0$. A query at time $t$, with $t$ at least every timestamp seen so far and at least every earlier query time, outputs

$$m(t) = \max\{x_i : t - T < \tau_i \le t\},$$

or $-\infty$ when no item has a timestamp in $(t - T, t]$. Queries can come at any time, not only when an item arrives, and one step can expire many items.

The array version, with an input array $A[0 \ldots n-1]$ and the output of all $n - W + 1$ full windows, is the offline special case. The **sliding window minimum** is the same problem for the reversed order, so every method on this page works for it with the comparisons reversed.

## Variants

- **Fixed or variable window.** In the count-based case $W$ is fixed. In the time-based case the number of items in the window changes, and in the [two pointers](/two-pointers/) style of problems the left end moves by its own rule. The deque handles all of these, because it only needs the left end never to move back.
- **Maximum and minimum together.** Two deques, or the combined filter of Lemire, which uses at most 3 comparisons per item for both.
- **Argmax.** Report the position of the maximum. The deque stores positions, so this costs nothing more. With ties, the test $\le$ on insert keeps the latest position of the maximum, and the test $<$ keeps the earliest.
- **Two dimensions.** The maximum over every $a \times b$ rectangle of an image, the grayscale dilation of [mathematical morphology](/mathematical-morphology/) with a flat rectangle. It separates into a pass over the rows with window $b$ and a pass over the columns with window $a$.
- **Any associative operator.** For sums, products or sketches, see [sliding-window aggregation](/sliding-window-aggregation/). Max is the *selective* case, $x \otimes y \in \{x, y\}$, which allows the deque method.

## Examples

A time-based window of length $T = 3$. The items are pairs (timestamp, value): $(1, 4), (2, 2), (2, 3), (4, 1), (7, 5), (8, 2)$. The deque is shown as pairs, front first, after each step.

| step | deque after the step | window $(t - T, t]$ | answer |
|---|---|---|---|
| insert $(1, 4)$ | $(1, 4)$ | | |
| insert $(2, 2)$ | $(1, 4), (2, 2)$ | | |
| insert $(2, 3)$ | $(1, 4), (2, 3)$ | | |
| query $t = 3$ | $(1, 4), (2, 3)$ | $(0, 3]$ | 4 |
| insert $(4, 1)$ | $(1, 4), (2, 3), (4, 1)$ | | |
| query $t = 4$ | $(2, 3), (4, 1)$ | $(1, 4]$ | 3 |
| query $t = 6$ | $(4, 1)$ | $(3, 6]$ | 1 |
| query $t = 7$ | empty | $(4, 7]$ | $-\infty$ |
| insert $(7, 5)$ | $(7, 5)$ | | |
| insert $(8, 2)$ | $(7, 5), (8, 2)$ | | |
| query $t = 8$ | $(7, 5), (8, 2)$ | $(5, 8]$ | 5 |

The insert of $(2, 3)$ removes $(2, 2)$ from the back, because $(2, 3)$ leaves no earlier and is larger. The query at $t = 4$ expires $(1, 4)$, the old maximum, and the answer 3 is ready at the new front. The query at $t = 7$ expires the last item, so the window is empty.

## Known algorithms

The streaming method keeps a deque $D$ of pairs (timestamp, value). For a count-based window, use the index $i$ as the timestamp, $T = W$, and query at $t$ after item $t$.

```pseudo id=main
INSERT(τ, x)
L1  while D is not empty and value(back(D)) ≤ x do pop the back of D
L2  push (τ, x) at the back of D
QUERY(t)
L3  while D is not empty and time(front(D)) ≤ t − T do pop the front of D
L4  if D is empty then return −∞
L5  return value(front(D))
```

**Why it is correct.** Call a stored item a *leader* if its value is greater than the value of every later item. The invariant is: $D$ holds, from front to back, exactly the leaders among the items that have arrived and have not yet expired, in order of arrival. Line L1 removes an item $y$ with $\mathrm{value}(y) \le x$; every later window that contains $y$ also contains the new item, because the new item has a timestamp at least as large and so expires no earlier, and so $y$ can never again be the unique largest. Since the values in $D$ strictly decrease and the timestamps do not decrease from front to back, the expired items form a prefix of $D$, which line L3 removes. The first leader of a set is an item with the largest value, so line L5 returns the maximum. The [monotonic deque algorithm](/sliding-window-maximum-deque/) proves the same invariant in full for count-based windows.

**Cost.** Each item is pushed once and popped at most once, so a stream of $n$ items and $q$ queries costs $O(n + q)$ time in total, $O(1)$ amortized per operation by the [aggregate method](/aggregate-method/). One insert can pop $W$ items, and one query can expire all of them, so the worst case for one step is $\Theta(W)$. The deque never holds more than the items of the window.

**Expected size.** If the $W$ values of a full window are independent with a continuous distribution, the deque holds on average $H_W = 1 + \frac12 + \cdots + \frac1W \approx \ln W$ items. The item $j$ places from the end is a leader exactly when it is the largest of the last $j$ items, which has probability $1/j$, and the expectation of the count is the sum of these probabilities.

The other methods:

| method | time per item | worst case per item | extra space | notes |
|---|---|---|---|---|
| recompute each window | $W - 1$ comparisons | $W - 1$ | $O(1)$ beyond the window | the baseline |
| monotone deque, above | $O(1)$ amortized, at most 2 comparisons on average | $\Theta(W)$ | at most $W$ items | count and time windows |
| van Herk and Gil-Werman blocks | about 3 comparisons | $O(1)$ | $O(W)$ | needs the next block, so the output lags by up to $W$ items; count windows |
| Lemire (2006) | at most 3 comparisons for max and min together | $O(W)$ | $O(W)$ | online, deque based |
| [DABA](/daba-queue/) with $\otimes = \max$ | at most 4 calls of max per insert, 3 per evict, 1 per query | $O(1)$ | $2W$ | worst-case constant, any window kind with FIFO order |
| [segment tree](/segment-tree/) over a ring buffer | $O(\log W)$ | $O(\log W)$ | $2W$ | also answers maxima of sub-windows |
| [sparse table](/sparse-table/) | $O(1)$ query after $O(n \log n)$ build | | $O(n \log n)$ | offline array only, any ranges |

The block method cuts the stream into blocks of $W$ items and stores, for each block, the prefix maxima and the suffix maxima. A window that does not start at a block boundary covers a suffix of one block and a prefix of the next, so its maximum is the larger of one suffix maximum and one prefix maximum. The page proves the deque bounds above. The comparison counts of the block method and of Lemire's filter are cited from Lemire (2006), and the DABA counts are proved on the [DABA page](/daba-queue/).

## Bounds

**Time.** Every item must be read, so $\Omega(n)$ time for $n$ items, and the deque meets this bound up to a constant.

**Space, proved here.** Every deterministic streaming algorithm that outputs the exact maximum of a count-based window of size $W$ needs at least $\log_2 \binom{2W - 1}{W} \ge W - 1$ bits of memory when the items come from a set of at least $W + 1$ values. Use the values $0, 1, \ldots, W$. For each non-increasing sequence $W \ge c_1 \ge c_2 \ge \cdots \ge c_W \ge 1$, feed the window $x_j = c_j$. If the algorithm then reads $j$ more items of value 0, for $j = 0, \ldots, W - 1$, it must output $\max(c_{j+1}, \ldots, c_W) = c_{j+1}$, so its future outputs spell out the whole sequence. Two different sequences must therefore leave different memory states. There are $\binom{2W - 1}{W}$ such sequences, and $\binom{2W - 1}{W} \ge 2^{W - 1}$ because it is the larger half of the sum $\sum_k \binom{2W-1}{k} = 2^{2W - 1}$. So the $O(W)$ items of the deque cannot be replaced by a sketch of size $o(W)$ bits, unlike the counting problems of [DGIM](/dgim-algorithm/), which allow an approximate answer.

**Worst case per item.** The deque has a worst case of $\Theta(W)$ for one step. DABA reaches $O(1)$ in the worst case with a constant number of comparisons, so the amortized bound is not a limit of the problem.

## Reductions

- **Minimum to maximum.** Negate the values, or reverse the order.
- **To sliding-window aggregation.** Max is associative with identity $-\infty$, so every SWAG method of [sliding-window aggregation](/sliding-window-aggregation/) applies, such as the [two-stacks queue](/two-stacks-queue/) and DABA. The deque is a special method for selective operators.
- **Queue with maximum.** A FIFO queue that answers its maximum is the same structure: push is INSERT, pop is an eviction of the oldest item. See the [queue with minimum](/min-queue/).
- **Range maximum query.** For an offline array, every window is a range, so a [range minimum query](/range-minimum-query/) structure answers all windows; this is slower than the deque for windows of one fixed length.
- **Dynamic programming.** Recurrences $f(i) = c_i + \max_{i - W \le j < i} f(j)$ are solved in $O(n)$ by feeding $f(j)$ into a sliding window maximum as soon as it is known.

## Applications

The running max and min filters of signal and image processing, which are the dilation and erosion of [mathematical morphology](/mathematical-morphology/) with a flat line element; peak detection over the last seconds of monitoring data; the highest and lowest price over a recent period in trading, as in channel indicators; the busiest link load over the last minutes in network monitoring; and the deque step of dynamic programs with a moving range of candidates.

## References
