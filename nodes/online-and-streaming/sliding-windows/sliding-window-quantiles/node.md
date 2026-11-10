---
tag: MXBG8V
kind: problem
slug: sliding-window-quantiles
name: Sliding window quantiles
aliases:
- approximate quantiles over a window
- sliding-window quantile summary
- windowed percentiles
area: online-and-streaming/sliding-windows
level: research
summary: Answer approximate rank and quantile queries, within eps*n in rank, over the last W items of a stream; Arasu and Manku (2004) use O((1/eps) log(1/eps) log W) words for fixed windows.
prereqs: [quantile, greenwald-khanna-summary, sliding-window-model]
see_also: [sliding-window-median, greenwald-khanna-summary, kll-sketch, q-digest, sliding-window-heavy-hitters, mergeable-summaries, time-based-window, count-based-window]
sources:
  - paper: doi:10.1145/1055558.1055598
    title: Arvind Arasu and Gurmeet Singh Manku, Approximate counts and quantiles over sliding windows, PODS 2004
    locator: the quantile algorithms for fixed-size windows, O((1/eps) log(1/eps) log N) space, and for variable-size windows, O((1/eps) log(1/eps) log(eps N) log N) space
  - paper: "Xuemin Lin, Hongjun Lu, Jian Xu and Jeffrey Xu Yu, Continuously maintaining quantile summaries of the most recent N elements over a data stream, ICDE 2004"
    locator: the sliding-window quantile summaries for the most recent N items and for the n-of-N model, with space of order 1/eps^2 times a logarithmic factor
  - paper: "Graham Cormode and Pavel Veselý, A tight lower bound for comparison-based quantile summaries, PODS 2020"
    locator: the lower bound of Omega((1/eps) log(eps N)) words for deterministic comparison-based summaries of a stream of N items
---

The sliding window quantiles problem asks for a summary of the last $W$ items of a stream that answers rank and quantile queries with a rank error of at most $\varepsilon n$, where $n$ is the number of items in the window. Exact answers need memory for the whole window, as the [sliding window median](/sliding-window-median/) page proves, and the usual quantile summaries of a whole stream, such as the [Greenwald-Khanna summary](/greenwald-khanna-summary/), cannot forget items that leave. Lin, Lu, Xu and Yu (2004) gave summaries for this model with space of order $1/\varepsilon^2$, and Arasu and Manku (2004) reduced the space to $O(\frac1\varepsilon \log \frac1\varepsilon \log W)$ words for fixed-size windows.

## In plain words

A service wants the 99th percentile of its response times over the last minute. Keeping every response time of the last minute and sorting them works, but costs memory in proportion to the traffic. A small summary that keeps only some of the values can answer such questions approximately: it may return a value whose position in the sorted order is off by a small fraction of the window. The difficulty in a window is that old values must leave. The usual trick is to cut the stream into blocks, keep a small summary per block, drop whole blocks when they expire, and combine the remaining summaries at query time.

## Definition

The input is a stream $x_1, x_2, \ldots$ of items from a totally ordered set, a window, and an accuracy $0 < \varepsilon < 1$. Let $V$ be the multiset of items in the current window and $n = |V|$. The **rank** of a value $v$ is $r(v) = |\{y \in V : y \le v\}|$.

- **Rank query.** Given $v$, return $\hat{r}$ with $|\hat{r} - r(v)| \le \varepsilon n$.
- **Quantile query.** Given $\varphi \in [0, 1]$, return an item $y \in V$ whose position in the sorted order of $V$ is within $\varepsilon n$ of $\lceil \varphi n \rceil$.

For **fixed-size windows**, $V$ is the last $W$ items. For **variable-size windows**, the window is chosen by timestamps, so $n$ changes and is not known in advance; Arasu and Manku bound memory there in terms of the stream length $N$. A related model, the *n-of-N* model of Lin et al., keeps one summary of the last $N$ items that answers queries for the last $n$ items for every $n \le N$.

## Variants

- **Deterministic or randomized.** The bounds below are deterministic. Randomized summaries such as the [KLL sketch](/kll-sketch/) can be kept per block and merged, which gives smaller memory with a failure probability $\delta$.
- **Comparison-based or over a bounded universe.** Over integers in $\{0, \ldots, U - 1\}$, structures such as the [q-digest](/q-digest/) avoid storing items and use space that depends on $\log U$.
- **Relative error.** For tail percentiles such as the 99.9th, the error is wanted relative to the distance from the end of the order, not relative to $n$.
- **Exact median.** With $\varepsilon = 0$ the problem is the [sliding window median](/sliding-window-median/) and its other ranks, which need $\Omega(W)$ memory.

## Examples

$W = 8$, $\varepsilon = 1/8$, and the window $7, 1, 9, 3, 3, 8, 2, 5$. Sorted, it is $1, 2, 3, 3, 5, 7, 8, 9$. For the median, $\varphi = 1/2$, the exact position is 4, and any item at position 3, 4 or 5 is a correct answer, so 3 and 5 are both allowed. A rank query for $v = 6$ has the exact answer $r(6) = 5$, and any $\hat{r}$ in $[4, 6]$ is allowed.

Now the item 6 arrives and 7 leaves. The sorted window is $1, 2, 3, 3, 5, 6, 8, 9$, and $r(6)$ becomes 6. A summary of the whole stream still counts the 7, so its ranks describe all items seen so far and not the window. After many such steps its rank errors for the window grow without bound. A window summary must drop the effect of 7.

## Known algorithms

**Blocks.** The deterministic methods cited here cut the stream into blocks, keep a quantile summary for each block, discard a block summary when the block has left the window, and answer a query by combining the summaries of the blocks in the window. A rank estimate is the sum of the estimates of the blocks. The error has two sources: the error of each block summary, and the part of the window in the block that straddles the window edge, which is dropped. With one block length $b = \varepsilon W / 2$ and a summary with rank error at most $\varepsilon b / 2$ per block, the two sources give at most $\frac{W}{b} \cdot \frac{\varepsilon b}{2} + b = \varepsilon W$.

For the memory, run a [Greenwald-Khanna summary](/greenwald-khanna-summary/) with rank error $\varepsilon b / 4$ on the current block. When the block is full, query it at the ranks $\frac{\varepsilon b}{4}, \frac{2 \varepsilon b}{4}, \ldots$ and keep only these $O(1/\varepsilon)$ items, with their ranks. A rank estimate from these items is off by at most $\varepsilon b / 4$ from the spacing and $\varepsilon b / 4$ from the summary, so $\varepsilon b / 2$ in total. The window holds at most $W/b = 2/\varepsilon$ finished blocks, so the memory is $O(1/\varepsilon^2)$ items for them, plus $O(\frac1\varepsilon \log(\varepsilon W))$ for the current block. This is the same argument as the Misra-Gries method of [sliding window heavy hitters](/sliding-window-heavy-hitters/). The better methods use blocks of several sizes in levels, with coarser summaries for longer blocks.

| method | window | space in words | type |
|---|---|---|---|
| store and sort the window | both | $W$ | exact |
| one block size, as above | fixed | $O(1/\varepsilon^2 + \frac1\varepsilon \log(\varepsilon W))$ | deterministic |
| Lin, Lu, Xu and Yu (2004) | fixed, and the n-of-N model | order $1/\varepsilon^2$ times a logarithmic factor | deterministic |
| Arasu and Manku (2004), fixed | fixed | $O(\frac1\varepsilon \log \frac1\varepsilon \log W)$ | deterministic |
| Arasu and Manku (2004), variable | variable | $O(\frac1\varepsilon \log \frac1\varepsilon \log(\varepsilon N) \log N)$ | deterministic |
| randomized block summaries | both | depends on $\delta$ | randomized |

The bounds of the named rows are cited from the papers, with $N$ the stream length, which equals the window size for fixed windows in the Arasu and Manku bound.

## Bounds

Cormode and Veselý (2020) prove that a deterministic comparison-based quantile summary of a stream of $N$ items needs $\Omega(\frac1\varepsilon \log(\varepsilon N))$ words. The first $W$ items of a stream fill a fixed-size window, so the same bound with $N = W$ holds for windows. The Arasu and Manku bound for fixed windows is within a factor of $O(\log \frac1\varepsilon)$ of it. Whether the window adds any cost beyond this factor is, as far as the cited works state, open.

## Reductions

- **Frequencies from quantiles.** A rank summary with error $\varepsilon n$ estimates the count of a value $v$ as $\hat{r}(v) - \hat{r}(v^-)$, where $v^-$ is the largest value below $v$, with error $2 \varepsilon n$. So sliding window quantiles solve [sliding window heavy hitters](/sliding-window-heavy-hitters/) with $2\varepsilon$ in place of $\varepsilon$.
- **Exact order statistics.** With $\varepsilon = 0$ the problem is the sliding order statistic of the [sliding window median](/sliding-window-median/) page.
- **From whole-stream summaries.** Any summary that can be merged, as in [mergeable summaries](/mergeable-summaries/), gives a window summary by the block method, with the costs above.

## Applications

Latency percentiles over the last minute in service monitoring, such as the 50th, 95th and 99th percentiles of response times; delay and jitter distributions in network monitoring; equi-depth histograms over recent data for query optimization in stream databases; and detection of distribution shift, by comparing quantiles of the current window with those of an older one.

## References
