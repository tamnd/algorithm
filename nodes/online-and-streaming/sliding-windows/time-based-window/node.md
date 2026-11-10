---
tag: 92SS9F
kind: concept
slug: time-based-window
name: Time-based window
aliases:
- timestamp-based window
- time window
- range-based window
area: online-and-streaming/sliding-windows
level: intro
summary: The window that holds the items whose timestamps are in the last W time units, so the number of items in it varies.
prereqs: [sliding-window-model, count-based-window]
see_also: [count-based-window, sliding-window-model, basic-counting, dgim-algorithm, tumbling-window, hopping-window, session-window, sliding-window-aggregation]
sources:
  - paper: doi:10.1137/S0097539701398363
    title: Mayur Datar, Aristides Gionis, Piotr Indyk and Rajeev Motwani, Maintaining stream statistics over sliding windows, SIAM Journal on Computing 31(6), 2002
    locator: the remarks on windows defined by timestamps, where several elements can arrive at the same time
  - paper: doi:10.14778/2824032.2824076
    title: Tyler Akidau et al., The Dataflow Model, a practical approach to balancing correctness, latency, and cost in massive-scale, unbounded, out-of-order data processing, PVLDB 8(12), 2015
    locator: Section 1.2 (windowing, event time and processing time)
  - paper: doi:10.1007/s00778-022-00778-6
    title: Juliane Verwiebe, Philipp M. Grulich, Jonas Traub and Volker Markl, Survey of window types for aggregation in stream processing systems, The VLDB Journal 32, 2023
    locator: the classification of window measures (count-based and time-based)
---

A time-based window is the part of a stream that holds the items whose timestamps are in the last $W$ time units. It is the second form of the [sliding window model](/sliding-window-model/). Unlike a [count-based window](/count-based-window/), it can hold any number of items, it can be empty, and many items can expire at the same moment. On this page each item $a_i$ of the stream $\sigma$ has a timestamp $\tau_i$, the timestamps do not decrease, and $t$ is the current time.

## In plain words

The window is the last few minutes, not the last few items. When traffic is heavy the window holds many items, and when it is quiet the window holds few or none. Items leave when they become too old, and the clock decides that, not the arrival of new items. If many items arrived in the same second, they all leave in the same later second. So an algorithm cannot plan for one exit per arrival, and its memory must also cope with a window that holds very many items.

## The idea

At time $t$ the time-based window of length $W$ is the set of items
$$\mathrm{win}_W(t) = \{\, a_i : t - W < \tau_i \le t \,\}.$$

- The number of items in the window is not fixed. Let $B$ be an upper bound on it.
- When the clock moves from $t - 1$ to $t$, all items with $\tau_i = t - W$ expire together, and all items with $\tau_i = t$ enter.
- The window is a half-open interval of length $W$ on the time axis. Other conventions, such as $[t - W, t]$, appear in systems; a page or a system must say which one it uses.
- If exactly one item arrives at each time step, the time-based window is a count-based window of size $W$.

**Effect on the bounds.** A count-based window is the special case of a time-based window with one item per time step. So each lower bound for count-based windows, as a function of $W$, also holds for time-based windows. For example, exact [basic counting](/basic-counting/) needs at least $W$ bits. For upper bounds, the count of items in the window is now at most $B$ instead of at most $W$. In the [DGIM algorithm](/dgim-algorithm/) the bucket timestamps still need $\lceil \log_2 W \rceil$ bits each (a time in the window, modulo $W$), but the number of buckets grows with $\log B$, because the bucket sizes must reach the number of 1s in the window. The error proof of DGIM uses only the order of the arrivals, so it holds without change if items with the same timestamp are inserted one at a time. One update can now expire many buckets, so the worst-case update time grows, while the amortized time stays $O(1)$ per item, since each bucket is removed at most once.

## Examples

- Let $W = 3$ and let the timestamps be $1, 1, 2, 5, 5, 6$. The window at time 5 is $(2, 5]$ and holds the two items of time 5. At time 6 it is $(3, 6]$ and holds three items. At time 7 it is $(4, 7]$ and still holds three. At time 8 it is $(5, 8]$: the two items of time 5 expire together, and one item is left. At time 4 the window $(1, 4]$ holds one item, and at time 9 it is empty.
- A rate limiter that allows at most 100 requests in each period of 60 seconds counts the requests in a time-based window of 60 seconds. The [sliding window log](/sliding-window-log/) does this exactly, and the [sliding window counter](/sliding-window-counter/) approximates it with two [fixed window](/fixed-window-counter/) counts.

## Where it is used

- Stream processing systems, where windows are defined in event time or in processing time. The [tumbling](/tumbling-window/), [hopping](/hopping-window/) and [session](/session-window/) windows of Dataflow, Flink and Kafka Streams are time-based.
- Window functions in SQL, where the frame `RANGE BETWEEN INTERVAL ... PRECEDING AND CURRENT ROW` is a time-based window over a timestamp column.
- Network monitoring and rate limiting, where a question is about "the last minute" and the arrival rate is variable.

## References
