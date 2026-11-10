---
tag: M89V4P
kind: concept
slug: landmark-window
name: Landmark window
aliases:
- growing window
- cumulative window
area: online-and-streaming/sliding-windows
level: intro
summary: The window from a fixed start point, the landmark, to the current time; it only grows until the landmark moves.
prereqs: [streaming-model, cash-register-model]
see_also: [sliding-window-model, tumbling-window, hopping-window, session-window, count-based-window, time-based-window, exponential-decay, cash-register-model]
sources:
  - paper: doi:10.1145/375663.375665
    title: Johannes Gehrke, Flip Korn and Divesh Srivastava, On computing correlated aggregates over continual data streams, SIGMOD 2001
    locator: the definitions of landmark windows and sliding windows for correlated aggregates
  - paper: doi:10.1016/B978-155860869-6/50039-1
    title: Yunyue Zhu and Dennis Shasha, StatStream, statistical monitoring of thousands of data streams in real time, VLDB 2002
    locator: pp. 358 to 369, the window models of the paper
  - paper: doi:10.1007/s00778-022-00778-6
    title: Juliane Verwiebe, Philipp M. Grulich, Jonas Traub and Volker Markl, Survey of window types for aggregation in stream processing systems, The VLDB Journal 32, 2023
    locator: Section 5.4, landmark windows
---

A landmark window holds all the items of a stream from a fixed start point, the landmark, up to the current time. It grows with each new item and never loses one, until the landmark itself moves, for example at midnight, and then the window starts again from empty. Gehrke, Korn and Srivastava (2001) computed aggregates over landmark windows and over sliding windows, and Zhu and Shasha (2002) used landmark windows, with sliding and damped windows, in StatStream. On this page $\sigma = a_1, a_2, \ldots$ is the stream, $\tau_i$ is the timestamp of $a_i$, $\ell$ is the landmark and $t$ is the current time.

## In plain words

A landmark window answers questions such as "how many orders since midnight" or "the largest value since the machine started". It has a fixed start and an end that moves with the clock. Nothing leaves the window, so it is as easy to handle as a stream with no deletions: an algorithm only adds new items. When the start moves to a new point, the algorithm throws its state away and starts again. This is much easier than a sliding window, where old items must leave one by one and the algorithm must find out which ones they are.

## The idea

For a landmark $\ell$, the window at time $t \ge \ell$ is
$$\mathrm{lm}_\ell(t) = \{\, a_i : \ell < \tau_i \le t \,\},$$
or, by positions, $a_{\ell+1}, \ldots, a_t$. The window only grows with $t$. Some systems use a sequence of landmarks $\ell_0 < \ell_1 < \cdots$, and at time $t$ the window starts at the last landmark $\ell_j \le t$.

**Computation.** Between two landmarks the window is an insertion-only stream, the [cash register model](/cash-register-model/). So each insertion-only streaming algorithm computes the function over a landmark window: run it from the landmark, and restart it at the next landmark. The space and the guarantees are those of the insertion-only algorithm. For example, the number of 1s in a landmark window is an exact counter of $\lceil \log_2 (m+1) \rceil$ bits for a window of $m$ items, while the exact count over a [count-based window](/count-based-window/) of size $W$ needs $W$ bits (see [basic counting](/basic-counting/)). The number of distinct values in a landmark window is the [distinct elements problem](/distinct-elements-problem/), solved by [HyperLogLog](/hyperloglog/) and the [KMV sketch](/kmv-sketch/).

**Relation to other windows.**

- A sliding window of size $W$ is a landmark window only while $t \le W$; after that, items expire.
- If the landmarks are $\ell_j = o + js$ and the query is asked only at the end of each period, the landmark windows are the [tumbling windows](/tumbling-window/) of size $s$. If the query is asked at every step inside each period, the window is a cumulative window: it starts at the period start and grows until the period ends.
- [Exponential decay](/exponential-decay/) also keeps all items since a landmark, but gives older items a smaller weight.

## Examples

- Landmark 0 and the bit stream $1, 0, 1, 1, 0, 1$. The count of 1s in the landmark window at times 1 to 6 is $1, 1, 2, 3, 3, 4$. A count-based window of size 4 gives $1, 1, 2, 3, 2, 3$ on the same stream, because the first 1 leaves it at time 5.
- Landmarks at each midnight: "the number of distinct visitors today" is a distinct count over the landmark window that starts at the last midnight. At the next midnight the sketch is reset.
- The maximum since the landmark needs one stored value. Over a sliding window the same question needs a [monotonic deque](/monotonic-deque/) or an approximate structure, see [sliding window maximum](/sliding-window-maximum/).

## Where it is used

- Running totals and statistics "since the start", "since the last reset" or "so far today" in monitoring and in databases of streams.
- Stream processing systems that report a growing window at a fixed step inside each period; Apache Flink SQL has a cumulating window function for this.
- Data mining over streams, where landmark, sliding and damped windows are the three common models, and frequent item and itemset algorithms are stated for each model.

## References
