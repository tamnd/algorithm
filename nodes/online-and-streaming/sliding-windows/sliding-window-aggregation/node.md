---
tag: 48F7Z3
kind: problem
slug: sliding-window-aggregation
name: Sliding-window aggregation
aliases:
- FIFO aggregation
- incremental sliding-window aggregation
- SWAG
area: online-and-streaming/sliding-windows
level: advanced
summary: Keep a window of stream items, insert at the back and evict at the front, and answer the aggregate of the window under an associative operator without a full recomputation.
prereqs: [monoid, queue, sliding-window-model, amortized-cost]
see_also: [two-stacks-queue, daba-queue, min-queue, sliding-window-maximum, segment-tree, count-based-window, time-based-window, tumbling-window]
sources:
  - url: https://arxiv.org/abs/2009.13768
    title: Kanat Tangwongsan, Martin Hirzel and Scott Schneider, In-order sliding-window aggregation in worst-case constant time, extended version (VLDB Journal 2021)
    locator: Section 2 (the SWAG abstract data type over a monoid, and Table 1 of operators), Section 8.1 (the known algorithms with their time and space bounds)
  - paper: doi:10.14778/2752939.2752940
    title: Kanat Tangwongsan, Martin Hirzel, Scott Schneider and Kun-Lung Wu, General incremental sliding-window aggregation, PVLDB 8(7), 2015
    locator: pages 702 to 713, FlatFAT and the Reactive Aggregator, with O(m + m log(n/m)) time for m updates
  - paper: doi:10.1145/3093742.3093925
    title: Kanat Tangwongsan, Martin Hirzel and Scott Schneider, Low-latency sliding-window aggregation in worst-case constant time, DEBS 2017
    locator: pages 66 to 77, Two-Stacks and DABA
  - paper: "Arvind Arasu and Jennifer Widom, Resource sharing in continuous sliding-window aggregates, VLDB 2004"
    locator: pages 336 to 347, B-Int, the base-interval method with O(log n) time
---

Sliding-window aggregation asks for a structure that holds the most recent items of a stream, supports insert at the back and evict at the front, and answers the aggregate $v_1 \otimes \cdots \otimes v_n$ of the items under an associative operator $\otimes$ with an identity, a [monoid](/monoid/). Recomputing the aggregate costs $n - 1$ calls of $\otimes$ per query; an inverse lets a running total subtract each evicted item, but max, string concatenation, sketch merges and matrix products have no inverse. For first-in first-out windows the [two-stacks queue](/two-stacks-queue/) solves it with $O(1)$ amortized calls per operation and [DABA](/daba-queue/) with $O(1)$ calls in the worst case. Tangwongsan, Hirzel and Schneider call the abstract type SWAG.

## In plain words

A stream of numbers or records flows past, and you care about only the most recent part of it: the last hundred readings, or everything from the last five minutes. After each new item you want one summary of that part, such as its total, its largest value, or a small sketch of it. New items join at one end, and old items leave at the other. Adding to a total is easy. Removing is the hard part: you cannot take an item back out of a maximum, because the maximum does not remember what the second largest was. Recomputing the summary from all items each time is slow. The methods on this page keep a few partial summaries so that each step costs only a few combine operations.

## Definition

Let $(M, \otimes, 1)$ be a monoid: $\otimes$ is associative and $1$ is its identity. A **SWAG** holds a sequence $v_1, \ldots, v_n$ of elements of $M$, initially empty, and supports:

- $\mathrm{insert}(v)$: the sequence becomes $v_1, \ldots, v_n, v$;
- $\mathrm{evict}()$, for $n \ge 1$: the sequence becomes $v_2, \ldots, v_n$;
- $\mathrm{query}()$: return $v_1 \otimes v_2 \otimes \cdots \otimes v_n$, or $1$ when $n = 0$.

The cost of an algorithm is the number of calls of $\otimes$ per operation, worst case or amortized, and the number of elements of $M$ it stores. The operator is a black box: an algorithm for the general case may not use commutativity, an inverse, or the values of the elements.

A stream model fixes when evict happens. In a [count-based window](/count-based-window/) of size $W$, each stream item is an insert followed by an evict once $n > W$. In a [time-based window](/time-based-window/) of length $T$, each item carries a timestamp, and before a query at time $t$ every item with timestamp at most $t - T$ is evicted. Both are in-order: items leave in the order they came.

## Variants

- **By the operator.** An *invertible* operator (a group, such as sum or the pair (sum, count)) allows subtract on evict. A *selective* operator with $x \otimes y \in \{x, y\}$ (max, min, argmax) allows the [monotonic deque](/monotonic-deque/) of [sliding-window maximum](/sliding-window-maximum/). A *general* monoid needs the methods below. Holistic statistics such as the median are not monoid aggregates with small elements; see [sliding-window median](/sliding-window-median/).
- **By the window.** Count-based and time-based sliding windows as above; [tumbling windows](/tumbling-window/) and [hopping windows](/hopping-window/), where whole groups leave at once; and [session windows](/session-window/).
- **Out of order.** Items may arrive late and must be inserted by timestamp, not at the back. FIFO methods do not apply; tree methods do.
- **Many window sizes.** Several queries with different window lengths share one structure over the longest window, which needs range queries over suffixes, not only the full window.

## Examples

A count-based window of size $W = 3$ over the stream $3, 1, 4, 1, 5, 9, 2, 6, 5, 3$, with sum and with max:

| step | item | window | sum | max |
|---|---|---|---|---|
| 1 | 3 | 3 | 3 | 3 |
| 2 | 1 | 3, 1 | 4 | 3 |
| 3 | 4 | 3, 1, 4 | 8 | 4 |
| 4 | 1 | 1, 4, 1 | 6 | 4 |
| 5 | 5 | 4, 1, 5 | 10 | 5 |
| 6 | 9 | 1, 5, 9 | 15 | 9 |
| 7 | 2 | 5, 9, 2 | 16 | 9 |
| 8 | 6 | 9, 2, 6 | 17 | 9 |
| 9 | 5 | 2, 6, 5 | 13 | 6 |
| 10 | 3 | 6, 5, 3 | 14 | 6 |

The sum is $S \leftarrow S + x_t - x_{t-3}$, two operations per step. The max has no such update. At step 9 the item 9 leaves, and it was the maximum. The new maximum 6 cannot be computed from the old maximum 9, the leaving item and the new item 5: the structure must have kept 6, an item that was never the maximum before. With string concatenation, the window a, b, c must give abc, not cba, which is why the order of the arguments matters.

Other monoids with a simple lifting: the mean as (sum, count) with componentwise addition; the variance as (count, mean, sum of squared deviations) with the pairwise merge formula; the [count-min sketch](/count-min-sketch/) with cellwise addition.

## Known algorithms

Costs are in calls of $\otimes$ for a window of $n$ items, and space is in stored elements of $M$. "General" means that the method needs neither commutativity nor an inverse.

| method | needs | query | insert | evict, worst | evict, amortized | space |
|---|---|---|---|---|---|---|
| recalculation | general | $n - 1$ | 0 | 0 | 0 | $n$ |
| subtract on evict | an inverse | 0 | 1 | 1 | 1 | $n + 1$ |
| [segment tree](/segment-tree/) over a [circular buffer](/circular-buffer/) | general, fixed $W$ | $O(\log W)$ | $O(\log W)$ | $O(\log W)$ | $O(\log W)$ | about $2W$ |
| B-Int (Arasu and Widom 2004) | general | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ | about $2n$ |
| FlatFAT, Reactive Aggregator (2015) | general | $O(\log n)$ | $O(n)$ | $O(n)$ | $O(\log n)$ | $2n$ to $4n$ |
| [Two-Stacks](/two-stacks-queue/) | general, FIFO | 1 | 1 | $n$ | 0 (2 per insert) | $2n$ |
| [DABA](/daba-queue/) (2017) | general, FIFO | 1 | 4 | 3 | 1.5 on average | $2n$ |
| DABA Lite (2021) | general, FIFO | 1 | 3 | 2 | | $n + 2$ |
| [monotonic deque](/monotonic-deque/) | $x \otimes y \in \{x, y\}$ | 0 | $O(n)$ | $O(1)$ | $O(1)$ (insert) | at most $n$ |

The amortized cost of a Two-Stacks evict is 0 when each insert is charged 2 calls, and DABA's averages are 2.5 per insert and 1.5 per evict. For FlatFAT the worst case $O(n)$ comes from resizing the array when the window grows; for a fixed $n$ each update walks one leaf-to-root path, $O(\log n)$ calls. The Reactive Aggregator processes $m$ updates in one batch with $O(m + m \log(n/m))$ calls, and does not need FIFO order. The bounds of the last five rows that are not proved on the linked pages are cited from Tangwongsan, Hirzel and Schneider, Section 8.1, which also lists FlatFIT (2017), Hammer Slide (2018), AMTA (2019) and the out-of-order finger B-tree FiBA (2019), all amortized $O(1)$ for FIFO windows with a worst case of $O(n)$ or $O(\log n)$.

## Bounds

**Space, proved here.** For the free monoid of strings over an alphabet $\Sigma$ with $|\Sigma| \ge 2$, any structure that supports evict and query must be able to tell apart all $|\Sigma|^n$ windows of length $n$: evicting the items one at a time and querying after each evict returns the suffixes $v_2 \cdots v_n, v_3 \cdots v_n, \ldots$, and from them the whole window can be read off. So two windows that differ must lead to different states, and the state needs at least $n \log_2 |\Sigma|$ bits. Storing the $n$ items themselves meets this bound, and Two-Stacks, DABA and DABA Lite store at most about $2n$ elements.

**Time, proved here.** In the free monoid, after $\mathrm{insert}(v)$ into a non-empty window with aggregate $a$, the answer $a \otimes v$ contains the new letter $v$ and is longer than $v$, so only a call of $\otimes$ made after $v$ arrived can produce it. So an insert followed by a query needs at least one call. DABA's worst-case 1, 4 and 3 calls are constant, so for FIFO windows no general method can be better by more than a constant factor.

## Reductions

- **Count-based window to SWAG.** Insert each item and evict when the size exceeds $W$: one insert, at most one evict and one query per item.
- **Time-based window to SWAG.** Store (timestamp, value) pairs, insert each item, and before a query at time $t$ evict while the oldest timestamp is at most $t - T$. Each item is inserted and evicted once, so the cost per item stays $O(1)$ amortized, even though one query may evict many items.
- **Lift, combine, lower.** A statistic $f$ that is not itself an associative operator often factors as a lift $\ell : X \to M$, a monoid $M$ and a lower map $M \to Y$, as for the mean $= \text{sum}/\text{count}$. The window structure then works on $\ell(x)$ values, and the query applies the lower map once.
- **Queue with minimum.** With $\otimes = \min$, SWAG is the [queue with minimum](/min-queue/).

## Applications

Windowed aggregates are the core of continuous queries in stream processing: rolling sums and averages in monitoring, the maximum price over the last minute in trading, rate limits over a recent period, and sketches of recent traffic in networks. A [moving average](/moving-average/) is the invertible case. Decayed aggregates, such as the [exponential moving average](/exponential-moving-average/) and [forward decay](/forward-decay/), avoid evictions by fading old items instead of removing them.

## References
