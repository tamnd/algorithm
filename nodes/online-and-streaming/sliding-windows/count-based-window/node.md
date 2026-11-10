---
tag: 4STCQT
kind: concept
slug: count-based-window
name: Count-based window
aliases:
- sequence-based window
- tuple-based window
- row-based window
area: online-and-streaming/sliding-windows
level: intro
summary: The window that holds the last W items of the stream, whatever their arrival times.
prereqs: [sliding-window-model, queue]
see_also: [time-based-window, sliding-window-model, basic-counting, dgim-algorithm, tumbling-window, hopping-window, sliding-window-aggregation, sliding-window]
sources:
  - paper: doi:10.1137/S0097539701398363
    title: Mayur Datar, Aristides Gionis, Piotr Indyk and Rajeev Motwani, Maintaining stream statistics over sliding windows, SIAM Journal on Computing 31(6), 2002
    locator: the definition of the sliding window of the last N elements, and the remarks on windows defined by timestamps
  - book: isbn:9781107077232
    title: Jure Leskovec, Anand Rajaraman and Jeffrey D. Ullman, Mining of Massive Datasets, second edition, Cambridge University Press, 2014
    locator: Chapter 4, Section 4.6, Counting Ones in a Window
  - paper: doi:10.1007/s00778-022-00778-6
    title: Juliane Verwiebe, Philipp M. Grulich, Jonas Traub and Volker Markl, Survey of window types for aggregation in stream processing systems, The VLDB Journal 32, 2023
    locator: the classification of window measures (count-based and time-based)
---

A count-based window is the part of a stream that holds the last $W$ items, where $W$ is a fixed number. It is the window of the first form of the [sliding window model](/sliding-window-model/), and the one that the [DGIM algorithm](/dgim-algorithm/) uses. The arrival times of the items have no effect on it: one new item always pushes out exactly one old item, once the window is full. On this page $\sigma = a_1, a_2, \ldots$ is the stream and $t$ is the number of items read so far.

## In plain words

Think of a row of a fixed number of seats. Each new item takes the seat at the front, every item moves back by one seat, and the item in the last seat leaves. A question about the window is a question about the items in the seats now. It does not matter if the items came fast or slowly. Because exactly one item leaves at each step, the age of an item tells you when it will leave. That makes count-based windows easier to handle than windows defined by a clock.

## The idea

At time $t$ the count-based window of size $W$ is
$$\mathrm{win}_W(t) = a_{\max(1,\, t-W+1)}, \ldots, a_t .$$

- When $t \ge W$ the window holds exactly $W$ items. When $t < W$ it holds all $t$ items.
- From time $t - 1$ to time $t$, with $t > W$, exactly one item enters ($a_t$) and exactly one item leaves ($a_{t-W}$).
- The item $a_i$ is in the windows of the times $i, i+1, \ldots, i+W-1$, so in exactly $W$ windows if the stream is long enough.
- The age of $a_i$ at time $t$ is $t - i$, and $a_i$ is in the window if and only if $t - i < W$. If the age is known to be less than $W$, the position $i$ can be kept modulo $W$ in $\lceil \log_2 W \rceil$ bits, and the age is $(t - i) \bmod W$.

An exact algorithm can store the window in a circular buffer of $W$ slots, the array form of a [queue](/queue/). The streaming question is how much less memory suffices for a given function. For [basic counting](/basic-counting/), the exact answer needs $W$ bits, and a relative error $\varepsilon$ needs $\Theta(\frac{1}{\varepsilon} \log^2 W)$ bits (DGIM 2002).

## Examples

- With $W = 3$ and the stream $5, 1, 4, 1, 5$, the windows at times 3, 4 and 5 are $(5, 1, 4)$, $(1, 4, 1)$ and $(4, 1, 5)$. Their sums are 10, 6 and 10.
- With $W = 4$ and the bit stream $1, 0, 1, 1, 0, 1$, the number of 1s in the window is 1, 1, 2, 3, 2, 3 at times 1 to 6. At time 6 the window is $1, 1, 0, 1$: the first 1 of the stream has expired.
- A time-based window of $W$ time units with exactly one item at each time step is the same as a count-based window of size $W$. With a variable rate, the two differ; see [time-based window](/time-based-window/).

## Where it is used

- The sliding window model of DGIM and the algorithms on it: [DGIM](/dgim-algorithm/), the [exponential histogram](/exponential-histogram/) and the [smooth histogram](/smooth-histogram/).
- Window functions in SQL, where the frame `ROWS BETWEEN W-1 PRECEDING AND CURRENT ROW` is a count-based window over the ordered rows.
- Moving statistics over the last $W$ samples, such as the [moving average](/moving-average/), and exact window aggregates with the [two-stacks queue](/two-stacks-queue/).
- The [sliding window technique](/sliding-window/) on arrays, where the window is a range of $W$ consecutive indices.

## References
