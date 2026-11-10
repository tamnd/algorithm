---
tag: A6HTEM
kind: model
slug: sliding-window-model
name: Sliding window model
aliases:
- sliding window streaming model
- sliding window model of data streams
area: online-and-streaming/sliding-windows
level: core
summary: A streaming model in which each query asks only about the last W items, or the items of the last W time units, and older items expire.
prereqs: [streaming-model, space-complexity, relative-error]
see_also: [count-based-window, time-based-window, basic-counting, dgim-algorithm, exponential-histogram, smooth-histogram, sliding-window-aggregation, turnstile-model]
sources:
  - paper: doi:10.1137/S0097539701398363
    title: Mayur Datar, Aristides Gionis, Piotr Indyk and Rajeev Motwani, Maintaining stream statistics over sliding windows, SIAM Journal on Computing 31(6), 2002
    locator: the definition of the sliding window model, the basic counting problem, the exponential histogram and the lower bounds
  - paper: doi:10.1137/090749281
    title: Vladimir Braverman and Rafail Ostrovsky, Effective computations on sliding windows, SIAM Journal on Computing 39(6), 2010
    locator: Section 1 (the model and earlier results) and Definition 1 (smooth functions)
  - book: isbn:9781107077232
    title: Jure Leskovec, Anand Rajaraman and Jeffrey D. Ullman, Mining of Massive Datasets, second edition, Cambridge University Press, 2014
    locator: Chapter 4, Section 4.6, Counting Ones in a Window
  - paper: doi:10.1561/0400000002
    title: S. Muthukrishnan, Data Streams, Algorithms and Applications, Foundations and Trends in Theoretical Computer Science 1(2), 2005
    locator: the section on the sliding window model among the stream models
---

The sliding window model is a variant of the [streaming model](/streaming-model/) in which each query is about the most recent part of the stream only: the last $W$ items, or the items that arrived in the last $W$ time units. Items older than the window expire, but the algorithm gets no message when an item expires, and it cannot read the item again. Datar, Gionis, Indyk and Motwani (DGIM) studied the model in 2002 and showed that exact answers often need memory linear in $W$, while answers with [relative error](/relative-error/) $\varepsilon$ need only polylogarithmic memory. On this page $\sigma = a_1, a_2, \ldots$ is the stream, $t$ is the current time, $W$ is the window size, and $n$ is the size of the universe of item values.

## The machine

The algorithm reads the stream $\sigma$ once, in order, one item at a time. The window size $W$ is fixed and known before the first item.

- **Count-based window.** At time $t$ the window is $a_{t-W+1}, \ldots, a_t$, the last $W$ items (all items when $t < W$). See [count-based window](/count-based-window/).
- **Time-based window.** Each item $a_i$ comes with a timestamp $\tau_i$, and $\tau_1 \le \tau_2 \le \cdots$. At time $t$ the window holds the items with $t - W < \tau_i \le t$. Many items can have the same timestamp, and some time steps have no item. See [time-based window](/time-based-window/).

At any time a query asks for a function $f$ of the items in the window, for example the number of 1s, the sum, the number of distinct values or the maximum. A deterministic algorithm must return a value $\hat f$ with $|\hat f - f| \le \varepsilon f$ at each query. A randomized algorithm must do so with probability at least $1 - \delta$ at each query, as in the [(ε, δ) guarantee](/epsilon-delta-guarantee/).

An item leaves the window when $W$ newer items have arrived (count-based) or when $W$ time units have passed (time-based). The algorithm sees no event at that moment. It must detect the expiry itself, from the positions or timestamps that it keeps. This is the main difference from the [turnstile model](/turnstile-model/), where a deletion is an explicit update that names the item.

## What it counts

- **Space**, in bits, as a function of $W$, $\varepsilon$, $\delta$ and the value range ($n$, or $R$ for integer values in $\{0, \ldots, R\}$). The space includes the hash seeds of a randomized algorithm. A position in a count-based window can be kept modulo $W$ in $\lceil \log_2 W \rceil$ bits, because a kept position is always inside the window.
- **Update time**, the work per arriving item, worst case or amortized.
- **Query time**, the work to answer one query.
- **The guarantee**, as a deterministic relative error or as $(\varepsilon, \delta)$.

The trivial solution stores the whole window: $W$ items of $\lceil \log_2 n \rceil$ bits each, in a [queue](/queue/). An algorithm in the model is interesting when its space is $o(W)$, usually polylogarithmic in $W$.

## Relation to other models

- **Insertion-only streams.** The [cash register model](/cash-register-model/) is the case $W = \infty$: no item expires. This is also the [landmark window](/landmark-window/), which starts at a fixed time and grows. Each sliding-window algorithm with $W$ at least the stream length is an insertion-only algorithm, so each lower bound for insertion-only streams also holds here.
- **Turnstile streams.** The sliding window looks like a stream with deletions, since each expiry deletes the oldest item. But the deletion is implicit. A turnstile algorithm can process the expiry only if it gets the expiring item, and to keep the window for that purpose takes $W \lceil \log_2 n \rceil$ bits. So the two models are different. For example, the sum of integers with negative values is exact in $O(\log W + \log R)$ bits in the turnstile model, but needs $\Omega(W)$ bits in the sliding window model.
- **Fixed-block windows.** [Tumbling windows](/tumbling-window/) and [hopping windows](/hopping-window/) cut the stream into blocks that start at fixed times. A tumbling window needs no expiry at all: the algorithm restarts at each block boundary. The sliding window model asks for an answer at every position, which is harder.
- **Decay models.** [Exponential decay](/exponential-decay/) and [forward decay](/forward-decay/) do not drop old items; they give them smaller weights. A sliding window is the decay function that is 1 on the last $W$ items and 0 before.
- **Arrays.** The [sliding window technique](/sliding-window/) for arrays and the [monotonic deque](/monotonic-deque/) keep the items of the window in memory, which uses $\Theta(W)$ words. They solve exact problems such as the [sliding window maximum](/sliding-window-maximum/). The streaming model asks for much less memory and accepts an approximate answer.

## Known results in the model

| Problem | Upper bound | Lower bound | Source |
|---|---|---|---|
| [Basic counting](/basic-counting/), exact | $W$ bits | $W$ bits | proved on the basic counting page |
| Basic counting, relative error $\varepsilon$, deterministic | $O(\frac{1}{\varepsilon} \log^2 W)$ bits | $\Omega(\frac{1}{\varepsilon} \log^2(\varepsilon W))$ bits | DGIM 2002, proved on the [theorem page](/exponential-histogram-bound/) |
| Basic counting, randomized | same | $\Omega(\frac{1}{\varepsilon} \log^2(\varepsilon W))$ bits | DGIM 2002, cited |
| Sum of integers in $\{0, \ldots, R\}$ | $O(\frac{1}{\varepsilon} \log W (\log W + \log R))$ bits | same order | DGIM 2002 |
| Sum of integers with negative values | $O(W \log R)$ bits (store the window) | $\Omega(W)$ bits for each constant factor | DGIM 2002, cited |
| Each $(\alpha, \beta)$-[smooth function](/smooth-function/) with an insertion-only sketch | $O(\frac{1}{\beta} \log W)$ sketches | | Braverman and Ostrovsky 2007, [smooth histogram](/smooth-histogram/) |
| [Distinct count](/sliding-window-distinct-count/) | $O(\frac{1}{\varepsilon^2} \log W \log\frac{1}{\varepsilon} \log\log W + \frac{1}{\varepsilon} \log^2 W)$ bits | $\Omega(\frac{1}{\varepsilon} \log^2 W + \frac{1}{\varepsilon^2} \log W)$ bits | Braverman, Grigorescu, Lang, Woodruff and Zhou 2018, cited |

The [DGIM algorithm](/dgim-algorithm/) reaches the upper bound for basic counting with $O(1)$ amortized and $O(\log W)$ worst-case update time and $O(1)$ query time. The [exponential histogram](/exponential-histogram/) is its general form. For associative aggregates computed exactly over a stored window, the [two-stacks queue](/two-stacks-queue/) and the [DABA queue](/daba-queue/) give $O(1)$ amortized and $O(1)$ worst-case operations; see [sliding-window aggregation](/sliding-window-aggregation/). For samples, see [sliding-window sampling](/sliding-window-sampling/) and [chain sampling](/chain-sampling/).

## References
