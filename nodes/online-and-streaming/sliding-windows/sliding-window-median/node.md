---
tag: 08ESMB
kind: problem
slug: sliding-window-median
name: Sliding window median
aliases:
- running median of windows
- running median over a window
- sliding order statistic
area: online-and-streaming/sliding-windows
level: advanced
summary: Report the median of the last W items after each item of a stream; two heaps with lazy deletion or an order-statistic tree take O(log W) per item, and Omega(log W) comparisons are needed.
prereqs: [median, binary-heap, sliding-window-model]
see_also: [order-statistic-tree, indexed-priority-queue, sliding-window-quantiles, sliding-window-maximum, sliding-window-aggregation, quantile, lazy-deletion]
sources:
  - book: isbn:9780262046305
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, fourth edition
    locator: Section 17.1, dynamic order statistics (OS-SELECT and the size field), and Chapter 6, heaps
  - paper: "Wolfgang Härdle and William Steiger, Optimal median smoothing, Journal of the Royal Statistical Society, Series C (Applied Statistics) 44(2), 1995"
    locator: pages 258 to 264, the running median with a double heap in O(log W) per item
  - paper: "Thomas S. Huang, George J. Yang and Gregory Y. Tang, A fast two-dimensional median filtering algorithm, IEEE Transactions on Acoustics, Speech, and Signal Processing 27(1), 1979"
    locator: pages 13 to 18, the histogram method for images with few grey levels
  - paper: "Simon Perreault and Patrick Hébert, Median filtering in constant time, IEEE Transactions on Image Processing 16(9), 2007"
    locator: pages 2389 to 2394, column histograms and O(1) time per pixel for 8-bit images
---

The sliding window median problem asks for the median of the last $W$ items of a stream after each new item. The median is not a monoid aggregate, so the methods of [sliding-window aggregation](/sliding-window-aggregation/) do not apply, and the window must be kept in an ordered structure. Two [binary heaps](/binary-heap/) with lazy deletion take $O(\log W)$ amortized time per item, and an [order-statistic tree](/order-statistic-tree/) takes $O(\log W)$ in the worst case. In the comparison model no method can do better than $\Omega(\log W)$ comparisons per item on average, as proved below.

## In plain words

You watch the last few values of a stream and want the middle one after each step. The middle value is a good summary when some values are wild, because a single huge spike does not move it much. Two piles help: one pile holds the smaller half of the window with its largest value on top, and the other holds the larger half with its smallest value on top. The median sits on top of the first pile. A new value goes on the pile where it belongs, the oldest value leaves its pile, and if one pile gets too big its top moves to the other pile. Removing an old value from deep inside a pile is slow, so the method only marks it as gone and throws it away later, when it comes to the top.

## Definition

The input is a stream $x_1, x_2, \ldots$ of items from a totally ordered set and a window size $W \ge 1$. After item $t$, let $n = \min(t, W)$ and let $y_1 \le y_2 \le \cdots \le y_n$ be the window $x_{t - n + 1}, \ldots, x_t$ in sorted order, with repeated values kept. Output the **lower median** $y_{\lceil n/2 \rceil}$.

For an even $n$ there are two middle items. This page reports the lower one, which is defined for every ordered set. When the items are numbers, many uses report the mean $(y_{n/2} + y_{n/2 + 1})/2$ instead, which needs the upper median too; the structures below give both.

The more general **sliding order statistic** asks for $y_r$ with a fixed rank $r$, or with the rank $\lceil qn \rceil$ for a fixed fraction $q$.

## Variants

- **Time-based window.** The window holds the items of the last $T$ time units, so $n$ changes. The methods below work unchanged, because items still leave in arrival order; one step may evict many items.
- **Other ranks.** A fixed quantile instead of the median: keep $\lceil qn \rceil$ live keys in the lower heap.
- **Approximate quantiles.** With $o(W)$ memory only an approximate rank is possible; see [sliding-window quantiles](/sliding-window-quantiles/).
- **Small integer values.** For values in $\{0, \ldots, U - 1\}$, a histogram of counts replaces the ordered structure, as in the median filters of image processing (Huang, Yang and Tang 1979).
- **Two dimensions.** The median filter over every $a \times b$ rectangle of an image. Unlike the maximum, the median is not separable into a row pass and a column pass. Perreault and Hébert (2007) reach $O(1)$ time per pixel for 8-bit images with one histogram per column.
- **Weighted median.** Each item carries a weight, and the answer is the item where the cumulative weight first reaches half the total. An order-statistic tree with weight sums in its nodes handles it.

## Examples

$W = 3$ and the stream $5, 2, 2, 8, 2, 9, 1, 2$, with the two-heap method below. Keys are pairs (value, index), so that the three items of value 2 are different keys. The lower heap is a max-heap and the upper heap a min-heap. Square brackets mark dead keys, which have left the window but are still in a heap.

| $t$ | $x_t$ | window | lower heap | upper heap | median |
|---|---|---|---|---|---|
| 1 | 5 | 5 | (5, 1) | | 5 |
| 2 | 2 | 5, 2 | (2, 2) | (5, 1) | 2 |
| 3 | 2 | 5, 2, 2 | (2, 3), (2, 2) | (5, 1) | 2 |
| 4 | 8 | 2, 2, 8 | (2, 3), (2, 2) | (8, 4) | 2 |
| 5 | 2 | 2, 8, 2 | (2, 5), (2, 3), [(2, 2)] | (8, 4) | 2 |
| 6 | 9 | 8, 2, 9 | (8, 4), (2, 5), [(2, 3)], [(2, 2)] | (9, 6) | 8 |
| 7 | 1 | 2, 9, 1 | (2, 5), [(2, 3)], [(2, 2)], (1, 7) | (9, 6) | 2 |
| 8 | 2 | 9, 1, 2 | (2, 8), (1, 7) | (9, 6) | 2 |

At $t = 3$ the key (2, 3) is larger than the top (2, 2), so it first goes to the upper heap and then moves down to restore the balance. At $t = 5$ the key (2, 2) leaves the window but is not at a top, so it stays as a dead key. At $t = 8$ the eviction of (2, 5) exposes (2, 3) and then (2, 2) at the top, and the pruning loop removes all three. The median jumps to 8 at $t = 6$ and back to 2 at $t = 7$, which shows why no running update without the whole window can work.

## Known algorithms

**Two heaps with lazy deletion.** Keep the window items in a ring buffer, a max-heap $lo$ and a min-heap $hi$ of keys $(x_i, i)$, the counts $n_{lo}$ and $n_{hi}$ of live keys in each heap, and $head$, the index of the oldest item in the window. A key is *dead* when its index is less than $head$. Since items leave in order of index, deadness needs no extra table.

```pseudo id=main
STEP(x)
L1  t ← t + 1; k ← (x, t); append x to the ring buffer
L2  if n_lo = 0 or k < TOP(lo) then push k on lo; n_lo ← n_lo + 1
L3  else push k on hi; n_hi ← n_hi + 1
L4  if t > W then
L5      e ← (x_{t−W}, t − W); head ← t − W + 1
L6      if e ≤ TOP(lo) then n_lo ← n_lo − 1 else n_hi ← n_hi − 1
L7  PRUNE(lo); PRUNE(hi)
L8  if n_lo > n_hi + 1 then pop TOP(lo) and push it on hi; n_lo ← n_lo − 1; n_hi ← n_hi + 1
L9  else if n_lo < n_hi then pop TOP(hi) and push it on lo; n_lo ← n_lo + 1; n_hi ← n_hi − 1
L10 PRUNE(lo); PRUNE(hi); COMPACT(lo); COMPACT(hi)
L11 return the value of TOP(lo)
PRUNE(h)
L12 while h is not empty and the index of TOP(h) is less than head do pop h
COMPACT(h)
L13 if size(h) > 2 · (live count of h) + 8 then keep only the live keys of h and rebuild the heap
```

**Correctness.** The keys are distinct, because the indices are. After each step these invariants hold:

- **(C)** $n_{lo}$ and $n_{hi}$ are the numbers of live keys in $lo$ and $hi$, and every key of the window is in exactly one heap.
- **(B)** $n_{hi} \le n_{lo} \le n_{hi} + 1$.
- **(S)** Every live key of $lo$ is less than every live key of $hi$.
- **(T)** The top of each non-empty heap is live.

*Insert, lines L2 and L3.* By (T) the top of $lo$ is its largest live key. If $k$ is less than that top, it is less than every live key of $hi$ by (S), so adding it to $lo$ keeps (S). Otherwise $k$ is greater than every live key of $lo$, so adding it to $hi$ keeps (S). After the insert the top of $lo$ is the old top or $k$, both live.

*Evict, lines L5 and L6.* The key $e$ is live before this step and is in one heap. By (S) and because the top of $lo$ is the largest live key of $lo$, $e$ is in $lo$ exactly when $e \le \mathrm{TOP}(lo)$. So line L6 decrements the right count, and (C) holds with the new value of $head$.

*Balance, lines L7 to L9.* Line L7 restores (T). Before the step $n_{lo} - n_{hi} \in \{0, 1\}$, and the insert and the evict each change it by exactly 1, so after them it is in $\{-2, -1, 0, 1, 2, 3\}$, and it has the right parity for the new window size. One move of a live top changes the difference by 2, so a single move at line L8 or L9 restores (B). Moving the largest live key of $lo$ to $hi$ keeps (S), because it is less than every live key of $hi$ and greater than every other live key of $lo$; the move from $hi$ to $lo$ is symmetric. Line L10 restores (T) for the heap that lost its top, and compaction removes only dead keys.

*Answer.* By (S) the $n_{lo} = \lceil n/2 \rceil$ live keys of $lo$ are the $\lceil n/2 \rceil$ smallest keys of the window, and by (T) the top of $lo$ is the largest of them, which is $y_{\lceil n/2 \rceil}$. For an even $n$ the top of $hi$ is $y_{n/2 + 1}$.

**Cost.** Lines L1 to L9 do a constant number of heap operations. Each key is pushed at most twice, once at line L2 or L3 and once by a move, and popped at most once per push, so all prune loops together pop at most $2t$ keys in $t$ steps. Line L13 rebuilds a heap of size $s$ in $O(s)$ time only when more than half of its keys are dead, and each dead key is removed once, so the rebuilds cost $O(1)$ amortized per item. After line L10 each heap holds at most $2W + 8$ keys, so every heap operation costs $O(\log W)$. The total is $O(\log W)$ amortized time per item and $O(W)$ space. Without compaction the heaps can grow without bound: on an increasing stream the evicted keys sink to the bottom of $lo$ and never reach its top.

**Other methods.**

| method | time per item | space | notes |
|---|---|---|---|
| sort each window | $O(W \log W)$ | $O(W)$ | baseline |
| [quickselect](/quickselect/) on each window | $O(W)$ expected | $O(W)$ | no state between steps |
| sorted array with binary search | $O(\log W)$ comparisons, $O(W)$ moves | $W$ | fast for small $W$ |
| two heaps with lazy deletion, above | $O(\log W)$ amortized | $O(W)$ | Härdle and Steiger (1995) use a double heap with $O(\log W)$ per item |
| two [indexed heaps](/indexed-priority-queue/) | $O(\log W)$ worst case | $O(W)$ | delete the evicted key at its stored position, no dead keys |
| [order-statistic tree](/order-statistic-tree/) | $O(\log W)$ worst case | $O(W)$ | insert $(x_t, t)$, delete $(x_{t-W}, t - W)$, select rank $\lceil n/2 \rceil$ |
| histogram of counts | $O(1)$ update, $O(U)$ search | $O(U)$ | values in $\{0, \ldots, U - 1\}$ |

The order-statistic tree is the simplest method with a worst-case bound, and it answers any rank, so it also solves the sliding order statistic. The heap and tree bounds are proved here or on the linked pages; the histogram bounds follow from the counts.

## Bounds

**Comparisons, proved here.** In the comparison model, every algorithm that outputs the lower median of each window needs $\Omega(n \log W)$ comparisons on some stream of $n$ items with $n \ge 2W$. So the two-heap and tree methods are optimal up to a constant factor.

*Proof.* Let $W = 2k + 1$ with $k \ge 1$. Take a block of $3k + 1$ items: $k + 1$ copies of a value $M$, then $k$ arbitrary values $z_1, \ldots, z_k$ with $-M < z_i < M$, then $k$ copies of $-M$. After the first $2k + 1$ items of the block, the window is exactly the block so far, whatever came before. After $j$ copies of $-M$, for $1 \le j \le k$, the window holds $k + 1 - j$ copies of $M$, all the $z_i$, and $j$ copies of $-M$, and its $(k + 1)$-th smallest item is the $(k + 1 - j)$-th smallest $z_i$. So the $k$ outputs of the block list the $z_i$ in sorted order, and the algorithm has sorted them. Take a stream of $b = \lfloor n / (3k + 1) \rfloor$ such blocks, with the $z$ values of each block in any order. The outputs determine the order of the $z$ values in every block, so a decision tree for the algorithm has at least $(k!)^b$ leaves and depth at least $b \log_2 k! = \Omega(n \log W)$. An even $W$ is handled the same way with one more copy of $M$. $\square$

**Space, proved here.** By the same block, the state of the algorithm after the items $M, \ldots, M, z_1, \ldots, z_k$ must determine the sorted list of the $z_i$, because the later outputs depend only on that state. If the values come from a set of $U$ values, there are $\binom{U + k - 1}{k}$ such multisets, so the state needs at least $\log_2 \binom{U + k - 1}{k} \ge k \log_2 (U / k)$ bits, which is $\Omega(W \log(U/W))$ for $U \ge 2W$. An exact streaming median therefore stores about as much as the window itself, and memory of size $o(W)$ requires an approximate answer.

## Reductions

- **Sorting reduces to it**, as in the proof above: $k$ items are sorted by a sliding median over $3k + 1$ items.
- **To a dynamic order-statistic structure.** Insert, delete and select by rank on a multiset solve every sliding order statistic.
- **Mean of the two middles.** For numbers, the lower and upper medians together give the conventional median of an even window.
- **To approximate quantiles.** Replacing the exact structure by a quantile summary with rank error $\varepsilon n$ gives an approximate median with less memory; see [sliding-window quantiles](/sliding-window-quantiles/).

## Applications

Median filters remove impulse noise from signals and images while keeping edges, which a moving average blurs. Running medians smooth time series in statistics, where they resist outliers, and they set robust baselines for anomaly detection in monitoring. The median latency of the last requests is a common service metric, though such systems often use an approximate quantile summary instead.

## References
