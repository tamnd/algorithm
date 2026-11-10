---
tag: 130NZR
kind: problem
slug: sliding-window-heavy-hitters
name: Sliding window heavy hitters
aliases:
- frequent items over a window
- sliding-window frequency estimation
area: online-and-streaming/sliding-windows
level: advanced
summary: Estimate item frequencies in the last W items within eps*W and report the items above a fraction phi of the window; O(1/eps) words suffice, and Misra-Gries per block is a simple method.
prereqs: [misra-gries-summary, sliding-window-model]
see_also: [misra-gries-summary, space-saving, count-min-sketch, sliding-window-quantiles, exponential-histogram, basic-counting, forward-decay, count-based-window]
sources:
  - paper: doi:10.1145/1055558.1055598
    title: Arvind Arasu and Gurmeet Singh Manku, Approximate counts and quantiles over sliding windows, PODS 2004
    locator: the frequency-count algorithms for fixed-size and variable-size windows, with O((1/eps) log^2(1/eps)) space for fixed-size windows
  - paper: doi:10.1145/1142351.1142393
    title: Lap-Kei Lee and H. F. Ting, A simpler and more efficient deterministic scheme for finding frequent items over sliding windows, PODS 2006
    locator: the frequent-items scheme for count-based windows with O(1/eps) space
  - paper: "Regant Y. S. Hung, Lap-Kei Lee and H. F. Ting, Finding frequent items over sliding windows with constant update time, Information Processing Letters 110(7), 2010"
    locator: pages 257 to 260, O(1/eps) space with O(1) update time
  - paper: doi:10.1109/INFOCOM.2016.7524364
    title: Ran Ben-Basat, Gil Einziger, Roy Friedman and Yaron Kassner, Heavy hitters in streams and sliding windows, INFOCOM 2016
    locator: Window Compact Space-Saving, with O(1) worst-case update and query time and O(1/eps) space, which matches the lower bound
---

The sliding window heavy hitters problem asks, over the last $W$ items of a stream, for every item whose frequency is at least a fraction $\varphi$ of the window, and for frequency estimates with an additive error of at most $\varepsilon W$. Exact counts need memory for the whole window, so the problem is approximate. A simple method runs a [Misra-Gries summary](/misra-gries-summary/) on each block of about $\varepsilon W / 2$ items and uses $O(1/\varepsilon^2)$ words; Arasu and Manku (2004), Lee and Ting (2006) and Ben-Basat, Einziger, Friedman and Kassner (2016) reduced the memory to $O(1/\varepsilon)$ words, which is optimal.

## In plain words

You watch the last ten thousand requests to a server and want to know which users make a large share of them. Counting every user exactly takes a lot of memory, and the counts must also go down as old requests leave. The way out is to accept small errors. Cut the stream into short pieces, keep a small summary of the most frequent users in each piece, and drop a piece's summary when the piece gets too old. Adding up the summaries of the pieces still in view gives each user's count to within a small margin. Any user with a large share shows up in some summary, so none is missed.

## Definition

The input is a stream $x_1, x_2, \ldots$ of items from a universe $U$, a window size $W$, an accuracy $0 < \varepsilon \le 1$ and a threshold $\varphi > \varepsilon$. After item $t$, let $f(x)$ be the number of positions $i$ with $t - W < i \le t$ and $x_i = x$.

- **Frequency estimation.** For any $x$, return $\hat{f}(x)$ with $f(x) - \varepsilon W \le \hat{f}(x) \le f(x)$, or with $|\hat{f}(x) - f(x)| \le \varepsilon W$.
- **Heavy hitters.** Return a set $H$ that contains every $x$ with $f(x) \ge \varphi W$ and no $x$ with $f(x) < (\varphi - \varepsilon) W$.

An algorithm for the first gives one for the second: report the stored items with $\hat{f}(x) \ge (\varphi - \varepsilon) W$. The model is the count-based window of the [sliding window model](/sliding-window-model/); memory is counted in words of $O(\log |U| + \log W)$ bits.

## Variants

- **Time-based windows.** The window holds the items of the last $T$ time units, so $W$ is replaced by the current number of items $n$, which changes. Arasu and Manku call these variable-size windows, and their bounds gain a factor that depends on the logarithm of the stream size.
- **Weighted items.** Each item carries a weight, such as bytes per packet.
- **Randomized sketches.** A [count-min sketch](/count-min-sketch/) whose cells are sliding-window counters, such as [exponential histograms](/exponential-histogram/), answers frequency queries for any item with high probability, and also handles time-based windows.
- **Time decay.** Instead of a hard window, decayed counts weigh recent items more; with [forward decay](/forward-decay/) any weighted frequency summary such as [Space-Saving](/space-saving/) works unchanged.

## Examples

$W = 8$ and $\varepsilon = 1/2$, so the block length is $b = \lfloor \varepsilon W / 2 \rfloor = 2$ and each block summary has $k = \lceil 2/\varepsilon \rceil = 4$ counters. The stream is a a b a c a a b d d a, with positions 1 to 11.

At $t = 11$ the window holds positions 4 to 11, the items a c a a b d d a, with $f(a) = 4$. The finished blocks are positions 1 and 2, 3 and 4, 5 and 6, 7 and 8, and 9 and 10. The blocks that start at 1 and at 3 are dropped, because their first position is outside the window. The kept summaries are $\{c: 1, a: 1\}$, $\{a: 1, b: 1\}$ and $\{d: 2\}$, and the current partial block is $\{a: 1\}$. So $\hat{f}(a) = 1 + 1 + 0 + 1 = 3$. The error 1 comes from position 4, which is in the window but in the dropped block, and it is less than $\varepsilon W = 4$.

## Known algorithms

**Misra-Gries per block.** Let $b = \max(1, \lfloor \varepsilon W / 2 \rfloor)$ and $k = \lceil 2/\varepsilon \rceil$. Cut the stream into blocks of $b$ consecutive positions, starting at position 1. Keep a Misra-Gries summary $M_{\text{cur}}$ with $k$ counters for the current block, and a queue $Q$ of the summaries of the finished blocks that lie entirely in the window.

```pseudo id=main
STEP(x)
L1  t ← t + 1; update M_cur with x, using k counters
L2  if b divides t then
L3      append (t − b + 1, M_cur) to Q; M_cur ← an empty summary
L4  while Q is not empty and the first block of Q starts at or before t − W do remove it from Q
ESTIMATE(x)
L5  return M_cur[x] plus the sum of M[x] over the summaries (s, M) in Q
```

*Error.* A Misra-Gries summary with $k$ counters over $m$ items underestimates each count by at most $m/(k + 1)$ and never overestimates. The blocks in $Q$ and the current block contain only positions in the window, at most $W$ in total, so their summaries lose at most $W/(k + 1) < \varepsilon W / 2$ together. The only other window positions are in the block that straddles the window edge, which line L4 has removed: at most $b - 1 < \varepsilon W / 2$ positions. So $f(x) - \varepsilon W < \hat{f}(x) \le f(x)$ for every $x$. When $b = 1$ no block straddles the edge, and each summary is exact.

*Cost.* $Q$ holds at most $\lfloor W/b \rfloor \le 4/\varepsilon$ summaries, since a block in $Q$ lies in the window, and each has at most $k$ counters, so the memory is $O(1/\varepsilon^2)$ words. A Misra-Gries update takes $O(1)$ amortized time with hashing, because a decrement of all $k$ counters removes $k$ units that earlier increments created. Line L4 removes each summary once. An estimate costs $O(1/\varepsilon)$ lookups, and a heavy-hitter report checks the $O(1/\varepsilon^2)$ stored keys.

**Better methods.**

| method | memory in words | update time | notes |
|---|---|---|---|
| exact counts of the window | $O(W)$ | $O(1)$ | the baseline |
| Misra-Gries per block, above | $O(1/\varepsilon^2)$ | $O(1)$ amortized | proved on this page |
| Arasu and Manku (2004) | $O(\frac1\varepsilon \log^2 \frac1\varepsilon)$ | | levels of blocks of growing sizes; also variable-size windows |
| Lee and Ting (2006) | $O(1/\varepsilon)$ | | a simpler deterministic scheme |
| Hung, Lee and Ting (2010) | $O(1/\varepsilon)$ | $O(1)$ | |
| Window Compact Space-Saving, Ben-Basat et al. (2016) | $O(1/\varepsilon)$ | $O(1)$ worst case, $O(1)$ query | optimal memory |
| count-min sketch with window counters | $O(\frac1\varepsilon \log \frac1\delta)$ window counters | $O(\log \frac1\delta)$ counter updates | randomized, error in both directions |

The bounds of the last four rows are cited from the papers.

## Bounds

**Memory, proved here.** Every deterministic structure that answers frequency queries with $|\hat{f}(x) - f(x)| < \varepsilon W$ over a universe of size $|U|$ needs at least $\log_2 \binom{|U|}{m}$ bits, where $m = \lfloor 1/(2\varepsilon) \rfloor$. Take any set $S$ of $m$ items and a window in which each item of $S$ appears at least $W/m \ge 2\varepsilon W$ times. Then $\hat{f}(x) > \varepsilon W$ for $x \in S$ and $\hat{f}(x) < \varepsilon W$ for $x \notin S$, so the answers reveal $S$, and different sets need different states. Since $\binom{|U|}{m} \ge (|U|/m)^m$, this is $\Omega(\frac1\varepsilon \log(\varepsilon |U|))$ bits, or $\Omega(1/\varepsilon)$ words, which the $O(1/\varepsilon)$ methods meet. The same argument holds for a whole stream, so the window costs no more than a constant factor in memory.

**Output.** At most $1/(\varphi - \varepsilon)$ items can have $f(x) \ge (\varphi - \varepsilon) W$, which bounds the size of a correct report.

## Reductions

- **Heavy hitters to frequency estimation**, by thresholding the stored candidates at $(\varphi - \varepsilon) W$.
- **To basic counting.** For one fixed item, the count over the window is the [basic counting](/basic-counting/) problem on the bit stream $[x_i = x]$.
- **Levels of blocks.** Instead of one block length, blocks of several lengths can be kept in levels, with fewer counters for shorter blocks, as in the structure of Arasu and Manku; this is how the memory falls below $O(1/\varepsilon^2)$.

## Applications

Finding the heaviest flows or source addresses in recent network traffic for anomaly and attack detection; trending queries and hashtags over the last hour; hot keys in caches and databases, where load must be balanced across servers; and top sellers or top errors in monitoring dashboards.

## References
