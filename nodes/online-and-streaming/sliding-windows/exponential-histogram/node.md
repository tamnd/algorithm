---
tag: PRB8V8
kind: data-structure
slug: exponential-histogram
name: Exponential histogram
aliases:
- EH
- sliding-window histogram
- exponential histogram of Datar et al.
area: online-and-streaming/sliding-windows
level: advanced
summary: Buckets with power-of-2 sizes, about k/2 of each size, that keep the sum of the last W integers in {0, ..., R} with relative error below 1/k.
model: word-ram
complexity:
  vars: {W: the window size, k: the accuracy parameter (relative error below 1/k), R: the largest item value}
  time: {amortized: O(R), worst: O((R + k) log(W R))}
  space: {extra: O(k (log W + log R) log W)}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 2002
  people: [Mayur Datar, Aristides Gionis, Piotr Indyk, Rajeev Motwani]
  note: Datar, Gionis, Indyk and Motwani introduced the exponential histogram in 2002 for basic counting, sums of bounded integers and other functions over sliding windows.
prereqs: [dgim-algorithm, basic-counting, sliding-window-model]
see_also: [dgim-algorithm, exponential-histogram-bound, smooth-histogram, smooth-function, basic-counting, time-based-window, moving-average, sliding-window-aggregation]
sources:
  - paper: doi:10.1137/S0097539701398363
    title: Mayur Datar, Aristides Gionis, Piotr Indyk and Rajeev Motwani, Maintaining stream statistics over sliding windows, SIAM Journal on Computing 31(6), 2002
    locator: the exponential histogram, its use for sums of integers in a bounded range and for weakly additive functions, and the lower bounds for sums
  - paper: doi:10.1137/090749281
    title: Vladimir Braverman and Rafail Ostrovsky, Effective computations on sliding windows, SIAM Journal on Computing 39(6), 2010
    locator: Section 1 (the comparison with exponential histograms and weakly additive functions)
  - book: isbn:9781107077232
    title: Jure Leskovec, Anand Rajaraman and Jeffrey D. Ullman, Mining of Massive Datasets, second edition, Cambridge University Press, 2014
    locator: Chapter 4, Section 4.6, Counting Ones in a Window (the extension to sums of integers)
---

An exponential histogram is a summary of the last $W$ items of a stream that keeps their sum, for items that are integers in $\{0, \ldots, R\}$, with [relative error](/relative-error/) less than $1/k$ in $O(k (\log W + \log R) \log W)$ bits. It keeps buckets whose sizes are powers of 2, with about $k/2$ buckets of each size, and for each bucket only the time of its newest unit. Datar, Gionis, Indyk and Motwani introduced it in 2002; the [DGIM algorithm](/dgim-algorithm/) is its special case $R = 1$. It works in the [sliding window model](/sliding-window-model/) with a [count-based window](/count-based-window/). On this page $\sigma = v_1, v_2, \ldots$ is the stream, $t$ is the current time, and $L = \lceil k/2 \rceil$.

## In plain words

Think of each item as a pile of coins: the value says how many coins. The structure does not keep the coins of each item. It ties the coins into bags of one, two, four, eight and more, with the newest coins in the small bags and the older coins in the big bags. On each bag it writes only the time of its newest coin. When there are too many bags of one size, the two oldest are tied into one bag of twice the size. A bag leaves when its time is too old. The answer is the number of coins in all bags, with half of the oldest bag, because only that bag can hold coins from outside the window.

## The abstract type

The structure keeps a window sum. The parameters are $W \ge 1$, $k \ge 1$ and $R \ge 0$, fixed at creation.

- `update(v)`, with $v \in \{0, \ldots, R\}$: append $v$ to the stream and advance the time by 1.
- `query(w)`, with $1 \le w \le W$: return $\hat s$ with $|\hat s - s| < s/k$ when $s \ge 1$, and $\hat s = 0$ when $s = 0$, where $s = \sum_{i > t - w} v_i$ is the sum of the last $w$ items.

The guarantee is deterministic and holds at each query.

## Representation

An item of value $v$ at time $t$ is $v$ **units**, each with timestamp $t$. A **bucket** stands for $2^j$ consecutive units in the order of arrival; it stores its timestamp, the timestamp of its newest unit. Level $j$ is a circular array with the timestamps of the buckets of size $2^j$, newest first. The structure also keeps $t \bmod W$ and the total of all bucket sizes.

**The bucket rule.** Let $r$ be the largest level present. Each level $j < r$ has $L$ or $L + 1$ buckets, level $r$ has 1 to $L + 1$, and the sizes do not decrease from the newest bucket to the oldest one. Unlike in DGIM, several buckets can have the same timestamp, when they hold units of one item.

## Operations

```pseudo id=main
EH-UPDATE(v)                            ▷ 0 ≤ v ≤ R; L = ⌈k/2⌉
L1  t ← t + 1
L2  while the oldest bucket has timestamp ≤ t − W do remove it
L3  repeat v times
L4      add the bucket (t, 1) as the newest bucket of level 0
L5      j ← 0
L6      while level j has L + 2 buckets do
L7          remove the two oldest buckets of level j; add a bucket of size 2^(j+1) with the newer of their two timestamps, as the newest bucket of level j + 1
L8          j ← j + 1

EH-QUERY(w)                             ▷ 1 ≤ w ≤ W
L9  B ← the buckets with timestamp > t − w; if B is empty then return 0
L10 2^r ← the size of the oldest bucket of B; S ← the sum of the sizes of the other buckets of B
L11 return S + (2^r + 1)/2
```

Line L2 can remove many buckets in one step: all the buckets that hold units of the item that leaves the window. Lines L3 to L8 insert the units one by one, each with the merge cascade of DGIM.

## Example

Take $W = 4$, $k = 2$ (so $L = 1$) and $R = 3$, with the stream $2, 0, 3, 1, 2, 0, 3$. Buckets are (timestamp, size), newest first.

| $t$ | $v_t$ | buckets after the update | estimate | true sum |
|---|---|---|---|---|
| 1 | 2 | (1, 1), (1, 1) | 2 | 2 |
| 3 | 3 | (3, 1), (3, 2), (1, 2) | 9/2 | 5 |
| 5 | 2 | (5, 1), (5, 1), (4, 2), (3, 2) | 11/2 | 6 |
| 7 | 3 | (7, 1), (7, 2), (5, 4) | 11/2 | 6 |

At $t = 3$ the first new unit makes three buckets of size 1, and the two oldest, both of time 1, merge into (1, 2). The second and third units then merge into (3, 2). At $t = 5$ line L2 removes (1, 2), because the item of time 1 has left the window $\{2, 3, 4, 5\}$. At $t = 7$ the window is the items $1, 2, 0, 3$, with sum 6; the estimate $1 + 2 + (4 + 1)/2 = 11/2$ has relative error $1/12$.

## Correctness

The proof is on the [proof page](proofs/correctness.md). It is the DGIM proof applied to the stream of units. The buckets cover consecutive blocks of units, and each unit that is in no bucket belongs to an item that has left the window. For a query, all buckets of $B$ but the oldest lie inside the last $w$ items, and the oldest has at least its newest unit inside, so the sum is in $[S + 1, S + 2^r]$. If $r \ge 1$, the bucket rule gives $S \ge L(2^r - 1)$, and the midpoint has relative error at most $(2^r - 1)/(2(L(2^r - 1) + 1)) < 1/(2L) \le 1/k$.

## Complexity

The bounds below are proved on the proof page, except the lower bounds, which are cited.

- **Buckets.** At most $(L + 1)(\lfloor \log_2 \frac{WR - 1}{L} + 1 \rfloor + 1)$, because the window sum is at most $WR$. For $W = 4$, $k = 2$ and $R = 3$ this is 8.
- **Space.** Each timestamp is a time in the window, kept modulo $W$ in $\lceil \log_2 W \rceil$ bits. So the space is $O(k \log(WR) \log W) = O(k (\log W + \log R) \log W)$ bits.
- **Update time.** Inserting the $v$ units one by one costs $O(v)$ amortized, since there are fewer merges than units, and $O(v \log(WR))$ in the worst case. The expiry of line L2 costs $O(1)$ amortized, since each bucket is removed once, and $O(k \log(WR))$ in the worst case, when all buckets of one old item leave together.
- **Query time.** $O(1)$ for $w = W$ from the total and the oldest bucket, and $O(k \log(WR))$ for a general $w$.
- **Lower bounds (cited).** DGIM prove that the sum of integers in $\{0, \ldots, R\}$ with relative error $\varepsilon$ needs $\Omega(\frac{1}{\varepsilon} \log W (\log W + \log R))$ bits, so the space is optimal. The case $R = 1$ is the [space theorem](/exponential-histogram-bound/) for basic counting.

## Variants

- **Basic counting.** With $R = 1$, the structure is the [DGIM algorithm](/dgim-algorithm/).
- **Fast insertion of large values.** The insertion of lines L3 to L8 is slow for large $v$. A batched insertion adds all $v$ units at level 0 at once and carries the overflow from level to level, as in binary addition; equal timestamps let it treat the new buckets of one level as one group.
- **Weakly additive functions.** DGIM apply the same buckets to functions $f$ of a set of items with $f(A) + f(B) \le f(A \cup B) \le C_f\,(f(A) + f(B))$ for disjoint $A$ and $B$, where each bucket keeps a summary from which $f$ of a union can be computed. For example, $F_p = \sum_i f_i^p$ with $p \ge 1$ satisfies these inequalities with $C_f = 2^{p-1}$, because $a^p + b^p \le (a + b)^p \le 2^{p-1}(a^p + b^p)$ for $a, b \ge 0$. The approximation factor then depends on $C_f$.
- **Smooth histograms.** Braverman and Ostrovsky (2007) keep whole sketches started at chosen times instead of buckets, and get a better factor for [smooth functions](/smooth-function/); see [smooth histogram](/smooth-histogram/).
- **Time-based windows.** With timestamps, an item of a [time-based window](/time-based-window/) is inserted at its time, and line L2 removes all buckets older than $W$ time units. The bucket count depends on the largest sum in a window instead of $WR$.

## When to use it

Use it for an approximate sum or count over the last $W$ items when $W$ is large and many windows must be kept at once, for example one per flow or per user. For exact sums over a stored window, use a circular buffer, or the [two-stacks queue](/two-stacks-queue/) for other associative aggregates; see [sliding-window aggregation](/sliding-window-aggregation/). For weights that fade with age instead of a hard window, see the [exponential moving average](/exponential-moving-average/).

## Pitfalls

- **Negative values.** The structure needs $v \ge 0$. DGIM prove that sums with negative values need $\Omega(W)$ bits for each constant-factor approximation, so no small structure can fix this.
- **Expiry of one item.** One item can be split over several buckets with the same timestamp. Line L2 must loop until the oldest bucket is inside the window; removing one bucket per step leaves expired units.
- **The half-bucket estimate.** As for DGIM, returning $S + 2^r/2$ with only $\lceil k/2 \rceil$ buckets per size can exceed the error $1/k$. Use the midpoint of line L11.
- **The average.** The window average is the sum divided by the number of items. For a count-based window the number of items is $\min(t, W)$, so the error stays $1/k$. For a time-based window the count is also approximate, and the two relative errors add up to about $2/k$.

## Implementations

## History

Datar, Gionis, Indyk and Motwani introduced the exponential histogram at SODA 2002 and in SIAM Journal on Computing in 2002, for basic counting, for sums of bounded integers, and for weakly additive functions. They proved the matching lower bounds for counting and for sums. Braverman and Ostrovsky (2007) generalized the idea from buckets to sketches with smooth histograms.

## References
