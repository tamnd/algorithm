---
tag: 670N1S
kind: problem
slug: basic-counting
name: Basic counting
aliases:
- counting ones in a sliding window
- count of 1s in the last N bits
- count of 1s in the last W bits
- basic counting problem
area: online-and-streaming/sliding-windows
level: core
summary: Count the 1s among the last W bits of a bit stream; exact answers need W bits, a relative error eps needs Theta((1/eps) log^2 W) bits.
prereqs: [sliding-window-model, count-based-window, relative-error]
see_also: [dgim-algorithm, exponential-histogram, exponential-histogram-bound, sliding-window-model, time-based-window, smooth-histogram, approximate-counting-problem, fixed-window-counter]
sources:
  - paper: doi:10.1137/S0097539701398363
    title: Mayur Datar, Aristides Gionis, Piotr Indyk and Rajeev Motwani, Maintaining stream statistics over sliding windows, SIAM Journal on Computing 31(6), 2002
    locator: the basic counting problem, the exponential histogram for it, and the lower bounds for exact and approximate counting
  - book: isbn:9781107077232
    title: Jure Leskovec, Anand Rajaraman and Jeffrey D. Ullman, Mining of Massive Datasets, second edition, Cambridge University Press, 2014
    locator: Chapter 4, Section 4.6, Counting Ones in a Window
  - paper: doi:10.1145/564870.564880
    title: Phillip B. Gibbons and Srikanta Tirthapura, Distributed streams algorithms for sliding windows, SPAA 2002
    locator: pp. 63 to 72, waves for basic counting over a sliding window and over the union of distributed streams
---

Basic counting is the problem of keeping the number of 1s among the last $W$ bits of a bit stream, so that a query at any time gets the count. It is the first problem of the [sliding window model](/sliding-window-model/), studied by Datar, Gionis, Indyk and Motwani (DGIM) in 2002. An exact answer needs $W$ bits of memory, as much as storing the window. With a [relative error](/relative-error/) $\varepsilon$, the [DGIM algorithm](/dgim-algorithm/) needs only $O(\frac{1}{\varepsilon} \log^2 W)$ bits, and this is optimal. On this page $\sigma = b_1, b_2, \ldots$ is the bit stream, $t$ is the current time and $W$ is the window size.

## In plain words

A stream of zeros and ones comes in, one at a time. At any moment you must say how many ones are among the most recent fixed number of items. If you keep every recent item, you can answer exactly. But you cannot do better than that for exact answers: any shorter memory confuses two histories that later give different answers. If an answer within a small percentage is good enough, you can keep much less. You remember groups of ones and only the time of the newest one in each group, with groups that get larger the older they are.

## Definition

**Input.** A window size $W \ge 1$, known in advance, and a bit stream $b_1, b_2, \ldots$ with $b_i \in \{0, 1\}$, read one bit at a time.

**Query.** At any time $t$, return the count
$$c(t) = \sum_{i = \max(1,\, t-W+1)}^{t} b_i .$$

**Exact version.** The answer must equal $c(t)$.

**Approximate version.** For a given $\varepsilon \in (0, 1)$, a deterministic algorithm must return $\hat c(t)$ with $|\hat c(t) - c(t)| \le \varepsilon\, c(t)$ at every time $t$. A randomized algorithm must do so with probability at least $1 - \delta$ for each fixed query time. The cost is the space in bits, the update time per bit and the query time.

## Variants

- **Any window up to $W$.** A query gives $w \le W$ and asks for the count of the last $w$ bits. DGIM answers it with the same structure and the same error.
- **Time-based windows.** Each bit has a timestamp, and the window holds the bits of the last $W$ time units; see [time-based window](/time-based-window/).
- **Sums.** The items are integers in $\{0, \ldots, R\}$ and the query asks for the sum over the window. The [exponential histogram](/exponential-histogram/) solves it in $O(\frac{1}{\varepsilon} \log W (\log W + \log R))$ bits. With negative values allowed, each constant-factor approximation needs $\Omega(W)$ bits (DGIM).
- **Additive error.** The answer may be off by $\varepsilon W$. Then the counts of the tumbling blocks of length $\lceil \varepsilon W \rceil$ suffice: keep the counts of the last $\lceil 1/\varepsilon \rceil + 1$ blocks, return the sum of the blocks that start inside the window plus the current block, and lose at most one partial block. This uses $O(\frac{1}{\varepsilon} \log W)$ bits.
- **Distributed streams.** Several parties see different streams, and the query asks for the count over the union of their windows. Gibbons and Tirthapura (2002) solve it with randomized waves.

## Examples

Let $W = 8$ and let the stream be $1, 0, 1, 1, 0, 1, 1, 1, 0, 1$. The exact counts at times 1 to 10 are $1, 1, 2, 3, 3, 4, 5, 6, 5, 6$. At time 9 the window is $b_2, \ldots, b_9 = 0, 1, 1, 0, 1, 1, 1, 0$, with 5 ones, because $b_1 = 1$ has expired. With $\varepsilon = 1/2$, every answer in $[2.5, 7.5]$ is correct at time 9. The [DGIM algorithm](/dgim-algorithm/) page runs its buckets on this stream.

## Known algorithms

| Algorithm | Space | Update | Query | Guarantee |
|---|---|---|---|---|
| Circular buffer of $W$ bits and a counter | $W + O(\log W)$ bits | $O(1)$ worst case | $O(1)$ | exact |
| [DGIM](/dgim-algorithm/) (exponential histogram) | $O(\frac{1}{\varepsilon} \log^2 W)$ bits | $O(1)$ amortized, $O(\log W)$ worst case | $O(1)$ | deterministic relative error $\varepsilon$ |
| Deterministic waves (Gibbons and Tirthapura 2002) | $O(\frac{1}{\varepsilon} \log^2 W)$ bits | $O(1)$ worst case | $O(1)$ | deterministic relative error $\varepsilon$ |
| Tumbling block counts | $O(\frac{1}{\varepsilon} \log W)$ bits | $O(1)$ | $O(1)$ | additive error $\varepsilon W$ |

The circular buffer keeps $b_{t-W+1}, \ldots, b_t$ and the count $c$. At each new bit it subtracts the bit that leaves, adds the new bit and overwrites the slot.

## Bounds

**Exact counting needs $W$ bits.** *Theorem.* Each deterministic algorithm that answers exact basic counting queries with window size $W$ has at least $2^W$ distinct memory states, so it uses at least $W$ bits.

*Proof.* Let $x \ne y$ be two strings in $\{0,1\}^W$, and feed each one to the algorithm as the first $W$ bits of a stream. Let $i$ be the largest index with $x_i \ne y_i$, so $x_p = y_p$ for all $p > i$. Suppose that the memory states after $x$ and after $y$ are the same. Feed $i - 1$ more zeros to both runs. The algorithm is deterministic, so both runs reach the same state and give the same answer at time $W + i - 1$. The window at that time holds positions $i, \ldots, W$ of the string, then $i - 1$ zeros. Its count is $x_i + \sum_{p > i} x_p$ for $x$ and $y_i + \sum_{p > i} y_p$ for $y$. These two counts differ by $|x_i - y_i| = 1$, so one of the two answers is wrong. This contradicts exactness. So the $2^W$ strings lead to $2^W$ distinct states. A memory of $s$ bits has at most $2^s$ states, so $s \ge W$. $\square$

The circular buffer shows that $W + O(\log W)$ bits suffice, so the bound is tight up to the counter.

**Approximate counting.** DGIM prove that each algorithm for relative error $\varepsilon$, deterministic or randomized, needs $\Omega(\frac{1}{\varepsilon} \log^2(\varepsilon W))$ bits. The [space theorem](/exponential-histogram-bound/) page proves the upper bound $O(\frac{1}{\varepsilon} \log^2 W)$ and the deterministic lower bound in full, and cites the randomized one. For constant $\varepsilon$ the answer is $\Theta(\log^2 W)$ bits: more than the $\log W$ bits of one counter, because the algorithm must also know when the counted 1s expire.

## Reductions

- Basic counting is the special case of the sum over a window with values in $\{0, 1\}$, so each lower bound for basic counting holds for sums, and each sum algorithm solves basic counting.
- A count of the items that satisfy a fixed predicate over a window is basic counting on the bit stream of the predicate values.
- The [DGIM algorithm](/dgim-algorithm/) is a special case of the [smooth histogram](/smooth-histogram/) idea for the count, which is a [smooth function](/smooth-function/).

## Applications

- Network monitoring: the number of packets of a given kind, or of failed requests, in the last $W$ packets.
- Rate limits and alarms that fire when the count of events in the last $W$ events passes a threshold.
- A building block for other window statistics: sums, averages ($\text{sum} / \text{count}$ with both approximate), the [moving average](/moving-average/) of bounded values, and the [heavy hitters](/sliding-window-heavy-hitters/) of a window.

## References
