---
tag: 4SW0BT
kind: concept
slug: tumbling-window
name: Tumbling window
aliases:
- fixed window
- non-overlapping window
area: online-and-streaming/sliding-windows
level: intro
summary: Windows of a fixed size s that cut the time axis into disjoint blocks [o + js, o + (j+1)s), so each item falls in exactly one window.
prereqs: [time-based-window]
see_also: [hopping-window, session-window, landmark-window, time-based-window, count-based-window, sliding-window-model, fixed-window-counter, sliding-window-aggregation]
sources:
  - paper: doi:10.14778/2824032.2824076
    title: Tyler Akidau et al., The Dataflow Model, a practical approach to balancing correctness, latency, and cost in massive-scale, unbounded, out-of-order data processing, PVLDB 8(12), 2015
    locator: Section 1.2 (fixed windows, also called tumbling) and Section 2.2.1 (window assignment)
  - paper: doi:10.1007/s00778-022-00778-6
    title: Juliane Verwiebe, Philipp M. Grulich, Jonas Traub and Volker Markl, Survey of window types for aggregation in stream processing systems, The VLDB Journal 32, 2023
    locator: the section on tumbling windows among the window types
  - url: https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/operators/windows/
    title: Apache Flink documentation, Windows
    locator: Window Assigners, Tumbling Windows (size and offset)
---

A tumbling window of size $s$ cuts the time axis into disjoint blocks of length $s$, and groups the items of a stream by the block that holds their timestamp. Each item falls in exactly one window, and a window closes for good when the time passes its end. The Dataflow model of Akidau et al. (2015) calls these windows fixed windows; Apache Flink and Kafka Streams call them tumbling windows. On this page an item of the stream $\sigma$ is a pair $(\tau, v)$ of a timestamp and a value, $s > 0$ is the window size and $o$ is the offset.

## In plain words

Draw marks on a time line at equal steps, for example at each full hour. Each hour is one window. An item goes into the hour in which it happened, and into no other window. When the clock passes the end of an hour, that hour is complete, and its result can be reported. Then a new hour starts with nothing in it. The windows never overlap and leave no gaps, so each item is counted once. An offset moves all the marks by the same amount, for example to start each day at local midnight instead of at midnight in another time zone.

## The idea

The windows are the half-open intervals
$$T_j = [\,o + js,\; o + (j+1)s\,), \qquad j \in \mathbb{Z}.$$
They are disjoint and their union is the whole time axis, so each timestamp $\tau$ is in exactly one window, the one with index $j = \lfloor (\tau - o)/s \rfloor$.

```pseudo id=main
TUMBLING-ASSIGN(τ, s, o)                ▷ timestamp τ, size s > 0, offset o
L1  j ← ⌊(τ − o)/s⌋
L2  return [o + j·s, o + (j+1)·s)

TUMBLING-SUMS(σ, s, o)                  ▷ σ: pairs (τ, v), τ nondecreasing
L3  cur ← none; acc ← 0
L4  for each (τ, v) in σ do
L5      start ← o + s·⌊(τ − o)/s⌋
L6      if cur ≠ none and start ≠ cur then emit (cur, cur + s, acc); acc ← 0
L7      cur ← start; acc ← acc + v
L8  if cur ≠ none then emit (cur, cur + s, acc)
```

**Computation.** Assignment costs $O(1)$ per item (line L1). When the timestamps do not decrease, at most one window is open at a time, so an aggregate needs the state of one window only: lines L3 to L8 keep one partial sum and emit it when the first item of a later window comes. Empty windows emit nothing. With out-of-order items, a system keeps one partial aggregate for each window that can still receive items, and closes a window when its end passes a watermark, an estimate of the event time that the input has reached.

**Relation to other windows.** A tumbling window is the [hopping window](/hopping-window/) whose hop equals its size; Dataflow states this. It is also a [landmark window](/landmark-window/) whose landmark moves forward by $s$ at each boundary. The [sliding window model](/sliding-window-model/) asks for an answer at every time, and the window moves by one step each time; a tumbling window answers once per block, which is why it needs no expiry and only one running aggregate.

## Examples

- Size $s = 10$ and offset $o = 0$. The timestamps $3, 9, 10, 14, 27$ go to the windows $[0, 10)$, $[0, 10)$, $[10, 20)$, $[10, 20)$ and $[20, 30)$. The timestamp 10 is in $[10, 20)$ and not in $[0, 10)$, because the end of a window is open.
- With the values $1, 2, 3, 4, 5$ for those items, TUMBLING-SUMS emits $(0, 10, 3)$, $(10, 20, 7)$ and $(20, 30, 5)$.
- Size $s = 10$ and offset $o = 3$: the windows are $[3, 13)$, $[13, 23)$ and so on. The timestamp 2 goes to $[-7, 3)$ and the timestamp 13 to $[13, 23)$. Negative timestamps work with the same formula, since $\lfloor \cdot \rfloor$ rounds down: $\tau = -1$ with $o = 0$ goes to $[-10, 0)$.
- The [fixed window counter](/fixed-window-counter/) of a rate limiter is a tumbling window that counts requests.

## Where it is used

- Stream processing systems: fixed windows in Dataflow and Apache Beam, tumbling windows in Apache Flink (with a size and an offset) and in Kafka Streams. These systems use half-open windows $[\text{start}, \text{end})$ aligned to the epoch plus the offset.
- Periodic reports, such as counts per minute, sums per hour and totals per day.
- Rate limiting with fixed periods, and the panes of [hopping windows](/hopping-window/), which are small tumbling windows that the hopping windows combine.

## References
